import numpy as np
from vtkmodules.vtkCommonCore import vtkUnsignedCharArray

from vibra.interface.viewer_3d.actors.solids_actor import SolidsActor
from ..coloring.color_table import ColorTable


class AnalysisActor(SolidsActor):
    def __init__(self, mesh):
        super().__init__(mesh)
        self.color_table: ColorTable | None = None
        self.clipped_data = self.data

    def apply_deformation(self, displacements, phase, magnification_factor):
        max_abs = np.max(np.linalg.norm(displacements, axis=0))
        u_def = displacements * np.cos(phase * np.pi / 180)
        deformed_coordinates = (
            self.mesh.nodal_coordinates[:, 1:] + (magnification_factor / max_abs) * u_def
        )
        self.update_coordinates(deformed_coordinates)

    def set_color_table(self, values, min_value, max_value):
        if self.data is None:
            return

        self.color_table = ColorTable(values, min_value, max_value)
        point_colors: vtkUnsignedCharArray = self.data.GetPointData().GetScalars()

        for i, val in enumerate(values):
            color = self.color_table.get_color(val)
            point_colors.SetTuple(i, color)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()
