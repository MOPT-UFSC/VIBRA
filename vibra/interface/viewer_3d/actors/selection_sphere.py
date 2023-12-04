import vtk


class SelectionSphere(vtk.vtkActor):
    def __init__(self) -> None:
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        sphere = vtk.vtkSphereSource()
        sphere_mapper = vtk.vtkPolyDataMapper()
        
        sphere.SetRadius(1)
        sphere.SetPhiResolution(20)
        sphere.SetThetaResolution(20)
        sphere.Update()
        
        sphere_mapper.SetInputData(sphere.GetOutput())
        self.SetMapper(sphere_mapper)
    
    def configure_appearance(self):
        self.GetProperty().SetOpacity(0.4)
