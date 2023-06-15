from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget
from vibra.interface.viewer_3d.actors.example_actor import ExampleActor
from vibra.interface.viewer_3d.actors.symbols_actors import (
    ArrowSymbols,
    ArrowSymbols2,
    ArrowSymbols3,
    ClampSymbols,
)


class ExampleRenderWidget(CommonRenderWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.update_plot()

    def update_plot(self):
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

    def show_points(self):
        self.example_actor.GetProperty().SetRepresentationToPoints()
        self.update()

    def show_lines(self):
        self.example_actor.GetProperty().SetRepresentationToWireframe()
        self.update()

    def show_faces(self):
        self.example_actor.GetProperty().SetRepresentationToSurface()
        self.update()
