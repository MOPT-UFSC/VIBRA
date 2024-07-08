from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import vtk

from molde.render_widgets import CommonRenderWidget

from vibra.interface.tabs.mesh_info_bar import MeshInfoBar
from vibra.interface.viewer_3d.actors.nodes_actor import NodesActor
from vibra.interface.viewer_3d.actors.edges_actor import EdgesActor
from vibra.interface.viewer_3d.actors.faces_actor import FacesActor
from vibra.interface.viewer_3d.actors.solids_actor import SolidsActor
from vibra.utils.interface_functions import get_main_window
from vibra.interface.viewer_3d.actors.selection_spheres import SelectionSpheres
from vibra import app

SHOW_POINTS = 0
SHOW_LINES = 1
SHOW_FACES = 2
SHOW_VOLUMES = 3


class MeshRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal(list, list, list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mouse_click = (0, 0)
        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        app().main_window.selection_changed.connect(self.update_selection)

        self.main_window = get_main_window()
        self.view_mode = SHOW_FACES
        self.selection_color = (20, 106, 245)

        self.mesh_info = MeshInfoBar()

        # replace the layout to add other usefull widgets
        QObjectCleanupHandler().add(self.layout())
        layout = QVBoxLayout()
        layout.addWidget(self.mesh_info)
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.nodes_actor = None
        self.faces_actor = None
        self.solids_actor = None
        self.edges_actor = None
        self.selection_spheres_actor = None

        self.create_axes()
        self.update_plot()

    def update_plot(self):
        if self.main_window.project is None:
            return

        model = self.main_window.project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        self.update_theme()
        self.remove_actors()

        self.selection_spheres_actor = SelectionSpheres()
        self.selection_spheres_actor.GetProperty().SetColor([1, 0, 0])
        self.selection_spheres_actor.VisibilityOff()
        self.selection_spheres_actor.PickableOff()
        self.renderer.AddActor(self.selection_spheres_actor)

        self.nodes_actor = NodesActor(mesh)
        self.renderer.AddActor(self.nodes_actor)

        self.faces_actor = FacesActor(mesh)
        self.renderer.AddActor(self.faces_actor)

        self.solids_actor = SolidsActor(mesh)
        self.renderer.AddActor(self.solids_actor)

        self.edges_actor = EdgesActor(self.solids_actor.data)
        self.edges_actor.GetProperty().SetColor(0, 0, 0)
        self.renderer.AddActor(self.edges_actor)

        self.renderer.ResetCamera()
        self.show_faces()
        self.main_window.project.thumbnail = self.get_thumbnail()

    #
    def show_points(self):
        self.view_mode = SHOW_POINTS
        self.nodes_actor.VisibilityOn()
        self.edges_actor.VisibilityOff()
        self.faces_actor.VisibilityOff()
        self.solids_actor.VisibilityOff()
        self.update_theme()
        self.update()

    def show_lines(self):
        self.view_mode = SHOW_LINES
        self.nodes_actor.VisibilityOn()
        self.edges_actor.VisibilityOn()
        self.faces_actor.VisibilityOff()
        self.solids_actor.VisibilityOff()
        self.update_theme()
        self.update()

    def show_faces(self):
        self.view_mode = SHOW_FACES
        self.nodes_actor.VisibilityOn()
        self.edges_actor.VisibilityOn()
        self.faces_actor.VisibilityOn()
        self.solids_actor.VisibilityOff()
        self.edges_actor.GetProperty().SetColor(0, 0, 0)
        self.update_theme()
        self.update()
    
    def show_volumes(self):
        self.view_mode = SHOW_VOLUMES
        self.nodes_actor.VisibilityOn()
        self.edges_actor.VisibilityOn()
        self.faces_actor.VisibilityOff()
        self.solids_actor.VisibilityOn()
        self.edges_actor.GetProperty().SetColor(0, 0, 0)
        self.update_theme()
        self.update()

    def set_theme(self, theme):
        super().set_theme(theme)

        if not self._actors_exists():
            return

        light_color = (1, 1, 1)
        dark_color = (0, 0, 0)

        # It it is showing faces, the colors are fixed
        # otherwise it should follow the theme
        if self.view_mode in (SHOW_FACES, SHOW_VOLUMES):
            self.edges_actor.GetProperty().SetColor(dark_color)
            self.faces_actor.GetProperty().SetColor(light_color)
            self.solids_actor.GetProperty().SetColor(light_color)

        elif theme == "light":
            self.edges_actor.GetProperty().SetColor(dark_color)
            self.faces_actor.GetProperty().SetColor(dark_color)
            self.solids_actor.GetProperty().SetColor(dark_color)

        elif theme == "dark":
            self.edges_actor.GetProperty().SetColor(light_color)
            self.faces_actor.GetProperty().SetColor(light_color)
            self.solids_actor.GetProperty().SetColor(light_color)

    def selection_callback(self, x, y):
        if not self._actors_exists():
            return

        picker = vtk.vtkCellPicker()
        picker.Pick(x, y, 0, self.renderer)
        clicked_cell = picker.GetCellId()
        clicked_actor = picker.GetActor()
        mesh = app().main_window.project.model.mesh

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers & Qt.ControlModifier
        shift_pressed = modifiers & Qt.ShiftModifier
        alt_pressed = modifiers & Qt.AltModifier

        if clicked_actor == self.nodes_actor:
            app().main_window.set_mesh_selection(
                nodes=[clicked_cell],
                join=ctrl_pressed, remove=alt_pressed,
            )

        elif clicked_actor == self.edges_actor:
            line_entity = mesh.lines_connectivity[clicked_cell][1]
            app().main_window.set_mesh_selection(
                nodes=[clicked_cell],
                join=ctrl_pressed, remove=alt_pressed,
            )

        elif (clicked_actor == self.faces_actor):
            face_entity = mesh.faces_connectivity[clicked_cell][1]
            app().main_window.set_mesh_selection(
                faces=[clicked_cell],
                join=ctrl_pressed, remove=alt_pressed,
            )

        elif (clicked_actor == self.solids_actor) and shift_pressed:
            face_entity = self.main_window.project.model.mesh.faces_connectivity[clicked_cell][1]
            for (volume, surfaces) in self.main_window.project.model.mesh.surfaces_from_volumes.items():
                if face_entity in surfaces:
                    self.select_volume(volume, join=ctrl_pressed, remove=alt_pressed)
                    break

        else:
            self.clear_selection()
            self.selection_changed.emit(self.selected_points,
                                        self.selected_lines,
                                        self.selected_faces,
                                        self.selected_volumes)
    def update_selection(self):
        '''
        Update the visualization of selected data.
        '''
        if not self._actors_exists():
            return

        self.nodes_actor.clear_colors()
        self.faces_actor.clear_colors()
        self.solids_actor.clear_colors()

        nodes = app().main_window.selected_element_nodes
        faces = app().main_window.selected_element_faces
        solids = app().main_window.selected_element_solids

        self.nodes_actor.paint_cells([255, 0, 0], nodes)
        self.faces_actor.paint_cells(self.selection_color, faces)
        self.solids_actor.paint_cells(self.selection_color, solids)
        self.update()

    def select_multiple_nodes(self, new_nodes, *, join=False, remove=False):
        if not self._actors_exists():
            return
        self.nodes_actor.paint_cells([255, 0, 0], new_nodes)
        self.update()
        if self.view_mode != SHOW_FACES:
            self.show_points()

    def select_multiple_faces(self, new_faces, *, join=False, remove=False):
        if not self._actors_exists():
            return
        self.faces_actor.paint_cells(self.selection_color, new_faces)
        self.update()
        self.show_faces()

    def select_multiple_volumes(self, new_volumes, *, join=False, remove=False):
        if not self._actors_exists():
            return
        self.solids_actor.paint_cells(self.selection_color, new_volumes)
        self.update()
        self.show_volumes()

    def clear_selection_spheres(self):
        if self.selection_spheres_actor is None:
            return
        self.selection_spheres_actor.VisibilityOff()

    def set_selection_spheres(self, all_centers, all_radius):
        if self.selection_spheres_actor is None:
            return
        self.selection_spheres_actor.create_geometry(all_centers, all_radius)
        self.selection_spheres_actor.VisibilityOn()
        self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.edges_actor)
        self.renderer.RemoveActor(self.faces_actor)
        self.renderer.RemoveActor(self.solids_actor)
        self.renderer.RemoveActor(self.selection_spheres_actor)
        self.edges_actor = None
        self.faces_actor = None
        self.solids_actor = None
        self.selection_spheres_actor = None

    def _actors_exists(self):
        actors = [self.solids_actor, self.faces_actor, self.edges_actor, self.selection_spheres_actor]
        return all([actor is not None for actor in actors])

    def _get_info_tab(self):
        pass
