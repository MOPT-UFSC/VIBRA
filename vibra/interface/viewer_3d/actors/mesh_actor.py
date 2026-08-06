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
from vibra.engine.mesher.mesh_setup import ElementTopology
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
        self.build_surfaces()
        self.update_section_plane()
        self.clear_colors()

    def create_variables(self):
        self.points = vtkPoints()
        self.surface_cells = vtkCellArray()
        self.section_cells = vtkCellArray()

        self.colors = vtkUnsignedCharArray()
        self.colors.SetName("color")
        self.colors.SetNumberOfComponents(3)

        self.data = vtkUnstructuredGrid()
        self.data.SetPoints(self.points)
        self.data.GetCellData().SetScalars(self.colors)

        self.surfaces_mapper = vtkDataSetMapper()
        self.surfaces_mapper.SetInputData(self.data)

        self.surfaces_actor = vtkActor()
        self.surfaces_actor.SetMapper(self.surfaces_mapper)
        self.AddPart(self.surfaces_actor)

    @function_timer
    def build_surfaces(self):
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

        self.data.SetCells(cell_type, self.surface_cells)
        self.colors.SetNumberOfTuples(n_cells)

        self.surfaces_mapper.Modified()

    @function_timer
    def update_section_plane(self):
        if self.mesh is None:
            return

        origin = np.array([0, 0, 0])
        normal = np.array([0, 0, -1])

        plane = vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)

        self.surfaces_mapper.RemoveAllClippingPlanes()
        self.surfaces_mapper.AddClippingPlane(plane)
        self.surfaces_mapper.Modified()
        self.surfaces_actor.Modified()

        coordinates = self.mesh.nodal_coordinates[:, 1:]
        connectivity = self.mesh.solids_connectivity[:, 4:]
        mask = inside_plane(coordinates, origin, normal).flatten()

        elements_inside_plane = np.all(mask[connectivity], axis=1)
        elements_outside_plane = ~np.any(mask[connectivity], axis=1)
        elements_in_middle = ~(elements_inside_plane & elements_outside_plane)

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
        for i in range(self.colors.GetNumberOfComponents()):
            self.colors.FillComponent(i, rgb[i])

        self.colors.Modified()
        self.surfaces_mapper.Modified()
