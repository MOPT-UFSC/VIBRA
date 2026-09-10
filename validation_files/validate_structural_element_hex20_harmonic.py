from typing import TYPE_CHECKING

from validation_files.data.WB.load_external_data import LoadExternalData
from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.postprocessing import StructuralPostprocessing
from vibra.engine.postprocessing.structural_post_solution_dataclass import NodalStresses
from vibra.engine.properties.material import Material
from vibra.engine.solvers.harmonic_solver import HarmonicSolver
from vibra.external_mesh.external_mesh_data import ExternalMeshData

if TYPE_CHECKING:
    from vibra.engine.model import Model

import os
from time import time

import matplotlib.pyplot as plt
import numpy as np

udof_labels = [
    "ux", 
    "uy", 
    "uz",
    ]


stresses_labels = [
    "sigma_x", 
    "sigma_y", 
    "sigma_z", 
    "tau_xy", 
    "tau_xz",
    "tau_yz", 
    ]


udof_index = {
    "Ux" : 0,
    "Uy" : 1,
    "Uz" : 2,
    }


def load_external_mesh_and_solve(integration_type: str):

    # start decoding the Ansys script file (ds.dat file or input file)
    filename = "ds_hex20_cuboid_harmonic.dat"
    mesh_path = f"validation_files/data/WB/structural/elements/hex20/mesh/{filename}"
    if not os.path.exists(mesh_path):
        return

    # define the known 'Named selections' from model
    named_selecion_to_tag = { 
                             "input_face" : 1,
                             "output_face" : 2,
                            }

    # define surfaces from each volume
    surfaces_from_volume = { 1 : [1, 2]}

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

    # Define the material properties

    density = 7850
    elasticity_modulus = 2e11
    poisson_ratio = 0.30
    thermal_expansion_coefficient = 1.1e-5

    material = Material(   
        name = "Carbon steel",
        identifier = 1,
        color = (200, 200, 200),
        material_density = density,
        elasticity_modulus = elasticity_modulus,
        poisson_ratio = poisson_ratio,
        thermal_expansion_coefficient = thermal_expansion_coefficient
        )

    ## intialize the model
    model = Model()
    model.mesh = mesh

    ## assign the created fluid
    model.properties._set_property("material", material, volume=1)
    
    for _surf_id in [1, 2]:
        model.properties._set_property("material", material, surface=_surf_id)

    ## boundary condition

    # dof prescription data
    dof_prescription_data = {
        "element_type": "3d_element",
        "real_values": [0.0, 0.0, 0.0],
        "imag_values": [0.0, 0.0, 0.0],
        }

    model.properties._set_property("prescribed_dof", dof_prescription_data, surface=1)

    # nodal load data
    nodal_load_data = {
        "element_type": "3d_element",
        "real_values": [0.0, 1.0, 1.0],
        "imag_values": [0.0, 0.0, 0.0],
        "element_integration": True,
        }

    model.properties._set_property("nodal_loads", nodal_load_data, surface=2)

    ## Define the analysis frequency setup
    analysis_setup = model.get_harmonic_analysis_setup(
        frequency_spacing = FrequencySpacing.EQUALLY_DISTRIBUTED,
        analysis_id = AnalysisID.STRUCTURAL_HARMONIC,
        f_min = 100,
        f_max = 2000,
        f_step = 100,
    )

    frequencies = analysis_setup.get_frequencies()

    # Set the analysis setup
    model.set_analysis_setup(analysis_setup)

    assembler = StructuralAssembler(model)

    # Set the analysis frequency setup
    assembler.assemble_global_matrices_and_excitations(reorder=False, print_log=True)

    t0 = time()
    # Run modal analysis
    harmonic_solver = HarmonicSolver(assembler)
    model.solution = harmonic_solver.solve_direct(print_log=True)
    dt = time() - t0
    print(f"Elapsed time to solve modal analysis: {round(dt, 4)}s")

    # Nodal results comparisons
    dofs_per_node = assembler.element_3d.DOF_PER_NODE

    path = PROJECT_DIR / f"validation_files/data/WB/structural/elements/hex20/results/{integration_type}/harmonic/"
    ext_data = LoadExternalData(path)

    WB_displacements_data = ext_data.load_displacements(entire_solution=True)
    WB_stresses_data = ext_data.load_stresses(entire_solution=True)

    structural_post = StructuralPostprocessing(model)

    t0 = time()
    avg_nodal_stresses, nodal_stresses_data = structural_post.get_structural_stresses(volume_ids=1)
    dt = time() - t0
    print(f"Time to compute nodal stresses: {dt} s")

    nodal_averaged_stresses = structural_post.nodal_stresses_post_process(avg_nodal_stresses)
    # nodal_stresses = structural_post.nodal_stresses_post_process(nodal_stresses_data)

    # sigma_x_el3780 = (nodal_stresses.sigma_x[(3780-1, 6200-1)] + nodal_stresses.sigma_x[(3780-1, 6257-1)]) / 2
    # sigma_x_el3784 = (nodal_stresses.sigma_x[(3784-1, 6200-1)] + nodal_stresses.sigma_x[(3784-1, 6257-1)]) / 2
    # sigma_x_node25428 = (sigma_x_el3780 + sigma_x_el3784) / 2

    # sigma_x_el3791 = (nodal_stresses.sigma_x[(3791-1, 6200-1)] + nodal_stresses.sigma_x[(3791-1, 6262-1)]) / 2
    # sigma_x_el3793 = (nodal_stresses.sigma_x[(3793-1, 6200-1)] + nodal_stresses.sigma_x[(3793-1, 6262-1)]) / 2
    # sigma_x_node25429 = (sigma_x_el3791 + sigma_x_el3793) / 2

    # sigma_x_25428 = getattr(nodal_averaged_stresses, "sigma_x")[25428 - 1]
    # sigma_x_25429 = getattr(nodal_averaged_stresses, "sigma_x")[25429 - 1]

    # print("Results for node 25428")
    # print(np.allclose(sigma_x_node25428, sigma_x_25428, atol=1e-8))

    # print("Results for node 25429")
    # print(np.allclose(sigma_x_node25429, sigma_x_25429, atol=1e-8))

    plot_type = "absolute"

    for node_id in [6200, 6228, 6628]:

        print()
        # displacements plots
        for dof_label in udof_labels:
            compare_nodal_displacements_results(
                node_id,
                dofs_per_node,
                dof_label,
                frequencies,
                model.solution.nodal_solution,
                integration_type,
                WB_displacements_data,
                plot_type=plot_type,
                )

        # plots for stresses
        for stress_label in stresses_labels[0:3]:
            compare_averaged_nodal_stresses_results(
                node_id, 
                stress_label, 
                frequencies, 
                nodal_averaged_stresses, 
                integration_type, 
                WB_stresses_data,
                plot_type=plot_type,
                )

    # # input_nodes = mesh.external_nodes_from_surfaces[1]
    # output_nodes = mesh.external_nodes_from_surfaces[2]
    # output_rows = output_nodes * dofs_per_node + udof_index.get("Uy")

    plt.show()


def compare_nodal_displacements_results(
        node_id: int, 
        dofs_per_node: int, 
        dof_label: str, 
        frequencies: np.ndarray, 
        solution: np.ndarray,
        integration_type: str,
        solution_reference: dict,
        named_selection: str = "all_solutions",
        plot_type: str = "absolute",
        ):

    response_vibra = get_model_response(
        node_id, 
        dof_label, 
        dofs_per_node, 
        solution,
        )

    freq_ref, response_ref = get_reference_nodal_response(
        node_id, 
        dof_label, 
        named_selection, 
        solution_reference,
        )

    if response_ref is None:
        return

    if response_vibra.size == response_ref.size:
        abs_diff = np.abs((response_vibra - response_ref) / response_ref)
        max_abs_diff = 100 * np.max(abs_diff)
        freq_max_diff = frequencies[np.argmax(abs_diff)]

        print(f"Maximum difference for {dof_label.capitalize()} @ node {node_id}: {max_abs_diff} [%] @ {freq_max_diff} [Hz]")
        # return

    title = f"Harmonic response at node {node_id} ({integration_type})"
    x_label = "Frequency [Hz]"
    y_label = f'Structural response {dof_label.capitalize()} [m] - {plot_type.capitalize()}'

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


def compare_averaged_nodal_stresses_results(
    node_id: int, 
    stress_label: str, 
    frequencies: np.ndarray, 
    nodal_averaged_stresses: NodalStresses,
    integration_type: str,
    solution_reference,
    named_selection: str = "all_solutions",
    plot_type: str = "absolute",
    ):

    response_vibra = getattr(nodal_averaged_stresses, stress_label)[node_id - 1]

    freq_ref, response_ref = get_reference_nodal_response(
        node_id, 
        stress_label, 
        named_selection, 
        solution_reference,
        )

    if response_vibra.size == response_ref.size:
        if np.sum(np.abs(response_ref)):
            abs_diff = np.abs((response_vibra - response_ref) / response_ref)
            max_abs_diff = 100 * np.max(abs_diff)
            freq_max_diff = frequencies[np.argmax(abs_diff)]

            print(f"Maximum difference for averaged {stress_label.capitalize()} @ node {node_id}: {max_abs_diff} [%] @ {freq_max_diff} [Hz]")

    title = f"Harmonic response at node {node_id} ({integration_type})"
    x_label = "Frequency [Hz]"
    y_label = f'Structural stress {stress_label} [Pa] - {plot_type.capitalize()}'

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


def get_model_response(
        apdl_node_id: int, 
        dof_label: str, 
        dofs_per_node: int, 
        solution: np.ndarray) -> np.ndarray:

    local_dof = udof_labels.index(dof_label)

    index = int((apdl_node_id - 1) * dofs_per_node) + local_dof

    return solution[index, :]


def get_reference_nodal_response(
    node_id: int,
    _label: str,
    named_selection: str,
    solution_reference: dict,
    ):

    key = (_label, named_selection)
    freq_ref, _, nodal_solution_ref = solution_reference.get(key, (None, None, None))

    if freq_ref is None:
        return None, None

    if not isinstance(nodal_solution_ref, dict):
        return None, None

    response_ref = nodal_solution_ref.get(node_id)

    return freq_ref, response_ref


if __name__ == "__main__":

    load_external_mesh_and_solve("reduced_integration")