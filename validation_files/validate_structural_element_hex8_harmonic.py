from vibra import PROJECT_DIR
from vibra.engine import AnalysisID 
from vibra.engine.properties.material import Material
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.element_type import HEXAHEDRON_8
from vibra.engine.model import Model
from vibra.engine.assemblers.structural_assembler import StructuralAssembler

from vibra.engine.solvers.harmonic_solver import HarmonicSolver
from vibra.external_mesh.external_mesh_data import ExternalMeshData

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

import os
import numpy as np
import matplotlib.pyplot as plt

from time import time

# @pytest.mark.slow
# @pytest.mark.skip

def load_external_mesh_and_solve():

    # start decoding the Ansys script file (ds.dat file or input file)
    mesh_path = f"validation_files/data/WB/structural/elements/hex8/extra_shape_functions/mesh/ds_hex8_cuboid_modal.dat"
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
    hex8_advanced_options = {"hex8" : {"extra_shape_functions" : True}}

    # assign the hex8 element advanced options as a global property
    model.properties._set_property("advanced_element_options", hex8_advanced_options)

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
        "real_values": [0.0, 1.0, 0.0],
        "imag_values": [0.0, 0.0, 0.0],
        "nodal_attribution": True,
        "averaged": False,
        }

    model.properties._set_property("nodal_loads", nodal_load_data, surface=2)

    ## Define the analysis frequency setup

    df = 20
    f_min = 20
    f_max = 2000
    frequencies = np.arange(f_min, f_max + df, df)

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

    dofs_per_node = assembler.element_3d.DOF_PER_NODE

   # compare nodal results
    node_4882 = 4882
    response_uy_node_4882 = get_model_response(node_4882, "uy", dofs_per_node, solution)
    freq_apdl, uy_node_4882_apdl = get_apdl_results(node_4882, "uy")

    response_uz_node_4882 = get_model_response(node_4882, "uz", dofs_per_node, solution)
    freq_apdl, uz_node_4882_apdl = get_apdl_results(node_4882, "uz")

    node_5522 = 5522
    response_uy_node_5522 = get_model_response(node_5522, "uy", dofs_per_node, solution)
    freq_apdl, uy_node_5522_apdl = get_apdl_results(node_5522, "uy")

    node_6210 = 6210
    response_uy_node_6210 = get_model_response(node_6210, "uy", dofs_per_node, solution)
    freq_apdl, uy_node_6210_apdl = get_apdl_results(node_6210, "uy")

    node_6269 = 6269
    response_uy_node_6269 = get_model_response(node_6269, "uy", dofs_per_node, solution)
    freq_apdl, uy_node_6269_apdl = get_apdl_results(node_6269, "uy")

    title = f"Harmonic response at node {node_4882}"

    fig1, ax1 = plt.subplots()
    ax1.semilogy(frequencies, np.abs(response_uy_node_4882), 'r', label='VIBRA')
    ax1.semilogy(freq_apdl, np.abs(uy_node_4882_apdl), 'k--', label='ANSYS')
    ax1.set(xlabel='Frequency [Hz]', ylabel='Structural response Uy [m] - Absolute', title=title)
    ax1.grid()
    ax1.legend()

    fig2, ax2 = plt.subplots()
    ax2.semilogy(frequencies, np.abs(response_uz_node_4882), 'r', label='VIBRA')
    ax2.semilogy(freq_apdl, np.abs(uz_node_4882_apdl), 'k--', label='ANSYS')
    ax2.set(xlabel='Frequency [Hz]', ylabel='Structural response Uz [m] - Absolute', title=title)
    ax2.grid()
    ax2.legend()

    title = f"Harmonic response at node {node_5522}"

    fig3, ax3 = plt.subplots()
    ax3.semilogy(frequencies, np.abs(response_uy_node_5522), 'r', label='VIBRA')
    ax3.semilogy(freq_apdl, np.abs(uy_node_5522_apdl), 'k--', label='ANSYS')
    ax3.set(xlabel='Frequency [Hz]', ylabel='Structural response Uy [m] - Absolute', title=title)
    ax3.grid()
    ax3.legend()

    title = f"Harmonic response at node {node_6210}"

    fig4, ax4 = plt.subplots()
    ax4.semilogy(frequencies, np.abs(response_uy_node_6210), 'r', label='VIBRA')
    ax4.semilogy(freq_apdl, np.abs(uy_node_6210_apdl), 'k--', label='ANSYS')
    ax4.set(xlabel='Frequency [Hz]', ylabel='Structural response Uy [m] - Absolute', title=title)
    ax4.grid()
    ax4.legend()

    title = f"Harmonic response at node {node_6269}"

    fig5, ax5 = plt.subplots()
    ax5.semilogy(frequencies, np.abs(response_uy_node_6269), 'r', label='VIBRA')
    ax5.semilogy(freq_apdl, np.abs(uy_node_6269_apdl), 'k--', label='ANSYS')
    ax5.set(xlabel='Frequency [Hz]', ylabel='Structural response Uy [m] - Absolute', title=title)
    ax5.grid()
    ax5.legend()

    plt.show()


def get_apdl_results(apdl_node_id: int, dof_label: str):

    results_path = PROJECT_DIR / "validation_files/data/WB/structural/elements/hex8/extra_shape_functions/results/"
    if not results_path.exists():
        return
    
    # load mechanical apdl results
    ansys_data = np.loadtxt(results_path / f"response_{dof_label}_node_{apdl_node_id}_Ansys.dat", skiprows=2)

    freq_apdl = ansys_data[:, 0]
    response_apdl = ansys_data[:, 1] + 1j * ansys_data[:, 2]

    return freq_apdl, response_apdl


def get_model_response(apdl_node_id: int, dof_label: str, dofs_per_node: int, solution: np.ndarray):

    dof_labels = ["ux", "uy", "uz"]
    local_dof = dof_labels.index(dof_label)

    index = int((apdl_node_id - 1) * dofs_per_node) + local_dof

    return solution[index, :]


if __name__ == "__main__":

    load_external_mesh_and_solve()