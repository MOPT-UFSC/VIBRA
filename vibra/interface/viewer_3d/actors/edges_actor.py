import vtk


class EdgesActor(vtk.vtkActor):
    def __init__(self, data):
        self.mapper = vtk.vtkDataSetMapper()
        self.edges_extractor = vtk.vtkExtractEdges()
        self.edges_extractor.UseAllPointsOn()
        self.data = None

        self.mapper.ScalarVisibilityOff()
        self.GetProperty().SetRepresentationToWireframe()

        self.SetMapper(self.mapper)
        self.extract_data(data)

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
        
        plane = vtk.vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)

        clipper = vtk.vtkExtractGeometry()
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
