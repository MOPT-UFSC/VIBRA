import vtk


class EdgesActor(vtk.vtkActor):
    def __init__(self, data):
        mapper = vtk.vtkDataSetMapper()
        self.SetMapper(mapper)
        self.extract_data(data)
    
    def extract_data(self, data):
        self.edges_extractor = vtk.vtkExtractEdges()
        self.edges_extractor.SetInputData(data)
        self.edges_extractor.Update()

        mapper = self.GetMapper()
        mapper.SetInputData(self.edges_extractor.GetOutput())
        mapper.ScalarVisibilityOff()

    def update(self):
        self.edges_extractor.Update()
        self.GetMapper().SetInputData(self.edges_extractor.GetOutput())