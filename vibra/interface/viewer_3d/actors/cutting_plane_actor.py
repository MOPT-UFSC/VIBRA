import vtk


class CuttingPlaneActor(vtk.vtkActor):
    def __init__(self):
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        plane = vtk.vtkPlaneSource()
        cone = vtk.vtkConeSource()

        plane.SetNormal(1, 0, 0)
        cone.SetCenter(0.025, 0, 0)
        cone.SetRadius(0.05)
        cone.SetHeight(0.05)

        plane.Update()
        cone.Update()

        append_filter = vtk.vtkAppendPolyData()
        append_filter.AddInputData(plane.GetOutput())
        append_filter.AddInputData(cone.GetOutput())
        append_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(append_filter.GetOutput())
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().SetColor(0.15, 0.82, 0.74)
        self.GetProperty().SetLineWidth(2)
        # self.GetProperty().SetOpacity(0.6)
        self.SetScale(3000, 3000, 3000)
