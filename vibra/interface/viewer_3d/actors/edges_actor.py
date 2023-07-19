import vtk


class EdgesActor(vtk.vtkActor):
    def __init__(self, data):
        self.mapper = vtk.vtkPolyDataMapper()
        self.edges_extractor = vtk.vtkExtractEdges()
        self.edges_extractor.UseAllPointsOn()
        
        self.mapper.ScalarVisibilityOff()
        self.GetProperty().SetRepresentationToWireframe()

        self.SetMapper(self.mapper)
        self.extract_data(data)
    
    def extract_data(self, data):
        if data == self.edges_extractor.GetInput():
            return

        self.edges_extractor.SetInputData(data)
        self.edges_extractor.Update()
        self.mapper.SetInputData(self.edges_extractor.GetOutput())
