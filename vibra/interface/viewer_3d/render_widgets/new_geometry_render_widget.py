from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from vibra.engine.model import Model
from vibra.interface.general.selection_handler import SelectionHandler
from vibra.interface.viewer_3d.actors.geometry_actor import GeometryActor
from vibra.interface.viewer_3d.actors.symbols_actor_acoustic import SymbolsActorAcoustic
from vibra.interface.viewer_3d.actors.symbols_actor_structural import SymbolsActorStructural
from vibra.interface.viewer_3d.render_widgets.vibra_render_widget import VibraRenderWidget
from vibra.utils.interface_utils import SectionPlane
from vibra.utils.time_utils import function_timer


class NewGeometryRenderWidget(VibraRenderWidget):
    def __init__(self):
        super().__init__()

        self.create_actors()

        self.left_clicked.connect(self.click_start_callback)
        self.left_released.connect(self.click_end_callback)

    def create_actors(self):
        self.create_common_actors()

        self.acoustic_symbols_actor = SymbolsActorAcoustic(self.model, self.renderer.GetActiveCamera())
        self.add_actors(self.acoustic_symbols_actor)

        self.structural_symbols_actor = SymbolsActorStructural(self.model, self.renderer.GetActiveCamera())
        self.add_actors(self.structural_symbols_actor)

        self.geometry_actor = GeometryActor(self.model)
        self.add_actors(self.geometry_actor)

    def set_model(self, model: Model | None):
        super().set_model(model)
        self.acoustic_symbols_actor.model = model
        self.structural_symbols_actor.model = model
        self.geometry_actor.model = model

    def set_section_plane(self, section_plane: SectionPlane | None):
        super().set_section_plane(section_plane)
        self.geometry_actor.section_plane = section_plane

    @function_timer
    def update_plot(self, reset_camera: bool = False):
        if self.isVisible():
            self._must_update = False
        else:
            self._must_update = True
            return

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

        if self.entity_visibility_handler is not None:
            self.geometry_actor.hide_surfaces()
            self.geometry_actor.show_surfaces(self.entity_visibility_handler.get_visible_surfaces())

        self.geometry_actor.update_caches()
        self.render()

    def click_end_callback(self, x1: int, y1: int):
        # TODO: move this method to the tools
        mouse_moved = self.mouse_moved(x1, y1)

        if mouse_moved:
            selection = self.area_pick(self._last_click_position[0], self._last_click_position[1], x1, y1)
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
