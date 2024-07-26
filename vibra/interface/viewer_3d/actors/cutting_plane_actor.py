import numpy as np
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkCylinderSource,
)
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from vibra.utils.math_functions import bounds_distance, lerp, rotation_matrices


class CuttingPlaneActor(vtkActor):
    def __init__(self, bounds):
        self.bounds = bounds
        self.create_geometry()
        self.configure_appearance()
        self.calculate_scale()

    def create_geometry(self):
        plane = vtkCubeSource()
        plane.SetCenter(0, 0, 0)
        plane.SetXLength(0.005)
        plane.SetYLength(1)
        plane.SetZLength(1)
        plane.Update()

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(plane.GetOutput())
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
