import vtk

from vibra.interface.viewer_3d.common_renderer import CommonRenderer
from vibra.interface.viewer_3d.example_actor import ExampleActor
from vibra.interface.viewer_3d.symbols_actors import (
    ArrowSymbols,
    ArrowSymbols2,
    ArrowSymbols3,
    ClampSymbols,
)


class ModelRenderer(CommonRenderer):
    def __init__(self):
        super().__init__()
        self.update_actors()

    def update_actors(self):
        self.example_actor = ExampleActor()
        self.AddActor(self.example_actor)

        self.symbols_actor = ClampSymbols(self)
        self.AddActor(self.symbols_actor)

        self.symbols_actor = ArrowSymbols(self)
        self.AddActor(self.symbols_actor)

        self.symbols_actor = ArrowSymbols2(self)
        self.AddActor(self.symbols_actor)

        self.symbols_actor = ArrowSymbols3(self)
        self.AddActor(self.symbols_actor)

    def show_points(self):
        self.example_actor.GetProperty().SetRepresentationToPoints()

    def show_edges(self):
        self.example_actor.GetProperty().SetRepresentationToWireframe()

    def show_faces(self):
        self.example_actor.GetProperty().SetRepresentationToSurface()
