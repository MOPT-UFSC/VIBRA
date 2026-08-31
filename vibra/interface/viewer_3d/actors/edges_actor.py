from typing import Optional

from molde.colors import Color, color_names
from vtkmodules.vtkCommonCore import vtkIdList
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkExtractCells, vtkExtractEdges
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from vibra import app
from vibra.utils.interface_utils import VisualizationFilter


class EdgesActor(vtkActor):
    def __init__(
        self,
        data,
        visualization_filter: Optional[VisualizationFilter] = None,
    ):
        self.visualization_filter = visualization_filter
        if self.visualization_filter is None:
            self.visualization_filter = VisualizationFilter.all_true()

        self.mapper = vtkDataSetMapper()
        self.cell_extractor = vtkExtractCells()
        self.edges_extractor = vtkExtractEdges()
        self.edges_extractor.UseAllPointsOn()
        self.data = None

        self.mapper.ScalarVisibilityOff()

        self.SetMapper(self.mapper)
        self.extract_data(data)
        self.configure_appearance()

    def extract_data(self, data):
        if data == self.cell_extractor.GetInput():
            return

        self.data = data

        self.cell_extractor.SetInputData(data)
        self.cell_extractor.ExtractAllCellsOn()
        self.cell_extractor.Update()
        self.edges_extractor.SetInputConnection(self.cell_extractor.GetOutputPort())
        self.edges_extractor.Update()
        self.mapper.SetInputConnection(self.edges_extractor.GetOutputPort())

    def distinguish_cells(self, cells: tuple[int]):
        if len(cells) == 0:  # disable if empty -> show all the edges
            self.cell_extractor.ExtractAllCellsOn()
            self.cell_extractor.Update()
            self.mapper.Modified()
            return

        ids = vtkIdList()
        for cell in cells:
            ids.InsertNextId(cell)

        self.cell_extractor.ExtractAllCellsOff()
        self.cell_extractor.SetCellList(ids)
        self.cell_extractor.Update()
        self.mapper.Modified()

    def apply_cut(self, origin, normal):
        if self.data is None:
            return

        plane = vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)

        clipper = vtkExtractGeometry()
        clipper.SetInputConnection(self.edges_extractor.GetOutputPort())
        clipper.SetImplicitFunction(plane)
        clipper.ExtractInsideOff()
        clipper.Update()
        self.clipped_data = clipper.GetOutput()

        mapper = self.GetMapper()
        mapper.InterpolateScalarsBeforeMappingOn()
        mapper.SetInputConnection(clipper.GetOutputPort())
        mapper.Modified()

    def disable_cut(self):
        if self.data is None:
            return

        self.GetMapper().RemoveAllClippingPlanes()
        self.GetMapper().RemoveAllInputConnections(0)
        self.GetMapper().SetInputConnection(self.edges_extractor.GetOutputPort())

    def configure_appearance(self):
        edges_thickness = app().config.user_preferences.edges_thickness
        r, g, b = app().config.user_preferences.edges_color.to_rgb_f()
        self.GetProperty().SetColor(r, g, b)
        self.GetProperty().SetRepresentationToWireframe()
        self.GetProperty().SetLineWidth(edges_thickness)
        self.paint_edges_when_mesh_has_error()

    def paint_edges_when_mesh_has_error(self):

        disconnected_nodes = app().project.model.mesh.disconnected_nodes
        nodes_collapsed_elements = app().project.model.mesh.nodes_from_collapsed_elements

        edges_error_color = color_names.GRAY_3

        if len(disconnected_nodes) > 0 or len(nodes_collapsed_elements) > 0:
            self.GetProperty().SetColor(edges_error_color.to_rgb_f())

    def paint_edges(self, color: Color, edges: tuple[int]):
        self.paint_cells(color, edges)

    def paint_cells(self, color: Color, cells: tuple[int]):
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

    def clear_colors(self):
        color = app().config.user_preferences.nodes_points_color
        disconected_nodes_color = color_names.GREEN
        collapsed_element_nodes_color = color_names.ORANGE

        if self.visualization_filter.points:
            self.set_color(color)
        else:
            self.set_color(Color(0, 0, 0, 0))

        disconnected_nodes = app().project.model.mesh.disconnected_nodes
        nodes_collapsed_elements = app().project.model.mesh.nodes_from_collapsed_elements

        if disconnected_nodes:
            self.paint_nodes(disconected_nodes_color, disconnected_nodes)

        if nodes_collapsed_elements.size:
            self.paint_nodes(collapsed_element_nodes_color, nodes_collapsed_elements)
