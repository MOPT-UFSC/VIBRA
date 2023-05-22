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

        data.Allocate(len(self.mesh.lines))
        cell_colors.SetNumberOfComponents(3)
        cell_colors.SetNumberOfTuples(len(self.mesh.lines))

        for i, (x, y, z) in enumerate(self.mesh.points):
            points.InsertPoint(i, x, y, z)

        for a, b in self.mesh.lines:
            data.InsertNextCell(vtk.VTK_LINE, 2, (a, b))

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
        r = int(r*255)
        g = int(g*255)
        b = int(b*255)

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
        self.GetMapper().ScalarVisibilityOff() # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()
