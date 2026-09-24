from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from enum import Enum, auto
from itertools import chain, combinations, pairwise

import numpy as np
import xxhash
from molde import Color
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkDataArray, vtkIntArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkAreaPicker, vtkHardwarePicker, vtkPolyDataMapper, vtkPropAssembly, vtkRenderer

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.properties.model_properties import ModelProperties
from vibra.interface.viewer_3d.coloring.color_table import ColorTable
from vibra.utils.interface_utils import SectionPlane
from vibra.utils.math_functions import inside_plane
from vibra.utils.time_utils import function_timer


@dataclass
class CachedInfo:
    mesh_id: int = 0
    result_colors_hash: str = ""
    node_colors_hash: str = ""
    surface_colors_hash: str = ""
    section_colors_hash: str = ""
    section_plane_hash: int = 0

    @classmethod
    def array_hash(cls, array: np.ndarray | vtkDataArray) -> str:
        ndarray = vtk_to_numpy(array) if isinstance(array, vtkDataArray) else array
        hasher = xxhash.xxh128()
        hasher.update(ndarray)
        return hasher.hexdigest()


class VisualizationMode(Enum):
    SHOW_RESULTS = auto()
    SHOW_ENTITIES = auto()


@dataclass
class PickedMesh:
    picked_nodes: set[int] = field(default_factory=set)
    picked_faces: set[int] = field(default_factory=set)
    picked_solids: set[int] = field(default_factory=set)

    def clear(self):
        self.picked_nodes.clear()
        self.picked_faces.clear()
        self.picked_solids.clear()


class ResultsActor(vtkPropAssembly):
    def __init__(self, model: Model | None):
        super().__init__()

        self.model = model
        self.section_plane: SectionPlane | None = None
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

        if self.section_plane is None:
            self.build_mesh_without_section_plane()
        else:
            self.build_mesh_with_section_plane()

        self.update_caches()

    def clear_data(self):
        self.cached_info = CachedInfo()
        self.result_colors.SetNumberOfTuples(0)

        self.node_data.SetVerts(vtkCellArray())
        self.node_colors.SetNumberOfTuples(0)
        self.node_ids.SetNumberOfTuples(0)
        self.node_colors.Modified()

        self.surface_data.SetPolys(vtkCellArray())
        self.surface_colors.SetNumberOfTuples(0)
        self.surface_ids.SetNumberOfTuples(0)
        self.surface_colors.Modified()

        self.volume_data.SetPolys(vtkCellArray())
        self.volume_colors.SetNumberOfTuples(0)
        self.volume_ids.SetNumberOfTuples(0)
        self.volume_colors.Modified()

    def _create_variables(self):
        self.visualization_mode = VisualizationMode.SHOW_RESULTS

        self.hardware_picker = vtkHardwarePicker()
        self.hardware_picker.SetPixelTolerance(0)
        self.hardware_picker.SnapToMeshPointOff()
        self.area_picker = vtkAreaPicker()
        self.area_picker.PickFromListOn()
        self.result_colors = vtkUnsignedCharArray()

        self.points = vtkPoints()
        self._masked_nodes = np.array([], dtype=int)

        self.node_colors = vtkUnsignedCharArray()
        self.node_ids = vtkIntArray()
        self.node_data = vtkPolyData()
        self.node_mapper = vtkPolyDataMapper()
        self.node_mapper.SetResolveCoincidentTopologyToShiftZBuffer()
        self.node_actor = vtkActor()

        self.edge_data = vtkPolyData()
        self.edge_mapper = vtkPolyDataMapper()
        self.edge_actor = vtkActor()

        self.surface_colors = vtkUnsignedCharArray()
        self.surface_ids = vtkIntArray()
        self.surface_data = vtkPolyData()
        self.surface_mapper = vtkPolyDataMapper()
        self.surface_actor = vtkActor()

        self.volume_colors = vtkUnsignedCharArray()
        self.volume_ids = vtkIntArray()
        self.volume_data = vtkPolyData()
        self.volume_mapper = vtkPolyDataMapper()
        self.volume_actor = vtkActor()

    def _configure_actors_parameters(self):
        self.result_colors.SetName("result_color")
        self.result_colors.SetNumberOfComponents(4)

        self.node_colors.SetName("color")
        self.node_colors.SetNumberOfComponents(3)
        self.node_ids.SetName("ids")
        self.node_data.SetPoints(self.points)
        self.node_data.GetPointData().SetScalars(self.result_colors)
        self.node_data.GetCellData().SetScalars(self.node_colors)
        self.node_data.GetCellData().AddArray(self.node_ids)
        self.node_mapper.SetScalarModeToUsePointData()
        self.node_mapper.SetInputData(self.node_data)
        self.node_actor.SetMapper(self.node_mapper)
        self.node_actor.GetProperty().SetPointSize(10)
        self.node_actor.GetProperty().RenderPointsAsSpheresOn()
        self.node_actor.GetProperty().LightingOff()
        self.AddPart(self.node_actor)

        self.edge_data.SetPoints(self.points)
        self.edge_data.GetPointData().SetScalars(self.result_colors)
        self.node_mapper.SetScalarModeToUsePointData()
        self.edge_mapper.SetInputData(self.edge_data)
        self.edge_actor.SetMapper(self.edge_mapper)
        self.edge_actor.GetProperty().SetRepresentationToWireframe()
        self.edge_actor.GetProperty().SetLineWidth(7)
        self.edge_actor.GetProperty().SetColor(1, 1, 1)
        self.edge_actor.PickableOff()
        self.AddPart(self.edge_actor)

        self.surface_colors.SetName("color")
        self.surface_colors.SetNumberOfComponents(4)
        self.surface_ids.SetName("ids")
        self.surface_data.SetPoints(self.points)
        self.surface_data.GetPointData().SetScalars(self.result_colors)
        self.surface_data.GetCellData().SetScalars(self.surface_colors)
        self.surface_data.GetCellData().AddArray(self.surface_ids)
        self.surface_mapper.SetScalarModeToUsePointData()
        self.surface_mapper.SetInputData(self.surface_data)
        self.surface_actor.SetForceOpaque(True)
        self.surface_actor.SetMapper(self.surface_mapper)
        self.AddPart(self.surface_actor)

        self.volume_colors.SetName("color")
        self.volume_colors.SetNumberOfComponents(4)
        self.volume_ids.SetName("ids")
        self.volume_data.SetPoints(self.points)
        self.volume_data.GetPointData().SetScalars(self.result_colors)
        self.volume_data.GetCellData().SetScalars(self.volume_colors)
        self.volume_data.GetCellData().AddArray(self.volume_ids)
        self.volume_mapper.SetScalarModeToUsePointData()
        self.volume_mapper.SetInputData(self.volume_data)
        self.volume_actor.SetForceOpaque(True)
        self.volume_actor.SetMapper(self.volume_mapper)
        self.AddPart(self.volume_actor)

    def build_mesh_without_section_plane(self):
        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None
        assert self.mesh.faces_connectivity is not None
        assert self.mesh.solids_connectivity is not None

        if not self._mesh_updated():
            return

        self.points.SetData(numpy_to_vtk(self.mesh.nodal_coordinates[:, 1:]))
        self.points.Modified()

        node_indexes = np.unique(self.mesh.faces_connectivity[:, 4:])
        node_cells = self._create_cells(node_indexes)
        self.node_data.SetVerts(node_cells)
        self.node_colors.SetNumberOfTuples(len(node_indexes))
        self.node_colors.Fill(255)
        self.node_mapper.Modified()
        self.node_ids.SetNumberOfTuples(len(node_indexes))
        vtk_to_numpy(self.node_ids)[:] = node_indexes

        edges_linearized = self._linearize_2d_cells(self.mesh.faces_connectivity)
        cells = self._create_cells(edges_linearized[:, 4:])
        self.edge_data.SetLines(cells)

        faces_triangulated = self._triangulate_2d_cells(self.mesh.faces_connectivity)
        face_cells = self._create_cells(faces_triangulated[:, 4:])
        self.surface_data.SetPolys(face_cells)
        self.surface_colors.SetNumberOfTuples(len(faces_triangulated))
        self.surface_mapper.Modified()
        self.surface_colors.Fill(255)
        self.surface_ids.SetNumberOfTuples(len(faces_triangulated))
        vtk_to_numpy(self.surface_ids)[:] = faces_triangulated[:, 0]

        self.volume_data.SetPolys(vtkCellArray())
        self.volume_colors.SetNumberOfTuples(0)
        self.volume_ids.SetNumberOfTuples(0)
        self.volume_colors.Modified()

    def build_mesh_with_section_plane(self):
        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None
        assert self.mesh.faces_connectivity is not None
        assert self.mesh.solids_connectivity is not None
        assert self.section_plane is not None

        if not self._mesh_updated():
            return

        self.points.SetData(numpy_to_vtk(self.mesh.nodal_coordinates[:, 1:]))
        self.points.Modified()

        faces_connectivity = self.mesh.faces_connectivity[:, 4:]
        solids_connectivity = self.mesh.solids_connectivity[:, 4:]
        self._masked_nodes = self._find_masked_nodes()
        visible_nodes_per_solid = self._masked_nodes[solids_connectivity].sum(axis=1, dtype=np.int8)
        solids_in_middle_mask = (0 < visible_nodes_per_solid) & (visible_nodes_per_solid < solids_connectivity.shape[1])
        faces_before_plane_mask = self._masked_nodes[faces_connectivity].all(axis=1)
        solids_in_middle = self.mesh.solids_connectivity[solids_in_middle_mask]
        faces_before_plane = self.mesh.faces_connectivity[faces_before_plane_mask]

        node_indexes = np.unique(np.concatenate((solids_in_middle[:, 4:].ravel(), faces_before_plane[:, 4:].ravel())))
        node_cells = self._create_cells(node_indexes)
        self.node_data.SetVerts(node_cells)
        self.node_colors.SetNumberOfTuples(len(node_indexes))
        self.node_colors.Fill(255)
        self.node_mapper.Modified()
        self.node_ids.SetNumberOfTuples(len(node_indexes))
        vtk_to_numpy(self.node_ids)[:] = node_indexes

        edges_linearized = np.vstack((
            self._linearize_2d_cells(faces_before_plane),
            self._linearize_3d_cells(solids_in_middle),
        ))  # fmt: skip
        cells = self._create_cells(edges_linearized[:, 4:])
        self.edge_data.SetLines(cells)

        faces_triangulated = self._triangulate_2d_cells(faces_before_plane)
        face_cells = self._create_cells(faces_triangulated[:, 4:])
        self.surface_data.SetPolys(face_cells)
        self.surface_colors.SetNumberOfTuples(len(faces_triangulated))
        self.surface_mapper.Modified()
        self.surface_colors.Fill(255)
        self.surface_ids.SetNumberOfTuples(len(faces_triangulated))
        vtk_to_numpy(self.surface_ids)[:] = faces_triangulated[:, 0]

        solids_triangulated = self._triangulate_3d_cells(solids_in_middle)
        solid_cells = self._create_cells(solids_triangulated[:, 4:])
        self.volume_data.SetPolys(solid_cells)
        self.volume_colors.SetNumberOfTuples(len(solids_triangulated))
        self.volume_mapper.Modified()
        self.volume_colors.Fill(255)
        self.volume_ids.SetNumberOfTuples(len(solids_triangulated))
        vtk_to_numpy(self.volume_ids)[:] = solids_triangulated[:, 0]

    def update_caches(self):
        result_colors_hash = CachedInfo.array_hash(self.result_colors)
        if result_colors_hash != self.cached_info.result_colors_hash:
            self.cached_info.result_colors_hash = result_colors_hash
            self.result_colors.Modified()

        node_colors_hash = CachedInfo.array_hash(self.node_colors)
        if node_colors_hash != self.cached_info.node_colors_hash:
            self.cached_info.node_colors_hash = node_colors_hash
            self.node_colors.Modified()

        surface_colors_hash = CachedInfo.array_hash(self.surface_colors)
        if surface_colors_hash != self.cached_info.surface_colors_hash:
            self.cached_info.surface_colors_hash = surface_colors_hash
            self.surface_colors.Modified()

        section_colors_hash = CachedInfo.array_hash(self.volume_colors)
        if section_colors_hash != self.cached_info.section_colors_hash:
            self.cached_info.section_colors_hash = section_colors_hash
            self.volume_colors.Modified()

        mesh_id = id(self.mesh)
        if mesh_id != self.cached_info.mesh_id:
            self.cached_info.mesh_id = mesh_id
            # Don't need to modify anything, but might in the future

        section_plane_hash = hash(self.section_plane)
        if section_plane_hash != self.cached_info.section_plane_hash:
            self.cached_info.section_plane_hash = section_plane_hash

    def pick(self, x: int, y: int, renderer: vtkRenderer) -> PickedMesh:
        self.hardware_picker.Pick(x, y, 0, renderer)
        cell_id = self.hardware_picker.GetCellId()

        match self.hardware_picker.GetActor():
            case self.volume_actor:
                ids = vtk_to_numpy(self.volume_ids)
                if 0 < cell_id < len(ids):
                    return PickedMesh(picked_solids={ids[cell_id]})

            case self.surface_actor:
                ids = vtk_to_numpy(self.surface_ids)
                if 0 < cell_id < len(ids):
                    return PickedMesh(picked_faces={ids[cell_id]})

            case self.node_actor:
                ids = vtk_to_numpy(self.node_ids)
                if 0 < cell_id < len(ids):
                    return PickedMesh(picked_nodes={ids[cell_id]})
            case _:
                ...

        return PickedMesh()

    def area_pick(self, x0: int, y0: int, x1: int, y1: int, renderer: vtkRenderer) -> PickedMesh:
        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None
        assert self.mesh.faces_connectivity is not None
        assert self.mesh.solids_connectivity is not None

        coordinates = self.mesh.nodal_coordinates[:, 1:]
        faces_coordinates = self.mesh.faces_connectivity[:, 4:]
        solid_coordinates = self.mesh.solids_connectivity[:, 4:]

        if self.section_plane is None:
            nodes_mask = np.ones(len(coordinates), dtype=bool)
        else:
            nodes_mask = self._masked_nodes.copy()
            visible_node_ids = vtk_to_numpy(self.node_ids)
            visible_nodes_mask = np.isin(self.mesh.nodal_coordinates[:, 0], visible_node_ids)
            nodes_mask[visible_nodes_mask] = True

        self.area_picker.AreaPick(x0, y0, x1, y1, renderer)
        frustum = self.area_picker.GetFrustum()

        for i in range(frustum.GetNumberOfPlanes()):
            plane = frustum.GetPlane(i)
            nodes_mask &= inside_plane(
                coordinates,
                plane.GetOrigin(),
                [-i for i in plane.GetNormal()],
            ).ravel()

        faces_mask = nodes_mask[faces_coordinates].any(axis=1)
        solids_mask = nodes_mask[solid_coordinates].any(axis=1)

        return PickedMesh(
            picked_nodes=set(self.mesh.nodal_coordinates[nodes_mask, 0].astype(int)),
            picked_faces=set(self.mesh.faces_connectivity[faces_mask, 0]),
            picked_solids=set(self.mesh.solids_connectivity[solids_mask, 0]),
        )

    def show_results_mode(self):
        self.visualization_mode = VisualizationMode.SHOW_RESULTS
        self.node_mapper.SetScalarModeToUsePointData()
        self.surface_mapper.SetScalarModeToUsePointData()
        self.volume_mapper.SetScalarModeToUsePointData()

    def show_entities_mode(self):
        self.visualization_mode = VisualizationMode.SHOW_ENTITIES
        self.node_mapper.SetScalarModeToUseCellData()
        self.surface_mapper.SetScalarModeToUseCellData()
        self.volume_mapper.SetScalarModeToUseCellData()

    def set_color(self, color: Color):
        rgb = color.to_rgb()
        for i in range(3):
            self.node_colors.FillComponent(i, rgb[i])
            self.surface_colors.FillComponent(i, rgb[i])
            self.volume_colors.FillComponent(i, rgb[i])
            self.result_colors.FillComponent(i, rgb[i])

    def set_coordinates(self, nodal_coordinates: np.ndarray):
        self.points.SetData(numpy_to_vtk(nodal_coordinates))

    def reset_coordinates(self):
        if self.mesh is None:
            return

        if self.mesh.nodal_coordinates is None:
            return

        nodal_coordinates = self.mesh.nodal_coordinates[:, 1:]
        self.points.SetData(numpy_to_vtk(nodal_coordinates))

    def set_color_scalars(
        self,
        values: np.ndarray,
        min_value=None,
        max_value=None,
        hide_out_of_range=False,
        colormap="viridis",
    ):
        color_table = ColorTable(values, min_value, max_value, colormap)
        if hide_out_of_range:
            color_table.SetBelowRangeColor(0, 0, 0, 0)
            color_table.SetAboveRangeColor(0, 0, 0, 0)
            color_table.UseBelowRangeColorOn()
            color_table.UseAboveRangeColorOn()
        color_table.Build()

        mapped = color_table.MapScalars(numpy_to_vtk(values), 0, -1)
        self.result_colors.SetNumberOfTuples(len(values))
        vtk_to_numpy(self.result_colors)[:] = vtk_to_numpy(mapped)

    def reset_color_scalars(self):
        self.result_colors.Fill(0)

    def set_node_color(self, color: Color):
        rgb = color.to_rgb()
        for i in range(3):
            self.node_colors.FillComponent(i, rgb[i])

    def set_edge_color(self, color: Color):
        self.edge_actor.GetProperty().SetColor(*color.to_rgb_f())

    def set_surface_color(self, color: Color):
        rgb = color.to_rgb()
        for i in range(3):
            self.surface_colors.FillComponent(i, rgb[i])

    def set_volume_color(self, color: Color):
        rgb = color.to_rgb()
        for i in range(3):
            self.volume_colors.FillComponent(i, rgb[i])

    def set_nodes_size(self, size: int):
        self.node_actor.GetProperty().SetPointSize(size)

    def set_edge_width(self, size: int):
        self.edge_actor.GetProperty().SetLineWidth(size)

    def paint_nodes(self, color: Color, nodes: Iterable[int]):
        if self.mesh is None:
            return

        nodes = list(nodes)
        if not nodes:
            return

        node_ids = vtk_to_numpy(self.node_ids)
        node_colors = vtk_to_numpy(self.node_colors)

        paint_position_mask = np.isin(node_ids, nodes)
        node_colors[paint_position_mask, :3] = color.to_rgb()

    def paint_face_elements(self, color: Color, face_elements: Iterable[int]):
        if self.mesh is None:
            return

        face_elements = list(face_elements)
        if not face_elements:
            return

        surface_ids = vtk_to_numpy(self.surface_ids)
        surface_colors = vtk_to_numpy(self.surface_colors)
        paint_position_mask = np.isin(surface_ids, face_elements)
        surface_colors[paint_position_mask, :3] = color.to_rgb()

    def paint_solid_elements(self, color: Color, solid_elements: Iterable[int]):
        if self.mesh is None:
            return

        assert self.mesh.faces_connectivity is not None
        assert self.mesh.solids_connectivity is not None
        assert self.mesh.nodal_coordinates is not None

        solid_elements = list(solid_elements)
        if not solid_elements:
            return

        section_ids = vtk_to_numpy(self.volume_ids)
        section_colors = vtk_to_numpy(self.volume_colors)
        paint_position_mask = np.isin(section_ids, solid_elements)
        section_colors[paint_position_mask, :3] = color.to_rgb()

    def paint_surfaces(self, color: Color, surfaces: Iterable[int]):
        if self.mesh is None:
            return

        assert self.mesh.faces_connectivity is not None

        surfaces = list(surfaces)
        if not surfaces:
            return

        selected_face_elements, *_ = np.where(np.isin(self.mesh.faces_connectivity[:, 1], surfaces))
        self.paint_face_elements(color, selected_face_elements)

    def paint_volumes(self, color: Color, volumes: Iterable[int]):
        if self.mesh is None:
            return

        assert self.mesh.solids_connectivity is not None

        volumes = list(volumes)
        if not volumes:
            return

        surface_groups = [self.mesh.surfaces_from_volume[v] for v in volumes if (v in self.mesh.surfaces_from_volume)]
        surfaces = list(chain.from_iterable(surface_groups))
        self.paint_surfaces(color, surfaces)

        if self.section_plane is None:
            return

        section_ids = vtk_to_numpy(self.volume_ids)
        section_colors = vtk_to_numpy(self.volume_colors)

        volumes = list(volumes)
        selected_elements, *_ = np.where(np.isin(self.mesh.solids_connectivity[:, 1], volumes))
        paint_position_mask = np.isin(section_ids, selected_elements)
        section_colors[paint_position_mask, :3] = color.to_rgb()

    def set_nodes_visibility(self, visible: bool):
        self.node_actor.SetVisibility(visible)

    def set_edges_visibility(self, visible: bool):
        self.edge_actor.SetVisibility(visible)

    def set_surfaces_visibility(self, visible: bool):
        self.surface_actor.SetVisibility(visible)

    def set_solids_visibility(self, visible: bool):
        self.volume_actor.SetVisibility(visible)

    def hide_nodes(self, nodes: Sequence[int] | None = None):
        if nodes is None:
            vtk_to_numpy(self.node_colors)[:, 3] = 0
        else:
            self._set_node_cells_visibility(nodes, visible=False)

    def show_nodes(self, nodes: Sequence[int] | None = None):
        if nodes is None:
            vtk_to_numpy(self.node_colors)[:, 3] = 255
        else:
            self._set_node_cells_visibility(nodes, visible=True)

    def hide_surfaces(self, surfaces: Sequence[int] | None = None):
        if surfaces is None:
            vtk_to_numpy(self.surface_colors)[:, 3] = 0
        else:
            self._set_surface_cells_visibility(surfaces, visible=False)

    def hide_volumes(self, volumes: Sequence[int] | None = None):
        if volumes is None:
            vtk_to_numpy(self.volume_colors)[:, 3] = 0
        else:
            self._set_volume_cells_visibility(volumes, visible=False)

    def show_surfaces(self, surfaces: Sequence[int] | None = None):
        if surfaces is None:
            vtk_to_numpy(self.surface_colors)[:, 3] = 255
        else:
            self._set_surface_cells_visibility(surfaces, visible=True)

    def show_volumes(self, volumes: Sequence[int] | None = None):
        if volumes is None:
            vtk_to_numpy(self.volume_colors)[:, 3] = 255
        else:
            self._set_volume_cells_visibility(volumes, visible=True)

    def _set_node_cells_visibility(self, nodes: Sequence[int], *, visible: bool):
        if self.mesh is None:
            return

        node_ids = vtk_to_numpy(self.node_ids)
        node_colors = vtk_to_numpy(self.node_colors)

        alpha = 255 if visible else 0
        mask = np.isin(node_ids, nodes)
        node_colors[mask, 3] = alpha

    def _set_surface_cells_visibility(self, surfaces: Sequence[int], *, visible: bool):
        if self.mesh is None:
            return

        assert self.mesh.faces_connectivity is not None

        surface_ids = vtk_to_numpy(self.surface_ids)
        surface_colors = vtk_to_numpy(self.surface_colors)

        alpha = 255 if visible else 0
        selected_face_elements, *_ = np.where(np.isin(self.mesh.faces_connectivity[:, 1], surfaces))
        mask = np.isin(surface_ids, selected_face_elements)
        surface_colors[mask, 3] = alpha

    def _set_volume_cells_visibility(self, volumes: Sequence[int], *, visible: bool):
        if self.mesh is None:
            return

        assert self.mesh.solids_connectivity is not None

        surface_groups = [self.mesh.surfaces_from_volume[v] for v in volumes if (v in self.mesh.surfaces_from_volume)]
        surfaces = list(chain.from_iterable(surface_groups))
        self._set_surface_cells_visibility(surfaces, visible=visible)

        if self.section_plane is None:
            return

        section_ids = vtk_to_numpy(self.volume_ids)
        section_colors = vtk_to_numpy(self.volume_colors)

        alpha = 255 if visible else 0
        selected_elements, *_ = np.where(np.isin(self.mesh.solids_connectivity[:, 1], volumes))
        paint_position_mask = np.isin(section_ids, selected_elements)
        section_colors[paint_position_mask, 3] = alpha

    def _get_parts(self) -> list[vtkActor]:
        return list(self.GetParts())  # pyright: ignore[reportArgumentType]

    def _create_cells(self, connectivity: np.ndarray) -> vtkCellArray:
        if connectivity.ndim == 1:
            connectivity = connectivity.reshape(-1, 1)

        helper = np.insert(connectivity, 0, connectivity.shape[1], axis=1)
        vtk_id_array = numpy_to_vtkIdTypeArray(helper.ravel())
        cell_array = vtkCellArray()
        cell_array.SetCells(connectivity.shape[0], vtk_id_array)
        return cell_array

    def _linearize_2d_cells(self, connectivity: np.ndarray) -> np.ndarray:
        n_nodes = connectivity[:, 4:].shape[1]
        match n_nodes:
            case 3 | 4:
                reorderings = list(pairwise(range(n_nodes)))
            case 6:
                reorderings = [
                    [0, 3], [3, 1],
                    [1, 4], [4, 2],
                    [2, 5], [5, 0],
                ]  # fmt: skip
            case 8:
                reorderings = [
                    [0, 4], [4, 1],
                    [1, 5], [5, 2],
                    [2, 6], [6, 3],
                    [3, 7], [7, 0],
                ]  # fmt: skip
            case _:
                raise NotImplementedError(f"Exploding to 2D cells is not supported for {n_nodes}-node cells")
        return self._explode_cells(connectivity, reorderings)

    def _linearize_3d_cells(self, connectivity: np.ndarray) -> np.ndarray:
        n_nodes = connectivity[:, 4:].shape[1]
        match n_nodes:
            case 4:
                reorderings = list(combinations(range(n_nodes), 2))
            case 8:
                reorderings = [
                    [0, 1], [1, 2], [2, 3], [3, 0],
                    [4, 5], [5, 6], [6, 7], [7, 4],
                    [0, 4], [1, 5], [2, 6], [3, 7],
                ]  # fmt: skip
            case 10:
                reorderings = [
                    [0, 4], [4, 1], [1, 5], [5, 2], [0, 6], [6, 2],
                    [0, 7], [7, 3], [2, 8], [8, 3], [1, 9], [9, 3],
                ]  # fmt: skip
            case 20:
                reorderings = [
                    [0, 8], [8, 1],
                    [1, 11], [11, 2],
                    [2, 13], [13, 3],
                    [3, 9], [9, 0],
                    [4, 16], [16, 5],
                    [5, 18], [18, 6],
                    [6, 19], [19, 7],
                    [7, 17], [17, 4],
                    [0, 10], [10, 4],
                    [1, 12], [12, 5],
                    [2, 14], [14, 6],
                    [3, 15], [15, 7],
                ]  # fmt: skip
            case _:
                raise NotImplementedError(f"Exploding to 2D cells is not supported for {n_nodes}-node cells")
        return self._explode_cells(connectivity, reorderings)

    def _triangulate_2d_cells(self, connectivity: np.ndarray) -> np.ndarray:
        n_nodes = connectivity[:, 4:].shape[1]
        match n_nodes:
            case 3:
                return connectivity
            case 4:
                reorderings = [[0, 3, 1], [1, 3, 2]]
            case 6:
                reorderings = [[0, 3, 5], [1, 4, 3], [2, 5, 4], [3, 4, 5]]
            case 8:
                reorderings = [
                    [0, 4, 7], [1, 5, 4], [2, 6, 5], [3, 7, 6], [4, 5, 6], [4, 6, 7],
                ]  # fmt: skip
            case _:
                raise NotImplementedError(f"Exploding to 2D cells is not supported for {n_nodes}-node cells")
        return self._explode_cells(connectivity, reorderings)

    def _triangulate_3d_cells(self, connectivity: np.ndarray) -> np.ndarray:
        n_nodes = connectivity[:, 4:].shape[1]

        match n_nodes:
            case 4:  # Tetrahedron Linear
                reorderings = list(combinations(range(n_nodes), 3))
            case 8:
                reorderings = [
                    [0, 1, 2], [0, 2, 3],
                    [4, 5, 6], [4, 6, 7],
                    [0, 1, 5], [0, 5, 4],
                    [3, 2, 6], [3, 6, 7],
                    [0, 3, 7], [0, 7, 4],
                    [1, 2, 6], [1, 6, 5],
                ]  # fmt: skip
            case 10:  # Tetrahedron Quadratic
                reorderings = [
                    [0, 4, 6], [1, 5, 4], [2, 6, 5], [4, 5, 6],
                    [0, 7, 4], [3, 9, 7], [1, 4, 9], [7, 9, 4],
                    [0, 6, 7], [2, 8, 6], [3, 7, 8], [6, 8, 7],
                    [1, 9, 5], [3, 8, 9], [2, 5, 8], [9, 8, 5],
                ]  # fmt: skip
            case 20:
                reorderings = [
                    [0, 8, 9], [1, 11, 8], [2, 13, 11], [3, 9, 13], [8, 11, 13], [8, 13, 9],
                    [4, 16, 17], [5, 18, 16], [6, 19, 18], [7, 17, 19], [16, 18, 19], [16, 19, 17],
                    [0, 8, 10], [1, 12, 8], [5, 16, 12], [4, 10, 16], [8, 12, 16], [8, 16, 10],
                    [2, 13, 14], [3, 15, 13], [7, 19, 15], [6, 14, 19], [13, 15, 19], [13, 19, 14],
                    [0, 9, 10], [3, 15, 9], [7, 17, 15], [4, 10, 17], [9, 15, 17], [9, 17, 10],
                    [1, 11, 12], [2, 14, 11], [6, 18, 14], [5, 12, 18], [11, 14, 18], [11, 18, 12],
                ]  # fmt: skip
            case _:
                raise NotImplementedError(f"Exploding to 2D cells is not supported for {n_nodes}-node cells")

        return self._explode_cells(connectivity, reorderings)

    def _explode_cells(self, connectivity: np.ndarray, reorderings: Sequence[Sequence[int]]) -> np.ndarray:
        column_order = [
            [0, 1, 2, 3] + [i + 4 for i in reordering]
            for reordering in reorderings
        ]  # fmt: skip

        stacked = []
        for order in column_order:
            connect = connectivity[:, order]
            stacked.append(connect)

        return np.concatenate(stacked)

    def _find_masked_nodes(self) -> np.ndarray:
        if self.mesh is None:
            return np.array([], dtype=int)

        if self.mesh.nodal_coordinates is None:
            return np.array([], dtype=int)

        if self.mesh.solids_connectivity is None:
            return np.array([], dtype=int)

        if self.section_plane is None:
            return np.array([], dtype=int)

        coordinates = self.mesh.nodal_coordinates[:, 1:]

        mask = inside_plane(
            coordinates,
            self.section_plane.origin,
            self.section_plane.get_normal(),
        ).ravel()

        return mask

    def _mesh_updated(self):
        if id(self.mesh) != self.cached_info.mesh_id:
            return True

        if hash(self.section_plane) != self.cached_info.section_plane_hash:  # noqa: SIM103
            return True

        return False
