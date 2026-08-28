from typing import TYPE_CHECKING

from validation_files.data.WB.load_external_data import LoadExternalData
from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.postprocessing import AcousticPostprocessing
from vibra.engine.postprocessing.acoustic_post_solution_dataclass import NodalParticleVelocities
from vibra.engine.properties.fluid import Fluid
from vibra.engine.solvers.harmonic_solver import HarmonicSolver
from vibra.external_mesh.external_mesh_data import ExternalMeshData

if TYPE_CHECKING:
    from vibra.engine.model import Model

import os
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np


particle_velocity_labels = ["Vx", "Vy", "Vz"]


def load_external_mesh_and_solve(**kwargs):

    # start decoding the Ansys script file (ds.dat file or input file)
    mesh_path = PROJECT_DIR / "validation_files/data/WB/acoustic/excitations/tet4/mesh/ds_tet4_tetrahedron_harmonic_acoustic.dat"
    if not os.path.exists(mesh_path):
        return
    
    # define the known 'Named selections' from model
    named_selecion_to_tag = {
        "input_face": 1,
        "output_face": 2,
    }

    # define surfaces from each volume
    surfaces_from_volume = { 1 : [2], 2 : [1]}

    t0 = perf_counter()
    external_mesh = ExternalMeshData()
    external_mesh.read_file(mesh_path)
    external_mesh.set_named_selections(list(named_selecion_to_tag.keys()))
    external_mesh.decode_mesh_data_from_file()

    # nodes_from_named_selection = external_mesh.nodes_from_named_selection
    # for ns, nodes in nodes_from_named_selection.items():
    #     print(ns, nodes)

    # return

    dt = perf_counter() - t0
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

    # define the fluid properties
    temperature = 293.15
    pressure = 101325
    rho_0 = 1.204263
    c_0 = 343.395034
    mu = 1.8247e-5
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

    ## assign the created fluid
    model = Model()
    model.mesh = mesh

    ## assign the created fluid
    for _vol_id in [1, 2]:
        model.properties._set_property("fluid", fluid, volume=_vol_id)

    for _surf_id in [1, 2]:
        model.properties._set_property("fluid", fluid, surface=_surf_id)

    # ## normal surface velocity data
    # data_Vn = {
    #     "real_values": [1],
    #     "imag_values": [0],
    #     "element_integration": True,
    # }

    # model.properties._set_property("surface_velocity", data_Vn, surface=1)

    data_ipw = {        
        "real_values": [1],
        "imag_values": [0],
        "ipw_vector": [1.0, 0, 0],
    }

    model.properties._set_property("incident_plane_wave", data_ipw, surface=1)

    ## acoustic pressure data
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
        f_min = 7.5,
        f_max = 1500,
        f_step = 7.5,
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
    t0 = perf_counter()
    model.solution = harmonic_solver.solve_direct(print_log=True)
    dt = perf_counter() - t0
    print(f"Elapsed time to solve harmonic analysis: {round(dt, 4)}")

    if model.solution is None:
        return
        
    t0 = perf_counter()
    acoustic_post = AcousticPostprocessing(model)

    input_particle_velocities = acoustic_post.get_particle_velocity_from_surface(1, volume_id=2)
    output_particle_velocities = acoustic_post.get_particle_velocity_from_surface(2, volume_id=1)

    dt = perf_counter() - t0
    print(f"Elapsed time to post-process data: {round(dt, 4)}")

    nodal_solution = model.solution.nodal_solution

    # Load the external data
    results_path = PROJECT_DIR / "validation_files/data/WB/acoustic/excitations/tet4/results/ipw_in_duct/"
    ext_data = LoadExternalData(results_path, rho_0)

    WB_pressure_data = ext_data.load_nodal_pressures()
    WB_particle_velocities_data = ext_data.load_particle_velocities()

    for (surf_id, named_selection) in ((1, "input_face"), (2, "output_face")):

        print()
        freq_WB, _, pressures_WB = WB_pressure_data[named_selection]
        avg_pressure_WB = np.average(list(pressures_WB.values()), axis=0)

        rows = mesh.external_nodes_from_surfaces[surf_id]
        avg_pressure_vibra = np.average(nodal_solution[rows, :], axis=0).flatten()

        abs_diff_pressure = np.abs((avg_pressure_WB - avg_pressure_vibra) / avg_pressure_WB)
        print(f"Deviation of te averaged pressure (Surface #{surf_id}): {100 * np.max(abs_diff_pressure)} %")

        for pv_label in particle_velocity_labels:

            freq_WB, _, input_velocities_WB = WB_particle_velocities_data[pv_label, named_selection]
            avg_particle_velocity_WB = np.average(list(input_velocities_WB.values()), axis=0)

            if named_selection == "input_face":
                particle_velocities_vibra = getattr(input_particle_velocities, pv_label)
            else:
                particle_velocities_vibra = getattr(output_particle_velocities, pv_label)

            avg_particle_velocity_vibra = np.average(list(particle_velocities_vibra.values()), axis=0)

            abs_diff_pressure = np.abs((avg_particle_velocity_WB - avg_particle_velocity_vibra) / avg_particle_velocity_WB)
            print(f"Deviation of the averaged particle velocity {pv_label} (Surface #{surf_id}): {100 * np.max(abs_diff_pressure)} %")

   # Nodal results comparisons
    dofs_per_node = assembler.element_3d.DOF_PER_NODE

    # define the plot type
    plot_type = "real"

    # configure the postprocessing setup
    postprocessing_setup = [
        ((319, 325), "input_face", input_particle_velocities),
        ((932, 946), "output_face", output_particle_velocities),
    ]

    # acoustic results plots
    for (node_ids, named_selection, particle_velocities) in postprocessing_setup:
        
        if isinstance(node_ids, int):
            node_ids = [node_ids]

        for node_id in node_ids:

            print()
            # plots for acoustic pressure

            compare_nodal_pressures_results(
                node_id,
                dofs_per_node,
                frequencies,
                model.solution.nodal_solution,
                WB_pressure_data,
                named_selection,
                plot_type=plot_type,
            )

            # plots for particle velocity
            for particle_velocity_label in particle_velocity_labels:
                compare_averaged_nodal_particle_velocity_results(
                    node_id,
                    frequencies,
                    particle_velocity_label,
                    particle_velocities,
                    WB_particle_velocities_data,
                    named_selection,
                    plot_type=plot_type,
                )

    plt.show()


def compare_nodal_pressures_results(
    node_id: int,
    dofs_per_node: int,
    frequencies: np.ndarray,
    solution: np.ndarray,
    solution_reference: dict,
    named_selection: str = "all_solutions",
    plot_type: str = "absolute",
):

    response_vibra = get_model_response(node_id, dofs_per_node, solution)
    freq_ref, response_ref = get_reference_nodal_response(node_id, "pressure", named_selection, solution_reference)

    if response_ref is None:
        return

    title = f"Harmonic response at node {node_id}"
    x_label = "Frequency [Hz]"
    y_label = f'Acoustic pressure [Pa] - {plot_type.capitalize()}'

    fig, ax = plt.subplots()
    if plot_type == "real":
        plot_data = np.real
        plot = ax.plot

    elif plot_type == "imaginary":
        plot_data = np.imag
        plot = ax.plot

    else:
        plot_data = np.abs
        plot = ax.semilogy

    plot(frequencies, plot_data(response_vibra), 'r', label='Vibra')
    plot(freq_ref, plot_data(response_ref), 'k--', label='APDL')

    ax.set(xlabel=x_label, ylabel=y_label, title=title)
    ax.grid()
    ax.legend()

    if response_vibra.size != response_ref.size:
        return

    abs_diff = np.abs((response_vibra - response_ref) / response_ref)
    max_abs_diff = 100 * np.max(abs_diff)
    freq_max_diff = frequencies[np.argmax(abs_diff)]

    print(f"Maximum difference for acoustic pressure @ node {node_id}: {max_abs_diff} [%] @ {freq_max_diff} [Hz]")


def compare_averaged_nodal_particle_velocity_results(
    node_id: int,
    frequencies: np.ndarray,
    particle_velocity_label: str,
    nodal_averaged_particle_velocity: NodalParticleVelocities,
    solution_reference,
    named_selection: str = "all_solutions",
    plot_type: str = "absolute",
):

    response_vibra = getattr(nodal_averaged_particle_velocity, particle_velocity_label).get(node_id - 1)
    if response_vibra is None:
        return

    freq_ref, response_ref = get_reference_nodal_response(node_id, particle_velocity_label, named_selection, solution_reference)

    title = f"Harmonic response at node {node_id}"

    x_label = "Frequency [Hz]"
    y_label = f'Acoustic particle velocity {particle_velocity_label} [m/s] - {plot_type.capitalize()}'

    fig, ax = plt.subplots()
    if plot_type == "real":
        plot_data = np.real
        plot = ax.plot

    elif plot_type == "imaginary":
        plot_data = np.imag
        plot = ax.plot

    else:
        plot_data = np.abs
        plot = ax.semilogy

    plot(frequencies, plot_data(response_vibra), 'r', label='Vibra')

    if isinstance(response_ref, np.ndarray):
        plot(freq_ref, plot_data(response_ref), 'k--', label='APDL')

    ax.set(xlabel=x_label, ylabel=y_label, title=title)
    ax.grid()
    ax.legend()

    if response_vibra.size != response_ref.size:
        return

    abs_diff = np.abs((response_vibra - response_ref) / response_ref)
    max_abs_diff = 100 * np.max(abs_diff)
    freq_max_diff = frequencies[np.argmax(abs_diff)]

    print(f"Maximum difference for averaged {particle_velocity_label.capitalize()} @ node {node_id}: {max_abs_diff} [%] @ {freq_max_diff} [Hz]")


def get_model_response(apdl_node_id: int, dofs_per_node: int, solution: np.ndarray) -> np.ndarray:

    local_dof = 0
    index = int((apdl_node_id - 1) * dofs_per_node) + local_dof

    return solution[index, :]


def get_reference_nodal_response(node_id: int, data_label: str, named_selection: str, solution_reference: dict):

    if data_label == "pressure":
        key = named_selection
    else:
        key = (data_label, named_selection)

    freq_ref, _, nodal_solution_ref = solution_reference.get(key, (None, None, None))

    if freq_ref is None:
        return None, None

    if not isinstance(nodal_solution_ref, dict):
        return None, None

    response_ref = nodal_solution_ref.get(node_id)

    return freq_ref, response_ref


if __name__ == "__main__":

    load_external_mesh_and_solve()