from typing import TYPE_CHECKING

from validation_files.data.WB.load_external_data import LoadExternalData
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.postprocessing import AcousticPostprocessing
from vibra.engine.properties.fluid import Fluid
from vibra.engine.solution import HarmonicSolution
from vibra.engine.solvers.harmonic_solver import HarmonicSolver
from vibra.external_mesh.external_mesh_data import ExternalMeshData
from vibra.interface.user_input.data_handler.file_handlers.file_handler import FileHandler

if TYPE_CHECKING:
    from vibra.engine.model import Model

import os
from time import time

# import pytest
import matplotlib.pyplot as plt
import numpy as np

pm_model = "DB"


def load_external_mesh_and_solve():
    # return

    # start decoding the Ansys script file (ds.dat file or input file)
    # mesh_path = "validation_files/data/WB/porous_material_models/mesh/silencer/ds_only_fluid_of_silencer_suction_stg1.dat"
    mesh_path = "validation_files/data/WB/transmission_loss/mesh/silencer/ds_only_fluid_of_silencer_suction_stg1.dat"

    if pm_model not in ["DB", "DBM", "JCA"]:
        return

    if not os.path.exists(mesh_path):
        return

    # define the known 'Named selections' from model
    named_selecion_to_tag = {
        "input_face": 1,
        "output_face": 2,
        "input_connected_faces": 3,
        "output_connected_faces": 4,
    }

    # define surfaces from each volume
    surfaces_from_volume = {1: [1, 2, 3, 4]}

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

    # Load the external data
    path = "validation_files/data/WB/transmission_loss/results/Zo_real"
    # path = "validation_files/data/WB/transmission_loss/results/Zo_complex"
    ext_data = LoadExternalData(path, fluid_density=rho_0)

    ## intialize the model
    model = Model()
    model.mesh = mesh

    ## assign the created fluid
    for vol_id in [1]:
        model.properties._set_property("fluid", fluid, volume=vol_id)

    model.properties._set_property("fluid", fluid, surface=1)
    model.properties._set_property("fluid", fluid, surface=2)

    # Normal surface velocity data
    data_Vn = {
        "real_values": [1],
        "imag_values": [0],
        "nodal_attribution": False,
        "averaged": False,
    }

    # Impedance data - constant value
    data_Z = {
        "real_values": [fluid.impedance],
        "imag_values": [0],
    }

    ## Impedance data - table of values

    # fluid_data_path = f"validation_files/data/WB/porous_material_models/results/silencer/complex_fluid_properties_DB_model.xlsx"
    # complex_fluid_data = DataImporter.load_spreadsheet_data_for_validation(fluid_data_path)
    # impedance_data = complex_fluid_data["complex_impedance"]

    # data_Z = {"values" : [impedance_data[:, 1] + 1j * impedance_data[:, 2]]}

    # data_Z = {
    #           "anechoic_termination": True,
    #           "volume_id": 1
    #           }

    model.properties._set_property("surface_velocity", data_Vn, surface=1)
    model.properties._set_property("specific_impedance", data_Z, surface=1)
    model.properties._set_property("specific_impedance", data_Z, surface=2)

    # Define the analysis frequency setup
    analysis_setup = model.get_harmonic_analysis_setup(
        frequency_spacing = FrequencySpacing.EQUALLY_DISTRIBUTED,
        analysis_id = AnalysisID.ACOUSTIC_HARMONIC,
        analysis_method = "direct",
        f_min = 5,
        f_max = 1400,
        f_step = 5,
    )

    frequencies = analysis_setup.get_frequencies()

    model.set_analysis_setup(analysis_setup)

    ## Configure porous material
    # pm_data = get_porous_material_data(model=pm_model)
    # model.properties._set_property("porous_material_model", pm_data, volume=1)
    # model.process_porous_material_properties()

    assembler = AcousticAssembler(model)

    # Set the analysis frequency setup
    assembler.assemble_global_matrices_and_excitations()

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
    acoustic_post = AcousticPostprocessing(model=model)

    input_particle_velocities = acoustic_post.get_particle_velocity_from_surface(1, volume_id=1)
    output_particle_velocities = acoustic_post.get_particle_velocity_from_surface(2, volume_id=1)

    input_Vx = np.average(input_particle_velocities.Vx_array(), axis=0)
    output_Vx = np.average(output_particle_velocities.Vx_array(), axis=0)

    mesh.process_face_elements_connected_to_nodes([1, 2])
    mesh.compute_nodal_areas()

    freq_TL, TL_model = acoustic_post.compute_transmission_loss(1, 2, surface_integration=False)

    # mask = TL_model <= 0
    # TL_model[mask] = np.zeros(sum(mask), dtype=float)

    dt = time() - t0
    print(f"Elapsed time to post-process data: {round(dt, 4)}")

    ## load external results data
    # results_path = f"validation_files/data/WB/transmission_loss/results/WB_results_silencer_only_fluid_{pm_model}_Vn1_Z1_Z2_complex.xlsx"
    # results_path = f"validation_files/data/WB/transmission_loss/results/WB_results_silencer_only_fluid_{pm_model}_Vn1_Z1_Z2_real.xlsx"
    # results_path = f"validation_files/data/WB/transmission_loss/results/WB_results_silencer_only_fluid_Vn1_Z1_Z2_complex.xlsx"
    results_path = "validation_files/data/WB/transmission_loss/results/WB_results_silencer_only_fluid_Vn1_Z1_Z2_real.xlsx"

    imported_results = FileHandler.read(results_path).to_dict()

    TL_data = imported_results["transmission_loss"]  # ports enabled

    WB_pressure_data = ext_data.load_nodal_pressures()
    WB_particle_velocities_data = ext_data.load_particle_velocities()
    # WB_nodal_area_data = load_nodal_area()

    # _, nodal_area_input = WB_nodal_area_data["input_face"]
    # _, nodal_area_output = WB_nodal_area_data["output_face"]

    # NA_in = np.array(list(nodal_area_input.values()), dtype=float).reshape(-1, 1)
    # NA_out = np.array(list(nodal_area_output.values()), dtype=float).reshape(-1, 1)

    # print(np.max(np.abs(NA_in-Aef_in)))
    # print(np.max(np.abs(NA_out-Aef_out)))

    freq_WB, _, input_velocities_WB = WB_particle_velocities_data["Vx", "input_face"]
    input_velocity_WB = np.average(list(input_velocities_WB.values()), axis=0)

    freq_WB, _, input_pressures_WB = WB_pressure_data["input_face"]
    input_pressure_WB = np.average(list(input_pressures_WB.values()), axis=0)

    freq_WB, _, output_velocities_WB = WB_particle_velocities_data["Vx", "output_face"]
    output_velocity_WB = np.average(list(output_velocities_WB.values()), axis=0)

    freq_WB, _, output_pressures_WB = WB_pressure_data["output_face"]
    output_pressure_WB = np.average(list(output_pressures_WB.values()), axis=0)

    # nodes from surfaces
    input_rows = mesh.external_nodes_from_surfaces[1]
    output_rows = mesh.external_nodes_from_surfaces[2]

    # load model results
    nodal_solution = model.solution.nodal_solution

    input_pressure = np.average(nodal_solution[input_rows, :], axis=0).flatten()
    output_pressure = np.average(nodal_solution[output_rows, :], axis=0).flatten()

    # Print the nodal results deviations

    abs_diff_node_6463 = np.abs((input_pressures_WB[6463] - nodal_solution[6463 - 1, :]) / (input_pressures_WB[6463]))
    print(f"\nDeviation of pressure (node 6463): {100 * np.max(abs_diff_node_6463)} %")

    abs_diff_node_6531 = np.abs((output_pressures_WB[6531] - nodal_solution[6531 - 1, :]) / (output_pressures_WB[6531]))
    print(f"Deviation of pressure (node 6531): {100 * np.max(abs_diff_node_6531)} %")

    abs_diff_node_6463 = np.abs((input_velocities_WB[6463] - input_particle_velocities.Vx[6463 - 1]) / (input_velocities_WB[6463]))
    print(f"Deviation of particle velocity (node 6463): {100 * np.max(abs_diff_node_6463)} %")

    abs_diff_node_6531 = np.abs((output_velocities_WB[6531] - output_particle_velocities.Vx[6531 - 1]) / (output_velocities_WB[6531]))
    print(f"Deviation of particle velocity (node 6531): {100 * np.max(abs_diff_node_6531)} %")

    abs_diff_input_face = np.abs((input_pressure - input_pressure_WB) / input_pressure_WB)
    print(f"Deviation (input face): {100 * np.max(abs_diff_input_face)} %")

    abs_diff_output_face = np.abs((output_pressure - output_pressure_WB) / output_pressure_WB)
    print(f"Deviation (output face): {100 * np.max(abs_diff_output_face)} %")

    # assert abs_diff < 1e-4

    title = "Harmonic response at input face"

    fig1, ax1 = plt.subplots()
    ax1.semilogy(frequencies, np.abs(input_pressure), "r", label="VIBRA")
    ax1.semilogy(freq_WB, np.abs(input_pressure_WB), "k--", label="ANSYS")
    ax1.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Absolute", title=title)
    ax1.grid()
    ax1.legend()

    fig2, ax2 = plt.subplots()
    ax2.plot(frequencies, np.real(input_pressure), "r", label="VIBRA")
    ax2.plot(freq_WB, np.real(input_pressure_WB), "k--", label="ANSYS")
    ax2.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Real", title=title)
    ax2.grid()
    ax2.legend()

    fig3, ax3 = plt.subplots()
    ax3.plot(frequencies, np.imag(input_pressure), "r", label="VIBRA")
    ax3.plot(freq_WB, np.imag(input_pressure_WB), "k--", label="ANSYS")
    ax3.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Imaginary", title=title)
    ax3.grid()
    ax3.legend()

    title = "Harmonic response at output face"

    fig4, ax4 = plt.subplots()
    ax4.semilogy(frequencies, np.abs(output_pressure), "r", label="VIBRA")
    ax4.semilogy(freq_WB, np.abs(output_pressure_WB), "k--", label="ANSYS")
    ax4.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Absolute", title=title)
    ax4.grid()
    ax4.legend()

    fig5, ax5 = plt.subplots()
    ax5.plot(frequencies, np.real(output_pressure), "r", label="VIBRA")
    ax5.plot(freq_WB, np.real(output_pressure_WB), "k--", label="ANSYS")
    ax5.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Real", title=title)
    ax5.grid()
    ax5.legend()

    fig6, ax6 = plt.subplots()
    ax6.plot(frequencies, np.imag(output_pressure), "r", label="VIBRA")
    ax6.plot(freq_WB, np.imag(output_pressure_WB), "k--", label="ANSYS")
    ax6.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Imaginary", title=title)
    ax6.grid()
    ax6.legend()

    # Plot the nodal results for pressure and particle velocity

    data_type = np.abs
    type_label = "absolute"

    fig7, ax7 = plt.subplots()
    title = "Acoustic pressure at node 6463"
    ax7.plot(frequencies, data_type(nodal_solution[6463 - 1, :]), "r", label="VIBRA")
    ax7.plot(freq_WB, data_type(input_pressures_WB[6463]), "k--", label="ANSYS")
    ax7.set_xlabel("Frequency [Hz]")
    ax7.set_ylabel(f"Acoustic Pressure [Pa] - {type_label}")
    ax7.set_title(title)
    ax7.grid()
    ax7.legend()

    fig8, ax8 = plt.subplots()
    title = "Acoustic pressure at node 6531"
    ax8.plot(frequencies, data_type(nodal_solution[6531 - 1, :]), "r", label="VIBRA")
    ax8.plot(freq_WB, data_type(output_pressures_WB[6531]), "k--", label="ANSYS")
    ax8.set_xlabel("Frequency [Hz]")
    ax8.set_ylabel(f"Acoustic Pressure [Pa] - {type_label}")
    ax8.set_title(title)
    ax8.grid()
    ax8.legend()

    fig9, ax9 = plt.subplots()
    title = "Particle velocity at node 6463"
    ax9.plot(frequencies, data_type(input_particle_velocities.Vx[6463 - 1]), "r", label="VIBRA")
    ax9.plot(freq_WB, data_type(input_velocities_WB[6463]), "k--", label="ANSYS")
    ax9.set_xlabel("Frequency [Hz]")
    ax9.set_ylabel(f"Particle velocity [m/s] - {type_label}")
    ax9.set_title(title)
    ax9.grid()
    ax9.legend()

    fig10, ax10 = plt.subplots()
    title = "Particle velocity at node 6531"
    ax10.plot(frequencies, data_type(output_particle_velocities.Vx[6531 - 1]), "r", label="VIBRA")
    ax10.plot(freq_WB, data_type(output_velocities_WB[6531]), "k--", label="ANSYS")
    ax10.set_xlabel("Frequency [Hz]")
    ax10.set_ylabel(f"Particle velocity [m/s] - {type_label}")
    ax10.set_title(title)
    ax10.grid()
    ax10.legend()

    fig11, ax11 = plt.subplots()
    title = "Input face particle velocity - average"
    ax11.plot(frequencies, data_type(input_Vx), "r", label="VIBRA")
    ax11.plot(freq_WB, data_type(input_velocity_WB), "k--", label="ANSYS")
    ax11.set_xlabel("Frequency [Hz]")
    ax11.set_ylabel(f"Particle velocity [m/s] - {type_label}")
    ax11.set_title(title)
    ax11.grid()
    ax11.legend()

    fig12, ax12 = plt.subplots()
    title = "Output face particle velocity - average"
    ax12.plot(frequencies, data_type(output_Vx), "r", label="VIBRA")
    ax12.plot(freq_WB, data_type(output_velocity_WB), "k--", label="ANSYS")
    ax12.set_xlabel("Frequency [Hz]")
    ax12.set_ylabel(f"Particle velocity [m/s] - {type_label}")
    ax12.set_title(title)
    ax12.grid()
    ax12.legend()

    # Transmission loss

    freq_WB_evaluated, TL_WB_evaluated = process_external_TL(model, ext_data)

    mask = TL_data[:, 0] <= analysis_setup.f_max
    freq_WB_direct = TL_data[:, 0][mask]
    TL_WB_direct = TL_data[:, 1][mask]

    # x_data = freq_WB_direct
    # y_data = np.abs(TL_WB_evaluated - TL_model)
    # ind = np.argmax(y_data)

    # print(x_data[ind], np.max(y_data))
    # print(np.array([x_data, y_data]).T)

    fig13, ax13 = plt.subplots()
    title = "Transmission loss"
    ax13.plot(freq_TL, TL_model, "r", label="VIBRA")
    ax13.plot(freq_WB_direct, TL_WB_direct, "k--", label="ANSYS")
    ax13.plot(freq_WB_evaluated, TL_WB_evaluated, "b--", label="ANSYS (ext.)")
    ax13.set_xlabel("Frequency [Hz]")
    ax13.set_ylabel("Transmission loss [dB]")
    ax13.set_title(title)
    ax13.grid()
    ax13.legend()

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


def process_external_TL(model: "Model", ext_data: LoadExternalData):

    input_surface_id = 1
    # output_surface_id = 2

    # A_in = model.mesh.surface_area_from_element_integration[input_surface_id]
    # A_out = model.mesh.surface_area_from_element_integration[output_surface_id]

    WB_nodal_area_data = ext_data.load_nodal_area()
    WB_pressure_data = ext_data.load_nodal_pressures()
    WB_particle_velocity_data = ext_data.load_particle_velocities()

    _, nodal_area_input = WB_nodal_area_data["input_face"]
    _, nodal_area_output = WB_nodal_area_data["output_face"]

    freq_WB, _, pressures_input = WB_pressure_data["input_face"]
    freq_WB, _, pressures_output = WB_pressure_data["output_face"]

    freq_WB, _, particle_velocity_input = WB_particle_velocity_data["Vx", "input_face"]
    freq_WB, _, particle_velocity_output = WB_particle_velocity_data["Vx", "output_face"]

    keys_na_in = list(nodal_area_input.keys())
    keys_pr_in = list(pressures_input.keys())
    keys_pv_in = list(particle_velocity_input.keys())

    keys_na_out = list(nodal_area_output.keys())
    keys_pr_out = list(pressures_output.keys())
    keys_pv_out = list(particle_velocity_output.keys())

    if (keys_na_in == keys_pr_in == keys_pv_in) and (keys_na_out == keys_pr_out == keys_pv_out):
        surf_velocity = model.properties._get_property("surface_velocity", surface=input_surface_id)
        if isinstance(surf_velocity, dict):
            if "real_values" in surf_velocity.keys():
                real_values = np.array(surf_velocity["real_values"])
                imag_values = np.array(surf_velocity["imag_values"])
                V_in = real_values + 1j * imag_values
            else:
                return None, None

        specific_impedance = model.properties._get_property("specific_impedance", surface=input_surface_id)
        anechoic_termination = model.properties._get_property("anechoic_termination", surface=input_surface_id)

        if isinstance(specific_impedance, dict):
            if "real_values" in specific_impedance.keys():
                real_values = np.array(specific_impedance["real_values"])
                imag_values = np.array(specific_impedance["imag_values"])
                Zo_in = real_values + 1j * imag_values

            elif "anechoic_termination" in specific_impedance.keys():
                rho_eff_pm, C_eff_pm = model.get_porous_material_model_effective_properties(input_surface_id)
                rho_eff_tv, C_eff_tv = model.get_viscous_thermal_model_effective_properties(input_surface_id)

                if isinstance(rho_eff_pm, np.ndarray):
                    density = rho_eff_pm
                    speed_of_sound = C_eff_pm

                elif isinstance(rho_eff_tv, np.ndarray):
                    density = rho_eff_tv
                    speed_of_sound = C_eff_tv

                else:
                    fluid = model.properties._get_property("fluid", surface=input_surface_id)
                    density = fluid.fluid_density
                    speed_of_sound = fluid.speed_of_sound

                Zo_in = density * speed_of_sound

            else:
                Zo_in = specific_impedance["values"]

        elif isinstance(anechoic_termination, dict):

            rho_eff_pm, C_eff_pm = model.get_porous_material_model_effective_properties(input_surface_id)
            rho_eff_tv, C_eff_tv = model.get_viscous_thermal_model_effective_properties(input_surface_id)

            if isinstance(rho_eff_pm, np.ndarray):
                density = rho_eff_pm
                speed_of_sound = C_eff_pm

            elif isinstance(rho_eff_tv, np.ndarray):
                density = rho_eff_tv
                speed_of_sound = C_eff_tv

            else:
                fluid: Fluid = model.properties._get_property("fluid", surface=input_surface_id)
                density = fluid.fluid_density
                speed_of_sound = fluid.speed_of_sound

            Zo_in = density * speed_of_sound

        else:
            return 0, 0

        P_downstream = V_in * Zo_in / 2
        V_downstream = P_downstream / Zo_in

        # P_in = np.array(list(pressures_input.values()), dtype=complex)
        # Vx_in = -np.array(list(particle_velocity_input.values()), dtype=complex)

        # P_downstream = (P_in + Zo_in * Vx_in) / 2
        # V_downstream = P_downstream / Zo_in

        I_in = np.real(P_downstream * np.conjugate(V_downstream)) / 2
        NA_in = np.array(list(nodal_area_input.values()), dtype=float).reshape(-1, 1)

        P_out = np.array(list(pressures_output.values()), dtype=complex)
        Vx_out = -np.array(list(particle_velocity_output.values()), dtype=complex)

        I_out = np.real(P_out * np.conjugate(Vx_out)) / 2
        NA_out = np.array(list(nodal_area_output.values()), dtype=float).reshape(-1, 1)

        W_in = 10 * np.log10(np.sum(I_in * NA_in, axis=0) / 1e-12)
        W_out = 10 * np.log10(np.sum(I_out * NA_out, axis=0) / 1e-12)

        # print(f"Incident power: {W_in}[dB]")

        TL = W_in - W_out

        return freq_WB, TL


if __name__ == "__main__":
    load_external_mesh_and_solve()
