from molde.render_widgets import CommonRenderWidget

from vibra.engine.model import Model
from vibra.interface.viewer_3d.actors.mesh_actor import MeshActor
from vibra.utils.preview_utils import SectionPlaneConfig
from vibra.utils.time_utils import context_timer, function_timer


class PreviewRenderWidget(CommonRenderWidget):
    def __init__(self):
        super().__init__()
        self.create_axes()

        self.model = None
        self.section_plane = None
        self.create_actors()

    def create_actors(self):
        self.mesh_actor = MeshActor(self.model)
        self.add_actors(self.mesh_actor)

    def update_model(self, model: Model | None):
        self.model = model
        self.mesh_actor.model = model

    def update_section_plane(self, section_plane: SectionPlaneConfig | None):
        self.section_plane = section_plane
        self.mesh_actor.section_plane = section_plane

    @function_timer
    def update_plot(self):
        self.mesh_actor.update()

        self.renderer.ResetCamera()
        with context_timer("render"):
            self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.renderer.ResetCamera()
