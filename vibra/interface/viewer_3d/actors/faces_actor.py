from typing import Optional

from molde import Color
from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_QUAD,
    VTK_QUADRATIC_QUAD,
    VTK_QUADRATIC_TRIANGLE,
    VTK_TRIANGLE,
    vtkPlane,
    vtkPolyData,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper, vtkPolyDataMapper

from vibra import app
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.utils.interface_utils import GeometryColorMode, VisualizationFilter


class FacesActor(vtkActor):
    NODES_TO_VTK_CELL = {
        3: VTK_TRIANGLE,
        6: VTK_QUADRATIC_TRIANGLE,
        4: VTK_QUAD,
        8: VTK_QUADRATIC_QUAD,
    }

    def __init__(
        self,
        mesh: Mesh,
        allow_hidding=True,
        update_normals=True,
        visualization_filter: Optional[VisualizationFilter] = None,
    ):
        self.visualization_filter = visualization_filter
        if self.visualization_filter is None:
            self.visualization_filter = VisualizationFilter.all_true()

        self.mesh = mesh
        self.data = None
        self.allow_hidding = allow_hidding
        self.update_normals = update_normals

        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        if self.mesh.nodal_coordinates.size == 0:
            return

        number_of_nodes = self.mesh.nodal_coordinates.shape[0]
        number_of_elements = len(self.mesh.faces_connectivity)
        nodes_per_element = len(self.mesh.faces_connectivity[0, 4:])

        if nodes_per_element in [6, 8]:
            data = vtkUnstructuredGrid()
            mapper = vtkDataSetMapper()
        else:
            data = vtkPolyData()
            mapper = vtkPolyDataMapper()

        points = vtkPoints()
        point_colors = vtkFloatArray()
        point_colors.SetNumberOfTuples(number_of_nodes)
        point_colors.Fill(0)

        cell_colors = vtkUnsignedCharArray()
        cell_colors.SetNumberOfComponents(4)
        cell_colors.SetNumberOfTuples(number_of_elements)
        cell_colors.Fill(0)

        face_indexes = vtkIntArray()
        face_indexes.SetName("face_indexes")
        face_indexes.Allocate(number_of_elements)

        surface_indexes = vtkIntArray()
        surface_indexes.SetName("surface_indexes")
        surface_indexes.Allocate(number_of_elements)

        volume_indexes = vtkIntArray()
        volume_indexes.SetName("volume_indexes")
        volume_indexes.Allocate(number_of_elements)

        cell_type = self.NODES_TO_VTK_CELL[nodes_per_element]
        data.Allocate(nodes_per_element * number_of_elements)

        coordinates = self.mesh.nodal_coordinates[:, 1:]
        points.SetData(numpy_to_vtk(coordinates))

        surface_to_volume = dict()
        for volume, surfaces in self.mesh.surfaces_from_volume.items():
            for surface in surfaces:
                surface_to_volume[surface] = volume

        self.visible_indexes = dict()
        hidden_surfaces = app().main_window.entity_visibility.get_hidden_surfaces()
        if not self.allow_hidding:
            hidden_surfaces.clear()

        for i, surface, _, _, *values in self.mesh.faces_connectivity:
            if surface in hidden_surfaces:
                continue

            volume = surface_to_volume.get(surface, -1)
            surface_indexes.InsertNextValue(surface)
            volume_indexes.InsertNextValue(volume)

            # This is usefull if part of the cells are hidden
            visible_index = face_indexes.InsertNextValue(i)
            self.visible_indexes[i] = visible_index
            data.InsertNextCell(cell_type, nodes_per_element, list(values))

        data.SetPoints(points)
        data.GetPointData().SetScalars(point_colors)
        data.GetCellData().SetScalars(cell_colors)
        data.GetCellData().AddArray(face_indexes)
        data.GetCellData().AddArray(surface_indexes)
        data.GetCellData().AddArray(volume_indexes)

        # Updating normals messes with the colors
        # this is why this option exists.
        if self.update_normals and isinstance(data, vtkPolyData):
            normals_filter = vtkPolyDataNormals()
            normals_filter.AddInputData(data)
            normals_filter.Update()
            self.data = normals_filter.GetOutput()
        else:
            self.data = data

        mapper.SetInputData(self.data)
        self.SetMapper(mapper)
        self.clear_colors()

    def configure_appearance(self):
        self.GetProperty().SetInterpolationToPhong()
        self.GetProperty().SetDiffuse(0.8)
        self.GetProperty().SetSpecular(0.5)
        self.GetProperty().SetSpecularPower(40)
        self.GetProperty().SetSpecularColor(1, 1, 1)
        self.clear_colors()

    def clear_colors(self):
        if self.data is None:
            return

        mesh = app().project.model.mesh
        properties = app().project.model.properties
        color_mode = self.visualization_filter.color_mode
        no_info_color = Color(20, 20, 20)

        if color_mode == GeometryColorMode.MATERIAL:
            for surface, face_elements in mesh.elements_from_surface.items():
                material: Material | None = properties._get_property("material", surface=surface)

                if (material is None) and (surface in mesh.volumes_from_surface):
                    volume = mesh.volumes_from_surface[surface][0]
                    material = properties._get_property("material", volume=volume)

                color = Color(*material.color) if (material is not None) else no_info_color
                self.paint_cells(color, face_elements)

        elif color_mode == GeometryColorMode.FLUID:
            for surface, face_elements in mesh.elements_from_surface.items():
                fluid: Fluid | None = properties._get_property("fluid", surface=surface)

                if (fluid is None) and (surface in mesh.volumes_from_surface):
                    volume = mesh.volumes_from_surface[surface][0]
                    fluid = properties._get_property("fluid", volume=volume)

                color = Color(*fluid.color) if (fluid is not None) else no_info_color
                self.paint_cells(color, face_elements)

        elif color_mode == GeometryColorMode.EMPTY:
            color = app().config.user_preferences.faces_color
            self.set_color(color)

    def set_color(self, color: Color):
        if self.data is None:
            return

        cell_colors = self.data.GetCellData().GetScalars()
        cell_colors.Fill(255)

        color = color.to_rgba()
        for component, value in enumerate(color):
            cell_colors.FillComponent(component, value)

        self.data.Modified()
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_points(self, color: Color, points):
        if self.data is None:
            return

        color = color.to_rgb()
        point_colors = self.data.GetPointData().GetScalars()
        for i in points:
            point_colors.SetTuple(i, color)

        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def paint_cells(self, color: Color, faces: tuple[int]):
        if self.data is None:
            return

        color = color.to_rgba()
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
