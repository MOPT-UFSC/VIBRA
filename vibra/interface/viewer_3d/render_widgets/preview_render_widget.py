from molde.render_widgets import CommonRenderWidget

from vibra.interface.viewer_3d.actors.mesh_actor import MeshActor


class PreviewRenderWidget(CommonRenderWidget):
    def __init__(self):
        super().__init__()
        self.create_axes()
        self.model = None

    def update_plot(self):
        if self.model is None:
            return

        self.remove_all_actors()
        self.mesh = MeshActor(self.model)
        self.mesh.build_mesh()
        self.add_actors(self.mesh)

        self.renderer.ResetCamera()
        self.update()
