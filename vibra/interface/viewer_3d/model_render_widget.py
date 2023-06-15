from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget
from vibra.interface.viewer_3d.actors.faces_actor import FacesActor
from vibra.interface.viewer_3d.actors.lines_actor import LinesActor
from vibra.interface.viewer_3d.actors.points_actor import PointsActor


SHOW_POINTS = 0
SHOW_LINES = 1
SHOW_FACES = 2


class ModelRenderWidget(CommonRenderWidget):
    def __init__(self, project, parent):
        super().__init__(parent)
        
        self.project = project
        self.view_mode = SHOW_FACES

        self.points_actor = None
        self.lines_actor = None
        self.faces_actor = None

        self.update_plot()

    def update_plot(self):
        if self.project is None:
            return
            
        mesh = self.project.mesh

        if mesh is None:
            return

        self.remove_actors()

        self.points_actor = PointsActor(mesh)
        self.renderer.AddActor(self.points_actor)

        self.lines_actor = LinesActor(mesh)
        self.renderer.AddActor(self.lines_actor)

        self.faces_actor = FacesActor(mesh)
        self.renderer.AddActor(self.faces_actor)

        self.renderer.ResetCamera()
        self.show_faces()

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

    def show_points(self):
        if not self._actors_exists():
            return

        self.points_actor.VisibilityOn()
        self.lines_actor.VisibilityOff()
        self.faces_actor.GetProperty().SetOpacity(0.1)

        self.points_actor.PickableOn()
        self.lines_actor.PickableOff()
        self.faces_actor.PickableOff()

        self.view_mode = SHOW_POINTS
        self.update()

    def show_lines(self):
        if not self._actors_exists():
            return

        self.points_actor.VisibilityOff()
        self.lines_actor.VisibilityOn()
        self.faces_actor.GetProperty().SetOpacity(0.1)

        self.points_actor.PickableOff()
        self.lines_actor.PickableOn()
        self.faces_actor.PickableOff()

        self.view_mode = SHOW_LINES
        self.update()

    def show_faces(self):
        if not self._actors_exists():
            return

        self.points_actor.VisibilityOff()
        self.lines_actor.VisibilityOff()
        self.faces_actor.GetProperty().SetOpacity(1)

        self.points_actor.PickableOff()
        self.lines_actor.PickableOff()
        self.faces_actor.PickableOn()

        self.view_mode = SHOW_FACES
        self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.points_actor)
        self.renderer.RemoveActor(self.lines_actor)
        self.renderer.RemoveActor(self.faces_actor)

        self.points_actor = None
        self.lines_actor = None
        self.faces_actor = None

    def _actors_exists(self):
        if self.points_actor is None:
            return False

        elif self.lines_actor is None:
            return False

        elif self.faces_actor is None:
            return False

        else:
            return True
