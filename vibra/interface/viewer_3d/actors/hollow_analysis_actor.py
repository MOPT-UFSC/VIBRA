import numpy as np
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkFloatArray

from ..coloring.color_table import ColorTable
from .hollow_solids_actor import HollowSolidsActor


class HollowAnalysisActor(HollowSolidsActor):
    def apply_deformation(self, displacements: np.ndarray, magnification_factor: float, max_abs: float):
        if max_abs == 0:
            max_abs = 1

        deltas = (magnification_factor / (10 * max_abs)) * displacements
        deformed_coordinates = deltas + self.mesh.nodal_coordinates[:, 1:]

        self.update_coordinates(deformed_coordinates)

    def plot_color_bar(self, values, min_value, max_value, colormap="jet"):
        color_table = ColorTable(values, min_value, max_value, colormap)
        self.set_color_table(color_table)

    def set_color_table(self, color_table: ColorTable):
        if self.data is None:
            return

        self.color_table = color_table
        point_colors: vtkFloatArray = self.data.GetPointData().GetScalars()
        point_colors.Fill(0)

        _tmp = vtk_to_numpy(point_colors)
        _tmp[:] = self.color_table.values_vector

        self.data.Modified()
        self.GetMapper().UseLookupTableScalarRangeOn()
        self.GetMapper().SetLookupTable(self.color_table)
        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def configure_appearance(self):
        super().configure_appearance()
        self.GetProperty().SetSpecular(0)
