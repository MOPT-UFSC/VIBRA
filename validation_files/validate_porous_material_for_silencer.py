import os
from time import time

import matplotlib.pyplot as plt
import numpy as np

from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.postprocessing import AcousticPostprocessing
from vibra.engine.properties.fluid import Fluid
from vibra.engine.solution import HarmonicSolution
from vibra.engine.solvers.harmonic_solver import HarmonicSolver
from vibra.external_mesh.external_mesh_data import ExternalMeshData
from vibra.interface.data_handler.data_importer import DataImporter

pm_model = "DB"


# @pytest.mark.slow
def load_external_mesh_and_solve():
    # return

    # start decoding the Ansys script file (ds.dat file or input file)
    mesh_path = "validation_files/data/WB/porous_material_models/mesh/silencer/ds_silencer_suction_stg1.dat"

    if pm_model not in ["DB", "DBM", "JCA"]:
        return

    if not os.path.exists(mesh_path):
        return

    # define the known 'Named selections' from model
    named_selecion_to_tag = {"input_face": 1, "output_face": 2}

    # define surfaces from each volume
    surfaces_from_volume = {1: [1, 2]}

    t0 = time()
    external_mesh = ExternalMeshData()
    external_mesh.read_file(mesh_path)
    external_mesh.set_named_selections(list(named_selecion_to_tag.keys()))
    external_mesh.decode_mesh_data_from_file()

    dt = time() - t0
    print(f"\nElapsed time to decode the external mesh data: {round(dt, 4)} s")

    mesh = Mesh()
    mesh.import_external_nodal_coordinates(external_mesh.nodal_coordinates, index_zero=True)
    mesh.import_external_faces_connectivity(external_mesh.faces_connectivities, index_zero=True, etype_tag=9)
    mesh.import_external_solids_connectivity(external_mesh.solids_connectivities, index_zero=True, etype_tag=4)
    mesh.map_face_elements_to_solid_elements()
    mesh.map_surfaces_to_volumes(surfaces_from_volume)

    # export the mesh data
    mesh.export_nodal_coordinates("nodal_coordinates.dat")
    mesh.export_solid_elements_connectivity("solids_connectivity.dat")
    mesh.export_face_elements_connectivity("faces_connectivity.dat")

    # Define the fluid properties

    temperature = 298.15
    pressure = 122525

    rho_0 = 2.634167
    c_0 = 225.307464
    mu = 8.156509e-06
    Cp = 1664.133942
    kt = 1.741553e-02
    gamma = 1.120295
    molar_mass = 51.951533

    fluid = Fluid(
        name="Silencer suction stg1",
        identifier=1,
        color=(200, 200, 200),
        pressure=pressure,
        temperature=temperature,
        fluid_density=rho_0,
        speed_of_sound=c_0,
        isentropic_exponent=gamma,
        thermal_conductivity=kt,
        specific_heat_Cp=Cp,
        dynamic_viscosity=mu,
        molar_mass=molar_mass,
    )

    ## intialize the model
    model = Model()
    model.mesh = mesh

    ## assign the created fluid
    for vol_id in [1, 2, 3]:
        model.properties._set_property("fluid", fluid, volume=vol_id)

    model.properties._set_property("fluid", fluid, surface=1)
    model.properties._set_property("fluid", fluid, surface=2)

    # Normal surface velocity data
    data_Vn = {
        "real_values": [1], 
        "imag_values": [0], 
        "element_integration": True, 
        }

    # Impedance data
    Zo = fluid.impedance
    data_Z = {
        "real_values": [Zo],
        "imag_values": [0],
    }

    model.properties._set_property("surface_velocity", data_Vn, surface=1)
    model.properties._set_property("specific_impedance", data_Z, surface=1)
    model.properties._set_property("specific_impedance", data_Z, surface=2)

    # Define the analysis frequency setup
    analysis_setup = model.get_harmonic_analysis_setup(
        analysis_id = AnalysisID.ACOUSTIC_HARMONIC,
        frequency_spacing = FrequencySpacing.EQUALLY_DISTRIBUTED,
        f_min = 5,
        f_max = 1400,
        f_step = 5,
    )

    frequencies = analysis_setup.get_frequencies()

    model.set_analysis_setup(analysis_setup)

    # Configure porous material
    pm_data = get_porous_material_data(model=pm_model)

    # model.properties._set_property("porous_material_model", pm_data, volume=1)
    model.properties._set_property("porous_material_model", pm_data, volume=2)
    model.properties._set_property("porous_material_model", pm_data, volume=3)

    model.process_porous_material_properties()

    # Define and process the assemble
    assembler = AcousticAssembler(model)
    assembler.assemble_global_matrices_and_excitations(print_log=True)

    # Define the analysis type and load setup
    harmonic_solver = HarmonicSolver(assembler)

    # Run harmonic analysis
    t0 = time()
    model.solution = harmonic_solver.solve_direct(print_log=True)
    dt = time() - t0
    print(f"Elapsed time to solve harmonic analysis: {round(dt, 4)}")

    if not isinstance(model.solution, HarmonicSolution):
        return

    t0 = time()
    acoustic_post = AcousticPostprocessing(model)

    input_particle_velocities = acoustic_post.get_particle_velocity_from_surface(1, 1)
    output_particle_velocities = acoustic_post.get_particle_velocity_from_surface(2, 1)

    input_Vx = np.average(input_particle_velocities.Vx_array(), axis=0)
    output_Vx = np.average(output_particle_velocities.Vx_array(), axis=0)

    mesh.process_face_elements_connected_to_nodes([1, 2])
    mesh.compute_nodal_areas()

    freq_TL, TL_model = acoustic_post.compute_transmission_loss(1, 2, surface_integration=False)

    dt = time() - t0
    print(f"Elapsed time to post-process data: {round(dt, 4)}")

    results_path = f"validation_files/data/WB/porous_material_models/results/silencer/WB_results_silencer_{pm_model}_Vn1_Z1_Z2.xlsx"
    imported_results = DataImporter.load_spreadsheet_data_for_validation(results_path)

    pressure_at_input_face = imported_results["input_face_pressure"]
    pressure_at_output_face = imported_results["output_face_pressure"]
    velocity_at_input_face = imported_results["input_face_velocity"]
    velocity_at_output_face = imported_results["output_face_velocity"]
    pressure_at_node_8904 = imported_results["pressure_at_node_8904"]
    pressure_at_node_8817 = imported_results["pressure_at_node_8817"]
    velocity_at_node_8904 = imported_results["velocity_at_node_8904"]
    velocity_at_node_8817 = imported_results["velocity_at_node_8817"]
    TL_data = imported_results["transmission_loss"]  # ports enabled

    output_ns = "output_face"

    if output_ns == "input_face":
        rows = mesh.external_nodes_from_surfaces[1]
        freq_ref = pressure_at_input_face[:, 0]
        results_ref = pressure_at_input_face[:, 1] + 1j * pressure_at_input_face[:, 2]

    else:
        rows = mesh.external_nodes_from_surfaces[2]
        freq_ref = pressure_at_output_face[:, 0]
        results_ref = pressure_at_output_face[:, 1] + 1j * pressure_at_output_face[:, 2]

    nodal_solution = model.solution.nodal_solution
    nodal_solution_face = np.average(nodal_solution[rows, :], axis=0).flatten()

    title = f"Harmonic response at {output_ns}"

    # abs_diff = np.max(np.abs((nodal_solution_face-results_ref)/results_ref))
    # print(f"Deviation: {100*abs_diff}")
    # assert abs_diff < 1e-4

    fig1, ax1 = plt.subplots()
    ax1.semilogy(frequencies, np.abs(nodal_solution_face), "r", label="VIBRA")
    ax1.semilogy(freq_ref, np.abs(results_ref), "k--", label="ANSYS")
    ax1.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Absolute", title=title)
    ax1.grid()
    ax1.legend()

    fig2, ax2 = plt.subplots()
    ax2.plot(frequencies, np.real(nodal_solution_face), "r", label="VIBRA")
    ax2.plot(freq_ref, np.real(results_ref), "k--", label="ANSYS")
    ax2.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Real", title=title)
    ax2.grid()
    ax2.legend()

    fig3, ax3 = plt.subplots()
    ax3.plot(frequencies, np.imag(nodal_solution_face), "r", label="VIBRA")
    ax3.plot(freq_ref, np.imag(results_ref), "k--", label="ANSYS")
    ax3.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Imaginary", title=title)
    ax3.grid()
    ax3.legend()

    # Plot the nodal results for pressure and particle velocity

    data_type = np.real
    type_label = "real"

    x_data_WB = pressure_at_node_8904[:, 0]
    y_data_WB = pressure_at_node_8904[:, 1] + 1j * pressure_at_node_8904[:, 2]

    fig4, ax4 = plt.subplots()
    title = "Acoustic pressure at node 8904"
    ax4.plot(frequencies, data_type(nodal_solution[8904 - 1, :]), "r", label="VIBRA")
    ax4.plot(x_data_WB, data_type(y_data_WB), "k--", label="ANSYS")
    ax4.set_xlabel("Frequency [Hz]")
    ax4.set_ylabel(f"Acoustic Pressure [Pa] - {type_label}")
    ax4.set_title(title)
    ax4.grid()
    ax4.legend()

    x_data_WB = pressure_at_node_8817[:, 0]
    y_data_WB = pressure_at_node_8817[:, 1] + 1j * pressure_at_node_8817[:, 2]

    fig5, ax5 = plt.subplots()
    title = "Acoustic pressure at node 8817"
    ax5.plot(frequencies, data_type(nodal_solution[8817 - 1, :]), "r", label="VIBRA")
    ax5.plot(x_data_WB, data_type(y_data_WB), "k--", label="ANSYS")
    ax5.set_xlabel("Frequency [Hz]")
    ax5.set_ylabel(f"Acoustic Pressure [Pa] - {type_label}")
    ax5.set_title(title)
    ax5.grid()
    ax5.legend()

    x_data_WB = velocity_at_node_8904[:, 0]
    y_data_WB = velocity_at_node_8904[:, 1] + 1j * velocity_at_node_8904[:, 2]

    fig6, ax6 = plt.subplots()
    title = "Particle velocity at node 8904"
    ax6.plot(frequencies, data_type(output_particle_velocities.Vx[8904 - 1]), "r", label="VIBRA")
    ax6.plot(x_data_WB, data_type(y_data_WB), "k--", label="ANSYS")
    ax6.set_xlabel("Frequency [Hz]")
    ax6.set_ylabel(f"Particle velocity [m/s] - {type_label}")
    ax6.set_title(title)
    ax6.grid()
    ax6.legend()

    x_data_WB = velocity_at_node_8817[:, 0]
    y_data_WB = velocity_at_node_8817[:, 1] + 1j * velocity_at_node_8817[:, 2]

    fig7, ax7 = plt.subplots()
    title = "Particle velocity at node 8817"
    ax7.plot(frequencies, data_type(input_particle_velocities.Vx[8817 - 1]), "r", label="VIBRA")
    ax7.plot(x_data_WB, data_type(y_data_WB), "k--", label="ANSYS")
    ax7.set_xlabel("Frequency [Hz]")
    ax7.set_ylabel(f"Particle velocity [m/s] - {type_label}")
    ax7.set_title(title)
    ax7.grid()
    ax7.legend()

    x_data_WB = velocity_at_input_face[:, 0]
    y_data_WB = velocity_at_input_face[:, 1] + 1j * velocity_at_input_face[:, 2]

    fig8, ax8 = plt.subplots()
    title = "Input face particle velocity - average"
    ax8.plot(frequencies, data_type(input_Vx), "r", label="VIBRA")
    ax8.plot(x_data_WB, data_type(y_data_WB), "k--", label="ANSYS")
    ax8.set_xlabel("Frequency [Hz]")
    ax8.set_ylabel(f"Particle velocity [m/s] - {type_label}")
    ax8.set_title(title)
    ax8.grid()
    ax8.legend()

    x_data_WB = velocity_at_output_face[:, 0]
    y_data_WB = velocity_at_output_face[:, 1] + 1j * velocity_at_output_face[:, 2]

    fig9, ax9 = plt.subplots()
    title = "Output face particle velocity - average"
    ax9.plot(frequencies, data_type(output_Vx), "r", label="VIBRA")
    ax9.plot(x_data_WB, data_type(y_data_WB), "k--", label="ANSYS")
    ax9.set_xlabel("Frequency [Hz]")
    ax9.set_ylabel(f"Particle velocity [m/s] - {type_label}")
    ax9.set_title(title)
    ax9.grid()
    ax9.legend()

    # Sound intensity at input face node

    x_data_WB = velocity_at_node_8817[:, 0]
    Vx_8817_WB = velocity_at_node_8817[:, 1] + 1j * velocity_at_node_8817[:, 2]
    P_8817_WB = pressure_at_node_8817[:, 1] + 1j * pressure_at_node_8817[:, 2]

    sound_int = np.real(nodal_solution[8817 - 1, :] * np.conj(input_particle_velocities.Vx[8817 - 1])) / 2
    y_data_WB = np.real(P_8817_WB * np.conj(Vx_8817_WB)) / 2

    fig10, ax10 = plt.subplots()
    title = "Sound intensity at node 8817"
    ax10.plot(frequencies, sound_int, "r", label="VIBRA")
    ax10.plot(x_data_WB, y_data_WB, "k--", label="ANSYS")
    ax10.set_xlabel("Frequency [Hz]")
    ax10.set_ylabel(f"Sound intensity [Pa.m/s] - {type_label}")
    ax10.set_title(title)
    ax10.grid()
    ax10.legend()

    # Sound intensity at output face node

    x_data_WB = velocity_at_node_8904[:, 0]
    Vx_8904_WB = velocity_at_node_8904[:, 1] + 1j * velocity_at_node_8904[:, 2]
    P_8904_WB = pressure_at_node_8904[:, 1] + 1j * pressure_at_node_8904[:, 2]

    sound_int = np.real(nodal_solution[8904 - 1, :] * np.conj(output_particle_velocities.Vx[8904 - 1])) / 2
    y_data_WB = np.real(P_8904_WB * np.conj(Vx_8904_WB)) / 2

    fig11, ax11 = plt.subplots()
    title = "Sound intensity at node 8904"
    ax11.plot(frequencies, sound_int, "r", label="VIBRA")
    ax11.plot(x_data_WB, y_data_WB, "k--", label="ANSYS")
    ax11.set_xlabel("Frequency [Hz]")
    ax11.set_ylabel(f"Sound intensity [Pa.m/s] - {type_label}")
    ax11.set_title(title)
    ax11.grid()
    ax11.legend()

    fig12, ax12 = plt.subplots()
    title = "Transmission loss"
    x_data_WB = TL_data[:, 0]
    y_data_WB = TL_data[:, 1]
    ax12.plot(freq_TL, TL_model, "r", label="VIBRA")
    ax12.plot(x_data_WB, data_type(y_data_WB), "k--", label="ANSYS")
    ax12.set_xlabel("Frequency [Hz]")
    ax12.set_ylabel(f"Transmission loss [dB] - {type_label}")
    ax12.set_title(title)
    ax12.grid()
    ax12.legend()

    plt.show()


def get_porous_material_data(model="DB"):

    if model == "DB":
        material_model_data = {
            "model": "Delany-Bazley",
            "C1": 0.0858,
            "C2": 0.700,
            "C3": 0.169,
            "C4": 0.595,
            "C5": 0.0497,
            "C6": 0.754,
            "C7": 0.0758,
            "C8": 0.732,
            "flow_resistivity": 1518.5066,
        }

    if model == "DBM":
        material_model_data = {
            "model": "Delany-Bazley-Miki",
            "C1": 0.1090,
            "C2": 0.618,
            "C3": 0.1600,
            "C4": 0.618,
            "C5": 0.070,
            "C6": 0.632,
            "C7": 0.1070,
            "C8": 0.632,
            "flow_resistivity": 1518.5066,
        }

    elif model == "JCA":
        material_model_data = {
            "model": "Jhonson-Champoux-Allard",
            "porosity": 0.9,
            "tortuosity": 1.0,
            "viscous_characteristic_length": 77e-6,
            "thermal_characteristic_length": 159e-6,
            "flow_resistivity": 1518.5066,
        }
    elif model == "JCAL":
        material_model_data = {
            "model": "Jhonson-Champoux-Allard-Lafarge",
            "porosity": 0.9,
            "tortuosity": 1.0,
            "viscous_characteristic_length": 77e-6,
            "thermal_characteristic_length": 159e-6,
            "flow_resistivity": 1518.5066,
        }

    return material_model_data


if __name__ == "__main__":
    load_external_mesh_and_solve()
