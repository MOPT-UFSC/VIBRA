import numpy as np
from molde.colors import color_names

from .faces_actor import FacesActor


class GhostActor(FacesActor):
    def __init__(self, mesh):
        super().__init__(mesh, allow_hidding=False, update_normals=False)

    def update_coordinates(self, coordinates):
        points = self.data.GetPoints()
        for i, xyz in enumerate(coordinates):
            points.SetPoint(i, xyz)
        points.Modified()

    def apply_deformation(self, displacements: np.ndarray, magnification_factor: float, max_abs: float):
        if max_abs == 0:
            max_abs = 1

        deltas = (magnification_factor / (10 * max_abs)) * displacements
        deformed_coordinates = deltas + self.mesh.nodal_coordinates[:, 1:]
        self.update_coordinates(deformed_coordinates)

    def configure_appearance(self):
        self.GetProperty().SetOpacity(0.05)
        self.GetProperty().LightingOff()
        self.PickableOff()
        self.set_color(color_names.WHITE)

    def SetVisibility(self, _arg):
        if _arg:
            self.VisibilityOn()
        else:
            self.VisibilityOff()

    def VisibilityOn(self):
        self.GetProperty().SetOpacity(0.05)

    def VisibilityOff(self):
        self.GetProperty().SetOpacity(0)
