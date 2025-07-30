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
    NODES_TO_VTK_CELL = {
        3: VTK_TRIANGLE,
        6: VTK_QUADRATIC_TRIANGLE,
        4: VTK_QUAD,
        8: VTK_QUADRATIC_QUAD,
    }

    def __init__(self, mesh: Mesh | None = None):
        self.mesh = mesh
        if self.mesh is None:
            self.mesh = app().project.model.mesh
        self.create_geometry()

    def create_geometry(self):
        if self.mesh.nodal_coordinates.size == 0:
            return

        self._create_data()
        self._create_textures()
        self._create_material_actor()
        self._create_fluid_actor()
        # self._create_porous_actor()

    def _create_data(self):
        number_of_face_elements = len(self.mesh.faces_connectivity)
        nodes_per_face_element = len(self.mesh.faces_connectivity[0, 4:])
        coordinates = self.mesh.nodal_coordinates[:, 1:]

        points = vtkPoints()
        points.SetData(numpy_to_vtk(coordinates))

        helper = np.insert(
            self.mesh.faces_connectivity[:, 4:],
            0,  # index
            nodes_per_face_element,
            axis=1,
        ).flatten()
        cells = vtk.vtkCellArray()
        cells.SetCells(number_of_face_elements, numpy_to_vtkIdTypeArray(helper))

        material_colors = vtkUnsignedCharArray()
        material_colors.SetName("material_colors")
        material_colors.SetNumberOfComponents(4)
        material_colors.SetNumberOfTuples(number_of_face_elements)
        material_colors.Fill(0)

        fluid_colors = vtkUnsignedCharArray()
        fluid_colors.SetName("fluid_colors")
        fluid_colors.SetNumberOfComponents(4)
        fluid_colors.SetNumberOfTuples(number_of_face_elements)
        fluid_colors.Fill(255)

        data = vtkPolyData()
        data.SetPoints(points)
        data.SetPolys(cells)
        data.GetCellData().AddArray(material_colors)
        data.GetCellData().AddArray(fluid_colors)

        add_normals = vtkPolyDataNormals()
        add_normals.SetInputData(data)
        add_normals.Update()

        add_tcoords = vtk.vtkTextureMapToCylinder()
        add_tcoords.SetInputData(add_normals.GetOutput())
        add_tcoords.PreventSeamOn()
        add_tcoords.Update()

        add_tangents = vtk.vtkPolyDataTangents()
        add_tangents.SetInputData(add_tcoords.GetOutput())
        add_tangents.Update()

        self.data = add_tangents.GetOutput()

        # self.data = vtkUnstructuredGrid()
        # self.data.DeepCopy(tangents.GetOutput())

    def _create_material_actor(self):
        number_of_face_elements = len(self.mesh.faces_connectivity)

        self.material_extractor = vtkExtractCells()
        self.data >> self.material_extractor
        self.material_extractor.cell_list = create_vtk_id_list(
            np.arange(0, number_of_face_elements // 2)
        )

        material_mapper = vtkDataSetMapper()
        self.material_extractor >> material_mapper

        self.material_actor = vtkActor(mapper=material_mapper)
        self.AddPart(self.material_actor)

        actor_property = self.material_actor.GetProperty()
        actor_property.SetInterpolationToPBR()

        actor_property.color = (1, 1, 1)
        actor_property.metallic = 0.5
        actor_property.roughness = 0.8
        actor_property.SetEmissiveFactor(1, 0, 0)
        # actor_property.normal_scale = 2
        # actor_property.normal_texture = self.material_normal_texture

    def _create_fluid_actor(self):
        number_of_face_elements = len(self.mesh.faces_connectivity)

        self.fluid_extractor = vtkExtractCells()
        self.data >> self.fluid_extractor
        self.fluid_extractor.cell_list = create_vtk_id_list(
            np.arange(number_of_face_elements // 2, number_of_face_elements)
        )

        fluid_mapper = vtkDataSetMapper()
        self.fluid_extractor >> fluid_mapper

        self.fluid_actor = vtkActor(mapper=fluid_mapper)
        self.AddPart(self.fluid_actor)

        actor_property = self.fluid_actor.GetProperty()
        actor_property.SetInterpolationToPBR()

        actor_property.color = (1, 0.2, 0.2)
        actor_property.opacity = 0.99
        actor_property.metallic = 0.6
        actor_property.roughness = 0.3
        actor_property.normal_texture = self.fluid_normal_texture
    
    def _create_porous_actor(self):
        number_of_face_elements = len(self.mesh.faces_connectivity)

        self.porous_extractor = vtkExtractCells()
        self.data >> self.porous_extractor
        self.porous_extractor.cell_list = create_vtk_id_list(
            np.arange(number_of_face_elements // 2, number_of_face_elements)
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
        self.fluid_normal_texture = read_texture(TEXTURE_DIR / "water_normal.jpg")
        self.material_normal_texture = read_texture(TEXTURE_DIR / "metal_normal.jpg")
        self.porous_normal_texture = read_texture(TEXTURE_DIR / "foam_normal.jpg")
