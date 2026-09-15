from collections import defaultdict
from typing import Optional, Sequence

import numpy as np
from molde.colors import Color, color_names
from vtkmodules.util.numpy_support import (
    numpy_to_vtk,
    numpy_to_vtkIdTypeArray,
    vtk_to_numpy,
)
from vtkmodules.vtkCommonCore import (
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPlane,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkExtractCells, vtkPolyDataNormals, vtkPolyDataTangents
from vtkmodules.vtkFiltersTexture import vtkTextureMapToPlane
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPropAssembly,
)

from vibra import TEXTURE_DIR, app
from vibra.engine.mesher.mesh import Mesh
from vibra.utils.interface_utils import GeometryColorMode, VisualizationFilter
from vibra.utils.vtk_utils import fill_array, read_texture


def get_first_visible_volume(volumes):
    for volume in volumes:
        if volume not in app().main_window.entity_visibility._volumes_to_hide:
            return volume


class MultimaterialGeometryActor(vtkPropAssembly):
    def __init__(
        self,
        mesh: Mesh,
        visualization_filter: Optional[VisualizationFilter] = None,
    ):
        self.visualization_filter = visualization_filter
        if self.visualization_filter is None:
            self.visualization_filter = VisualizationFilter.all_true()

        self.mesh = mesh
        self.extractors: dict[str, vtkExtractCells] = dict()
        self.create_geometry()

    def create_geometry(self):
        if self.mesh.nodal_coordinates.size == 0:
            return

        self.extractors.clear()
        self._create_textures()
        self._create_surfaces()

        self._create_default_actor()
        self._create_empty_actor()
        self._create_material_volume_actor()
        self._create_material_wall_actor()
        self._create_fluid_actor()
        self._create_porous_actor()
        self._create_perforated_actor()

        # The bounds calculated for this actor are not correct
        # We also cannot correct it, so we have to disable it
        self.UseBoundsOff()
        self.clear_colors()

    def clear_colors(self):
        mesh = app().project.model.mesh
        properties = app().project.model.properties
        color_mode = self.visualization_filter.color_mode

        if color_mode == GeometryColorMode.EMPTY:
            self.reload_composition()
            return self.set_color(color_names.WHITE)

        color_to_surfaces = defaultdict(list)
        self.reload_composition()
        surfaces_with_perforated_plates = self._surfaces_with_perforated_plate()
        surfaces = mesh.lines_from_surface.keys()  # We don't have just "surfaces" yet

        for surface in surfaces:
            volumes = mesh.volumes_from_surface.get(surface, ())
            volume = get_first_visible_volume(volumes)

            fluid = properties._get_property("fluid", surface=surface, volume=volume)
            material = properties._get_property("material", surface=surface, volume=volume)
            porous = properties._get_property("porous_material_model", surface=surface, volume=volume)

            if porous is not None:
                color = color_names.YELLOW_6

            elif surface in surfaces_with_perforated_plates:
                color = color_names.WHITE

            elif material is not None:
                color = Color(*material.color)

            elif fluid is not None:
                color = Color(*fluid.color)

            else:
                color = color_names.WHITE

            color_to_surfaces[color].append(surface)

        for color, surfaces in color_to_surfaces.items():
            self.paint_surfaces(color, surfaces)

    def reload_composition(self):
        mesh = app().project.model.mesh
        properties = app().project.model.properties
        color_mode = self.visualization_filter.color_mode
        surfaces = mesh.lines_from_surface.keys()  # We don't have just "surfaces" yet
        visible_surfaces = app().main_window.entity_visibility.get_visible_surfaces()

        if color_mode == GeometryColorMode.EMPTY:
            self.clear_composition()
            self.default_actor.VisibilityOn()
            self.configure_composition("default", visible_surfaces)
            return

        self.default_actor.VisibilityOff()
        composition_to_surfaces = defaultdict(list)
        surfaces_with_perforated_plates = self._surfaces_with_perforated_plate()

        for surface in surfaces:
            volumes = mesh.volumes_from_surface.get(surface, ())
            volume = get_first_visible_volume(volumes)

            if surface in visible_surfaces:
                composition_to_surfaces["default"].append(surface)
            else:
                continue

            fluid = properties._get_property("fluid", surface=surface, volume=volume)
            material_wall = properties._get_property("material", surface=surface)
            material_volume = properties._get_property("material", volume=volume)
            porous = properties._get_property("porous_material_model", surface=surface, volume=volume)

            if surface in surfaces_with_perforated_plates:
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
        if array.size == 0:
            return

        # Ensure cell ids are valid, ignore otherwise
        cells = np.array(cells)
        cells = cells[(0 <= cells) & (cells < array.size)]

        array[cells] = color_fmt
        self.data.Modified()

        for actor in self.get_parts():
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

    def disable_cut(self):
        for actor in self.get_parts():
            actor.GetMapper().RemoveAllClippingPlanes()

    def apply_cut(self, origin, normal):
        plane = vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)

        for actor in self.get_parts():
            actor.GetMapper().RemoveAllClippingPlanes()
            actor.GetMapper().AddClippingPlane(plane)
            actor.GetMapper().Modified()
            actor.Modified()

    def get_parts(self) -> list[vtkActor]:
        return list(super().GetParts())

    def _surfaces_to_cells(self, surfaces: Sequence[int]) -> np.ndarray:
        vtk_array = self.data.GetCellData().GetArray("surface_indices")
        if vtk_array is None:
            return np.array([])

        array = vtk_to_numpy(vtk_array)
        mask = np.isin(array, list(surfaces))
        return np.where(mask)[0]

    def _create_surfaces(self):
        combined_surfaces = vtkAppendPolyData()
        visible_surfaces = app().main_window.entity_visibility.get_visible_surfaces()

        for surface, elements in self.mesh.elements_from_surface.items():
            if surface not in visible_surfaces:
                continue

            coords, connect = self._reduce_connectivity(
                self.mesh.nodal_coordinates[:, 1:],
                self.mesh.faces_connectivity[elements, 4:],
            )

            points = vtkPoints()
            points.SetData(numpy_to_vtk(coords))
            cells = self._create_cells(connect)

            data = vtkPolyData()
            data.SetPoints(points)
            data.SetPolys(cells)

            volumes = self.mesh.volumes_from_surface.get(surface)

            # Every surface have its own plane defining
            # how to project the texture coordinates on it
            add_tcoords = vtkTextureMapToPlane()
            add_tcoords.AutomaticPlaneGenerationOff()

            # This should have been calculated by the mesher
            # or even better: by a geometry class
            surface_normals = self.mesh.normals_surface.get(surface)
            if surface_normals is None:
                element_face_normals = self.mesh.get_stacked_normals_for_surface_elements(surface)
                normal = np.average(element_face_normals, axis=0).flatten()
            else:
                normal = np.average(surface_normals, axis=0).round(6)
            normal /= np.linalg.norm(normal)

            nx, ny, nz = normal * 0.08
            p1 = np.array([-ny, nz, nx])
            p2 = np.cross(p1, normal)

            add_tcoords.SetOrigin(0, 0, 0)
            add_tcoords.SetPoint1(p1)
            add_tcoords.SetPoint2(p2)

            add_tcoords.SetInputData(data)
            add_tcoords.Update()
            data = add_tcoords.GetOutput()

            fill_array(data, "surface_indices", surface)
            if isinstance(volumes, np.ndarray | list) and (len(volumes) != 0):
                fill_array(data, "volume_indices", volumes[0])

            combined_surfaces.AddInputData(data)

        combined_surfaces.Update()

        add_normals = vtkPolyDataNormals()
        add_normals.SetInputData(combined_surfaces.GetOutput())
        add_normals.Update()

        add_tangents = vtkPolyDataTangents()
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
        old_indices = np.unique(connectivity)
        new_indices = np.arange(len(old_indices))

        if mapping is None:
            mapping = np.zeros(np.max(connectivity) + 1, dtype=int)
        mapping[old_indices] = new_indices

        return coords[old_indices], mapping[connectivity]

    def _create_cells(self, connectivity: np.ndarray) -> vtkCellArray:
        nodes_per_element = len(connectivity[0, :])
        triangulated: np.ndarray

        if nodes_per_element in (3, 6):
            triangulated = connectivity[:, :3]

        elif nodes_per_element in (4, 8):
            lower = connectivity[:, [0, 1, 3]]
            upper = connectivity[:, [1, 2, 3]]
            triangulated = np.append(lower, upper, axis=0)

        else:
            raise NotImplementedError(f"Elements with {nodes_per_element} nodes are not supported")

        # Add a "3" column at the start, as expected by VTK
        helper = np.insert(triangulated, 0, 3, axis=1)
        vtk_id_array = numpy_to_vtkIdTypeArray(helper.flatten())

        cells = vtkCellArray()
        cells.SetCells(len(triangulated), vtk_id_array)

        return cells

    def _create_empty_actor(self):
        self.empty_actor = self._new_actor_extraction("empty")
        self.empty_actor.SetTexture(self.chess_texture)

    def _create_default_actor(self):
        """
        This is the only pickable actor that extracts all cells.

        It is used to enable selection whithout further modifications
        and the performance does not degrade too much.

        It is also shown when the user whant to disable colors and textures.
        """
        self.default_actor = self._new_actor_extraction("default")
        self.default_actor.VisibilityOff()
        self.default_actor.PickableOn()

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
        self.material_actor.GetProperty().SetDiffuse(0.7)
        self.material_actor.GetProperty().SetNormalScale(0.5)
        self.material_actor.GetProperty().SetNormalTexture(self.material_normal_texture)
        self.material_actor.SetTexture(self.wall_texture)

    def _create_fluid_actor(self):
        self.fluid_actor = self._new_actor_extraction("fluid")
        self.fluid_actor.GetProperty().SetDiffuse(0.5)
        self.fluid_actor.GetProperty().SetAmbient(0.6)

    def _create_porous_actor(self):
        self.porous_actor = self._new_actor_extraction("porous")
        self.porous_actor.GetProperty().SetSpecular(0)
        self.porous_actor.GetProperty().SetDiffuse(0.4)
        self.porous_actor.GetProperty().SetAmbient(0.4)
        self.fluid_actor.GetProperty().SetNormalScale(0.8)
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
        self.actor.PickableOff()

        self.AddPart(self.actor)
        return self.actor

    def _create_textures(self):
        self.porous_normal_texture = read_texture(TEXTURE_DIR / "porous_normal.jpg")
        self.material_normal_texture = read_texture(TEXTURE_DIR / "metal_normal.jpg")
        self.perforated_opacity_texture = read_texture(TEXTURE_DIR / "perforated_opacity.png")
        self.perforated_normal_texture = read_texture(TEXTURE_DIR / "perforated_normal.jpg")
        self.chess_texture = read_texture(TEXTURE_DIR / "chess_texture.jpg")
        self.wall_texture = read_texture(TEXTURE_DIR / "wall_texture.png")

    def _surfaces_with_perforated_plate(self):
        # Find both surfaces of a perforated plate
        mesh = app().project.model.mesh
        properties = app().project.model.properties

        surfaces_with_perforated_plates = set()
        for surface, _ in mesh.volumes_from_surface.items():
            perforated = properties._get_property("perforated_plate_model", surface=surface)
            decoupling = properties._get_property("degrees_of_freedom_decoupling", surface=surface)
            if (perforated is not None) and (decoupling is not None):
                complementary_surface = decoupling.get("new_surface_id")
                surfaces_with_perforated_plates.add(surface)
                surfaces_with_perforated_plates.add(complementary_surface)

        return surfaces_with_perforated_plates
