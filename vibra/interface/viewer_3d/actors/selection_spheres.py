import vtk


class SelectionSpheres(vtk.vtkActor):
    def __init__(self) -> None:
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self, centers=None, radius=None):
        if centers is None:
            centers = [(0,0,0)]
        
        if radius is None:
            radius = [1]

        data = vtk.vtkAppendPolyData()
        for c, r in zip(centers, radius):
            sphere = vtk.vtkSphereSource()
            sphere.SetRadius(r)
            sphere.SetCenter(c)
            sphere.SetPhiResolution(20)
            sphere.SetThetaResolution(20)
            sphere.Update()

            data.AddInputData(sphere.GetOutput())
        data.Update()

        sphere_mapper = vtk.vtkPolyDataMapper()
        sphere_mapper.SetInputData(data.GetOutput())
        self.SetMapper(sphere_mapper)
    
    def configure_appearance(self):
        self.GetProperty().SetOpacity(0.4)
        self.GetProperty().SetColor([1, 0, 0])
        self.VisibilityOff()
        self.PickableOff()
