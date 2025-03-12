from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkExtractEdges
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from vibra import app


class EdgesActor(vtkActor):
    def __init__(self, data):
        self.mapper = vtkDataSetMapper()
        self.edges_extractor = vtkExtractEdges()
        self.edges_extractor.UseAllPointsOn()
        self.data = None

        self.mapper.ScalarVisibilityOff()

        self.SetMapper(self.mapper)
        self.extract_data(data)
        self.configure_appearance()

    def extract_data(self, data):
        if data == self.edges_extractor.GetInput():
            return

        self.data = data

        self.edges_extractor.SetInputData(data)
        self.edges_extractor.Update()
        self.mapper.SetInputData(self.edges_extractor.GetOutput())

    def apply_cut(self, origin, normal):
        if self.data is None:
            return

        plane = vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)

        clipper = vtkExtractGeometry()
        clipper.SetInputData(self.data)
        clipper.SetImplicitFunction(plane)
        clipper.ExtractInsideOff()
        clipper.Update()
        self.clipped_data = clipper.GetOutput()

        mapper = self.GetMapper()
        mapper.InterpolateScalarsBeforeMappingOn()
        mapper.SetInputConnection(clipper.GetOutputPort())
        mapper.Modified()

    def disable_cut(self):
        if self.data is None:
            return

        self.GetMapper().RemoveAllClippingPlanes()
        self.GetMapper().RemoveAllInputConnections(0)
        self.GetMapper().SetInputData(self.data)

    def configure_appearance(self):
        r, g, b = app().config.user_preferences.edges_color.to_rgb_f()
        self.GetProperty().SetColor(r, g, b)
        self.GetProperty().SetRepresentationToWireframe()
        edges_thickness = app().config.user_preferences.edges_thickness
        self.GetProperty().SetLineWidth(edges_thickness)
