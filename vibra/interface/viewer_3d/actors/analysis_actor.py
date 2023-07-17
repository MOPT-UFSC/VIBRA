import vtk

from vibra.interface.viewer_3d.actors.solids_actor import SolidsActor
import numpy as np


class AnalysisActor(SolidsActor):
    def __init__(self, mesh, displacements=None, phase=0, magnification_factor=0):
        self.displacements = displacements
        self.phase = phase
        self.magnification_factor = magnification_factor

        super().__init__(mesh)

        self.lookup_table = vtk.vtkLookupTable()
        self.lookup_table.SetHueRange(2 / 3, 0)

    def get_deformed_coordinates(self):
        max_abs = np.max(np.linalg.norm(self.displacements, axis=0))
        self.u_def = self.displacements*np.cos(self.phase*np.pi/180)
        def_coordinates = self.mesh.nodal_coordinates[:, 1:] + (self.magnification_factor/max_abs)*self.u_def
        return def_coordinates

    def get_coordinates(self):
        '''
        Replaces the behaviour of the method in solids actor
        '''
        if self.displacements is None:
            return super().get_coordinates()
        else:
            return self.get_deformed_coordinates()

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

        mapper = self.GetMapper()
        mapper.InterpolateScalarsBeforeMappingOn()
        mapper.SetInputData(clipper.GetOutput())
        mapper.Modified()

    def disable_cut(self):
        if self.data is None:
            return

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

        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()
