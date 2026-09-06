from typing import TYPE_CHECKING

from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, ModalAnalysisSetup
from vibra.engine.assemblers.structural.structural_assembler import StructuralAssembler
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.properties.material import Material
from vibra.engine.solvers.modal_solver import ModalSolver
from vibra.external_mesh.external_mesh_data import ExternalMeshData

if TYPE_CHECKING:
    from vibra.engine.model import Model

import os
from time import time

import numpy as np


def load_external_mesh_and_solve(integration_type: str):

    # start decoding the Ansys script file (ds.dat file or input file)
    mesh_path = "validation_files/data/WB/structural/elements/hex20/mesh/ds_hex20_cuboid_modal.dat"
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
    prescribed_dof_data = {
        "element_type": "3d_element",
        "real_values": [0.0, 0.0, 0.0],
        "imag_values": [0.0, 0.0, 0.0],
        }

    model.properties._set_property("prescribed_dof", prescribed_dof_data, surface=1)

    ## Define the analysis setup
    analysis_setup = ModalAnalysisSetup(
        analysis_id = AnalysisID.STRUCTURAL_MODAL,
        modes_number = 40,
        sigma_factor = 0.01,
        )

    # Set the analysis setup
    model.set_analysis_setup(analysis_setup)

    assembler = StructuralAssembler(model)

    # Set the analysis frequency setup
    assembler.assemble_global_matrices_and_excitations(reorder=False, print_log=True)

    t0 = time()
    # Run modal analysis
    modal_solver = ModalSolver(assembler)
    modal_solver.solve(print_log=True)
    natural_frequencies = modal_solver.natural_frequencies
    dt = time() - t0
    print(f"Elapsed time to solve modal analysis: {round(dt, 4)}s")

    results_path = PROJECT_DIR / f"validation_files/data/WB/structural/elements/hex20/results/{integration_type}/"
    natural_frequencies_ref = np.loadtxt(results_path / "natural_frequencies_Ansys.dat")[:, 1]

    # modes_indices = np.arange(natural_frequencies.size)
    # nat_freq_data = np.array([modes_indices, natural_frequencies]).T
    # np.savetxt("natural_frequencies_Vibra.dat", nat_freq_data, fmt = "%i %.12e", delimiter=',')

    fnat_diff = 100 * (np.abs(natural_frequencies[1:] - natural_frequencies_ref[1:]) / natural_frequencies_ref[1:])
    assert np.max(fnat_diff) < 5e-3

    print()
    print(">>> RESULTS COMPARISON:")
    for i, nat_freq in enumerate(natural_frequencies):
        print(f"Mode {i+1}: {nat_freq : .8f} Hz (Vibra) vs {natural_frequencies_ref[i]: .8f} Hz (Ansys)")

    print(f"\nMaximum percentual difference: {np.max(fnat_diff) : .4e}")

if __name__ == "__main__":

    load_external_mesh_and_solve(integration_type="reduced_integration")