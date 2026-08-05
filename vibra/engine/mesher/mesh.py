import logging
import sys
from collections import defaultdict
from copy import deepcopy
from itertools import permutations
from pathlib import Path
from typing import Literal, Optional, Self

# from time import perf_counter
import gmsh
import numpy as np
from scipy.linalg import svd
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import VTK_HEXAHEDRON, VTK_QUADRATIC_HEXAHEDRON, VTK_QUADRATIC_TETRA, VTK_TETRA, vtkUnstructuredGrid
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

from vibra.engine.mesher.mesh_setup import HEXAHEDRON_8, HEXAHEDRON_20, TETRAHEDRON_4, TETRAHEDRON_10, ElementTopology, MeshRefinementSetup, MeshSetup
from vibra.errors import MeshingAlgorithmError
from vibra.interface.numeric_checks.unit_utilities import convert_length_unit

MeshQualityParams = Literal["gamma", "volume", "minSJ", "aspectRatio"]


class Mesh:
    def __init__(self, **kwargs):
        self.length_unit = kwargs.get("length_unit", "millimeter")
        self.geometry_qf = kwargs.get("geometry_qf", 1.0)

        self.geometry_setup = None
        self.geometry_imported = True
        self.reset_variables()

    def reset_variables(self):
        self.element_topology: Optional[ElementTopology] = None

        ## geometry-related attributes

        self.nodes_to_highlight = list()
        self.efaces_to_highlight = list()

        self.surfaces_from_volume = dict()
        self.lines_from_surface = defaultdict(list)
        self.points_from_line = dict()

        self.volumes_from_surface = defaultdict(list)
        self.surfaces_from_line = defaultdict(list)
        self.lines_from_point = defaultdict(list)
        self.face_elements_connected_to_nodes = defaultdict(list)

        self.length_from_lines = dict()
        self.area_from_surfaces = dict()
        self.volume_from_bodies = dict()

        ## mesh-related attributes

        self.nodal_coordinates = np.zeros((0, 4), dtype=float)
        self.nodes_from_volumes = np.zeros((0, 4), dtype=float)
        self.nodes_from_surfaces = np.zeros((0, 4), dtype=float)
        self.nodes_from_lines = np.zeros((0, 4), dtype=float)

        self.lines_connectivity = np.zeros((0, 4), dtype=int)
        self.faces_connectivity = np.zeros((0, 4), dtype=int)
        self.solids_connectivity = np.zeros((0, 4), dtype=int)

        self.geometry_information = defaultdict(list)

        self.quality_bins = {
            "gamma": (0.7, 0.15),
            "volume": (1e-3, 0),
            "minSJ": (0.3, 0.1),
            "aspectRatio": (4, 1.5),
        }

        self.mesh_quality_data = dict()

        self.disconnected_nodes_data = dict()
        self.collapsed_elements_data = dict()
        self.collapsed_3d_elements = set()
        self.collapsed_2d_elements = set()
        self.collapsed_1d_elements = set()

        self.nodes_from_points = dict()
        self.points_from_nodes = dict()

        self.map_solid_elements = dict()
        self.map_face_elements = dict()
        self.map_line_elements = dict()

        self.elements_from_line = dict()
        self.elements_from_surface = dict()
        self.elements_from_volume = dict()

        self.face_to_solid_element = dict()
        self.solid_to_face_elements = defaultdict(list)

        self.face_element_thickness = dict()
        self.surface_from_solid_element = defaultdict(list)

        self.external_nodes_from_lines = dict()
        self.external_nodes_from_surfaces = dict()
        self.external_nodes_from_volumes = dict()
        self.external_connectivity_from_lines = dict()
        self.external_connectivity_from_surfaces = dict()

        self.normals_surface = dict()
        self.curvatures_surface = dict()
        self.nodal_normals_data = dict()
        self.solid_elements_center = dict()
        self.surfaces_centers = dict()
        self.surface_area_from_element_integration = dict()
        self.cylindrical_surfaces_data = dict()

        self.nodal_area = defaultdict(list)

        self.nodes_collapsed_elements = list()

        self.cache_nodal_coordinates = None
        self.cache_lines_connectivity = None
        self.cache_faces_connectivity = None
        self.cache_solids_connectivity = None

        self.cache_surfaces_from_volume = dict()
        self.cache_lines_from_surface = dict()
        self.cache_points_from_line = dict()

        self.error_data = dict()

    def has_decoupling(self) -> bool:
        return all(
            [
                self.cache_nodal_coordinates is not None,
                self.cache_lines_connectivity is not None,
                self.cache_faces_connectivity is not None,
                self.cache_solids_connectivity is not None,
            ]
        )

    def all_node_ids(self) -> set[int]:
        if self.nodal_coordinates is None:
            return set()

        if self.nodal_coordinates.size == 0:
            return set()

        return set(self.nodal_coordinates[:, 0].flatten().astype(int))

    def all_face_element_ids(self) -> set[int]:
        if self.faces_connectivity is None:
            return

        if self.faces_connectivity.size == 0:
            return set()

        return set(self.faces_connectivity[:, 0].flatten().astype(int))

    def all_solid_element_ids(self) -> set[int]:
        if self.solids_connectivity is None:
            return set()

        if self.solids_connectivity.size == 0:
            return set()

        return set(self.solids_connectivity[:, 0].flatten().astype(int))

    def all_point_ids(self) -> set[int]:
        return set(self.geometry_information.get("points", set()))

    def all_line_ids(self) -> set[int]:
        return set(self.geometry_information.get("lines", set()))

    def all_surface_ids(self) -> set[int]:
        return set(self.geometry_information.get("surfaces", set()))

    def all_solid_ids(self) -> set[int]:
        return set(self.geometry_information.get("volumes", set()))

    def set_length_unit(self, length_unit: str = "millimeter"):
        self.length_unit = length_unit

    def get_length_unit_factor(self):
        if self.length_unit == "millimeter":
            return 1e-3
        elif self.length_unit == "inch":
            return 0.0254
        else:
            return 1

    def load_cad(self, path: str | Path, mesh_setup: MeshSetup, threads: int = 0) -> Self:
        if not gmsh.is_initialized():
            gmsh.initialize("", False, interruptible=False)
            gmsh.option.set_number("General.Terminal", 0)
            gmsh.option.set_number("General.Verbosity", 0)
            gmsh.option.set_number("Geometry.Tolerance", mesh_setup.geometry_tolerance)

            gmsh.option.set_number("General.NumThreads", threads)
            gmsh.option.set_number("Mesh.MaxNumThreads1D", threads)
            gmsh.option.set_number("Mesh.MaxNumThreads2D", threads)
            gmsh.option.set_number("Mesh.MaxNumThreads3D", threads)

            logging.info("Loading geometry... [10/100]")
            gmsh.open(str(path))

        logging.info("Configuring mesh... [20/100]")
        self._configure_mesh(mesh_setup)

        if mesh_setup.merge_connected_volumes:
            self._merge_nodes_from_adjacent_volumes()

        logging.info("Processing geometry data... [25/100]")
        self.process_geometry_information()

        logging.info("Processing geometry data... [35/100]")
        self.process_downwards_adjacencies_from_entities()
        self.process_upwards_adjacencies_from_entities()

        try:
            dimension = mesh_setup.element_setup.dimensions
            gmsh.model.mesh.generate(dimension)
        except Exception as e:
            gmsh.finalize()

            exception = MeshingAlgorithmError(
                "A problem occurred while generating the mesh.\n"
                "Reducing the size of the elements and/or changing the 3D meshing "
                "algorithm may help resolve the issue.\n"
                "If neither of these options works, we suggest reviewing the CAD geometry "
                "to eliminate any potential underlying geometric issues."
            )
            logging.error(str(exception))
            raise exception from e

        logging.info("Post-processing mesh... [60/100]")
        self.post_process_mesh_data()
        self.update_element_topology_based_on_connectivity()

        logging.info("Post-processing mesh... [95/100]")
        if mesh_setup.compute_quality_metrics:
            self.compute_mesh_quality_parameters()

        gmsh.finalize()

        logging.info(
            f"Mesh generated with {len(self.nodal_coordinates)} nodes"
            f", {len(self.lines_connectivity)} dim 1"
            f", {len(self.faces_connectivity)} dim 2"
            f"and {len(self.solids_connectivity)} dim 3 elements"
        )

        return self

    def _configure_mesh(self, mesh_setup: MeshSetup):
        if mesh_setup.refinement_parameters:
            self._local_mesh_refine(
                mesh_setup.maximum_element_size,
                mesh_setup.refinement_parameters,
            )
        else:
            gmsh.option.setNumber("Mesh.MeshSizeMin", mesh_setup.minimum_element_size)
            gmsh.option.setNumber("Mesh.MeshSizeMax", mesh_setup.maximum_element_size)

        gmsh.option.setNumber("Mesh.RandomSeed", mesh_setup.random_seed)
        gmsh.option.setNumber("Mesh.MeshSizeFactor", mesh_setup.size_factor)
        gmsh.option.setNumber("Mesh.Algorithm", mesh_setup.element_setup.algorithm_2d)
        gmsh.option.setNumber("Mesh.Algorithm3D", mesh_setup.element_setup.algorithm_3d)
        gmsh.option.setNumber("Mesh.RecombinationAlgorithm", mesh_setup.element_setup.recombination_algorithm)
        gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", mesh_setup.element_setup.subdivision_algorithm)
        gmsh.option.setNumber("Mesh.RecombineAll", mesh_setup.element_setup.recombine_all)
        gmsh.option.setNumber("Mesh.ElementOrder", mesh_setup.element_setup.element_order)
        gmsh.option.setNumber("Mesh.SecondOrderIncomplete", mesh_setup.element_setup.second_order_incomplete)

        gmsh.model.mesh.clear()
        gmsh.model.occ.synchronize()

    def _merge_nodes_from_adjacent_volumes(self):
        """This method merges all nodes from adjacent volumes."""
        # lines_list = gmsh.model.getEntities(1)
        volumes_list = gmsh.model.getEntities(3)
        # gmsh.model.occ.fragment(lines_list, lines_list)
        gmsh.model.occ.fragment(volumes_list, volumes_list)
        gmsh.model.occ.synchronize()

    def load_mesh(self, path: Path | str, **kwargs):
        geometry_tolerance = kwargs.get("geometry_tolerance", 1e-8)
        threads = kwargs.get("threads", 0)
        gmsh_gui = kwargs.get("gmsh_gui", False)
        self.geometry_imported = False

        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", threads)
        gmsh.option.setNumber("Geometry.Tolerance", geometry_tolerance)

        logging.info("Loading mesh data... [25/100]")
        gmsh.open(str(path))

        logging.info("Loading mesh data... [90/100]")
        gmsh.model.occ.synchronize()

        logging.info("Post-processing mesh... [50/100]")
        self.post_process_mesh_data()
        self.update_element_topology_based_on_connectivity()

        logging.info("Post-processing mesh... [80/100]")
        self.process_downwards_adjacencies_from_mesh_data()

        logging.info("Post-processing mesh... [90/100]")
        self.process_upwards_adjacencies_from_entities()

        if gmsh_gui:
            if "-nopopup" not in sys.argv:
                gmsh.fltk.run()

        gmsh.finalize()

        logging.info(
            f"The mesh file contains {len(self.nodal_coordinates)} nodes"
            f", {len(self.lines_connectivity)} dim 1"
            f", {len(self.faces_connectivity)} dim 2"
            f"and {len(self.solids_connectivity)} dim 3 elements"
        )

        return self

    def update_element_topology_based_on_connectivity(self):
        """
        This method updates the element type based on the connectivity information.
        It's only used when working with NASTRAN files.
        """

        if self.solids_connectivity.size:
            nodes_per_element = self.solids_connectivity[0, 4:].size
        elif self.faces_connectivity.size:
            nodes_per_element = self.faces_connectivity[0, 4:].size
        else:
            print("Invalid mesh detected for 3D and 2D elements.")
            return

        if nodes_per_element in [3, 4] and self.faces_connectivity.size:
            self.element_topology = TETRAHEDRON_4
        elif nodes_per_element == 10:
            self.element_topology = TETRAHEDRON_10
        elif nodes_per_element == 8:
            self.element_topology = HEXAHEDRON_8
        elif nodes_per_element == 20:
            self.element_topology = HEXAHEDRON_20

    def process_downwards_adjacencies_from_mesh_data(self):
        """
        This method processes the downwards adjacencies from entities
        from the solids, faces and lines connectivities matrices.
        """

        self.process_geometry_information()

        e_nodes_2d = self.faces_connectivity[0, 4:].size
        for vol_id in self.geometry_information.get("volumes"):
            nodes_from_volume = self.get_nodes_from_volume(vol_id)
            if nodes_from_volume is None:
                continue

            mask = np.sum(np.isin(self.faces_connectivity[:, 4:], nodes_from_volume), axis=1) == e_nodes_2d
            self.surfaces_from_volume[vol_id] = [int(tag) for tag in set(self.faces_connectivity[mask, 1])]

        if self.lines_connectivity.size:
            e_nodes_1d = self.lines_connectivity[0, 4:].size
            for surf_id in self.geometry_information.get("surfaces"):
                nodes_from_surface = self.get_nodes_from_surface(surf_id)
                if nodes_from_surface is None:
                    continue

                mask = (
                    np.sum(
                        np.isin(self.lines_connectivity[:, 4:], nodes_from_surface),
                        axis=1,
                    )
                    == e_nodes_1d
                )
                self.lines_from_surface[surf_id] = [int(tag) for tag in set(self.lines_connectivity[mask, 1])]

        self.process_lines_from_mesh_data()
        self.process_lines_connectivitiy_from_mesh_data()
        self.process_points_from_mesh_data()

    def process_lines_from_mesh_data(self):
        """
        This method processes the nodes from lines and the lines
        from surfaces based on the surfaces connectivity.
        """

        if self.lines_connectivity.size:
            return

        index = 0
        line_id = 0

        self.external_nodes_from_lines.clear()
        surface_ids = self.geometry_information.get("surfaces")

        while index < len(surface_ids):
            fixed_tag = surface_ids[index]
            nodes_fixed = self.get_nodes_from_surface(fixed_tag)

            for sweep_tag in surface_ids[index + 1 :]:
                nodes_sweep = self.get_nodes_from_surface(sweep_tag)
                intersect_nodes = np.intersect1d(nodes_fixed, nodes_sweep)
                if intersect_nodes.size <= 1:
                    continue

                check_overlap_1 = False
                check_overlap_2 = False

                line_nodes = list(set(intersect_nodes))

                for _line_nodes in self.separate_nodes_from_disconnected_lines(line_nodes).values():
                    _line_nodes.sort()
                    if _line_nodes in self.external_nodes_from_lines.values():
                        continue

                    for _line_id, nodes_from_line in self.external_nodes_from_lines.items():
                        check_overlap_1 = np.isin(nodes_from_line, _line_nodes).all()
                        if check_overlap_1:
                            break

                        check_overlap_2 = np.isin(_line_nodes, nodes_from_line).all()
                        if check_overlap_2:
                            break

                    if check_overlap_1:
                        continue

                    if check_overlap_2:
                        self.external_nodes_from_lines[_line_id] = _line_nodes
                        continue

                    line_id += 1
                    self.external_nodes_from_lines[line_id] = _line_nodes

            index += 1

        self.lines_from_surface.clear()
        for line_id, line_nodes in self.external_nodes_from_lines.items():
            self.length_from_lines[line_id] = 0.0
            for surf_id in self.geometry_information.get("surfaces"):
                surface_nodes = self.get_nodes_from_surface(surf_id)
                if surface_nodes is None:
                    continue

                if np.isin(line_nodes, surface_nodes).all():
                    self.lines_from_surface[surf_id].append(line_id)

    def separate_nodes_from_disconnected_lines(self, node_ids: list) -> dict:
        """
        This method group nodes from each line using a
        a recursive structure.

        Parameters
        ----------

        node_ids: list
            a list containing the intersection nodes from two neighboor surfaces.

        Returns
        -------
        group_of_connected_nodes: dict
            a dictionary whose the keys are the group of nodes indexes and the
            values are the node IDs.

        """

        n_nodes_2d = self.faces_connectivity[0, 4:].size

        if n_nodes_2d in [3, 4]:
            n_nodes_1d = 2

        elif n_nodes_2d in [6, 8]:
            n_nodes_1d = 3

        else:
            return

        # get the 2D element connectivities that contains two node_ids inside
        filt_rows = np.sum(np.isin(self.faces_connectivity[:, 4:], node_ids), axis=1) == n_nodes_1d
        filt_connectivities = deepcopy([list(nodes) for nodes in self.faces_connectivity[filt_rows, 4:]])

        if not filt_connectivities:
            return dict()

        connectivities = list()
        for connect in filt_connectivities:
            # filter the 1D element connectivities from 2D connectivities
            line_connect = [int(node) for node in connect if node in node_ids]
            line_connect.sort()

            # ignore the duplicate edge connectivities
            if line_connect in connectivities:
                continue

            connectivities.append(line_connect)

        index = 0
        iter_count = 0
        group_of_connected_nodes = defaultdict(list)

        do_not_update = False
        while len(connectivities) > 0 and iter_count <= 1000:
            non_mapped = list()

            if not do_not_update:
                index += 1
                start_connect = connectivities[0]
                connectivities.remove(start_connect)
                group_of_connected_nodes[index] = [node for node in start_connect]

            for connect in connectivities:
                if not np.isin(group_of_connected_nodes[index], connect).any():
                    non_mapped.append(connect)
                    continue

                for node_id in connect:
                    if node_id in group_of_connected_nodes[index]:
                        continue

                    group_of_connected_nodes[index].append(node_id)

            iter_count += 1
            connectivities = non_mapped
            do_not_update = np.isin(group_of_connected_nodes[index], non_mapped).any()

        return group_of_connected_nodes

    def process_lines_connectivitiy_from_mesh_data(self):
        """
        This method processes the lines connectivity
        based on the surfaces connectivity.
        """

        if self.lines_connectivity.size:
            return

        connect_data = self.faces_connectivity[:, 4:]
        n_nodes_2d = self.faces_connectivity[0, 4:].size

        if n_nodes_2d in [3, 4]:
            n_nodes_1d = 2
            e_type = 2

        elif n_nodes_2d in [6, 8]:
            n_nodes_1d = 3
            e_type = 3

        last_index = 0
        first_index = 0
        self.lines_connectivity = np.empty((0, 4 + n_nodes_1d), dtype=int)

        for line_id, node_ids in self.external_nodes_from_lines.items():
            connectivity_from_line = list()
            filt_rows = np.sum(np.isin(connect_data, node_ids), axis=1) == n_nodes_1d

            for _connect in connect_data[filt_rows, :]:
                edge_connect = [node_id for node_id in _connect if node_id in node_ids]
                edge_connect = self.reorder_connectivity_based_on_distances(edge_connect)

                if edge_connect in connectivity_from_line:
                    continue

                connectivity_from_line.append(edge_connect)

            if not connectivity_from_line:
                continue

            connectivity_array = np.array(connectivity_from_line, dtype=int)

            rows = connectivity_array.shape[0]
            aux_ones = np.ones(rows, dtype=int)

            last_index += rows
            indexes = np.arange(first_index, last_index, dtype=int)

            connectivity = np.zeros((rows, 4 + n_nodes_1d), dtype=int)
            connectivity[:, 0] = indexes
            connectivity[:, 1] = aux_ones * line_id
            connectivity[:, 2] = aux_ones * e_type
            connectivity[:, 3] = aux_ones * n_nodes_1d
            connectivity[:, 4:] = connectivity_array

            self.lines_connectivity = np.append(self.lines_connectivity, connectivity, axis=0)
            first_index = last_index

        if self.external_nodes_from_lines:
            self.map_elements_from_lines()
            self.geometry_information["lines"] = list(self.external_nodes_from_lines.keys())
            # np.savetxt("lines_connectivity.dat", self.lines_connectivity, delimiter=",", fmt="%i")

    def reorder_connectivity_based_on_distances(self, el_connect: list[int]):
        """
        This method reorders the line element connectivity based on
        the nodal distances.

        Parameters
        ----------
        el_connect: list
            The initial random element connectivity.

        Returns
        -------
        reordered_connect: list
            The reordered element connectivity (following the order:
            corner nodes and middle node, whenever applicable).
        """

        perm_nodes = np.array(list(permutations(el_connect, 2)), dtype=int)

        P1 = self.nodal_coordinates[perm_nodes[:, 0], 1:]
        P2 = self.nodal_coordinates[perm_nodes[:, 1], 1:]

        lengths = np.linalg.norm(P2 - P1, axis=1)
        reordered_connect = np.sort(perm_nodes[np.argmax(lengths), :])

        if len(el_connect) == 3:
            mask = np.isin(el_connect, reordered_connect, invert=True)
            middle_node = np.array(el_connect, dtype=int)[mask]
            reordered_connect = np.append(reordered_connect, middle_node, axis=0)

        return list(reordered_connect)

    def process_points_from_mesh_data(self):
        """
        This method processes the corner nodes and the
        points based on lines_connectivity attribute.

        """

        if not self.lines_connectivity.size:
            return

        def get_non_repeated_values(line_connectivities: np.ndarray):
            """
            This function returns the non-repeated values
            from a given input list of values.

            Parameters
            ----------
            values: np.ndarray
                An array containing the connectivities
                of the 1D elements of a line.

            Returns
            -------
            non_repeated_values: list
                The output list of non-repeated values.

            """
            values = line_connectivities[:, [0, 1]].flatten()
            _, indexes, count = np.unique(values, return_index=True, return_counts=True)
            non_repeated_values = list(values[indexes[count == 1]])
            return non_repeated_values

        point_id = 0
        self.points_from_line.clear()

        for line_id in self.geometry_information.get("lines"):
            line_connect = self.get_connectivity_from_line(line_id)
            corner_nodes = get_non_repeated_values(line_connect)

            points_from_line = list()

            for _node_id in corner_nodes:
                node_id = int(_node_id)
                if node_id in self.points_from_nodes.keys():
                    points_from_nodes = self.points_from_nodes.get(node_id)
                    points_from_line.append(points_from_nodes)
                    continue

                point_id += 1
                points_from_line.append(point_id)
                self.nodes_from_points[point_id] = node_id
                self.points_from_nodes[node_id] = point_id

            self.points_from_line[line_id] = points_from_line

        self.geometry_information["points"] = list(self.nodes_from_points.keys())

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

    def import_external_nodal_coordinates(self, data, index_zero=True):
        """ """
        if isinstance(data, list):
            data = np.array(data)

        rows, cols = data.shape

        indexes = data[:, 0]
        if index_zero:
            indexes -= 1

        self.nodal_coordinates = np.zeros((rows, cols), dtype=float)
        self.nodal_coordinates[:, 0] = indexes
        self.nodal_coordinates[:, 1:] = data[:, 1:]

    def import_external_solids_connectivity(self, connectivity: dict, index_zero: bool = True, etype_tag: float = 1):
        """ """
        self.elements_from_volume.clear()

        aux = list()
        for key, connect_data in connectivity.items():
            self.elements_from_volume[key[0]] = connect_data[:, 0] - 1
            for nodes in connect_data:
                aux.append(nodes)

        data = np.array(aux, dtype=int)
        rows, cols = data.shape

        indexes = data[:, 0]
        volumes = data[:, 1]
        nodes_per_element = data[:, 2]
        connect = data[:, 3:]

        if index_zero:
            connect -= 1
            indexes -= 1

        aux = np.ones(rows)
        self.solids_connectivity = np.zeros((rows, cols + 1), dtype=int)
        self.solids_connectivity[:, 0] = indexes
        self.solids_connectivity[:, 1] = volumes
        self.solids_connectivity[:, 2] = aux * etype_tag
        self.solids_connectivity[:, 3] = nodes_per_element
        self.solids_connectivity[:, 4:] = connect

        nodes_from_volume = defaultdict(list)
        for elem_id, vol_id, _, _, *node_ids in self.solids_connectivity:
            nodes_from_volume[vol_id].extend(node_ids)

        self.external_nodes_from_volumes.clear()
        for key, values in nodes_from_volume.items():
            self.external_nodes_from_volumes[key] = np.unique(values).astype(int)

    def import_external_faces_connectivity(self, connectivity: dict, index_zero: bool = True, etype_tag: float = 1):
        """ """
        self.elements_from_surface.clear()

        aux_list = list()
        for key, connect_data in connectivity.items():
            self.elements_from_surface[key[0]] = connect_data[:, 0] - 1
            for nodes in connect_data:
                aux_list.append(nodes)

        data = np.array(aux_list, dtype=int)
        rows, cols = data.shape

        indexes = data[:, 0]
        surface = data[:, 1]
        nodes_per_element = data[:, 2]
        connect = data[:, 3:]

        if index_zero:
            connect -= 1
            indexes -= 1

        aux = np.ones(rows)
        self.faces_connectivity = np.zeros((rows, cols + 1), dtype=int)
        self.faces_connectivity[:, 0] = indexes
        self.faces_connectivity[:, 1] = surface
        self.faces_connectivity[:, 2] = aux * etype_tag
        self.faces_connectivity[:, 3] = nodes_per_element
        self.faces_connectivity[:, 4:] = connect

        nodes_from_surface = defaultdict(list)
        for elem_id, surf_id, _, _, *node_ids in self.faces_connectivity:
            nodes_from_surface[surf_id].extend(node_ids)

        self.external_nodes_from_surfaces.clear()
        for key, values in nodes_from_surface.items():
            self.external_nodes_from_surfaces[key] = np.unique(values).astype(int)

    def map_surfaces_to_volumes(self, surfaces_from_volume: dict[int, list[int]]):
        self.volumes_from_surface.clear()
        self.surfaces_from_volume.clear()
        for vol_id, surf_ids in surfaces_from_volume.items():
            for surf_id in surf_ids:
                self.volumes_from_surface[surf_id] = [vol_id]

            self.surfaces_from_volume[vol_id] = surf_ids
    
    def export_nodal_coordinates(self, filename):
        fmt = ["%i", "%.16f", "%.16f", "%.16f"]
        header = "Node index || Coordinate x [m] || Coordinate y [m] || Coordinate z [m]"
        np.savetxt(filename, self.nodal_coordinates, delimiter=",", header=header, fmt=fmt)

    def export_line_elements_connectivity(self, filename):
        header = "Index || Element ID || Line ID || Element type ID || Connected Node IDs"
        np.savetxt(filename, self.lines_connectivity, delimiter=",", header=header, fmt="%i")

    def export_face_elements_connectivity(self, filename):
        header = "Index || Element ID || Face ID || Element type ID || Connected Node IDs"
        np.savetxt(filename, self.faces_connectivity, delimiter=",", header=header, fmt="%i")

    def export_solid_elements_connectivity(self, filename):
        header = "Index || Solid ID || Element type ID || Element ID || Connected Node IDs"
        np.savetxt(filename, self.solids_connectivity, delimiter=",", header=header, fmt="%i")

    def export_vtu_file(self, filename):
        """This methods exports vtu file."""
        points = vtkPoints()
        vtk_dataset = vtkUnstructuredGrid()
        for id, coords in enumerate(self.nodal_coordinates[:, 1:]):
            points.InsertPoint(id, list(coords))
            vtk_dataset.SetPoints(points)
        #
        NODES_PER_ELEMENT = len(self.solids_connectivity[0, 4:])
        if NODES_PER_ELEMENT == 4:
            vtk_cell = VTK_TETRA
        elif NODES_PER_ELEMENT == 10:
            vtk_cell = VTK_QUADRATIC_TETRA
        elif NODES_PER_ELEMENT == 8:
            vtk_cell = VTK_HEXAHEDRON
        elif NODES_PER_ELEMENT == 20:
            vtk_cell = VTK_QUADRATIC_HEXAHEDRON
        else:
            raise TypeError("Unsupported element type.")

        n_nodes, nf_elem, ns_elem = self.get_mesh_info()
        vtk_dataset.Allocate(ns_elem)
        for id, connect in enumerate(self.solids_connectivity[:, 4:]):
            vtk_dataset.InsertNextCell(vtk_cell, NODES_PER_ELEMENT, list(connect))

        # unod1 = np.zeros((nnode), dtype=complex)
        # for i in range(nnode):
        #     unod1[i] = P[i, modo1]

        # array1 = vtkDoubleArray()
        # array1.SetNumberOfComponents(1)
        # array1.SetNumberOfTuples(nnode)
        # array1.SetName('Pressure Real')

        # for id in range(nnode):
        #     values1 = [np.real(unod1[id])]
        #     array1.SetTuple(id, values1)
        #     vtk_dataset.GetPointData().AddArray(array1)

        writer = vtkXMLUnstructuredGridWriter()
        writer.SetFileName(filename)
        writer.SetInputData(vtk_dataset)
        writer.Write()

    def _local_mesh_refine(self, global_size: float, refinement_setups: list[MeshRefinementSetup]):
        setup_sizes = [setup.element_size for setup in refinement_setups]
        max_size = max([global_size, *setup_sizes])
        coarsening = max_size > global_size

        if coarsening:
            # Allow mesh sizes larger than the ones derived from the imported
            # geometry points, otherwise gmsh caps the size and "unrefinement"
            # has no effect. Note that with merge_connected_volumes enabled the
            # size transition is graded across merged shared faces (expected).
            gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)

        gmsh.model.mesh.field.add("Constant")
        gmsh.model.mesh.field.setNumbers(1, "SurfacesList", [])
        gmsh.model.mesh.field.setNumbers(1, "VolumesList", [])
        gmsh.model.mesh.field.setNumber(1, "VOut", max_size)

        fields_list = [1]
        for setup in refinement_setups:
            match setup.entity_type:
                case "surfaces":
                    option = "SurfacesList"
                case "volumes":
                    option = "VolumesList"
                case _:
                    continue

            if coarsening and setup.element_size >= max_size:
                continue

            threshold_type = gmsh.model.mesh.field.add("Constant")
            gmsh.model.mesh.field.setNumbers(
                threshold_type,
                option,
                setup.entity_ids,
            )
            gmsh.model.mesh.field.setNumber(
                threshold_type,
                "VIn",
                setup.element_size,
            )
            fields_list.append(threshold_type)

        if coarsening:
            self._add_inverted_refinement_fields(global_size, max_size, refinement_setups, fields_list)

        minimum_field = gmsh.model.mesh.field.add("Min")
        gmsh.model.mesh.field.setNumbers(minimum_field, "FieldsList", fields_list)
        gmsh.model.mesh.field.setAsBackgroundMesh(minimum_field)

    def _add_inverted_refinement_fields(
        self,
        global_size: float,
        max_size: float,
        refinement_setups: list[MeshRefinementSetup],
        fields_list: list[int],
    ):
        """Keeps the volumes not covered by any refinement setup at the global
        size when the background field is raised to the coarsest size."""
        volume_setups = [setup for setup in refinement_setups if setup.entity_type == "volumes"]
        if not volume_setups:
            return

        listed_volumes = set()
        for setup in volume_setups:
            listed_volumes |= set(setup.entity_ids)

        complement_volumes = [vol for dim, vol in gmsh.model.getEntities(3) if vol not in listed_volumes]
        if not complement_volumes:
            return

        complement_field = gmsh.model.mesh.field.add("Constant")
        gmsh.model.mesh.field.setNumbers(complement_field, "VolumesList", complement_volumes)
        gmsh.model.mesh.field.setNumber(complement_field, "VIn", global_size)
        fields_list.append(complement_field)

    def clear_mesh_data(self):
        self.nodal_coordinates = np.zeros((0, 4), dtype=float)
        self.nodes_from_volumes = np.zeros((0, 4), dtype=float)
        self.nodes_from_surfaces = np.zeros((0, 4), dtype=float)
        self.nodes_from_lines = np.zeros((0, 4), dtype=float)

        self.lines_connectivity = np.zeros((0, 4), dtype=int)
        self.faces_connectivity = np.zeros((0, 4), dtype=int)
        self.solids_connectivity = np.zeros((0, 4), dtype=int)

        self.disconnected_nodes_data.clear()
        self.collapsed_elements_data.clear()
        self.collapsed_1d_elements.clear()
        self.collapsed_2d_elements.clear()
        self.collapsed_3d_elements.clear()

        self.nodes_from_points.clear()
        self.points_from_nodes.clear()

        self.map_solid_elements.clear()
        self.map_face_elements.clear()
        self.map_line_elements.clear()

        self.mesh_quality_data.clear()

        self.solid_elements_center.clear()
        self.external_nodes_from_lines.clear()
        self.external_nodes_from_surfaces.clear()
        self.external_nodes_from_volumes.clear()
        self.external_connectivity_from_lines.clear()
        self.external_connectivity_from_surfaces.clear()

        self.normals_surface.clear()
        self.curvatures_surface.clear()

        # cache mesh attributes for degrees of freedom decoupling
        self.cache_nodal_coordinates = None
        self.cache_lines_connectivity = None
        self.cache_faces_connectivity = None
        self.cache_solids_connectivity = None

    def clear_geometry_data(self):
        self.geometry_information.clear()

        self.surfaces_from_volume.clear()
        self.lines_from_surface.clear()
        self.points_from_line.clear()

        self.volumes_from_surface.clear()
        self.surfaces_from_line.clear()
        self.lines_from_point.clear()

        self.length_from_lines.clear()
        self.area_from_surfaces.clear()
        self.volume_from_bodies.clear()

        self.cache_surfaces_from_volume.clear()
        self.cache_lines_from_surface.clear()
        self.cache_points_from_line.clear()

    def get_points_from_geometry(self, from_cache: bool = True):
        output_ids = set()
        if from_cache:
            points_from_line = self.cache_points_from_line
        else:
            points_from_line = self.points_from_line

        for point_ids in points_from_line.values():
            output_ids |= set(point_ids)

        return list(output_ids)

    def get_lines_from_geometry(self, from_cache: bool = True):
        output_ids = set()
        if from_cache:
            lines_from_surface = self.cache_lines_from_surface
        else:
            lines_from_surface = self.lines_from_surface

        for line_ids in lines_from_surface.values():
            output_ids |= set(line_ids)

        return list(output_ids)

    def get_surfaces_from_geometry(self, from_cache: bool = True):
        output_ids = set()
        if from_cache:
            surfaces_from_volume = self.cache_surfaces_from_volume
        else:
            surfaces_from_volume = self.surfaces_from_volume

        for surface_ids in surfaces_from_volume.values():
            output_ids |= set(surface_ids)

        return list(output_ids)

    def get_points_and_lines_from_surfaces(self, surface_ids: list[int]):
        point_ids = set()
        line_ids = set()
        for surface_id in surface_ids:
            lines_from_surface = self.cache_lines_from_surface[surface_id]
            line_ids |= set(lines_from_surface)
            for line_id in lines_from_surface:
                points_from_line = self.cache_points_from_line[line_id]
                point_ids |= set(points_from_line)

        point_ids = [int(point_id) for point_id in point_ids]
        line_ids = [int(line_id) for line_id in line_ids]

        return point_ids, line_ids

    def process_surface_normals_and_curvatures(self, tag: int):
        """This method processes the surface curvatures and normal
        at surface nodes.

        Parameters
        ----------
        tag : int
            It represents the gmsh surface's tag.
        """
        node_tags, _, param = gmsh.model.mesh.getNodes(2, tag, True)
        normals_surface = gmsh.model.getNormal(tag, param).reshape(-1, 3)
        curvatures_surface = gmsh.model.getCurvature(2, tag, param)
        sorted_indexes = np.argsort(node_tags)
        self.normals_surface[tag] = normals_surface[sorted_indexes, :]

        # processs the unit length factor to curvatures
        conv_factor = convert_length_unit(1.0, self.length_unit, "meter")

        # convert the curvature unit to 1/m
        self.curvatures_surface[tag] = curvatures_surface[sorted_indexes] / conv_factor

    def process_cylindrical_surfaces(self):

        # t0 = perf_counter()
        self.cylindrical_surfaces_data.clear()
        for surface_id, curvatures in self.curvatures_surface.items():
            avg_curvature = np.average(curvatures)
            if not np.all(curvatures - avg_curvature < 1e-5):
                continue

            if not avg_curvature:
                continue

            # surface normals
            normals_surface = self.normals_surface.get(surface_id)
            if normals_surface is None:
                continue

            # solve the SVD problem to find the axis
            _, _, Vh = svd(normals_surface, full_matrices=False, compute_uv=True, overwrite_a=False)

            # define the last vector as the axis_candidate
            axis_candidate = Vh[-1]
            dot_products = np.abs(np.dot(normals_surface, axis_candidate))

            # chech if all normals is perpendicular to axis_candidate
            if np.all(dot_products < 1e-3):
                # print(f"The surface {surface_id} is cylindrical.")
                self.cylindrical_surfaces_data[surface_id] = 2 / avg_curvature

        # dt = perf_counter() - t0
        # print(f"Time to process cylindrical surfaces: {dt} [s]")

    def post_process_mesh_data(self):
        """This method processes the nodal coordinates, connectivities
        from all geometric entities, nodal normals, and curvatures
        from the data provided by GMSH.
        """

        self.clear_mesh_data()

        indexes, coords, _ = gmsh.model.mesh.getNodes(includeBoundary=True)
        total_nodes = int(np.max(indexes))

        unit_length_factor = self.get_length_unit_factor()
        self.nodal_coordinates = np.zeros((total_nodes, 4))
        self.nodal_coordinates[indexes - 1, 1:] = coords.reshape(-1, 3) * unit_length_factor
        self.nodal_coordinates[indexes - 1, :1] = indexes.reshape(-1, 1) - 1

        nodes_from_volumes = gmsh.model.mesh.getNodes(dim=3, includeBoundary=True)[0]
        nodes_from_surfaces = gmsh.model.mesh.getNodes(dim=2, includeBoundary=True)[0]
        nodes_from_lines = gmsh.model.mesh.getNodes(dim=1, includeBoundary=True)[0]

        if isinstance(nodes_from_volumes, np.ndarray):
            self.nodes_from_volumes = np.unique(nodes_from_volumes) - 1

        if isinstance(nodes_from_surfaces, np.ndarray):
            self.nodes_from_surfaces = np.unique(nodes_from_surfaces) - 1

        if isinstance(nodes_from_lines, np.ndarray):
            self.nodes_from_lines = np.unique(nodes_from_lines) - 1

        connectivity_dim1 = dict()
        connectivity_dim2 = dict()
        connectivity_dim3 = dict()

        for dim, tag in gmsh.model.getEntities():
            elements_data = dict()
            element_types, element_indexes, element_nodes = gmsh.model.mesh.getElements(dim, tag)

            if not element_indexes:
                continue

            if dim == 2:
                if self.geometry_imported:
                    self.process_surface_normals_and_curvatures(tag)

            for i, element_type in enumerate(element_types):
                _, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(element_type)

                array_element_nodes = np.array(element_nodes[i]).reshape(-1, nodes_per_element)
                array_element_nodes -= 1

                elements_data[element_type] = {
                    "indexes": element_indexes[i],
                    "array_element_nodes": array_element_nodes,
                }

            if dim == 0:  # Points
                node_id = element_nodes[0][0] - 1
                self.nodes_from_points[tag] = int(node_id)
                self.points_from_nodes[node_id] = tag

            elif dim == 1:  # Lines
                connectivity_dim1[dim, tag] = elements_data
                # print(tag, elements_data)

            elif dim == 2:  # Surfaces
                connectivity_dim2[dim, tag] = elements_data

            elif dim == 3:  # Solids
                connectivity_dim3[dim, tag] = elements_data

        logging.info("Post-processing mesh... [65/100]")
        self.process_cylindrical_surfaces()

        self.lines_connectivity, self.map_line_elements = self._get_connectivity_array(connectivity_dim1)
        self.faces_connectivity, self.map_face_elements = self._get_connectivity_array(connectivity_dim2)
        self.solids_connectivity, self.map_solid_elements = self._get_connectivity_array(connectivity_dim3)

        logging.info("Post-processing mesh... [68/100]")
        self.process_mesh_related_mappings("Post-processing")

        logging.info("Post-processing mesh... [80/100]")
        self.disconnected_nodes_data = self.process_disconnected_nodes_criterion()

        logging.info("Post-processing mesh... [90/100]")
        self.collapsed_3d_elements, self.collapsed_2d_elements, self.collapsed_1d_elements = self.get_collapsed_elements()
        self.collapsed_elements_data = self.get_collapsed_elements_data()

    def cache_mesh_information(self):
        self.cache_nodal_coordinates = deepcopy(self.nodal_coordinates)

        self.cache_surfaces_from_volume = deepcopy(self.surfaces_from_volume)
        self.cache_lines_from_surface = deepcopy(self.lines_from_surface)
        self.cache_points_from_line = deepcopy(self.points_from_line)

        self.cache_lines_connectivity = deepcopy(self.lines_connectivity)
        self.cache_faces_connectivity = deepcopy(self.faces_connectivity)
        self.cache_solids_connectivity = deepcopy(self.solids_connectivity)

    def get_nodes_from_line(self, line_id: int, from_cache: bool = False):

        if line_id in self.external_nodes_from_lines.keys():
            return self.external_nodes_from_lines.get(line_id)

        if from_cache:
            if self.cache_lines_connectivity is None:
                return
            connect_data = self.cache_lines_connectivity
        else:
            connect_data = self.lines_connectivity

        if not connect_data.size:
            return None

        rows = np.where(connect_data[:, 1] == line_id)[0]
        nodes = np.unique(connect_data[rows, 4:]).astype(int)

        return np.sort(nodes)

    def get_nodes_from_surface(self, surface_id: int, from_cache: bool = False):

        if surface_id in self.external_nodes_from_surfaces.keys():
            return self.external_nodes_from_surfaces.get(surface_id)

        if from_cache:
            connect_data = self.cache_faces_connectivity
        else:
            connect_data = self.faces_connectivity

        if not connect_data.size:
            return None

        rows = np.where(connect_data[:, 1] == surface_id)[0]
        nodes = np.unique(connect_data[rows, 4:]).astype(int)

        return np.sort(nodes)

    def get_nodes_from_volume(self, volume_id: int, from_cache: bool = False):

        if volume_id in self.external_nodes_from_volumes.keys():
            return self.external_nodes_from_volumes.get(volume_id)

        if from_cache:
            connect_data = self.cache_solids_connectivity
        else:
            connect_data = self.solids_connectivity

        if not connect_data.size:
            return None

        rows = np.where(connect_data[:, 1] == volume_id)[0]
        nodes = np.unique(connect_data[rows, 4:]).astype(int)

        return np.sort(nodes)

    def get_connectivity_from_line(self, line_id: int, from_cache: bool = False) -> np.ndarray:

        if line_id in self.external_connectivity_from_lines.keys():
            return self.external_connectivity_from_lines.get(line_id)

        if from_cache:
            rows = self.cache_lines_connectivity[:, 1] == line_id
            return self.cache_lines_connectivity[rows, 4:]

        else:
            rows = self.lines_connectivity[:, 1] == line_id
            return self.lines_connectivity[rows, 4:]

    def get_connectivity_from_surface(self, surface_id: int, from_cache: bool = False) -> np.ndarray:

        if surface_id in self.external_connectivity_from_surfaces.keys():
            return self.external_connectivity_from_surfaces.get(surface_id)

        if from_cache:
            rows = self.cache_faces_connectivity[:, 1] == surface_id
            return self.cache_faces_connectivity[rows, 4:]

        else:
            rows = self.faces_connectivity[:, 1] == surface_id
            return self.faces_connectivity[rows, 4:]

    def get_connectivity_from_volume(self, volume_id: int, from_cache: bool = False) -> np.ndarray:

        if from_cache:
            rows = self.cache_solids_connectivity[:, 1] == volume_id
            return self.cache_solids_connectivity[rows, 4:]

        else:
            rows = self.solids_connectivity[:, 1] == volume_id
            return self.solids_connectivity[rows, 4:]

    def get_surfaces_from_node(self, node_id: int):

        mask = np.sum(np.isin(self.faces_connectivity[:, 4:], node_id), axis=1) == 1
        if not mask.any():
            return list()

        surfaces_from_node = [int(surf_id) for surf_id in np.unique(self.faces_connectivity[:, 1][mask])]
        return surfaces_from_node

    def get_volumes_from_selected_nodes(self, selected_nodes: list | np.ndarray, return_volumes: bool = False):

        if return_volumes:
            mask = np.sum(np.isin(self.solids_connectivity[:, 4:], selected_nodes), axis=1) >= 1
            volume_ids = [int(vol_id) for vol_id in np.unique(self.solids_connectivity[:, 1][mask])]
            return volume_ids

        volumes_from_nodes = defaultdict(list)
        for node_id in selected_nodes:
            mask = np.sum(np.isin(self.solids_connectivity[:, 4:], node_id), axis=1) >= 1
            volume_ids = [int(vol_id) for vol_id in np.unique(self.solids_connectivity[:, 1][mask])]
            volumes_from_nodes[node_id].extend(volume_ids)

        return volumes_from_nodes

    def get_volumes_from_selected_points(self, selected_points: list | np.ndarray):
        volumes_from_points = defaultdict(list)
        for line_id, points_from_line in self.points_from_line.items():
            if not np.isin(points_from_line, selected_points).any():
                continue

            for surf_id in self.surfaces_from_line.get(line_id):
                for vol_id in self.volumes_from_surface.get(surf_id):
                    for point_id in selected_points:
                        if point_id not in points_from_line:
                            continue

                        vol_ids = volumes_from_points.get(point_id)
                        if vol_ids is None or vol_id not in vol_ids:
                            volumes_from_points[point_id].append(vol_id)

        return volumes_from_points

    def get_volumes_from_selected_lines(self, selected_lines: list | np.ndarray):
        volumes_from_lines = defaultdict(list)
        for surf_id, lines_from_surface in self.lines_from_surface.items():
            if not np.isin(lines_from_surface, selected_lines).any():
                continue

            for vol_id in self.volumes_from_surface.get(surf_id):
                for line_id in selected_lines:
                    if line_id not in lines_from_surface:
                        continue

                    vol_ids = volumes_from_lines.get(line_id)
                    if vol_ids is None or vol_id not in vol_ids:
                        volumes_from_lines[line_id].append(vol_id)

        return volumes_from_lines

    def get_volumes_from_selected_surfaces(self, selected_surfaces: list | np.ndarray):
        volumes_from_surfaces = defaultdict(list)
        for selected_surface in selected_surfaces:
            vol_ids = self.volumes_from_surface.get(selected_surface)
            if vol_ids is None:
                continue

            for vol_id in vol_ids:
                if selected_surface in volumes_from_surfaces.keys():
                    if vol_id in volumes_from_surfaces.get(selected_surface):
                        continue

                volumes_from_surfaces[selected_surface].append(vol_id)

        return volumes_from_surfaces

    def restore_data_from_cache(self):
        self.nodal_coordinates = deepcopy(self.cache_nodal_coordinates)
        self.lines_connectivity = deepcopy(self.cache_lines_connectivity)
        self.faces_connectivity = deepcopy(self.cache_faces_connectivity)
        self.solids_connectivity = deepcopy(self.cache_solids_connectivity)

        self.surfaces_from_volume = deepcopy(self.cache_surfaces_from_volume)
        self.lines_from_surface = deepcopy(self.cache_lines_from_surface)
        self.points_from_line = deepcopy(self.cache_points_from_line)

        self.cache_nodal_coordinates = None
        self.cache_lines_connectivity = None
        self.cache_faces_connectivity = None
        self.cache_solids_connectivity = None

        self.cache_surfaces_from_volume.clear()
        self.cache_lines_from_surface.clear()
        self.cache_points_from_line.clear()

        self.process_mesh_related_mappings("Loading")

        surface_ids = set()
        for line_surfaces in self.surfaces_from_volume.values():
            surface_ids |= set(line_surfaces)
        surface_ids = list(surface_ids)

        line_ids = set()
        for line_lines in self.lines_from_surface.values():
            line_ids |= set(line_lines)
        line_ids = list(line_ids)

        point_ids = set()
        for line_points in self.points_from_line.values():
            point_ids |= set(line_points)
        point_ids = list(point_ids)

        for line_id in deepcopy(self.length_from_lines).keys():
            if line_id in line_ids:
                continue
            self.length_from_lines.pop(line_id)

        for surface_id in deepcopy(self.area_from_surfaces).keys():
            if surface_id in surface_ids:
                continue
            self.area_from_surfaces.pop(surface_id)

        self.geometry_information["surfaces"] = surface_ids
        self.geometry_information["lines"] = line_ids
        self.geometry_information["points"] = point_ids

        for point_id in deepcopy(self.nodes_from_points).keys():
            if point_id in point_ids:
                continue
            self.nodes_from_points.pop(point_id)

        self.points_from_nodes.clear()
        self.points_from_nodes = {v: k for k, v in self.nodes_from_points.items()}

    def process_solid_elements_from_surfaces(self):
        self.surface_from_solid_element.clear()
        for surface_id in self.geometry_information.get("surfaces"):
            surface_nodes = self.get_nodes_from_surface(surface_id)
            if surface_nodes is None:
                continue

            mask = np.sum(np.isin(self.solids_connectivity[:, 4:], surface_nodes), axis=1) >= 1
            if not mask.any():
                continue

            for el_index in self.solids_connectivity[mask, 0]:
                self.surface_from_solid_element[el_index].append(surface_id)

    def process_mesh_related_mappings(self, label: str = "Loading"):

        logging.info(f"{label} mesh... [70/100]")
        self.map_elements_from_volumes()

        logging.info(f"{label} mesh... [75/100]")
        self.map_elements_from_surfaces()

        logging.info(f"{label} mesh... [80/100]")
        self.map_elements_from_lines()

        logging.info(f"{label} mesh... [85/100]")
        self.map_face_elements_to_solid_elements()

    def map_elements_from_lines(self):
        self.elements_from_line.clear()
        for line_id in np.unique(self.lines_connectivity[:, 1]).astype(int):
            rows = np.where(self.lines_connectivity[:, 1] == line_id)[0]
            self.elements_from_line[line_id] = self.lines_connectivity[rows, 0]

    def map_elements_from_surfaces(self):
        self.elements_from_surface.clear()
        for surface_id in np.unique(self.faces_connectivity[:, 1]).astype(int):
            rows = np.where(self.faces_connectivity[:, 1] == surface_id)[0]
            self.elements_from_surface[surface_id] = self.faces_connectivity[rows, 0]

    def map_elements_from_volumes(self):
        self.elements_from_volume.clear()
        for volume_id in np.unique(self.solids_connectivity[:, 1]).astype(int):
            rows = np.where(self.solids_connectivity[:, 1] == volume_id)[0]
            self.elements_from_volume[volume_id] = self.solids_connectivity[rows, 0]

    def get_line_from_element(self, element_id: int) -> int | None:
        line_id = None
        row = np.where(self.lines_connectivity[:, 0] == element_id)[0]
        if row.size:
            line_id = int(self.lines_connectivity[row, 1])

        return line_id

    def get_surface_from_element(self, element_id: int) -> int | None:
        surface_id = None
        row = np.where(self.faces_connectivity[:, 0] == element_id)[0]
        if row.size:
            surface_id = int(self.faces_connectivity[row, 1])

        return surface_id

    def get_volume_from_element(self, element_id: int) -> int | None:
        volume_id = None
        row = np.where(self.solids_connectivity[:, 0] == element_id)[0]
        if row.size:
            volume_id = int(self.solids_connectivity[row, 1])

        return volume_id

    def get_elements_from_lines(self, line_ids: list[int]):
        element_ids = list()
        for line_id in line_ids:
            rows = np.where(self.lines_connectivity[:, 1] == line_id)[0]
            element_ids.extend(self.lines_connectivity[rows, 0])
        return element_ids

    def process_face_elements_connected_to_nodes(self, selected_ids: int | list):

        self.face_elements_connected_to_nodes.clear()
        self.surface_area_from_element_integration.clear()

        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        for tag in selected_ids:
            connect_data = self.get_connectivity_from_surface(tag)

            # integrate the total surface area by the summation of each element area
            area = 0.0
            for element_nodes in connect_data:
                area += self.process_element_area_from_connectivity(element_nodes)

            self.surface_area_from_element_integration[tag] = area
            face_nodes = np.unique(connect_data).astype(int)

            for node in np.sort(face_nodes):
                rows = np.where(connect_data == node)[0]
                # rows = np.sum(np.isin(connect_data, node), axis=1) == 1
                self.face_elements_connected_to_nodes[node].extend(connect_data[rows, :])

    def get_nodes_from_solid_elements(self, node_id: int):
        (rows,) = np.where(self.solids_connectivity[:, 1] == node_id)
        return np.unique(self.solids_connectivity[rows, 4:]).astype(int)

    def map_face_elements_to_solid_elements_reference(self):
        self.face_to_solid_element = dict()
        self.solid_to_face_elements = defaultdict(list)

        if len(self.solids_connectivity) == 0:
            return

        nodes_per_face_element = len(self.faces_connectivity[0, 4:])
        node_ids = np.array([*set(self.faces_connectivity[:, 4:].flatten())], dtype=int)

        mask_0 = np.sum(np.isin(self.solids_connectivity[:, 4:], node_ids), axis=1) >= nodes_per_face_element
        filtered_data = self.solids_connectivity[mask_0, :]

        self.nodes_to_highlight.clear()
        self.efaces_to_highlight.clear()

        for e2d_id, surf_id, _, _, *face_nodes in self.faces_connectivity:
            mask_1 = np.sum(np.isin(filtered_data[:, 4:], face_nodes), axis=1) == nodes_per_face_element

            if np.sum(mask_1) == 0:
                # TODO: remove these attributes when we are sure that no more errors
                # occur after processing the degrees of freedom decoupling.
                # The problematic nodes and face elements are highlighted after closing the section plane UI.
                self.nodes_to_highlight.append(face_nodes)
                self.efaces_to_highlight.append(e2d_id)
                continue

            e3d_id = filtered_data[mask_1, 0][0]
            self.face_to_solid_element[e2d_id] = e3d_id
            self.solid_to_face_elements[e3d_id].append(e2d_id)

    def map_face_elements_to_solid_elements(self):
        """
        This method implements a faster algorithm when compared with
        the one implemented in map_face_elements_to_solid_elements_reference.

        If something goes wrong with this mapping compare the output of this
        with the reference version.
        """

        # Get the set of nodes that are part of a face
        all_face_nodes = np.unique(self.faces_connectivity[:, 4:])

        # Counts how many nodes of a solid are touching a face
        face_nodes_per_solid = np.sum(
            np.isin(
                self.solids_connectivity[:, 4:],
                all_face_nodes,
            ),
            axis=1,
        )

        # Filters all solids that contains a complete external face
        nodes_per_face = self.faces_connectivity[:, 4:].shape[1]
        external_solids = self.solids_connectivity[face_nodes_per_solid >= nodes_per_face]

        # Maps the nodes connected to each solid
        node_to_solid_ids = defaultdict(set)
        for solid_id, _, _, _, *solid_nodes in external_solids:
            for node in solid_nodes:
                node_to_solid_ids[node].add(solid_id)

        self.face_to_solid_element = dict()
        self.solid_to_face_elements = defaultdict(list)

        for face_id, _, _, _, *face_nodes in self.faces_connectivity:
            candidate_solids = list()
            for node in face_nodes:
                candidate = node_to_solid_ids[node]
                candidate_solids.append(candidate)

            # The correspondent element is the one that contains all nodes from this face.
            correspondent_solids = set.intersection(*candidate_solids)
            if not correspondent_solids:
                continue

            # Populate the dicts using the first solid found.
            solid_id, *_ = correspondent_solids
            self.face_to_solid_element[face_id] = solid_id
            self.solid_to_face_elements[solid_id].append(face_id)

    def get_collapsed_elements(self):

        logging.info("Checking collapsed 3D elements... [90/100]")
        mask = self._repeated_mask(self.solids_connectivity[:, 4:])
        collapsed_solids = self.solids_connectivity[mask]
        solids_set = set(collapsed_solids[:, 0].tolist()) if collapsed_solids.size else set()

        logging.info("Checking collapsed 2D elements... [95/100]")
        mask = self._repeated_mask(self.faces_connectivity[:, 4:])
        collapsed_faces = self.faces_connectivity[mask]
        faces_set = set(collapsed_faces[:, 0].tolist()) if collapsed_faces.size else set()

        logging.info("Checking collapsed 1D elements... [98/100]")
        mask = self._repeated_mask(self.lines_connectivity[:, 4:])
        collapsed_lines = self.lines_connectivity[mask]
        lines_set = set(collapsed_lines[:, 0].tolist()) if collapsed_lines.size else set()

        return solids_set, faces_set, lines_set

    def _repeated_mask(self, data: np.ndarray[int]) -> np.ndarray[bool]:
        sorted_data = data.copy()
        sorted_data.sort(axis=1)
        mask = np.any(
            sorted_data[:, :-1] == sorted_data[:, 1:],
            axis=1,
        )
        return mask

    def process_disconnected_nodes_criterion(self):
        """
        This method processes the disconnected nodes criterion for volumes,
        surfaces and lines-related elements.
        """

        disconnected_nodes_data = dict()
        if self.geometry_information.get("volumes"):
            nodes_from_3d_elements = np.unique(self.solids_connectivity[:, 4:].flatten())
            if nodes_from_3d_elements.size:
                if self.nodes_from_volumes.size != nodes_from_3d_elements.size:
                    mask_3d = np.isin(self.nodes_from_volumes, nodes_from_3d_elements, invert=True)
                    if mask_3d.any():
                        disconnected_nodes_data["elements_3D"] = [int(node_id) for node_id in self.nodes_from_volumes[mask_3d]]

        if self.geometry_information.get("surfaces"):
            nodes_from_2d_elements = np.unique(self.faces_connectivity[:, 4:].flatten())
            if nodes_from_2d_elements.size:
                if self.nodes_from_surfaces.size != nodes_from_2d_elements.size:
                    mask_2d = np.isin(self.nodes_from_surfaces, nodes_from_2d_elements, invert=True)
                    if mask_2d.any():
                        disconnected_nodes_data["elements_2D"] = [int(node_id) for node_id in self.nodes_from_surfaces[mask_2d]]

        if self.geometry_information.get("lines"):
            nodes_from_1d_elements = np.unique(self.lines_connectivity[:, 4:].flatten())
            if nodes_from_1d_elements.size:
                if self.nodes_from_lines.size != nodes_from_1d_elements.size:
                    mask_1d = np.isin(self.nodes_from_lines, nodes_from_1d_elements, invert=True)
                    if mask_1d.any():
                        disconnected_nodes_data["elements_1D"] = [int(node_id) for node_id in self.nodes_from_lines[mask_1d]]

        return disconnected_nodes_data

    def get_list_of_disconnected_nodes(self):
        """
        This method returns the disconnected nodes list if they exist.
        """
        disconnected_nodes = self.disconnected_nodes_data.get("elements_3D")
        if isinstance(disconnected_nodes, list) and len(disconnected_nodes):
            return disconnected_nodes

        disconnected_nodes = self.disconnected_nodes_data.get("elements_2D")
        if isinstance(disconnected_nodes, list) and len(disconnected_nodes):
            return disconnected_nodes

        disconnected_nodes = self.disconnected_nodes_data.get("elements_1D")
        if isinstance(disconnected_nodes, list) and len(disconnected_nodes):
            return disconnected_nodes

        return list()

    def get_list_of_nodes_from_collapsed_elements(self):
        """
        This method returns a list containing the nodes from collapsed elements.
        """
        nodes_from_collapsed_1d_elements = self.lines_connectivity[np.array(list(self.collapsed_1d_elements), dtype=int), 4:].flatten()
        nodes_from_collapsed_2d_elements = self.faces_connectivity[np.array(list(self.collapsed_2d_elements), dtype=int), 4:].flatten()
        nodes_from_collapsed_3d_elements = self.solids_connectivity[np.array(list(self.collapsed_3d_elements), dtype=int), 4:].flatten()

        nodes_from_collapsed_elements = np.concatenate(
            [
                nodes_from_collapsed_1d_elements,
                nodes_from_collapsed_2d_elements,
                nodes_from_collapsed_3d_elements,
            ]
        )

        nodes_from_collapsed_elements = np.unique(nodes_from_collapsed_elements)

        return nodes_from_collapsed_elements

    def get_collapsed_elements_data(self) -> dict:
        """
        This method returns the collapsed elements data in form of a dictionary.
        """
        collapsed_elements_data = dict()
        collapsed_1d_elements = list(self.collapsed_1d_elements)
        collapsed_2d_elements = list(self.collapsed_2d_elements)
        collapsed_3d_elements = list(self.collapsed_3d_elements)

        if collapsed_1d_elements or collapsed_2d_elements or collapsed_3d_elements:
            collapsed_elements_data = {
                "collpased_1d_elements": collapsed_1d_elements,
                "collpased_2d_elements": collapsed_2d_elements,
                "collpased_3d_elements": collapsed_3d_elements,
            }

        return collapsed_elements_data

    def get_face_elements_connected_to_nodes(self, node_ids: list[int] | np.ndarray, surface_id: int | None = None) -> dict:
        """
        This method calculates the face elements connected to the nodes.

        Parameters
        ----------
        node_ids: list or np.ndarray
            The selected node ID list in which the element faces should be mapped.

        surface_id: int or None, optional
            It corresponds to the surface tag in which the element faces should be
            mapped.

        Returns
        -------
        face_elements_connected_to_nodes: dict
            A dictionary mapping the element face ID to the neighboor node IDs.
        """
        # t0 = time()

        if surface_id is None:
            mask_0 = np.sum(np.isin(self.faces_connectivity[:, 4:], node_ids), axis=1) >= 1
            filtered_data = self.faces_connectivity[mask_0, :]

        progress = 0
        nodes_number = len(node_ids)
        face_elements_connected_to_nodes = dict()

        for i, node_id in enumerate(node_ids):
            if surface_id is None:
                mask = np.sum(filtered_data[:, 4:] == node_id, axis=1) == 1
                face_elements_connected_to_nodes[node_id, surface_id] = filtered_data[:, 0][mask]

            else:
                connect_from_surface = self.get_connectivity_from_surface(surface_id)

                mask = np.sum(connect_from_surface == node_id, axis=1) == 1
                face_elements_connected_to_nodes[node_id, surface_id] = connect_from_surface[mask, :]

            current_progress = int(100 * i / nodes_number)
            if current_progress % 5 and progress != current_progress:
                progress = current_progress
                logging.info(f"Obtaining face elements connected to nodes... [{progress}/100]\nSurface [{surface_id}]")

        # dt = time() - t0
        # print(f"Loop time: {dt} s")

        return face_elements_connected_to_nodes

    def get_solid_elements_connected_to_nodes(
        self,
        node_ids: list[int] | np.ndarray | None = None,
        surface_id: int | None = None,
        return_nodes: bool = False,
    ) -> dict[int, np.ndarray]:
        """
        This method processes the solid elements connected to the nodes.
        It returns a dictionary mapping the node IDs to the solid element IDs.
        """

        # t0 = time()

        if node_ids is None:
            if isinstance(surface_id, int):
                node_ids = self.get_nodes_from_surface(surface_id)

        if node_ids is None:
            return

        mask_0 = np.sum(np.isin(self.solids_connectivity[:, 4:], node_ids), axis=1) >= 1
        filtered_data = self.solids_connectivity[mask_0, :]

        elem_ids = filtered_data[:, 0]
        connect_nodes = filtered_data[:, 4:]

        # progress = 0
        # number_nodes = len(node_ids)
        solid_elements_connected_to_nodes = dict()

        for i, node_id in enumerate(node_ids):
            # mask = np.sum(connect_nodes == node_id, axis=1) == 1
            # solid_elements_connected_to_nodes[node_id] = elem_ids[mask]
            solid_elements_connected_to_nodes[node_id] = elem_ids[np.where(connect_nodes == node_id)[0]]

            # current_progress = int(100*(i + 1) / number_nodes)
            # if current_progress % 5 and progress != current_progress:
            #     progress = current_progress
            #     logging.info(
            #         f"Obtaining solid elements connected to nodes... [{int(100 * i / number_nodes)}/100]"
            #     )

        # dt = time() - t0
        # print(f"Loop time: {dt} s")

        if return_nodes:
            nodes_from_solid_elements = np.sort(np.unique(connect_nodes).astype(int))
            return solid_elements_connected_to_nodes, nodes_from_solid_elements

        return solid_elements_connected_to_nodes

    def get_solid_elements_from_nodes(
        self,
        node_ids: list[int] | np.ndarray,
        return_enodes: bool = False,
    ):

        mask = np.sum(np.isin(self.solids_connectivity[:, 4:], node_ids), axis=1) >= 1
        element_ids = self.solids_connectivity[mask, 0]

        if not return_enodes:
            return element_ids

        # unique, counts = np.unique(self.solids_connectivity[mask, 4:], return_counts=True)
        # counts_map = dict(zip(unique, counts))

        unique = np.unique(self.solids_connectivity[mask, 4:])
        element_nodes = np.sort(unique)

        return element_ids, element_nodes  # , counts_map

    def get_global_dofs(self, node_ids: list[int] | np.ndarray, dofs_per_node: int):
        pass

    def get_surface_nodal_normals_reference(self, surface_id: int) -> dict:
        """
        This method processes the average normals in the surface nodes considering the element faces
        normals connected to same node.

        Parameters
        ----------
        surface_id: int
            The tag of surface in which the normals average will be computed.

        Returns
        -------
        data_normals: dict
            A dictionary mapping the node IDs to the average normal vector.
        """

        nodes_from_surface = self.get_nodes_from_surface(surface_id)
        if nodes_from_surface is None:
            return dict()

        nodes_from_surface = np.sort(nodes_from_surface)
        face_elements_connected_to_nodes = self.get_face_elements_connected_to_nodes(nodes_from_surface, surface_id)

        data_normals = dict()
        for node_id in nodes_from_surface:
            face_elem_connect = face_elements_connected_to_nodes[node_id, surface_id]

            n = 0.0
            for face_connect in face_elem_connect:
                n += self.get_element_face_normal(face_connect)

            data_normals[node_id] = n / len(face_elem_connect)

        return data_normals

    def get_surface_nodal_normals(self, surface_id: int, volume_id: int):
        """
        This method processes the average normals in the surface nodes considering
        the element faces normals connected to the same node.

        Parameters
        ----------
        surface_id: int
            The tag of surface in which the normals average will be computed.

        Returns
        -------
        avg_node_normals: dict
            A dictionary mapping the node IDs to the average normal vector.
        """

        if isinstance(volume_id, int):
            solid_elements_connected_to_nodes = self.get_solid_elements_connected_to_nodes(surface_id=surface_id)

            elements_set = set()
            for elements in solid_elements_connected_to_nodes.values():
                elements_set |= set(elements)

            filtered_elements = list()
            for elem3d_id in elements_set:
                if self.solids_connectivity[elem3d_id, 1] == volume_id:
                    filtered_elements.append(elem3d_id)

            filt_element3d_connect = self.solids_connectivity[filtered_elements, 4:]

        face_connectivity = self.get_connectivity_from_surface(surface_id)

        if face_connectivity is None:
            return

        # noodes per element
        nodes_per_element = face_connectivity[0, :].size

        # tria3 surface element
        if nodes_per_element == 3:
            column_indexes = [(0, 1, 2)]

        # quad4 surface element
        elif nodes_per_element == 4:
            column_indexes = [(0, 1, 2), (0, 2, 3)]

        # tria6 surface element
        elif nodes_per_element == 6:
            column_indexes = [(3, 1, 4), (3, 4, 2), (3, 2, 5), (3, 5, 0)]

        # quad8 surface element
        elif nodes_per_element == 8:
            column_indexes = [(0, 4, 7), (4, 1, 5), (5, 2, 6), (6, 3, 7), (4, 6, 7), (4, 5, 6)]

        else:
            return NotImplementedError(f"Normal not implemented for surface with {nodes_per_element} nodes")

        Vn_sum = defaultdict(float)

        for indexes in column_indexes:
            inside_face_connectivity = face_connectivity[:, indexes]
            norm_cross = self.process_stacked_cross_products(inside_face_connectivity)

            for i, e_nodes in enumerate(inside_face_connectivity):
                mask = np.sum(np.isin(filt_element3d_connect, e_nodes), axis=1) == 3
                connect_3d = filt_element3d_connect[mask, :].flatten()
                if connect_3d.size == 0:
                    print(f"No solid element touches the surface nodes: {e_nodes}")

                center_coords_2d = np.average(self.nodal_coordinates[e_nodes, 1:], axis=0)
                center_coords_3d = np.average(self.nodal_coordinates[connect_3d, 1:], axis=0)
                vector_inside = center_coords_3d - center_coords_2d
                dot_product = np.dot(norm_cross[i, :], vector_inside)

                factor = 1 if dot_product < 0 else -1

                for node in e_nodes:
                    Vn_sum[node] += norm_cross[i, :] * factor

        nodal_unit_normals = dict()

        for node in self.get_nodes_from_surface(surface_id):
            Vn = Vn_sum[node]
            nodal_unit_normals[node] = Vn / np.linalg.norm(Vn)

        return nodal_unit_normals

    def get_stacked_normals_for_surface_elements(self, surface_id: int):
        """
        This method processes the stacked surface elements normals from
        selected surface.

        Parameter
        ---------
        surface_id: int
            The surface ID.

        Returns
        -------
        stacked_normals: np.ndarray
            The stacked element surface normals.
        """

        face_connectivity = self.get_connectivity_from_surface(surface_id)

        if face_connectivity is None:
            return

        stacked_normals = self.process_stacked_cross_products(face_connectivity)

        return stacked_normals

    def process_stacked_cross_products(self, connectivities: np.ndarray, normalized: bool = True):
        """
        This method processes the stacked cross products for the given
        triangular connectivities.

        Parameter
        ---------
        connectivities: np.ndarray
            The stacked triangular connectivities.

        normalized: bool, optional
            This argument controls when the output vectors will be
            normalized (default is True).

        Returns
        -------
        stacked_cross_products: np.ndarray
            The stacked cross products for each triangular connectivity.
        """

        nodes_1 = connectivities[:, 0]
        nodes_2 = connectivities[:, 1]
        nodes_3 = connectivities[:, 2]

        X1 = self.nodal_coordinates[nodes_1, 1]
        Y1 = self.nodal_coordinates[nodes_1, 2]
        Z1 = self.nodal_coordinates[nodes_1, 3]

        X2 = self.nodal_coordinates[nodes_2, 1]
        Y2 = self.nodal_coordinates[nodes_2, 2]
        Z2 = self.nodal_coordinates[nodes_2, 3]

        X3 = self.nodal_coordinates[nodes_3, 1]
        Y3 = self.nodal_coordinates[nodes_3, 2]
        Z3 = self.nodal_coordinates[nodes_3, 3]

        v_21 = np.array([X2 - X1, Y2 - Y1, Z2 - Z1]).T
        v_31 = np.array([X3 - X1, Y3 - Y1, Z3 - Z1]).T

        stacked_cross_products = np.cross(v_21, v_31, axis=1)

        if normalized:
            norm_cross = np.linalg.norm(stacked_cross_products, axis=1).reshape(-1, 1)
            return stacked_cross_products / norm_cross

        return stacked_cross_products

    def compute_nodal_areas(self):
        self.nodal_area.clear()
        for node, connectivities in self.face_elements_connected_to_nodes.items():
            for connect in connectivities:
                area = self.process_element_area_from_connectivity(connect)
                if area is not None:
                    self.nodal_area[node].append(area)

    def process_element_area_from_connectivity(self, elem_connect: list[int] | np.ndarray) -> np.ndarray | None:
        """
        This method calculates the area of a surface element
        based on their connectivities.

        Parameters
        ----------
        elem_connect: list
            The element face connectivity.

        Returns
        -------
        area: float
            The area of surface element.

        """

        def compute_triangular_area(nodes: list):
            coord_A = self.nodal_coordinates[nodes[0], 1:]
            coord_B = self.nodal_coordinates[nodes[1], 1:]
            coord_C = self.nodal_coordinates[nodes[2], 1:]
            vect_AB = coord_B - coord_A
            vect_BC = coord_C - coord_B
            area = np.linalg.norm(np.cross(vect_AB, vect_BC)) / 2
            return area

        # internal triangles of TRIA3 element
        if len(elem_connect) == 3:
            points_nodes = [
                [elem_connect[0], elem_connect[1], elem_connect[2]],
            ]

        # internal triangles of QUAD4 element
        elif len(elem_connect) == 4:
            points_nodes = [
                [elem_connect[0], elem_connect[1], elem_connect[2]],
                [elem_connect[0], elem_connect[2], elem_connect[3]],
            ]

        # internal triangles of TRIA6 element
        elif len(elem_connect) == 6:
            points_nodes = [
                [elem_connect[0], elem_connect[3], elem_connect[5]],
                [elem_connect[5], elem_connect[3], elem_connect[1]],
                [elem_connect[1], elem_connect[4], elem_connect[5]],
                [elem_connect[5], elem_connect[4], elem_connect[2]],
            ]

        # internal triangles of QUAD8 element
        elif len(elem_connect) == 8:
            points_nodes = [
                [elem_connect[7], elem_connect[0], elem_connect[4]],
                [elem_connect[4], elem_connect[1], elem_connect[5]],
                [elem_connect[5], elem_connect[7], elem_connect[4]],
                [elem_connect[5], elem_connect[2], elem_connect[6]],
                [elem_connect[6], elem_connect[3], elem_connect[7]],
                [elem_connect[7], elem_connect[5], elem_connect[6]],
            ]

        else:
            points_nodes = list()

        area = 0.0
        for nodes in points_nodes:
            area += compute_triangular_area(nodes)

        return area

    def set_face_element_thickness(self, surface_id: int, data: dict):
        for face_element in self.elements_from_surface.get(surface_id, list()):
            self.face_element_thickness[face_element] = data

    def get_mesh_info(self):
        n_nodes = self.nodal_coordinates.shape[0]
        n_face_elements = self.faces_connectivity.shape[0]
        n_solid_elements = self.solids_connectivity.shape[0]
        return n_nodes, n_face_elements, n_solid_elements

    def compute_mesh_quality_parameters(self) -> dict | None:

        quality_parameters = [
            "gamma",
            "volume",
            "minSJ",
            "aspectRatio",
        ]

        logging.info("Computing mesh quality metrics... [10/100]")
        _, element_tags, _ = gmsh.model.mesh.get_elements(3, -1)
        if not element_tags:
            return

        # process the mesh quality metrics
        elements = element_tags[0]
        N_elem = len(elements)
        N_param = len(quality_parameters)
        quality_table = np.zeros((N_elem, N_param), dtype=float)

        logging.info("Computing mesh quality metrics... [25/100]")
        min_edge_quals = gmsh.model.mesh.getElementQualities(elements, "minEdge")
        max_edge_quals = gmsh.model.mesh.getElementQualities(elements, "maxEdge")

        logging.info("Computing mesh quality metrics... [40/100]")
        quality_table[:, 0] = gmsh.model.mesh.get_element_qualities(elements, "gamma")
        quality_table[:, 1] = gmsh.model.mesh.get_element_qualities(elements, "volume")
        quality_table[:, 2] = gmsh.model.mesh.get_element_qualities(elements, "minSJ")
        quality_table[:, 3] = max_edge_quals / min_edge_quals  # aspect ratio

        # compute the mesh quality statistics
        logging.info("Computing mesh quality metrics... [70/100]")
        quality_statistics: dict[MeshQualityParams, list[float]] = dict()
        for i, parameter in enumerate(quality_parameters):
            column = quality_table[:, i]
            worst = np.max(column) if (parameter == "aspectRatio") else np.min(column)
            quality_statistics[parameter] = [worst, np.mean(column), np.std(column)]

        # compute the bad elements
        logging.info("Computing mesh quality metrics... [85/100]")
        bad_elements: dict[MeshQualityParams, np.ndarray] = dict()
        for j, parameter in enumerate(quality_parameters):
            limit = self.quality_bins.get(parameter)
            if parameter == "aspectRatio":
                bad_elements[parameter] = np.where(quality_table[:, j] > limit[0])[0]
            else:
                bad_elements[parameter] = np.where(quality_table[:, j] < limit[1])[0]

        # compute the histogram data
        logging.info("Computing mesh quality metrics... [95/100]")
        histograms_data: dict[MeshQualityParams, dict] = dict()
        for i, parameter in enumerate(quality_parameters):
            column = quality_table[:, i]
            bins = np.linspace(np.min(column), np.max(column), 30)
            hist, bin_edges = np.histogram(column, bins=bins)

            histograms_data[parameter] = [
                hist,
                bin_edges,
                np.percentile(column, 5),
                np.percentile(column, 95),
            ]

        self.mesh_quality_data = {
            "statistics": quality_statistics,
            "bad_elements": bad_elements,
            "histograms_data": histograms_data,
        }

    def compute_initial_mesh_size(self, path: str, geometry_tolerance: float = 1e-10, threads: int = 0):
        gmsh.initialize("", False, interruptible=False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        # gmsh.option.setNumber("General.NumThreads", threads)
        gmsh.option.setNumber("Geometry.Tolerance", geometry_tolerance)

        gmsh.open(str(path))

        try:
            geometry_info = defaultdict(list)
            for dim, tag in gmsh.model.getEntities():
                if dim == 0:
                    continue

                value = gmsh.model.occ.getMass(dim, tag)
                if dim == 1:
                    geometry_info["lengths"].append(value)

                elif dim == 2:
                    geometry_info["areas"].append(value)

                elif dim == 3:
                    geometry_info["volumes"].append(value)

            total_area = np.sum(geometry_info["areas"])
            if total_area <= 5e7:
                number_of_elements = 4e4
            else:
                number_of_elements = 1e5

            area_elem = total_area / number_of_elements

            # the length side of equilateral triangle
            length = np.ceil(np.sqrt(2 * area_elem))

            return length * self.geometry_qf

        finally:
            pass

    def compute_bounding_box_sizes(self, geo_entities):
        xmin = ymin = zmin = xmax = ymax = zmax = 0
        volume = 0
        for dim, tag in geo_entities:
            # This mass is considering a density of 1, so it is equal the solid volume
            volume += gmsh.model.occ.getMass(dim, tag)
            xmin2, ymin2, zmin2, xmax2, ymax2, zmax2 = gmsh.model.getBoundingBox(dim, tag)
            xmin = min(xmin, xmin2)
            ymin = min(ymin, ymin2)
            zmin = min(zmin, zmin2)

            xmax = max(xmax, xmax2)
            ymax = max(ymax, ymax2)
            zmax = max(zmax, zmax2)

        bb_sides = sorted([(xmax - xmin), (ymax - ymin), (zmax - zmin)], reverse=True)

        return bb_sides, volume

    def process_geometry_information(self):
        self.clear_geometry_data()

        unit_factor = self.get_length_unit_factor()
        labels = ["points", "lines", "surfaces", "volumes"]

        for dim, tag in gmsh.model.getEntities():
            label = labels[dim]
            self.geometry_information[label].append(tag)

            if dim == 0:
                continue

            value = 0.0
            if self.geometry_imported:
                value = gmsh.model.occ.getMass(dim, tag)

            if dim == 3:
                self.volume_from_bodies[tag] = value * (unit_factor**3)

            elif dim == 2:
                self.area_from_surfaces[tag] = value * (unit_factor**2)
                if self.area_from_surfaces[tag] == 0:
                    continue

                uv_min, uv_max = gmsh.model.getParametrizationBounds(dim, tag)
                uv_mid = (uv_min + uv_max) / 2
                center = gmsh.model.getValue(dim, tag, uv_mid) * unit_factor
                self.surfaces_centers[tag] = center

            elif dim == 1:
                self.length_from_lines[tag] = value * (unit_factor**1)

    def process_downwards_adjacencies_from_entities(self):
        """
        This method processes the downwards adjacencies
        from the geometric entities.
        """

        self.surfaces_from_volume.clear()
        self.lines_from_surface.clear()
        self.points_from_line.clear()

        for dim, tag in gmsh.model.getEntities():
            _, downwards = gmsh.model.getAdjacencies(dim, tag)
            downwards = [int(_id) for _id in downwards]

            if dim == 3:
                self.surfaces_from_volume[tag] = downwards

            elif dim == 2:
                self.lines_from_surface[tag] = downwards

            elif dim == 1:
                self.points_from_line[tag] = downwards

    def process_upwards_adjacencies_from_entities(self):
        """
        This method processes the upwards adjacencies
        from the geometric entities.
        """

        self.volumes_from_surface.clear()
        self.surfaces_from_line.clear()
        self.lines_from_point.clear()

        for vol_id, surface_ids in self.surfaces_from_volume.items():
            for surface_id in surface_ids:
                self.volumes_from_surface[surface_id].append(vol_id)

        for surf_id, line_ids in self.lines_from_surface.items():
            for line_id in line_ids:
                self.surfaces_from_line[line_id].append(surf_id)

        for line_id, point_ids in self.points_from_line.items():
            for point_id in point_ids:
                self.lines_from_point[point_id].append(line_id)

    def are_there_volumes_in_geometry(self) -> bool:
        volumes = self.geometry_information.get("volumes")
        if isinstance(volumes, list):
            if volumes:
                return True
        return False

    def _get_connectivity_array(self, input_dict):
        """
        The returned value is an array where each line is a connectivity
        and the colums follow this order:

        Element index || Line/Face/Solid tag || Element type || Nodes per element || Connectivity
        """

        if not isinstance(input_dict, dict):
            raise TypeError("get_connectivity_data only accepts dicts as input.")

        max_cols = 0
        n_list = list()
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

        internal_indexes = np.arange(n, dtype=int)
        output_data[:, 0] = internal_indexes

        start, end, ind = 0, 0, 0
        for (entity_dim, entity_tag), e_data in input_dict.items():
            for etype_tag, data in e_data.items():
                end += n_list[ind]
                indexes = data["indexes"]
                connectivity = data["array_element_nodes"]

                rows = len(indexes)
                cols = connectivity.shape[1]
                aux = np.ones(rows, dtype=int)

                output_data[start:end, 1] = aux * entity_tag
                output_data[start:end, 2] = aux * etype_tag
                output_data[start:end, 3] = aux * cols
                output_data[start:end, 4 : 4 + cols] = connectivity
                gmsh_elements[start:end] = indexes

                start = end
                ind += 1

        map_elements = dict(zip(gmsh_elements, internal_indexes))

        return output_data, map_elements

    def get_array_based_elements_mapping(self, entity: str = "lines"):
        """ """
        if entity == "lines":
            keys = list(self.map_line_elements.keys())
            values = list(self.map_line_elements.values())

        elif entity == "faces":
            keys = list(self.map_face_elements.keys())
            values = list(self.map_face_elements.values())

        elif entity == "solids":
            keys = list(self.map_solid_elements.keys())
            values = list(self.map_solid_elements.values())

        else:
            return None

        return np.array([keys, values], dtype=int).T

    def process_element_average_coordinates(self, element_ids: list[int]) -> dict:
        """
        This method calculates the element average center coordinates of the selected element ID.

        Parameters
        ----------
        element_ids: list
            A list of selected solid element IDs.

        Returns
        -------
        solid_elements_center: dict
            A dictionary that maps each element ID to the respective element center coordinates.

        """

        solid_elements_center = dict()

        for i, element_id in enumerate(element_ids):
            nodes = self.get_nodes_from_solid_elements(element_id)
            solid_elements_center[element_id] = np.average(self.nodal_coordinates[nodes, 1:], axis=0)

        return solid_elements_center

    def get_average_nodal_coordinates(self, surface_ids: list[int], averaged=False):
        nodal_coordinates = self.nodal_coordinates

        rows = list()
        for surface_id in surface_ids:
            nodes = self.get_nodes_from_surface(surface_id)
            if nodes is None:
                continue

            if averaged:
                for row in nodes:
                    rows.append(row)
            else:
                rows.append(list(nodes))

        center_coords = list()
        if rows:
            if averaged:
                avg_coords = np.average(nodal_coordinates[rows, 1:], axis=0)
                center_coords.append(avg_coords)
            else:
                for row in rows:
                    avg_coords = np.average(nodal_coordinates[row, 1:], axis=0)
                    center_coords.append(avg_coords)

        return center_coords

    def get_geometric_surface_center(self, surface_id: int) -> np.ndarray | None:
        return self.surfaces_centers.get(surface_id)

    def get_element_face_normal(self, connect: np.ndarray):

        coords = self.nodal_coordinates[connect, 1:]

        P1 = coords[0, :]
        P2 = coords[1, :]
        P3 = coords[2, :]

        P2P1 = np.array(P2 - P1)
        P3P1 = np.array(P3 - P1)

        cross = np.cross(P2P1, P3P1)
        norm_cross = np.linalg.norm(cross)

        if not norm_cross:
            return 0

        cross /= norm_cross

        if self.solids_connectivity.size:
            mask = np.sum(np.isin(self.solids_connectivity[:, 4:], connect), axis=1) == len(connect)
            solid_element_id = self.solids_connectivity[mask, 0]
            solid_connectivity = self.solids_connectivity[solid_element_id, 4:].flatten()

            face_element_center = np.average(coords, axis=0)
            solid_element_center = np.average(self.nodal_coordinates[solid_connectivity, 1:], axis=0)
            vector = solid_element_center - face_element_center

            if np.dot(cross, vector) > 0:
                cross *= -1
                print(f"The element face normal has been inverted -> corresponding solid element {solid_element_id}.")

        return cross

    def get_element_face_normal_batched(self, face_connectivity: np.ndarray) -> np.ndarray:
        """
        This should work similar to the method `get_element_face_normal`.

        While there the expected parameter is a single connectivity row,
        containing only the node indexes, here we allow for 2D arrays with
        multiple entries on each line and it is required to include the indexes
        of the whole array, just like in `self.faces_connectivity`.

        (The names are a bit misleading, we should try to fix it some day)
        """

        original_ndim = face_connectivity.ndim
        if original_ndim == 1:
            face_connectivity = face_connectivity.reshape(1, -1)

        face_coords = self.nodal_coordinates[face_connectivity[:, 4:], 1:]
        P1 = face_coords[:, 0, :]
        P2 = face_coords[:, 1, :]
        P3 = face_coords[:, 2, :]

        P2P1 = np.array(P2 - P1)
        P3P1 = np.array(P3 - P1)

        cross = np.cross(P2P1, P3P1, axis=1)
        norm_cross = np.linalg.norm(cross, axis=1).reshape(-1, 1)
        cross /= norm_cross

        if self.solids_connectivity.size:
            solid_element_ids = np.array([self.face_to_solid_element[i] for i in face_connectivity[:, 0]])
            solid_connectivity = self.solids_connectivity[solid_element_ids]
            solid_coords = self.nodal_coordinates[solid_connectivity[:, 4:], 1:]

            face_element_center = np.average(face_coords, axis=1)
            solid_element_center = np.average(solid_coords, axis=1)
            vector = solid_element_center - face_element_center

            inverted_normal_mask = np.vecdot(cross, vector, axis=1) > 0
            if np.any(inverted_normal_mask):
                cross[inverted_normal_mask] *= -1

                broken_face_ids = face_connectivity[inverted_normal_mask, 0]
                broken_solid_ids = solid_connectivity[inverted_normal_mask, 0]

                for f, s in zip(broken_face_ids, broken_solid_ids):
                    print(f"Inverted normal found on face element {f} associated to solid element {s}.")

            if original_ndim == 1:
                cross = cross.ravel()

        return cross

    def set_nodal_normals_data(self, surface_id: int, normals_data: dict):
        for node_id, nodal_normal in normals_data.items():
            self.nodal_normals_data[surface_id, node_id] = nodal_normal

    def get_principal_diagonal_structure_parallelepiped(self):
        """
        This method updates the principal structure diagonal parallelepiped attribute.

        """
        nodal_coordinates = self.nodal_coordinates.copy()
        x_min, y_min, z_min = np.min(nodal_coordinates[:, 1:], axis=0)
        x_max, y_max, z_max = np.max(nodal_coordinates[:, 1:], axis=0)
        principal_diagonal = np.sqrt((x_max - x_min) ** 2 + (y_max - y_min) ** 2 + (z_max - z_min) ** 2)
        return principal_diagonal

    def check_selected_ids(
        self,
        selected_ids: str | int | list[int] | np.ndarray,
        selection: str = "nodes",
        single_id: bool = False,
    ):
        try:
            message = ""
            if isinstance(selected_ids, str):
                tokens = selected_ids.strip().split(",")
                try:
                    tokens.remove("")
                except Exception:
                    pass
                list_ids = list(map(int, tokens))

            elif isinstance(selected_ids, list):
                list_ids = selected_ids

            elif isinstance(selected_ids, (tuple, np.ndarray)):
                list_ids = list(selected_ids)

            elif isinstance(selected_ids, int):
                list_ids = [selected_ids]

            all_ids = list()
            if selection == "nodes":
                all_ids = list(self.nodal_coordinates[:, 0])

            elif selection == "face_elements":
                all_ids = list(self.faces_connectivity[:, 0])

            elif selection == "solid_elements":
                all_ids = list(self.solids_connectivity[:, 0])

            elif selection == "points":
                if selection in self.geometry_information.keys():
                    all_ids = self.geometry_information["points"]

            elif selection == "lines":
                if "lines" in self.geometry_information.keys():
                    all_ids = self.geometry_information["lines"]

            elif selection == "surfaces":
                if selection in self.geometry_information.keys():
                    all_ids = self.geometry_information["surfaces"]

            elif selection == "volumes":
                if selection in self.geometry_information.keys():
                    all_ids = self.geometry_information["volumes"]

            else:
                return None

            _size = len(all_ids)

            if len(list_ids) == 0:
                message = "An empty input field has been detected for the Selection ID. "
                message += "You should enter a valid Selection ID to proceed."

            elif len(list_ids) >= 1:
                if single_id and len(list_ids) > 1:
                    message = "Multiple Selected IDs"

                else:
                    try:
                        for _id in list_ids:
                            if _id not in all_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                                message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                                break

                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                        message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                        message += f"\n\n{str(error_log)}"

        except Exception as log_error:
            message = "Wrong input for the Selected ID's. "
            message += f"\n\n{str(log_error)}"

        if message != "":
            window_title = "Error"
            title = "Invalid entry to the Selection ID"
            error_data = [window_title, title, message]
            return None, error_data

        if single_id:
            return list_ids[0], None
        else:
            return list_ids, None

    def get_nearest_node_from_coordinate(self, point_coords: np.ndarray):
        """
        This method calculates the nearest node from the input
        point's coordinates.

        Parameter
        ---------
        point_coords: np.ndarray
            The point coordinates.

        Return
        ------
        nearest_node: int
            The nearest Node ID.

        nearest_coords: np.ndarray
            The nearest Node coordinates.
        """
        if not self.nodal_coordinates.any():
            return None, None

        diff = self.nodal_coordinates[:, 1:] - point_coords
        indexes = np.argsort(np.linalg.norm(diff, axis=1))

        nearest_node = int(self.nodal_coordinates[indexes[0], 0])
        nearest_coords = self.nodal_coordinates[indexes[0], 1:]

        return nearest_node, nearest_coords

    def get_elements_and_nodes_from_sphere(
        self,
        surface_ids,
        selection_radius,
        averaged=False,
        filter_type=0,
        export_data=False,
    ):
        list_center_coords = self.get_average_nodal_coordinates(surface_ids, averaged=averaged)

        if not list_center_coords:
            return list(), list()

        selected_elements = list()
        nodes_inside_sphere = list()
        node_indexes = self.nodal_coordinates[:, 0]
        nodal_coordinates = self.nodal_coordinates[:, 1:]

        for center_coords in list_center_coords:
            if filter_type == 0:  # filters the elements inside sphere based on elements coordinates center
                filter_radius = 1.1 * selection_radius
                _, filtered_elements = self.get_nodes_inside_sphere_and_its_elements_connected(center_coords, filter_radius)

                if filtered_elements:
                    filtered_solid_elements = self.process_element_average_coordinates(filtered_elements)
                    element_indexes = np.array(list(filtered_solid_elements.keys()), dtype=int)
                    elements_center_coordinates = np.array(list(filtered_solid_elements.values()), dtype=float)
                else:
                    return

                diff_nodes = np.linalg.norm(nodal_coordinates - center_coords, axis=1)
                diff_elem = np.linalg.norm(elements_center_coordinates - center_coords, axis=1)

                mask_nodes = diff_nodes <= selection_radius
                mask_elem = diff_elem <= selection_radius

                if sum(mask_nodes):
                    for node_id in node_indexes[mask_nodes]:
                        if node_id not in nodes_inside_sphere:
                            nodes_inside_sphere.append(node_id)

                if sum(mask_elem):
                    for element_id in element_indexes[mask_elem]:
                        if element_id not in selected_elements:
                            selected_elements.append(element_id)

            else:  # filters the elements inside sphere based on nodal coordinates
                diff_nodes = np.linalg.norm(nodal_coordinates - center_coords, axis=1)
                mask_nodes = diff_nodes <= selection_radius

                if sum(mask_nodes):
                    nodes_inside_sphere = node_indexes[mask_nodes]
                    selection_data = self.get_solid_elements_connected_to_nodes(node_ids=nodes_inside_sphere)
                    for _node, element_ids in selection_data.items():
                        for element_id in element_ids:
                            if element_id not in selected_elements:
                                selected_elements.append(element_id)

        self.nodes_inside_sphere = nodes_inside_sphere
        self.selected_elements = selected_elements

        if export_data:
            # list_nodes = np.array(nodes_inside_sphere, dtype=int).reshape(-1,1)
            # list_elements = np.array(selected_elements, dtype=int).reshape(-1,1)
            list_nodes = np.array(nodes_inside_sphere).reshape(-1, 1)
            list_elements = np.array(selected_elements).reshape(-1, 1)
            connectivity = self.solids_connectivity[:, 4:]
            rows = len(list_elements)
            cols = connectivity.shape[1]
            data_elem = np.zeros((rows, cols + 1), dtype=int)
            data_elem[:, 0] = selected_elements
            data_elem[:, 1:] = connectivity[selected_elements, :]

            np.savetxt("nodes_inside_sphere.dat", list_nodes, delimiter=";", fmt="%i")
            np.savetxt("selected_elements.dat", list_elements, delimiter=";", fmt="%i")
            np.savetxt("selected_elements_data.dat", data_elem, delimiter=";", fmt="%i")
            # print(f"Number of nodes: {len(nodes_inside_sphere)}")
            # print(f"Number of elements: {len(selected_elements)}")

        return selected_elements, nodes_inside_sphere

    def get_nodes_inside_sphere_and_its_elements_connected(self, center_coords, selection_radius):
        node_indexes = self.nodal_coordinates[:, 0]
        nodal_coordinates = self.nodal_coordinates[:, 1:]

        diff_nodes = np.linalg.norm(nodal_coordinates - center_coords, axis=1)
        mask_nodes = diff_nodes <= selection_radius
        nodes_inside_sphere = node_indexes[mask_nodes]

        selection_data = self.get_solid_elements_connected_to_nodes(node_ids=nodes_inside_sphere)

        _selected_elements = list()
        for _node, element_ids in selection_data.items():
            _selected_elements.extend(element_ids)

        selected_elements = np.array([*set(_selected_elements)], dtype=int)

        return nodes_inside_sphere, list(selected_elements)

    def set_error_data(self, title: str, message: str):
        self.error_data = {"title": title, "message": message}

    def reset_error_data(self):
        self.error_data.clear()
