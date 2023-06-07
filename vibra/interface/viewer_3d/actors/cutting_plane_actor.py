import vtk


class CuttingPlaneActor(vtk.vtkActor):
    def __init__(self):
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        plane = vtk.vtkPlaneSource()
        arrow = vtk.vtkArrowSource()

        plane.SetNormal(1, 0, 0)

        plane.Update()
        arrow.Update()

        append_filter = vtk.vtkAppendPolyData()
        append_filter.AddInputData(plane.GetOutput())
        append_filter.AddInputData(arrow.GetOutput())
        append_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(append_filter.GetOutput())
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().RenderPointsAsSpheresOn()
        self.GetProperty().SetPointSize(9)
        self.GetProperty().SetLineWidth(2)
        self.GetProperty().SetColor(1, 0, 0)
        self.GetProperty().SetEdgeVisibility(True)
        self.GetProperty().SetOpacity(0.6)
        self.SetScale(3000, 3000, 3000)
