from vibra.engine.mesher.geometry_info import GeometryInfo
import logging
from pathlib import Path

import gmsh
import numpy as np

from vibra.engine.mesher.gmsh_common import GmshCommon
from vibra.engine.mesher.mesh import Mesh
from vibra.utils.utils import group_by

logger = logging.getLogger(__name__)


class MeshReader(GmshCommon):
    def __init__(self, path: str | Path | None = None):
        self.path: Path | None = None
        if path is not None:
            self.set_path(path)

    def set_path(self, path: str | Path):
        self.path = Path(path).expanduser()

    def read_mesh_and_info(self) -> tuple[Mesh, GeometryInfo]:
        mesh = self.read_mesh()
        geometry_info = GeometryInfo()

        geometry_info._solids_to_surfaces = mesh.surfaces_from_volume
        geometry_info._surfaces_to_curves = mesh.lines_from_surface
        geometry_info._curves_to_points = mesh.points_from_line
        geometry_info._surfaces_to_solids = mesh.volumes_from_surface
        geometry_info._curves_to_surfaces = mesh.surfaces_from_line
        geometry_info._points_to_curves = mesh.lines_from_point

        return mesh, geometry_info

    def read_mesh(self) -> Mesh:
        gmsh.initialize("", False, interruptible=False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", 0)
        gmsh.option.setNumber("Geometry.Tolerance", 1e-8)

        logger.info("Loading mesh data... [25/100]")
        gmsh.open(str(self.path))

        logger.info("Loading mesh data... [90/100]")
        gmsh.model.occ.synchronize()

        mesh = self._create_mesh_from_gmsh_state()
        mesh.geometry_imported = False

        logger.info("Post-processing mesh... [80/100]")
        self._process_geometry_information(mesh)
        self._process_adjacencies(mesh)

        gmsh.finalize()

        logger.info(
            f"The mesh file contains {len(mesh.nodal_coordinates)} nodes"
            f", {len(mesh.lines_connectivity)} dim 1"
            f", {len(mesh.faces_connectivity)} dim 2"
            f"and {len(mesh.solids_connectivity)} dim 3 elements"
        )

        return mesh

    def _process_adjacencies(self, mesh: Mesh):
        """
        This method processes the downwards adjacencies from entities
        from the solids, faces and lines connectivities matrices.
        """

        e_nodes_2d = mesh.faces_connectivity[0, 4:].size
        for vol_id in mesh.geometry_information.get("volumes"):
            nodes_from_volume = mesh.get_nodes_from_volume(vol_id)
            if nodes_from_volume is None:
                continue

            mask = np.sum(np.isin(mesh.faces_connectivity[:, 4:], nodes_from_volume), axis=1) == e_nodes_2d
            mesh.surfaces_from_volume[vol_id] = [int(tag) for tag in set(mesh.faces_connectivity[mask, 1])]

        if mesh.lines_connectivity.size:
            e_nodes_1d = mesh.lines_connectivity[0, 4:].size
            for surf_id in mesh.geometry_information.get("surfaces"):
                nodes_from_surface = mesh.get_nodes_from_surface(surf_id)
                if nodes_from_surface is None:
                    continue

                mask = (
                    np.sum(
                        np.isin(mesh.lines_connectivity[:, 4:], nodes_from_surface),
                        axis=1,
                    )
                    == e_nodes_1d
                )
                mesh.lines_from_surface[surf_id] = [int(tag) for tag in set(mesh.lines_connectivity[mask, 1])]

        # mesh.process_lines_from_mesh_data()
        self._process_lines_from_mesh_data(mesh)
        self._process_lines_connectivitiy_from_mesh_data(mesh)
        self._process_points_from_mesh_data(mesh)
        mesh.process_upwards_adjacencies()

    def _process_lines_from_mesh_data(self, mesh: Mesh):
        """
        This method processes the nodes from lines and the lines
        from surfaces based on the surfaces connectivity.
        """

        if mesh.lines_connectivity.size:
            return

        index = 0
        line_id = 0

        mesh.external_nodes_from_lines.clear()
        surface_ids = mesh.geometry_information.get("surfaces")

        while index < len(surface_ids):
            fixed_tag = surface_ids[index]
            nodes_fixed = mesh.get_nodes_from_surface(fixed_tag)

            for sweep_tag in surface_ids[index + 1 :]:
                nodes_sweep = mesh.get_nodes_from_surface(sweep_tag)
                intersect_nodes = np.intersect1d(nodes_fixed, nodes_sweep)
                if intersect_nodes.size <= 1:
                    continue

                check_overlap_1 = False
                check_overlap_2 = False

                line_nodes = list(set(intersect_nodes))

                for _line_nodes in mesh.separate_nodes_from_disconnected_lines(line_nodes).values():
                    _line_nodes.sort()
                    if _line_nodes in mesh.external_nodes_from_lines.values():
                        continue

                    for _line_id, nodes_from_line in mesh.external_nodes_from_lines.items():
                        check_overlap_1 = np.isin(nodes_from_line, _line_nodes).all()
                        if check_overlap_1:
                            break

                        check_overlap_2 = np.isin(_line_nodes, nodes_from_line).all()
                        if check_overlap_2:
                            break

                    if check_overlap_1:
                        continue

                    if check_overlap_2:
                        mesh.external_nodes_from_lines[_line_id] = _line_nodes
                        continue

                    line_id += 1
                    mesh.external_nodes_from_lines[line_id] = _line_nodes

            index += 1

        mesh.lines_from_surface.clear()
        for line_id, line_nodes in mesh.external_nodes_from_lines.items():
            mesh.length_from_lines[line_id] = 0.0
            for surf_id in mesh.geometry_information.get("surfaces"):
                surface_nodes = mesh.get_nodes_from_surface(surf_id)
                if surface_nodes is None:
                    continue

                if np.isin(line_nodes, surface_nodes).all():
                    mesh.lines_from_surface[surf_id].append(line_id)

    def _process_lines_connectivitiy_from_mesh_data(self, mesh: Mesh):
        """
        This method processes the lines connectivity
        based on the surfaces connectivity.
        """

        if mesh.lines_connectivity.size:
            return

        connect_data = mesh.faces_connectivity[:, 4:]
        n_nodes_2d = mesh.faces_connectivity[0, 4:].size

        if n_nodes_2d in [3, 4]:
            n_nodes_1d = 2
            e_type = 2

        elif n_nodes_2d in [6, 8]:
            n_nodes_1d = 3
            e_type = 3

        last_index = 0
        first_index = 0
        mesh.lines_connectivity = np.empty((0, 4 + n_nodes_1d), dtype=int)

        for line_id, node_ids in mesh.external_nodes_from_lines.items():
            connectivity_from_line = []
            filt_rows = np.sum(np.isin(connect_data, node_ids), axis=1) == n_nodes_1d

            for _connect in connect_data[filt_rows, :]:
                edge_connect = [node_id for node_id in _connect if node_id in node_ids]
                edge_connect = mesh.reorder_connectivity_based_on_distances(edge_connect)

                if edge_connect in connectivity_from_line:
                    continue

                connectivity_from_line.append(edge_connect)

            if not connectivity_from_line:
                continue

            connectivity_array = np.array(connectivity_from_line, dtype=int)

            rows = connectivity_array.shape[0]
            aux_ones = np.ones(rows, dtype=int)

            last_index += rows
            indices = np.arange(first_index, last_index, dtype=int)

            connectivity = np.zeros((rows, 4 + n_nodes_1d), dtype=int)
            connectivity[:, 0] = indices
            connectivity[:, 1] = aux_ones * line_id
            connectivity[:, 2] = aux_ones * e_type
            connectivity[:, 3] = aux_ones * n_nodes_1d
            connectivity[:, 4:] = connectivity_array

            mesh.lines_connectivity = np.append(mesh.lines_connectivity, connectivity, axis=0)
            first_index = last_index

        if mesh.external_nodes_from_lines:
            mesh.elements_from_line = group_by(
                keys=mesh.lines_connectivity[:, Mesh.ColumnEnum.ENTITY_INDEX],
                values=mesh.lines_connectivity[:, Mesh.ColumnEnum.ELEMENT_INDEX],
            )
            mesh.geometry_information["lines"] = list(mesh.external_nodes_from_lines.keys())

    def _process_points_from_mesh_data(self, mesh: Mesh):
        """
        This method processes the corner nodes and the
        points based on lines_connectivity attribute.

        """

        if not mesh.lines_connectivity.size:
            return

        point_id = 0
        mesh.points_from_line.clear()

        for line_id in mesh.geometry_information.get("lines"):
            line_connect = mesh.get_connectivity_from_line(line_id)
            corner_nodes = self._get_non_repeated_values(line_connect)

            points_from_line = []

            for _node_id in corner_nodes:
                node_id = int(_node_id)
                if node_id in mesh.points_from_nodes:
                    points_from_nodes = mesh.points_from_nodes.get(node_id)
                    points_from_line.append(points_from_nodes)
                    continue

                point_id += 1
                points_from_line.append(point_id)
                mesh.nodes_from_points[point_id] = node_id
                mesh.points_from_nodes[node_id] = point_id

            mesh.points_from_line[line_id] = points_from_line

        mesh.geometry_information["points"] = list(mesh.nodes_from_points.keys())

    def _get_non_repeated_values(self, line_connectivities: np.ndarray):
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
        _, indices, count = np.unique(values, return_index=True, return_counts=True)
        non_repeated_values = list(values[indices[count == 1]])
        return non_repeated_values
