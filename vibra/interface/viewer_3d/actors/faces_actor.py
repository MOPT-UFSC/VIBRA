from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPolyData,
    VTK_TRIANGLE,
    VTK_QUADRATIC_TRIANGLE,
    VTK_QUAD,
    VTK_QUADRATIC_QUAD
)
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
from vtkmodules.util.numpy_support import numpy_to_vtk

from vibra import app


class FacesActor(vtkActor):
    def __init__(self, mesh, allow_hidding=True, update_normals=True):
        self.mesh = mesh
        self.data = None
        self.allow_hidding = allow_hidding
        self.update_normals = update_normals

        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        #
        data = vtkPolyData()
        points = vtkPoints()
        mapper = vtkPolyDataMapper()
        point_colors = vtkUnsignedCharArray()
        cell_colors = vtkUnsignedCharArray()
        cell_indexes = vtkIntArray()
        cell_indexes.SetName("cell_indexes")
        cell_colors.Fill(0)
        
        number_of_nodes = self.mesh.nodal_coordinates.shape[0]
        number_of_elements = len(self.mesh.faces_connectivity)
        nodes_per_element = len(self.mesh.faces_connectivity[0, 4:])

        face_nodes = [3, 6, 4, 8]
        types = [VTK_TRIANGLE, VTK_QUADRATIC_TRIANGLE, VTK_QUAD, VTK_QUADRATIC_QUAD]
        aux = dict(zip(face_nodes, types))
        try:
            cell_type = aux[nodes_per_element]
        except:
            raise NotImplementedError("Not implemented plane element")

        data.Allocate(nodes_per_element * number_of_elements)

        point_colors.SetNumberOfComponents(3)
        point_colors.SetNumberOfTuples(number_of_nodes)
        cell_colors.SetNumberOfComponents(4)
        cell_colors.SetNumberOfTuples(number_of_elements)
        cell_indexes.Allocate(number_of_elements)

        coordinates = self.mesh.nodal_coordinates[:, 1:]
        points.SetData(numpy_to_vtk(coordinates))

        self.visible_indexes = dict()
        hidden_surfaces = app().main_window.hidden_surfaces if self.allow_hidding else set()
        # for i, values in enumerate(self.mesh.faces_connectivity[:, 4:]):
        for i, surface, _, _, *values in self.mesh.faces_connectivity:
            if surface in hidden_surfaces:
                continue

            # This is usefull if part of the cells are hidden
            visible_index = cell_indexes.InsertNextValue(i)
            self.visible_indexes[i] = visible_index
            data.InsertNextCell(cell_type, nodes_per_element, list(values))

        data.SetPoints(points)
        data.GetPointData().SetScalars(point_colors)
        data.GetCellData().SetScalars(cell_colors)
        data.GetCellData().AddArray(cell_indexes)

        # Updating the normals messes with the colors
        # this is why this option exists.
        if self.update_normals:
            normals_filter = vtkPolyDataNormals()
            normals_filter.AddInputData(data)
            normals_filter.Update()
            self.data = normals_filter.GetOutput()
        else:
            self.data = data

        mapper.SetInputData(self.data)
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().SetInterpolationToPhong()
        self.GetProperty().SetDiffuse(0.8)
        self.GetProperty().SetSpecular(0.5)
        self.GetProperty().SetSpecularPower(40)
        self.GetProperty().SetSpecularColor(1, 1, 1)
        self.clear_colors()

    def clear_colors(self, color=(255, 255, 255, 255)):
        if self.data is None:
            return

        self.set_color(color)

    def set_color(self, color: tuple[int, int, int, int] | tuple[int, int, int]):
        # TODO: Use this function instead of clear colors directly

        cell_colors = self.data.GetCellData().GetScalars()
        cell_colors.Fill(255)

        for component, value in enumerate(color):
            cell_colors.FillComponent(component, value)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_points(self, color, points):
        if self.data is None:
            return

        point_colors = self.data.GetPointData().GetScalars()
        for i in points:
            point_colors.SetTuple(i, color)

        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_cells(
        self,
        color: tuple[int, int, int] | tuple[int, int, int, int],
        faces: tuple[int],
    ):
        if self.data is None:
            return

        if len(color) == 3:
            color = *color, 255

        cell_colors = self.data.GetCellData().GetScalars()
        for i in faces:
            visible_index = self.visible_indexes.get(i, -1)
            if visible_index >= 0:
                cell_colors.SetTuple(visible_index, color)

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
