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
        cell_colors = vtk.vtkUnsignedCharArray()

        data.Allocate(len(self.mesh.lines_connectivity))
        cell_colors.SetNumberOfComponents(3)
        cell_colors.SetNumberOfTuples(len(self.mesh.lines_connectivity))

        for _, x, y, z in self.mesh.nodal_coordinates:
            points.InsertNextPoint(x, y, z)

        connect = self.mesh.lines_connectivity[:, 4:]
        if len(connect[0, :]) == 2:    
            for a, b in connect:
                data.InsertNextCell(vtk.VTK_LINE, 2, (a, b))
        else:
            for a, b, c in connect:
                data.InsertNextCell(vtk.VTK_QUADRATIC_EDGE, 3, (a, b, c))

        data.SetPoints(points)
        data.GetCellData().SetScalars(cell_colors)

        mapper.SetInputData(data)
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().SetLineWidth(3)
        self.clear_colors()

    def clear_colors(self):
        data = self.GetMapper().GetInput()
        cell_colors = data.GetCellData().GetScalars()

        r, g, b = self.GetProperty().GetColor()
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)

        cell_colors.FillComponent(0, r)
        cell_colors.FillComponent(1, g)
        cell_colors.FillComponent(2, b)

        self.GetMapper().ScalarVisibilityOff()

    def paint_cells(self, color: tuple[3], cells: tuple[int]):
        data = self.GetMapper().GetInput()
        cell_colors = data.GetCellData().GetScalars()

        for i in cells:
            cell_colors.SetTuple(i, color)

        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()
