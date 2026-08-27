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

    def apply_deformation(self, deformed_coordinates: np.ndarray):
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
