import numpy as np
from molde import Color
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    VTK_QUADRATIC_HEXAHEDRON,
    VTK_QUADRATIC_TETRA,
    VTK_TETRA,
    VTK_TRIANGLE,
    vtkCellArray,
    vtkPlane,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper, vtkPropAssembly

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.properties import Fluid, Material
from vibra.utils.math_functions import inside_plane
from vibra.utils.time_utils import function_timer


class MeshActor(vtkPropAssembly):
    def __init__(self, model: Model):
        self.model = model

        self.create_variables()
        self.last_mesh_id = 0

    @property
    def mesh(self) -> Mesh | None:
        if self.model is None:
            return

        return self.model.mesh

    def update(self):
        self.build_surface()
        self.update_section_plane()
        self.clear_colors()

    def create_variables(self):
        self.points = vtkPoints()

        self.surface_cells = vtkCellArray()
        self.surface_colors = vtkUnsignedCharArray()
        self.surface_colors.SetName("color")
        self.surface_colors.SetNumberOfComponents(3)

        self.surface_data = vtkUnstructuredGrid()
        self.surface_data.SetPoints(self.points)
        self.surface_data.GetCellData().SetScalars(self.surface_colors)

        self.surface_mapper = vtkDataSetMapper()
        self.surface_mapper.SetInputData(self.surface_data)

        self.surface_actor = vtkActor()
        self.surface_actor.SetMapper(self.surface_mapper)
        self.AddPart(self.surface_actor)

        self.section_cells = vtkCellArray()
        self.section_colors = vtkUnsignedCharArray()
        self.section_colors.SetName("color")
        self.section_colors.SetNumberOfComponents(3)

        self.section_data = vtkUnstructuredGrid()
        self.section_data.SetPoints(self.points)
        self.section_data.GetCellData().SetScalars(self.section_colors)

        self.section_mapper = vtkDataSetMapper()
        self.section_mapper.SetInputData(self.section_data)

        self.section_actor = vtkActor()
        self.section_actor.SetMapper(self.section_mapper)
        self.AddPart(self.section_actor)

    @function_timer
    def build_surface(self):
        if self.mesh is None:
            return

        mesh_id = id(self.mesh)
        if mesh_id == self.last_mesh_id:
            return
        self.last_mesh_id = mesh_id

        coordinates = self.mesh.nodal_coordinates[:, 1:]
        self.points.SetData(numpy_to_vtk(coordinates))

        connectivity = self.mesh.faces_connectivity[:, 4:]
        n_cells = len(connectivity)
        cell_type = VTK_TRIANGLE

        helper = np.insert(connectivity, 0, connectivity.shape[1], axis=1)
        vtk_id_array = numpy_to_vtkIdTypeArray(helper.flatten())
        self.surface_cells.SetCells(n_cells, vtk_id_array)

        self.surface_data.SetCells(cell_type, self.surface_cells)
        self.surface_colors.SetNumberOfTuples(n_cells)
        self.surface_mapper.Modified()

    @function_timer
    def update_section_plane(self):
        if self.mesh is None:
            return

        origin = np.array([0, 0, 0])
        normal = np.array([0, 0, -1])

        plane = vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)

        self.surface_mapper.RemoveAllClippingPlanes()
        self.surface_mapper.AddClippingPlane(plane)
        self.surface_mapper.Modified()
        self.surface_actor.Modified()

        coordinates = self.mesh.nodal_coordinates[:, 1:]
        connectivity = self.mesh.solids_connectivity[:, 4:]
        mask = inside_plane(coordinates, origin, normal).flatten()

        elements_inside_plane = np.all(mask[connectivity], axis=1)
        elements_outside_plane = ~np.any(mask[connectivity], axis=1)
        elements_in_middle = ~(elements_inside_plane | elements_outside_plane)

        filtered_connectivity = connectivity[elements_in_middle]
        n_cells = len(filtered_connectivity)
        cell_type = VTK_TETRA

        helper = np.insert(filtered_connectivity, 0, filtered_connectivity.shape[1], axis=1)
        vtk_id_array = numpy_to_vtkIdTypeArray(helper.flatten())
        self.section_cells.SetCells(n_cells, vtk_id_array)

        self.section_data.SetCells(cell_type, self.section_cells)
        self.section_colors.SetNumberOfTuples(n_cells)
        self.section_mapper.Modified()

    @function_timer
    def clear_colors(self):
        if self.model is None:
            return

        for v in self.model.properties.volume_properties.values():
            if isinstance(v, Fluid | Material):
                self.set_color(Color.from_rgb(*v.color))
                return

        self.set_color(Color(255, 255, 255))

    def set_color(self, color: Color):
        rgb = color.to_rgb()
        for i in range(self.surface_colors.GetNumberOfComponents()):
            self.surface_colors.FillComponent(i, rgb[i])
            self.section_colors.FillComponent(i, rgb[i])

        self.surface_colors.Modified()
        self.section_colors.Modified()
