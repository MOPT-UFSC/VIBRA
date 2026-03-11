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

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

import os
import numpy as np
import matplotlib.pyplot as plt

from time import time
from pathlib import Path


stresses_labels = [
    "sigma_x", 
    "sigma_y", 
    "sigma_z", 
    "tau_xy", 
    "tau_xz",
    "tau_yz", 
    ]


def load_external_mesh_and_solve(case: str, extra_shape_function: bool = False):

    # start decoding the Ansys script file (ds.dat file or input file)
    mesh_path = f"validation_files/data/WB/structural/elements/hex8/mesh/ds_hex8_{case}_modal.dat"

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
    esf = extra_shape_function

    element_options = {
        "hex8" : {"extra_shape_functions" : esf}
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
        "real_values": [0.0, 1.0, 0.0],
        "imag_values": [0.0, 0.0, 0.0],
        "nodal_attribution": True,
        "averaged": False,
        }

    model.properties._set_property("nodal_loads", nodal_load_data, surface=2)

    ## Define the analysis frequency setup

    df = 20
    f_min = 20
    f_max = 40
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

    Ke = assembler.data_K[0, :, :]
    Me = assembler.data_M[0, :, :]

    folder = "with_esf" if esf else "without_esf"
    results_path = PROJECT_DIR / f"validation_files/data/WB/structural/elements/hex8/results/{folder}/{case}/"

    # Ke_ansys = np.loadtxt(results_path / "Ke_ansys.csv", delimiter=",")
    # Me_ansys = np.loadtxt(results_path / "Me_ansys.csv", delimiter=",")

    # mask = np.where(Me_ansys != 0)

    # dev_Ke = np.abs((Ke_ansys - Ke) / Ke_ansys)
    # dev_Me = np.abs((Me_ansys[mask] - Me[mask]) / Me_ansys[mask])

    # print()
    # print(f"Maximum relative deviation for Ke: {np.max(dev_Ke)}")
    # print(f"Maximum relative deviation for Me: {np.max(dev_Me)}")
    # print()

    n_elements = int(case.split("_")[1].replace("e", ""))

    for elem_id in range(1, n_elements+1, 1):

        Ke = assembler.data_K[elem_id-1, :, :]
        Me = assembler.data_M[elem_id-1, :, :]

        Ke_ansys = np.loadtxt(results_path / f"Ke_{elem_id}_ansys.txt", skiprows=7)
        Me_ansys = np.loadtxt(results_path / f"Me_{elem_id}_ansys.txt", skiprows=7)

        triu_ind = np.triu_indices(24)

        mask = np.where(Me_ansys != 0)

        dev_Ke = np.abs((Ke_ansys - Ke[triu_ind]) / Ke_ansys)
        dev_Me = np.abs((Me_ansys[mask] - Me[triu_ind].flatten()[mask]) / Me_ansys[mask])

        print()
        print(f"Results for element #{elem_id}:")
        print(f"Maximum relative deviation for Ke: {np.max(dev_Ke)}")
        print(f"Maximum relative deviation for Me: {np.max(dev_Me)}")
        print()


    # np.savetxt(f"Ke_vibra.csv", Ke, delimiter=",")
    # np.savetxt(f"Me_vibra.csv", Me, delimiter=",")

    # t0 = time()
    # # Run modal analysis
    # harmonic_solver = HarmonicSolver(assembler)
    # solution = harmonic_solver.solve_direct(print_log=True)
    # dt = time() - t0
    # print(f"Elapsed time to solve modal analysis: {round(dt, 4)}s")

if __name__ == "__main__":
    load_external_mesh_and_solve("cube_512e", extra_shape_function=True)