import numpy as np
from vtkmodules.vtkCommonCore import vtkUnsignedCharArray

from vibra.interface.viewer_3d.actors.solids_actor import SolidsActor
from ..coloring.color_table import ColorTable


class AnalysisActor(SolidsActor):

    def apply_deformation(self, displacements: np.ndarray, magnification_factor: float, max_abs: float):

        if max_abs == 0:
            max_abs = 1

        deltas = (magnification_factor / (10 * max_abs)) * displacements
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
