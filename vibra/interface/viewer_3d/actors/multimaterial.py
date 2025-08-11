from collections import defaultdict
from pathlib import Path
from typing import Sequence

import numpy as np
import vtk
from molde import Color
from vtkmodules.util.numpy_support import (
    numpy_to_vtk,
    numpy_to_vtkIdTypeArray,
    vtk_to_numpy,
)
from vtkmodules.vtkCommonCore import (
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkExtractCells, vtkPolyDataNormals
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPropAssembly,
)

from vibra import TEXTURE_DIR, app
from vibra.engine.mesher.mesh import Mesh
from vibra.utils.polydata_utils import fill_array


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
    texture.Update()

    return texture


class MultimaterialGeometryActor(vtkPropAssembly):
    def __init__(self, mesh: Mesh | None = None):
        self.mesh = mesh
        if self.mesh is None:
            self.mesh = app().project.model.mesh

        self.extractors: dict[str, vtkExtractCells] = dict()
        self.create_geometry()

    def create_geometry(self):
        if self.mesh.nodal_coordinates.size == 0:
            return

        self.extractors.clear()
        self._create_textures()
        self._create_surfaces()

        self._create_empty_actor()
        self._create_material_volume_actor()
        self._create_material_wall_actor()
        self._create_fluid_actor()
        self._create_porous_actor()
        self._create_perforated_actor()

        self.clear_colors()

    def clear_colors(self):
        mesh = app().project.model.mesh
        properties = app().project.model.properties
        color_to_surfaces = defaultdict(list)
        self.reload_composition()

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

    def reload_composition(self):
        mesh = app().project.model.mesh
        properties = app().project.model.properties
        composition_to_surfaces = defaultdict(list)

        for surface, volumes in mesh.volumes_from_surface.items():
            volume = volumes[0]

            if surface in app().main_window.hidden_surfaces:
                continue

            if volume in app().main_window.hidden_volumes:
                continue

            fluid = properties._get_property("fluid", surface=surface, volume=volume)
            material_wall = properties._get_property("material", surface=surface)
            material_volume = properties._get_property("material", volume=volume)
            porous = properties._get_property("porous_material_model", surface=surface, volume=volume)
            perforated = properties._get_property("perforated_plate_model", surface=surface, volume=volume)

            if perforated is not None:
                composition = "perforated"
            elif porous is not None:
                composition = "porous"
            elif material_volume is not None:
                composition = "material_volume"
            elif material_wall is not None:
                composition = "material_wall"
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
        extractor = self.extractors.get(constitution, None)
        if extractor is None:
            return

        cells = self._surfaces_to_cells(surfaces)
        extractor.SetCellIds(cells, len(cells))

    def clear_composition(self):
        for extractor in self.extractors.values():
            extractor.SetCellIds([], 0)

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
            points.SetData(numpy_to_vtk(coords + (1, 1, 0)))

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
            add_tcoords = vtk.vtkTextureMapToPlane()
            add_tcoords.AutomaticPlaneGenerationOff()

            # This should have been calculated by the mesher
            # or even better: by a geometry class
            all_normals = self.mesh.normals_surface.get(surface)
            normal = np.average(all_normals, axis=0) if (all_normals is not None) else (0, 0, 1)
            normal /= np.linalg.norm(normal)
            nx, ny, nz = normal * 0.08
            p1 = np.array([-ny, nx, nz])
            p2 = np.cross(p1, normal)

            add_tcoords.SetOrigin(0, 0, 0)
            add_tcoords.SetPoint1(p1)
            add_tcoords.SetPoint2(p2)

            add_tcoords.SetInputData(data)
            add_tcoords.Update()
            data = add_tcoords.GetOutput()

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
        self.empty_actor = self._new_actor_extraction("empty")
        self.empty_actor.SetTexture(self.chess_texture)

    def _create_material_volume_actor(self):
        self.material_actor = self._new_actor_extraction("material_volume")
        self.material_actor.GetProperty().SetSpecularPower(80)
        self.material_actor.GetProperty().SetSpecular(1.5)
        self.material_actor.GetProperty().SetDiffuse(0.6)
        self.material_actor.GetProperty().SetNormalScale(0.5)
        self.material_actor.GetProperty().SetNormalTexture(self.material_normal_texture)

    def _create_material_wall_actor(self):
        self.material_actor = self._new_actor_extraction("material_wall")
        self.material_actor.GetProperty().SetSpecularPower(80)
        self.material_actor.GetProperty().SetSpecular(1.5)
        self.material_actor.GetProperty().SetDiffuse(0.6)
        self.material_actor.GetProperty().SetNormalScale(0.5)
        self.material_actor.GetProperty().SetNormalTexture(self.material_normal_texture)
        self.material_actor.SetTexture(self.wall_texture)

    def _create_fluid_actor(self):
        self.fluid_actor = self._new_actor_extraction("fluid")
        self.fluid_actor.GetProperty().SetOpacity(0.8)
        self.fluid_actor.GetProperty().SetDiffuse(0.5)
        self.fluid_actor.GetProperty().SetAmbient(0.6)
        self.fluid_actor.GetProperty().SetSpecular(0.8)
        self.fluid_actor.GetProperty().SetSpecularPower(100)
        self.fluid_actor.GetProperty().SetNormalScale(1.2)
        self.fluid_actor.SetTexture(self.wave_texture)

    def _create_porous_actor(self):
        self.porous_actor = self._new_actor_extraction("porous")
        self.porous_actor.GetProperty().SetSpecular(0)
        self.porous_actor.GetProperty().SetDiffuse(0.5)
        self.porous_actor.GetProperty().SetAmbient(0.1)
        self.fluid_actor.GetProperty().SetNormalScale(3)
        self.porous_actor.GetProperty().SetNormalTexture(self.porous_normal_texture)

    def _create_perforated_actor(self):
        self.perforated_actor = self._new_actor_extraction("perforated")
        self.perforated_actor.GetProperty().SetSpecularPower(80)
        self.perforated_actor.GetProperty().SetSpecular(1.5)
        self.perforated_actor.GetProperty().SetDiffuse(0.8)
        self.perforated_actor.GetProperty().SetAmbient(0.5)
        self.perforated_actor.GetProperty().SetNormalScale(3)
        self.perforated_actor.GetProperty().SetNormalTexture(self.perforated_normal_texture)
        self.perforated_actor.SetTexture(self.perforated_opacity_texture)

    def _new_actor_extraction(self, name: str):
        extractor = vtkExtractCells()
        self.extractors[name] = extractor

        mapper = vtkDataSetMapper()
        mapper.SetScalarModeToUseCellData()
        mapper.ScalarVisibilityOn()

        self.data >> extractor >> mapper

        self.actor = vtkActor(mapper=mapper)
        self.AddPart(self.actor)

        return self.actor

    def _create_textures(self):
        self.porous_normal_texture = read_texture(TEXTURE_DIR / "porous_normal.jpg")
        self.material_normal_texture = read_texture(TEXTURE_DIR / "metal_normal.jpg")
        self.perforated_opacity_texture = read_texture(TEXTURE_DIR / "perforated_opacity.png")
        self.perforated_normal_texture = read_texture(TEXTURE_DIR / "perforated_normal.jpg")
        self.chess_texture = read_texture(TEXTURE_DIR / "chess_texture.jpg")
        self.wave_texture = read_texture(TEXTURE_DIR / "wave_texture.png")
        self.wall_texture = read_texture(TEXTURE_DIR / "wall_texture.png")
