from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from vibra.engine.model import Model
from vibra.interface.general.selection_handler import SelectionHandler
from vibra.interface.viewer_3d.actors.mesh_actor import MeshActor
from vibra.interface.viewer_3d.render_widgets.vibra_render_widget import VibraRenderWidget
from vibra.utils.interface_utils import SectionPlane
from vibra.utils.time_utils import function_timer


class NewMeshRenderWidget(VibraRenderWidget):
    def __init__(self):
        super().__init__()

        self.create_actors()

        self.left_clicked.connect(self.click_start_callback)
        self.left_released.connect(self.click_end_callback)

    def create_actors(self):
        self.create_common_actors()

        self.mesh_actor = MeshActor(self.model)
        self.add_actors(self.mesh_actor)

    def set_model(self, model: Model | None):
        super().set_model(model)
        self.mesh_actor.model = model

    def set_section_plane(self, section_plane: SectionPlane | None):
        super().set_section_plane(section_plane)
        self.mesh_actor.section_plane = section_plane

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

        self.mesh_actor.show_volumes()
        self.mesh_actor.show_surfaces()
        if self.entity_visibility_handler is not None:
            self.mesh_actor.hide_volumes(self.entity_visibility_handler.get_hidden_volumes())
            self.mesh_actor.hide_surfaces(self.entity_visibility_handler.get_hidden_surfaces())

        self.mesh_actor.update_caches()
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
