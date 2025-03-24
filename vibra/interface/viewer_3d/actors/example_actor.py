from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkPolyDataNormals
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
from vibra import app


class ExampleActor(vtkActor):
    def __init__(self):
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        head = vtkSphereSource()
        body = vtkSphereSource()
        legs = vtkSphereSource()
        nose = vtkConeSource()

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

        append_filter = vtkAppendPolyData()
        append_filter.AddInputData(head.GetOutput())
        append_filter.AddInputData(body.GetOutput())
        append_filter.AddInputData(legs.GetOutput())
        append_filter.AddInputData(nose.GetOutput())
        append_filter.Update()

        normals_filter = vtkPolyDataNormals()
        normals_filter.AddInputData(append_filter.GetOutput())
        normals_filter.Update()

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(normals_filter.GetOutput())
        self.SetMapper(mapper)

    def configure_appearance(self):
        if not app().config.user_preferences.compatibility_mode:
            self.GetProperty().RenderPointsAsSpheresOn()
        self.GetProperty().SetPointSize(4)
        self.GetProperty().SetLineWidth(2)
