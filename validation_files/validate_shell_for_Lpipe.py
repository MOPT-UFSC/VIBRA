from typing import TYPE_CHECKING

from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.properties.material import Material
from vibra.engine.solution import HarmonicSolution
from vibra.engine.solvers.harmonic_solver import HarmonicSolver
from vibra.external_mesh.external_mesh_data import ExternalMeshData
from vibra.interface.data_handler.data_importer import DataImporter

if TYPE_CHECKING:
    from vibra.engine.model import Model

import os
from time import time

import matplotlib.pyplot as plt

# import pytest
import numpy as np

# valid mesh sizes: 20mm and 200mm.
mesh_size = "200mm"


# @pytest.mark.slow
# @pytest.mark.skip


def load_external_mesh_and_solve():

    # start decoding the Ansys script file (ds.dat file or input file)
    mesh_path = "validation_files/data/WB/structural/shell/L_pipe/mesh/ds_Lpipe_with_caps.dat"

    if not os.path.exists(mesh_path):
        return

    # define the known 'Named selections' from model
    named_selecion_to_tag = {
        "input_face": 2,
        "output_face": 3,
    }

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
    mesh.import_external_faces_connectivity(external_mesh.solids_connectivities, index_zero=True, etype_tag=4)
    mesh.export_nodal_coordinates("nodal_coordinates.dat")
    mesh.export_solid_elements_connectivity("solids_connectivity.dat")

    for named_selection, surf_data in external_mesh.elements_from_named_selection.items():
        if named_selection in ["input_edges", "output_edges"]:
            continue

        tag = named_selecion_to_tag[named_selection]
        mesh.elements_from_surface[tag] = surf_data["element2d_indices"] - 1
        mesh.external_connectivity_from_surfaces[tag] = surf_data["connectivity"] - 1
        ns_nodes = external_mesh.nodes_from_named_selection[named_selection]
        mesh.external_nodes_from_surfaces[tag] = np.array(ns_nodes, dtype=int) - 1

    # # Load the external data
    # path = f"validation_files/data/WB/structural/shell/pipes/results/results_for_L_pipe.xlsx"
    # ext_data = LoadExternalData(path, fluid_density=rho_0)

    ## intialize the model
    model = Model()
    model.mesh = mesh

    thickness_data = {
        "surface_thickness": 0.008,
        "thickness_offset": "middle",
    }

    model.properties._set_property("surface_thickness", thickness_data, surface=1)

    # Define the material properties

    density = 7850
    elasticity_modulus = 2e11
    poisson_ratio = 0.30
    thermal_expansion_coefficient = 1.1e-5

    material = Material(
        name="Carbon steel",
        identifier=1,
        color=(200, 200, 200),
        material_density=density,
        elasticity_modulus=elasticity_modulus,
        poisson_ratio=poisson_ratio,
        thermal_expansion_coefficient=thermal_expansion_coefficient,
    )

    model.properties._set_property("material", material, surface=1)

    # Prescribed dof data
    prescribed_dof_data = {
        "element_type": "2d_element",
        "real_values": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "imag_values": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    }

    model.properties._set_property("prescribed_dof", prescribed_dof_data, surface=2)

    # Nodal loads data
    distributed_load_data = {
        "element_type": "2d_element",
        "real_values": [100.0, None, None],
        "imag_values": [0.0, None, None],
        "unit": "N/m²",
    }

    model.properties._set_property("distributed_loads", distributed_load_data, surface=3)

    # Define the analysis frequency setup
    analysis_setup = model.get_harmonic_analysis_setup(
        analysis_id = AnalysisID.STRUCTURAL_HARMONIC,
        frequency_spacing = FrequencySpacing.EQUALLY_DISTRIBUTED,
        f_min = 2,
        f_max = 300,
        f_step = 2,
        global_damping = (1e-3, 1e-7, 0),
    )

    frequencies = analysis_setup.get_frequencies()

    model.set_analysis_setup(analysis_setup)

    # Define and process the assemble
    assembler = StructuralAssembler(model)
    assembler.assemble_global_matrices_and_excitations()

    # Initialize the solver
    # modal_solver = ModalSolver(assembler)
    harmonic_solver = HarmonicSolver(assembler)

    # t0 = time()
    # # solution = modal_solver.solve()
    # dt = time() - t0
    # print(f"Elapsed time to solve modal analysis: {round(dt, 4)}\n\n")

    # print("::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    # print(":: PLOTTING THE OBTAINED RESULTS FOR MODAL ANALYSIS ::")
    # print("::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")

    # for k, freq in enumerate(modal_solver.natural_frequencies):
    #     print(f"Mode: {k+1} ==> Natural frequency: {freq : .4f} Hz")

    t0 = time()
    # solution = modal_solver.solve()
    model.solution = harmonic_solver.solve_direct(print_log=True)
    dt = time() - t0
    print(f"Elapsed time to solve the analysis: {round(dt, 4)}")

    if not isinstance(model.solution, HarmonicSolution):
        return

    # print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    # print(":: PLOTTING THE OBTAINED RESULTS FOR HARMONIC ANALYSIS ::")
    # print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")

    selected_nodes = mesh.external_nodes_from_surfaces[3]

    dof_index = {"ux": 0, "uy": 1, "uz": 2, "rx": 3, "ry": 4, "rz": 5}

    element_2d = model.structural_element_2d
    if element_2d is None:
        return

    dof_per_node = element_2d.DOF_PER_NODE
    gdof = dof_per_node * selected_nodes.reshape(-1, 1) + np.arange(dof_per_node, dtype=int)

    ux_rows = gdof[:, dof_index["ux"]]
    uy_rows = gdof[:, dof_index["uy"]]

    nodal_solution = model.solution.nodal_solution

    response_ux = np.average(nodal_solution[ux_rows, :], axis=0).flatten()
    response_uy = np.average(nodal_solution[uy_rows, :], axis=0).flatten()

    dt = time() - t0
    print(f"Elapsed time to post-process data: {round(dt, 4)}")

    ## load external results data
    results_path = "validation_files/data/WB/structural/shell/L_pipe/results/results_for_L_pipe.xlsx"
    imported_results = DataImporter.load_spreadsheet_data_for_validation(results_path)

    output_face_ux_lin = imported_results["output_face_ux_lin"]
    output_face_ux_quad = imported_results["output_face_ux_quad"]

    output_face_uy_lin = imported_results["output_face_uy_lin"]
    output_face_uy_quad = imported_results["output_face_uy_quad"]

    freq_WB = output_face_ux_lin[:, 0]
    output_face_ux_lin_WB = output_face_ux_lin[:, 1] + 1j * output_face_ux_lin[:, 2]

    freq_WB = output_face_ux_quad[:, 0]
    output_face_ux_quad_WB = output_face_ux_quad[:, 1] + 1j * output_face_ux_quad[:, 2]

    freq_WB = output_face_uy_lin[:, 0]
    output_face_uy_lin_WB = output_face_uy_lin[:, 1] + 1j * output_face_uy_lin[:, 2]

    freq_WB = output_face_uy_quad[:, 0]
    output_face_uy_quad_WB = output_face_uy_quad[:, 1] + 1j * output_face_uy_quad[:, 2]

    title = "Harmonic response at output face"

    fig1, ax1 = plt.subplots()
    ax1.semilogy(frequencies, np.abs(response_ux), "r", label="VIBRA")
    ax1.semilogy(freq_WB, np.abs(output_face_ux_lin_WB), "k--", label="ANSYS (lin.)")
    ax1.semilogy(freq_WB, np.abs(output_face_ux_quad_WB), "b--", label="ANSYS (quad.)")
    ax1.set(xlabel="Frequency [Hz]", ylabel="Magnitude of displacement Ux [m]", title=title)
    ax1.grid()
    ax1.legend()

    fig2, ax2 = plt.subplots()
    ax2.semilogy(frequencies, np.abs(response_uy), "r", label="VIBRA")
    ax2.semilogy(freq_WB, np.abs(output_face_uy_lin_WB), "k--", label="ANSYS (lin.)")
    ax2.semilogy(freq_WB, np.abs(output_face_uy_quad_WB), "b--", label="ANSYS (quad.)")
    ax2.set(xlabel="Frequency [Hz]", ylabel="Magnitude of displacement Uy [m]", title=title)
    ax2.grid()
    ax2.legend()

    plt.show()


if __name__ == "__main__":
    load_external_mesh_and_solve()
