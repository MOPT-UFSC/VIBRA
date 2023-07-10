import vtk

from vibra.interface.viewer_3d.actors.solids_actor import SolidsActor


class AnalysisActor(SolidsActor):
    def __init__(self, mesh):
        super().__init__(mesh)
        self.lookup_table = vtk.vtkLookupTable()
        self.lookup_table.SetHueRange(2 / 3, 0)

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

    def plot_colorbar(self, values):
        if self.data is None:
            return

        self.lookup_table.SetTableRange(round(min(values), 1), round(max(values), 1))
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
