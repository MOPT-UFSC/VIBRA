from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from vibra.interface.viewer_3d.actors.faces_actor import FacesActor
from vibra.interface.viewer_3d.actors.lines_actor import LinesActor
from vibra.interface.viewer_3d.actors.points_actor import PointsActor
from vibra.interface.viewer_3d.render_widgets.common_render_widget import CommonRenderWidget
from vibra.interface.viewer_3d.interactor_styles.selection_interactor import (
    SelectionInteractor,
)
from vibra.interface.tabs.geometry_info_bar import GeometryInfoBar

SHOW_POINTS = 0
SHOW_LINES = 1
SHOW_FACES = 2


class GeometryRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal(set, set, set, set)

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
        self.selected_points = set()
        self.selected_lines = set()
        self.selected_faces = set()
        self.selected_volumes = set()

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
        
        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = (modifiers & Qt.ControlModifier)
        shift_pressed = (modifiers & Qt.ShiftModifier)
        alt_pressed = (modifiers & Qt.AltModifier)

        if clicked_actor == self.points_actor:
            self.select_point(clicked_cell, join=shift_pressed, remove=alt_pressed)

        elif clicked_actor == self.lines_actor:
            line_entity = self.project.model.mesh.lines_connectivity[clicked_cell][1]
            self.select_line(line_entity, join=shift_pressed, remove=alt_pressed)

        elif (clicked_actor == self.faces_actor) and not ctrl_pressed:
            face_entity = self.project.model.mesh.faces_connectivity[clicked_cell][1]
            self.select_face(face_entity, join=shift_pressed, remove=alt_pressed)

        elif (clicked_actor == self.faces_actor) and ctrl_pressed:
            face_entity = self.project.model.mesh.faces_connectivity[clicked_cell][1]
            for volume, surfaces in self.project.model.mesh.surfaces_from_volumes.items():
                if face_entity in surfaces:
                    self.select_volume(volume, join=shift_pressed, remove=alt_pressed)
                    break

        else:
            self.clear_selection()
            self.selection_changed.emit(self.selected_points, self.selected_lines, self.selected_faces, self.selected_volumes)

        self.update()

    def select_point(self, new_point, *, join=False, remove=False):
        self.select_multiple_points([new_point], join=join, remove=remove)

    def select_line(self, new_line, *, join=False, remove=False):
        self.select_multiple_lines([new_line], join=join, remove=remove)

    def select_face(self, new_face, *, join=False, remove=False):
        self.select_multiple_faces([new_face], join=join, remove=remove)

    def select_volume(self, new_volume, *, join=False, remove=False):
        self.select_multiple_volumes([new_volume], join=join, remove=remove)

    def select_multiple_points(self, new_points, *, join=False, remove=False):
        if self.view_mode != SHOW_POINTS:
            return
        
        if join:
            self.selected_points |= set(new_points)
        elif remove:
            self.selected_points -= set(new_points)
        else:
            self.selected_points = set(new_points)

        self.points_actor.clear_colors()
        self.points_actor.paint_cells(self.selection_color, self.selected_points)
        self.update()
        self.selection_changed.emit(self.selected_points, self.selected_lines, self.selected_faces, self.selected_volumes)

    def select_multiple_lines(self, new_lines, *, join=False, remove=False):
        if self.view_mode != SHOW_LINES:
            return

        if join:
            self.selected_lines |= set(new_lines)
        elif remove:
            self.selected_lines -= set(new_lines)
        else:
            self.selected_lines = set(new_lines)

        all_element_indexes = []
        for line in self.selected_lines:
            element_indexes = self.project.model.mesh.entity_ranges[1, line]
            all_element_indexes.extend(element_indexes)

        self.lines_actor.clear_colors()
        self.lines_actor.paint_cells(self.selection_color, all_element_indexes)
        self.update()
        self.selection_changed.emit(self.selected_points, self.selected_lines, self.selected_faces, self.selected_volumes)

    def select_multiple_faces(self, new_faces, *, join=False, remove=False):
        if self.view_mode != SHOW_FACES:
            return

        if join:
            self.selected_faces |= set(new_faces)
        elif remove:
            self.selected_faces -= set(new_faces)
        else:
            self.selected_faces = set(new_faces)
        self.selected_volumes.clear()

        all_element_indexes = []
        for face in self.selected_faces:
            element_indexes = self.project.model.mesh.entity_ranges[2, face]
            all_element_indexes.extend(element_indexes)

        self.faces_actor.clear_colors()
        self.faces_actor.paint_cells(self.selection_color, all_element_indexes)
        self.update()
        self.selection_changed.emit(self.selected_points, self.selected_lines, self.selected_faces, self.selected_volumes)

    def select_multiple_volumes(self, new_volumes, *, join=False, remove=False):
        if self.view_mode != SHOW_FACES:
            return

        if join:
            self.selected_volumes |= set(new_volumes)
        elif remove:
            self.selected_volumes -= set(new_volumes)
        else:
            self.selected_volumes = set(new_volumes)
        self.selected_faces.clear()

        all_element_indexes = []
        for volume in self.selected_volumes:
            surfaces = self.project.model.mesh.surfaces_from_volumes[volume]
            for face in surfaces:
                element_indexes = self.project.model.mesh.entity_ranges[2, face]
                all_element_indexes.extend(element_indexes)

        self.faces_actor.clear_colors()
        self.faces_actor.paint_cells(self.selection_color, all_element_indexes)
        self.update()
        self.selection_changed.emit(self.selected_points, self.selected_lines, self.selected_faces, self.selected_volumes)

    def clear_selection(self):
        self.points_actor.clear_colors()
        self.lines_actor.clear_colors()
        self.faces_actor.clear_colors()
        self.selected_points = set()
        self.selected_lines = set()
        self.selected_faces = set()
        self.selected_volumes = set()

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
