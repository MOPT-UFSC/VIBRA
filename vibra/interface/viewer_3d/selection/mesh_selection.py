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
        self.solid_elements_center = np.array([])
        self.face_elements_center = np.array([])
        self.cell_picker = vtkCellPicker()
        self.cell_picker.SetTolerance(0.0018)

    def precompute_data(self):
        mesh = app().project.model.mesh
        if mesh is None:
            return

        solids_connectivity = mesh.solids_connectivity[:, 4:]
        faces_connectivity = mesh.faces_connectivity[:, 4:]
        nodal_coordinates = mesh.nodal_coordinates[:, 1:]

        if mesh.solids_connectivity.size > 0:
            self.solid_elements_center = np.average(
                nodal_coordinates[solids_connectivity],
                axis=1,
            )
        else:
            self.solid_elements_center = np.array([])

        if mesh.faces_connectivity.size > 0:
            self.face_elements_center = np.average(
                nodal_coordinates[faces_connectivity],
                axis=1,
            )
        else:
            self.face_elements_center = np.array([])

    def pick(
        self, x: int, y: int
    ) -> tuple[
        set[int],
        set[int],
    ]:
        picked_nodes, nodes_distance = self._pick_node(x, y)
        picked_faces, faces_distance = self._pick_face(x, y)
        picked_solids, solids_distance = self._pick_solid(x, y)

        # Cheating a bit to prioritize point selection
        nodes_distance *= 0.98
        closest = min(nodes_distance, faces_distance, solids_distance)

        if closest == nodes_distance:
            return picked_nodes, set(), set()
        else:
            return set(), picked_faces, picked_solids

    def area_pick(
        self, x0: int, y0: int, x1: int, y1: int
    ) -> tuple[
        set[int],
        set[int],
    ]:
        picked_nodes = self._area_pick_nodes(x0, y0, x1, y1)
        picked_faces = self._area_pick_faces(x0, y0, x1, y1)

        picked_solids = set()
        if self.solid_elements_center.size > 0:
            picked_solids = self._area_pick_solids(x0, y0, x1, y1)

        return picked_nodes, picked_faces, picked_solids

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

        node_size = 8
        if np.linalg.norm(click - screen_coords) < node_size / 2:
            return {mesh.nodal_coordinates[index, 0].astype(int)}, camera_distance
        else:
            return set(), float("inf")

    def _pick_face(self, x: int, y: int) -> set[int]:
        face_id, face_distance = pick_actor_cell_info(
            x,
            y,
            self.mesh_render_widget.faces_actor,
            "face_indexes",
            self.mesh_render_widget.renderer,
        )

        if face_id < 0:
            return set(), float("inf")

        return {face_id}, face_distance

    def _pick_solid(self, x: int, y: int) -> set[int]:
        solid_id, solid_distance = pick_actor_cell_info(
            x,
            y,
            self.mesh_render_widget.solids_actor,
            "solid_indexes",
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

    def _area_pick_faces(self, x0: int, y0: int, x1: int, y1: int) -> set[int]:
        mesh = app().project.model.mesh
        if mesh is None:
            return set()

        if self.face_elements_center.size == 0:
            return set()

        mask_selected_faces = get_coordinates_inside_area(
            self.face_elements_center,
            (x0, y0, x1, y1),
            self.mesh_render_widget.renderer,
        )

        face_indexes = mesh.faces_connectivity[:, 0].astype(int)
        return set(face_indexes[mask_selected_faces])

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

        if self.solid_elements_center.size == 0:
            return set()

        mask_selected_elements = get_coordinates_inside_area(
            self.solid_elements_center,
            (x0, y0, x1, y1),
            self.mesh_render_widget.renderer,
        )

        solid_indexes = mesh.solids_connectivity[:, 0].astype(int)
        return set(solid_indexes[mask_selected_elements])
