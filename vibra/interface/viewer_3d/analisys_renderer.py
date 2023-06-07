import vtk

from vibra.engine.mesh import Mesh
from vibra.interface.viewer_3d.actors.example_actor import ExampleActor
from vibra.interface.viewer_3d.actors.clipped_actor import ClippedActor
from vibra.interface.viewer_3d.actors.lines_actor import LinesActor
from vibra.interface.viewer_3d.actors.points_actor import PointsActor
from vibra.interface.viewer_3d.common_renderer import CommonRenderer
from vibra.interface.viewer_3d.actors.cutting_plane_actor import CuttingPlaneActor

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
        self.AddActor(self.plane_actor)

    def remove_actors(self):
        self.RemoveActor(self.model_actor)
        self.RemoveActor(self.plane_actor)

    def configure_plane(self, position, normal):   
        self.plane_actor.SetPosition(position)
        self.plane_actor.SetOrientation(normal)
        self.update()

    def apply_cut(self, position, normal):
        self.model_actor.apply_cut(position, normal)
        self.update()

    def _actors_exists(self):
        if self.model_actor is None:
            return False
        else:
            return True
