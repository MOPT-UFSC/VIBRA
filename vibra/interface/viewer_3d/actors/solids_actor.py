from time import time

import numpy as np
from vtkmodules.vtkCommonCore import (
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
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper
from vtkmodules.util.numpy_support import numpy_to_vtk

from vibra import app
from vibra.engine.mesher.element_type import *


class SolidsActor(vtkActor):
    def __init__(self, mesh, allow_hidding=True):
        self.mesh = mesh
        self.data = None
        self.allow_hidding = allow_hidding

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
            nodes_order = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19)
            nodes_connectivity = self.mesh.solids_connectivity[:, nodes_order]

        else:
            raise NotImplementedError("Unknown element type")

        number_of_nodes = self.mesh.nodal_coordinates.shape[0]
        number_of_elements = self.mesh.solids_connectivity.shape[0]
        nodes_per_element = nodes_connectivity.shape[1]

        data.Allocate(number_of_elements * nodes_per_element)

        point_colors.SetNumberOfComponents(3)
        point_colors.SetNumberOfTuples(number_of_nodes)
        cell_colors.SetNumberOfComponents(3)
        cell_colors.SetNumberOfTuples(number_of_elements)
        solid_indexes.Allocate(number_of_elements)
        
        coordinates = self.get_coordinates()
        points.SetData(numpy_to_vtk(coordinates))

        hidden_volumes = app().main_window.hidden_volumes if self.allow_hidding else set()
        self.visible_indexes = dict()
        # for i, nodes in enumerate(nodes_connectivity):
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

        self.data = data
        mapper.SetInputData(self.data)
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

    def paint_cells(self, color: tuple[3], volumes: tuple[int]):
        if self.data is None:
            return

        cell_colors = self.data.GetCellData().GetScalars()
        for i in volumes:
            visible_index = self.visible_indexes.get(i, -1)
            if visible_index >= 0:
                cell_colors.SetTuple(visible_index, color)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def apply_cut(self, origin, normal):
        plane = vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)

        clipper = vtkExtractGeometry()
        clipper.SetInputData(self.data)
        clipper.SetImplicitFunction(plane)
        clipper.ExtractInsideOff()
        clipper.Update()
        self.clipped_data = clipper.GetOutput()

        mapper = self.GetMapper()
        mapper.InterpolateScalarsBeforeMappingOn()
        mapper.SetInputConnection(clipper.GetOutputPort())
        mapper.Modified()

    def disable_cut(self):
        self.GetMapper().RemoveAllClippingPlanes()
        self.GetMapper().RemoveAllInputConnections(0)
        self.GetMapper().SetInputData(self.data)
