from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import chain

import numpy as np
import xxhash
from molde import Color
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkDataArray, vtkIntArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import (
    VTK_TRIANGLE,
    VTK_VERTEX,
    vtkCellArray,
    vtkPlane,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper, vtkHardwarePicker, vtkPropAssembly

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.properties import Fluid, Material
from vibra.engine.properties.model_properties import ModelProperties
from vibra.utils.math_functions import inside_plane
from vibra.utils.time_utils import function_timer


@dataclass
class CachedInfo:
    mesh_id: int = 0
    surface_colors_hash: str = ""
    section_colors_hash: str = ""

    @classmethod
    def array_hash(cls, array: np.ndarray | vtkDataArray) -> str:
        ndarray = vtk_to_numpy(array) if isinstance(array, vtkDataArray) else array
        hasher = xxhash.xxh128()
        hasher.update(ndarray)
        return hasher.hexdigest()


class MeshActor(vtkPropAssembly):
    def __init__(self, model: Model | None):
        super().__init__()

        self.model = model
        self.section_plane = None
        self.cached_info = CachedInfo()

        self._create_variables()
        self._configure_actors_parameters()

    @property
    def mesh(self) -> Mesh | None:
        if self.model is None:
            return

        return self.model.mesh

    @property
    def properties(self) -> ModelProperties | None:
        if self.model is None:
            return

        return self.model.properties

    @function_timer
    def update(self):
        if self.mesh is None:
            self.clear_data()
            return

        self.update_mesh_common()
        self.update_node()
        self.update_surface()
        self.update_section_plane()
        self.update_colors()
        self.update_caches()

    def clear_data(self):
        self.cached_info = CachedInfo()

        self.node_data.SetCells(0, vtkCellArray())
        self.node_colors.SetNumberOfTuples(0)
        self.node_ids.SetNumberOfTuples(0)
        self.node_colors.Modified()

        self.surface_data.SetCells(0, vtkCellArray())
        self.surface_colors.SetNumberOfTuples(0)
        self.surface_ids.SetNumberOfTuples(0)
        self.surface_colors.Modified()

        self.section_data.SetCells(0, vtkCellArray())
        self.section_colors.SetNumberOfTuples(0)
        self.section_ids.SetNumberOfTuples(0)
        self.section_colors.Modified()

    def _create_variables(self):
        self.points = vtkPoints()
        self.solids_on_section = np.zeros((0, 4), dtype=int)

        self.node_colors = vtkUnsignedCharArray()
        self.node_ids = vtkIntArray()
        self.node_data = vtkUnstructuredGrid()
        self.node_mapper = vtkDataSetMapper()
        self.node_actor = vtkActor()

        self.surface_colors = vtkUnsignedCharArray()
        self.surface_ids = vtkIntArray()
        self.surface_data = vtkUnstructuredGrid()
        self.surface_mapper = vtkDataSetMapper()
        self.surface_actor = vtkActor()

        self.section_colors = vtkUnsignedCharArray()
        self.section_ids = vtkIntArray()
        self.section_data = vtkUnstructuredGrid()
        self.section_mapper = vtkDataSetMapper()
        self.section_actor = vtkActor()

    def _configure_actors_parameters(self):
        self.node_colors.SetName("color")
        self.node_colors.SetNumberOfComponents(3)
        self.node_ids.SetName("ids")
        self.node_data.SetPoints(self.points)
        _ = self.node_data.GetCellData().SetScalars(self.node_colors)
        _ = self.node_data.GetCellData().AddArray(self.node_ids)
        self.node_mapper.SetInputData(self.node_data)
        self.node_actor.SetMapper(self.node_mapper)
        self.node_actor.GetProperty().SetPointSize(5)
        self.node_actor.GetProperty().RenderPointsAsSpheresOn()
        self.node_actor.GetProperty().LightingOff()
        # self.AddPart(self.node_actor)

        self.surface_colors.SetName("color")
        self.surface_colors.SetNumberOfComponents(3)
        self.surface_ids.SetName("ids")
        self.surface_data.SetPoints(self.points)
        _ = self.surface_data.GetCellData().SetScalars(self.surface_colors)
        _ = self.surface_data.GetCellData().AddArray(self.surface_ids)
        self.surface_mapper.SetInputData(self.surface_data)
        self.surface_actor.SetMapper(self.surface_mapper)
        self.AddPart(self.surface_actor)

        self.section_colors.SetName("color")
        self.section_colors.SetNumberOfComponents(3)
        self.section_ids.SetName("ids")
        self.section_data.SetPoints(self.points)
        _ = self.section_data.GetCellData().SetScalars(self.section_colors)
        _ = self.section_data.GetCellData().AddArray(self.section_ids)
        self.section_mapper.SetInputData(self.section_data)
        self.section_actor.SetMapper(self.section_mapper)
        self.AddPart(self.section_actor)

    def update_mesh_common(self):
        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None

        # AND modifier is the same
        if id(self.mesh) == self.cached_info.mesh_id:
            return

        coordinates = self.mesh.nodal_coordinates[:, 1:]
        self.points.SetData(numpy_to_vtk(coordinates))
        self.points.Modified()

    def update_node(self):
        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None
        assert self.mesh.faces_connectivity is not None

        if id(self.mesh) == self.cached_info.mesh_id:
            return

        node_indexes = np.unique(self.mesh.faces_connectivity[:, 4:])
        n_cells = len(node_indexes)

        cells = self._create_cells(node_indexes)
        self.node_data.SetCells(VTK_VERTEX, cells)
        self.node_colors.SetNumberOfTuples(n_cells)
        self.node_colors.Fill(255)
        self.node_mapper.Modified()

        self.node_ids.SetNumberOfTuples(n_cells)
        view = vtk_to_numpy(self.node_ids)
        view[:] = node_indexes

    def update_surface(self):
        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None
        assert self.mesh.faces_connectivity is not None

        if id(self.mesh) == self.cached_info.mesh_id:
            return

        connectivity = self.mesh.faces_connectivity[:, 4:]
        n_cells = len(connectivity)
        cell_type = VTK_TRIANGLE

        cells = self._create_cells(connectivity)
        self.surface_data.SetCells(cell_type, cells)
        self.surface_colors.SetNumberOfTuples(n_cells)
        self.surface_mapper.Modified()

        self.surface_ids.SetNumberOfTuples(n_cells)
        view = vtk_to_numpy(self.surface_ids)
        view[:] = self.mesh.faces_connectivity[:, 0]

    def update_section_plane(self):
        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None
        assert self.mesh.faces_connectivity is not None
        assert self.mesh.solids_connectivity is not None

        self.node_mapper.RemoveAllClippingPlanes()
        self.surface_mapper.RemoveAllClippingPlanes()

        if self.section_plane is None:
            self.section_data.SetCells(0, vtkCellArray())
            self.section_colors.SetNumberOfTuples(0)
            self.section_ids.SetNumberOfTuples(0)
            self.section_colors.Modified()
            return

        plane = vtkPlane()
        plane.SetOrigin(self.section_plane.origin)
        plane.SetNormal(self.section_plane.normal)

        self.node_mapper.AddClippingPlane(plane)
        self.surface_mapper.AddClippingPlane(plane)
        self.surface_mapper.Modified()
        self.surface_actor.Modified()

        coordinates = self.mesh.nodal_coordinates[:, 1:]
        connectivity = self.mesh.solids_connectivity[:, 4:]
        mask = inside_plane(
            coordinates,  # pyright: ignore[reportArgumentType]
            self.section_plane.origin,
            self.section_plane.normal,
        ).flatten()

        counts = mask[connectivity].sum(axis=1, dtype=np.int8)
        elements_in_middle = (0 < counts) & (counts < connectivity.shape[1])

        triangulated_connectivity = self._make_triangles(self.mesh.solids_connectivity[elements_in_middle])
        n_cells = len(triangulated_connectivity)

        cells = self._create_cells(triangulated_connectivity[:, 4:])
        self.section_data.SetCells(VTK_TRIANGLE, cells)
        self.section_colors.SetNumberOfTuples(n_cells)
        self.section_mapper.Modified()

        self.section_ids.SetNumberOfTuples(n_cells)
        view = vtk_to_numpy(self.section_ids)
        view[:] = triangulated_connectivity[:, 0]

    def update_colors(self):
        self.set_color(Color(255, 255, 255), update=False)

        if self.properties is None:
            return

        surface_colors = defaultdict(list)
        volume_colors = defaultdict(list)

        for entity, _property, tag, value in self.properties.iterate_properties():
            if not isinstance(value, Material | Fluid):
                continue

            color = Color.from_rgb(*value.color)
            match entity:
                case "surface":
                    surface_colors[color].append(tag)
                case "volume":
                    volume_colors[color].append(tag)
                case _:
                    pass

        for color, tags in surface_colors.items():
            self.paint_surfaces(color, tags)

        for color, tags in volume_colors.items():
            self.paint_volumes(color, tags)

    def set_color(self, color: Color, update: bool = True):
        rgb = color.to_rgb()
        for i in range(self.surface_colors.GetNumberOfComponents()):
            self.surface_colors.FillComponent(i, rgb[i])
            self.section_colors.FillComponent(i, rgb[i])

        if update:
            self.surface_colors.Modified()
            self.section_colors.Modified()

    def paint_face_elements(self, color: Color, face_elements: Sequence[int] | np.ndarray):
        surface_ids = vtk_to_numpy(self.surface_ids)
        surface_colors = vtk_to_numpy(self.surface_colors)
        paint_position_mask = np.isin(surface_ids, face_elements)
        surface_colors[paint_position_mask] = color.to_rgb()

        if self.cached_info.surface_colors_hash != CachedInfo.array_hash(surface_colors):
            self.surface_colors.Modified()

    def paint_solid_elements(self, color: Color, solid_elements: Sequence[int] | np.ndarray):
        # First paint the elements with solid IDs
        section_ids = vtk_to_numpy(self.section_ids)
        section_colors = vtk_to_numpy(self.section_colors)
        paint_position_mask = np.isin(section_ids, solid_elements)
        section_colors[paint_position_mask] = color.to_rgb()

        if self.cached_info.section_colors_hash != CachedInfo.array_hash(section_colors):
            self.section_colors.Modified()
            self.section_mapper.Modified()

        assert self.mesh.faces_connectivity is not None
        assert self.mesh.solids_connectivity is not None

        # Second paint the elements with face IDs (which can also be solids)
        solids_mask = np.isin(self.mesh.solids_connectivity[:, 0], solid_elements)
        face_mask = np.isin(
            self.mesh.faces_connectivity[:, 4:],
            self.mesh.solids_connectivity[solids_mask, 4:],
        ).all(axis=1)
        face_elements = self.mesh.faces_connectivity[face_mask, 0]
        self.paint_face_elements(color, face_elements)

    def paint_surfaces(self, color: Color, surfaces: Sequence[int] | np.ndarray):
        if self.mesh is None:
            return

        assert self.mesh.faces_connectivity is not None
        selected_face_elements, *_ = np.where(np.isin(self.mesh.faces_connectivity[:, 1], surfaces))
        self.paint_face_elements(color, selected_face_elements)

    def paint_volumes(self, color: Color, volumes: Sequence[int] | np.ndarray):
        if self.mesh is None:
            return

        surface_groups = [self.mesh.surfaces_from_volume[v] for v in volumes if (v in self.mesh.surfaces_from_volume)]
        surfaces = list(chain.from_iterable(surface_groups))
        self.paint_surfaces(color, surfaces)

        if self.section_plane is None:
            return

        section_ids = vtk_to_numpy(self.section_ids)
        section_colors = vtk_to_numpy(self.section_colors)

        selected_elements, *_ = np.where(np.isin(self.mesh.solids_connectivity[:, 1], volumes))
        paint_position_mask = np.isin(section_ids, selected_elements)
        section_colors[paint_position_mask] = color.to_rgb()

        if self.cached_info.section_colors_hash != CachedInfo.array_hash(section_colors):
            self.section_colors.Modified()

    def picked_dim_tag(self, picker: vtkHardwarePicker) -> tuple[int, int] | None:
        match picker.GetActor():
            case self.section_actor:
                dim = 3
                ids = vtk_to_numpy(self.section_ids)
            case self.surface_actor:
                dim = 2
                ids = vtk_to_numpy(self.surface_ids)
            case self.node_actor:
                dim = 0
                ids = vtk_to_numpy(self.node_ids)
            case _:
                return

        cell_id = picker.GetCellId()
        if 0 < cell_id < len(ids):
            return dim, ids[cell_id]

    def update_caches(self):
        self.cached_info.mesh_id = id(self.mesh)
        self.cached_info.surface_colors_hash = CachedInfo.array_hash(self.surface_colors)
        self.cached_info.section_colors_hash = CachedInfo.array_hash(self.section_colors)

    def _get_parts(self) -> list[vtkActor]:
        return list(self.GetParts())  # pyright: ignore[reportArgumentType]

    def _create_cells(self, connectivity: np.ndarray) -> vtkCellArray:
        if connectivity.ndim == 1:
            connectivity = connectivity.reshape(-1, 1)

        helper = np.insert(connectivity, 0, connectivity.shape[1], axis=1)
        vtk_id_array = numpy_to_vtkIdTypeArray(helper.flatten())
        cell_array = vtkCellArray()
        cell_array.SetCells(connectivity.shape[0], vtk_id_array)
        return cell_array

    def _make_triangles(self, connectivity: np.ndarray) -> np.ndarray:
        reorderings = [[0, 1, 2], [1, 3, 2]]
        column_order = [
            [0, 1, 2, 3] + [i + 4 for i in reordering]
            for reordering in reorderings
        ]  # fmt: skip

        stacked = []
        for order in column_order:
            connect = connectivity[:, order]
            stacked.append(connect)

        return np.concatenate(stacked)
