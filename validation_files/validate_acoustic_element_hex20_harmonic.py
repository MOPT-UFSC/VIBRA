from typing import TYPE_CHECKING

from validation_files.data.WB.load_external_data import LoadExternalData
from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.assemblers.acoustic.acoustic_assembler import AcousticAssembler
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.postprocessing.acoustic_postprocessing import AcousticPostprocessing
from vibra.engine.properties.fluid import Fluid
from vibra.engine.solvers.harmonic_solver import HarmonicSolver
from vibra.external_mesh.external_mesh_data import ExternalMeshData

if TYPE_CHECKING:
    from vibra.engine.model import Model

import os
from time import time

import matplotlib.pyplot as plt
import numpy as np

# @pytest.mark.slow
# @pytest.mark.skip


def load_external_mesh_and_solve():

    # start decoding the Ansys script file (ds.dat file or input file)
    mesh_path = PROJECT_DIR / "validation_files/data/WB/acoustic/elements/hex20/mesh/rectangular_cavities_hex20.dat"
    results_path = PROJECT_DIR / "validation_files/data/WB/acoustic/elements/hex20/results/"

    if not os.path.exists(mesh_path):
        return

    if not results_path.exists():
        return

    # define the known 'Named selections' from model
    named_selecion_to_tag = {
        "input_face": 1,
        "output_face": 2,
    }

    # define surfaces from each volume
    surfaces_from_volume = {1: [1, 3, 4], 2: [2, 5]}

    t0 = time()
    external_mesh = ExternalMeshData()
    external_mesh.read_file(mesh_path)
    external_mesh.set_named_selections(list(named_selecion_to_tag.keys()))
    external_mesh.decode_mesh_data_from_file()

    # nodes_from_named_selection = external_mesh.nodes_from_named_selection
    # for ns, nodes in nodes_from_named_selection.items():
    #     print(ns, nodes)

    # return

    dt = time() - t0
    print(f"\nElapsed time to decode the external mesh data: {round(dt, 4)} s")

    mesh = Mesh()
    mesh.import_external_nodal_coordinates(external_mesh.nodal_coordinates, index_zero=True)
    mesh.import_external_faces_connectivity(external_mesh.faces_connectivities, index_zero=True, etype_tag=9)
    mesh.import_external_solids_connectivity(external_mesh.solids_connectivities, index_zero=True, etype_tag=11)
    mesh.map_face_elements_to_solid_elements()
    mesh.map_surfaces_to_volumes(surfaces_from_volume)

    # export the mesh data
    mesh.export_nodal_coordinates("nodal_coordinates.dat")
    mesh.export_solid_elements_connectivity("solids_connectivity.dat")
    mesh.export_face_elements_connectivity("faces_connectivity.dat")

    # check collapsed elements
    # collapsed_3d_elements, collapsed_2d_elements, collapsed_1d_elements = mesh.get_collapsed_elements()

    # return
    # define the fluid properties
    temperature = 293.15
    pressure = 101325
    rho_0 = 1.204263
    c_0 = 343.395034
    mu = 1 * 1.8247e-5
    Cp = 1006.400178
    kt = 2.5503e-02
    gamma = 1.401985
    molar_mass = 28.958601

    fluid = Fluid(
        name="Air_20C",
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
    for _vol_id in [1, 2]:
        model.properties._set_property("fluid", fluid, volume=_vol_id)

    for _surf_id in [1, 2]:
        model.properties._set_property("fluid", fluid, surface=_surf_id)

    ## normal surface velocity data
    data_Vn = {
        "real_values": [1],
        "imag_values": [0],
        "element_integration": True,
    }

    model.properties._set_property("surface_velocity", data_Vn, surface=1)

    # ## acoustic pressure data
    # data_Pa = {
    #     "real_values": [1],
    #     "imag_values": [0],
    # }

    # model.properties._set_property("acoustic_pressure", data_Pa, surface=1)

    ## boundary impedance setup
    Zo = fluid.impedance

    data_Z = {
        "real_values": [Zo],
        "imag_values": [0],
    }

    # model.properties._set_property("specific_impedance", data_Z, surface=1)
    model.properties._set_property("specific_impedance", data_Z, surface=2)

    ## Define the analysis frequency setup
    analysis_setup = model.get_harmonic_analysis_setup(
        frequency_spacing = FrequencySpacing.EQUALLY_DISTRIBUTED,
        analysis_id = AnalysisID.ACOUSTIC_HARMONIC,
        f_min = 5,
        f_max = 1400,
        f_step = 5,
    )

    frequencies = analysis_setup.get_frequencies()

    # Set the analysis setup
    model.set_analysis_setup(analysis_setup)

    assembler = AcousticAssembler(model)

    # Set the analysis frequency setup
    assembler.assemble_global_matrices_and_excitations(reorder=False, print_log=True)

    # Define the analysis type and load setup
    harmonic_solver = HarmonicSolver(assembler)

    # Run harmonic analysis
    t0 = time()
    model.solution = harmonic_solver.solve_direct(print_log=True)
    dt = time() - t0
    print(f"Elapsed time to solve harmonic analysis: {round(dt, 4)}")

    if model.solution is None:
        return
    
    t0 = time()
    acoustic_post = AcousticPostprocessing(model)

    input_particle_velocities = acoustic_post.get_particle_velocity_from_surface(1, volume_id=1)
    output_particle_velocities = acoustic_post.get_particle_velocity_from_surface(2, volume_id=2)

    # input_Vx = np.average(input_particle_velocities.Vx_array(), axis=0)
    # output_Vx = np.average(output_particle_velocities.Vx_array(), axis=0)

    dt = time() - t0
    print(f"Elapsed time to post-process data: {round(dt, 4)}")

    input_rows = mesh.external_nodes_from_surfaces[1]
    output_rows = mesh.external_nodes_from_surfaces[2]

    nodal_solution = model.solution.nodal_solution

    input_pressure = np.average(nodal_solution[input_rows, :], axis=0).flatten()
    output_pressure = np.average(nodal_solution[output_rows, :], axis=0).flatten()

    # hex8
    node_in = 3235
    node_out = 2276

    # Load the external data
    ext_data = LoadExternalData(results_path / "Vn_Z0", rho_0)

    WB_pressure_data = ext_data.load_nodal_pressures()
    WB_particle_velocities_data = ext_data.load_particle_velocities()

    freq_WB, _, input_velocities_WB = WB_particle_velocities_data["Vx", "input_face"]
    # input_Vx_WB = np.average(list(input_velocities_WB.values()), axis=0)

    freq_WB, _, input_pressures_WB = WB_pressure_data["input_face"]
    input_pressure_WB = np.average(list(input_pressures_WB.values()), axis=0)

    freq_WB, _, output_velocities_WB = WB_particle_velocities_data["Vx", "output_face"]
    # output_Vx_WB = np.average(list(output_velocities_WB.values()), axis=0)

    freq_WB, _, output_pressures_WB = WB_pressure_data["output_face"]
    output_pressure_WB = np.average(list(output_pressures_WB.values()), axis=0)

    # Print the nodal results deviations
    abs_diff_node_Pin = np.abs((input_pressures_WB[node_in] - nodal_solution[node_in - 1, :]) / (input_pressures_WB[node_in]))
    print(f"\nDeviation of pressure (node {node_in}): {100 * np.max(abs_diff_node_Pin)} %")

    abs_diff_node_Pout = np.abs((output_pressures_WB[node_out] - nodal_solution[node_out - 1, :]) / (output_pressures_WB[node_out]))
    print(f"Deviation of pressure (node {node_out}): {100 * np.max(abs_diff_node_Pout)} %")

    abs_diff_node_Vin = np.abs((input_velocities_WB[node_in] - input_particle_velocities.Vx[node_in - 1]) / (input_velocities_WB[node_in]))
    print(f"Deviation of particle velocity (node {node_in}): {100 * np.max(abs_diff_node_Vin)} %")

    abs_diff_node_Vout = np.abs(
        (output_velocities_WB[node_out] - output_particle_velocities.Vx[node_out - 1]) / (output_velocities_WB[node_out])
    )
    print(f"Deviation of particle velocity (node {node_out}): {100 * np.max(abs_diff_node_Vout)} %")

    abs_diff_Pinput_face = np.abs((input_pressure_WB - input_pressure) / input_pressure_WB)
    print(f"Deviation of pressure (input face): {100 * np.max(abs_diff_Pinput_face)} %")

    abs_diff_Poutput_face = np.abs((output_pressure_WB - output_pressure) / output_pressure_WB)
    print(f"Deviation of pressure (output face): {100 * np.max(abs_diff_Poutput_face)} %")

    # abs_diff_Vinput_face = np.abs((input_Vx_WB - input_Vx) / input_Vx_WB)
    # print(f"Deviation of particle velocity (input face): {100 * np.max(abs_diff_Vinput_face)} %")

    # abs_diff_Voutput_face = np.abs((output_Vx_WB - output_Vx) / output_Vx_WB)
    # print(f"Deviation of particle velocity (output face): {100 * np.max(abs_diff_Voutput_face)} %")

    title = "Harmonic response at input face"

    fig1, ax1 = plt.subplots()
    ax1.plot(frequencies, np.real(input_pressure), "r", label="Vibra")
    ax1.plot(freq_WB, np.real(input_pressure_WB), "k--", label="Ansys")
    ax1.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Real", title=title)
    ax1.grid()
    ax1.legend()

    fig2, ax2 = plt.subplots()
    ax2.plot(frequencies, np.imag(input_pressure), "r", label="Vibra")
    ax2.plot(freq_WB, np.imag(input_pressure_WB), "k--", label="Ansys")
    ax2.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Imaginary", title=title)
    ax2.grid()
    ax2.legend()

    title = "Harmonic response at output face"

    fig3, ax3 = plt.subplots()
    ax3.plot(frequencies, np.real(output_pressure), "r", label="Vibra")
    ax3.plot(freq_WB, np.real(output_pressure_WB), "k--", label="Ansys")
    ax3.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Real", title=title)
    ax3.grid()
    ax3.legend()

    fig4, ax4 = plt.subplots()
    ax4.plot(frequencies, np.imag(output_pressure), "r", label="Vibra")
    ax4.plot(freq_WB, np.imag(output_pressure_WB), "k--", label="Ansys")
    ax4.set(xlabel="Frequency [Hz]", ylabel="Acoustic Pressure [Pa] - Imaginary", title=title)
    ax4.grid()
    ax4.legend()

    # Plot the nodal results for pressure and particle velocity

    data_type = np.abs
    type_label = "absolute"

    fig5, ax5 = plt.subplots()
    title = f"Acoustic pressure at node {node_in}"
    ax5.semilogy(frequencies, data_type(nodal_solution[node_in - 1, :]), "r", label="Vibra")
    ax5.semilogy(freq_WB, data_type(input_pressures_WB[node_in]), "k--", label="Ansys")
    ax5.set_xlabel("Frequency [Hz]")
    ax5.set_ylabel(f"Acoustic Pressure [Pa] - {type_label}")
    ax5.set_title(title)
    ax5.grid()
    ax5.legend()

    fig6, ax6 = plt.subplots()
    title = f"Acoustic pressure at node {node_out}"
    ax6.semilogy(frequencies, data_type(nodal_solution[node_out - 1, :]), "r", label="Vibra")
    ax6.semilogy(freq_WB, data_type(output_pressures_WB[node_out]), "k--", label="Ansys")
    ax6.set_xlabel("Frequency [Hz]")
    ax6.set_ylabel(f"Acoustic Pressure [Pa] - {type_label}")
    ax6.set_title(title)
    ax6.grid()
    ax5.legend()

    fig7, ax7 = plt.subplots()
    title = f"Particle velocity at node {node_in}"
    ax7.semilogy(frequencies, data_type(input_particle_velocities.Vx[node_in - 1]), "r", label="Vibra")
    ax7.semilogy(freq_WB, data_type(input_velocities_WB[node_in]), "k--", label="Ansys")
    ax7.set_xlabel("Frequency [Hz]")
    ax7.set_ylabel(f"Particle velocity [m/s] - {type_label}")
    ax7.set_title(title)
    ax7.grid()
    ax7.legend()

    fig8, ax8 = plt.subplots()
    title = f"Particle velocity at node {node_out}"
    ax8.semilogy(frequencies, data_type(output_particle_velocities.Vx[node_out - 1]), "r", label="Vibra")
    ax8.semilogy(freq_WB, data_type(output_velocities_WB[node_out]), "k--", label="Ansys")
    ax8.set_xlabel("Frequency [Hz]")
    ax8.set_ylabel(f"Particle velocity [m/s] - {type_label}")
    ax8.set_title(title)
    ax8.grid()
    ax8.legend()

    # fig9, ax9 = plt.subplots()
    # title = "Input face particle velocity - average"
    # ax9.plot(frequencies, data_type(input_Vx), 'r', label='Vibra')
    # ax9.plot(freq_WB, data_type(input_Vx_WB), 'k--', label='Ansys')
    # ax9.set_xlabel('Frequency [Hz]')
    # ax9.set_ylabel(f'Particle velocity [m/s] - {type_label}')
    # ax9.set_title(title)
    # ax9.grid()
    # ax9.legend()

    # fig10, ax10 = plt.subplots()
    # title = "Output face particle velocity - average"
    # ax10.plot(frequencies, data_type(output_Vx), 'r', label='Vibra')
    # ax10.plot(freq_WB, data_type(output_Vx_WB), 'k--', label='Ansys')
    # ax10.set_xlabel('Frequency [Hz]')
    # ax10.set_ylabel(f'Particle velocity [m/s] - {type_label}')
    # ax10.set_title(title)
    # ax10.grid()
    # ax10.legend()

    plt.show()


def get_color(index: int):
    colors = [
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
        (0.25, 0.25, 0.25),
    ]

    if index <= 6:
        return colors[index]
    else:
        return tuple(np.random.randint(0, 255, size=3) / 255)


if __name__ == "__main__":
    load_external_mesh_and_solve()
