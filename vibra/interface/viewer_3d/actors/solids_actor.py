from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.vtkCommonCore import (
    vtkIdList,
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
    vtkFloatArray,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    VTK_QUADRATIC_HEXAHEDRON,
    VTK_QUADRATIC_TETRA,
    VTK_TETRA,
    vtkPlane,
    vtkPolyData,
    vtkSphere,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersCore import vtkExtractCells
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from vibra import app
from vibra.engine.mesher.mesh_setup import Hexahedron8, Hexahedron20, Tetrahedron4, Tetrahedron10
from molde import Color

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.mesher.mesh import Mesh

ALWAYS_FALSE = vtkSphere()
ALWAYS_FALSE.SetRadius(0)


class SolidsActor(vtkActor):
    def __init__(self, mesh: "Mesh"):
        self.mesh = mesh
        self.data = None
        self.has_distinguished_cells = False

        self.create_geometry()
        self.configure_appearance()

    def get_coordinates(self):
        # Default way of getting coordinates
        # If it need to be changed a subclass does it
        # A generic solid actor doesn't need to know
        # anything about the simulation
        return self.mesh.nodal_coordinates[:, 1:]

    def create_geometry(self):
        data = vtkUnstructuredGrid()
        points = vtkPoints()
        point_colors = vtkFloatArray()
        cell_colors = vtkUnsignedCharArray()
        solid_indices = vtkIntArray()
        solid_indices.SetName("solid_indices")

        if self.mesh.element_topology == Tetrahedron4:
            cell_type = VTK_TETRA
            nodes_connectivity = self.mesh.solids_connectivity

        elif self.mesh.element_topology == Tetrahedron10:
            cell_type = VTK_QUADRATIC_TETRA
            nodes_order = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 12)
            nodes_connectivity = self.mesh.solids_connectivity[:, nodes_order]

        elif self.mesh.element_topology == Hexahedron8:
            cell_type = VTK_HEXAHEDRON
            nodes_connectivity = self.mesh.solids_connectivity

        elif self.mesh.element_topology == Hexahedron20:
            cell_type = VTK_QUADRATIC_HEXAHEDRON
            nodes_order = (
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19
            )  # fmt: skip
            nodes_connectivity = self.mesh.solids_connectivity[:, nodes_order]

        else:
            raise NotImplementedError("Unknown element topology")

        number_of_nodes = self.mesh.nodal_coordinates.shape[0]
        number_of_elements = self.mesh.solids_connectivity.shape[0]
        nodes_per_element = nodes_connectivity.shape[1]

        data.Allocate(number_of_elements * nodes_per_element)

        point_colors.SetNumberOfTuples(number_of_nodes)
        cell_colors.SetNumberOfComponents(4)
        cell_colors.SetNumberOfTuples(number_of_elements)
        solid_indices.Allocate(number_of_elements)

        coordinates = self.get_coordinates()
        points.SetData(numpy_to_vtk(coordinates))

        hidden_volumes = self.get_hidden_volumes()
        self.visible_indices = dict()

        for i, volume, _, _, *nodes in nodes_connectivity:
            if volume in hidden_volumes:
                continue

            # This is usefull if part of the cells are hidden
            visible_index = solid_indices.InsertNextValue(i)
            self.visible_indices[i] = visible_index
            data.InsertNextCell(cell_type, len(nodes), nodes)

        data.SetPoints(points)
        data.GetPointData().SetScalars(point_colors)
        data.GetCellData().SetScalars(cell_colors)
        data.GetCellData().AddArray(solid_indices)
        self.data: vtkPolyData = data

        self.has_distinguished_cells = False
        self.cell_extractor = vtkExtractCells()
        self.cell_extractor.SetInputData(data)
        self.cell_extractor.ExtractAllCellsOn()
        self.cell_extractor.Update()

        self.clipper = vtkExtractGeometry()
        self.clipper.SetInputConnection(self.cell_extractor.GetOutputPort())
        self.clipper.SetImplicitFunction(ALWAYS_FALSE)
        self.clipper.ExtractInsideOff()
        self.clipper.Update()

        self.clipper_mapper = vtkDataSetMapper()
        self.clipper_mapper.InterpolateScalarsBeforeMappingOn()
        self.clipper_mapper.SetInputConnection(self.clipper.GetOutputPort())

        self.SetMapper(self.clipper_mapper)

    def update_coordinates(self, coordinates):
        points = self.data.GetPoints()
        points.SetData(numpy_to_vtk(coordinates))

    def get_hidden_volumes(self):
        return app().main_window.entity_visibility.get_hidden_volumes()

    def configure_appearance(self):
        self.GetProperty().SetInterpolationToPhong()
        self.GetProperty().SetPointSize(3)
        self.GetProperty().SetLineWidth(0.1)
        self.clear_colors()

        mapper = self.GetMapper()
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(1.1, 0)

    def clear_colors(self):
        if self.data is None:
            return

        if self.has_distinguished_cells:
            color = Color(255, 0, 0)
        else:
            color = Color(255, 255, 255)

        self.set_color(color)

    def set_color(self, color: Color):
        cell_colors = self.data.GetCellData().GetScalars()
        cell_colors.Fill(255)
        color = color.to_rgb()
        for component, value in enumerate(color):
            cell_colors.FillComponent(component, value)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()
        self.GetMapper().ScalarVisibilityOn()

    def paint_points(self, color : Color, points):
        if self.data is None:
            return

        color = color.to_rgb()
        point_colors = self.data.GetPointData().GetScalars()
        for i in points:
            if point_colors.GetNumberOfTuples() <= i:
                break
            point_colors.SetTuple(i, color)

        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_solids(self, color: Color, solids: tuple[int]):
        cells = []
        for i in solids:
            visible_index = self.visible_indices.get(i, -1)
            if visible_index >= 0:
                cells.append(visible_index)
        self.paint_cells(color, cells)

    def paint_cells(self, color: Color, cells: tuple[int]):
        if self.data is None:
            return

        color = color.to_rgba()
        cell_colors = self.data.GetCellData().GetScalars()
        for cell in cells:
            cell_colors.SetTuple(cell, color)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def apply_cut(self, origin, normal):
        plane = vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)
        self.clipper.SetImplicitFunction(plane)

    def disable_cut(self):
        self.clipper.SetImplicitFunction(ALWAYS_FALSE)

    def distinguish_solids(self, solids: tuple[int]):
        cells = []
        for i in solids:
            visible_index = self.visible_indices.get(i, -1)
            if visible_index >= 0:
                cells.append(visible_index)

        self.distinguish_cells(cells)

    def distinguish_cells(self, cells: tuple[int]):
        if len(cells) == 0:  # disable if empty
            self.has_distinguished_cells = False
            self.cell_extractor.ExtractAllCellsOn()
            return

        self.has_distinguished_cells = True

        ids = vtkIdList()
        for cell in cells:
            ids.InsertNextId(cell)

        self.cell_extractor.ExtractAllCellsOff()
        self.cell_extractor.SetCellList(ids)
        self.cell_extractor.Update()

        self.clear_colors()
