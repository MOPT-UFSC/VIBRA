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
    vtkCoordinate,
)

from vibra import app


class MeshSelection:
    def __init__(self, mesh_render_widget: "MeshRenderWidget"):
        self.mesh_render_widget = mesh_render_widget

    def pick_node(self, x: int, y: int) -> set[int]:
        '''
        Pick a node in the mesh.

        This function finds the 3D coordinates of the mouse click (only works if it hit something).
        Then, the closest node is picked.
        To make sure this is a node, we project it into the screen and check if the screen distance
        to the node is smaller than the node visual radius.
        '''

        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        renderer = self.mesh_render_widget.renderer
        cell_picker = vtkCellPicker()
        cell_picker.SetTolerance(0.0018)
        cell_picker.Pick(x, y, 0, renderer)

        pick_position = np.array(cell_picker.GetPickPosition())
        i = np.argmin(np.linalg.norm(mesh.nodal_coordinates[:, 1:] - pick_position, axis=1))

        coordinate = vtkCoordinate()
        coordinate.SetCoordinateSystemToWorld()
        coordinate.SetValue(mesh.nodal_coordinates[i, 1:])
        view_coords = coordinate.GetComputedViewportValue(renderer)
        click = np.array([x, y])

        node_size = 10
        if np.linalg.norm(click - view_coords) < node_size / 2:
            return {mesh.nodal_coordinates[i, 0].astype(int)}

        return set()

    def pick_solid(self, x: int, y: int) -> set[int]:
        cell_id = self._pick_actor_cell_id(x, y, self.mesh_render_widget.solids_actor)
        if cell_id >= 0:
            return {cell_id}
        return set()

    def area_pick_nodes(self, x0: int, y0: int, x1: int, y1: int) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        picked_indexes = self._area_pick_node_internal_indexes(x0, y0, x1, y1)
        picked_nodes = set(mesh.nodal_coordinates[picked_indexes, 0].astype(int))
        return picked_nodes

    def area_pick_solids(self, x0: int, y0: int, x1: int, y1: int) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        picked_nodes = self._area_pick_node_internal_indexes(x0, y0, x1, y1)
        mask_selected_elements = np.any(
            np.isin(mesh.solids_connectivity[:, 4:], picked_nodes), axis=1
        )

        return set(mesh.solids_connectivity[mask_selected_elements, 0].astype(int))

    def _area_pick_node_internal_indexes(self, x0: int, y0: int, x1: int, y1: int) -> list[int]:
        picker = vtkAreaPicker()
        extractor = vtkExtractSelectedFrustum()
        picker.AreaPick(x0, y0, x1, y1, self.mesh_render_widget.renderer)
        extractor.SetFrustum(picker.GetFrustum())

        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        bounds = mesh.nodal_coordinates[:, (1, 1, 2, 2, 3, 3)]
        picked_indexes = [i for i, bound in enumerate(bounds) if extractor.OverallBoundsTest(bound)]

        return picked_indexes

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
