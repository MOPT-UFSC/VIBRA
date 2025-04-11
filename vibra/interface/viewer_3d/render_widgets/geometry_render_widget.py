import numpy as np
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget
from molde.utils import TreeInfo
from molde.utils.format_sequences import format_long_sequence
from molde import Color
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication

from vibra import app
from vibra.utils.image_functions import removes_image_background
from vibra.engine.properties.fluid import Fluid

from ..actors.faces_actor import FacesActor
from ..actors.ghost_actor import GhostActor
from ..actors.lines_actor import LinesActor
from ..actors.points_actor import PointsActor
from ..actors.section_plane_actor import SectionPlaneActor
from ..actors.selection_spheres import SelectionSpheres
from ..actors.symbols.new_symbols_actor import NewSymbolsActor
from ..selection.geometry_selection import GeometrySelection

from .model_info_text import( 
    points_info_text,
    lines_info_text, 
    faces_info_text, 
    volumes_info_text, 
    surface_thickness_info_text, 
    material_info_text, 
    fluid_info_text, 
    porous_material_info_text, 
    perforated_plate_info_text, 
    acoustic_boundary_conditions_info_text, 
    structural_boundary_conditions_info_text
)


class GeometryRenderWidget(CommonRenderWidget):
    selection_changed = Signal(set, set, set, set)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_interactor_style(BoxSelectionInteractorStyle())

        self.geometry_selection = GeometrySelection(self)
        self.selection_color = (20, 106, 245)
        self.mouse_click = (0, 0)

        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        app().main_window.selection_changed.connect(self.update_selection)
        app().main_window.section_plane.value_changed.connect(self.update_section_plane)
        app().main_window.theme_changed.connect(self.update_theme)
        app().main_window.visualization_changed.connect(self.visualization_changed_callback)

        self.geometry_selection = GeometrySelection(self)

        self.points_actor = None
        self.lines_actor = None
        self.faces_actor = None
        self.ghost_actor = None
        self.selection_spheres_actor = None
        self.selection_color = app().config.user_preferences.selection_color.to_rgb()

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

        self.remove_all_actors()

        self.points_actor = PointsActor(mesh)
        self.lines_actor = LinesActor(mesh)
        self.faces_actor = FacesActor(mesh)
        self.selection_spheres_actor = SelectionSpheres()
        self.symbols_actor = NewSymbolsActor(self.renderer)

        has_hidden_part = bool(app().main_window.hidden_surfaces)
        self.ghost_actor = GhostActor(mesh)
        self.ghost_actor.SetVisibility(has_hidden_part)

        self.plane_actor = SectionPlaneActor(self.faces_actor.GetBounds())
        self.plane_actor.VisibilityOff()

        self.add_actors(
            self.points_actor,
            self.lines_actor,
            self.faces_actor,
            self.selection_spheres_actor,
            self.ghost_actor,
            self.plane_actor,
            self.symbols_actor,
        )

        with self.update_lock:
            self.update_theme()
            self.visualization_changed_callback()
            self.update_section_plane()

        if reset_camera:
            self.renderer.ResetCamera()
        else:
            self.update()

        if app().project.thumbnail is None:
            self.save_thumbnail()
    
    def save_thumbnail(self):
        thumbnail = app().project.thumbnail

        if not self.isVisible():
            return

        self.render_interactor.GetRenderWindow().OffScreenRenderingOn()

        color = Color(247, 0, 255)
        self.renderer.SetBackground(color.to_rgb_f())
        self.renderer.SetBackground2(color.to_rgb_f())
        self.faces_actor.set_color((255, 255, 255))
        self.lines_actor.set_color(Color(0, 0, 0))

        self.disable_scale_bar()
        thumbnail = self.get_thumbnail()
        app().project.thumbnail = removes_image_background(thumbnail)
        
        if app().config.user_preferences.show_reference_scale_bar:
            self.enable_scale_bar()

        self.update_theme()
        self.render_interactor.GetRenderWindow().OffScreenRenderingOff()

    def visualization_changed_callback(self):
        if not self.actors_exists():
            return

        visualization = app().main_window.visualization_filter
        faces_opacity = 1 if visualization.faces else 0.1

        self.symbols_actor.SetVisibility(
            visualization.acoustic_symbols | visualization.structural_symbols
        )
        self.points_actor.SetVisibility(visualization.points)
        self.lines_actor.SetVisibility(visualization.lines)
        self.faces_actor.GetProperty().SetOpacity(faces_opacity)

        self.points_actor.SetPickable(visualization.faces)
        self.lines_actor.SetPickable(visualization.faces)
        self.faces_actor.SetPickable(visualization.faces)
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

        self.renderer.RemoveActor(self.faces_actor)
        self.faces_actor = FacesActor(mesh)
        self.renderer.AddActor(self.faces_actor)

        has_hidden_part = bool(app().main_window.hidden_surfaces)
        self.ghost_actor.SetVisibility(has_hidden_part)

        self.update_section_plane()
        # self.update()

    def update_symbols(self):
        if not self.actors_exists():
            return
        self.symbols_actor.build()

    #
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
            self.geometry_selection.set_section_plane(xyz, normal)
        else:
            self.geometry_selection.clear_section_plane()

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)

        if mouse_moved:
            (
                picked_points,
                picked_lines,
                picked_faces,
                picked_volumes,
            ) = self.geometry_selection.area_pick(x0, y0, x, y)

        else:
            (
                picked_points,
                picked_lines,
                picked_faces,
                picked_volumes,
            ) = self.geometry_selection.pick(x, y)

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers & Qt.ControlModifier
        shift_pressed = modifiers & Qt.ShiftModifier
        alt_pressed = modifiers & Qt.AltModifier

        if not shift_pressed:
            picked_volumes.clear()

        app().main_window.set_geometry_selection(
            points=picked_points,
            lines=picked_lines,
            surfaces=picked_faces,
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
        self.faces_actor.clear_colors()

        points = app().main_window.selected_geometry_points
        lines = app().main_window.selected_geometry_lines
        faces = app().main_window.selected_geometry_surfaces
        volumes = app().main_window.selected_geometry_volumes

        mesh = app().project.model.mesh

        # the cells are 0-indexed
        # but the points are 1-indexed
        point_cells = {i - 1 for i in points}

        all_faces_elements = list()
        # Get the face elements of all selected faces
        for face in faces:
            indexes = mesh.elements_from_surface.get(face, [])
            all_faces_elements.extend(indexes)

        # Get the face elements of all selected volumes
        for volume in volumes:
            surfaces = app().project.model.mesh.surfaces_from_volumes[volume]
            for face in surfaces:
                indexes = app().project.model.mesh.elements_from_surface.get(face, [])
                all_faces_elements.extend(indexes)

        self.points_actor.paint_cells(self.selection_color, point_cells)
        self.lines_actor.paint_lines(self.selection_color, lines)
        self.faces_actor.paint_cells(self.selection_color, all_faces_elements)
        self.selection_color = app().config.user_preferences.selection_color.to_rgb()

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
        has_hidden_part = bool(app().main_window.hidden_surfaces)
        self.ghost_actor.SetVisibility(has_hidden_part)
        self.plane_actor.VisibilityOff()
        self.points_actor.disable_cut()
        self.lines_actor.disable_cut()
        self.faces_actor.disable_cut()
        self.update()

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True):
        self.plane_actor.configure_section_plane(position, rotation)
        xyz = self.plane_actor.calculate_xyz_position(position)
        normal = self.plane_actor.calculate_normal_vector(rotation)
        if inverted:
            normal = -normal

        self.points_actor.apply_cut(xyz, normal)
        self.faces_actor.apply_cut(xyz, normal)
        self.lines_actor.apply_cut(xyz, normal)

        self.ghost_actor.VisibilityOn()
        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.update()

    def remove_all_actors(self):
        super().remove_all_actors()
        self.nodes_actor = None
        self.edges_actor = None
        self.faces_actor = None
        self.solids_actor = None
        self.selection_spheres_actor = None
        self.plane_actor = None
        self.symbols_actor = None
        self.nodes_actor = None
        self.ghost_actor = None

    def actors_exists(self):
        return len(self._widget_actors) > 0

    def update_info_text(self):
        text = ""
        text += points_info_text()
        text += lines_info_text()
        text += faces_info_text()
        text += volumes_info_text()
        text += surface_thickness_info_text()
        text += material_info_text()
        text += fluid_info_text()
        text += porous_material_info_text()
        text += perforated_plate_info_text()
        text += acoustic_boundary_conditions_info_text()
        text += structural_boundary_conditions_info_text()

        self.set_info_text(text)
        self.update()
