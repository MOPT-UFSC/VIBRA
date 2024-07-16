import vtk
from vibra import app

class FacesActor(vtk.vtkActor):
    def __init__(self, mesh, allow_hidding=True):
        self.mesh = mesh
        self.data = None
        self.allow_hidding = allow_hidding

        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        #
        data = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        mapper = vtk.vtkPolyDataMapper()
        point_colors = vtk.vtkUnsignedCharArray()
        cell_colors = vtk.vtkUnsignedCharArray()
        cell_indexes = vtk.vtkIntArray()
        cell_indexes.SetName("cell_indexes")
        #
        nel = len(self.mesh.faces_connectivity[0, 4:])
        # face_nodes = [3, 6, 4, 8]
        # types = [vtk.VTK_TRIANGLE, vtk.VTK_QUADRATIC_TRIANGLE, vtk.VTK_QUAD, vtk.VTK_QUADRATIC_QUAD]
        # aux = dict(zip(face_nodes, types))
        #
        data.Allocate(nel * len(self.mesh.faces_connectivity))
        point_colors.SetNumberOfComponents(3)
        point_colors.SetNumberOfTuples(len(self.mesh.nodal_coordinates))
        cell_colors.SetNumberOfComponents(3)
        cell_colors.SetNumberOfTuples(len(self.mesh.faces_connectivity))
        cell_indexes.Allocate(len(self.mesh.faces_connectivity))


        for _, x, y, z in self.mesh.nodal_coordinates:
            points.InsertNextPoint(x, y, z)
        #
        self.visible_indexes = dict()
        hidden_surfaces = app().main_window.hidden_surfaces if self.allow_hidding else set()
        # for i, values in enumerate(self.mesh.faces_connectivity[:, 4:]):
        for i, surface, _, _, *values in self.mesh.faces_connectivity:
            if surface in hidden_surfaces:
                continue
            try:
                data.InsertNextCell(vtk.VTK_TRIANGLE, nel, list(values))
                visible_index = cell_indexes.InsertNextValue(i)  # This is usefull if part of the cells are hidden
                self.visible_indexes[i] = visible_index
            except:
                raise NotImplementedError("Not implemented plane element")

        data.SetPoints(points)
        data.GetPointData().SetScalars(point_colors)
        data.GetCellData().SetScalars(cell_colors)
        data.GetCellData().AddArray(cell_indexes)

        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.AddInputData(data)
        normals_filter.Update()

        self.data = normals_filter.GetOutput()
        mapper.SetInputData(self.data)
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().SetInterpolationToPhong()
        self.GetProperty().SetDiffuse(0.8)
        self.GetProperty().SetSpecular(0.5)
        self.GetProperty().SetSpecularPower(40)
        self.GetProperty().SetSpecularColor(1, 1, 1)
        self.clear_colors()

    def clear_colors(self):
        if self.data is None:
            return

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

    def paint_points(self, color, points):
        if self.data is None:
            return

        point_colors = self.data.GetPointData().GetScalars()
        for i in points:
            point_colors.SetTuple(i, color)

        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_cells(self, color: tuple[3], faces: tuple[int]):
        if self.data is None:
            return

        cell_colors = self.data.GetCellData().GetScalars()
        for i in faces:
            visible_index = self.visible_indexes.get(i, -1)
            if visible_index >= 0:
                cell_colors.SetTuple(visible_index, color)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()
    
    def disable_cut(self):
        self.GetMapper().RemoveAllClippingPlanes()

    def apply_cut(self, origin, normal):
        plane = vtk.vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)
        self.GetMapper().RemoveAllClippingPlanes()
        self.GetMapper().AddClippingPlane(plane)