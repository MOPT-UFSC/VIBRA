from molde import Color
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from vibra import app

from ..actors.edges_actor import EdgesActor
from ..actors.faces_actor import FacesActor
from ..actors.ghost_actor import GhostActor
from ..actors.hollow_solids_actor import HollowSolidsActor
from ..actors.nodes_actor import NodesActor
from ..actors.section_plane_actor import SectionPlaneActor
from ..actors.selection_spheres import SelectionSpheres
from ..actors.solids_actor import SolidsActor
from ..selection.mesh_selection import MeshSelection
from .model_info_text import (
    nodes_info_text,
    mesh_faces_info_text,
    mesh_solids_info_text,
    mesh_structural_boundary_conditions_info_text, 
)

import logging


class MeshRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_interactor_style(BoxSelectionInteractorStyle())

        self.mesh_selection = MeshSelection(self)
        self.selection_color = (20, 106, 245)
        self.mouse_click = (0, 0)

        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        app().main_window.theme_changed.connect(self.update_theme)
        app().main_window.visualization_filter_changed.connect(self.visualization_changed_callback)
        app().main_window.selection_changed.connect(self.update_selection)
        app().main_window.section_plane.value_changed.connect(self.update_section_plane)

        # The fast area selection just works if it is on
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.renderer.RemoveAllLights()

        self.remove_all_actors()
        self.create_axes()
        self.create_scale_bar()
        self.create_camera_light(0.1, 0.1)
        self.update_plot()

    def set_theme(self, *args, **kwargs):
        self.update_theme()

    def update_theme(self):
        user_preferences = app().config.user_preferences
        bkg_1 = user_preferences.renderer_background_color_1
        bkg_2 = user_preferences.renderer_background_color_2
        font_color = user_preferences.renderer_font_color

        if bkg_1 is None:
            raise ValueError('Missing value "bkg_1"')
        if bkg_2 is None:
            raise ValueError('Missing value "bkg_2"')
        if font_color is None:
            raise ValueError('Missing value "font_color"')

        self.renderer.GradientBackgroundOn()
        self.renderer.SetBackground(bkg_1.to_rgb_f())
        self.renderer.SetBackground2(bkg_2.to_rgb_f())

        if hasattr(self, "text_actor"):
            self.text_actor.GetTextProperty().SetColor(font_color.to_rgb_f())

        if hasattr(self, "scale_bar_actor"):
            self.scale_bar_actor.GetLegendTitleProperty().SetColor(font_color.to_rgb_f())
            self.scale_bar_actor.GetLegendLabelProperty().SetColor(font_color.to_rgb_f())

        self.update_selection()

    def update_scale_bar_visibility(self):
        user_preferences = app().config.user_preferences

        if user_preferences.show_reference_scale_bar:
            self.enable_scale_bar()
        else:
            self.disable_scale_bar()

    def enable_scale_bar(self):
        self.scale_bar_actor.VisibilityOn()

    def disable_scale_bar(self):
        self.scale_bar_actor.VisibilityOff()

    def update_renderer_font_size(self):
        user_preferences = app().config.user_preferences
        font_size_px = int(user_preferences.renderer_font_size * 4 / 3)

        info_text_property = self.text_actor.GetTextProperty()
        info_text_property.SetFontSize(font_size_px)

        scale_bar_title_property = self.scale_bar_actor.GetLegendTitleProperty()
        scale_bar_label_property = self.scale_bar_actor.GetLegendLabelProperty()
        scale_bar_title_property.SetFontSize(font_size_px)
        scale_bar_label_property.SetFontSize(font_size_px)

    def update_plot(self, reset_camera=True):
        mesh = app().project.model.mesh
        if mesh is None:
            return

        logging.info("Updating the mesh render... [25/100]")
        self.mesh_selection.precompute_data()
        self.remove_all_actors()

        # TODO: load the mesh directly inside the actors
        self.nodes_actor = NodesActor(mesh)
        self.faces_actor = FacesActor(mesh)
        self.solids_actor: SolidsActor | HollowSolidsActor = HollowSolidsActor(mesh)
        self.edges_actor = EdgesActor(self.solids_actor.data)
        self.selection_spheres_actor = SelectionSpheres()

        visualization = app().main_window.visualization_filter
        section_plane = app().main_window.section_plane
        has_hidden_part = bool(app().main_window.hidden_surfaces) or section_plane.cutting
        self.ghost_actor = GhostActor(mesh)
        self.ghost_actor.SetVisibility(visualization.ghost and has_hidden_part)

        self.plane_actor = SectionPlaneActor(self.faces_actor.GetBounds())
        self.plane_actor.VisibilityOff()

        logging.info("Updating the mesh render... [75/100]")
        self.add_actors(
            self.nodes_actor,
            self.edges_actor,
            self.faces_actor,
            self.solids_actor,
            self.ghost_actor,
            self.plane_actor,
        )

        with self.update_lock:
            self.update_theme()
            self.update_section_plane()
            self.visualization_changed_callback()

        if reset_camera:
            self.renderer.ResetCamera()

        logging.info("Updating the mesh render... [95/100]")
        self.update()

    def visualization_changed_callback(self):
        if not self.actors_exists():
            return

        visualization = app().main_window.visualization_filter
        section_plane = app().main_window.section_plane
        has_hidden_part = bool(app().main_window.hidden_surfaces) or section_plane.cutting

        # Nodes actor are always visible.
        # We hide them painting the cells as transparent.
        self.nodes_actor.SetVisibility(True)

        self.edges_actor.SetVisibility(visualization.lines)
        self.faces_actor.SetVisibility(visualization.faces)
        self.solids_actor.SetVisibility(visualization.solids)
        self.ghost_actor.SetVisibility(visualization.ghost and has_hidden_part)

        self.update_selection()
        self.update()
    
    def update_hidden_plot(self):
        self.update_plot(reset_camera=False)

    def click_callback(self, x, y):
        self.mouse_click = (x, y)

    def selection_callback(self, x, y):
        if not self.actors_exists():
            return

        section_plane_widget = app().main_window.section_plane
        if section_plane_widget.cutting:
            xyz = self.plane_actor.calculate_xyz_position(section_plane_widget.get_position())
            normal = self.plane_actor.calculate_normal_vector(section_plane_widget.get_rotation())
            if section_plane_widget.get_inverted():
                normal = -normal
            self.mesh_selection.set_section_plane(xyz, normal)            
        else:
            self.mesh_selection.clear_section_plane()

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)

        if mouse_moved:
            picked_nodes, picked_faces, picked_solids = self.mesh_selection.area_pick(x0, y0, x, y)
        else:
            picked_nodes, picked_faces, picked_solids = self.mesh_selection.pick(x, y)

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers & Qt.ControlModifier
        alt_pressed = modifiers & Qt.AltModifier

        app().main_window.set_mesh_selection(
            nodes=picked_nodes,
            faces=picked_faces,
            solids=picked_solids,
            join=ctrl_pressed,
            remove=alt_pressed,
        )

    def update_selection(self):
        """
        Update the visualization of selected data.
        """
        if not self.actors_exists():
            return

        self.update_info_text()
        visualization = app().main_window.visualization_filter

        # In this renderer the faces should be transparent
        # all the time, except when they are selected
        self.faces_actor.set_color(Color(0, 0, 0, 0))
        self.solids_actor.clear_colors()

        if visualization.points:
            self.nodes_actor.clear_colors()
        else:
            self.nodes_actor.set_color(Color(0, 0, 0, 0))

        nodes = app().main_window.selected_mesh_nodes
        faces = app().main_window.selected_mesh_faces
        solids = app().main_window.selected_mesh_solids
    
        selection_faces_color = app().config.user_preferences.selection_faces_color
        selection_nodes_points_color = app().config.user_preferences.selection_nodes_points_color

        self.nodes_actor.paint_cells(selection_nodes_points_color, nodes)
        self.faces_actor.paint_cells(selection_faces_color.apply_factor(1.4), faces)
        self.solids_actor.paint_cells(selection_faces_color, solids)
        self.edges_actor.configure_appearance()
        self.update()

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

    def remove_all_actors(self):
        super().remove_all_actors()
        self.nodes_actor = None
        self.edges_actor = None
        self.faces_actor = None
        self.solids_actor = None
        self.selection_spheres_actor = None
        self.plane_actor = None
        self.nodes_actor = None
        self.ghost_actor = None

    def actors_exists(self):
        return len(self._widget_actors) > 0

    def _get_info_tab(self):
        pass

    def update_section_plane(self):
        if not self.actors_exists():
            return

        section_plane = app().main_window.section_plane

        if not section_plane.cutting:
            self._disable_section_plane()
            return

        position = section_plane.get_position()
        rotation = section_plane.get_rotation()
        inverted = section_plane.get_inverted()

        if section_plane.editing:
            self.plane_actor.configure_section_plane(position, rotation)
            self.plane_actor.VisibilityOn()
            self.plane_actor.GetProperty().SetColor(0, 0.333, 0.867)
            self.plane_actor.GetProperty().SetOpacity(0.8)
            self.update()
        else:
            show_plane = not section_plane.keep_section_plane
            self._apply_section_plane(position, rotation, inverted, show_plane)

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True):
        if isinstance(self.solids_actor, HollowSolidsActor):
            mesh = app().project.model.mesh
            if mesh is None:
                return

            if mesh.solids_connectivity.size > 0:
                self.remove_actors(self.solids_actor, self.edges_actor)
                self.solids_actor = SolidsActor(mesh)
                self.edges_actor = EdgesActor(self.solids_actor.data)
                self.add_actors(self.solids_actor, self.edges_actor)

        self.plane_actor.configure_section_plane(position, rotation)
        xyz = self.plane_actor.calculate_xyz_position(position)
        normal = self.plane_actor.calculate_normal_vector(rotation)
        if inverted:
            normal = -normal

        self.nodes_actor.apply_cut(xyz, normal)
        self.faces_actor.apply_cut(xyz, normal)
        self.solids_actor.apply_cut(xyz, normal)
        self.edges_actor.apply_cut(xyz, normal)

        visualization = app().main_window.visualization_filter
        self.ghost_actor.SetVisibility(visualization.ghost)
        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.update()

    def _disable_section_plane(self):
        visualization = app().main_window.visualization_filter
        section_plane = app().main_window.section_plane
        has_hidden_part = bool(app().main_window.hidden_surfaces) or section_plane.cutting
        self.ghost_actor.SetVisibility(visualization.ghost and has_hidden_part)
        self.plane_actor.VisibilityOff()

        self.nodes_actor.disable_cut()
        self.faces_actor.disable_cut()
        self.solids_actor.disable_cut()
        self.edges_actor.disable_cut()
        self.update()

    def update_info_text(self):
        text = ""
        text += nodes_info_text()
        text += mesh_faces_info_text()
        text += mesh_solids_info_text()
        text += mesh_structural_boundary_conditions_info_text()

        self.set_info_text(text)
        self.update()

