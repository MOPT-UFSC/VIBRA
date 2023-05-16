import vtk

from vibra.engine.mesh import Mesh
from vibra.interface.viewer_3d.common_renderer import CommonRenderer
from vibra.interface.viewer_3d.example_actor import ExampleActor
from vibra.interface.viewer_3d.faces_actor import FacesActor
from vibra.interface.viewer_3d.lines_actor import LinesActor
from vibra.interface.viewer_3d.points_actor import PointsActor


class ModelRenderer(CommonRenderer):
    def __init__(self):
        super().__init__()
        self.update_actors()

    def update_actors(self):
        mesh = Mesh.from_file("data/geometries/vessel.step")

        self.points_actor = PointsActor(mesh)
        self.AddActor(self.points_actor)

        self.lines_actor = LinesActor(mesh)
        self.AddActor(self.lines_actor)

        self.faces_actor = FacesActor(mesh)
        self.AddActor(self.faces_actor)

        self.show_faces()

    def show_points(self):
        self.points_actor.VisibilityOn()
        self.lines_actor.VisibilityOff()
        self.faces_actor.GetProperty().SetOpacity(0.03)
        self.rerender_window()

    def show_edges(self):
        self.points_actor.VisibilityOff()
        self.lines_actor.VisibilityOn()
        self.faces_actor.GetProperty().SetOpacity(0.03)
        self.rerender_window()

    def show_faces(self):
        self.points_actor.VisibilityOff()
        self.lines_actor.VisibilityOff()
        self.faces_actor.GetProperty().SetOpacity(1)
        self.rerender_window()
