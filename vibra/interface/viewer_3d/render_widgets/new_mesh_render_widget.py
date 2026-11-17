from datetime import datetime

from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from vibra.engine.model import Model
from vibra.interface.general.entity_visibility_handler import EntityVisibilityHandler
from vibra.interface.general.selection_handler import SelectionHandler
from vibra.interface.user_preferences import UserPreferences
from vibra.interface.viewer_3d.actors.mesh_actor import MeshActor
from vibra.utils.interface_utils import SectionPlane, VisualizationFilter
from vibra.utils.time_utils import function_timer


class NewMeshRenderWidget(CommonRenderWidget):
    def __init__(self):
        super().__init__()
        self.set_interactor_style(BoxSelectionInteractorStyle())

        self.model: Model | None = None
        self.section_plane: SectionPlane | None = None
        self.user_preferences = UserPreferences()
        self.visualization_filter = VisualizationFilter(faces=True, symbols=True)
        self.selection_handler: SelectionHandler | None = None
        self.entity_visibility_handler: EntityVisibilityHandler | None = None

        self._last_click_time = None
        self._last_click_position = (0, 0)
        self._is_double_click = False
        self._must_update = False

        self.create_actors()

        self.left_clicked.connect(self.click_start_callback)
        self.left_released.connect(self.click_end_callback)

    def create_actors(self):
        self.create_axes()
        self.create_scale_bar()

        self.mesh_actor = MeshActor(self.model)
        self.add_actors(self.mesh_actor)

    def set_model(self, model: Model | None):
        self.model = model
        self.mesh_actor.model = model

    def set_section_plane(self, section_plane: SectionPlane | None):
        self.section_plane = section_plane
        self.mesh_actor.section_plane = section_plane

    def set_visualization_filter(self, visualization_filter: VisualizationFilter | None):
        if visualization_filter is None:
            visualization_filter = VisualizationFilter(faces=True, symbols=True)
        self.visualization_filter = visualization_filter

    def set_selection_handler(self, selection_handler: SelectionHandler | None):
        self.selection_handler = selection_handler

    def set_entity_visibility_handler(self, entity_visibility_handler: EntityVisibilityHandler | None):
        self.entity_visibility_handler = entity_visibility_handler

    def set_user_preferences(self, user_preferences: UserPreferences | None):
        if user_preferences is None:
            user_preferences = UserPreferences()
        self.user_preferences = user_preferences

    @function_timer
    def update_plot(self, reset_camera: bool = False):
        if self.isVisible():
            self._must_update = False
        else:
            self._must_update = True
            return

        self.mesh_actor.update()

        self.update_visualization()

        if reset_camera:
            self.renderer.ResetCamera()

        self.render()

    @function_timer
    def update_visualization(self):
        self.renderer.SetBackground(self.user_preferences.renderer_background_color_1.to_rgb_f())
        self.renderer.SetBackground2(self.user_preferences.renderer_background_color_2.to_rgb_f())

        self.mesh_actor.set_node_color(self.user_preferences.nodes_points_color)
        self.mesh_actor.set_edge_color(self.user_preferences.edges_color)
        self.mesh_actor.set_surface_color(self.user_preferences.faces_color)
        self.mesh_actor.set_volume_color(self.user_preferences.volumes_color)

        self.mesh_actor.set_nodes_size(self.user_preferences.nodes_size)
        self.mesh_actor.set_edge_thickness(self.user_preferences.edges_thickness)

        self.mesh_actor.set_nodes_visibility(visible=self.visualization_filter.points)
        self.mesh_actor.set_edges_visibility(visible=self.visualization_filter.lines)
        self.mesh_actor.set_surfaces_visibility(visible=self.visualization_filter.faces)
        self.mesh_actor.set_solids_visibility(visible=self.visualization_filter.faces)

        if self.selection_handler is not None:
            self.mesh_actor.paint_solid_elements(
                self.user_preferences.selection_volumes_color,
                self.selection_handler.mesh_solids,
            )
            self.mesh_actor.paint_face_elements(
                self.user_preferences.selection_faces_color,
                self.selection_handler.mesh_faces,
            )
            self.mesh_actor.paint_nodes(
                self.user_preferences.selection_nodes_points_color,
                self.selection_handler.mesh_nodes,
            )
            self.mesh_actor.paint_volumes(
                self.user_preferences.selection_volumes_color,
                self.selection_handler.geometry_volumes,
            )
            self.mesh_actor.paint_surfaces(
                self.user_preferences.selection_faces_color,
                self.selection_handler.geometry_surfaces,
            )
            self.mesh_actor.paint_nodes(
                self.user_preferences.selection_nodes_points_color,
                self.selection_handler.geometry_points,
            )

        if self.entity_visibility_handler is not None:
            self.mesh_actor.hide_volumes()
            self.mesh_actor.show_volumes(self.entity_visibility_handler.get_visible_volumes())
            self.mesh_actor.hide_surfaces(self.entity_visibility_handler.get_hidden_surfaces())

        self.mesh_actor.update_caches()
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
        alt_pressed = modifiers & Qt.KeyboardModifier.AltModifier

        self.selection_handler.update_from(
            selection,
            join=ctrl_pressed,
            remove=alt_pressed,
        )

    def pick(self, x: int, y: int) -> SelectionHandler:
        picked = self.mesh_actor.pick(x, y, self.renderer)

        selection = SelectionHandler(self.model)
        selection.set_mesh_selection(
            nodes=picked.picked_nodes,
            faces=picked.picked_faces,
            solids=picked.picked_solids,
        )
        return selection

    def area_pick(self, x0: int, y0: int, x1: int, y1: int) -> SelectionHandler:
        picked = self.mesh_actor.area_pick(x0, y0, x1, y1, self.renderer)

        selection = SelectionHandler(self.model)
        selection.set_mesh_selection(
            nodes=picked.picked_nodes,
            faces=picked.picked_faces,
            solids=picked.picked_solids,
        )
        return selection

    def render(self):
        # render is a better name for this action
        # I will update it later inside Molde
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        if self._must_update:
            self.update_plot()
