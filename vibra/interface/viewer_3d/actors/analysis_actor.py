import vtk

from vibra.interface.viewer_3d.actors.solids_actor import SolidsActor
import numpy as np


class AnalysisActor(SolidsActor):
    def __init__(self, mesh):
        super().__init__(mesh)

        self.lookup_table = vtk.vtkLookupTable()
        self.lookup_table.SetHueRange(2 / 3, 0)
        self.clipped_data = self.data

    def apply_deformation(self, displacements, phase, magnification_factor):
        max_abs = np.max(np.linalg.norm(displacements, axis=0))
        u_def = displacements * np.cos(phase * np.pi / 180)
        deformed_coordinates = self.mesh.nodal_coordinates[:, 1:] + (magnification_factor/max_abs) * u_def
        self.update_coordinates(deformed_coordinates)

    def apply_cut(self, origin, normal):
        if self.data is None:
            return

        plane = vtk.vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)

        clipper = vtk.vtkExtractGeometry()
        clipper.SetInputData(self.data)
        clipper.SetImplicitFunction(plane)
        clipper.Update()
        self.clipped_data = clipper.GetOutput()

        mapper = self.GetMapper()
        mapper.InterpolateScalarsBeforeMappingOn()
        mapper.SetInputData(self.clipped_data)
        mapper.Modified()

    def disable_cut(self):
        if self.data is None:
            return
        self.clipped_data = self.data
        mapper = self.GetMapper()
        mapper.SetInputData(self.data)
        mapper.Modified()

    def plot_colorbar(self, values, min_value, max_value):
        if self.data is None:
            return

        self.lookup_table.SetTableRange(min_value, max_value)
        self.lookup_table.Build()

        point_colors = self.data.GetPointData().GetScalars()
        for i, val in enumerate(values):
            color = [0, 0, 0]
            # yes, vtk uses it as a fucking pointer instead of returning a tuple...
            self.lookup_table.GetColor(val, color)
            color = [int(i * 255) for i in color]
            point_colors.SetTuple(i, color)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()