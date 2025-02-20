from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..render_widgets.geometry_render_widget import GeometryRenderWidget


import numpy as np
from vtkmodules.vtkRenderingCore import (
    vtkCellPicker,
    vtkCoordinate,
)

from vibra import app

from .common_selection import get_coordinates_inside_area, pick_actor_cell_info


class GeometrySelection:
    def __init__(self, geometry_render_widget: "GeometryRenderWidget"):
        self.geometry_render_widget = geometry_render_widget

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
        volume_ids, _ = self._pick_volume(x, y)

        # Cheating a bit to prioritize point selection
        point_distance *= 0.98
        closest = min(point_distance, line_distance, surface_distance)

        if closest == point_distance:
            return point_ids, set(), set(), volume_ids

        elif closest == line_distance:
            return set(), line_ids, set(), volume_ids

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
        internal_picked_nodes = self._area_pick_node_internal_indexes(x0, y0, x1, y1)

        points = self._area_pick_points(x0, y0, x1, y1)
        lines = self._pick_lines_from_indexes(internal_picked_nodes)
        surfaces = self._pick_surfaces_from_indexes(internal_picked_nodes)
        volumes = self._pick_volumes_from_indexes(internal_picked_nodes)

        return points, lines, surfaces, volumes

    def _pick_point(self, x: int, y: int) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set(), float("inf")

        renderer = self.geometry_render_widget.renderer
        cell_picker = vtkCellPicker()
        cell_picker.SetTolerance(0.0018)
        cell_picker.Pick(x, y, 0, renderer)

        pick_position = np.array(cell_picker.GetPickPosition())
        all_points = self._get_nodes_subset()  # The point id is 1-indexed
        i = np.argmin(np.linalg.norm(all_points[:, 1:] - pick_position, axis=1))

        camera_position = np.array(renderer.GetActiveCamera().GetPosition())
        camera_distance = np.linalg.norm(camera_position - pick_position)

        coordinate = vtkCoordinate()
        coordinate.SetCoordinateSystemToWorld()
        coordinate.SetValue(all_points[i, 1:])
        view_coords = coordinate.GetComputedViewportValue(renderer)
        click = np.array([x, y])

        node_size = 15
        if np.linalg.norm(click - view_coords) < node_size / 2:
            return {1 + all_points[i, 0].astype(int)}, camera_distance
        else:
            return set(), float("inf")

    def _pick_line(self, x: int, y: int) -> set[int]:
        line_id, line_distance = pick_actor_cell_info(
            x,
            y,
            self.geometry_render_widget.lines_actor,
            "line_indexes",
            self.geometry_render_widget.renderer,
        )
        if line_id >= 0:
            return {line_id}, line_distance
        else:
            return set(), line_distance

    def _pick_surface(self, x: int, y: int) -> set[int]:
        surface_id, surface_distance = pick_actor_cell_info(
            x,
            y,
            self.geometry_render_widget.faces_actor,
            "surface_indexes",
            self.geometry_render_widget.renderer,
        )
        if surface_id >= 0:
            return {surface_id}, surface_distance
        else:
            return set(), surface_distance

    def _pick_volume(self, x: int, y: int) -> set[int]:
        volume_id, volume_distance = pick_actor_cell_info(
            x,
            y,
            self.geometry_render_widget.faces_actor,
            "volume_indexes",
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

        all_points = self._get_nodes_subset()
        renderer = self.geometry_render_widget.renderer
        mask = get_coordinates_inside_area(
            all_points[:, 1:],
            (x0, y0, x1, y1),
            renderer,
        )
        return set(all_points[mask, 0].astype(int) + 1)

    def _pick_lines_from_indexes(self, internal_picked_nodes: list[int]) -> set[int]:
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

        line_indexes = mesh.lines_connectivity[:, 1].astype(int)
        all_lines = np.unique(line_indexes)
        unselected = np.unique(line_indexes[mask_unselected])
        return set(all_lines) - set(unselected)

    def _pick_surfaces_from_indexes(self, internal_picked_nodes: list[int]) -> set[int]:
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

        surface_indexes = mesh.faces_connectivity[:, 1].astype(int)
        all_surfaces = np.unique(surface_indexes)
        unselected = np.unique(surface_indexes[mask_unselected])
        return set(all_surfaces) - set(unselected)

    def _pick_volumes_from_indexes(self, internal_picked_nodes: list[int]) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        mask_selected_elements = np.any(
            np.isin(mesh.solids_connectivity[:, 4:], internal_picked_nodes),
            axis=1,
        )

        return set(mesh.solids_connectivity[mask_selected_elements, 1].astype(int))

    def _get_nodes_subset(self):
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        node_indexes = list()
        for _, (node_id,) in mesh.nodes_from_points.items():
            node_indexes.append(node_id)

        return mesh.nodal_coordinates[node_indexes]

    def _area_pick_node_internal_indexes(self, x0: int, y0: int, x1: int, y1: int) -> list[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        renderer = self.geometry_render_widget.renderer
        mask = get_coordinates_inside_area(
            mesh.nodal_coordinates[:, 1:],
            (x0, y0, x1, y1),
            renderer,
        )

        # returns the index of True values
        return np.nonzero(mask.flatten())
