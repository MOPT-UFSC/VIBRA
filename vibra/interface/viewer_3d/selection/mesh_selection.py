from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..render_widgets.mesh_render_widget import MeshRenderWidget

import numpy as np
from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkExtractSelectedFrustum
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkAreaPicker,
    vtkCellPicker,
)

from vibra.utils.interface_utils import world_to_screen_coords, screen_to_world_coords
from vibra.utils.math_functions import points_in_between
from vibra import app


class MeshSelection:
    def __init__(self, mesh_render_widget: "MeshRenderWidget"):
        self.mesh_render_widget = mesh_render_widget
        self.elements_center = np.array([])

    def precompute_data(self):
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        solids_connectivity = mesh.solids_connectivity[:, 4:]
        nodal_coordinates = mesh.nodal_coordinates[:, 1:]

        if mesh.solids_connectivity.size <= 0:
            return

        self.elements_center = np.average(
            nodal_coordinates[solids_connectivity],
            axis=1,
        )

    def pick(
        self, x: int, y: int
    ) -> tuple[
        set[int],
        set[int],
    ]:
        picked_nodes = self.pick_node(x, y)
        picked_solids = self.pick_solid(x, y)
        return picked_nodes, picked_solids

    def area_pick(
        self, x0: int, y0: int, x1: int, y1: int
    ) -> tuple[
        set[int],
        set[int],
    ]:
        picked_nodes = self.area_pick_nodes(x0, y0, x1, y1)
        picked_solids = self.area_pick_solids(x0, y0, x1, y1)
        return picked_nodes, picked_solids

    def pick_node(self, x: int, y: int) -> set[int]:
        """
        Pick a node in the mesh.

        This function finds the 3D coordinates of the mouse click (only works if it hit something).
        Then, the closest node is picked.
        To make sure this is a node, we project it into the screen and check if the screen distance
        to the node is smaller than the node visual radius.
        """

        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        renderer = self.mesh_render_widget.renderer
        cell_picker = vtkCellPicker()
        cell_picker.SetTolerance(0.0018)
        cell_picker.Pick(x, y, 0, renderer)

        pick_position = np.array(cell_picker.GetPickPosition())
        distance_to_pick_position = np.linalg.norm(
            pick_position - mesh.nodal_coordinates[:, 1:],
            axis=1,
        )

        index = np.argmin(distance_to_pick_position)
        world_coords = mesh.nodal_coordinates[index, 1:]
        screen_coords = world_to_screen_coords(world_coords, renderer)
        click = np.array([x, y])

        node_size = 10
        if np.linalg.norm(click - screen_coords) < node_size / 2:
            return {mesh.nodal_coordinates[index, 0].astype(int)}
        else:
            return set()

    def pick_solid(self, x: int, y: int) -> set[int]:
        cell_id = self._pick_actor_cell_id(x, y, self.mesh_render_widget.solids_actor)
        if cell_id >= 0:
            return {cell_id}
        return set()

    def area_pick_nodes(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        mask: list[int] | None = None,
    ) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        mask = self._get_coordinates_inside_area(
            coordinates=mesh.nodal_coordinates[:, 1:],
            area=(x0, y0, x1, y1),
        )
        node_indexes = mesh.nodal_coordinates[:, 0].astype(int)
        picked_nodes = set(node_indexes[mask])
        return picked_nodes

    def area_pick_solids(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
    ) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        mask_selected_elements = self._get_coordinates_inside_area(
            coordinates=self.elements_center,
            area=(x0, y0, x1, y1),
        )
        solid_indexes = mesh.solids_connectivity[:, 0].astype(int)
        return set(solid_indexes[mask_selected_elements])

    def _get_coordinates_inside_area(
        self,
        coordinates: np.ndarray,
        area: list[int, int, int, int],
    ) -> list[int]:
        x0, y0, x1, y1 = area
        renderer = self.mesh_render_widget.renderer

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

    def _pick_actor_cell_id(self, x, y, target_actor: vtkActor):
        cell_picker = vtkCellPicker()
        cell_picker.SetTolerance(0.0018)
        renderer = self.mesh_render_widget.renderer

        pickability = self._narrow_pickability_to_actor(target_actor)
        cell_picker.Pick(x, y, 0, renderer)
        self._restore_pickability(pickability)

        cell_id = cell_picker.GetCellId()
        _position = cell_picker.GetPickPosition()

        if cell_id < 0:
            return cell_id

        # Try to get the cell_indexes array that shows the original
        # cell array even if it is being clipped.
        data: vtkPolyData = target_actor.GetMapper().GetInput()
        if not data:
            return cell_id

        cell_indexes: vtkIntArray = data.GetCellData().GetArray("cell_indexes")
        if not cell_indexes:
            return cell_id

        new_cell_id = cell_indexes.GetValue(cell_id)
        return new_cell_id

    def _narrow_pickability_to_actor(self, target_actor: vtkActor):
        actor: vtkActor
        pickability = dict()
        renderer = self.mesh_render_widget.renderer

        for actor in renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            actor.SetPickable(actor == target_actor)
        return pickability

    def _restore_pickability(self, pickability: dict):
        actor: vtkActor
        renderer = self.mesh_render_widget.renderer

        for actor in renderer.GetActors():
            actor.SetPickable(pickability[actor])
