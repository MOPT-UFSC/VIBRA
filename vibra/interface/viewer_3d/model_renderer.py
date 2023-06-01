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

        self.selection_color = (20, 106, 245)
        self.selected_points = []
        self.selected_lines = []
        self.selected_faces = []

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

        self.ResetCamera()
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

    def select_point(self, point):
        if self.view_mode != SHOW_POINTS:
            return
        self.selected_points = [point]
        self.points_actor.clear_colors()
        self.points_actor.paint_cells(self.selection_color, [point])

    def select_line(self, line):
        if self.view_mode != SHOW_LINES:
            return
        self.selected_lines = [line]
        self.lines_actor.clear_colors()
        self.lines_actor.paint_cells(self.selection_color, self.project.mesh.line_entities[line])

    def select_face(self, face):
        if self.view_mode != SHOW_FACES:
            return
        self.selected_faces = [face]
        self.faces_actor.clear_colors()
        self.faces_actor.paint_cells(self.selection_color, self.project.mesh.face_entities[face])
        self.update()

    def clear_selection(self):
        self.points_actor.clear_colors()
        self.lines_actor.clear_colors()
        self.faces_actor.clear_colors()
        self.selected_points = []
        self.selected_lines = []
        self.selected_faces = []

    def selection_callback(self, obj, event):
        if not self._actors_exists():
            return

        clicked_cell = obj.selection_picker.GetCellId()
        clicked_actor = obj.selection_picker.GetActor()

        self.clear_selection()

        if clicked_actor == self.points_actor:
            self.select_point(clicked_cell)

        if clicked_actor == self.lines_actor:
            line_entity = self._find_key(clicked_cell, self.project.mesh.line_entities)
            self.select_line(line_entity)

        if clicked_actor == self.faces_actor:
            face_entity = self._find_key(clicked_cell, self.project.mesh.face_entities)
            self.select_face(face_entity)

        self.update()

    def _find_key(self, value, dictionary):
        '''
        Given a dictionary finds the key that contains 
        some value in it.

        This function only make sense if the dict 
        values are sets, because in sets it is a 
        very inexpensive operation.
        '''
        for key, values in dictionary.items():
            if value in values:
                return key
        else:
            return None

    def _actors_exists(self):
        if self.points_actor is None:
            return False

        elif self.lines_actor is None:
            return False

        elif self.faces_actor is None:
            return False

        else:
            return True
