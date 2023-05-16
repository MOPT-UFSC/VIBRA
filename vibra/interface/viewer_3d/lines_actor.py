import vtk


class LinesActor(vtk.vtkActor):
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

        for a, b in self.mesh.lines:
            data.InsertNextCell(vtk.VTK_LINE, 2, (a, b))

        data.SetPoints(points)
        mapper.SetInputData(data)
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().SetLineWidth(5)
