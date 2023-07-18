import vtk


class EdgesActor(vtk.vtkActor):
    def __init__(self, data):
        self.edges_extractor = vtk.vtkExtractEdges()
        self.edges_extractor.SetInputData(data)
        self.edges_extractor.Update()

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(self.edges_extractor.GetOutput())
        mapper.ScalarVisibilityOff()
        self.SetMapper(mapper)

    def update(self):
        self.edges_extractor.Update()
        self.GetMapper().SetInputData(self.edges_extractor.GetOutput())