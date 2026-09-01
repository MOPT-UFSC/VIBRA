import os
from time import time

import matplotlib.pyplot as plt
import numpy as np

from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.assemblers.acoustic.acoustic_assembler import AcousticAssembler
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.postprocessing import AcousticPostprocessing
from vibra.engine.properties.fluid import Fluid
from vibra.engine.solution import HarmonicSolution
from vibra.engine.solvers.harmonic_solver import HarmonicSolver
from vibra.external_mesh.external_mesh_data import ExternalMeshData
from vibra.interface.data_handler.data_importer import DataImporter


def load_external_mesh_and_solve():

    # start decoding the Ansys script file (ds.dat file or input file)
    mesh_path = "validation_files/data/WB/viscous_thermal_loss/mesh/ds_viscous_thermal_reference_geometry.dat"

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

    # Define the fluid properties

    temperature = 293.15
    pressure = 101325

    rho_0 = 1.204263
    c_0 = 343.395034
    mu = 1.8247e-05
    Cp = 1006.400178
    kt = 2.5503e-02
    gamma = 1.401985
    molar_mass = 28.958601

    fluid = Fluid(
        name="Air std",
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
    for vol_id in [1, 2, 3, 4, 5]:
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

    ## Define the analysis frequency setup
    analysis_setup = model.get_harmonic_analysis_setup(
        frequency_spacing = FrequencySpacing.EQUALLY_DISTRIBUTED,
        analysis_id = AnalysisID.ACOUSTIC_HARMONIC,
        f_min = 5,
        f_max = 1600,
        f_step = 5,
    )

    frequencies = analysis_setup.get_frequencies()

    model.set_analysis_setup(analysis_setup)

    # Configure the viscous-thermal models

    narrow_slit_duct_data = get_viscous_thermal_model_data_for_narrow_slit_duct(0.003)
    model.set_viscous_thermal_model_data(narrow_slit_duct_data, volume=1)

    # rectangular_duct_data = get_viscous_thermal_model_data_for_rectangular_duct(0.03, 0.003, 200)
    # model.set_viscous_thermal_model_data(rectangular_duct_data, volume=1)

    major_duct_data = get_viscous_thermal_model_data_for_circular_duct(0.016)
    model.set_viscous_thermal_model_data(major_duct_data, volume=2)
    model.set_viscous_thermal_model_data(major_duct_data, volume=3)

    minor_duct_data = get_viscous_thermal_model_data_for_circular_duct(0.004)
    model.set_viscous_thermal_model_data(minor_duct_data, volume=4)
    model.set_viscous_thermal_model_data(minor_duct_data, volume=5)

    model.process_viscous_thermal_model_properties()

    assembler = AcousticAssembler(model)

    # Set the analysis frequency setup
    assembler.assemble_global_matrices_and_excitations(print_log=True)

    # Define the analysis type and load setup
    harmonic_solver = HarmonicSolver(assembler)

    # Run harmonic analysis

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

    results_path = "validation_files/data/WB/viscous_thermal_loss/results/circular_and_narrow_slit_ducts_results.xlsx"
    # results_path = f"validation_files/data/WB/viscous_thermal_loss/results/circular_and_rectangular_ducts_results.xlsx"
    # results_path = f"validation_files/data/WB/viscous_thermal_loss/results/circular_ducts_results.xlsx"
    # results_path = f"validation_files/data/WB/viscous_thermal_loss/results/only_fluid_results.xlsx"

    imported_results = DataImporter.load_spreadsheet_data_for_validation(results_path)

    pressure_at_input_face = imported_results["input_pressure"]
    pressure_at_output_face = imported_results["output_pressure"]
    velocity_at_input_face = imported_results["input_velocity_Vx"]
    velocity_at_output_face = imported_results["output_velocity_Vx"]
    pressure_at_node_4885 = imported_results["pressure_at_node_4885"]
    pressure_at_node_4978 = imported_results["pressure_at_node_4978"]
    velocity_at_node_4885 = imported_results["velocity_Vx_at_node_4885"]
    velocity_at_node_4978 = imported_results["velocity_Vx_at_node_4978"]
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

    x_data_WB = pressure_at_node_4885[:, 0]
    y_data_WB = pressure_at_node_4885[:, 1] + 1j * pressure_at_node_4885[:, 2]

    fig4, ax4 = plt.subplots()
    title = "Acoustic pressure at node 4885"
    ax4.plot(frequencies, data_type(nodal_solution[4885 - 1, :]), "r", label="VIBRA")
    ax4.plot(x_data_WB, data_type(y_data_WB), "k--", label="ANSYS")
    ax4.set_xlabel("Frequency [Hz]")
    ax4.set_ylabel(f"Acoustic Pressure [Pa] - {type_label}")
    ax4.set_title(title)
    ax4.grid()
    ax4.legend()

    x_data_WB = pressure_at_node_4978[:, 0]
    y_data_WB = pressure_at_node_4978[:, 1] + 1j * pressure_at_node_4978[:, 2]

    fig5, ax5 = plt.subplots()
    title = "Acoustic pressure at node 4978"
    ax5.plot(frequencies, data_type(nodal_solution[4978 - 1, :]), "r", label="VIBRA")
    ax5.plot(x_data_WB, data_type(y_data_WB), "k--", label="ANSYS")
    ax5.set_xlabel("Frequency [Hz]")
    ax5.set_ylabel(f"Acoustic Pressure [Pa] - {type_label}")
    ax5.set_title(title)
    ax5.grid()
    ax5.legend()

    x_data_WB = velocity_at_node_4885[:, 0]
    y_data_WB = velocity_at_node_4885[:, 1] + 1j * velocity_at_node_4885[:, 2]

    fig6, ax6 = plt.subplots()
    title = "Particle velocity at node 4885"
    ax6.plot(frequencies, data_type(input_particle_velocities.Vx[4885 - 1]), "r", label="VIBRA")
    ax6.plot(x_data_WB, data_type(y_data_WB), "k--", label="ANSYS")
    ax6.set_xlabel("Frequency [Hz]")
    ax6.set_ylabel(f"Particle velocity [m/s] - {type_label}")
    ax6.set_title(title)
    ax6.grid()
    ax6.legend()

    x_data_WB = velocity_at_node_4978[:, 0]
    y_data_WB = velocity_at_node_4978[:, 1] + 1j * velocity_at_node_4978[:, 2]

    fig7, ax7 = plt.subplots()
    title = "Particle velocity at node 4978"
    ax7.plot(frequencies, data_type(output_particle_velocities.Vx[4978 - 1]), "r", label="VIBRA")
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

    # Plot the transmission loss between input and output faces

    fig10, ax10 = plt.subplots()
    title = "Transmission loss"
    x_data_WB = TL_data[:, 0]
    y_data_WB = TL_data[:, 1]
    ax10.plot(freq_TL, TL_model, "r", label="VIBRA")
    ax10.plot(x_data_WB, data_type(y_data_WB), "k--", label="ANSYS")
    ax10.set_xlabel("Frequency [Hz]")
    ax10.set_ylabel(f"Transmission loss [dB] - {type_label}")
    ax10.set_title(title)
    ax10.grid()
    ax10.legend()

    plt.show()


def get_viscous_thermal_model_data_for_circular_duct(diameter: float):

    data = {"formulation": "LRF model", "section_type": "Circular duct", "diameter": diameter}

    return data


def get_viscous_thermal_model_data_for_rectangular_duct(width: float, height: float, number_of_terms: int):

    data = {"formulation": "Stinson model", "section_type": "Rectangular duct", "width": width, "height": height, "number_of_terms": number_of_terms}

    return data


def get_viscous_thermal_model_data_for_narrow_slit_duct(height: float):

    data = {"formulation": "Stinson model", "section_type": "Narrow slit duct", "height": height}

    return data


if __name__ == "__main__":
    load_external_mesh_and_solve()
