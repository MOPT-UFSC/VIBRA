from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget

from vibra.engine.model import Model
from vibra.interface.viewer_3d.actors.geometry_actor import GeometryActor
from vibra.utils.interface_utils import SectionPlane


class PreviewRenderWidget(CommonRenderWidget):
    def __init__(self):
        super().__init__()
        self.create_axes()
        self.set_interactor_style(BoxSelectionInteractorStyle())

        self.model: Model | None = None
        self.section_plane: SectionPlane | None = None

        self.create_actors()

    def create_actors(self):
        self.geometry_actor = GeometryActor(self.model)
        self.add_actors(self.geometry_actor)
