from vibra.utils.time_utils import warn_delays
import logging

from molde.colors import Color, color_names
from molde.render_widgets import CommonRenderWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from vibra import LOGO_DIR, app
from vibra.interface.loading_window import LoadingWindow
from vibra.utils.interface_utils import VisualizationFilter

from ..actors.edges_actor import EdgesActor
from ..actors.faces_actor import FacesActor
from ..actors.ghost_actor import GhostActor
from ..actors.hollow_solids_actor import HollowSolidsActor
from ..actors.legend_actor import LegendActor
from ..actors.nodes_actor import NodesActor
from ..actors.section_plane_actor import SectionPlaneActor
from ..actors.selection_spheres import SelectionSpheres
from ..actors.solids_actor import SolidsActor
from ..render_tools.selection_tool import SelectionTool
from ..selection.mesh_selection import MeshSelection
from .model_info_text import (
    mesh_faces_info_text,
    mesh_solids_info_text,
    mesh_structural_boundary_conditions_info_text,
    nodes_info_text,
)


class MeshRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.visualization_filter = VisualizationFilter(
            lines=True,
            faces=True,
            solids=True,
            symbols=True,
        )

        self.mesh_selection = MeshSelection(self)
        self.selection_color = (20, 106, 245)
        self.mouse_click = (0, 0)

        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        app().main_window.theme_changed.connect(self.update_theme)
        app().main_window.visualization_changed.connect(self.visualization_changed_callback)
        app().main_window.selection.selection_changed.connect(self.update_selection)
        app().main_window.section_plane.value_changed.connect(self.update_section_plane)

        # The fast area selection just works if it is on
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.renderer.RemoveAllLights()

        self.set_default_render_tool()
        self.remove_all_actors()
        self.create_axes()
        self.update_logo()
        self.create_scale_bar()
        self.create_camera_light(0.1, 0.1)
        self.update_plot()

        self.bad_elements_plot = False

    def showEvent(self, event):
        super().showEvent(event)
        self.update_section_plane()

    def update_logo(self):
        if hasattr(self, "vibra_logo"):
            self.renderer.RemoveViewProp(self.vibra_logo)

        path = LOGO_DIR / self.get_logo_for_current_theme()
        self.vibra_logo = self.create_logo(path)
        self.vibra_logo.SetPosition(0.895, 0.91)
        self.vibra_logo.SetPosition2(0.10, 0.10)

    def get_logo_for_current_theme(self) -> str:
        if app().config.user_preferences.interface_theme == "light":
            return "vibra_colored_light_background.png"
        
        
        return "vibra_colored_dark_background.png"
    
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
        self.update_logo()

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
        self.nodes_actor = NodesActor(mesh, visualization_filter=self.visualization_filter)
        self.faces_actor = FacesActor(mesh, visualization_filter=self.visualization_filter)
        self.solids_actor: SolidsActor | HollowSolidsActor = HollowSolidsActor(mesh)
        self.edges_actor = EdgesActor(
            self.solids_actor.data,
            visualization_filter=self.visualization_filter,
        )
        self.selection_spheres_actor = SelectionSpheres()

        # Create empty variables to be used when switching actors
        self._cache_hollow_solids_actor: HollowSolidsActor | None = self.solids_actor
        self._cache_full_solids_actor: SolidsActor | None = None

        visualization = self.visualization_filter
        self.ghost_actor = GhostActor(mesh)
        self.ghost_actor.SetVisibility(visualization.ghost and app().main_window.has_hidden_part())

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

        # Nodes actor are always visible.
        # We hide them painting the cells as transparent.
        self.nodes_actor.SetVisibility(True)

        mesh = app().project.model.mesh
        mesh_error = mesh.collapsed_elements_data or mesh.disconnected_nodes_data
        distinguished_solids = app().main_window.distinguished_solids

        visualization = self.visualization_filter
        self.edges_actor.SetVisibility(visualization.lines and not distinguished_solids)
        self.faces_actor.SetVisibility(visualization.faces and not mesh_error)
        self.solids_actor.SetVisibility(visualization.solids and not mesh_error)
        self.faces_actor.SetVisibility(visualization.faces and not mesh_error)
        self.ghost_actor.SetVisibility(visualization.ghost and app().main_window.has_hidden_part())

        if distinguished_solids:
            self.switch_to_solids_actor()
            self.solids_actor.distinguish_solids(distinguished_solids)
            self.solids_actor.SetVisibility(True)

        self.update_selection()
        self.update()

    def update_hidden_plot(self):
        self.update_plot(reset_camera=False)

    def click_callback(self, x, y):
        self.mouse_click = (x, y)

    @warn_delays(0.2)
    def selection_callback(self, x, y):
        if not self.actors_exists():
            return

        if not isinstance(self.interactor_style, SelectionTool):
            return

        if not self.interactor_style.is_selecting:
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

        app().main_window.selection.set_mesh_selection(
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

        # In this renderer the faces should be transparent
        # all the time, except when they are selected
        self.faces_actor.set_color(Color(0, 0, 0, 0))
        self.solids_actor.clear_colors()
        self.nodes_actor.clear_colors()

        nodes = app().main_window.selection.mesh_nodes
        faces = app().main_window.selection.mesh_faces
        solids = app().main_window.selection.mesh_solids

        selection_faces_color = app().config.user_preferences.selection_faces_color
        selection_nodes_points_color = app().config.user_preferences.selection_nodes_points_color

        self.nodes_actor.paint_nodes(selection_nodes_points_color, nodes)
        self.faces_actor.paint_cells(selection_faces_color.apply_factor(1.4), faces)
        self.solids_actor.paint_solids(selection_faces_color, solids)
        self.edges_actor.configure_appearance()

        mesh = app().project.model.mesh
        mesh_error = mesh.collapsed_elements_data or mesh.disconnected_nodes_data
        if mesh_error:
            self.add_problematic_mesh_legend()

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

    def switch_to_hollow_actor(self):
        if not isinstance(self.solids_actor, SolidsActor):
            return

        mesh = app().project.model.mesh
        if mesh is None:
            return

        if not isinstance(self._cache_hollow_solids_actor, HollowSolidsActor):
            self._cache_hollow_solids_actor = HollowSolidsActor(mesh)

        self._cache_full_solids_actor = self.solids_actor

        self.remove_actors(self.solids_actor, self.edges_actor)
        self.solids_actor = self._cache_hollow_solids_actor
        self.edges_actor = EdgesActor(
            self.solids_actor.data,
            visualization_filter=self.visualization_filter,
        )
        self.add_actors(self.solids_actor, self.edges_actor)
        self.visualization_changed_callback()

    def switch_to_solids_actor(self):
        if not isinstance(self.solids_actor, HollowSolidsActor):
            return

        mesh = app().project.model.mesh
        if mesh is None:
            return

        if not mesh.are_there_volumes_in_geometry():
            return

        if not isinstance(self._cache_full_solids_actor, SolidsActor):
            self._cache_full_solids_actor = SolidsActor(mesh)

        self._cache_hollow_solids_actor = self.solids_actor

        self.remove_actors(self.solids_actor, self.edges_actor)
        self.solids_actor = self._cache_full_solids_actor
        self.edges_actor = EdgesActor(
            self.solids_actor.data,
            visualization_filter=self.visualization_filter,
        )
        self.add_actors(self.solids_actor, self.edges_actor)
        self.visualization_changed_callback()

    def update_section_plane(self):
        if not self.actors_exists():
            return

        if not self.isVisible():
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
            LoadingWindow(self._apply_section_plane).run(
                position,
                rotation,
                inverted,
                show_plane,
            )

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True):
        logging.info("Switching to solid actor... [50/100]")
        self.switch_to_solids_actor()

        logging.info("Configuring section plane... [60/100]")
        xyz, normal = self.plane_actor.configure_section_plane(position, rotation)
        if inverted:
            normal = -normal

        logging.info("Applying cut... [70/100]")
        self.nodes_actor.apply_cut(xyz, normal)
        self.faces_actor.apply_cut(xyz, normal)
        self.solids_actor.apply_cut(xyz, normal)
        self.edges_actor.apply_cut(xyz, normal)

        logging.info("Updating visualization... [80/100]")
        visualization = self.visualization_filter
        self.ghost_actor.SetVisibility(visualization.ghost)
        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)

        logging.info("Updating... [99/100]")
        self.update()

    def _disable_section_plane(self):
        visualization = self.visualization_filter
        self.ghost_actor.SetVisibility(visualization.ghost and app().main_window.has_hidden_part())
        self.plane_actor.VisibilityOff()

        self.nodes_actor.disable_cut()
        self.faces_actor.disable_cut()
        self.solids_actor.disable_cut()
        self.edges_actor.disable_cut()

        self.switch_to_hollow_actor()
        self.update()

    def update_info_text(self):
        text = ""
        text += nodes_info_text()
        text += mesh_faces_info_text()
        text += mesh_solids_info_text()
        text += mesh_structural_boundary_conditions_info_text()

        self.set_info_text(text)
        self.update()

    def add_problematic_mesh_legend(self):
        legend_actor = LegendActor()

        if app().project.model.mesh.disconnected_nodes_data:
            legend_actor.add_item("Disconnected nodes", color_names.GREEN)

        if app().project.model.mesh.collapsed_elements_data:
            legend_actor.add_item("Collapsed element nodes", color_names.ORANGE)

        self.add_actors(legend_actor)

    def set_default_render_tool(self):
        tool = SelectionTool()
        self.set_interactor_style(tool)
        tool.update_mouse_cursor_in_render_widgets(tool.current_cursor)
