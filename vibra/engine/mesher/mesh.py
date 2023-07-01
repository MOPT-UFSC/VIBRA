import os
import sys
from pathlib import Path

import gmsh
import numpy as np

from vibra.engine.mesher.element_info import (
    HEXAHEDRON_8,
    HEXAHEDRON_20,
    TETRAHEDRON_4,
    TETRAHEDRON_10,
    ElementInfo,
)


class Mesh:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        self.dimention = 0
        self.nodal_coordinates_2 = np.array([])
        self.lines_connectivity_2 = np.array([])
        self.faces_connectivity_2 = np.array([])
        self.solids_connectivity_2 = np.array([])

    def load_cad(
        self,
        path: (str | Path),
        element_info: ElementInfo,
        element_size: float,
        *,
        tolerance: float = 1e-6,
        size_factor: float = 1.0,
        dimention: int = 3,
        threads: int = 1
    ):
        path = Path(path)
        gmsh.initialize("", False)

        self._configure_mesh(element_info, element_size, tolerance, size_factor, threads)
        gmsh.merge(str(path))

        self.dimention = min(dimention, gmsh.model.getDimension())
        gmsh.model.mesh.generate(dim=self.dimention)
        self._process_mesh()
        gmsh.finalize()

    def export_nodes_coordinates(self, filename):
        header = "Node index || Coordinate x [m] || Coordinate y [m] || Coordinate z [m]"
        np.savetxt(
            filename,
            self.nodal_coordinates_2,
            delimiter=";",
            header=header,
            fmt=["%i", "%.16f", "%.16f", "%.16f"],
        )

    def export_faces_connectivity(self, filename):
        header = "Index || Element ID || Face ID || Element type ID || Connected Node IDs"
        np.savetxt(filename, self.faces_connectivity_2, delimiter=";", header=header, fmt="%i")

    def export_solids_connectivity(self, filename):
        header = "Index || Solid ID || Element type ID || Element ID || Connected Node IDs"
        np.savetxt(filename, self.solids_connectivity_2, delimiter=";", header=header, fmt="%i")

    def _configure_mesh(self, element_info, element_size, tolerance, size_factor, threads):
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("Mesh.MeshSizeMin", element_size)
        gmsh.option.setNumber("Mesh.MeshSizeMax", element_size)
        gmsh.option.setNumber("Geometry.Tolerance", tolerance)
        gmsh.option.setNumber("Mesh.MeshSizeFactor", size_factor)
        gmsh.option.setNumber("General.NumThreads", threads)

        gmsh.option.setNumber("Mesh.Algorithm", element_info.algorithm_2d)
        gmsh.option.setNumber("Mesh.Algorithm3D", element_info.algorithm_3d)
        gmsh.option.setNumber("Mesh.RecombinationAlgorithm", element_info.recombination_algorithm)
        gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", element_info.subdivision_algorithm)
        gmsh.option.setNumber("Mesh.RecombineAll", element_info.recombine_all)
        gmsh.option.setNumber("Mesh.SecondOrderIncomplete", element_info.second_order_incomplete)
        gmsh.option.setNumber("Mesh.ElementOrder", element_info.element_order)

    def _process_mesh(self):
        """
        Transform gmsh data in a more manageable format (aka nodal coords and connectivity).
        """
        indexes, coords, _ = gmsh.model.mesh.getNodes(includeBoundary=True)
        total_nodes = int(np.max(indexes))
        self.nodal_coordinates_2 = np.zeros((total_nodes, 4))
        self.nodal_coordinates_2[indexes - 1, 1:] = coords.reshape(-1, 3) / 1000
        self.nodal_coordinates_2[indexes - 1, :1] = indexes.reshape(-1, 1)

        connectivity_dim2 = dict()
        connectivity_dim3 = dict()

        for dim, tag in gmsh.model.getEntities():
            elements_data = dict()
            element_types, element_indexes, element_nodes = gmsh.model.mesh.getElements(dim, tag)

            if not element_indexes:
                continue

            for i, element_type in enumerate(element_types):
                _, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(
                    element_type
                )

                array_element_nodes = np.array(element_nodes[i]).reshape(-1, nodes_per_element)

                elements_data[element_type] = {
                    "indexes": element_indexes[i],
                    "array_element_nodes": array_element_nodes,
                    "element_to_nodes": dict(zip(element_indexes[i], array_element_nodes)),
                }

            if dim == 1:  # Lines
                pass

            elif dim == 2:  # Surfaces
                connectivity_dim2[tag] = elements_data

            elif dim == 3:  # Solids
                connectivity_dim3[tag] = elements_data

        self.faces_connectivity_2 = self._get_connectivity_array(connectivity_dim2)
        self.solids_connectivity_2 = self._get_connectivity_array(connectivity_dim3)

    def _get_connectivity_array(self, input_dict):
        if not isinstance(input_dict, dict):
            raise TypeError("get_connectivity_data only accepts dicts as input.")

        max_cols = 0
        n_list = []
        for data_0 in input_dict.values():
            for data_1 in data_0.values():
                if "indexes" in data_1.keys():
                    n_list.append(len(data_1["indexes"]))
                    array_nodes = data_1["array_element_nodes"]
                    if max_cols < array_nodes.shape[1]:
                        max_cols = array_nodes.shape[1]

        n = int(np.sum(n_list))
        output_data = np.zeros((n, max_cols + 4), dtype=int)

        start, end, ind = 0, 0, 0
        for entity_tag, e_data in input_dict.items():
            for etype_tag, data in e_data.items():
                end += n_list[ind]
                indexes = data["indexes"]
                nodes = data["array_element_nodes"]
                rows = len(indexes)
                cols = nodes.shape[1]

                output_data[start:end, 1] = np.ones(rows) * entity_tag
                output_data[start:end, 2] = np.ones(rows) * etype_tag
                output_data[start:end, 3] = indexes
                output_data[start:end, 4 : 4 + cols] = nodes
                start = end
                ind += 1

        output_data[:, 0] = np.arange(1, n + 1, 1)

        return output_data


if __name__ == "__main__":
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Paralelepipedo.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Tetraedro.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Cubo_1m3.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Cilindro.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\script_files\\script_hex_elements.txt"

    path = "data/geometries/geom_akio.stp"

    if not os.path.exists(path):
        raise FileNotFoundError

    mesh = Mesh()
    mesh.load_cad(path, TETRAHEDRON_4, 100)
