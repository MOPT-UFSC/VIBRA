import numpy as np
import vtk

from vibra.engine.mesh import Mesh
from vibra.interface.viewer_3d.actors.clipped_actor import ClippedActor
from vibra.interface.viewer_3d.actors.cutting_plane_actor import (
    CuttingPlaneActor,
)
from vibra.interface.viewer_3d.actors.example_actor import ExampleActor
from vibra.interface.viewer_3d.actors.lines_actor import LinesActor
from vibra.interface.viewer_3d.actors.points_actor import PointsActor
from vibra.interface.viewer_3d.common_renderer import CommonRenderer

SHOW_POINTS = 0
SHOW_LINES = 1
SHOW_FACES = 2


class AnalisysRenderer(CommonRenderer):
    def __init__(self, project=None):
        super().__init__()
        self.project = project

        self.model_actor = None
        self.plane_actor = None

        self.update_actors()

    def set_project(self, project):
        self.project = project
        self.update_actors()
        self.ResetCamera()

    def update_actors(self):
        if self.project is None:
            return

        mesh = self.project.mesh

        if mesh is None:
            return

        self.remove_actors()

        self.model_actor = ClippedActor(mesh)
        self.AddActor(self.model_actor)

        self.plane_actor = CuttingPlaneActor()
        self.plane_actor.VisibilityOff()
        self.AddActor(self.plane_actor)

    def remove_actors(self):
        self.RemoveActor(self.model_actor)
        self.RemoveActor(self.plane_actor)

    def configure_plane(self, position, orientation):
        if not self._actors_exists():
            return

        self.disable_cut()
        self.plane_actor.VisibilityOn()
        self.model_actor.GetProperty().SetOpacity(0.2)

        self.plane_actor.SetPosition(position)
        self.plane_actor.SetOrientation(orientation)
        self.update()

    def apply_cut(self, position, orientation):
        if not self._actors_exists():
            return

        normal = self._calculate_normal_vector(orientation)
        self.model_actor.apply_cut(position, normal)
        self.model_actor.GetProperty().SetOpacity(1)
        self.update()

    def disable_cut(self):
        if not self._actors_exists():
            return
        self.plane_actor.VisibilityOff()
        self.model_actor.disable_cut()

    def _actors_exists(self):
        if self.model_actor is None:
            return False
        else:
            return True

    def _calculate_normal_vector(self, orientation):
        # https://forum.gamemaker.io/index.php?threads/solved-3d-rotations-with-a-shader-matrix-or-a-matrix-glsl-es.61064/

        orientation = np.array(orientation) * np.pi / 180

        sin = np.sin(orientation)
        cos = np.cos(orientation)

        rx = np.array(
            [
                [1, 0, 0, 0],
                [0, cos[0], -sin[0], 0],
                [0, sin[0], cos[0], 0],
                [0, 0, 0, 1],
            ]
        )

        ry = np.array(
            [
                [cos[1], 0, sin[1], 0],
                [0, 1, 0, 0],
                [-sin[1], 0, cos[1], 0],
                [0, 0, 0, 1],
            ]
        )

        rz = np.array(
            [
                [cos[2], -sin[2], 0, 0],
                [sin[2], cos[2], 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

        normal = rz @ rx @ ry @ np.array([1, 0, 0, 1])
        return normal[:3]
