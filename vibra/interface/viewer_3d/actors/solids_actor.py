from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.vtkCommonCore import (
    vtkIdList,
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
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
from vibra.engine.mesher.element_type import (
    HEXAHEDRON_8,
    HEXAHEDRON_20,
    TETRAHEDRON_4,
    TETRAHEDRON_10,
)

ALWAYS_FALSE = vtkSphere()
ALWAYS_FALSE.SetRadius(0)


class SolidsActor(vtkActor):
    def __init__(self, mesh, allow_hidding=True):
        self.mesh = mesh
        self.data = None
        self.allow_hidding = allow_hidding
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
        mapper = vtkDataSetMapper()
        point_colors = vtkUnsignedCharArray()
        cell_colors = vtkUnsignedCharArray()
        solid_indexes = vtkIntArray()
        solid_indexes.SetName("solid_indexes")

        if self.mesh.element_type == TETRAHEDRON_4:
            cell_type = VTK_TETRA
            nodes_connectivity = self.mesh.solids_connectivity

        elif self.mesh.element_type == TETRAHEDRON_10:
            cell_type = VTK_QUADRATIC_TETRA
            nodes_order = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 12)
            nodes_connectivity = self.mesh.solids_connectivity[:, nodes_order]

        elif self.mesh.element_type == HEXAHEDRON_8:
            cell_type = VTK_HEXAHEDRON
            nodes_connectivity = self.mesh.solids_connectivity

        elif self.mesh.element_type == HEXAHEDRON_20:
            cell_type = VTK_QUADRATIC_HEXAHEDRON
            nodes_order = (
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 
                15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19
            )  # fmt: skip
            nodes_connectivity = self.mesh.solids_connectivity[:, nodes_order]

        else:
            raise NotImplementedError("Unknown element type")

        number_of_nodes = self.mesh.nodal_coordinates.shape[0]
        number_of_elements = self.mesh.solids_connectivity.shape[0]
        nodes_per_element = nodes_connectivity.shape[1]

        data.Allocate(number_of_elements * nodes_per_element)

        point_colors.SetNumberOfComponents(4)
        point_colors.SetNumberOfTuples(number_of_nodes)
        cell_colors.SetNumberOfComponents(4)
        cell_colors.SetNumberOfTuples(number_of_elements)
        solid_indexes.Allocate(number_of_elements)

        coordinates = self.get_coordinates()
        points.SetData(numpy_to_vtk(coordinates))

        hidden_volumes = app().main_window.hidden_volumes if self.allow_hidding else set()
        self.visible_indexes = dict()

        for i, volume, _, _, *nodes in nodes_connectivity:
            if volume in hidden_volumes:
                continue

            # This is usefull if part of the cells are hidden
            visible_index = solid_indexes.InsertNextValue(i)
            self.visible_indexes[i] = visible_index
            data.InsertNextCell(cell_type, len(nodes), nodes)

        data.SetPoints(points)
        data.GetPointData().SetScalars(point_colors)
        data.GetCellData().SetScalars(cell_colors)
        data.GetCellData().AddArray(solid_indexes)
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

        mapper.InterpolateScalarsBeforeMappingOn()
        mapper.SetInputConnection(self.clipper.GetOutputPort())
        self.SetMapper(mapper)

    def update_coordinates(self, coordinates):
        points = self.data.GetPoints()
        points.SetData(numpy_to_vtk(coordinates))

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
            color = (255, 0, 0)
        else:
            color = (255, 255, 255)

        self.set_color(color)

    def set_color(self, color):
        point_colors = self.data.GetPointData().GetScalars()
        cell_colors = self.data.GetCellData().GetScalars()

        point_colors.Fill(255)
        cell_colors.Fill(255)

        for component, value in enumerate(color):
            point_colors.FillComponent(component, value)
            cell_colors.FillComponent(component, value)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()
        self.GetMapper().ScalarVisibilityOn()

    def paint_points(self, color, points):
        if self.data is None:
            return

        point_colors = self.data.GetPointData().GetScalars()
        for i in points:
            if point_colors.GetNumberOfTuples() <= i:
                break
            point_colors.SetTuple(i, color)

        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_solids(self, color: tuple[3], solids: tuple[int]):
        cells = []
        for i in solids:
            visible_index = self.visible_indexes.get(i, -1)
            if visible_index >= 0:
                cells.append(visible_index)
        self.paint_cells(color, cells)

    def paint_cells(self, color: tuple[3], cells: tuple[int]):
        if self.data is None:
            return

        if len(color) == 3:
            color = *color, 255

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
            visible_index = self.visible_indexes.get(i, -1)
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
