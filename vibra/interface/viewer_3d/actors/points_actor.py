import vtk


class PointsActor(vtk.vtkActor):
    def __init__(self, mesh):
        self.mesh = mesh
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        data = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        mapper = vtk.vtkPolyDataMapper()
        data.Allocate(len(self.mesh.lines))

        # I hope the indexes match
        for pts in self.mesh.points_entities.values():
            for i in pts:
                x, y, z = self.mesh.points[i]
                points.InsertPoint(i, x, y, z)
        data.SetPoints(points)

        vertexFilter = vtk.vtkVertexGlyphFilter()
        vertexFilter.SetInputData(data)
        vertexFilter.Update()

        mapper.SetInputData(vertexFilter.GetOutput())
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().RenderPointsAsSpheresOn()
        self.GetProperty().SetPointSize(5)
