
import os
import sys
import gmsh
import logging
import numpy as np
from pathlib import Path

from vibra.engine.mesher.element_type import *
from vibra.utils.progress_status import ProgressStatus


class Mesh:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        self.dimension = 0
        self.entity_ranges = dict()
        self.element_type = DEFAULT_ELEMENT_TYPE
        self.nodal_coordinates = np.array([])
        self.lines_connectivity = np.array([])
        self.faces_connectivity = np.array([])
        self.solids_connectivity = np.array([])
        self.nodes_from_lines = dict()
        self.nodes_from_surfaces = dict()
        self.nodes_from_volumes = dict()
        self.entity_ranges = dict()
        self.surfaces_from_volumes = dict()


    @classmethod
    def from_cad(
        cls,
        path: (str | Path),
        *,
        minimum_element_size: float = 30.0,
        maximum_element_size: float = 30.0,
        element_type: ElementType = DEFAULT_ELEMENT_TYPE,
        geometry_tolerance: float = 1e-6,
        size_factor: float = 0.5,
        dimension: int = 3,
        threads: int = 1,
        gmsh_gui: bool = False,
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
            minimum_element_size = minimum_element_size,
            maximum_element_size = maximum_element_size,
            element_type = element_type,
            geometry_tolerance = geometry_tolerance,
            size_factor = size_factor,
            dimension = dimension,
            threads = threads,
            gmsh_gui = gmsh_gui,
        )
        return obj

    def load_cad(
        self,
        path: (str | Path),
        *,
        minimum_element_size: float = 30.0,
        maximum_element_size: float = 30.0,
        element_type: ElementType = DEFAULT_ELEMENT_TYPE,
        geometry_tolerance: float = 1e-6,
        size_factor: float = 0.50,
        dimension: int = 3,
        threads: int = 2,
        gmsh_gui: bool = False
    ):
        # path = "C:\Repositorios\VIBRA\data\examples\script_files\script_hex_elements.txt"
        self.basename = os.path.basename(path)

        path = Path(path)
        gmsh.initialize("", False)
        logging.info(f"Generating mesh from {path}" + ProgressStatus(0, 100))

        logging.info("Configuring Mesh" + ProgressStatus(5, 100))
        self._configure_mesh(
            element_type,
            minimum_element_size,
            maximum_element_size,
            geometry_tolerance,
            size_factor,
            threads,
        )

        logging.info("Loading Geometry" + ProgressStatus(10, 100))
        gmsh.merge(str(path))

        self.dimension = min(dimension, gmsh.model.getDimension())
        self.element_type = element_type

        logging.info("Loading Geometry" + ProgressStatus(15, 100))
        gmsh.model.mesh.generate(dim=self.dimension)

        logging.info("Processing Mesh" + ProgressStatus(70, 100))
        self._process_mesh()
        
        if gmsh_gui:
            if '-nopopup' not in sys.argv:
                gmsh.fltk.run()
        
        gmsh.finalize()

        if not os.path.exists("vibra/output_data"):
            os.mkdir("vibra/output_data")

        self.export_nodes_coordinates("vibra/output_data/nodal_coordinates.dat")
        self.export_faces_connectivity("vibra/output_data/faces_connectivitiy.dat")
        self.export_solids_connectivity("vibra/output_data/solids_connectivitiy.dat")

        logging.info(
            f"Mesh generated with {len(self.nodal_coordinates)} nodes"
            f", {len(self.lines_connectivity)} dim 1"
            f", {len(self.faces_connectivity)} dim 2"
            f"and {len(self.solids_connectivity)} dim 3 elements" + ProgressStatus(100, 100)
        )

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

    def _configure_mesh(
        self,
        element_type,
        minimum_element_size,
        maximum_element_size,
        tolerance,
        size_factor,
        threads,
    ):

        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", threads)
        gmsh.option.setNumber("Geometry.Tolerance", tolerance)
        
        if size_factor != 0:
            gmsh.option.setNumber("Mesh.MeshSizeFactor", size_factor)
        else:
            gmsh.option.setNumber("Mesh.MeshSizeMin", minimum_element_size)
            gmsh.option.setNumber("Mesh.MeshSizeMax", maximum_element_size)

        if "script" not in self.basename:
            gmsh.option.setNumber("Mesh.Algorithm", element_type.algorithm_2d)
            gmsh.option.setNumber("Mesh.Algorithm3D", element_type.algorithm_3d)
            gmsh.option.setNumber("Mesh.RecombinationAlgorithm", element_type.recombination_algorithm)
            gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", element_type.subdivision_algorithm)
            gmsh.option.setNumber("Mesh.RecombineAll", element_type.recombine_all)

        gmsh.option.setNumber("Mesh.ElementOrder", element_type.element_order)
        gmsh.option.setNumber("Mesh.SecondOrderIncomplete", element_type.second_order_incomplete)


    def _process_mesh(self):
        """
        Transform gmsh data in a more manageable format (aka nodal coords and connectivity).
        """
        self.reset_variables()
        indexes, coords, _ = gmsh.model.mesh.getNodes(includeBoundary=True)
        total_nodes = int(np.max(indexes))
        self.nodal_coordinates = np.zeros((total_nodes, 4))
        self.nodal_coordinates[indexes - 1, 1:] = coords.reshape(-1, 3) / 1000
        self.nodal_coordinates[indexes - 1, :1] = indexes.reshape(-1, 1)

        connectivity_dim1 = dict()
        connectivity_dim2 = dict()
        connectivity_dim3 = dict()

        for dim, tag in gmsh.model.getEntities():

            if dim == 3:
                _, downwards = gmsh.model.getAdjacencies(dim, tag)
                self.surfaces_from_volumes[tag] = list(downwards)

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
                self.nodes_from_lines[tag] = np.array([*set(element_nodes[0])], dtype=int) - 1

            elif dim == 2:  # Surfaces
                connectivity_dim2[dim, tag] = elements_data
                self.nodes_from_surfaces[tag] = np.array([*set(element_nodes[0])], dtype=int) - 1

            elif dim == 3:  # Solids
                connectivity_dim3[dim, tag] = elements_data
                self.nodes_from_volumes[tag] = np.array([*set(element_nodes[0])], dtype=int) - 1

        self.lines_connectivity = self._get_connectivity_array(connectivity_dim1)
        self.faces_connectivity = self._get_connectivity_array(connectivity_dim2)
        self.solids_connectivity = self._get_connectivity_array(connectivity_dim3)

    def get_model_areas(self, path):
        """ This method returns returns the all surface area processed using 
            gmsh internal functions.

        """

        surfaces_areas = dict()
        bodies_volumes = dict()

        # The adoption of quadratic elements ensures better results for area calculations.
        element_type = TETRAHEDRON_10
        gmsh.initialize("", False)

        gmsh.merge(str(path))

        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", 4)
        gmsh.option.setNumber("Geometry.Tolerance", 1e-8)
        gmsh.option.setNumber("Mesh.MeshSizeFactor", 0.1)

        gmsh.option.setNumber("Mesh.Algorithm", element_type.algorithm_2d)
        gmsh.option.setNumber("Mesh.Algorithm3D", element_type.algorithm_3d)
        gmsh.option.setNumber("Mesh.RecombinationAlgorithm", element_type.recombination_algorithm)
        gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", element_type.subdivision_algorithm)
        gmsh.option.setNumber("Mesh.RecombineAll", element_type.recombine_all)

        gmsh.option.setNumber("Mesh.ElementOrder", element_type.element_order)
        gmsh.option.setNumber("Mesh.SecondOrderIncomplete", element_type.second_order_incomplete)

        gmsh.model.mesh.generate(dim=2)

        for dim, tag in gmsh.model.getEntities():
    
            if dim == 2:  # Surfaces

                p = gmsh.model.addPhysicalGroup(2, [tag])
                gmsh.plugin.setNumber("MeshVolume", "Dimension", 2)
                gmsh.plugin.setNumber("MeshVolume", "PhysicalGroup", p)
                gmsh.plugin.run("MeshVolume")
                views = gmsh.view.getTags()
                _, _, data = gmsh.view.getListData(views[-1])

                surfaces_areas[tag] = data[-1][-1]/(1e6)

            # maybe it is going to be necessary evaluate the bodies volumes too
            # elif dim == 3:  # Solids
    
            #     p = gmsh.model.addPhysicalGroup(3, [tag])
            #     gmsh.plugin.setNumber("MeshVolume", "Dimension", 3)
            #     gmsh.plugin.setNumber("MeshVolume", "PhysicalGroup", p)
            #     gmsh.plugin.run("MeshVolume")
            #     views = gmsh.view.getTags()
            #     _, _, data = gmsh.view.getListData(views[-1])

            #     bodies_volumes[tag] = data[-1][-1]
        
        gmsh.finalize()

        return surfaces_areas#, bodies_volumes

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
    mesh.load_cad(path, 100, element_type=TETRAHEDRON_4)
