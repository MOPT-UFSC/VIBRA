from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..render_widgets.geometry_render_widget import GeometryRenderWidget

import numpy as np
from vtkmodules.vtkFiltersGeneral import vtkExtractSelectedFrustum
from vtkmodules.vtkRenderingCore import (
    vtkAreaPicker,
    vtkCellPicker,
    vtkCoordinate,
)

from vibra import app

from .common_selection import pick_actor_cell_info


class GeometrySelection:
    def __init__(self, geometry_render_widget: "GeometryRenderWidget"):
        self.geometry_render_widget = geometry_render_widget

    def pick_point(self, x: int, y: int) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        renderer = self.geometry_render_widget.renderer
        cell_picker = vtkCellPicker()
        cell_picker.SetTolerance(0.0018)
        cell_picker.Pick(x, y, 0, renderer)

        pick_position = np.array(cell_picker.GetPickPosition())
        all_points = self._get_nodes_subset()  # The point id is 1-indexed
        i = np.argmin(np.linalg.norm(all_points[:, 1:] - pick_position, axis=1))

        coordinate = vtkCoordinate()
        coordinate.SetCoordinateSystemToWorld()
        coordinate.SetValue(all_points[i, 1:])
        view_coords = coordinate.GetComputedViewportValue(renderer)
        click = np.array([x, y])

        node_size = 15
        if np.linalg.norm(click - view_coords) < node_size / 2:
            return {1 + all_points[i, 0].astype(int)}
        else:
            return set()

    def pick_line(self, x: int, y: int) -> set[int]:
        cell_id = pick_actor_cell_info(
            x,
            y,
            self.geometry_render_widget.lines_actor,
            "line_indexes",
            self.geometry_render_widget.renderer,
        )
        if cell_id >= 0:
            return {cell_id}
        else:
            return set()

    def pick_surface(self, x: int, y: int) -> set[int]:
        surface = pick_actor_cell_info(
            x,
            y,
            self.geometry_render_widget.faces_actor,
            "surface_indexes",
            self.geometry_render_widget.renderer,
        )
        if surface >= 0:
            return {surface}
        else:
            return set()

    def pick_volume(self, x: int, y: int) -> set[int]:
        volume = pick_actor_cell_info(
            x,
            y,
            self.geometry_render_widget.faces_actor,
            "volume_indexes",
            self.geometry_render_widget.renderer,
        )
        if volume >= 0:
            return {volume}
        else:
            return set()

    def area_pick_points(self, x0: int, y0: int, x1: int, y1: int) -> set[int]:
        picked_nodes = self._area_pick_node_internal_indexes(x0, y0, x1, y1)
        all_points = self._get_nodes_subset()
        picked_points = set(picked_nodes) & set(all_points[:, 0].astype(int))
        return {i + 1 for i in picked_points}

    def area_pick_lines(self, x0: int, y0: int, x1: int, y1: int) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        picked_nodes = self._area_pick_node_internal_indexes(x0, y0, x1, y1)
        mask_selected_elements = np.all(
            np.isin(mesh.lines_connectivity[:, 4:], picked_nodes),
            axis=1
        )

        return set(mesh.lines_connectivity[mask_selected_elements, 1].astype(int))

    def area_pick_surfaces(self, x0: int, y0: int, x1: int, y1: int) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        picked_nodes = self._area_pick_node_internal_indexes(x0, y0, x1, y1)
        mask_selected_elements = np.all(
            np.isin(mesh.faces_connectivity[:, 4:], picked_nodes),
            axis=1
        )

        return set(mesh.faces_connectivity[mask_selected_elements, 1].astype(int))

    def area_pick_volumes(self, x0: int, y0: int, x1: int, y1: int) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        picked_nodes = self._area_pick_node_internal_indexes(x0, y0, x1, y1)
        mask_selected_elements = np.all(
            np.isin(mesh.solids_connectivity[:, 4:], picked_nodes), 
            axis=1
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
        picker = vtkAreaPicker()
        extractor = vtkExtractSelectedFrustum()
        picker.AreaPick(x0, y0, x1, y1, self.geometry_render_widget.renderer)
        extractor.SetFrustum(picker.GetFrustum())

        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        bounds = mesh.nodal_coordinates[:, (1, 1, 2, 2, 3, 3)]
        picked_indexes = [i for i, bound in enumerate(bounds) if extractor.OverallBoundsTest(bound)]

        return picked_indexes
