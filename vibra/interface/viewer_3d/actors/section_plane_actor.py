import numpy as np
from vtkmodules.vtkFiltersSources import (
    vtkCubeSource,
)
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from vibra.utils.math_functions import bounds_distance, lerp, rotation_matrices


class SectionPlaneActor(vtkActor):
    def __init__(self, bounds):
        self._bounds = bounds
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

    def configure_section_plane(self, position, orientation):
        xyz = self.calculate_xyz_position(position)
        normal = self.calculate_normal_vector(orientation)
        self.SetPosition(xyz)
        self.SetOrientation(orientation)
        return xyz, normal

    def calculate_xyz_position(self, position):
        x = lerp(self._bounds[0], self._bounds[1], position[0] / 100)
        y = lerp(self._bounds[2], self._bounds[3], position[1] / 100)
        z = lerp(self._bounds[4], self._bounds[5], position[2] / 100)
        return x, y, z

    def calculate_normal_vector(self, orientation):
        # https://forum.gamemaker.io/index.php?threads/solved-3d-rotations-with-a-shader-matrix-or-a-matrix-glsl-es.61064/

        orientation = np.array(orientation) * np.pi / 180
        rx, ry, rz = rotation_matrices(*orientation)

        normal = rz @ rx @ ry @ np.array([1, 0, 0, 1])
        return normal[:3]

    def calculate_scale(self):
        scale = bounds_distance(self._bounds)
        self.SetScale(scale, scale, scale)
