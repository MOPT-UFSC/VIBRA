from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
    vtkIdList,
)
from typing import Sequence
import numpy as np
from vtkmodules.vtkCommonDataModel import (
    VTK_QUAD,
    VTK_QUADRATIC_QUAD,
    VTK_QUADRATIC_TRIANGLE,
    VTK_TRIANGLE,
    vtkPlane,
    vtkPolyData,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals, vtkExtractCells
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPropAssembly,
    vtkPolyDataMapper,
    vtkDataSetMapper,
)

from vibra import app, TEXTURE_DIR
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.utils.interface_utils import ColorMode
from vibra.utils.polydata_utils import fill_array
from molde import Color
import vtk


def create_vtk_id_list(id_list: Sequence[int]) -> vtkIdList:
    vtk_id_list = vtkIdList()
    for id in id_list:
        vtk_id_list.InsertNextId(id)
    return vtk_id_list


def read_texture(filename: str):
    reader = vtk.vtkJPEGReader()
    reader.SetFileName(filename)
    reader.Update()

    texture = vtk.vtkTexture()
    texture.InterpolateOn()
    texture.SetInputData(reader.GetOutput())
    texture.Update

    return texture


class MultimaterialGeometryActor(vtkPropAssembly):
    def __init__(self, mesh: Mesh | None = None):
        self.mesh = mesh
        if self.mesh is None:
            self.mesh = app().project.model.mesh
        self.create_geometry()

    def create_geometry(self):
        if self.mesh.nodal_coordinates.size == 0:
            return

        self._create_surfaces()
        self._create_textures()
        self._create_material_actor()
        # self._create_fluid_actor()
        # self._create_porous_actor()

    def _create_surfaces(self):
        nodes_per_element = len(self.mesh.faces_connectivity[0, 4:])

        combined_surfaces = vtk.vtkAppendPolyData()
        for surface, elements in self.mesh.elements_from_surface.items():
            coords, connect = self._reduce_connectivity(
                self.mesh.nodal_coordinates[:, 1:],
                self.mesh.faces_connectivity[elements, 4:],
            )

            points = vtkPoints()
            points.SetData(numpy_to_vtk(coords))

            cells = vtk.vtkCellArray()
            helper = np.insert(connect, 0, nodes_per_element, axis=1)
            vtk_id_array = numpy_to_vtkIdTypeArray(helper.flatten())
            cells.SetCells(len(connect), vtk_id_array)

            data = vtkPolyData()
            data.SetPoints(points)
            data.SetPolys(cells)

            volume = self.mesh.volumes_from_surface[surface][0]
            fill_array(data, "surface_indexes", surface)
            fill_array(data, "volume_indexes", volume)

            # Every surface have its own plane defining
            # how to project the texture coordinates
            add_tcoords = vtk.vtkTextureMapToPlane()
            add_tcoords.SetInputData(data)
            add_tcoords.SetSRange(0, 10)
            add_tcoords.SetTRange(0, 10)
            add_tcoords.Update()

            combined_surfaces.AddInputData(add_tcoords.GetOutput())

        combined_surfaces.Update()

        add_normals = vtkPolyDataNormals()
        add_normals.SetInputData(combined_surfaces.GetOutput())
        add_normals.Update()

        add_tangents = vtk.vtkPolyDataTangents()
        add_tangents.SetInputData(add_normals.GetOutput())
        add_tangents.Update()

        self.data: vtkPolyData = add_tangents.GetOutput()

        fill_array(self.data, "material_color", (255, 255, 0, 255))
        fill_array(self.data, "fluid_color", (0, 255, 0, 255))

    def _reduce_connectivity(
        self,
        coords: np.ndarray,
        connectivity: np.ndarray,
        mapping: np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        old_indexes = np.unique(connectivity)
        new_indexes = np.arange(len(old_indexes))

        if mapping is None:
            mapping = np.zeros(np.max(connectivity) + 1, dtype=int)
        mapping[old_indexes] = new_indexes

        return coords[old_indexes], mapping[connectivity]

    def _create_material_actor(self):
        material_mapper = vtkPolyDataMapper()
        self.data >> material_mapper
        material_mapper.SetScalarModeToUseCellFieldData()
        material_mapper.SetColorModeToDirectScalars()
        material_mapper.SelectColorArray("fluid_color")
        material_mapper.ScalarVisibilityOn()

        self.material_actor = vtkActor(mapper=material_mapper)
        self.AddPart(self.material_actor)

        actor_property = self.material_actor.GetProperty()
        actor_property.SetInterpolationToPhong()
        actor_property.specular_power = 80
        actor_property.specular = 1.5
        actor_property.diffuse = 0.6
        actor_property.normal_scale = 0.5
        actor_property.normal_texture = self.material_normal_texture

    def _create_fluid_actor(self):
        fluid_mapper = vtkDataSetMapper()
        self.data >> fluid_mapper
        fluid_mapper.SetScalarModeToUseCellFieldData()
        fluid_mapper.SelectColorArray("fluid_color")
        fluid_mapper.ScalarVisibilityOn()

        self.fluid_actor = vtkActor(mapper=fluid_mapper)
        self.AddPart(self.fluid_actor)

        actor_property = self.fluid_actor.GetProperty()
        actor_property.color = Color(190, 190, 255).to_rgb_f()
        actor_property.specular_color = (1, 1, 1)
        actor_property.specular_power = 40
        actor_property.specular = 0.7
        actor_property.normal_scale = 2
        actor_property.normal_texture = self.fluid_normal_texture

    def _create_porous_actor(self):
        number_of_face_elements = len(self.mesh.faces_connectivity)

        self.porous_extractor = vtkExtractCells()
        self.data >> self.porous_extractor
        self.porous_extractor.cell_list = create_vtk_id_list(
            np.arange(0, number_of_face_elements // 2)
        )

        porous_mapper = vtkDataSetMapper()
        self.porous_extractor >> porous_mapper

        self.porous_actor = vtkActor(mapper=porous_mapper)
        self.AddPart(self.porous_actor)

        actor_property = self.porous_actor.GetProperty()
        actor_property.SetInterpolationToPBR()

        actor_property.color = (0.03, 0.03, 0.03)
        actor_property.opacity = 1
        actor_property.metallic = 0.2
        actor_property.roughness = 0.9
        actor_property.normal_texture = self.porous_normal_texture
        actor_property.normal_scale = 5

    def _create_textures(self):
        self.fluid_normal_texture = read_texture(TEXTURE_DIR / "perlin_normal.jpg")
        self.material_normal_texture = read_texture(TEXTURE_DIR / "metal_normal.jpg")
        self.porous_normal_texture = read_texture(TEXTURE_DIR / "foam_normal.jpg")
