from vibra.interface.user_preferences import UserPreferences
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget

from vibra.engine.model import Model
from vibra.interface.viewer_3d.actors.geometry_actor import GeometryActor
from vibra.interface.viewer_3d.actors.symbols_actor_acoustic import SymbolsActorAcoustic
from vibra.interface.viewer_3d.actors.symbols_actor_structural import SymbolsActorStructural
from vibra.utils.interface_utils import GeometryRendererConfig, SectionPlane, VisualizationFilter


class GeometryRenderWidget(CommonRenderWidget):
    def __init__(self):
        super().__init__()
        self.set_interactor_style(BoxSelectionInteractorStyle())

        self.model: Model | None = None
        self.section_plane: SectionPlane | None = None
        self.user_preferences = GeometryRendererConfig()
        self.visualization_filter = VisualizationFilter(faces=True, symbols=True)

        self.create_actors()

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

    def set_user_preferences(self, preferences: UserPreferences | None):
        if preferences is None:
            preferences = UserPreferences()
        self.user_preferences = preferences

    def set_visualization_filter(self, visualization_filter: VisualizationFilter | None):
        if visualization_filter is None:
            visualization_filter = VisualizationFilter(faces=True, symbols=True)
        self.visualization_filter = visualization_filter

    def update_plot(self, reset_camera: bool = False):
        self.geometry_actor.update()
        self.acoustic_symbols_actor.build()
        self.structural_symbols_actor.build()

        self.update_visualization()

        if reset_camera:
            self.renderer.ResetCamera()

        self.render()

    def update_visualization(self):
        self.renderer.SetBackground(self.mesh_config.background_bottom.to_rgb_f())
        self.renderer.SetBackground2(self.mesh_config.background_top.to_rgb_f())

        self.geometry_actor.set_point_color(self.user_preferences.points_color)
        self.geometry_actor.set_line_color(self.user_preferences.lines_color)
        self.geometry_actor.set_surface_color(self.user_preferences.surfaces_color)

        self.geometry_actor.set_point_size(self.user_preferences.points_size)
        self.geometry_actor.set_line_thickness(self.user_preferences.lines_thickness)

        self.geometry_actor.set_points_visibility(visible=self.visualization_filter.points)
        self.geometry_actor.set_lines_visibility(visible=self.visualization_filter.lines)
        self.geometry_actor.set_surfaces_visibility(visible=self.visualization_filter.faces)

        self.geometry_actor.update_caches()

    def render(self):
        # render is a better name for this action
        # I will update it later inside Molde
        self.update()
