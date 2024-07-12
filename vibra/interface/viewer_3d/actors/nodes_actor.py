
from vibra.engine.mesher.element_type import *

import vtk
import numpy as np
from time import time


class NodesActor(vtk.vtkActor):
    def __init__(self, mesh, hidden_nodes=None):
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
        data = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        mapper = vtk.vtkPolyDataMapper()
        cell_colors = vtk.vtkUnsignedCharArray()
        cell_indexes = vtk.vtkIntArray()
        cell_indexes.SetName("cell_indexes")

        data.Allocate(len(self.mesh.nodal_coordinates))
        cell_colors.SetNumberOfComponents(4)
        cell_colors.SetNumberOfTuples(len(self.mesh.nodal_coordinates))
        cell_colors.Fill(0)
        cell_indexes.SetNumberOfTuples(len(self.mesh.nodal_coordinates))

        for i, (x, y, z) in enumerate(self.get_coordinates()):
            cell_indexes.InsertValue(i, i)  # This is usefull if part of the cells are hidden
            points.InsertNextPoint(x, y, z)
            data.InsertNextCell(vtk.VTK_VERTEX, 1, [i])

        data.SetPoints(points)
        data.GetCellData().SetScalars(cell_colors)
        data.GetCellData().AddArray(cell_indexes)
        self.data = data 

        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)

    def update_coordinates(self, coordinates):
        points: vtk.vtkPoints
        points = self.data.GetPoints()
        for i, xyz in enumerate(coordinates):
            points.SetPoint(i, xyz)
        points.Modified()

    def configure_appearance(self):
        self.GetProperty().RenderPointsAsSpheresOn()
        self.GetProperty().SetPointSize(10)
        self.GetProperty().LightingOff()
        self.clear_colors((0, 0, 0, 0))

    def clear_colors(self, color=(255, 255, 255, 255)):
        if self.data is None:
            return

        cell_colors = self.data.GetCellData().GetScalars()
        r, g, b, a = color

        cell_colors.FillComponent(0, r)
        cell_colors.FillComponent(1, g)
        cell_colors.FillComponent(2, b)
        cell_colors.FillComponent(3, a)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_cells(self, color: tuple[int, int, int] | tuple[int, int, int, int], volumes: tuple[int]):
        if self.data is None:
            return

        if len(color) == 3:
            color = *color, 255

        cell_colors = self.data.GetCellData().GetScalars()
        for i in volumes:
            cell_colors.SetTuple(i, color)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()
    
    def disable_cut(self):
        self.GetMapper().RemoveAllClippingPlanes()

    def apply_cut(self, origin, normal):
        plane = vtk.vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)
        self.GetMapper().RemoveAllClippingPlanes()
        self.GetMapper().AddClippingPlane(plane)
    