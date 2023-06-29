import vtk

from vibra.interface.viewer_3d.actors.faces_actor import FacesActor


class AnalisysActor(FacesActor):
    def apply_cut(self, origin, normal):
        if self.data is None:
            return

        plane = vtk.vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)

        clipper = vtk.vtkClipPolyData()
        clipper.SetInputData(self.data)
        clipper.SetClipFunction(plane)
        clipper.SetOutputPointsPrecision(10)
        clipper.SetValue(-1)
        clipper.Update()

        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.AddInputData(clipper.GetOutput())
        normals_filter.Update()

        mapper = self.GetMapper()
        mapper.SetInputData(normals_filter.GetOutput())
        mapper.Modified()

    def disable_cut(self):
        if self.data is None:
            return

        mapper = self.GetMapper()
        mapper.SetInputData(self.data)
        mapper.Modified()

    def plot_colorbar(self, values, colorbar=None):
        if self.data is None:
            return

        point_colors = self.data.GetPointData().GetScalars()

        min_, max_ = min(values), max(values)

        for i, val in enumerate(values):
            color = (
                int(255 * (val - min_) / (max_ - min_)),
                int(255 * (val - min_) / (max_ - min_) / 3),
                int(255 * (val - min_) / (max_ - min_) / 2),
            )
            point_colors.SetTuple(i, color)

        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()
