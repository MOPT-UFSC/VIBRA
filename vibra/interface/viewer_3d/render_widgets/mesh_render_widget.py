from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import vtk

from molde.render_widgets import CommonRenderWidget

from vibra.interface.tabs.mesh_info_bar import MeshInfoBar
from vibra.interface.viewer_3d.actors.nodes_actor import NodesActor
from vibra.interface.viewer_3d.actors.edges_actor import EdgesActor
from vibra.interface.viewer_3d.actors.faces_actor import FacesActor
from vibra.interface.viewer_3d.actors.solids_actor import SolidsActor
from vibra.interface.viewer_3d.actors.cutting_plane_actor import CuttingPlaneActor
from vibra.utils.interface_functions import get_main_window
from vibra.interface.viewer_3d.actors.selection_spheres import SelectionSpheres
from vibra import app
from molde.utils.format_sequences import format_long_sequence

SHOW_POINTS = 0
SHOW_LINES = 1
SHOW_FACES = 2
SHOW_VOLUMES = 3


class MeshRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal(list, list, list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mouse_click = (0, 0)

        self.main_window = app().main_window
        self.view_mode = SHOW_FACES
        self.selection_color = (20, 106, 245)

        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        self.main_window.selection_changed.connect(self.update_selection)

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
        self.plane_actor = None

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

        self.plane_actor = CuttingPlaneActor(self.solids_actor.GetBounds())
        self.plane_actor.VisibilityOff()
        self.renderer.AddActor(self.plane_actor)

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
        self.update()

    def show_lines(self):
        self.view_mode = SHOW_LINES
        self.nodes_actor.VisibilityOn()
        self.edges_actor.VisibilityOn()
        self.faces_actor.VisibilityOff()
        self.solids_actor.VisibilityOff()
        self.update()

    def show_faces(self):
        self.view_mode = SHOW_FACES
        self.nodes_actor.VisibilityOn()
        self.edges_actor.VisibilityOn()
        self.faces_actor.VisibilityOn()
        self.solids_actor.VisibilityOff()
        self.edges_actor.GetProperty().SetColor(0, 0, 0)
        self.update()
    
    def show_volumes(self):
        self.view_mode = SHOW_VOLUMES
        self.nodes_actor.VisibilityOn()
        self.edges_actor.VisibilityOn()
        self.faces_actor.VisibilityOff()
        self.solids_actor.VisibilityOn()
        self.edges_actor.GetProperty().SetColor(0, 0, 0)
        self.update()

    def set_theme(self, theme):
        super().set_theme(theme)

        try:
            if not self._actors_exists():
                return
        except AttributeError:
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

    def click_callback(self, x, y):
        self.mouse_click = (x, y)

    def selection_callback(self, x, y):
        if not self._actors_exists():
            return

        # TODO: pick both nodes, faces and solids isolated
        # then select only get the closest to the camera
        cell_picker = vtk.vtkCellPicker()
        cell_picker.SetTolerance(0.002)

        cell_picker.Pick(x, y, 0, self.renderer)
        clicked_cell = cell_picker.GetCellId()
        clicked_actor = cell_picker.GetActor()

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers & Qt.ControlModifier
        shift_pressed = modifiers & Qt.ShiftModifier
        alt_pressed = modifiers & Qt.AltModifier

        if clicked_actor == self.nodes_actor:
            self.main_window.set_mesh_selection(
                nodes=[clicked_cell],
                join=ctrl_pressed, remove=alt_pressed,
            )

        elif clicked_actor == self.faces_actor:
            self.main_window.set_mesh_selection(
                faces=[clicked_cell],
                join=ctrl_pressed, remove=alt_pressed,
            )
        
        elif clicked_actor == self.solids_actor:
            self.main_window.set_mesh_selection(
                solids=[clicked_cell],
                join=ctrl_pressed, remove=alt_pressed,
            )
        else:
            self.main_window.set_mesh_selection(
                join=ctrl_pressed, remove=alt_pressed,
            )

    def _narrow_pickability_to_actor(self, target_actor: vtk.vtkActor):
        actor: vtk.vtkActor
        pickability = dict()
        for actor in self.renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            actor.SetPickable(actor == target_actor)
        return pickability 
    
    def _restore_pickability(self, pickability: dict):
        actor: vtk.vtkActor
        for actor in self.renderer.GetActors():
            actor.SetPickable(pickability[actor])

    def update_selection(self):
        '''
        Update the visualization of selected data.
        '''
        if not self._actors_exists():
            return
        
        self.update_selection_info()

        self.nodes_actor.clear_colors()
        self.faces_actor.clear_colors()
        self.solids_actor.clear_colors()

        nodes = self.main_window.selected_mesh_nodes
        faces = self.main_window.selected_mesh_faces
        solids = self.main_window.selected_mesh_solids

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
        self.renderer.RemoveActor(self.nodes_actor)
        self.renderer.RemoveActor(self.edges_actor)
        self.renderer.RemoveActor(self.faces_actor)
        self.renderer.RemoveActor(self.solids_actor)
        self.renderer.RemoveActor(self.nodes_actor)
        self.renderer.RemoveActor(self.selection_spheres_actor)
        self.renderer.RemoveActor(self.plane_actor)
        self.nodes_actor = None
        self.edges_actor = None
        self.faces_actor = None
        self.solids_actor = None
        self.selection_spheres_actor = None
        self.plane_actor = None
        self.nodes_actor = None

    def _actors_exists(self):
        actors = [self.solids_actor, self.faces_actor, self.edges_actor, self.selection_spheres_actor]
        return all([actor is not None for actor in actors])

    def _get_info_tab(self):
        pass

    def start_cutting_mode(self):
        if not self._actors_exists():
            return
        self.plane_actor.VisibilityOn()
        self.update()

    def stop_cutting_mode(self):
        if not self._actors_exists():
            return
        self.plane_actor.VisibilityOff()
        self.solids_actor.disable_cut()
        self.faces_actor.disable_cut()
        self.edges_actor.disable_cut()
        self.nodes_actor.disable_cut()
        self.update()

    def configure_cutting_plane(self, position, orientation):
        if not self._actors_exists():
            return

        self.plane_actor.configure_cutting_plane(position, orientation)
        self.update()

    def apply_cutting_plane(self, position, orientation):
        if not self._actors_exists():
            return

        xyz = self.plane_actor.calculate_x_y_z_position(position)
        normal = self.plane_actor.calculate_normal_vector(orientation)
        self.solids_actor.apply_cut(xyz, normal)
        self.faces_actor.apply_cut(xyz, normal)
        self.edges_actor.apply_cut(xyz, normal)
        self.nodes_actor.apply_cut(xyz, normal)

        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)

        self.update()
    
    def update_selection_info(self):
        text = ""
        text += self.nodes_info_text()
        text += self.faces_info_text()
        
        self.set_info_text(text)
    
    def nodes_info_text(self):
        nodes = list(self.main_window.selected_mesh_nodes)
        text = ""
        if len(nodes) > 1:
            text += (
                f"{len(nodes)} nodes in selection\n"
                f"{format_long_sequence(nodes)}\n\n"
            )
        elif len(nodes) == 1:
            text += f"Node: {nodes[0]}\n\n"

        return text

    def faces_info_text(self):
        faces = list(self.main_window.selected_mesh_faces)
        text = ""
        if len(faces) > 1:
            text += (
                f"{len(faces)} faces in selection\n"
                f"{format_long_sequence(faces)}\n\n"
            )
        elif len(faces) == 1:
            text += f"Face: {faces[0]}\n\n"
        
        return text

