from vibra.interface.viewer_3d.actors.example_actor import ExampleActor
from vibra.interface.viewer_3d.actors.symbols_actors import (
    ArrowSymbols,
    ArrowSymbols2,
    ArrowSymbols3,
    ClampSymbols,
)
from vibra.interface.viewer_3d.render_widgets.common_render_widget import CommonRenderWidget


class ExampleRenderWidget(CommonRenderWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.example_actor = None

        self.create_axes()
        self.update_plot()

    def update_plot(self):
        self.remove_actors()

        self.example_actor = ExampleActor()
        self.renderer.AddActor(self.example_actor)

        self.symbols_actor = ClampSymbols(self.renderer)
        self.renderer.AddActor(self.symbols_actor)

        self.symbols_actor = ArrowSymbols(self.renderer)
        self.renderer.AddActor(self.symbols_actor)

        self.symbols_actor = ArrowSymbols2(self.renderer)
        self.renderer.AddActor(self.symbols_actor)

        self.symbols_actor = ArrowSymbols3(self.renderer)
        self.renderer.AddActor(self.symbols_actor)

        self.renderer.ResetCamera()

    def show_points(self):
        self.example_actor.GetProperty().SetRepresentationToPoints()
        self.update()

    def show_lines(self):
        self.example_actor.GetProperty().SetRepresentationToWireframe()
        self.update()

    def show_faces(self):
        self.example_actor.GetProperty().SetRepresentationToSurface()
        self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.example_actor)
        self.example_actor = None

    def _actors_exists(self):
        actors = [
            self.example_actor,
        ]

        return all([actor is not None for actor in actors])
