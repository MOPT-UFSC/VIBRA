from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..render_widgets.geometry_render_widget import GeometryRenderWidget


import numpy as np
from vtkmodules.vtkRenderingCore import (
    vtkCellPicker,
    vtkCoordinate,
)

from vibra import app
from vibra.utils.math_functions import inside_plane

from .common_selection import get_coordinates_inside_area, pick_actor_cell_info


class GeometrySelection:
    def __init__(self, geometry_render_widget: "GeometryRenderWidget"):
        self.geometry_render_widget = geometry_render_widget
        self.section_plane_config = None

    def pick(
        self, x: int, y: int
    ) -> tuple[
        set[int],
        set[int],
        set[int],
        set[int],
    ]:
        point_ids, point_distance = self._pick_point(x, y)
        line_ids, line_distance = self._pick_line(x, y)
        surface_ids, surface_distance = self._pick_surface(x, y)

        volume_ids = set()
        mesh = app().project.model.mesh
        for surface in surface_ids:
            surface_volumes = mesh.volumes_from_surface.get(surface, [])
            volume_ids.update(surface_volumes)

        # Cheating a bit to prioritize selection of points and lines
        point_distance *= 0.98
        line_distance *= 0.99
        closest = min(point_distance, line_distance, surface_distance)

        if closest == point_distance:
            return point_ids, set(), set(), set()

        elif closest == line_distance:
            return set(), line_ids, set(), set()

        elif closest == surface_distance:
            return set(), set(), surface_ids, volume_ids

        else:
            return set(), set(), set(), volume_ids

    def area_pick(
        self, x0: int, y0: int, x1: int, y1: int
    ) -> tuple[
        set[int],
        set[int],
        set[int],
        set[int],
    ]:
        internal_picked_nodes = self._area_pick_node_internal_indices(x0, y0, x1, y1)

        points = self._area_pick_points(x0, y0, x1, y1)
        lines = self._pick_lines_from_indices(internal_picked_nodes)
        surfaces = self._pick_surfaces_from_indices(internal_picked_nodes)
        volumes = self._pick_volumes_from_indices(internal_picked_nodes)

        mesh = app().project.model.mesh
        if (mesh is not None) and ((mesh.solids_connectivity is None) or (mesh.solids_connectivity.size == 0)):
            volumes = set()
            for surface in surfaces:
                vols = mesh.volumes_from_surface.get(surface, [])
                volumes.update(vols)

        return points, lines, surfaces, volumes

    def set_section_plane(self, position, rotation):
        self.section_plane_config = (position, rotation)

    def clear_section_plane(self):
        self.section_plane_config = None

    def _pick_point(self, x: int, y: int) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set(), float("inf")

        renderer = self.geometry_render_widget.renderer
        cell_picker = vtkCellPicker()
        cell_picker.SetTolerance(0.0018)
        cell_picker.Pick(x, y, 0, renderer)

        pick_position = np.array(cell_picker.GetPickPosition())
        points_coords = self._get_points_coords()  # The point id is 1-indexed
        plane_mask = self._section_plane_mask(points_coords[:, 1:])
        points_coords = points_coords[plane_mask]

        if points_coords.size == 0:
            return set(), float("inf")

        i = np.argmin(np.linalg.norm(points_coords[:, 1:] - pick_position, axis=1))
        camera_position = np.array(renderer.GetActiveCamera().GetPosition())
        camera_distance = np.linalg.norm(camera_position - pick_position)

        coordinate = vtkCoordinate()
        coordinate.SetCoordinateSystemToWorld()
        coordinate.SetValue(points_coords[i, 1:])
        view_coords = coordinate.GetComputedViewportValue(renderer)
        click = np.array([x, y])

        node_size = 15
        if np.linalg.norm(click - view_coords) < node_size / 2:
            equivalent_node_index = points_coords[i, 0].astype(int)
            return {mesh.points_from_nodes[equivalent_node_index]}, camera_distance
        else:
            return set(), float("inf")

    def _pick_line(self, x: int, y: int) -> set[int]:
        line_id, line_distance = pick_actor_cell_info(
            x,
            y,
            self.geometry_render_widget.lines_actor,
            "line_indices",
            self.geometry_render_widget.renderer,
        )
        if line_id >= 0:
            return {line_id}, line_distance
        else:
            return set(), line_distance

    def _pick_surface(self, x: int, y: int) -> set[int]:
        # A actor can not be picked if it is not visible, so we make it
        # visible and then revert it back to the previous state
        default_actor = self.geometry_render_widget.multimaterial.default_actor

        visibility = default_actor.GetVisibility()
        default_actor.SetVisibility(True)
        surface_id, surface_distance = pick_actor_cell_info(
            x,
            y,
            self.geometry_render_widget.multimaterial,
            "surface_indices",
            self.geometry_render_widget.renderer,
        )
        default_actor.SetVisibility(visibility)

        if surface_id >= 0:
            return {surface_id}, surface_distance
        else:
            return set(), surface_distance

    def _pick_volume(self, x: int, y: int) -> set[int]:
        volume_id, volume_distance = pick_actor_cell_info(
            x,
            y,
            self.geometry_render_widget.multimaterial,
            "volume_indices",
            self.geometry_render_widget.renderer,
        )
        if volume_id >= 0:
            return {volume_id}, volume_distance
        else:
            return set(), volume_distance

    def _area_pick_points(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
    ) -> set[int]:

        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        renderer = self.geometry_render_widget.renderer
        points_coords = self._get_points_coords()
        plane_mask = self._section_plane_mask(points_coords[:, 1:])

        mask = get_coordinates_inside_area(
            points_coords[:, 1:],
            (x0, y0, x1, y1),
            renderer,
        )

        equivalent_node_indices = points_coords[mask & plane_mask, 0].astype(int)
        return {mesh.points_from_nodes[i] for i in equivalent_node_indices}

    def _pick_lines_from_indices(self, internal_picked_nodes: list[int]) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        mask_unselected = np.any(
            np.isin(
                mesh.lines_connectivity[:, 4:],
                internal_picked_nodes,
                invert=True,
            ),
            axis=1,
        )

        line_indices = mesh.lines_connectivity[:, 1].astype(int)
        all_lines = np.unique(line_indices)
        unselected = np.unique(line_indices[mask_unselected])
        return set(all_lines) - set(unselected)

    def _pick_surfaces_from_indices(self, internal_picked_nodes: list[int]) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        mask_unselected = np.any(
            np.isin(
                mesh.faces_connectivity[:, 4:],
                internal_picked_nodes,
                invert=True,
            ),
            axis=1,
        )

        surface_indices = mesh.faces_connectivity[:, 1].astype(int)
        all_surfaces = np.unique(surface_indices)
        unselected = np.unique(surface_indices[mask_unselected])
        return set(all_surfaces) - set(unselected)

    def _pick_volumes_from_indices(self, internal_picked_nodes: list[int]) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        mask_selected_elements = np.any(
            np.isin(mesh.solids_connectivity[:, 4:], internal_picked_nodes),
            axis=1,
        )

        return set(mesh.solids_connectivity[mask_selected_elements, 1].astype(int))

    def _get_points_coords(self):
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        node_indices = list()
        for _, node_id in mesh.nodes_from_points.items():
            node_indices.append(node_id)

        return mesh.nodal_coordinates[node_indices]

    def _area_pick_node_internal_indices(self, x0: int, y0: int, x1: int, y1: int) -> list[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        renderer = self.geometry_render_widget.renderer
        plane_mask = self._section_plane_mask(mesh.nodal_coordinates[:, 1:])
        mask = plane_mask & get_coordinates_inside_area(
            mesh.nodal_coordinates[:, 1:],
            (x0, y0, x1, y1),
            renderer,
        )

        # returns the index of True values
        return np.nonzero(mask.flatten())

    def _section_plane_mask(self, coordinates: np.ndarray):
        if self.section_plane_config is None:
            return np.ones(coordinates.shape[0], dtype=bool)

        position, rotation = self.section_plane_config
        plane_mask = inside_plane(coordinates, position, rotation)
        return plane_mask
