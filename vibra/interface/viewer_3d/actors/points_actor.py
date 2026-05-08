from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vibra.engine.mesher.mesh import Mesh

from molde import Color
from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import VTK_VERTEX, vtkPlane, vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from vibra import app


class PointsActor(vtkActor):
    def __init__(self, mesh: Mesh):
        self.mesh = mesh
        self.point_to_cell = dict()

        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        number_of_points = self.mesh.nodal_coordinates.shape[0]

        data = vtkPolyData()
        points = vtkPoints()
        mapper = vtkPolyDataMapper()
        cell_colors = vtkUnsignedCharArray()

        data.Allocate(number_of_points)
        cell_colors.SetNumberOfComponents(4)
        cell_colors.SetNumberOfTuples(number_of_points)

        self.point_to_cell = dict()
        for point_id, node_id in self.mesh.nodes_from_points.items():
            _, x, y, z = self.mesh.nodal_coordinates[node_id]
            i = points.InsertNextPoint(x, y, z)
            cell_id = data.InsertNextCell(VTK_VERTEX, 1, [i])
            self.point_to_cell[point_id] = cell_id

        data.SetPoints(points)
        data.GetCellData().SetScalars(cell_colors)

        mapper.SetInputData(data)
        self.SetMapper(mapper)

        self.clear_colors()

    def configure_appearance(self):
        points_size = app().config.user_preferences.points_size
        if not app().config.user_preferences.compatibility_mode:
            self.GetProperty().RenderPointsAsSpheresOn()

        self.GetProperty().SetPointSize(points_size)
        self.GetProperty().LightingOff()
        self.clear_colors()

    def clear_colors(self):
        rgba = app().config.user_preferences.nodes_points_color
        self.set_color(rgba)

        # By default prints the decoupled points as Transparent
        self.paint_points(
            Color(0, 0, 0, 0),  # transparent
            self._get_decoupled_points(),
        )

    def _get_decoupled_points(self):
        if self.mesh.cache_nodal_coordinates is None:
            return StopIteration()

        current_number_of_nodes = self.mesh.nodal_coordinates.shape[0]
        original_number_of_nodes = self.mesh.cache_nodal_coordinates.shape[0]

        for point, node in self.mesh.nodes_from_points.items():
            if node in range(original_number_of_nodes, current_number_of_nodes):
                yield point

    def set_color(self, color: Color):
        r, g, b, a = color.to_rgba()
        data = self.GetMapper().GetInput()
        cell_colors = data.GetCellData().GetScalars()

        cell_colors.FillComponent(0, r)
        cell_colors.FillComponent(1, g)
        cell_colors.FillComponent(2, b)
        cell_colors.FillComponent(3, a)

        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_points(self, color: Color, points: tuple[int]):
        cells = []
        for point in points:
            cell = self.point_to_cell.get(point)
            if cell is None:
                continue
            cells.append(cell)
        self.paint_cells(color, cells)

    def paint_cells(self, color: Color, cells: tuple[int]):
        data = self.GetMapper().GetInput()
        cell_colors = data.GetCellData().GetScalars()

        color = color.to_rgba()

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

    def set_zbuffer_offsets(self, factor: float, units: float):
        """
        This functions is usefull to make a object appear in front of the others.
        If the object should never be hidden, the parameters should be set to
        factor = 1 and offset = -66000.
        """
        mapper = self.GetMapper()
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyLineOffsetParameters(factor, units)
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(factor, units)
        mapper.SetRelativeCoincidentTopologyPointOffsetParameter(units)
        mapper.Update()
