import vtk

from vibra.interface.viewer_3d.example_actor import ExampleActor


class ModelRenderer(vtk.vtkRenderer):
    def __init__(self):
        super().__init__()

        self.configure_renderer()
        self.update_actors()

    def configure_renderer(self):
        pass

    def update_actors(self):
        self.example_actor = ExampleActor()
        self.AddActor(self.example_actor)

    def show_points(self):
        self.example_actor.GetProperty().SetRepresentationToPoints()

    def show_edges(self):
        self.example_actor.GetProperty().SetRepresentationToWireframe()

    def show_faces(self):
        self.example_actor.GetProperty().SetRepresentationToSurface()