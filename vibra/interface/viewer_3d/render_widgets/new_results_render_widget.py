from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget

from vibra.engine.model import Model
from vibra.interface.viewer_3d.actors.results_actor import ResultsActor
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
        self.results_actor = ResultsActor(self.model)
        self.add_actors(self.results_actor)
