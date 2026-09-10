from typing import TYPE_CHECKING

from molde import Color
from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.vtkCommonCore import vtkIntArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import (
    VTK_LINE,
    VTK_QUADRATIC_EDGE,
    VTK_VERTEX,
    vtkPlane,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from vibra import app

if TYPE_CHECKING:
    from vibra.engine.mesher.mesh import Mesh


class LinesActor(vtkActor):
    NODES_TO_VTK_CELL = {2: VTK_LINE, 3: VTK_QUADRATIC_EDGE}

    def __init__(self, mesh: "Mesh"):
        self.mesh = mesh
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        nodes_per_line = len(self.mesh.lines_connectivity[0, 4:])
        number_of_lines = self.mesh.lines_connectivity.shape[0]

        self.data = vtkUnstructuredGrid()
        points = vtkPoints()
        mapper = vtkDataSetMapper()
        self.data.Allocate(number_of_lines * 3)

        line_indices = vtkIntArray()
        line_indices.SetName("line_indices")
        line_indices.Allocate(number_of_lines)

        cell_colors = vtkUnsignedCharArray()
        cell_colors.SetNumberOfComponents(4)

        coordinates = self.mesh.nodal_coordinates[:, 1:]
        points.SetData(numpy_to_vtk(coordinates))

        # Vertices need to be added first
        for _, line_id, _, _, *values in self.mesh.lines_connectivity:
            self.data.InsertNextCell(VTK_VERTEX, 1, [values[0]])
            line_indices.InsertNextValue(line_id)
            cell_colors.InsertNextTuple4(0, 0, 0, 0)

            self.data.InsertNextCell(VTK_VERTEX, 1, [values[1]])
            line_indices.InsertNextValue(line_id)
            cell_colors.InsertNextTuple4(0, 0, 0, 0)

        cell_type = self.NODES_TO_VTK_CELL[nodes_per_line]
        for _, line_id, _, _, *values in self.mesh.lines_connectivity:
            self.data.InsertNextCell(cell_type, nodes_per_line, values)
            line_indices.InsertNextValue(line_id)
            cell_colors.InsertNextTuple4(0, 0, 0, 0)

        self.data.SetPoints(points)
        self.data.GetCellData().SetScalars(cell_colors)
        self.data.GetCellData().AddArray(line_indices)

        mapper.SetInputData(self.data)
        self.SetMapper(mapper)
        self.clear_colors()

    def configure_appearance(self):
        lines_thickness = app().config.user_preferences.lines_thickness
        self.GetProperty().SetLineWidth(lines_thickness)
        self.GetProperty().SetPointSize(lines_thickness)

        self.GetProperty().LightingOff()
        self.GetProperty().RenderLinesAsTubesOn()
        self.GetProperty().RenderPointsAsSpheresOn()
        self.clear_colors()

    def clear_colors(self):
        color = app().config.user_preferences.lines_color
        self.set_color(color)

        # By default prints the decoupled lines as Transparent
        self.paint_cells(
            Color(0, 0, 0, 0),  # Transparent
            self._get_decoupled_line_cells(),
        )

    def _get_decoupled_line_cells(self):
        if self.mesh.cache_lines_connectivity is None:
            return StopIteration()

        number_of_lines = self.mesh.lines_connectivity.shape[0]
        number_of_vertices = number_of_lines * 2
        original_number_of_lines = self.mesh.cache_lines_connectivity.shape[0]

        for line_element in range(original_number_of_lines, number_of_lines):
            yield line_element * 2 + 0
            yield line_element * 2 + 1
            yield number_of_vertices + line_element

    def set_color(self, color: Color):
        cell_colors: vtkUnsignedCharArray = self.data.GetCellData().GetScalars()
        r, g, b, a = color.to_rgba()

        cell_colors.FillComponent(0, r)
        cell_colors.FillComponent(1, g)
        cell_colors.FillComponent(2, b)
        cell_colors.FillComponent(3, a)
        cell_colors.Modified()

        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOn()
        self.GetMapper().Update()

    def paint_lines(self, color: Color, lines: tuple[int]):
        number_of_lines = self.mesh.lines_connectivity.shape[0]
        number_of_vertices = number_of_lines * 2

        all_lines_elements = list()
        for line in lines:
            indices = app().project.model.mesh.elements_from_line.get(line, [])
            all_lines_elements.extend(indices)

        cells = []
        for line_element in all_lines_elements:
            cells.append(line_element * 2 + 0)
            cells.append(line_element * 2 + 1)
            cells.append(number_of_vertices + line_element)

        self.paint_cells(color, cells)

    def paint_cells(self, color: Color, cells: tuple[int]):
        cell_colors: vtkUnsignedCharArray = self.data.GetCellData().GetScalars()

        color = color.to_rgba()
        for i in cells:
            cell_colors.SetTuple(i, color)

        cell_colors.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOn()
        self.GetMapper().Update()

    def disable_cut(self):
        self.GetMapper().RemoveAllClippingPlanes()

    def apply_cut(self, origin, normal):
        plane = vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)
        self.GetMapper().RemoveAllClippingPlanes()
        self.GetMapper().AddClippingPlane(plane)
