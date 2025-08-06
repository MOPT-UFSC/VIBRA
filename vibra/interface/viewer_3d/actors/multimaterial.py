from vtkmodules.util.numpy_support import (
    numpy_to_vtk,
    numpy_to_vtkIdTypeArray,
    vtk_to_numpy,
)
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
from pathlib import Path
from time import perf_counter
from collections import defaultdict


def create_vtk_id_list(id_list: Sequence[int]) -> vtkIdList:
    vtk_id_list = vtkIdList()
    for id in id_list:
        vtk_id_list.InsertNextId(id)
    return vtk_id_list


def read_texture(path: str | Path | None):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f'Texture file "{path}" not found')

    if path.suffix == ".png":
        reader = vtk.vtkPNGReader()
    elif path.suffix == ".jpg":
        reader = vtk.vtkJPEGReader()
    else:
        raise ValueError(f"Unsupported image format {path.suffix}")

    reader.SetFileName(path)
    reader.Update()

    texture = vtk.vtkTexture()
    texture.InterpolateOn()
    texture.RepeatOn()
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

        t0 = perf_counter()
        self._create_surfaces()
        t1 = perf_counter()
        self._create_textures()
        t2 = perf_counter()
        self._create_empty_actor()
        t3 = perf_counter()
        self._create_material_actor()
        t4 = perf_counter()
        self._create_fluid_actor()
        t5 = perf_counter()
        self._create_porous_actor()
        t6 = perf_counter()
        self.clear_colors()
        t7 = perf_counter()
        self.reload_composition()
        t8 = perf_counter()

        print("Multimaterial times:")
        print(t1 - t0)
        print(t2 - t1)
        print(t3 - t2)
        print(t4 - t3)
        print(t5 - t4)
        print(t6 - t5)
        print(t7 - t6)
        print(t8 - t7)
        print()

    def clear_colors(self):
        mesh = app().project.model.mesh
        properties = app().project.model.properties
        color_to_surfaces = defaultdict(list)

        for surface, volumes in mesh.volumes_from_surface.items():
            volume = volumes[0]
            fluid = properties._get_property("fluid", surface=surface, volume=volume)
            material = properties._get_property("material", surface=surface, volume=volume)

            if material is not None:
                color = tuple(material.color)
            elif fluid is not None:
                color = tuple(fluid.color)
            else:
                color = (255, 255, 255)

            color_to_surfaces[color].append(surface)

        for color, surfaces in color_to_surfaces.items():
            self.paint_surfaces(Color(*color), surfaces)

        # This is pretty slow, need to find a better way to update
        self.reload_composition()

    def reload_composition(self):
        mesh = app().project.model.mesh
        properties = app().project.model.properties
        composition_to_surfaces = defaultdict(list)

        for surface, volumes in mesh.volumes_from_surface.items():
            volume = volumes[0]
            fluid = properties._get_property("fluid", surface=surface, volume=volume)
            material = properties._get_property("material", surface=surface, volume=volume)

            if material is not None:
                composition = "material"
            elif fluid is not None:
                composition = "fluid"
            else:
                composition = "empty"

            composition_to_surfaces[composition].append(surface)

        self.clear_composition()
        for composition, surfaces in composition_to_surfaces.items():
            self.configure_composition(composition, surfaces)

    def set_color(self, color: Color):
        for i, c in enumerate(color.to_rgba()):
            self.cell_colors.FillComponent(i, c)

    def paint_surfaces(self, color: Color, surfaces: Sequence[int]):
        cells = self._surfaces_to_cells(surfaces)
        self.paint_cells(color, cells)

    def paint_cells(self, color: Color, cells: Sequence[int]):
        color_fmt = color.to_rgba()
        array = vtk_to_numpy(self.cell_colors)
        array[cells] = color_fmt
        self.data.Modified()

        collection = vtk.vtkActorCollection()
        self.GetActors(collection)
        for actor in collection:
            actor: vtkActor
            actor.GetMapper().SetScalarModeToUseCellData()
            actor.GetMapper().ScalarVisibilityOff()  # Just to force color updates
            actor.GetMapper().ScalarVisibilityOn()

    def configure_composition(self, constitution: str, surfaces: Sequence[int]):
        if constitution == "empty":
            extractor = self.empty_extractor
        elif constitution == "material":
            extractor = self.material_extractor
        elif constitution == "fluid":
            extractor = self.fluid_extractor
        elif constitution == "porous":
            extractor = self.porous_extractor
        else:
            raise ValueError(f'Unknown constitution: "{constitution}"')

        cells = self._surfaces_to_cells(surfaces)
        extractor.AddCellIds(cells, len(cells))

    def clear_composition(self):
        self.material_extractor.SetCellIds([], 0)
        self.fluid_extractor.SetCellIds([], 0)
        self.porous_extractor.SetCellIds([], 0)
        self.empty_extractor.SetCellIds([], 0)

    def _surfaces_to_cells(self, surfaces: Sequence[int]) -> np.ndarray:
        array = vtk_to_numpy(self.data.GetCellData().GetArray("surface_indexes"))
        mask = np.isin(array, list(surfaces))
        return np.where(mask)[0]

    def _create_surfaces(self):
        nodes_per_element = len(self.mesh.faces_connectivity[0, 4:])

        combined_surfaces = vtk.vtkAppendPolyData()
        for surface, elements in self.mesh.elements_from_surface.items():
            coords, connect = self._reduce_connectivity(
                self.mesh.nodal_coordinates[:, 1:],
                self.mesh.faces_connectivity[elements, 4:],
            )

            points = vtkPoints()
            points.SetData(numpy_to_vtk(coords + (1, 0, 0)))

            # The format here is [n, p0, p1, ..., pn, n, p0, p1, ..., pn]
            # Therefore I add a "n" column at the start and then flatten it
            cells = vtk.vtkCellArray()
            helper = np.insert(connect, 0, nodes_per_element, axis=1)
            vtk_id_array = numpy_to_vtkIdTypeArray(helper.flatten())
            cells.SetCells(len(connect), vtk_id_array)

            data = vtkPolyData()
            data.SetPoints(points)
            data.SetPolys(cells)

            volume = self.mesh.volumes_from_surface[surface][0]

            # Every surface have its own plane or cylinder defining
            # how to project the texture coordinates on it
            surface_is_curved = np.any(self.mesh.curvatures_surface.get(surface))
            if surface_is_curved:
                add_tcoords = vtk.vtkTextureMapToCylinder()
                add_tcoords.AutomaticCylinderGenerationOn()
                add_tcoords.PreventSeamOn()
            else:
                add_tcoords = vtk.vtkTextureMapToPlane()
                add_tcoords.SetTRange(0, 0.5)
                add_tcoords.SetSRange(0, 0.5)

            add_tcoords.SetInputData(data)
            add_tcoords.Update()
            data = add_tcoords.GetOutput()

            transform_texture = vtk.vtkTransformTextureCoords()
            transform_texture.SetInputData(data)
            transform_texture.SetScale(10, 10, 10)
            transform_texture.Update()
            data = transform_texture.GetOutput()

            fill_array(data, "surface_indexes", surface)
            fill_array(data, "volume_indexes", volume)

            combined_surfaces.AddInputData(data)

        combined_surfaces.Update()

        add_normals = vtkPolyDataNormals()
        add_normals.SetInputData(combined_surfaces.GetOutput())
        add_normals.Update()

        add_tangents = vtk.vtkPolyDataTangents()
        add_tangents.SetInputData(add_normals.GetOutput())
        add_tangents.Update()

        self.data: vtkPolyData = add_tangents.GetOutput()

        self.cell_colors = fill_array(self.data, "color", (255, 255, 255, 255))
        self.data.GetCellData().SetScalars(self.cell_colors)

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

    def _create_empty_actor(self):
        self.empty_extractor = vtkExtractCells()

        empty_mapper = vtkDataSetMapper()
        empty_mapper.SetScalarModeToUseCellData()
        empty_mapper.ScalarVisibilityOn()

        self.data >> self.empty_extractor >> empty_mapper

        self.empty_actor = vtkActor(mapper=empty_mapper)
        self.AddPart(self.empty_actor)

        self.empty_actor.texture = self.chess_texture

    def _create_material_actor(self):
        self.material_extractor = vtkExtractCells()

        material_mapper = vtkDataSetMapper()
        material_mapper.SetScalarModeToUseCellData()
        material_mapper.ScalarVisibilityOn()

        self.data >> self.material_extractor >> material_mapper

        self.material_actor = vtkActor(mapper=material_mapper)
        self.AddPart(self.material_actor)

        actor_property = self.material_actor.GetProperty()
        actor_property.specular_power = 80
        actor_property.specular = 1.5
        actor_property.diffuse = 0.6
        actor_property.normal_scale = 0.5
        actor_property.normal_texture = self.material_normal_texture

    def _create_fluid_actor(self):
        self.fluid_extractor = vtkExtractCells()

        fluid_mapper = vtkDataSetMapper()
        fluid_mapper.SetScalarModeToUseCellData()
        fluid_mapper.ScalarVisibilityOn()

        self.data >> self.fluid_extractor >> fluid_mapper

        self.fluid_actor = vtkActor(mapper=fluid_mapper)
        self.AddPart(self.fluid_actor)

        actor_property = self.fluid_actor.GetProperty()
        actor_property.opacity = 0.8
        actor_property.specular_power = 40
        actor_property.specular = 0.7
        actor_property.diffuse = 1
        actor_property.normal_scale = 1.5
        actor_property.normal_texture = self.fluid_normal_texture

    def _create_porous_actor(self):
        self.porous_extractor = vtkExtractCells()

        porous_mapper = vtkDataSetMapper()
        porous_mapper.SetScalarModeToUseCellData()
        porous_mapper.ScalarVisibilityOn()

        self.data >> self.porous_extractor >> porous_mapper

        self.porous_actor = vtkActor(mapper=porous_mapper)
        self.AddPart(self.porous_actor)

        actor_property = self.porous_actor.GetProperty()
        actor_property.specular = 0
        actor_property.diffuse = 0.5
        actor_property.normal_texture = self.porous_normal_texture
        actor_property.normal_scale = 1

    def _create_textures(self):
        self.fluid_normal_texture = read_texture(TEXTURE_DIR / "perlin_normal.jpg")
        self.material_normal_texture = read_texture(TEXTURE_DIR / "metal_normal.jpg")
        self.porous_normal_texture = read_texture(TEXTURE_DIR / "foam_normal.jpg")
        self.wave_texture = read_texture(TEXTURE_DIR / "wave_normal.png")
        self.chess_texture = read_texture(TEXTURE_DIR / "chess_texture.jpg")
