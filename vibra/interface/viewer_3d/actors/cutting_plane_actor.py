import vtk
import numpy as np
from vibra.utils.math_functions import lerp, rotation_matrices, bounds_distance



class CuttingPlaneActor(vtk.vtkActor):
    def __init__(self, bounds):
        self.bounds = bounds
        self.create_geometry()
        self.configure_appearance()
        self.calculate_scale()

    def create_geometry(self):
        plane = vtk.vtkPlaneSource()
        cylinder = vtk.vtkCylinderSource()
        cone = vtk.vtkConeSource()

        plane.SetNormal(1, 0, 0)
        cone.SetCenter(0.025, 0, 0)
        cone.SetRadius(0.01)
        cone.SetHeight(0.04)
        cone.SetResolution(10)

        plane.Update()
        cone.Update()
        cylinder.Update()

        append_filter = vtk.vtkAppendPolyData()
        append_filter.AddInputData(plane.GetOutput())
        # append_filter.AddInputData(cone.GetOutput())
        # append_filter.AddInputData(cylinder.GetOutput())
        append_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(append_filter.GetOutput())
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().SetColor(0, 0.333, 0.867)
        self.GetProperty().LightingOff()
        self.PickableOff()

    def configure_cutting_plane(self, position, orientation): 
        x = lerp(self.bounds[0], self.bounds[1], position[0] / 100)
        y = lerp(self.bounds[2], self.bounds[3], position[1] / 100)
        z = lerp(self.bounds[4], self.bounds[5], position[2] / 100)
        self.SetPosition(x, y, z)
        self.SetOrientation(orientation)

        self.GetProperty().SetColor(0, 0.333, 0.867)
        self.GetProperty().SetOpacity(0.8)
    
    def calculate_x_y_z_position(self, position):
        x = lerp(self.bounds[0], self.bounds[1], position[0] / 100)
        y = lerp(self.bounds[2], self.bounds[3], position[1] / 100)
        z = lerp(self.bounds[4], self.bounds[5], position[2] / 100)
        return x, y, z
    
    def calculate_normal_vector(self, orientation):
        # https://forum.gamemaker.io/index.php?threads/solved-3d-rotations-with-a-shader-matrix-or-a-matrix-glsl-es.61064/

        orientation = np.array(orientation) * np.pi / 180
        rx, ry, rz = rotation_matrices(*orientation)

        normal = rz @ rx @ ry @ np.array([1, 0, 0, 1])
        return normal[:3]
    
    def calculate_scale(self):
        scale = bounds_distance(self.bounds)
        self.SetScale(scale, scale, scale)
