from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..render_widgets.mesh_render_widget import MeshRenderWidget

import numpy as np
from vtkmodules.vtkRenderingCore import (
    vtkCellPicker,
)

from vibra import app
from vibra.utils.interface_utils import world_to_screen_coords

from .common_selection import get_coordinates_inside_area, pick_actor_cell_info


class MeshSelection:
    def __init__(self, mesh_render_widget: "MeshRenderWidget"):
        self.mesh_render_widget = mesh_render_widget
        self.elements_center = np.array([])
        self.cell_picker = vtkCellPicker()
        self.cell_picker.SetTolerance(0.0018)

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
        picked_nodes, nodes_distance = self._pick_node(x, y)
        picked_solids, solids_distance = self._pick_solid(x, y)

        # Cheating a bit to prioritize point selection
        nodes_distance *= 0.98
        closest = min(nodes_distance, solids_distance)

        if closest == nodes_distance:
            return picked_nodes, set()
        
        elif closest == solids_distance:
            return set(), picked_solids
        
        else:
            return set(), set()

    def area_pick(
        self, x0: int, y0: int, x1: int, y1: int
    ) -> tuple[
        set[int],
        set[int],
    ]:
        picked_nodes = self._area_pick_nodes(x0, y0, x1, y1)
        picked_solids = self._area_pick_solids(x0, y0, x1, y1)
        return picked_nodes, picked_solids

    def _pick_node(self, x: int, y: int) -> set[int]:
        """
        Pick a node in the mesh.

        This function finds the 3D coordinates of the mouse click (only works if it hit something).
        Then, the closest node is picked.
        To make sure this is a node, we project it into the screen and check if the screen distance
        to the node is smaller than the node visual radius.
        """

        mesh = app().project.model.mesh
        if mesh is None:
            return set(), float("inf")

        renderer = self.mesh_render_widget.renderer
        self.cell_picker.Pick(x, y, 0, renderer)

        pick_position = np.array(self.cell_picker.GetPickPosition())
        distance_to_pick_position = np.linalg.norm(
            pick_position - mesh.nodal_coordinates[:, 1:],
            axis=1,
        )

        index = np.argmin(distance_to_pick_position)
        world_coords = mesh.nodal_coordinates[index, 1:]
        screen_coords = world_to_screen_coords(world_coords, renderer)
        click = np.array([x, y])

        camera_position = np.array(renderer.GetActiveCamera().GetPosition())
        camera_distance = np.linalg.norm(camera_position - pick_position)

        node_size = 10
        if np.linalg.norm(click - screen_coords) < node_size / 2:
            return {mesh.nodal_coordinates[index, 0].astype(int)}, camera_distance
        else:
            return set(), float("inf")

    def _pick_solid(self, x: int, y: int) -> set[int]:
        solid_id, solid_distance = pick_actor_cell_info(
            x,
            y,
            self.mesh_render_widget.solids_actor,
            "cell_indexes",
            self.mesh_render_widget.renderer,
        )

        if solid_id < 0:
            return set(), float("inf")
    
        return {solid_id}, solid_distance

    def _area_pick_nodes(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
    ) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        mask = get_coordinates_inside_area(
            mesh.nodal_coordinates[:, 1:],
            (x0, y0, x1, y1),
            self.mesh_render_widget.renderer,
        )

        node_indexes = mesh.nodal_coordinates[:, 0].astype(int)
        picked_nodes = set(node_indexes[mask])
        return picked_nodes

    def _area_pick_solids(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
    ) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        mask_selected_elements = get_coordinates_inside_area(
            self.elements_center,
            (x0, y0, x1, y1),
            self.mesh_render_widget.renderer,
        )

        solid_indexes = mesh.solids_connectivity[:, 0].astype(int)
        return set(solid_indexes[mask_selected_elements])
