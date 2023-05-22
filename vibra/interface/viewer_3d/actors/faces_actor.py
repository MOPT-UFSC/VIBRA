import vtk


class FacesActor(vtk.vtkActor):
    def __init__(self, mesh):
        self.mesh = mesh
        self.create_geometry()
        self.configure_appearance()
        self.color_stack = []

    def create_geometry(self):
        data = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        mapper = vtk.vtkPolyDataMapper()
        point_colors = vtk.vtkUnsignedCharArray()
        cell_colors = vtk.vtkUnsignedCharArray()

        data.Allocate(len(self.mesh.faces))
        point_colors.SetNumberOfComponents(3)
        point_colors.SetNumberOfTuples(len(self.mesh.points))
        cell_colors.SetNumberOfComponents(3)
        cell_colors.SetNumberOfTuples(len(self.mesh.faces))

        for i, (x, y, z) in enumerate(self.mesh.points):
            points.InsertPoint(i, x, y, z)

        for a, b, c in self.mesh.faces:
            data.InsertNextCell(vtk.VTK_TRIANGLE, 3, [a, b, c])

        data.SetPoints(points)
        data.GetPointData().SetScalars(point_colors)
        data.GetCellData().SetScalars(cell_colors)

        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.AddInputData(data)
        normals_filter.Update()

        mapper.SetInputData(normals_filter.GetOutput())
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.clear_colors()

    def clear_colors(self):
        data = self.GetMapper().GetInput()
        point_colors = data.GetPointData().GetScalars()
        cell_colors = data.GetCellData().GetScalars()
        
        r, g, b = self.GetProperty().GetColor()
        r = int(r*255)
        g = int(g*255)
        b = int(b*255)

        point_colors.FillComponent(0, r)
        point_colors.FillComponent(1, g)
        point_colors.FillComponent(2, b)

        cell_colors.FillComponent(0, r)
        cell_colors.FillComponent(1, g)
        cell_colors.FillComponent(2, b)

        self.GetMapper().ScalarVisibilityOff()

    def push(self):
        data = self.GetMapper().GetInput()
        cell_colors = data.GetCellData().GetScalars()

        mode = self.GetMapper().GetScalarMode()
        colors = vtk.vtkUnsignedCharArray()
        colors.DeepCopy(cell_colors)

        self.color_stack.append((mode, colors))

    def pop(self):
        if not self.color_stack:
            return None
        
        mode, colors = self.color_stack.pop()
        data = self.GetMapper().GetInput()
        data.GetCellData().SetScalars(colors)

        self.GetMapper().SetScalarMode(mode)
        self.GetMapper().ScalarVisibilityOff() # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

        return colors

    def paint_points(self, color, points):
       
        data = self.GetMapper().GetInput()
        point_colors = data.GetPointData().GetScalars()
        
        for i in points:
            point_colors.SetTuple(i, color)

        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff() # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_cells(self, color: tuple[3], faces: tuple[int]):
        data = self.GetMapper().GetInput()
        cell_colors = data.GetCellData().GetScalars()
        
        for i in faces:
            cell_colors.SetTuple(i, color)
    
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff() # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()
