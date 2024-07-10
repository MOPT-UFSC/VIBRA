
from vibra.engine.mesher.element_type import *

import vtk
import numpy as np
from time import time


class NodesActor(vtk.vtkActor):
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
        data = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        mapper = vtk.vtkPolyDataMapper()
        cell_colors = vtk.vtkUnsignedCharArray()

        data.Allocate(len(self.mesh.nodal_coordinates))
        cell_colors.SetNumberOfComponents(3)
        cell_colors.SetNumberOfTuples(len(self.mesh.nodal_coordinates))
        cell_colors.FillComponent(0, 0)
        cell_colors.FillComponent(1, 0)
        cell_colors.FillComponent(2, 1)

        for i, (x, y, z) in enumerate(self.get_coordinates()):
            points.InsertNextPoint(x, y, z)
            data.InsertNextCell(vtk.VTK_VERTEX, 1, [i])

        data.SetPoints(points)
        data.GetCellData().SetScalars(cell_colors)
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
        self.GetProperty().SetPointSize(8)
        self.GetProperty().LightingOff()
        self.clear_colors()

    def clear_colors(self):
        if self.data is None:
            return

        cell_colors = self.data.GetCellData().GetScalars()

        r, g, b = self.GetProperty().GetColor()
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)

        cell_colors.FillComponent(0, r)
        cell_colors.FillComponent(1, g)
        cell_colors.FillComponent(2, b)

        self.GetMapper().ScalarVisibilityOff()

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