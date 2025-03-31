from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.vtkCommonCore import vtkIntArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import (
    VTK_LINE,
    VTK_QUADRATIC_EDGE,
    VTK_VERTEX,
    vtkPlane,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from vibra import app


class LinesActor(vtkActor):
    NODES_TO_VTK_CELL = {2: VTK_LINE, 3: VTK_QUADRATIC_EDGE}

    def __init__(self, mesh):
        self.mesh = mesh
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        nodes_per_line = self.mesh.lines_connectivity.shape[1] - 4
        number_of_lines = self.mesh.lines_connectivity.shape[0]

        data = vtkPolyData()
        points = vtkPoints()
        mapper = vtkPolyDataMapper()
        data.Allocate(number_of_lines * 3)

        line_indexes = vtkIntArray()
        line_indexes.SetName("line_indexes")
        line_indexes.Allocate(number_of_lines)

        cell_colors = vtkUnsignedCharArray()
        cell_colors.SetNumberOfComponents(3)

        coordinates = self.mesh.nodal_coordinates[:, 1:]
        points.SetData(numpy_to_vtk(coordinates))

        # Vertices need to be added first
        for _, line_id, _, _, *values in self.mesh.lines_connectivity:
            data.InsertNextCell(VTK_VERTEX, 1, [values[0]])
            line_indexes.InsertNextValue(line_id)
            cell_colors.InsertNextTuple3(0, 0, 0)

            data.InsertNextCell(VTK_VERTEX, 1, [values[-1]])
            line_indexes.InsertNextValue(line_id)
            cell_colors.InsertNextTuple3(0, 0, 0)

        cell_type = self.NODES_TO_VTK_CELL[nodes_per_line]
        for _, line_id, _, _, *values in self.mesh.lines_connectivity:
            data.InsertNextCell(cell_type, nodes_per_line, values)
            line_indexes.InsertNextValue(line_id)
            cell_colors.InsertNextTuple3(0, 0, 0)

        data.SetPoints(points)
        data.GetCellData().SetScalars(cell_colors)
        data.GetCellData().AddArray(line_indexes)

        mapper.SetInputData(data)
        self.SetMapper(mapper)
        self.clear_colors()

    def configure_appearance(self):
        lines_thickness = app().config.user_preferences.lines_thickness
        self.GetProperty().SetLineWidth(lines_thickness)

        self.GetProperty().LightingOff()
        self.GetProperty().RenderLinesAsTubesOn()
        self.GetProperty().RenderPointsAsSpheresOn()
        self.GetProperty().SetPointSize(6)
        self.clear_colors()

    def clear_colors(self):
        data = self.GetMapper().GetInput()
        cell_colors: vtkUnsignedCharArray = data.GetCellData().GetScalars()
        r, g, b = app().config.user_preferences.lines_color.to_rgb()

        cell_colors.FillComponent(0, r)
        cell_colors.FillComponent(1, g)
        cell_colors.FillComponent(2, b)

        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_lines(self, color: tuple[3], lines: tuple[int]):
        number_of_lines = self.mesh.lines_connectivity.shape[0]
        number_of_vertices = number_of_lines * 2

        all_lines_elements = list()
        for line in lines:
            indexes = app().project.model.mesh.elements_from_line.get(line, [])
            all_lines_elements.extend(indexes)

        cells = []
        for line_element in all_lines_elements:
            cells.append(line_element * 2 + 0)
            cells.append(line_element * 2 + 1)
            cells.append(number_of_vertices + line_element)

        self.paint_cells(color, cells)

    def paint_cells(self, color: tuple[3], cells: tuple[int]):
        data = self.GetMapper().GetInput()
        cell_colors: vtkUnsignedCharArray = data.GetCellData().GetScalars()

        for i in cells:
            cell_colors.SetTuple(i, color)

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
