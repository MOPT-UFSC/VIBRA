import numpy as np
import gmsh
from pathlib import Path


class Mesh:
    def __init__(self):
        self.nodal_coordinates = np.array([])
        
        self.lines_connectivity = np.array([])
        self.faces_connectivity = np.array([])
        self.solids_connectivity = np.array([])

        # self.points = []
        # self.lines = []
        # self.faces = []

        # self.points_entities = dict()
        # self.line_entities = dict()
        # self.face_entities = dict()

    def load_cad(self, path: (str | Path), mesh_configuration):
        path = Path(path)

        gmsh.initialize("", False)
        self._configure_mesh(mesh_configuration)
        gmsh.merge(str(path))
        gmsh.model.mesh.generate(dim=mesh_configuration.dimention)
        self._process_mesh(mesh_configuration)

    def _configure_mesh(self, mesh_configuration):
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)

        gmsh.option.setNumber("Mesh.MeshSizeMin", mesh_configuration.element_size)
        gmsh.option.setNumber("Mesh.MeshSizeMax", mesh_configuration.element_size)
        gmsh.option.setNumber("Mesh.MeshSizeFactor", mesh_configuration.size_factor)
        gmsh.option.setNumber("Geometry.Tolerance", mesh_configuration.tolerance)

        gmsh.option.setNumber("Mesh.Algorithm", mesh_configuration.algorithm_2d)
        gmsh.option.setNumber("Mesh.Algorithm3D", mesh_configuration.algorithm_3d)
        gmsh.option.setNumber("Mesh.RecombinationAlgorithm", mesh_configuration.recombination_algorithm)
        gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", mesh_configuration.subdivision_algorithm)
        
        gmsh.option.setNumber("General.NumThreads", mesh_configuration.number_of_threads)
        
    def _process_mesh(self, mesh_configuration):
        indexes, coords, _ = gmsh.model.mesh.getNodes(includeBoundary=True)
        total_nodes = int(np.max(indexes))
        self.nodal_coordinates = np.zeros(total_nodes * 3).reshape(-1, 3)
        self.nodal_coordinates[indexes - 1] = coords.reshape(-1, 3)

        connectivity_dim1 = dict()
        connectivity_dim2 = dict()
        connectivity_dim3 = dict()

        for dim, tag in gmsh.model.getEntities():
            element_types, element_indexes, element_nodes = gmsh.model.mesh.getElements(dim, tag)

            if not element_indexes:
                continue

            
            _elements_data = dict()
            for i, element_type in enumerate(element_types):
                _, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(element_type)

                array_element_nodes = np.array(element_nodes[i]).reshape(-1, nodes_per_element)    

                _elements_data[element_type] = {    "indexes"             : element_indexes[i],
                                                    "array_element_nodes" : array_element_nodes,
                                                    "element_to_nodes"    : dict(zip(element_indexes[i], array_element_nodes))    } 
                
        #     *_, _points = gmsh.model.mesh.getElements(dim, tag)

        #     if _points:
        #         _points = _points[0]
        #     else:
        #         continue

        #     if dim == 0:
        #         entities[dim, tag].append(tag - 1)

        #     elif dim == 1:
        #         offset = len(lines)
        #         for i, (a, b) in enumerate(_points.reshape(-1, 2) - 1):
        #             lines.append((a, b))
        #             entities[dim, tag].append(i + offset)

        #     elif dim == 2:
        #         offset = len(faces)

        #         # I am assuming all the faces are triangles
        #         for i, (a, b, c) in enumerate(_points.reshape(-1, 3) - 1):
        #             faces.append((a, b, c))
        #             entities[dim, tag].append(i + offset)

        #     else:
        #         NotImplemented



