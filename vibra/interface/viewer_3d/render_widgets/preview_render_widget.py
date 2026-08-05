from molde.render_widgets import CommonRenderWidget

from vibra.interface.viewer_3d.actors.mesh_actor import MeshActor
from vibra.utils.time_utils import function_timer


class RenderUpdateManager:
    def need_mesh_update(self, mesh) -> bool:
        return False


class PreviewRenderWidget(CommonRenderWidget):
    def __init__(self):
        super().__init__()
        self.create_axes()

        self.model = None
        self.create_actors()

    def create_actors(self):
        self.mesh_actor = MeshActor(self.model)
        self.add_actors(self.mesh_actor)

    def update_model(self, model: None):
        self.model = model
        self.mesh_actor.model = model

    @function_timer
    def update_plot(self):
        if self.model is None:
            return

        self.mesh_actor.update()

        self.renderer.ResetCamera()
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.renderer.ResetCamera()
