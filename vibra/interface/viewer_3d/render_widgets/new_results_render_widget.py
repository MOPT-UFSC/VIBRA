from vibra.engine.model import Model
from vibra.interface.viewer_3d.actors.results_actor import ResultsActor
from vibra.interface.viewer_3d.render_widgets.vibra_render_widget import VibraRenderWidget
from vibra.utils.interface_utils import SectionPlane
from vibra.utils.time_utils import function_timer


class NewResultsRenderWidget(VibraRenderWidget):
    def __init__(self):
        super().__init__()

        self.create_actors()

    def create_actors(self):
        self.create_axes()
        self.create_scale_bar()

        self.results_actor = ResultsActor(self.model)
        self.add_actors(self.results_actor)

    def set_model(self, model: Model | None):
        super().set_model(model)
        self.results_actor.model = model

    def set_section_plane(self, section_plane: SectionPlane | None):
        super().set_section_plane(section_plane)
        self.results_actor.section_plane = section_plane

    @function_timer
    def update_plot(self, reset_camera: bool = False):
        if self.isVisible() or reset_camera:
            self._must_update = False
        else:
            self._must_update = True
            return

        self.results_actor.update()

        self.update_visualization()

        if reset_camera:
            self.renderer.ResetCamera()

        self.render()

    @function_timer
    def update_visualization(self):
        self.renderer.SetBackground(self.user_preferences.renderer_background_color_1.to_rgb_f())
        self.renderer.SetBackground2(self.user_preferences.renderer_background_color_2.to_rgb_f())

        self._update_nodes_appearance()
        self._update_edges_appearance()
        self._update_surfaces_appearance()
        self._update_solids_appearance()

        self.results_actor.show_volumes()
        self.results_actor.show_surfaces()
        if self.entity_visibility_handler is not None:
            self.results_actor.hide_volumes(self.entity_visibility_handler.get_hidden_volumes())
            self.results_actor.hide_surfaces(self.entity_visibility_handler.get_hidden_surfaces())

        self.results_actor.update_caches()
        self.render()

    def _update_nodes_appearance(self):
        self.results_actor.set_nodes_visibility(visible=self.visualization_filter.points)
        if not self.visualization_filter.points:
            return

        self.results_actor.set_node_color(self.user_preferences.nodes_points_color)
        self.results_actor.set_nodes_size(self.user_preferences.nodes_size)

    def _update_edges_appearance(self):
        self.results_actor.set_edges_visibility(visible=self.visualization_filter.lines)
        if not self.visualization_filter.lines:
            return

        self.results_actor.set_edge_color(self.user_preferences.edges_color)
        self.results_actor.set_edge_thickness(self.user_preferences.edges_thickness)

    def _update_surfaces_appearance(self):
        self.results_actor.set_surfaces_visibility(visible=self.visualization_filter.faces)
        if not self.visualization_filter.faces:
            return

        self.results_actor.set_surface_color(self.user_preferences.faces_color)

    def _update_solids_appearance(self):
        self.results_actor.set_solids_visibility(visible=self.visualization_filter.faces)
        if not self.visualization_filter.faces:
            return

        self.results_actor.set_volume_color(self.user_preferences.volumes_color)
