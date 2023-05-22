import vtk

from vibra.engine.mesh import Mesh
from vibra.interface.viewer_3d.actors.example_actor import ExampleActor
from vibra.interface.viewer_3d.actors.faces_actor import FacesActor
from vibra.interface.viewer_3d.actors.lines_actor import LinesActor
from vibra.interface.viewer_3d.actors.points_actor import PointsActor
from vibra.interface.viewer_3d.common_renderer import CommonRenderer


SHOW_POINTS = 0
SHOW_LINES = 1
SHOW_FACES = 2


class ModelRenderer(CommonRenderer):
    def __init__(self, project=None):
        super().__init__()
        self.project = project
        self.view_mode = SHOW_FACES

        self.points_actor = None
        self.lines_actor = None
        self.faces_actor = None

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

        self.points_actor = PointsActor(mesh)
        self.AddActor(self.points_actor)

        self.lines_actor = LinesActor(mesh)
        self.AddActor(self.lines_actor)

        self.faces_actor = FacesActor(mesh)
        self.AddActor(self.faces_actor)

        self.show_faces()

    def remove_actors(self):
        self.RemoveActor(self.points_actor)
        self.RemoveActor(self.lines_actor)
        self.RemoveActor(self.faces_actor)

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

    def show_edges(self):
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

    def update_selection(self, selection_interactor):
        if not self._actors_exists():
            return 

        clicked_cell = selection_interactor.selection_picker.GetCellId()
        clicked_actor = selection_interactor.selection_picker.GetActor()

        selection_color = (20, 106, 245)
        self.points_actor.clear_colors()
        self.lines_actor.clear_colors()
        self.faces_actor.clear_colors()

        if (clicked_actor == self.points_actor) and (self.view_mode == SHOW_POINTS):
            self.points_actor.paint_cells(selection_color, [clicked_cell])

        if (clicked_actor == self.lines_actor) and (self.view_mode == SHOW_LINES):
            cells_to_highlight = self._find_subset(clicked_cell, self.project.mesh.line_entities.values())
            self.lines_actor.paint_cells(selection_color, cells_to_highlight)

        if (clicked_actor == self.faces_actor) and (self.view_mode == SHOW_FACES):
            cells_to_highlight = self._find_subset(clicked_cell, self.project.mesh.face_entities.values())
            self.faces_actor.paint_cells(selection_color, cells_to_highlight)
            
        self.update()

    def _find_subset(self, value, sets):
        for subset in sets:
            if value in subset:
                return subset
        else:
            return set()

    def _actors_exists(self):
        if self.points_actor is None:
            return False

        elif self.lines_actor is None:
            return False

        elif self.faces_actor is None:
            return False

        else:
            return True
