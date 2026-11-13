from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget

from vibra.engine.model import Model
from vibra.interface.viewer_3d.actors.mesh_actor import MeshActor
from vibra.utils.interface_utils import SectionPlane


class NewMeshRenderWidget(CommonRenderWidget):
    def __init__(self):
        super().__init__()
        self.create_axes()
        self.set_interactor_style(BoxSelectionInteractorStyle())

        self.model: Model | None = None
        self.section_plane: SectionPlane | None = None

        self.create_actors()

    def create_actors(self):
        self.mesh_actor = MeshActor(self.model)
        self.add_actors(self.mesh_actor)

    def update_plot(self, reset_camera: bool = False): ...
