import logging
from datetime import datetime

from molde import Color
from molde.render_widgets import CommonRenderWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from vibra import ICON_DIR, app
from vibra.utils.image_functions import removes_image_background
from vibra.utils.interface_utils import VisualizationFilter
from vibra.utils.time_utils import warn_delays

from ..actors.ghost_actor import GhostActor
from ..actors.lines_actor import LinesActor
from ..actors.multimaterial import MultimaterialGeometryActor
from ..actors.points_actor import PointsActor
from ..actors.section_plane_actor import SectionPlaneActor
from ..actors.selection_spheres import SelectionSpheres
from ..actors.symbols_actor_acoustic import SymbolsActorAcoustic
from ..actors.symbols_actor_acoustic_fixed_size import SymbolsActorAcousticFixedSize
from ..actors.symbols_actor_structural import SymbolsActorStructural
from ..render_tools.selection_tool import SelectionTool
from ..selection.geometry_selection import GeometrySelection
from .model_info_text import (
    acoustic_boundary_conditions_info_text,
    faces_info_text,
    fluid_info_text,
    lines_info_text,
    mass_source_info_text,
    material_info_text,
    perforated_plate_info_text,
    points_info_text,
    porous_material_info_text,
    proportional_damping_info_text,
    structural_boundary_conditions_info_text,
    viscous_thermal_info_text,
    volumes_info_text,
)


class GeometryRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.geometry_selection = GeometrySelection(self)
        self.mouse_click = (0, 0)
        self.last_click_time: datetime | None = None
        self.is_double_click = False

        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        app().main_window.selection.selection_changed.connect(self.update_selection)
        app().main_window.section_plane.value_changed.connect(self.update_section_plane)
        app().main_window.theme_changed.connect(self.update_theme)
        app().main_window.visualization_changed.connect(self.visualization_changed_callback)

        self.selection_faces_color = app().config.user_preferences.selection_faces_color
        self.selection_nodes_points_color = app().config.user_preferences.selection_nodes_points_color
        self.selection_lines_color = app().config.user_preferences.selection_lines_color

        self.set_default_render_tool()

        # The fast area selection just works if it is on
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.renderer.RemoveAllLights()
        self.renderer.UseFXAAOn()

        # dont't remove, transparency depends on it
        self.renderer.UseDepthPeelingOn()
        self.renderer.SetMaximumNumberOfPeels(1)
        self.renderer.SetOcclusionRatio(0.9)
        self.render_interactor.GetRenderWindow().SetMultiSamples(0)

        self.visualization_filter = VisualizationFilter(
            points=True,
            lines=True,
            faces=True,
            solids=True,
            symbols=True,
        )

        self.remove_all_actors()
        self.create_logos()
        self.create_axes()
        self.create_scale_bar()
        self.create_camera_light(0.1, 0.1)
        self.update_plot()

    def create_logos(self):
        if hasattr(self, "vibra_logo"):
            self.renderer.RemoveViewProp(self.vibra_logo)

        path = ICON_DIR / "logo_vibra_comp.png"
        self.vibra_logo = self.create_logo(path)
        self.vibra_logo.SetPosition(0.895, 0.91)
        self.vibra_logo.SetPosition2(0.10, 0.10)

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

        logging.info("Updating the geometry render... [25/100]")
        self.remove_all_actors()

        self.points_actor = PointsActor(mesh)
        self.lines_actor = LinesActor(mesh)
        self.multimaterial = MultimaterialGeometryActor(mesh, visualization_filter=self.visualization_filter)

        self.selection_spheres_actor = SelectionSpheres()
        self.symbols_actor_structural = SymbolsActorStructural(self.renderer)
        self.symbols_actor_acoustic = SymbolsActorAcoustic(self.renderer)
        self.symbols_actor_acoustic_fixed_size = SymbolsActorAcousticFixedSize(self.renderer)

        self.ghost_actor = GhostActor(mesh)
        self.ghost_actor.SetVisibility(app().main_window.has_hidden_part())

        self.plane_actor = SectionPlaneActor(self.ghost_actor.GetBounds())
        self.plane_actor.VisibilityOff()

        logging.info("Updating the geometry render... [75/100]")
        self.add_actors(
            self.points_actor,
            self.lines_actor,
            self.multimaterial,
            self.selection_spheres_actor,
            self.ghost_actor,
            self.plane_actor,
            self.symbols_actor_structural,
            self.symbols_actor_acoustic,
            self.symbols_actor_acoustic_fixed_size,
        )

        with self.update_lock:
            self.update_theme()
            self.update_section_plane()
            self.visualization_changed_callback()

        if reset_camera:
            self.renderer.ResetCamera()

        logging.info("Updating the geometry render... [95/100]")
        self.update()

        if app().project.model.thumbnail is None:
            self.save_thumbnail()

    @warn_delays
    def save_thumbnail(self):
        thumbnail = app().project.model.thumbnail

        self.render_interactor.GetRenderWindow().OffScreenRenderingOn()

        color = Color(247, 0, 255)
        self.renderer.SetBackground(color.to_rgb_f())
        self.renderer.SetBackground2(color.to_rgb_f())
        self.lines_actor.set_color(Color(0, 0, 0))

        self.disable_scale_bar()
        thumbnail = self.get_thumbnail()
        thumbnail = removes_image_background(thumbnail)
        app().project.set_thumbnail(thumbnail)

        if app().config.user_preferences.show_reference_scale_bar:
            self.enable_scale_bar()

        self.update_theme()
        self.render_interactor.GetRenderWindow().OffScreenRenderingOff()

    def visualization_changed_callback(self):
        if not self.actors_exists():
            return

        visualization = self.visualization_filter

        # It may happen that the analysis toolbar has not been created yet. If so, retrieve the analysis type and physical domain from the project
        try:
            physical_domain = app().main_window.analysis_toolbar.combo_box_physical_domain.currentText()
        except Exception:
            physical_domain = app().project.get_physical_domain()

        self.symbols_actor_structural.SetVisibility(visualization.symbols and (physical_domain == "Structural"))
        self.symbols_actor_acoustic.SetVisibility(visualization.symbols and (physical_domain == "Acoustic"))
        self.symbols_actor_acoustic_fixed_size.SetVisibility(visualization.symbols and (physical_domain == "Acoustic"))
        self.points_actor.SetVisibility(visualization.points)
        self.lines_actor.SetVisibility(visualization.lines)
        self.multimaterial.SetVisibility(visualization.faces)
        self.ghost_actor.SetVisibility(visualization.ghost and app().main_window.has_hidden_part())

        self.points_actor.SetPickable(visualization.faces)
        self.lines_actor.SetPickable(visualization.faces)
        self.multimaterial.SetPickable(visualization.faces)

        self.update_selection()
        self.update()

    def update_hidden_plot(self):
        # We could just call the update_plot function,
        # but this is much simpler and faster
        if app().project is None:
            return

        model = app().project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        if not self.actors_exists():
            self.update_plot()
            return

        visualization = self.visualization_filter
        self.ghost_actor.SetVisibility(visualization.ghost and app().main_window.has_hidden_part())

        self.remove_actors(self.multimaterial)
        self.multimaterial = MultimaterialGeometryActor(mesh, visualization_filter=self.visualization_filter)
        self.add_actors(self.multimaterial)

        self.update_selection()
        self.update_section_plane()

    def update_symbols(self):
        if not self.actors_exists():
            return

        # self.symbols_actor.build() should be enough
        # but for some reason that I can't understand
        # it causes segmentation fault
        self.remove_actors(self.symbols_actor_structural, self.symbols_actor_acoustic, self.symbols_actor_acoustic_fixed_size)
        self.symbols_actor_structural = SymbolsActorStructural(self.renderer)
        self.symbols_actor_acoustic = SymbolsActorAcoustic(self.renderer)
        self.symbols_actor_acoustic_fixed_size = SymbolsActorAcousticFixedSize(self.renderer)
        self.add_actors(self.symbols_actor_structural, self.symbols_actor_acoustic, self.symbols_actor_acoustic_fixed_size)
        self.visualization_changed_callback()
        self.update()

    #
    def click_callback(self, x, y):
        self.mouse_click = (x, y)

        self.is_double_click = False
        current_click_time = datetime.now()
        if self.last_click_time is not None:
            time_since_last_click = (current_click_time - self.last_click_time).total_seconds()
            self.is_double_click = time_since_last_click < 0.5
        self.last_click_time = current_click_time

    @warn_delays(0.2)  # this is already too much and should be optimized
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
            self.geometry_selection.set_section_plane(xyz, normal)
        else:
            self.geometry_selection.clear_section_plane()

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)

        if mouse_moved:
            (
                picked_points,
                picked_lines,
                picked_surfaces,
                picked_volumes,
            ) = self.geometry_selection.area_pick(x0, y0, x, y)

        else:
            (
                picked_points,
                picked_lines,
                picked_surfaces,
                picked_volumes,
            ) = self.geometry_selection.pick(x, y)

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers & Qt.ControlModifier
        shift_pressed = modifiers & Qt.ShiftModifier
        alt_pressed = modifiers & Qt.AltModifier
    
        select_volume = any([
            self.is_double_click,
            shift_pressed,
            app().main_window.selection.volume_selection_mode
        ])

        if select_volume:
            picked_surfaces.clear()
        else:
            picked_volumes.clear()

        app().main_window.selection.set_geometry_selection(
            points=picked_points,
            lines=picked_lines,
            surfaces=picked_surfaces,
            volumes=picked_volumes,
            join=ctrl_pressed,
            remove=alt_pressed,
        )

        self.update()

    def update_selection(self):
        if not self.actors_exists():
            return

        self.points_actor.clear_colors()
        self.lines_actor.clear_colors()
        self.multimaterial.clear_colors()

        points = app().main_window.selection.geometry_points
        lines = app().main_window.selection.geometry_lines
        surfaces = app().main_window.selection.geometry_surfaces | app().main_window.selection.surface_of_selected_volumes

        self.points_actor.paint_points(self.selection_nodes_points_color, points)
        self.lines_actor.paint_lines(self.selection_lines_color, lines)
        self.multimaterial.paint_surfaces(self.selection_faces_color, surfaces)

        self.selection_nodes_points_color = app().config.user_preferences.selection_nodes_points_color
        self.selection_faces_color = app().config.user_preferences.selection_faces_color
        self.selection_lines_color = app().config.user_preferences.selection_lines_color

        self.update_info_text()

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

    def _disable_section_plane(self):
        visualization = self.visualization_filter
        self.ghost_actor.SetVisibility(visualization.ghost and app().main_window.has_hidden_part())
        self.plane_actor.VisibilityOff()
        self.points_actor.disable_cut()
        self.lines_actor.disable_cut()
        self.multimaterial.disable_cut()
        self.update()

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True):
        self.plane_actor.configure_section_plane(position, rotation)
        xyz = self.plane_actor.calculate_xyz_position(position)
        normal = self.plane_actor.calculate_normal_vector(rotation)
        if inverted:
            normal = -normal

        self.points_actor.apply_cut(xyz, normal)
        self.multimaterial.apply_cut(xyz, normal)
        self.lines_actor.apply_cut(xyz, normal)

        visualization = self.visualization_filter
        self.ghost_actor.SetVisibility(visualization.ghost)
        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.update()

    def remove_all_actors(self):
        super().remove_all_actors()
        self.nodes_actor = None
        self.edges_actor = None
        self.multimaterial = None
        self.selection_spheres_actor = None
        self.plane_actor = None
        self.symbols_actor_structural = None
        self.symbols_actor_acoustic = None
        self.symbols_actor_acoustic_fixed_size = None
        self.nodes_actor = None
        self.ghost_actor = None

    def actors_exists(self):
        return len(self._widget_actors) > 0

    def get_analysis_type_and_physical_domain(self):
        try:
            analysis_toolbar = app().main_window.analysis_toolbar
            analysis_type = analysis_toolbar.combo_box_analysis_type.currentText()
            physical_domain = analysis_toolbar.combo_box_physical_domain.currentText()
        except Exception:
            analysis_type = app().project.get_analysis_type()
            physical_domain = app().project.get_physical_domain()

        analysis_type = analysis_type.lower()
        physical_domain = physical_domain.lower()

        return analysis_type, physical_domain

    @warn_delays
    def update_info_text(self):
        analysis_type, physical_domain = self.get_analysis_type_and_physical_domain()

        text = ""
        text += points_info_text()
        text += lines_info_text()
        text += faces_info_text()
        text += volumes_info_text()

        if physical_domain == "structural":
            text += material_info_text()
            text += structural_boundary_conditions_info_text()

        elif physical_domain == "acoustic":
            text += fluid_info_text()
            text += proportional_damping_info_text()
            text += porous_material_info_text()
            text += viscous_thermal_info_text()
            text += perforated_plate_info_text()
            text += acoustic_boundary_conditions_info_text()
            text += mass_source_info_text()

        self.set_info_text(text)
        self.update()

    def set_default_render_tool(self):
        tool = SelectionTool()
        self.set_interactor_style(tool)
        tool.update_mouse_cursor_in_render_widgets(tool.current_cursor)
