import numpy as np
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkCutter
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper

from vibra.interface.viewer_3d.actors.solids_actor import SolidsActor
from ..coloring.color_table import ColorTable


class AnalysisActor(SolidsActor):

    def create_geometry(self):
        super().create_geometry()
        self.cutter = vtkCutter()
        self.cutter.SetInputData(self.data)

        self.cutter_mapper = vtkPolyDataMapper()
        self.cutter_mapper.SetInputConnection(self.cutter.GetOutputPort())
        self.cutter_mapper.InterpolateScalarsBeforeMappingOn()
        self.SetMapper(self.cutter_mapper)

    def apply_deformation(self, deformed_coordinates: np.ndarray):
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

    def apply_cut(self, origin, normal):
        super().apply_cut(origin, normal)
        self.clipper.Update()
        self.SetMapper(self.clipper_mapper)


    def apply_cutter(self, origin, normal):
        if self.data is None:
            return

        plane = vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)

        self.cutter.SetCutFunction(plane)
        self.cutter.SetInputData(self.data)
        self.cutter.Update()
        self.SetMapper(self.cutter_mapper)
