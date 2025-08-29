from vibra.engine.properties.material import Material
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.element_type import *
from vibra.engine.model import Model
# from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
# from vibra.engine.solvers.acoustic_modal_solver import AcousticModalSolver
# from vibra.engine.solvers.acoustic_harmonic_solver import AcousticHarmonicSolver
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.solvers.structural_modal_solver import StructuralModalSolver

from vibra.external_mesh.external_mesh_data import ExternalMeshData
from data.validation.load_external_data import LoadExternalData

import os
# import pytest

import matplotlib.pyplot as plt
import numpy as np

from pandas import read_excel
from openpyxl import load_workbook

from time import time

# @pytest.mark.slow
def load_external_mesh_and_solve():
    return

    # nodal_coordinates = np.array([[0, 0.0, 0.0, 0.0],
    #                               [1, 1.0, 0.0, 0.0],
    #                               [2, 0.0, 1.0, 0.0]], dtype=float)

    # face_connectivity = np.array([[0, 1, 3, 3, 0, 1, 2]], dtype=int)

    nodal_coordinates = np.array([[0, 0.0, 0.0, 0.0],
                                  [1, 0.5, 0.0, 0.0],
                                  [2, 1.0, 0.0, 0.0],
                                  [3, 0.0, 0.5, 0.0],
                                  [4, 0.5, 0.5, 0.0],
                                  [5, 1.0, 0.5, 0.0]], dtype=float)

    face_connectivity = np.array([  [0, 1, 3, 3, 0, 1, 3],
                                    [1, 1, 3, 3, 1, 4, 3],
                                    [2, 1, 3, 3, 1, 2, 4],
                                    [3, 1, 3, 3, 2, 5, 4]  ], dtype=int)

    # nodal_coordinates = np.array([[0, 0.0, 0.0, 0.0],
    #                               [1, 0.5, 0.0, 0.0],
    #                               [2, 1.0, 0.0, 0.0],
    #                               [3, 0.0, 0.5, 0.0],
    #                               [4, 0.5, 0.5, 0.0],
    #                               [5, 1.0, 0.5, 0.0],
    #                               [6, 0.0, 1.0, 0.0],
    #                               [7, 0.5, 1.0, 0.0],
    #                               [8, 1.0, 1.0, 0.0]], dtype=float)

    # face_connectivity = np.array([[0, 1, 3, 3, 0, 1, 3],
    #                               [1, 1, 3, 3, 1, 4, 3],
    #                               [2, 1, 3, 3, 1, 2, 4],
    #                               [3, 1, 3, 3, 2, 5, 4],
    #                               [4, 1, 3, 3, 3, 4, 6],
    #                               [5, 1, 3, 3, 4, 7, 6],
    #                               [6, 1, 3, 3, 4, 5, 7],
    #                               [7, 1, 3, 3, 5, 8, 7]], dtype=int)

    nodal_coordinates = np.loadtxt("C:/Repositorios/VIBRA/nodal_coordinates.dat", delimiter=",")
    face_connectivity = np.loadtxt("C:/Repositorios/VIBRA/faces_connectivity.dat", delimiter=",", dtype=int)

    mesh = Mesh()
    mesh.import_external_nodal_coordinates(nodal_coordinates, index_zero=False)
    # mesh.import_external_solids_connectivity(connectivity, index_zero=True, etype_tag=4)
    # mesh.export_nodal_coordinates("nodal_coordinates.dat")
    # mesh.export_solid_elements_connectivity("solids_connectivity.dat")
    mesh.element_type = TETRAHEDRON_4

    tag = 1
    mesh.elements_from_surface[tag] = face_connectivity[:, 0]
    mesh.external_connectivity_from_surfaces[tag] = face_connectivity[:, 4:]
    mesh.faces_connectivity = face_connectivity
    mesh.nodes_from_surfaces[tag] = nodal_coordinates[:, 0]

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

    # Set the defined fluid
    model = Model()
    model.mesh =  mesh
    model.generated_mesh = True

    model.set_material(material, surface=1)

    # Surface thickness
    data_st = { 
               "surface_thickness" : 0.012,
               "thickness_offset" : "middle",
               }

    model.properties._set_property("surface_thickness", data_st, surface=1)

    # Define the analysis setup
    analysis_setup = {
                      "analysis_id" : 2, 
                      "modes" : 40, 
                      "sigma_factor" : 1e-2
                      }
    
    # Set the analysis setup
    model.set_analysis_setup(analysis_setup)

    # Define and process the assemble
    assembler = StructuralAssembler(model)
    assembler.process_assemble()

    # Initialize the solver
    modal_solver = StructuralModalSolver(assembler)

    # t0 = time()
    # # Run modal analysis
    # modal_solver = StructuralModalSolver(assembler)
    # modal_solver.solve()
    # natural_frequencies = modal_solver.natural_frequencies
    # modal_shape = modal_solver.solution
    # dt = time() - t0
    # print(f"Elapsed time to solve modal analysis: {round(dt, 4)}s")
    # return

    t0 = time()

    print(f"\nNatural frequencies: \n {natural_frequencies}")

    # element_3d = model.acoustic_element_3d

    # mesh._process_face_elements_connected_to_nodes([1, 2])
    # mesh.compute_nodal_areas()