from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import VTK_VERTEX, vtkPlane, vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from vibra import app


class PointsActor(vtkActor):
    def __init__(self, mesh):
        self.mesh = mesh
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        number_of_points = self.mesh.nodal_coordinates.shape[0]

        data = vtkPolyData()
        points = vtkPoints()
        mapper = vtkPolyDataMapper()
        cell_colors = vtkUnsignedCharArray()

        data.Allocate(number_of_points)
        cell_colors.SetNumberOfComponents(3)
        cell_colors.SetNumberOfTuples(number_of_points)

        point_indexes = vtkIntArray()
        point_indexes.SetName("point_indexes")
        point_indexes.Allocate(number_of_points)

        for tag, (node_id,) in sorted(self.mesh.nodes_from_points.items()):
            _, x, y, z = self.mesh.nodal_coordinates[node_id]
            points.InsertNextPoint(x, y, z)
            data.InsertNextCell(VTK_VERTEX, 1, [node_id])

        data.SetPoints(points)
        data.GetCellData().SetScalars(cell_colors)
        data.GetCellData().AddArray(point_indexes)

        mapper.SetInputData(data)
        self.SetMapper(mapper)
        
        self.clear_colors()

    def configure_appearance(self):
        self.GetProperty().RenderPointsAsSpheresOn()
        self.GetProperty().SetPointSize(15)
        self.GetProperty().LightingOff()
        self.clear_colors()

    def clear_colors(self):
        data = self.GetMapper().GetInput()
        cell_colors = data.GetCellData().GetScalars()
        r, g, b = app().config.user_preferences.nodes_points_color.to_rgb()

        cell_colors.FillComponent(0, r)
        cell_colors.FillComponent(1, g)
        cell_colors.FillComponent(2, b)

        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_cells(self, color: tuple[3], cells: tuple[int]):
        data = self.GetMapper().GetInput()
        cell_colors = data.GetCellData().GetScalars()

        for i in cells:
            cell_colors.SetTuple(i, color)

        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def apply_cut(self, origin, normal):
        plane = vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)
        self.GetMapper().RemoveAllClippingPlanes()
        self.GetMapper().AddClippingPlane(plane)

    def disable_cut(self):
        self.GetMapper().RemoveAllClippingPlanes()
