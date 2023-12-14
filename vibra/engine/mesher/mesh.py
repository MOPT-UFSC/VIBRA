import logging
import os
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile
from collections import defaultdict

import gmsh
import numpy as np

from vibra.engine.mesher.element_type import *
from vibra.engine.mesher.geometry_setup import GeometrySetup
from vibra.engine.mesher.reordering import Reordering
from vibra.utils.progress_status import ProgressStatus

# FieldsList=[]


class Mesh:
    def __init__(self):
        self.geometry_setup = None
        self.mesh_setup = None
        self.reset_variables()

    def reset_variables(self):
        self.reordering = None
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
        self.gmsh_elements_from_surfaces = dict()
        self.gmsh_elements_from_volumes = dict()
        self.elements_from_volumes = dict()
        self.elements_from_surfaces = dict()
        self.volume_from_element = dict()
        self.surface_from_element = dict()
        self.entity_ranges = dict()
        self.surfaces_from_volumes = dict()
        self.connectivity_from_surfaces = dict()
        self.nodes_from_face_element = dict()
        self.nodes_from_solid_element = dict()
        self.solid_elements_center = dict()
        self.volume_from_surface = defaultdict(list)
        self.face_elements_from_nodes = defaultdict(list)
        self.solid_elements_from_nodes = defaultdict(list)

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
        path = Path(path)

        obj = Mesh()
        obj.load_cad(
            path,
            minimum_element_size=minimum_element_size,
            maximum_element_size=maximum_element_size,
            element_type=element_type,
            geometry_tolerance=geometry_tolerance,
            size_factor=size_factor,
            dimension=dimension,
            threads=threads,
            gmsh_gui=gmsh_gui,
        )

        # saves the data to edit mesh parameters later
        with open(path, "r", encoding="iso-8859-1") as file:
            obj.geometry_setup = GeometrySetup(
                file.read(),
                suffix=path.suffix,
            )

        return obj

    def update_parameters(self, *args, **kwargs):
        self.load_cad_string(
            self.geometry_setup.data,
            self.geometry_setup.suffix,
            *args,
            **kwargs,
        )

    def load_cad_string(self, string: str, suffix: str, *args, **kwargs):
        # sadly in windows we cannot use the with statement
        # that removes the files automatically =(
        tmp = NamedTemporaryFile(suffix=suffix, delete=False)
        tmp_path = Path(tmp.name)

        with open(tmp_path, "w") as file:
            file.write(string)

        self.load_cad(tmp.name, *args, **kwargs)
        tmp.close()
        tmp_path.unlink(missing_ok=True)  # deletes the file

        self.geometry_setup = GeometrySetup(string, suffix)

    def load_cad(   self,
                    path: (str | Path),
                    *,
                    minimum_element_size: float = 30.0,
                    maximum_element_size: float = 30.0,
                    element_type: ElementType = DEFAULT_ELEMENT_TYPE,
                    geometry_tolerance: float = 1e-6,
                    size_factor: float = 0.50,
                    dimension: int = 3,
                    threads: int = 2,
                    gmsh_gui: bool = False ):
        
        self.mesh_setup = dict( minimum_element_size=minimum_element_size,
                                maximum_element_size=maximum_element_size,
                                element_type=element_type,
                                geometry_tolerance=geometry_tolerance,
                                size_factor=size_factor,
                                dimension=dimension,
                                threads=threads )

        path = Path(path)
        gmsh.initialize("", False)
        logging.info(f"Generating mesh from {path}")

        logging.info("Configuring Mesh" + ProgressStatus(5, 100))
        self._configure_mesh(   element_type,
                                minimum_element_size,
                                maximum_element_size,
                                geometry_tolerance,
                                size_factor,
                                threads,   )

        logging.info("Loading Geometry" + ProgressStatus(10, 100))
        gmsh.merge(str(path))

        self.dimension = min(dimension, gmsh.model.getDimension())
        self.element_type = element_type
        
        self._merge_nodes_from_adjacent_volumes()
        
        logging.info("Loading Geometry" + ProgressStatus(15, 100))
        gmsh.model.mesh.generate(dim=element_type.dimensions)
        gmsh.model.mesh.removeDuplicateNodes()

        logging.info("Processing Mesh" + ProgressStatus(70, 100))
        self._process_mesh()

        if gmsh_gui:
            if "-nopopup" not in sys.argv:
                gmsh.fltk.run()

        gmsh.finalize()

        logging.info(   f"Mesh generated with {len(self.nodal_coordinates)} nodes"
                        f", {len(self.lines_connectivity)} dim 1"
                        f", {len(self.faces_connectivity)} dim 2"
                        f"and {len(self.solids_connectivity)} dim 3 elements"   )

    def _merge_nodes_from_adjacent_volumes(self):
        """ This method merges all nodes from adjacent volumes.
        """
        volumes_list = gmsh.model.getEntities(3)
        gmsh.model.occ.fragment(volumes_list,volumes_list)
        gmsh.model.occ.synchronize()    

    def import_nodes_coordinates(self, filename):
        header = "Node index || Coordinate x [m] || Coordinate y [m] || Coordinate z [m]"
        return np.loadtxt(
            filename,
            delimiter=";",
            header=header,
            fmt=["%i", "%.16f", "%.16f", "%.16f"],
        )

    def import_faces_connectivity(self, filename):
        header = "Index || Element ID || Face ID || Element type ID || Connected Node IDs"
        return np.loadtxt(filename, delimiter=";", header=header, fmt="%i")

    def import_solids_connectivity(self, filename):
        header = "Index || Solid ID || Element type ID || Element ID || Connected Node IDs"
        return np.loadtxt(filename, delimiter=";", header=header, fmt="%i")
    
    def import_external_nodal_coordinates(self, filename, index_zero=True):
        """
        """
        data = np.loadtxt(filename, delimiter=",")
        rows, cols = data.shape
        
        indexes = data[:,0]
        if index_zero:
            indexes -= 1   

        self.nodal_coordinates = np.zeros((rows, cols), dtype=float)
        self.nodal_coordinates[:,0] = indexes
        self.nodal_coordinates[:,1:] = data[:,1:]

    def import_external_connectivity(self, filename, index_zero=True, etype_tag=1, e_nodes=1):
        """
        """
        data = np.loadtxt(filename, delimiter=",")
        rows, cols = data.shape
        
        indexes = data[:,0]
        connect = data[:, 1:]
        if index_zero:
            connect -= 1

        aux = np.ones(rows)
        self.solids_connectivity = np.zeros((rows, cols+3), dtype=int)
        self.solids_connectivity[:, 0] = indexes
        self.solids_connectivity[:, 1] = aux
        self.solids_connectivity[:, 2] = aux*etype_tag
        self.solids_connectivity[:, 3] = aux*e_nodes
        self.solids_connectivity[:, 4:] = connect
        #
        self.elements_from_volumes.clear()
        self.elements_from_volumes[1] = np.arange(rows, dtype=int)

    def export_nodes_coordinates(self, filename):
        fmt = ["%i", "%.16f", "%.16f", "%.16f"]
        header = "Node index || Coordinate x [m] || Coordinate y [m] || Coordinate z [m]"
        np.savetxt(filename, self.nodal_coordinates, delimiter=";", header=header, fmt=fmt)

    def export_faces_connectivity(self, filename):
        header = "Index || Element ID || Face ID || Element type ID || Connected Node IDs"
        np.savetxt(filename, self.faces_connectivity, delimiter=";", header=header, fmt="%i")

    def export_solids_connectivity(self, filename):
        header = "Index || Solid ID || Element type ID || Element ID || Connected Node IDs"
        np.savetxt(filename, self.solids_connectivity, delimiter=";", header=header, fmt="%i")

    def local_mesh_refine(self, lc_geral, mesh_refinement_parameters):
        fields_list = []
        gmsh.model.mesh.field.add("Constant")
        gmsh.model.mesh.field.setNumbers(1, "SurfacesList", [])
        gmsh.model.mesh.field.setNumber(1, "VOut", lc_geral)
        fields_list.append(1)

        for size, faces in mesh_refinement_parameters:
            threshold_type = gmsh.model.mesh.field.add("Constant")
            gmsh.model.mesh.field.setNumbers(threshold_type, "SurfacesList", faces)
            gmsh.model.mesh.field.setNumber(threshold_type, "VIn", size)
            fields_list.append(threshold_type)

        minimum_field = gmsh.model.mesh.field.add("Min")
        gmsh.model.mesh.field.setNumbers(minimum_field, "FieldsList", fields_list)
        gmsh.model.mesh.field.setAsBackgroundMesh(minimum_field)

    def _configure_mesh(
        self,
        element_type,
        minimum_element_size,
        maximum_element_size,
        tolerance,
        size_factor,
        threads,
        mesh_refinement_parameters=None,
    ):
        if mesh_refinement_parameters is None:
            mesh_refinement_parameters = []

        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", threads)
        gmsh.option.setNumber("Geometry.Tolerance", tolerance)

        if size_factor != 0:
            gmsh.option.setNumber("Mesh.MeshSizeFactor", size_factor)
        else:
            # gmsh.option.setNumber("Mesh.MeshSizeMin", minimum_element_size)
            # gmsh.option.setNumber("Mesh.MeshSizeMax", maximum_element_size)
            self.local_mesh_refine(minimum_element_size, mesh_refinement_parameters)

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
        indexes, coords, _ = gmsh.model.mesh.getNodes(includeBoundary=True)
        total_nodes = int(np.max(indexes))
        self.nodal_coordinates = np.zeros((total_nodes, 4))
        self.nodal_coordinates[indexes - 1, 1:] = coords.reshape(-1, 3) / 1000
        self.nodal_coordinates[indexes - 1, :1] = indexes.reshape(-1, 1) - 1

        connectivity_dim1 = dict()
        connectivity_dim2 = dict()
        connectivity_dim3 = dict()

        self.nodes_from_lines.clear()
        self.nodes_from_surfaces.clear()
        self.nodes_from_volumes.clear()

        self.surfaces_from_volumes.clear()
        self.volume_from_surface.clear()
        self.gmsh_elements_from_surfaces.clear()
        self.gmsh_elements_from_volumes.clear()

        for dim, tag in gmsh.model.getEntities():
            if dim == 3:
                _, downwards = gmsh.model.getAdjacencies(dim, tag)
                self.surfaces_from_volumes[tag] = list(downwards)
                for surf_id in list(downwards):
                    self.volume_from_surface[surf_id].append(tag)

            elements_data = dict()
            element_types, element_indexes, element_nodes = gmsh.model.mesh.getElements(dim, tag)

            if not element_indexes:
                continue

            for i, element_type in enumerate(element_types):
                _, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(element_type)

                array_element_nodes = np.array(element_nodes[i]).reshape(-1, nodes_per_element)
                array_element_nodes -= 1  # index connectivity from 0

                elements_data[element_type] = { "indexes": element_indexes[i],
                                                "array_element_nodes": array_element_nodes,
                                                "element_to_nodes": dict(zip(element_indexes[i], array_element_nodes)) }

            if dim == 0:  # Points
                # The index of points is one less than the
                # tag value, that is why this is the correct range.
                self.entity_ranges[dim, tag] = (tag - 1, tag)

            elif dim == 1:  # Lines
                connectivity_dim1[dim, tag] = elements_data
                self.nodes_from_lines[tag] = np.array([*set(element_nodes[0])], dtype=int) - 1

            elif dim == 2:  # Surfaces
                connectivity_dim2[dim, tag] = elements_data
                self.nodes_from_surfaces[tag] = np.array([*set(element_nodes[0])], dtype=int) - 1
                array_element_indexes = np.array([*set(element_indexes[0])], dtype=int) - 1
                self.connectivity_from_surfaces[tag] = {"element_indexes" : array_element_indexes,
                                                        "connectivity" : array_element_nodes}
                self.gmsh_elements_from_surfaces[tag] = np.array([*set(element_indexes[0])], dtype=int)

            elif dim == 3:  # Solids
                connectivity_dim3[dim, tag] = elements_data
                self.nodes_from_volumes[tag] = np.array([*set(element_nodes[0])], dtype=int) - 1
                self.gmsh_elements_from_volumes[tag] = np.array([*set(element_indexes[0])], dtype=int)
        
        self.lines_connectivity, self.map_line_elements = self._get_connectivity_array(connectivity_dim1)
        self.faces_connectivity, self.map_face_elements = self._get_connectivity_array(connectivity_dim2)
        self.solids_connectivity, self.map_solid_elements = self._get_connectivity_array(connectivity_dim3)
        #
        self._maps_surfaces_by_elements()
        self._maps_volumes_by_elements()

    def _maps_surfaces_by_elements(self):
        self.surface_from_element.clear()
        self.elements_from_surfaces.clear()
        for tag, gmsh_indexes in self.elements_from_surfaces.items():
            n = len(gmsh_indexes)
            internal_indexes = np.zeros(n, dtype=int)
            for i, gmsh_index in enumerate(gmsh_indexes):
                index = self.map_face_elements[gmsh_index]
                internal_indexes[i] = index
                self.surface_from_element[index] = tag
            self.elements_from_surfaces[tag] = internal_indexes

    def _maps_volumes_by_elements(self):
        self.volume_from_element.clear()
        self.elements_from_volumes.clear()
        for tag, gmsh_indexes in self.gmsh_elements_from_volumes.items():
            n = len(gmsh_indexes)
            internal_indexes = np.zeros(n, dtype=int)
            for i, gmsh_index in enumerate(gmsh_indexes):
                index = self.map_solid_elements[gmsh_index]
                internal_indexes[i] = index
                self.volume_from_element[index] = tag
            self.elements_from_volumes[tag] = internal_indexes

    def _process_face_elements_connected_to_nodes(self):
        self.nodes_from_face_element.clear()
        self.face_elements_from_nodes.clear()
        for i, connected_nodes in enumerate(self.faces_connectivity[:, 4:]):
            self.nodes_from_face_element[i] = connected_nodes
            for node in connected_nodes:
                self.face_elements_from_nodes[node].append(i)

    def _process_solid_elements_connected_to_nodes(self):
        self.nodes_from_solid_element.clear()
        self.solid_elements_from_nodes.clear()
        for i, connected_nodes in enumerate(self.solids_connectivity[:, 4:]):
            self.nodes_from_solid_element[i] = connected_nodes
            for node in connected_nodes:
                self.solid_elements_from_nodes[node].append(i)

    def _process_nodes_reordering(self):
        """ This method processes the nodes reordering to reduce the global matrices 
            bandwidth and improve the solution performance.
        """
        # print(f"Nodal coordinates: {self.nodal_coordinates.shape}")
        # print(f"Connectivity: {self.solids_connectivity.shape}")
        # np.savetxt("nodal_coordinates.dat", self.nodal_coordinates, delimiter=",", fmt=["%i", "%.16f", "%.16f", "%.16f"])
        # np.savetxt("faces_connectivity.dat", self.faces_connectivity, delimiter=",", fmt='%i')
        # np.savetxt("solids_connectivity.dat", self.solids_connectivity, delimiter=",", fmt='%i')
        
        self.reordering = Reordering(self)
        self.reordering._process_reordering()
        self.nodal_coordinates = self.reordering.get_new_nodal_coordinates()
        self.lines_connectivity = self.reordering.get_new_connectivity(self.lines_connectivity)
        self.faces_connectivity = self.reordering.get_new_connectivity(self.faces_connectivity)
        self.solids_connectivity = self.reordering.get_new_connectivity(self.solids_connectivity)
        self.nodes_from_lines = self.reordering.updates_nodes_from(self.nodes_from_lines)
        self.nodes_from_surfaces = self.reordering.updates_nodes_from(self.nodes_from_surfaces)
        self.nodes_from_volumes = self.reordering.updates_nodes_from(self.nodes_from_volumes)
        self.connectivity_from_surfaces = self.reordering.updates_nodes_from(self.connectivity_from_surfaces)

        # self._process_face_elements_connected_to_nodes()
        self._process_solid_elements_connected_to_nodes()
        self._process_element_centroids()

        # print(f"Nodal coordinates (after): {self.nodal_coordinates.shape}")
        # print(f"Connectivity (after): {self.solids_connectivity.shape}")
        # np.savetxt("nodal_coordinates_reordered.dat", self.nodal_coordinates, delimiter=",", fmt=["%i", "%.16f", "%.16f", "%.16f"])
        # np.savetxt("faces_connectivity_reordered.dat", self.faces_connectivity, delimiter=",", fmt='%i')
        # np.savetxt("solids_connectivity_reordered.dat", self.solids_connectivity, delimiter=",", fmt='%i')

    def get_mesh_info(self):
        n_nodes = self.nodal_coordinates.shape[0]
        n_face_elements = self.faces_connectivity.shape[0]
        n_solid_elements = self.solids_connectivity.shape[0]
        return n_nodes, n_face_elements, n_solid_elements

    def get_geometry_info(self):
        points = len(self.entity_ranges)
        lines = len(self.nodes_from_lines)
        surfaces = len(self.nodes_from_surfaces)
        volumes = len(self.nodes_from_volumes)
        return points, lines, surfaces, volumes

    def get_model_areas(self, path):
        """This method returns returns the all surface area processed using
        gmsh internal functions.

        """

        surfaces_areas = dict()
        bodies_volumes = dict()

        # The adoption of quadratic elements ensures better results for area calculations.
        element_type = TETRAHEDRON_10
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", 4)
        gmsh.merge(str(path))

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

                surfaces_areas[tag] = data[-1][-1] / (1e6)

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

        return surfaces_areas  # , bodies_volumes

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
        gmsh_elements = np.zeros(n, dtype=int)

        start, end, ind = 0, 0, 0
        for (entity_dim, entity_tag), e_data in input_dict.items():
            entity_start = start
            for etype_tag, data in e_data.items():

                end += n_list[ind]
                indexes = data["indexes"]
                nodes = data["array_element_nodes"]

                rows = len(indexes)
                cols = nodes.shape[1]
                aux = np.ones(rows, dtype=int)

                output_data[start:end, 1] = aux * entity_tag
                output_data[start:end, 2] = aux * etype_tag
                # output_data[start:end, 3] = indexes
                output_data[start:end, 3] = aux * cols
                output_data[start:end, 4 : 4 + cols] = nodes
                gmsh_elements[start:end] = indexes

                start = end
                ind += 1

            entity_end = end
            self.entity_ranges[entity_dim, entity_tag] = (entity_start, entity_end)

        internal_indexes = np.arange(n, dtype=int)
        # output_data[:, 0] = np.arange(1, n + 1, 1)
        output_data[:, 0] = internal_indexes 
        map_elements = dict(zip(gmsh_elements, internal_indexes))

        return output_data, map_elements

    def _process_element_centroids(self):
        """ This method evaluates the element average center coordinates. """
        self.solid_elements_center.clear()
        for index, nodes in self.nodes_from_solid_element.items():
            self.solid_elements_center[index] = np.average(self.nodal_coordinates[nodes, 1:], axis=0)
            # print(index, self.solid_elements_center[index])


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
