import numpy as np
from vtkmodules.vtkCommonCore import vtkUnsignedCharArray

from ..coloring.color_table import ColorTable
from .hollow_solids_actor import HollowSolidsActor


class HollowAnalysisActor(HollowSolidsActor):
    def apply_deformation(self, displacements, phase, magnification_factor):
        max_abs = np.max(np.linalg.norm(displacements, axis=0))
        u_def = displacements * np.cos(phase * np.pi / 180)
        deltas = (magnification_factor / max_abs) * u_def
        deformed_coordinates = deltas + self.mesh.nodal_coordinates[:, 1:]
        self.update_coordinates(deformed_coordinates)

    def plot_color_bar(self, values, min_value, max_value):
        color_table = ColorTable(values, min_value, max_value)
        self.set_color_table(color_table)

    def set_color_table(self, color_table: ColorTable):
        if self.data is None:
            return

        self.color_table = color_table
        point_colors: vtkUnsignedCharArray = self.data.GetPointData().GetScalars()
        point_colors.Fill(0)

        for i, val in enumerate(self.color_table.values_vector):
            color = self.color_table.get_color(val)
            point_colors.SetTuple(i, color)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()
