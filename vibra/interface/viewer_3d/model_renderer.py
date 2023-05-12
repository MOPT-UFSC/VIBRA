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
        example_actor = ExampleActor()
        self.AddActor(example_actor)

    def show_points(self, condition):
        pass

    def show_edges(self, condition):
        pass

    def show_faces(self, condition):
        pass
