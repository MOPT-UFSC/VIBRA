import os
import logging
from pathlib import Path

import gmsh
import numpy as np

from vibra.utils.progress_status import ProgressStatus
from vibra.engine.mesher.element_info import (
    DEFAULT,
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
        self.entity_ranges = dict()
        self.element_info = DEFAULT
        self.nodal_coordinates = np.array([])
        self.lines_connectivity = np.array([])
        self.faces_connectivity = np.array([])
        self.solids_connectivity = np.array([])

    @classmethod
    def from_cad(
        cls,
        path: (str | Path),
        *,
        element_size: float = 0.0,
        element_info: ElementInfo = DEFAULT,
        tolerance: float = 1e-6,
        size_factor: float = 1.0,
        dimention: int = 3,
        threads: int = 1
    ):
        """
        Custom constructor so you can create a mesh with this sintax:
        mesh = Mesh.from_cad(...)

        I am not puting it in the default constructor because maybe
        we need to create a mesh from data that is not a CAD.

        Then you can create other constructor like this and avoid a
        lot of confusing if statements in the __init__ method.
        """
        obj = Mesh()
        obj.load_cad(
            path,
            element_size=element_size,
            element_info=element_info,
            tolerance=tolerance,
            size_factor=size_factor,
            dimention=dimention,
            threads=threads,
        )
        return obj

    def load_cad(
        self,
        path: (str | Path),
        *,
        element_size: float = 0.0,
        element_info: ElementInfo = DEFAULT,
        tolerance: float = 1e-6,
        size_factor: float = 1.0,
        dimention: int = 3,
        threads: int = 1
    ):
        path = Path(path)
        gmsh.initialize("", False)

        logging.info("Configuring Mesh" + ProgressStatus(5, 100))
        self._configure_mesh(element_info, element_size, tolerance, size_factor, threads)

        logging.info("Loading Geometry" + ProgressStatus(10, 100))
        gmsh.merge(str(path))

        self.dimention = min(dimention, gmsh.model.getDimension())
        self.element_info = element_info

        logging.info("Loading Geometry" + ProgressStatus(15, 100))
        gmsh.model.mesh.generate(dim=self.dimention)

        logging.info("Processing Mesh" + ProgressStatus(70, 100))
        self._process_mesh()
        gmsh.finalize()

    def export_nodes_coordinates(self, filename):
        header = "Node index || Coordinate x [m] || Coordinate y [m] || Coordinate z [m]"
        np.savetxt(
            filename,
            self.nodal_coordinates,
            delimiter=";",
            header=header,
            fmt=["%i", "%.16f", "%.16f", "%.16f"],
        )

    def export_faces_connectivity(self, filename):
        header = "Index || Element ID || Face ID || Element type ID || Connected Node IDs"
        np.savetxt(filename, self.faces_connectivity, delimiter=";", header=header, fmt="%i")

    def export_solids_connectivity(self, filename):
        header = "Index || Solid ID || Element type ID || Element ID || Connected Node IDs"
        np.savetxt(filename, self.solids_connectivity, delimiter=";", header=header, fmt="%i")

    def _configure_mesh(self, element_info, element_size, tolerance, size_factor, threads):
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", threads)
        gmsh.option.setNumber("Geometry.Tolerance", tolerance)
        gmsh.option.setNumber("Mesh.MeshSizeFactor", size_factor)
        if element_size != 0:
            gmsh.option.setNumber("Mesh.MeshSizeMin", element_size)
            gmsh.option.setNumber("Mesh.MeshSizeMax", element_size)

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
        self.nodal_coordinates = np.zeros((total_nodes, 4))
        self.nodal_coordinates[indexes - 1, 1:] = coords.reshape(-1, 3) / 1000
        self.nodal_coordinates[indexes - 1, :1] = indexes.reshape(-1, 1)

        connectivity_dim1 = dict()
        connectivity_dim2 = dict()
        connectivity_dim3 = dict()
        self.entity_ranges = dict()

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
                # not sure if it should be done here, but that is an easy way to fix the
                # connectivity to start from 0
                array_element_nodes -= 1

                elements_data[element_type] = {
                    "indexes": element_indexes[i],
                    "array_element_nodes": array_element_nodes,
                    "element_to_nodes": dict(zip(element_indexes[i], array_element_nodes)),
                }

            if dim == 0:  # Points
                # The index of points is one less than the
                # tag value, that is why this is the correct range.
                self.entity_ranges[dim, tag] = range(tag - 1, tag)

            elif dim == 1:  # Lines
                connectivity_dim1[dim, tag] = elements_data

            elif dim == 2:  # Surfaces
                connectivity_dim2[dim, tag] = elements_data

            elif dim == 3:  # Solids
                connectivity_dim3[dim, tag] = elements_data

        self.lines_connectivity = self._get_connectivity_array(connectivity_dim1)
        self.faces_connectivity = self._get_connectivity_array(connectivity_dim2)
        self.solids_connectivity = self._get_connectivity_array(connectivity_dim3)

    def _get_connectivity_array(self, input_dict):
        """
        The returned value is an array where each line is a connectivity
        and the collums follow this order:

        Index || Element index || Solid ID || Element type ID || Node IDS
        """

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
        for (entity_dim, entity_tag), e_data in input_dict.items():
            entity_start = start
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
            entity_end = end
            self.entity_ranges[entity_dim, entity_tag] = range(entity_start, entity_end)

        output_data[:, 0] = np.arange(1, n + 1, 1)

        return output_data


if __name__ == "__main__":
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Paralelepipedo.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Tetraedro.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Cubo_1m3.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Cilindro.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\script_files\\script_hex_elements.txt"

    path = "data/geometries/vessel.step"

    if not os.path.exists(path):
        raise FileNotFoundError

    mesh = Mesh()
    mesh.load_cad(path, 100, element_info=TETRAHEDRON_4)
