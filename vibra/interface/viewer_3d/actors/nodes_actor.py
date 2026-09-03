from collections.abc import Sequence
from typing import Optional

from molde.colors import Color, color_names
from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import VTK_VERTEX, vtkPlane, vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from vibra import app
from vibra.engine.mesher.mesh import Mesh
from vibra.utils.interface_utils import VisualizationFilter


class NodesActor(vtkActor):
    def __init__(
        self,
        mesh: Mesh,
        hidden_nodes=None,
        visualization_filter: Optional[VisualizationFilter] = None,
    ):
        self.visualization_filter = visualization_filter
        if self.visualization_filter is None:
            self.visualization_filter = VisualizationFilter.all_true()

        self.mesh = mesh
        self.data = None
        self.hidden_nodes = hidden_nodes if hidden_nodes is not None else set()

        self.create_geometry()
        self.configure_appearance()

    def get_coordinates(self):
        # Default way of getting coordinates
        # If it need to be changed a subclass does it
        # A generic solid actor doesn't need to know
        # anything about the simulation
        return self.mesh.nodal_coordinates[:, 1:]

    def create_geometry(self):
        data = vtkPolyData()
        points = vtkPoints()
        mapper = vtkPolyDataMapper()
        cell_colors = vtkUnsignedCharArray()
        cell_indexes = vtkIntArray()
        cell_indexes.SetName("cell_indexes")

        data.Allocate(len(self.mesh.nodal_coordinates))
        cell_colors.SetNumberOfComponents(4)
        cell_colors.SetNumberOfTuples(len(self.mesh.nodal_coordinates))
        cell_colors.Fill(0)
        cell_indexes.SetNumberOfTuples(len(self.mesh.nodal_coordinates))

        for i, (x, y, z) in enumerate(self.get_coordinates()):
            cell_indexes.InsertValue(i, i)  # This is usefull if part of the cells are hidden
            points.InsertNextPoint(x, y, z)
            data.InsertNextCell(VTK_VERTEX, 1, [i])

        data.SetPoints(points)
        data.GetCellData().SetScalars(cell_colors)
        data.GetCellData().AddArray(cell_indexes)
        self.data = data
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)

        self.clear_colors()

    def update_coordinates(self, coordinates):
        points: vtkPoints
        points = self.data.GetPoints()
        for i, xyz in enumerate(coordinates):
            points.SetPoint(i, xyz)
        points.Modified()

    def configure_appearance(self):
        nodes_size = app().config.user_preferences.nodes_size
        if not app().config.user_preferences.compatibility_mode:
            self.GetProperty().RenderPointsAsSpheresOn()
        self.GetProperty().SetPointSize(nodes_size)
        self.GetProperty().LightingOff()
        self.clear_colors()

    def clear_colors(self):
        visualization = self.visualization_filter
        color = app().config.user_preferences.nodes_points_color
        disconected_nodes_color = color_names.GREEN
        collapsed_element_nodes_color = color_names.ORANGE

        if visualization.points:
            self.set_color(color)
        else:
            self.set_color(Color(0, 0, 0, 0))

        disconnected_nodes = self.mesh.disconnected_nodes
        nodes_collapsed_elements = self.mesh.nodes_from_collapsed_elements

        if disconnected_nodes:
            self.paint_nodes(disconected_nodes_color, disconnected_nodes)

        if nodes_collapsed_elements:
            self.paint_nodes(collapsed_element_nodes_color, nodes_collapsed_elements)

    def set_color(self, color: Color):
        if self.data is None:
            return

        r, g, b, a = color.to_rgba()
        cell_colors = self.data.GetCellData().GetScalars()
        cell_colors.FillComponent(0, r)
        cell_colors.FillComponent(1, g)
        cell_colors.FillComponent(2, b)
        cell_colors.FillComponent(3, a)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_nodes(self, color: Color, nodes: Sequence[int]):
        self.paint_cells(color, nodes)

    def paint_cells(self, color: Color, cells: Sequence[int]):
        if self.data is None:
            return

        color = color.to_rgba()
        cell_colors = self.data.GetCellData().GetScalars()
        for i in cells:
            cell_colors.SetTuple(i, color)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def disable_cut(self):
        self.GetMapper().RemoveAllClippingPlanes()

    def apply_cut(self, origin, normal):
        plane = vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)
        self.GetMapper().RemoveAllClippingPlanes()
        self.GetMapper().AddClippingPlane(plane)
