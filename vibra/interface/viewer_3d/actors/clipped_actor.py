import vtk


class ClippedActor(vtk.vtkActor):
    def __init__(self, mesh):
        self.mesh = mesh
        self.create_geometry()
        self.configure_appearance()
        self.color_stack = []

    def create_geometry(self):
        self.data = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        mapper = vtk.vtkPolyDataMapper()
        point_colors = vtk.vtkUnsignedCharArray()
        cell_colors = vtk.vtkUnsignedCharArray()

        self.data.Allocate(len(self.mesh.faces))
        point_colors.SetNumberOfComponents(3)
        point_colors.SetNumberOfTuples(len(self.mesh.points))
        cell_colors.SetNumberOfComponents(3)
        cell_colors.SetNumberOfTuples(len(self.mesh.faces))

        for i, (x, y, z) in enumerate(self.mesh.points):
            points.InsertPoint(i, x, y, z)

        for a, b, c in self.mesh.faces:
            self.data.InsertNextCell(vtk.VTK_TRIANGLE, 3, [a, b, c])

        self.data.SetPoints(points)
        self.data.GetPointData().SetScalars(point_colors)
        self.data.GetCellData().SetScalars(cell_colors)

        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.AddInputData(self.data)
        normals_filter.Update()

        mapper.SetInputConnection(normals_filter.GetOutputPort())
        self.SetMapper(mapper)

    def apply_cut(self, origin, normal):
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
        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.AddInputData(self.data)
        normals_filter.Update()

        mapper = self.GetMapper()
        mapper.SetInputData(normals_filter.GetOutput())
        mapper.Modified()

    def configure_appearance(self):
        self.GetProperty().SetInterpolationToPhong()
        self.GetProperty().SetDiffuse(0.8)
        self.GetProperty().SetSpecular(0.5)
        self.GetProperty().SetSpecularPower(40)
        self.GetProperty().SetSpecularColor(1, 1, 1)
        self.clear_colors()

    def clear_colors(self):
        point_colors = self.data.GetPointData().GetScalars()
        cell_colors = self.data.GetCellData().GetScalars()

        r, g, b = self.GetProperty().GetColor()
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)

        point_colors.FillComponent(0, r)
        point_colors.FillComponent(1, g)
        point_colors.FillComponent(2, b)

        cell_colors.FillComponent(0, r)
        cell_colors.FillComponent(1, g)
        cell_colors.FillComponent(2, b)

        self.GetMapper().ScalarVisibilityOff()

    def push(self):
        self.data = self.GetMapper().GetInput()
        cell_colors = self.data.GetCellData().GetScalars()

        mode = self.GetMapper().GetScalarMode()
        colors = vtk.vtkUnsignedCharArray()
        colors.DeepCopy(cell_colors)

        self.color_stack.append((mode, colors))

    def pop(self):
        if not self.color_stack:
            return None

        mode, colors = self.color_stack.pop()
        self.data.GetCellData().SetScalars(colors)

        self.GetMapper().SetScalarMode(mode)
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

        return colors

    def paint_points(self, color, points):
        point_colors = self.data.GetPointData().GetScalars()

        for i in points:
            point_colors.SetTuple(i, color)

        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_cells(self, color: tuple[3], faces: tuple[int]):
        cell_colors = self.data.GetCellData().GetScalars()

        for i in faces:
            cell_colors.SetTuple(i, color)

        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()
