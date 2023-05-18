import vtk

from vibra.engine.mesh import Mesh
from vibra.interface.viewer_3d.common_renderer import CommonRenderer
from vibra.interface.viewer_3d.example_actor import ExampleActor
from vibra.interface.viewer_3d.faces_actor import FacesActor
from vibra.interface.viewer_3d.lines_actor import LinesActor
from vibra.interface.viewer_3d.points_actor import PointsActor


class ModelRenderer(CommonRenderer):
    def __init__(self, project=None):
        super().__init__()
        self.project = project

        self.points_actor = None
        self.lines_actor = None
        self.faces_actor = None

        self.update_actors()

    def set_project(self, project):
        self.project = project
        self.update_actors()

    def update_actors(self):
        mesh = Mesh.from_file("data/geometries/geom_akio.stp")

        self.points_actor = PointsActor(mesh)
        self.AddActor(self.points_actor)

        self.lines_actor = LinesActor(mesh)
        self.AddActor(self.lines_actor)

        self.faces_actor = FacesActor(mesh)
        self.AddActor(self.faces_actor)

        self.show_faces()

    def show_points(self):
        if not self._actors_exists():
            return

        self.points_actor.VisibilityOn()
        self.lines_actor.VisibilityOff()
        self.faces_actor.GetProperty().SetOpacity(0.1)
        self.update()

    def show_edges(self):
        if not self._actors_exists():
            return

        self.points_actor.VisibilityOff()
        self.lines_actor.VisibilityOn()
        self.faces_actor.GetProperty().SetOpacity(0.1)
        self.update()

    def show_faces(self):
        if not self._actors_exists():
            return

        self.points_actor.VisibilityOff()
        self.lines_actor.VisibilityOff()
        self.faces_actor.GetProperty().SetOpacity(1)
        self.update()

    def set_theme(self, theme):
        super().set_theme(theme)

        if not self._actors_exists():
            return

        if theme == "light":
            self.points_actor.GetProperty().SetColor(0.2, 0.2, 0.2)
            self.lines_actor.GetProperty().SetColor(0.2, 0.2, 0.2)
        elif theme == "dark":
            self.points_actor.GetProperty().SetColor(1, 1, 1)
            self.lines_actor.GetProperty().SetColor(1, 1, 1)

    def _actors_exists(self):
        if self.points_actor is None:
            return False
        
        elif self.lines_actor is None:
            return False
        
        elif self.faces_actor is None:
            return False
        
        else:
            return True