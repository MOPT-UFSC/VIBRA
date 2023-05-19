import vtk


class ExampleActor(vtk.vtkActor):
    def __init__(self):
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        head = vtk.vtkSphereSource()
        body = vtk.vtkSphereSource()
        legs = vtk.vtkSphereSource()
        nose = vtk.vtkConeSource()

        head.SetCenter(0, 4.5, 0)
        body.SetCenter(0, 2.5, 0)
        nose.SetCenter(1, 4.5, 0)

        head.SetRadius(1)
        body.SetRadius(1.5)
        legs.SetRadius(2)
        nose.SetRadius(0.3)

        head.SetPhiResolution(20)
        head.SetThetaResolution(20)
        body.SetPhiResolution(20)
        body.SetThetaResolution(20)
        legs.SetPhiResolution(20)
        legs.SetThetaResolution(20)

        head.Update()
        body.Update()
        legs.Update()
        nose.Update()

        append_filter = vtk.vtkAppendPolyData()
        append_filter.AddInputData(head.GetOutput())
        append_filter.AddInputData(body.GetOutput())
        append_filter.AddInputData(legs.GetOutput())
        append_filter.AddInputData(nose.GetOutput())
        append_filter.Update()

        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.AddInputData(append_filter.GetOutput())
        normals_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(normals_filter.GetOutput())
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().RenderPointsAsSpheresOn()
        self.GetProperty().SetPointSize(9)
        self.GetProperty().SetLineWidth(2)
