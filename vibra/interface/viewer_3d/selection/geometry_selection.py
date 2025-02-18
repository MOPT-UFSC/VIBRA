from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..render_widgets.geometry_render_widget import GeometryRenderWidget


import numpy as np
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkCoordinate,
)

from vibra import app
from vibra.utils.interface_utils import screen_to_world_coords
from vibra.utils.math_functions import points_in_between

from .common_selection import pick_actor_cell_info


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
        point_ids, point_distance = self.pick_point(x, y)
        line_ids, line_distance = self.pick_line(x, y)
        surface_ids, surface_distance = self.pick_surface(x, y)
        volume_ids, _ = self.pick_volume(x, y)

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

        points = self.area_pick_points(x0, y0, x1, y1, internal_picked_nodes)
        lines = self.area_pick_lines(x0, y0, x1, y1, internal_picked_nodes)
        surfaces = self.area_pick_surfaces(x0, y0, x1, y1, internal_picked_nodes)
        volumes = self.area_pick_volumes(x0, y0, x1, y1, internal_picked_nodes)

        return points, lines, surfaces, volumes

    def pick_point(self, x: int, y: int) -> set[int]:
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

    def pick_line(self, x: int, y: int) -> set[int]:
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

    def pick_surface(self, x: int, y: int) -> set[int]:
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

    def pick_volume(self, x: int, y: int) -> set[int]:
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

    def area_pick_points(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        internal_picked_nodes: list[int] | None = None,
    ) -> set[int]:
        if internal_picked_nodes is None:
            internal_picked_nodes = self._area_pick_node_internal_indexes(
                x0, y0, x1, y1
            )

        all_points = self._get_nodes_subset()
        picked_points = set(internal_picked_nodes) & set(all_points[:, 0].astype(int))
        return {i + 1 for i in picked_points}

    def area_pick_lines(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        internal_picked_nodes: list[int] | None = None,
    ) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        if internal_picked_nodes is None:
            internal_picked_nodes = self._area_pick_node_internal_indexes(
                x0, y0, x1, y1
            )

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

        mask_selected_elements = np.any(
            np.isin(mesh.lines_connectivity[:, 4:], internal_picked_nodes),
            axis=1,
        )

        return set(mesh.lines_connectivity[mask_selected_elements, 1].astype(int))

    def _pick_id(self, x: int, y: int, actor: vtkActor, array_name: str) -> int:
        cell_id, camera_distance = pick_actor_cell_info(
            x,
            y,
            actor,
            array_name,
            self.geometry_render_widget.renderer,
        )

        if cell_id < 0:
            return set(), float("inf")

        return {cell_id}, camera_distance

    # def area_pick_surfaces(
    #     self,
    #     x0: int,
    #     y0: int,
    #     x1: int,
    #     y1: int,
    #     internal_picked_nodes: list[int] | None = None,
    # ) -> set[int]:
    #     mesh = app().project.model.mesh
    #     if mesh is None:
    #         return set()

    #     if internal_picked_nodes is None:
    #         internal_picked_nodes = self._area_pick_node_internal_indexes(
    #             x0, y0, x1, y1
    #         )

    #     mask_selected_elements = np.any(
    #         np.isin(mesh.faces_connectivity[:, 4:], internal_picked_nodes),
    #         axis=1,
    #     )

    #     return set(mesh.faces_connectivity[mask_selected_elements, 1].astype(int))

    def area_pick_surfaces(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        internal_picked_nodes: list[int] | None = None,
    ) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        if internal_picked_nodes is None:
            internal_picked_nodes = self._area_pick_node_internal_indexes(
                x0, y0, x1, y1
            )

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

    def area_pick_volumes(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        internal_picked_nodes: list[int] | None = None,
    ) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        if internal_picked_nodes is None:
            internal_picked_nodes = self._area_pick_node_internal_indexes(
                x0, y0, x1, y1
            )

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

    def _get_coordinates_inside_area(
        self,
        coordinates: np.ndarray,
        area: list[int, int, int, int],
    ) -> list[int]:
        x0, y0, x1, y1 = area
        renderer = self.geometry_render_widget.renderer

        upper_left_3d = screen_to_world_coords((x0, y0, 0), renderer)
        upper_right_3d = screen_to_world_coords((x1, y0, 0), renderer)
        bottom_left_3d = screen_to_world_coords((x0, y1, 0), renderer)

        mask_horizontal = points_in_between(
            coordinates,
            upper_left_3d,
            upper_right_3d,
        )

        mask_vertical = points_in_between(
            coordinates,
            upper_left_3d,
            bottom_left_3d,
        )

        return mask_horizontal & mask_vertical

    def _area_pick_node_internal_indexes(
        self, x0: int, y0: int, x1: int, y1: int
    ) -> list[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        mask = self._get_coordinates_inside_area(
            mesh.nodal_coordinates[:, 1:],
            (x0, y0, x1, y1),
        )

        return np.arange(mesh.nodal_coordinates.shape[0])[mask]

        # picker = vtkAreaPicker()
        # extractor = vtkExtractSelectedFrustum()
        # picker.AreaPick(x0, y0, x1, y1, self.geometry_render_widget.renderer)
        # extractor.SetFrustum(picker.GetFrustum())

        # mesh = app().project.model.mesh
        # if mesh is None:
        #     return set()

        # bounds = mesh.nodal_coordinates[:, (1, 1, 2, 2, 3, 3)]
        # picked_indexes = [
        #     i for i, bound in enumerate(bounds) if extractor.OverallBoundsTest(bound)
        # ]

        # return picked_indexes
