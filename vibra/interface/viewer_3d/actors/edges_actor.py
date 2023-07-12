import vtk


class EdgesActor(vtk.vtkActor):
    def __init__(self, data):
        edges_extractor = vtk.vtkExtractEdges()
        edges_extractor.SetInputData(data)
        edges_extractor.Update()

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(edges_extractor.GetOutput())
        mapper.ScalarVisibilityOff()
        self.SetMapper(mapper)