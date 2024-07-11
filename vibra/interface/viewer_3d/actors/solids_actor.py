
from vibra.engine.mesher.element_type import *

import vtk
import numpy as np
from time import time


class SolidsActor(vtk.vtkActor):
    def __init__(self, mesh):
        self.mesh = mesh
        self.data = None

        self.create_geometry()
        self.configure_appearance()

    def get_coordinates(self):
        # Default way of getting coordinates
        # If it need to be changed a subclass does it
        # A generic solid actor doesn't need to know
        # anything about the simulation
        return self.mesh.nodal_coordinates[:, 1:]

    def create_geometry(self):
        data = vtk.vtkUnstructuredGrid()
        points = vtk.vtkPoints()
        mapper = vtk.vtkDataSetMapper()
        point_colors = vtk.vtkUnsignedCharArray()
        cell_colors = vtk.vtkUnsignedCharArray()

        if self.mesh.element_type == TETRAHEDRON_4:
            cell_type = vtk.VTK_TETRA
            nodes_connectivity = self.mesh.solids_connectivity[:, 4:]

        elif self.mesh.element_type == TETRAHEDRON_10:
            cell_type = vtk.VTK_QUADRATIC_TETRA
            nodes_order = (4, 5, 6, 7, 8, 9, 10, 11, 13, 12)
            nodes_connectivity = self.mesh.solids_connectivity[:, nodes_order]

        elif self.mesh.element_type == HEXAHEDRON_8:
            cell_type = vtk.VTK_HEXAHEDRON
            nodes_connectivity = self.mesh.solids_connectivity[:, 4:]

        elif self.mesh.element_type == HEXAHEDRON_20:
            cell_type = vtk.VTK_QUADRATIC_HEXAHEDRON
            nodes_order = (4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19)
            nodes_connectivity = self.mesh.solids_connectivity[:, nodes_order]

        else:
            raise NotImplementedError("Unknown element type")
        
        number_of_nodes = self.mesh.nodal_coordinates.shape[0]
        number_of_elements = self.mesh.solids_connectivity.shape[0]
        nodes_per_element = nodes_connectivity.shape[1]

        data.Allocate( number_of_elements * nodes_per_element )

        point_colors.SetNumberOfComponents(3)
        point_colors.SetNumberOfTuples(number_of_nodes)
        cell_colors.SetNumberOfComponents(3)
        cell_colors.SetNumberOfTuples(number_of_elements)

        for x, y, z in self.get_coordinates():
            points.InsertNextPoint(x, y, z)

        for nodes in nodes_connectivity:
            data.InsertNextCell(cell_type, len(nodes), nodes)

        data.SetPoints(points)
        data.GetPointData().SetScalars(point_colors)
        data.GetCellData().SetScalars(cell_colors)

        self.data = data
        mapper.SetInputData(self.data)
        self.SetMapper(mapper)

    def update_coordinates(self, coordinates):
        points = self.data.GetPoints()
        for i, xyz in enumerate(coordinates):
            points.SetPoint(i, xyz)
        points.Modified()

    def configure_appearance(self):
        self.GetProperty().SetInterpolationToPhong()
        self.GetProperty().SetPointSize(3)
        self.GetProperty().SetLineWidth(0.1)
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

    def paint_cells(self, color: tuple[3], volumes: tuple[int]):

        if self.data is None:
            return

        cell_colors = self.data.GetCellData().GetScalars()
        for i in volumes:
            cell_colors.SetTuple(i, color)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()
    
    def apply_cut(self, origin, normal):
        plane = vtk.vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)

        clipper = vtk.vtkExtractGeometry()
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
