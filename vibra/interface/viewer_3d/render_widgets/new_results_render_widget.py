from vibra.interface.viewer_3d.actors.results_actor import ResultsActor
from vibra.interface.viewer_3d.render_widgets.vibra_render_widget import VibraRenderWidget


class NewResultsRenderWidget(VibraRenderWidget):
    def __init__(self):
        super().__init__()
        self.create_axes()

        self.create_actors()

    def create_actors(self):
        self.results_actor = ResultsActor(self.model)
        self.add_actors(self.results_actor)

    def update_plot(self, reset_camera: bool = False): ...
