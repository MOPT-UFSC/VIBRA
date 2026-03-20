from vibra import PROJECT_DIR
from vibra.engine import AnalysisID 
from vibra.engine.properties.material import Material
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.element_type import HEXAHEDRON_8
from vibra.engine.model import Model
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.postprocessing import StructuralPostprocessing

from vibra.engine.solvers.harmonic_solver import HarmonicSolver
from vibra.external_mesh.external_mesh_data import ExternalMeshData
from validation_files.data.WB.load_external_data import LoadExternalData
from vibra.engine.postprocessing.structural_post_solution_dataclass import NodalStresses


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

import os
import numpy as np
import matplotlib.pyplot as plt

from time import time


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


def load_external_mesh_and_solve(**kwargs):

    # start decoding the Ansys script file (ds.dat file or input file)
    mesh_path = f"validation_files/data/WB/structural/elements/hex8/mesh/ds_hex8_cuboid_modal.dat"
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
    mesh.import_external_solids_connectivity(external_mesh.solids_connectivities, index_zero=True, etype_tag=11)
    mesh.import_external_faces_connectivity(external_mesh.faces_connectivities, index_zero=True, etype_tag=9)
    mesh.export_nodal_coordinates("nodal_coordinates.dat")
    mesh.export_solid_elements_connectivity("solids_connectivity.dat")
    mesh.export_face_elements_connectivity("faces_connectivity.dat")
    mesh.element_type = HEXAHEDRON_8

    for named_selection, surf_data in external_mesh.elements_from_named_selection.items():

        if named_selection in ["input_edges", "output_edges"]:
            continue

        tag = named_selecion_to_tag[named_selection]
        mesh.elements_from_surface[tag] = surf_data["element_indexes"] - 1
        mesh.external_connectivity_from_surfaces[tag] = surf_data["connectivity"] - 1
        ns_nodes = external_mesh.nodes_from_named_selection[named_selection]
        mesh.external_nodes_from_surfaces[tag] = np.array(ns_nodes, dtype=int) - 1


    for vol_id, surf_ids in surfaces_from_volume.items():
        for surf_id in surf_ids:
            mesh.volumes_from_surface[surf_id] = [vol_id]
        mesh.surfaces_from_volume[vol_id] = surf_ids

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

    ## assign the created fluid
    model = Model()
    model.mesh =  mesh
    model.generated_mesh = True

    model.properties._set_property("material", material, volume=1)
    
    for _surf_id in [1, 2]:
        model.properties._set_property("material", material, surface=_surf_id)

    ## advanced options for structural hex8 element
    extra_shape_function = kwargs.get("extra_shape_function", False)
    Bbar_formulation = kwargs.get("Bbar_formulation", False)

    element_options = {
        "hex8" : {
            "extra_shape_functions" : extra_shape_function,
            "Bbar_formulation" : Bbar_formulation,
            }
        }

    # assign the hex8 element advanced options as a global property
    model.properties._set_property("advanced_element_options", element_options)

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
        "nodal_attribution": True,
        "averaged": False,
        }

    model.properties._set_property("nodal_loads", nodal_load_data, surface=2)

    ## Define the analysis frequency setup

    df = 100
    f_min = 100
    f_max = 2000
    frequencies = np.arange(f_min, f_max + df, df, dtype=float)

    analysis_setup = {
        "analisys_id" : AnalysisID.STRUCTURAL_HARMONIC,
        "f_min" : f_min,
        "f_max" : f_max,
        "f_step" : df,
        "frequencies" : frequencies,
        "global_damping" : (0., 0., 0e-2),
        }

    # Set the analysis setup
    model.set_analysis_setup(analysis_setup)

    assembler = StructuralAssembler(model)

    # Set the analysis frequency setup
    assembler.assemble_global_matrices_and_excitations(reorder=False)

    t0 = time()
    # Run modal analysis
    harmonic_solver = HarmonicSolver(assembler)
    solution = harmonic_solver.solve_direct(print_log=True)
    dt = time() - t0
    print(f"Elapsed time to solve modal analysis: {round(dt, 4)}s")

    if Bbar_formulation:
        folder = "Bbar"
    else:
        folder = "with_esf" if extra_shape_function else "without_esf"

    results_path = PROJECT_DIR / f"validation_files/data/WB/structural/elements/hex8/results/{folder}/"
    ext_data = LoadExternalData(results_path)

    WB_displacements_data = ext_data.load_displacements(entire_solution=True)
    WB_stresses_data = ext_data.load_stresses(entire_solution=True)

    structural_post = StructuralPostprocessing(structural_harmonic_solver=harmonic_solver)

    t0 = time()
    avg_nodal_stresses, _ = structural_post.get_structural_stresses(volume_ids=1)
    dt = time() - t0
    print(f"Time to compute nodal stresses: {dt} s")

    nodal_averaged_stresses = structural_post.nodal_stresses_post_process(avg_nodal_stresses)
    # element_averaged_stresses = structural_post.nodal_stresses_post_process(element_stresses)

   # Nodal results comparisons
    dofs_per_node = assembler.element_3d.DOF_PER_NODE

    # define the plot type
    plot_type = "absolute"

    # displacements plots
    for node_id in [5100, 6199, 6232]:

        print()
        # plots for displacements
        for udof_label in udof_labels:
            compare_nodal_displacements_results(
                node_id,
                dofs_per_node,
                udof_label,
                frequencies,
                solution,
                extra_shape_function,
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
                extra_shape_function, 
                WB_stresses_data,
                plot_type=plot_type,
                )

    plt.show()


def compare_nodal_displacements_results(
        node_id: int, 
        dofs_per_node: int, 
        dof_label: str, 
        frequencies: np.ndarray, 
        solution: np.ndarray,
        esf: bool,
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

    title = f"Harmonic response at node {node_id} - {"(ESF included)" if esf else "(ESF excluded)"}"
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

    if response_vibra.size != response_ref.size:
        return

    abs_diff = np.abs((response_vibra - response_ref) / response_ref)
    max_abs_diff = 100 * np.max(abs_diff)
    freq_max_diff = frequencies[np.argmax(abs_diff)]

    print(f"Maximum difference for {dof_label.capitalize()} @ node {node_id}: {max_abs_diff} [%] @ {freq_max_diff} [Hz]")


def compare_averaged_nodal_stresses_results(
    node_id: int, 
    stress_label: str, 
    frequencies: np.ndarray, 
    nodal_averaged_stresses: NodalStresses,
    esf: bool,
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

    # freq_apdl, response_apdl = get_apdl_reference_stresses_results(node_id, stress_label, esf)

    title = f"Harmonic response at node {node_id} - {"(ESF included)" if esf else "(ESF excluded)"}"
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

    if response_vibra.size != response_ref.size:
        return

    abs_diff = np.abs((response_vibra - response_ref) / response_ref)
    max_abs_diff = 100 * np.max(abs_diff)
    freq_max_diff = frequencies[np.argmax(abs_diff)]

    print(f"Maximum difference for averaged {stress_label.capitalize()} @ node {node_id}: {max_abs_diff} [%] @ {freq_max_diff} [Hz]")


def compare_nodal_stresses_results(
    element_id: int,
    node_id: int,
    stress_label: str, 
    frequencies: np.ndarray, 
    nodal_stresses: dict,
    esf: bool,
    plot_type: str = "absolute",
    ):

    file_name = f"stress_{stress_label}_element_{element_id}_node_{node_id}_Ansys.dat"

    row = stresses_labels.index(stress_label)
    response_vibra = nodal_stresses.get((element_id-1, node_id-1))[row, :]

    freq_apdl, response_apdl = get_apdl_reference_stresses_results(node_id, stress_label, esf, file_name=file_name)

    title = f"Harmonic response at element {element_id} and node {node_id} - {"(ESF included)" if esf else "(ESF excluded)"}"
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
    plot(freq_apdl, plot_data(response_apdl), 'k--', label='APDL')

    ax.set(xlabel=x_label, ylabel=y_label, title=title)
    ax.grid()
    ax.legend()

    abs_diff = np.abs((response_vibra - response_apdl) / response_apdl)
    max_abs_diff = 100 * np.max(abs_diff)
    freq_max_diff = frequencies[np.argmax(abs_diff)]

    print(f"Maximum difference for {stress_label.capitalize()} @ element {element_id} / node {node_id}: {max_abs_diff} [%] @ {freq_max_diff} [Hz]")


def get_apdl_reference_displacement_results(
        apdl_node_id: int, 
        dof_label: str,
        extra_shape_functions: bool,
        ) -> np.ndarray | None:
    
    folder = "with_esf" if extra_shape_functions else "without_esf"
    results_path = PROJECT_DIR / f"validation_files/data/WB/structural/elements/hex8/results/{folder}/"
    
    if not results_path.exists():
        return None, None
    
    # load mechanical apdl results
    ansys_data = np.loadtxt(results_path / f"response_{dof_label}_node_{apdl_node_id}_Ansys.dat", skiprows=2)

    freq_apdl = ansys_data[:, 0]
    response_apdl = ansys_data[:, 1] + 1j * ansys_data[:, 2]

    return freq_apdl, response_apdl


def get_apdl_reference_stresses_results(
        apdl_node_id: int, 
        stress_label: str,
        extra_shape_functions: bool,
        file_name: str | None = None,
        ) -> np.ndarray | None:
    
    folder = "with_esf" if extra_shape_functions else "without_esf"
    results_path = PROJECT_DIR / f"validation_files/data/WB/structural/elements/hex8/results/{folder}/"
    
    if not results_path.exists():
        return None, None
    
    # load mechanical apdl results
    if not isinstance(file_name, str):
        file_path = results_path / f"stress_{stress_label}_node_{apdl_node_id}_Ansys.dat"
    else:
        file_path = results_path / file_name

    if not file_path.exists():
        print(f"Invalid path: {file_path}")
        return None, None

    ansys_data = np.loadtxt(file_path, skiprows=2)

    freq_apdl = ansys_data[:, 0]
    response_apdl = ansys_data[:, 1] + 1j * ansys_data[:, 2]

    return freq_apdl, response_apdl


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

    load_external_mesh_and_solve(extra_shape_function=False, Bbar_formulation=True)