import vtk


class FacesActor(vtk.vtkActor):
    def __init__(self, mesh):
        self.mesh = mesh
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        data = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        mapper = vtk.vtkPolyDataMapper()
        data.Allocate(len(self.mesh.lines))

        for i, (x, y, z) in enumerate(self.mesh.points):
            points.InsertPoint(i, x, y, z)

        for a, b, c in self.mesh.faces:
            data.InsertNextCell(vtk.VTK_TRIANGLE, 3, [a, b, c])

        data.SetPoints(points)

        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.AddInputData(data)
        normals_filter.Update()

        mapper.SetInputData(normals_filter.GetOutput())
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().SetInterpolationToPhong()
        self.GetProperty().SetDiffuse(0.8)
        self.GetProperty().SetSpecular(0.5)
        self.GetProperty().SetSpecularPower(40)
        self.GetProperty().SetSpecularColor(1, 1, 1)
