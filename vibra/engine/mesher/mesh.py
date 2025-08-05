import logging
import os
import sys
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from time import time
from traceback import print_exception

import gmsh
import numpy as np
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    VTK_QUADRATIC_HEXAHEDRON,
    VTK_QUADRATIC_TETRA,
    VTK_TETRA,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

from vibra.engine.mesher.element_type import (
    DEFAULT_ELEMENT_TYPE,
    TETRAHEDRON_4,
    ElementType,
)


class Mesh:
    def __init__(self, **kwargs):
        self.length_unit = kwargs.get("length_unit", "milimeter")
        self.geometry_qf = kwargs.get("geometry_qf", 1.0)

        self.geometry_setup = None
        self.mesh_setup = None
        self.geometry_imported = True

        self.reset_variables()

    def reset_variables(self):
        self.element_type = DEFAULT_ELEMENT_TYPE

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
        self.lines_connectivity = np.zeros((0, 4), dtype=int)
        self.faces_connectivity = np.zeros((0, 4), dtype=int)
        self.solids_connectivity = np.zeros((0, 4), dtype=int)

        self.geometry_information = defaultdict(list)

        self.mesh_quality_parameters = [
            "gamma",
            "volume",
            "minSJ",
            "aspectRatio",
        ]
        self.quality_bins = {
            "gamma": (0.7, 0.15),
            "volume": (1e-3, 0),
            "minSJ": (0.3, 0.1),
            "aspectRatio": (4, 1.5),
        }
        self.mesh_quality = dict()
        self.mesh_quality_statistics = dict()
        self.mesh_bad_elements = dict()
        self.mesh_quality_histograms_data = dict()
        self.mesh_quality_temp = None

        self.collapsed_solids = set()
        self.collapsed_faces = set()
        self.collapsed_lines = set()

        self.nodes_from_points = dict()
        self.points_from_nodes = dict()
        self.nodes_from_lines = dict()
        self.nodes_from_surfaces = dict()
        self.nodes_from_volumes = dict()
        self.surfaces_from_node = defaultdict(list)

        self.map_solid_elements = dict()
        self.map_face_elements = dict()
        self.map_line_elements = dict()

        self.elements_from_line = dict()
        self.elements_from_surface = dict()
        self.elements_from_volume = dict()

        self.line_from_element = dict()
        self.surface_from_element = dict()
        self.volume_from_element = dict()

        self.face_to_solid_element = dict()
        self.solid_to_face_elements = defaultdict(list)

        self.face_element_thickness = dict()
        self.surface_from_solid_element = defaultdict(list)

        self.connectivity_from_lines = dict()
        self.connectivity_from_surfaces = dict()

        self.nodes_from_face_element = dict()
        self.nodes_from_solid_element = dict()
        self.solid_elements_center = dict()

        self.nodes_out_of_face_element = dict()
        self.surface_area_from_element_integration = dict()

        self.nodal_area = defaultdict(list)

        self.normals_surface = dict()
        self.curvatures_surface = dict()
        self.nodal_normals_data = dict()

        self.principal_diagonal = None
        self.nodes_collapsed_elements = None

        self.cache_nodal_coordinates = None
        self.cache_lines_connectivity = None
        self.cache_faces_connectivity = None
        self.cache_solids_connectivity = None

        self.cache_surfaces_from_volume = dict()
        self.cache_lines_from_surface = dict()
        self.cache_points_from_line = dict()

        self.cache_connectivity_from_lines = dict()
        self.cache_connectivity_from_surfaces = dict()
        self.decoupled_points = list()

    def set_length_unit(self, length_unit: str = "milimeter"):
        self.length_unit = length_unit

    def get_length_unit_factor(self):
        if self.length_unit == "milimeter":
            return 1e-3
        elif self.length_unit == "inch":
            return 0.0254
        else:
            return 1

    def load_cad(
        self,
        path: (str | Path),
        *,
        minimum_element_size: float = 30.0,
        maximum_element_size: float = 30.0,
        element_type: ElementType = DEFAULT_ELEMENT_TYPE,
        geometry_tolerance: float = 1e-8,
        size_factor: float = 1,
        dimension: int = 3,
        threads: int = 0,
        gmsh_gui: bool = False,
        mesh_refinement_parameters=list(),
        mesh_connection=True,
        **kwargs,
    ):
        self.mesh_setup = dict(
            minimum_element_size=minimum_element_size,
            maximum_element_size=maximum_element_size,
            element_type=element_type,
            geometry_tolerance=geometry_tolerance,
            size_factor=size_factor,
            dimension=dimension,
            threads=threads,
            mesh_refinement_parameters=mesh_refinement_parameters,
            mesh_connection=mesh_connection,
        )

        self.mesh_connection = mesh_connection

        gmsh.initialize("", False, interruptible=False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", threads)
        gmsh.option.setNumber("Geometry.Tolerance", geometry_tolerance)

        logging.info("Loading geometry... [10/100]")
        gmsh.open(str(path))

        logging.info("Configuring mesh... [20/100]")
        self._configure_mesh(
            element_type,
            minimum_element_size,
            maximum_element_size,
            size_factor,
            mesh_refinement_parameters,
        )

        gmsh.model.occ.synchronize()
        self.element_type = element_type

        if self.mesh_connection:
            self._merge_nodes_from_adjacent_volumes()

        try:
            logging.info("Generating mesh... [45/100]")
            gmsh.model.mesh.generate(dim=dimension)

            logging.info("Generating mesh... [60/100]")
            self.process_geometry_information()
            self.process_downwards_adjacencies_from_entities()
            self.process_upwards_adjacencies_from_entities()

            gmsh.model.mesh.removeDuplicateNodes()

        except Exception as error_log:
            print_exception(error_log)
            gmsh.finalize()

        logging.info("Post-processing mesh... [70/100]")
        self.post_process_mesh_data()
        self.calculate_mesh_quality_parameters()
        self.calculate_mesh_quality_statistics()
        self.calculate_mesh_bad_elements()
        self.calculate_mesh_quality_histograms()

        if gmsh_gui:
            gmsh.fltk.run()

        gmsh.finalize()

        logging.info(
            f"Mesh generated with {len(self.nodal_coordinates)} nodes"
            f", {len(self.lines_connectivity)} dim 1"
            f", {len(self.faces_connectivity)} dim 2"
            f"and {len(self.solids_connectivity)} dim 3 elements"
        )

        return self

    def _merge_nodes_from_adjacent_volumes(self):
        """This method merges all nodes from adjacent volumes."""
        # lines_list = gmsh.model.getEntities(1)
        volumes_list = gmsh.model.getEntities(3)
        # gmsh.model.occ.fragment(lines_list, lines_list)
        gmsh.model.occ.fragment(volumes_list, volumes_list)
        gmsh.model.occ.synchronize()

    def load_mesh(
        self,
        path: Path | str,
        element_type: ElementType = DEFAULT_ELEMENT_TYPE,
        geometry_tolerance: float = 1e-8,
        threads: int = 0,
        gmsh_gui: bool = False,
    ):
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", threads)
        gmsh.option.setNumber("Geometry.Tolerance", geometry_tolerance)

        logging.info("Loading mesh data... [25/100]")
        gmsh.open(path)

        logging.info("Loading mesh data... [90/100]")
        gmsh.model.occ.synchronize()

        self.element_type = element_type

        logging.info("Post-processing mesh... [50/100]")
        self.post_process_mesh_data()

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

    def process_downwards_adjacencies_from_mesh_data(self):
        """This method computes the downwards adjacencies from entities
        from the solids, faces and lines connectivities matrices.
        """

        self.process_geometry_information()

        e_nodes_2d = self.faces_connectivity[0, 4:].size
        for vol_id in self.geometry_information.get("volumes"):
            nodes_from_volume = self.nodes_from_volumes[vol_id]
            mask = (
                np.sum(
                    np.isin(self.faces_connectivity[:, 4:], nodes_from_volume), axis=1
                )
                == e_nodes_2d
            )
            self.surfaces_from_volume[vol_id] = [
                int(tag) for tag in set(self.faces_connectivity[mask, 1])
            ]

        if self.lines_connectivity.size:
            e_nodes_1d = self.lines_connectivity[0, 4:].size
            for surf_id in self.geometry_information.get("surfaces"):
                nodes_from_surface = self.nodes_from_surfaces[surf_id]
                mask = (
                    np.sum(
                        np.isin(self.lines_connectivity[:, 4:], nodes_from_surface),
                        axis=1,
                    )
                    == e_nodes_1d
                )
                self.lines_from_surface[surf_id] = [
                    int(tag) for tag in set(self.lines_connectivity[mask, 1])
                ]

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

        self.nodes_from_lines.clear()
        surface_ids = self.geometry_information.get("surfaces")

        while index < len(surface_ids):
            fixed_tag = surface_ids[index]
            nodes_fixed = self.nodes_from_surfaces[fixed_tag]

            for sweep_tag in surface_ids[index + 1 :]:
                nodes_sweep = self.nodes_from_surfaces[sweep_tag]
                intersect_nodes = np.intersect1d(nodes_fixed, nodes_sweep)
                if intersect_nodes.size <= 1:
                    continue

                check_overlap_1 = False
                check_overlap_2 = False

                line_nodes = list(set(intersect_nodes))
                for _line_nodes in self.separate_nodes_from_disconnected_lines(
                    line_nodes
                ).values():
                    _line_nodes.sort()
                    if _line_nodes in self.nodes_from_lines.values():
                        continue

                    for _line_id, nodes_from_line in self.nodes_from_lines.items():
                        check_overlap_1 = np.isin(nodes_from_line, _line_nodes).all()
                        if check_overlap_1:
                            break

                        check_overlap_2 = np.isin(_line_nodes, nodes_from_line).all()
                        if check_overlap_2:
                            break

                    if check_overlap_1:
                        continue

                    if check_overlap_2:
                        self.nodes_from_lines[_line_id] = _line_nodes
                        continue

                    line_id += 1
                    self.nodes_from_lines[line_id] = _line_nodes

            index += 1

        self.lines_from_surface.clear()
        for line_id, line_nodes in self.nodes_from_lines.items():
            self.length_from_lines[line_id] = 0.0
            for surf_id, surface_nodes in self.nodes_from_surfaces.items():
                if np.isin(line_nodes, surface_nodes).all():
                    self.lines_from_surface[surf_id].append(line_id)

        # for _id in [17, 18, 19, 20, 22, 23, 24, 25]:
        #     lines = self.lines_from_surface.get(_id)
        #     print(f"Surface: {_id} -> {lines}")

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
        # get the 2D element connectivities that contains two node_ids inside
        filt_rows = (
            np.sum(np.isin(self.faces_connectivity[:, 4:], node_ids), axis=1) == 2
        )
        filt_connectivities = deepcopy(
            [list(nodes) for nodes in self.faces_connectivity[filt_rows, 4:]]
        )

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
        if connect_data.shape[1] in [3, 4]:
            n_nodes = 2
            e_type = 2

        elif connect_data.shape[1] in [6, 8]:
            n_nodes = 3
            e_type = 3

        last_index = 0
        first_index = 0
        self.lines_connectivity = np.empty((0, 4 + n_nodes), dtype=int)

        for line_id, node_ids in self.nodes_from_lines.items():
            connectivity_from_line = list()
            filt_rows = np.sum(np.isin(connect_data, node_ids), axis=1) == n_nodes

            for _connect in connect_data[filt_rows, :]:
                edge_connect = [node_id for node_id in _connect if node_id in node_ids]
                edge_connect.sort()
                if edge_connect in connectivity_from_line:
                    continue

                connectivity_from_line.append(edge_connect)

            if not connectivity_from_line:
                continue

            connectivity_array = np.array(connectivity_from_line, dtype=int)
            self.connectivity_from_lines[line_id] = connectivity_array

            rows = connectivity_array.shape[0]
            aux_ones = np.ones(rows, dtype=int)

            last_index += rows
            indexes = np.arange(first_index, last_index, dtype=int)

            connectivity = np.zeros((rows, 4 + n_nodes), dtype=int)
            connectivity[:, 0] = indexes
            connectivity[:, 1] = aux_ones * line_id
            connectivity[:, 2] = aux_ones * e_type
            connectivity[:, 3] = aux_ones * n_nodes
            connectivity[:, 4:] = connectivity_array

            self.lines_connectivity = np.append(
                self.lines_connectivity, connectivity, axis=0
            )
            first_index = last_index

        if self.nodes_from_lines:
            self.map_elements_from_lines()
            self.geometry_information["lines"] = list(self.nodes_from_lines.keys())
            # np.savetxt("lines_connectivity.dat", self.lines_connectivity, delimiter=",", fmt="%i")

    def process_points_from_mesh_data(self):
        """
        This method processes the corner nodes and the
        points based on lines_connectivity attribute.

        """

        if not self.lines_connectivity.size:
            return

        def get_non_repeated_values(values: list):
            """
            This function returns the non-repeated values
            from a given input list of values.

            Parameters
            ----------
            values: list
                The input list of values to be processed.

            Returns
            -------
            non_repeated_values: list
                The output list of non-repeated values.

            """
            non_repeated_nodes = set()
            repeated_nodes = set()

            for value in values:
                if value in non_repeated_nodes:
                    repeated_nodes.add(value)
                    non_repeated_nodes.remove(value)
                else:
                    non_repeated_nodes.add(value)

            return list(non_repeated_nodes)

        point_id = 0
        self.points_from_line.clear()
        for line_id, line_connect in self.connectivity_from_lines.items():
            points_from_line = list()
            corner_nodes = get_non_repeated_values(line_connect.flatten())

            for _node_id in corner_nodes:
                node_id = int(_node_id)
                if node_id in self.points_from_nodes.keys():
                    point_from_node = self.points_from_nodes.get(node_id)
                    points_from_line.append(point_from_node)
                    continue

                point_id += 1
                points_from_line.append(point_id)
                self.nodes_from_points[point_id] = node_id
                self.points_from_nodes[node_id] = point_id

            self.points_from_line[line_id] = points_from_line

        self.geometry_information["points"] = list(self.nodes_from_points.keys())

    def import_nodes_coordinates(self, filename):
        header = (
            "Node index || Coordinate x [m] || Coordinate y [m] || Coordinate z [m]"
        )
        return np.loadtxt(
            filename,
            delimiter=";",
            header=header,
            fmt=["%i", "%.16f", "%.16f", "%.16f"],
        )

    def import_faces_connectivity(self, filename):
        header = (
            "Index || Element ID || Face ID || Element type ID || Connected Node IDs"
        )
        return np.loadtxt(filename, delimiter=";", header=header, fmt="%i")

    def import_solids_connectivity(self, filename):
        header = (
            "Index || Solid ID || Element type ID || Element ID || Connected Node IDs"
        )
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

    def import_external_solids_connectivity(
        self, connectivity: dict, index_zero: bool = True, etype_tag: float = 1
    ):
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

        for key, values in nodes_from_volume.items():
            self.nodes_from_volumes[key] = np.array([*set(values)], dtype=int)

    def import_external_faces_connectivity(
        self, connectivity: dict, index_zero: bool = True, etype_tag: float = 1
    ):
        """ """
        self.elements_from_surface.clear()

        aux_list = list()
        for key, connect_data in connectivity.items():
            self.elements_from_surface[key[0]] = connect_data[:, 0] - 1
            for nodes in connect_data:
                aux_list.append(nodes)

        data = np.array(aux_list, dtype=int)
        rows, cols = data.shape

        aux_dict = defaultdict(list)
        for _, surface_id, _, *nodes in data:
            aux_dict[surface_id].extend(list(nodes))

        self.nodes_from_surfaces.clear()
        for surface_id, nodes in aux_dict.items():
            ordered_nodes = np.array([*set(nodes)], dtype=int)
            if index_zero:
                ordered_nodes -= 1
            self.nodes_from_surfaces[surface_id] = ordered_nodes

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
        for elem_id, vol_id, _, _, *node_ids in self.faces_connectivity:
            nodes_from_surface[vol_id].extend(node_ids)

        for key, values in nodes_from_surface.items():
            self.nodes_from_surfaces[key] = np.array([*set(values)], dtype=int)

    def export_nodal_coordinates(self, filename):
        fmt = ["%i", "%.16f", "%.16f", "%.16f"]
        header = (
            "Node index || Coordinate x [m] || Coordinate y [m] || Coordinate z [m]"
        )
        np.savetxt(
            filename, self.nodal_coordinates, delimiter=",", header=header, fmt=fmt
        )

    def export_line_elements_connectivity(self, filename):
        header = (
            "Index || Element ID || Line ID || Element type ID || Connected Node IDs"
        )
        np.savetxt(
            filename, self.lines_connectivity, delimiter=",", header=header, fmt="%i"
        )

    def export_face_elements_connectivity(self, filename):
        header = (
            "Index || Element ID || Face ID || Element type ID || Connected Node IDs"
        )
        np.savetxt(
            filename, self.faces_connectivity, delimiter=",", header=header, fmt="%i"
        )

    def export_solid_elements_connectivity(self, filename):
        header = (
            "Index || Solid ID || Element type ID || Element ID || Connected Node IDs"
        )
        np.savetxt(
            filename, self.solids_connectivity, delimiter=",", header=header, fmt="%i"
        )

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

    def local_mesh_refine(self, global_size: float | int, refinement_parameters: list):
        fields_list = [1]
        gmsh.model.mesh.field.add("Constant")
        gmsh.model.mesh.field.setNumbers(1, "SurfacesList", [])
        gmsh.model.mesh.field.setNumbers(1, "VolumesList", [])
        gmsh.model.mesh.field.setNumber(1, "VOut", global_size)

        for selection_type, local_size, selection_ids in refinement_parameters:
            threshold_type = gmsh.model.mesh.field.add("Constant")
            if selection_type == "surfaces":
                gmsh.model.mesh.field.setNumbers(
                    threshold_type, "SurfacesList", selection_ids
                )
            else:
                gmsh.model.mesh.field.setNumbers(
                    threshold_type, "VolumesList", selection_ids
                )

            gmsh.model.mesh.field.setNumber(threshold_type, "VIn", local_size)
            fields_list.append(threshold_type)

        minimum_field = gmsh.model.mesh.field.add("Min")
        gmsh.model.mesh.field.setNumbers(minimum_field, "FieldsList", fields_list)
        gmsh.model.mesh.field.setAsBackgroundMesh(minimum_field)

    def _configure_mesh(
        self,
        element_type: ElementType,
        minimum_element_size: float,
        maximum_element_size: float,
        size_factor: float,
        refinement_parameters=list(),
    ):
        if refinement_parameters:
            self.local_mesh_refine(maximum_element_size, refinement_parameters)

        else:
            gmsh.option.setNumber("Mesh.MeshSizeMin", minimum_element_size)
            gmsh.option.setNumber("Mesh.MeshSizeMax", maximum_element_size)

        gmsh.option.setNumber("Mesh.RandomSeed", 1234)
        gmsh.option.setNumber("Mesh.MeshSizeFactor", size_factor)
        gmsh.option.setNumber("Mesh.Algorithm", element_type.algorithm_2d)
        gmsh.option.setNumber("Mesh.Algorithm3D", element_type.algorithm_3d)
        gmsh.option.setNumber(
            "Mesh.RecombinationAlgorithm", element_type.recombination_algorithm
        )
        gmsh.option.setNumber(
            "Mesh.SubdivisionAlgorithm", element_type.subdivision_algorithm
        )
        gmsh.option.setNumber("Mesh.RecombineAll", element_type.recombine_all)
        gmsh.option.setNumber("Mesh.ElementOrder", element_type.element_order)
        gmsh.option.setNumber(
            "Mesh.SecondOrderIncomplete", element_type.second_order_incomplete
        )

    def clear_mesh_data(self):
        self.nodal_coordinates = np.zeros((0, 4), dtype=float)
        self.lines_connectivity = np.zeros((0, 4), dtype=int)
        self.faces_connectivity = np.zeros((0, 4), dtype=int)
        self.solids_connectivity = np.zeros((0, 4), dtype=int)

        self.nodes_from_points.clear()
        self.points_from_nodes.clear()
        self.nodes_from_lines.clear()
        self.nodes_from_surfaces.clear()
        self.nodes_from_volumes.clear()
        self.surfaces_from_node.clear()

        self.map_solid_elements.clear()
        self.map_face_elements.clear()
        self.map_line_elements.clear()

        self.solid_elements_center.clear()
        self.connectivity_from_lines.clear()
        self.connectivity_from_surfaces.clear()

        self.curvatures_surface.clear()
        self.normals_surface.clear()

        # cache mesh attributes for degrees of freedom decoupling

        self.cache_nodal_coordinates = None
        self.cache_lines_connectivity = None
        self.cache_faces_connectivity = None
        self.cache_solids_connectivity = None

        self.cache_connectivity_from_lines.clear()
        self.cache_connectivity_from_surfaces.clear()
        self.decoupled_points.clear()

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
        self.curvatures_surface[tag] = curvatures_surface[sorted_indexes]

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
        self.nodal_coordinates[indexes - 1, 1:] = (
            coords.reshape(-1, 3) * unit_length_factor
        )
        self.nodal_coordinates[indexes - 1, :1] = indexes.reshape(-1, 1) - 1

        connectivity_dim1 = dict()
        connectivity_dim2 = dict()
        connectivity_dim3 = dict()

        for dim, tag in gmsh.model.getEntities():
            elements_data = dict()
            element_types, element_indexes, element_nodes = gmsh.model.mesh.getElements(
                dim, tag
            )

            if not element_indexes:
                continue

            if dim == 2:
                if self.geometry_imported:
                    self.process_surface_normals_and_curvatures(tag)

            for i, element_type in enumerate(element_types):
                _, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(
                    element_type
                )

                array_element_nodes = np.array(element_nodes[i]).reshape(
                    -1, nodes_per_element
                )
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
                self.nodes_from_lines[tag] = (
                    np.array([*set(element_nodes[0])], dtype=int) - 1
                )

            elif dim == 2:  # Surfaces
                connectivity_dim2[dim, tag] = elements_data
                surface_nodes = np.array([*set(element_nodes[0])], dtype=int) - 1
                self.nodes_from_surfaces[tag] = surface_nodes
                self._update_surfaces_from_nodes(tag, surface_nodes)
                del surface_nodes

            elif dim == 3:  # Solids
                connectivity_dim3[dim, tag] = elements_data
                self.nodes_from_volumes[tag] = (
                    np.array([*set(element_nodes[0])], dtype=int) - 1
                )

        logging.info("Post-processing mesh... [80/100]")

        self.lines_connectivity, self.map_line_elements = self._get_connectivity_array(
            connectivity_dim1
        )
        self.faces_connectivity, self.map_face_elements = self._get_connectivity_array(
            connectivity_dim2
        )
        self.solids_connectivity, self.map_solid_elements = (
            self._get_connectivity_array(connectivity_dim3)
        )

        self.process_mesh_related_mappings()
        self.collapsed_solids, self.collapsed_faces, self.collapsed_lines = (
            self.get_collapsed_elements()
        )

    def cache_mesh_information(self):
        self.cache_nodal_coordinates = deepcopy(self.nodal_coordinates)

        self.cache_surfaces_from_volume = deepcopy(self.surfaces_from_volume)
        self.cache_lines_from_surface = deepcopy(self.lines_from_surface)
        self.cache_points_from_line = deepcopy(self.points_from_line)

        self.cache_lines_connectivity = deepcopy(self.lines_connectivity)
        self.cache_faces_connectivity = deepcopy(self.faces_connectivity)
        self.cache_solids_connectivity = deepcopy(self.solids_connectivity)

        self.process_connectivities_from_lines_and_surfaces(from_cache=True)

    def process_connectivities_from_lines_and_surfaces(self, from_cache: bool = False):
        """This method processes the connectivities from lines
        and surfaces, gathering the information in dictionaries
        with entity tags as keys.
        """

        for dim in [1, 2, 3]:
            if dim == 1:
                if from_cache:
                    if self.cache_lines_connectivity is None:
                        return
                    connect_data = self.cache_lines_connectivity
                else:
                    connect_data = self.lines_connectivity

            elif dim == 2:
                if from_cache:
                    connect_data = self.cache_faces_connectivity
                else:
                    connect_data = self.faces_connectivity

            elif dim == 3:
                if from_cache:
                    connect_data = self.cache_solids_connectivity
                else:
                    connect_data = self.solids_connectivity

            if not connect_data.size:
                continue

            tags = [int(entity_tag) for entity_tag in set(connect_data[:, 1])]

            for tag in tags:
                tag = int(tag)
                rows = connect_data[:, 1] == tag
                connectivity = connect_data[rows, 4:]
                nodes = np.array([*set(connectivity.flatten())], dtype=int)

                if dim == 1:
                    if from_cache:
                        self.cache_connectivity_from_lines[tag] = connectivity
                    else:
                        self.nodes_from_lines[tag] = nodes
                        self.connectivity_from_lines[tag] = connectivity

                elif dim == 2:
                    if from_cache:
                        self.cache_connectivity_from_surfaces[tag] = connectivity
                    else:
                        self.nodes_from_surfaces[tag] = nodes
                        self.connectivity_from_surfaces[tag] = connectivity

                elif dim == 3:
                    if from_cache:
                        pass
                    else:
                        self.nodes_from_volumes[tag] = nodes

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

        self.process_mesh_related_mappings()

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

    def _update_surfaces_from_nodes(self, surface_id, node_ids):
        for node_id in node_ids:
            self.surfaces_from_node[node_id].append(surface_id)

    def process_solid_elements_from_surfaces(self):
        self.surface_from_solid_element.clear()
        surface_nodes = np.array([*set(self.faces_connectivity[:, 4:])], dtype=int)
        for surface_id, surface_nodes in self.nodes_from_surfaces.items():
            mask_0 = (
                np.sum(np.isin(self.solids_connectivity[:, 4:], surface_nodes), axis=1)
                >= 1
            )
            for el_index in self.solids_connectivity[mask_0, 0]:
                self.surface_from_solid_element[el_index].append(surface_id)

    def process_mesh_related_mappings(self):
        logging.info("Loading mesh... [70/100]")
        self.process_connectivities_from_lines_and_surfaces()

        logging.info("Loading mesh... [75/100]")
        self.map_elements_from_lines_surfaces_and_volumes()

        logging.info("Loading mesh... [80/100]")
        self.map_face_elements_to_solid_elements()

        logging.info("Loading mesh... [85/100]")
        self.get_principal_diagonal_structure_parallelepiped()

    def map_elements_from_lines_surfaces_and_volumes(self):
        self.map_elements_from_lines()
        self.map_elements_from_surfaces()
        self.map_elements_from_volumes()

    def get_elements_from_lines(self, line_ids: list[int]):
        element_ids = list()
        for line_id in line_ids:
            rows = np.isin(self.lines_connectivity[:, 1], line_id)
            element_ids.extend(self.lines_connectivity[rows, 0])

        return element_ids

    def map_elements_from_lines(self):
        self.elements_from_line.clear()
        self.line_from_element.clear()
        line_ids = [int(_id) for _id in set(self.lines_connectivity[:, 1])]

        for line_id in line_ids:
            rows = np.isin(self.lines_connectivity[:, 1], line_id)
            element_ids = self.lines_connectivity[rows, 0]
            self.elements_from_line[line_id] = element_ids

            for element_id in element_ids:
                self.line_from_element[element_id] = line_id

    def map_elements_from_surfaces(self):
        self.elements_from_surface.clear()
        self.surface_from_element.clear()
        surface_ids = [int(_id) for _id in set(self.faces_connectivity[:, 1])]

        for surface_id in surface_ids:
            rows = np.isin(self.faces_connectivity[:, 1], surface_id)
            element_ids = self.faces_connectivity[rows, 0]
            self.elements_from_surface[surface_id] = element_ids

            for element_id in element_ids:
                self.surface_from_element[element_id] = surface_id

    def map_elements_from_volumes(self):
        self.elements_from_volume.clear()
        self.volume_from_element.clear()
        volume_ids = [int(_id) for _id in set(self.solids_connectivity[:, 1])]

        for volume_id in volume_ids:
            rows = np.isin(self.solids_connectivity[:, 1], volume_id)
            element_ids = self.solids_connectivity[rows, 0]
            self.elements_from_volume[volume_id] = element_ids

            for element_id in element_ids:
                self.volume_from_element[element_id] = volume_id

    def _process_face_elements_connected_to_nodes(self, selected_ids: int | list):
        self.nodes_from_face_element.clear()
        self.face_elements_connected_to_nodes.clear()
        self.surface_area_from_element_integration.clear()

        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        for tag in selected_ids:
            connect_data = self.connectivity_from_surfaces[tag]

            # integrate the total surface area by the summation of element areas
            area = 0.0
            for element_nodes in connect_data:
                area += self.process_triangular_area_by_nodal_coordinates(element_nodes)

            self.surface_area_from_element_integration[tag] = area
            face_nodes = np.array([*set(connect_data.flatten())], dtype=int)

            for node in face_nodes:
                mask = np.sum(np.isin(connect_data, node), axis=1) == 1
                self.face_elements_connected_to_nodes[node].extend(
                    connect_data[mask, :]
                )

        # import json
        # with open("areas_data.json", "r") as file:
        #     areas_data = json.load(file)

    def process_solid_elements_connected_to_nodes(self):
        # t0 = time()

        self.nodes_from_solid_element.clear()
        for el, connected_nodes in enumerate(self.solids_connectivity[:, 4:]):
            self.nodes_from_solid_element[el] = connected_nodes

        # dt = time() - t0
        # print(f"Elapsed '_process_solid_elements_connected_to_nodes': {dt} s")

    def map_face_elements_to_solid_elements_reference(self):
        self.face_to_solid_element = dict()
        self.solid_to_face_elements = defaultdict(list)

        if len(self.solids_connectivity) == 0:
            return

        nodes_per_face_element = len(self.faces_connectivity[0, 4:])
        node_ids = np.array([*set(self.faces_connectivity[:, 4:].flatten())], dtype=int)

        mask_0 = (
            np.sum(np.isin(self.solids_connectivity[:, 4:], node_ids), axis=1)
            >= nodes_per_face_element
        )
        filtered_data = self.solids_connectivity[mask_0, :]

        self.nodes_to_highlight.clear()
        self.efaces_to_highlight.clear()

        for e2d_id, surf_id, _, _, *face_nodes in self.faces_connectivity:
            mask_1 = (
                np.sum(np.isin(filtered_data[:, 4:], face_nodes), axis=1)
                == nodes_per_face_element
            )

            if np.sum(mask_1) == 0:
                # TODO: remove these attributes when we are sure that no more errors
                # occur after processing the degrees of freedom decoupling.
                # The problematic nodes and face elements are highlighted after closing the section plane UI.
                self.nodes_to_highlight.append(face_nodes)
                self.efaces_to_highlight.append(e2d_id)
                print(surf_id, e2d_id, face_nodes)
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
        external_solids = self.solids_connectivity[
            face_nodes_per_solid >= nodes_per_face
        ]

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
        mask = self._repeated_mask(self.solids_connectivity[:, 4:])
        collapsed_solids = self.solids_connectivity[mask]
        solids_set = set(collapsed_solids[:, 0].tolist()) if collapsed_solids.size else set()

        mask = self._repeated_mask(self.faces_connectivity[:, 4:])
        collapsed_faces = self.faces_connectivity[mask]
        faces_set = set(collapsed_faces[:, 0].tolist()) if collapsed_faces.size else set()

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

    def get_face_elements_connected_to_nodes(
        self, node_ids: list[int] | np.ndarray, surface_id: int | None = None
    ) -> dict:
        """
        This method computes the face elements connected to the nodes.

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
            mask_0 = (
                np.sum(np.isin(self.faces_connectivity[:, 4:], node_ids), axis=1) >= 1
            )
            filtered_data = self.faces_connectivity[mask_0, :]

        progress = 0
        nodes_number = len(node_ids)
        face_elements_connected_to_nodes = dict()

        for i, node_id in enumerate(node_ids):
            if surface_id is None:
                mask = np.sum(filtered_data[:, 4:] == node_id, axis=1) == 1
                face_elements_connected_to_nodes[node_id, surface_id] = filtered_data[
                    :, 0
                ][mask]

            else:
                connect_from_surface = self.connectivity_from_surfaces[surface_id]
                mask = np.sum(connect_from_surface == node_id, axis=1) == 1
                face_elements_connected_to_nodes[node_id, surface_id] = (
                    connect_from_surface[mask, :]
                )

            current_progress = int(100 * i / nodes_number)
            if current_progress % 5 and progress != current_progress:
                progress = current_progress
                logging.info(
                    f"Obtaining face elements connected to nodes... [{progress}/100]\nSurface [{surface_id}]"
                )

        # dt = time() - t0
        # print(f"Loop time: {dt} s")

        return face_elements_connected_to_nodes

    def get_solid_elements_connected_to_nodes(self, **kwargs) -> dict:
        """
        This method processes the solid elements connected to the nodes.
        It returns a dictionary mapping the node IDs to the solid element IDs.
        """

        # t0 = time()

        surface_id = kwargs.get("surface_id")
        if isinstance(surface_id, int):
            node_ids = self.nodes_from_surfaces.get(surface_id)
        else:
            node_ids = kwargs.get("node_ids")

        mask_0 = np.sum(np.isin(self.solids_connectivity[:, 4:], node_ids), axis=1) >= 1
        filtered_data = self.solids_connectivity[mask_0, :]

        elem_ids = filtered_data[:, 0]
        connect_nodes = filtered_data[:, 4:]

        progress = 0
        number_nodes = len(node_ids)
        solid_elements_connected_to_nodes = dict()

        for i, node_id in enumerate(node_ids):
            mask = np.sum(connect_nodes == node_id, axis=1) == 1
            solid_elements_connected_to_nodes[node_id] = elem_ids[mask]

            current_progress = int(100 * i / number_nodes)
            if current_progress % 5 and progress != current_progress:
                progress = current_progress
                logging.info(
                    f"Obtaining solid elements connected to nodes... [{int(100 * i / number_nodes)}/100]"
                )

        # dt = time() - t0
        # print(f"Loop time: {dt} s")

        return solid_elements_connected_to_nodes

    def get_average_normals_for_surface_nodes_reference(self, surface_id: int) -> dict:
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

        nodes_from_surface = self.nodes_from_surfaces.get(surface_id)
        if nodes_from_surface is None:
            return dict()

        nodes_from_surface = np.sort(nodes_from_surface)
        face_elements_connected_to_nodes = self.get_face_elements_connected_to_nodes(
            nodes_from_surface, surface_id
        )

        data_normals = dict()
        for node_id in nodes_from_surface:
            face_elem_connect = face_elements_connected_to_nodes[node_id, surface_id]

            n = 0.0
            for face_connect in face_elem_connect:
                n += self.get_element_face_normal(face_connect)

            data_normals[node_id] = n / len(face_elem_connect)

        return data_normals

    def get_average_normals_for_surface_nodes(self, surface_id: int, **kwargs):
        """
        This method processes the average normals in the surface nodes considering the element faces
        normals connected to same node.

        Parameters
        ----------
        surface_id: int
            The tag of surface in which the normals average will be computed.

        Returns
        -------
        avg_node_normals: dict
            A dictionary mapping the node IDs to the average normal vector.
        """

        num = defaultdict(float)
        den = defaultdict(int)

        face_connectivity = self.connectivity_from_surfaces.get(surface_id)
        eface_normals = self.get_stacked_normals_for_surface_elements(surface_id)
        nodes_from_surface = np.sort(self.nodes_from_surfaces.get(surface_id))

        for i, connect in enumerate(face_connectivity):
            e_normal = eface_normals[i, :].flatten()
            for node in connect:
                num[node] += e_normal
                den[node] += 1

        avg_node_normals = {node: num[node] / den[node] for node in nodes_from_surface}

        return avg_node_normals

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

        face_connectivity = self.connectivity_from_surfaces.get(surface_id)
        if face_connectivity is None:
            return

        X1 = self.nodal_coordinates[face_connectivity[:, 0], 1]
        Y1 = self.nodal_coordinates[face_connectivity[:, 0], 2]
        Z1 = self.nodal_coordinates[face_connectivity[:, 0], 3]

        X2 = self.nodal_coordinates[face_connectivity[:, 1], 1]
        Y2 = self.nodal_coordinates[face_connectivity[:, 1], 2]
        Z2 = self.nodal_coordinates[face_connectivity[:, 1], 3]

        X3 = self.nodal_coordinates[face_connectivity[:, 2], 1]
        Y3 = self.nodal_coordinates[face_connectivity[:, 2], 2]
        Z3 = self.nodal_coordinates[face_connectivity[:, 2], 3]

        P2P1 = np.array([X2 - X1, Y2 - Y1, Z2 - Z1]).T
        P3P1 = np.array([X3 - X1, Y3 - Y1, Z3 - Z1]).T

        cross = np.cross(P2P1, P3P1, axis=1)
        norm_cross = np.linalg.norm(cross, axis=1)

        norm_cross = norm_cross.reshape(-1, 1, 1)
        cross = cross.reshape(-1, 1, 3)

        stacked_normals = cross / norm_cross

        return stacked_normals

    def compute_nodal_areas(self):
        self.nodal_area.clear()
        for node, connectivities in self.face_elements_connected_to_nodes.items():
            for connect in connectivities:
                area = self.process_triangular_area_by_nodal_coordinates(connect)
                if area is not None:
                    self.nodal_area[node].append(area)

    def process_triangular_area_by_nodal_coordinates(
        self, node_ids: list[int] | np.ndarray
    ) -> np.ndarray | None:
        """ """
        if len(node_ids) != 3:
            return None

        coord_A = self.nodal_coordinates[node_ids[0], 1:]
        coord_B = self.nodal_coordinates[node_ids[1], 1:]
        coord_C = self.nodal_coordinates[node_ids[2], 1:]

        AB = coord_B - coord_A
        BC = coord_C - coord_B
        area = np.linalg.norm(np.cross(AB, BC)) / 2

        return area

    def set_face_element_thickness(self, surface_id: int, data: dict):
        for face_element in self.elements_from_surface[surface_id]:
            self.face_element_thickness[face_element] = data

    def get_mesh_info(self):
        n_nodes = self.nodal_coordinates.shape[0]
        n_face_elements = self.faces_connectivity.shape[0]
        n_solid_elements = self.solids_connectivity.shape[0]
        return n_nodes, n_face_elements, n_solid_elements

    def calculate_mesh_quality_parameters(self):
        if not gmsh.model.mesh.getElements(3, -1)[1]:
            return

        parameters = [
            "gamma",
            "volume",
            "minSJ",
        ]

        elements = gmsh.model.mesh.getElements(3, -1)[1][0]

        for parameter in parameters:
            element_qualities_dict = dict()
            qualities_array = np.array(
                gmsh.model.mesh.getElementQualities(elements, parameter)
            )

            for i, element in enumerate(elements):
                element_qualities_dict[element] = qualities_array[i]

            self.mesh_quality[parameter] = element_qualities_dict

        element_qualities_dict = dict()
        min_edge_quals = np.array(
            gmsh.model.mesh.getElementQualities(elements, "minEdge")
        )
        max_edge_quals = np.array(
            gmsh.model.mesh.getElementQualities(elements, "maxEdge")
        )
        aspect_ratio_quals = max_edge_quals / min_edge_quals

        for i, element in enumerate(elements):
            element_qualities_dict[element] = aspect_ratio_quals[i]

        self.mesh_quality["aspectRatio"] = element_qualities_dict

    def calculate_mesh_quality_statistics(self):
        if not self.mesh_quality:
            return

        for parameter in ["gamma", "volume", "minSJ", "aspectRatio"]:
            qualities_array = list(self.mesh_quality[parameter].values())

            if parameter == "aspectRatio":
                worst_value = np.amax(qualities_array)
            else:
                worst_value = np.amin(qualities_array)

            statistics = [
                worst_value,
                np.mean(qualities_array),
                np.std(qualities_array),
            ]

            self.mesh_quality_statistics[parameter] = statistics

    def calculate_mesh_bad_elements(self):
        if not self.mesh_quality:
            return

        bad_elements = []
        for parameter in self.mesh_quality_parameters:
            for element in self.mesh_quality[parameter].keys():
                quality = self.mesh_quality[parameter][element]

                if parameter == "aspectRatio":
                    if quality > self.quality_bins[parameter][0]:
                        bad_elements.append(element)
                elif quality < self.quality_bins[parameter][1]:
                    bad_elements.append(element)

            bad_elements_vibra = [
                int(self.map_solid_elements[gmsh_tags]) for gmsh_tags in bad_elements
            ]
            self.mesh_bad_elements[parameter] = bad_elements_vibra

    def calculate_mesh_quality_histograms(self):
        if not self.mesh_quality:
            return

        for parameter in self.mesh_quality_parameters:
            mesh_quality_vals = list(self.mesh_quality[parameter].values())

            bins = np.linspace(min(mesh_quality_vals), max(mesh_quality_vals), 30)
            hist, bin_edges = np.histogram(mesh_quality_vals, bins=bins)

            percentile_5 = np.percentile(mesh_quality_vals, 5)
            percentile_95 = np.percentile(mesh_quality_vals, 95)

            self.mesh_quality_histograms_data[parameter] = [
                hist,
                bin_edges,
                percentile_5,
                percentile_95,
            ]

    def compute_initial_mesh_size(
        self, path, geometry_tolerance: float = 1e-10, threads: int = 0
    ):
        gmsh.initialize("", False, interruptible=False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", threads)
        gmsh.option.setNumber("Geometry.Tolerance", geometry_tolerance)

        gmsh.open(path)

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
            gmsh.finalize()

    def compute_bounding_box_sizes(self, geo_entities):
        xmin = ymin = zmin = xmax = ymax = zmax = 0
        volume = 0
        for dim, tag in geo_entities:
            # This mass is considering a density of 1, so it is equal the solid volume
            volume += gmsh.model.occ.getMass(dim, tag)
            xmin2, ymin2, zmin2, xmax2, ymax2, zmax2 = gmsh.model.getBoundingBox(
                dim, tag
            )
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

            elif dim == 1:
                self.length_from_lines[tag] = value * (unit_factor**1)

    def process_downwards_adjacencies_from_entities(self):
        """This method processes the downwards adjacencies
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
        """This method processes the upwards adjacencies
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

    def _get_connectivity_array(self, input_dict):
        """
        The returned value is an array where each line is a connectivity
        and the collums follow this order:

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
        This method computes the element average center coordinates of the selected element ID.

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
            nodes = self.nodes_from_solid_element[element_id]
            solid_elements_center[element_id] = np.average(
                self.nodal_coordinates[nodes, 1:], axis=0
            )

        return solid_elements_center

    def get_average_nodal_coordinates(self, surface_ids: list[int], averaged=False):
        nodal_coordinates = self.nodal_coordinates

        rows = list()
        for surface_id in surface_ids:
            if averaged:
                for row in self.nodes_from_surfaces[surface_id]:
                    rows.append(row)
            else:
                _nodes = list(self.nodes_from_surfaces[surface_id])
                rows.append(_nodes)

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

    def get_element_face_normal(self, connect: np.ndarray):
        # ie = self.faces_connectivity[element_id, 4:]
        coords = self.nodal_coordinates[connect, 1:]

        P1 = coords[0, :]
        P2 = coords[1, :]
        P3 = coords[2, :]

        P2P1 = np.array(P2 - P1)
        P3P1 = np.array(P3 - P1)

        cross = np.cross(P2P1, P3P1)
        norm_cross = np.linalg.norm(cross)

        if norm_cross == 0:
            return 0.0

        normal = cross / np.linalg.norm(cross)

        return normal

    def set_nodal_normals_data(self, normals_data: dict):
        for node_id, nodal_normal in normals_data.items():
            self.nodal_normals_data[node_id] = nodal_normal

    def get_principal_diagonal_structure_parallelepiped(self):
        """
        This method updates the principal structure diagonal parallelepiped attribute.

        """
        nodal_coordinates = self.nodal_coordinates.copy()
        x_min, y_min, z_min = np.min(nodal_coordinates[:, 1:], axis=0)
        x_max, y_max, z_max = np.max(nodal_coordinates[:, 1:], axis=0)
        self.principal_diagonal = np.sqrt(
            (x_max - x_min) ** 2 + (y_max - y_min) ** 2 + (z_max - z_min) ** 2
        )
        # print('The base length is: {}[m]'.format(round(self.principal_diagonal, 6)))

    def get_elements_and_nodes_from_sphere(
        self,
        surface_ids,
        selection_radius,
        averaged=False,
        filter_type=0,
        export_data=False,
    ):
        list_center_coords = self.get_average_nodal_coordinates(
            surface_ids, averaged=averaged
        )

        if not list_center_coords:
            return list(), list()

        selected_elements = list()
        nodes_inside_sphere = list()
        node_indexes = self.nodal_coordinates[:, 0]
        nodal_coordinates = self.nodal_coordinates[:, 1:]

        for center_coords in list_center_coords:
            if (
                filter_type == 0
            ):  # filters the elements inside sphere based on elements coordinates center
                filter_radius = 1.1 * selection_radius
                _, filtered_elements = (
                    self.get_nodes_inside_sphere_and_its_elements_connected(
                        center_coords, filter_radius
                    )
                )

                if filtered_elements:
                    filtered_solid_elements = self.process_element_average_coordinates(
                        filtered_elements
                    )
                    element_indexes = np.array(
                        list(filtered_solid_elements.keys()), dtype=int
                    )
                    elements_center_coordinates = np.array(
                        list(filtered_solid_elements.values()), dtype=float
                    )
                else:
                    return

                diff_nodes = np.linalg.norm(nodal_coordinates - center_coords, axis=1)
                diff_elem = np.linalg.norm(
                    elements_center_coordinates - center_coords, axis=1
                )

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
                    selection_data = self.get_solid_elements_connected_to_nodes(
                        node_ids=nodes_inside_sphere
                    )
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

    def get_nodes_inside_sphere_and_its_elements_connected(
        self, center_coords, selection_radius
    ):
        node_indexes = self.nodal_coordinates[:, 0]
        nodal_coordinates = self.nodal_coordinates[:, 1:]

        diff_nodes = np.linalg.norm(nodal_coordinates - center_coords, axis=1)
        mask_nodes = diff_nodes <= selection_radius
        nodes_inside_sphere = node_indexes[mask_nodes]

        selection_data = self.get_solid_elements_connected_to_nodes(
            node_ids=nodes_inside_sphere
        )

        _selected_elements = list()
        for _node, element_ids in selection_data.items():
            _selected_elements.extend(element_ids)

        selected_elements = np.array([*set(_selected_elements)], dtype=int)

        return nodes_inside_sphere, list(selected_elements)

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
                message = (
                    "An empty input field has been detected for the Selection ID. "
                )
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
