from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from vibra.interface.viewer_3d.actors.faces_actor import FacesActor
from vibra.interface.viewer_3d.actors.lines_actor import LinesActor
from vibra.interface.viewer_3d.actors.points_actor import PointsActor
from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget
from vibra.interface.viewer_3d.interactor_styles.selection_interactor import (
    SelectionInteractor,
)
from vibra.interface.tabs.geometry_info_bar import GeometryInfoBar

SHOW_POINTS = 0
SHOW_LINES = 1
SHOW_FACES = 2


class GeometryRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal(list, list, list)

    def __init__(self, project, parent=None):
        super().__init__(parent)

        self.project = project
        self.view_mode = SHOW_FACES
        
        self.geometry_info = GeometryInfoBar()

        # replace the layout to add other usefull widgets
        QObjectCleanupHandler().add(self.layout())
        layout = QVBoxLayout()
        layout.addWidget(self.geometry_info)
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.points_actor = None
        self.lines_actor = None
        self.faces_actor = None

        self.selection_color = (20, 106, 245)
        self.selected_points = []
        self.selected_lines = []
        self.selected_faces = []

        self.style = SelectionInteractor()
        self.style.AddObserver("SelectionEvent", self.selection_callback)
        self.render_interactor.SetInteractorStyle(self.style)

        self.create_axes()
        self.update_plot()

    def update_plot(self):
        if self.project is None:
            return

        model = self.project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        self.update_theme()
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

    #
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

    #
    def selection_callback(self, obj, event):
        if not self._actors_exists():
            return

        clicked_cell = obj.selection_picker.GetCellId()
        clicked_actor = obj.selection_picker.GetActor()

        self.clear_selection()

        if clicked_actor == self.points_actor:
            self.select_point(clicked_cell)

        if clicked_actor == self.lines_actor:
            line_entity = self.project.model.mesh.lines_connectivity[clicked_cell][1]
            self.select_line(line_entity)

        if clicked_actor == self.faces_actor:
            face_entity = self.project.model.mesh.faces_connectivity[clicked_cell][1]
            self.select_face(face_entity)

        self.update()

    def select_point(self, point):
        if self.view_mode != SHOW_POINTS:
            return
        self.selected_points = [point]
        self.points_actor.clear_colors()
        self.points_actor.paint_cells(self.selection_color, [point])
        self.update()
        self.selection_changed.emit(self.selected_points, self.selected_lines, self.selected_faces)

    def select_line(self, line):
        if self.view_mode != SHOW_LINES:
            return

        element_indexes = self.project.model.mesh.entity_ranges[1, line]
        self.selected_lines = [line]
        self.lines_actor.clear_colors()
        self.lines_actor.paint_cells(self.selection_color, element_indexes)
        self.update()
        self.selection_changed.emit(self.selected_points, self.selected_lines, self.selected_faces)

    def select_face(self, face):
        if self.view_mode != SHOW_FACES:
            return

        element_indexes = self.project.model.mesh.entity_ranges[2, face]
        self.selected_faces = [face]
        self.faces_actor.clear_colors()
        self.faces_actor.paint_cells(self.selection_color, element_indexes)
        self.update()
        self.selection_changed.emit(self.selected_points, self.selected_lines, self.selected_faces)

    def clear_selection(self):
        self.points_actor.clear_colors()
        self.lines_actor.clear_colors()
        self.faces_actor.clear_colors()
        self.selected_points = []
        self.selected_lines = []
        self.selected_faces = []

    #
    def remove_actors(self):
        self.renderer.RemoveActor(self.points_actor)
        self.renderer.RemoveActor(self.lines_actor)
        self.renderer.RemoveActor(self.faces_actor)

        self.points_actor = None
        self.lines_actor = None
        self.faces_actor = None

    def _actors_exists(self):
        actors = [
            self.points_actor,
            self.lines_actor,
            self.faces_actor,
        ]
        return all([actor is not None for actor in actors])
