from datetime import datetime

import numpy as np
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from vibra.engine.model import Model
from vibra.interface.general.selection_handler import SelectionHandler
from vibra.interface.user_preferences import UserPreferences
from vibra.interface.viewer_3d.actors.geometry_actor import GeometryActor
from vibra.interface.viewer_3d.actors.symbols_actor_acoustic import SymbolsActorAcoustic
from vibra.interface.viewer_3d.actors.symbols_actor_structural import SymbolsActorStructural
from vibra.interface.viewer_3d.render_tools.selection_tool import SelectionTool
from vibra.utils.interface_utils import SectionPlane, VisualizationFilter
from vibra.utils.time_utils import function_timer


class NewGeometryRenderWidget(CommonRenderWidget):
    def __init__(self):
        super().__init__()
        self.set_interactor_style(BoxSelectionInteractorStyle())

        self.model: Model | None = None
        self.section_plane: SectionPlane | None = None
        self.user_preferences = UserPreferences()
        self.visualization_filter = VisualizationFilter(faces=True, symbols=True)
        self.selection_handler: SelectionHandler | None = None

        self._last_click_time = None
        self._last_click_position = (0, 0)
        self._is_double_click = False

        self.create_actors()

        self.left_clicked.connect(self.click_start_callback)
        self.left_released.connect(self.click_end_callback)

    def create_actors(self):
        self.create_axes()
        self.create_scale_bar()

        self.acoustic_symbols_actor = SymbolsActorAcoustic(self.model, self.renderer.GetActiveCamera())
        self.add_actors(self.acoustic_symbols_actor)

        self.structural_symbols_actor = SymbolsActorStructural(self.model, self.renderer.GetActiveCamera())
        self.add_actors(self.structural_symbols_actor)

        self.geometry_actor = GeometryActor(self.model)
        self.add_actors(self.geometry_actor)

    def set_model(self, model: Model | None):
        self.model = model
        self.acoustic_symbols_actor.model = model
        self.structural_symbols_actor.model = model
        self.geometry_actor.model = model

    def set_section_plane(self, section_plane: SectionPlane | None):
        self.section_plane = section_plane
        self.geometry_actor.section_plane = section_plane

    def set_visualization_filter(self, visualization_filter: VisualizationFilter | None):
        if visualization_filter is None:
            visualization_filter = VisualizationFilter(faces=True, symbols=True)
        self.visualization_filter = visualization_filter

    def set_selection_handler(self, selection_handler: SelectionHandler | None):
        self.selection_handler = selection_handler

    def set_user_preferences(self, user_preferences: UserPreferences | None):
        if user_preferences is None:
            user_preferences = UserPreferences()
        self.user_preferences = user_preferences

    @function_timer
    def update_plot(self, reset_camera: bool = False):
        self.geometry_actor.update()
        self.acoustic_symbols_actor.build()
        self.structural_symbols_actor.build()

        self.update_visualization()

        if reset_camera:
            self.renderer.ResetCamera()

        self.render()

    @function_timer
    def update_visualization(self):
        self.renderer.SetBackground(self.user_preferences.renderer_background_color_1.to_rgb_f())
        self.renderer.SetBackground2(self.user_preferences.renderer_background_color_2.to_rgb_f())

        self.geometry_actor.set_point_color(self.user_preferences.nodes_points_color)
        self.geometry_actor.set_line_color(self.user_preferences.lines_color)
        self.geometry_actor.set_surface_color(self.user_preferences.faces_color)

        self.geometry_actor.set_point_size(self.user_preferences.points_size)
        self.geometry_actor.set_line_thickness(self.user_preferences.lines_thickness)

        self.geometry_actor.set_points_visibility(visible=self.visualization_filter.points)
        self.geometry_actor.set_lines_visibility(visible=self.visualization_filter.lines)
        self.geometry_actor.set_surfaces_visibility(visible=self.visualization_filter.faces)

        if self.selection_handler is not None:
            self.geometry_actor.paint_volumes(
                self.user_preferences.selection_volumes_color,
                self.selection_handler.geometry_volumes,
            )
            self.geometry_actor.paint_surfaces(
                self.user_preferences.selection_faces_color,
                self.selection_handler.geometry_surfaces,
            )
            self.geometry_actor.paint_lines(
                self.user_preferences.selection_lines_color,
                self.selection_handler.geometry_lines,
            )
            self.geometry_actor.paint_points(
                self.user_preferences.selection_nodes_points_color,
                self.selection_handler.geometry_points,
            )

        self.geometry_actor.update_caches()
        self.render()

    def click_start_callback(self, x0: int, y0: int):
        click_position = (x0, y0)
        click_time = datetime.now()
        self._is_double_click = False

        if self._last_click_time is not None:
            time_since_last_click = (click_time - self._last_click_time).total_seconds()

            x1, y1 = self._last_click_position
            moved_x = abs(x0 - x1) > self.user_preferences.click_dist_tolerance
            moved_y = abs(y0 - y1) > self.user_preferences.click_dist_tolerance
            mouse_moved = moved_x or moved_y

            self._is_double_click = (time_since_last_click < self.user_preferences.click_time_tolerance) and not mouse_moved

        self._last_click_time = click_time
        self._last_click_position = click_position

    def click_end_callback(self, x1: int, y1: int):
        # TODO: move this method to the tools

        x0, y0 = self._last_click_position
        moved_x = abs(x0 - x1) > self.user_preferences.click_dist_tolerance
        moved_y = abs(y0 - y1) > self.user_preferences.click_dist_tolerance
        mouse_moved = moved_x or moved_y

        if mouse_moved:
            selection = self.area_pick(x0, y0, x1, y1)
        else:
            selection = self.pick(x1, y1)

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers & Qt.KeyboardModifier.ControlModifier
        shift_pressed = modifiers & Qt.KeyboardModifier.ShiftModifier
        alt_pressed = modifiers & Qt.KeyboardModifier.AltModifier

        select_volume = any([self._is_double_click, shift_pressed, self.selection_handler.volume_selection_mode])
        if select_volume:
            selection.geometry_surfaces.clear()
        else:
            selection.geometry_volumes.clear()

        self.selection_handler.update_from(
            selection,
            join=ctrl_pressed,
            remove=alt_pressed,
        )

    def pick(self, x: int, y: int) -> SelectionHandler:
        return self.geometry_actor.pick(x, y, self.renderer)

    def area_pick(self, x0: int, y0: int, x1: int, y1: int) -> SelectionHandler:
        return self.geometry_actor.area_pick(x0, y0, x1, y1, self.renderer)

    def render(self):
        # render is a better name for this action
        # I will update it later inside Molde
        self.update()
