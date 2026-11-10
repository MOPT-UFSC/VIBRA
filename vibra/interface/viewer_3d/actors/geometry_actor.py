from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from enum import IntEnum, auto

import numpy as np
import xxhash
from molde import Color
from scipy.linalg import svd
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkDataArray, vtkFloatArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals, vtkPolyDataTangents
from vtkmodules.vtkRenderingCore import vtkActor, vtkAreaPicker, vtkHardwarePicker, vtkPolyDataMapper, vtkPropAssembly, vtkRenderer

from vibra import TEXTURE_DIR
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.utils.interface_utils import SectionPlane
from vibra.utils.math_functions import inside_plane
from vibra.utils.time_utils import function_timer
from vibra.utils.vtk_utils import create_cells, linearize_1d_cells, read_texture, triangulate_2d_cells


class GeometryTextures(IntEnum):
    WHITE_TEXTURE = auto()
    CHESS_TEXTURE = auto()
    SPONGE_TEXTURE = auto()
    HOLES_TEXTURE = auto()

    def bias(self):
        return (float(self) - 1) * self.span()

    @classmethod
    def span(cls):
        return 1 / len(cls)


@dataclass
class GeometryCachedInfo:
    mesh_id: int = 0
    point_colors_hash: str = ""
    line_colors_hash: str = ""
    surface_colors_hash: str = ""
    texture_coords_hash: str = ""
    section_plane_hash: int = 0

    @classmethod
    def array_hash(cls, array: np.ndarray | vtkDataArray) -> str:
        ndarray = vtk_to_numpy(array) if isinstance(array, vtkDataArray) else array
        hasher = xxhash.xxh128()
        hasher.update(ndarray)
        return hasher.hexdigest()


@dataclass
class PickedGeometry:
    picked_points: set[int] = field(default_factory=set)
    picked_lines: set[int] = field(default_factory=set)
    picked_surfaces: set[int] = field(default_factory=set)

    def clear(self):
        self.picked_points.clear()
        self.picked_lines.clear()
        self.picked_surfaces.clear()


class GeometryActor(vtkPropAssembly):
    def __init__(self, model: Model | None):
        super().__init__()

        self.model = model
        self.section_plane: SectionPlane | None = None
        self.cached_info = GeometryCachedInfo()

        self._create_variables()
        self._configure_actors_parameters()

    @property
    def mesh(self) -> Mesh | None:
        if self.model is None:
            return

        return self.model.mesh

    def update(self):
        if self.mesh is None:
            self.clear_data()
            return

        self.build_mesh()

        self.update_caches()

    def clear_data(self):
        self.point_data.SetPolys(vtkCellArray())
        self.point_colors.SetNumberOfTuples(0)
        self.point_colors.Modified()

        self.line_data.SetPolys(vtkCellArray())
        self.line_colors.SetNumberOfTuples(0)
        self.line_colors.Modified()

        self.surface_data.SetPolys(vtkCellArray())
        self.surface_colors.SetNumberOfTuples(0)
        self.surface_colors.Modified()

        self._point_ids = np.array([], dtype=int)
        self._line_ids = np.array([], dtype=int)
        self._node_surface_ids = np.array([], dtype=int)
        self._cell_surface_ids = np.array([], dtype=int)

    def _create_variables(self):
        self.hardware_picker = vtkHardwarePicker()
        self.hardware_picker.SetPixelTolerance(0)
        self.hardware_picker.SnapToMeshPointOff()
        self.area_picker = vtkAreaPicker()
        self.area_picker.PickFromListOn()

        self.points = vtkPoints()
        self.texture_coords = vtkFloatArray()

        self.point_colors = vtkUnsignedCharArray()
        self.point_data = vtkPolyData()
        self.point_mapper = vtkPolyDataMapper()
        self.point_mapper.SetResolveCoincidentTopologyToShiftZBuffer()
        self.point_actor = vtkActor()

        self.line_colors = vtkUnsignedCharArray()
        self.line_data = vtkPolyData()
        self.line_mapper = vtkPolyDataMapper()
        self.line_actor = vtkActor()

        self.surface_colors = vtkUnsignedCharArray()
        self.surface_data = vtkPolyData()
        self.surface_mapper = vtkPolyDataMapper()
        self.surface_actor = vtkActor()

        self._point_ids = np.array([], dtype=int)
        self._line_ids = np.array([], dtype=int)
        self._node_surface_ids = np.array([], dtype=int)
        self._cell_surface_ids = np.array([], dtype=int)

        self.diffuse_texture = read_texture(TEXTURE_DIR / "diffuse.jpg")

    def _configure_actors_parameters(self):
        self.texture_coords.SetName("tcoords")
        self.texture_coords.SetNumberOfComponents(2)

        self.point_colors.SetName("color")
        self.point_colors.SetNumberOfComponents(4)
        self.point_data.SetPoints(self.points)
        self.point_data.GetCellData().SetScalars(self.point_colors)
        self.point_mapper.SetInputData(self.point_data)
        self.point_actor.SetMapper(self.point_mapper)
        self.point_actor.GetProperty().SetPointSize(15)
        self.point_actor.GetProperty().RenderPointsAsSpheresOn()
        self.point_actor.GetProperty().LightingOff()
        self.AddPart(self.point_actor)

        self.line_colors.SetName("color")
        self.line_colors.SetNumberOfComponents(4)
        self.line_data.SetPoints(self.points)
        self.line_data.GetCellData().SetScalars(self.line_colors)
        self.line_mapper.SetInputData(self.line_data)
        self.line_mapper.SetResolveCoincidentTopologyToShiftZBuffer()
        self.line_actor.SetMapper(self.line_mapper)
        self.line_actor.GetProperty().SetRepresentationToWireframe()
        self.line_actor.GetProperty().RenderLinesAsTubesOn()
        self.line_actor.GetProperty().SetLineWidth(5)
        self.line_actor.GetProperty().SetColor(1, 1, 1)
        self.AddPart(self.line_actor)

        self.surface_colors.SetName("color")
        self.surface_colors.SetNumberOfComponents(4)
        self.surface_data.SetPoints(self.points)
        self.surface_data.GetCellData().SetScalars(self.surface_colors)
        self.surface_data.GetPointData().SetTCoords(self.texture_coords)
        self.surface_mapper.SetInputData(self.surface_data)
        self.surface_actor.SetMapper(self.surface_mapper)
        self.surface_actor.SetTexture(self.diffuse_texture)
        self.AddPart(self.surface_actor)

    @function_timer
    def build_mesh(self):
        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None
        assert self.mesh.lines_connectivity is not None
        assert self.mesh.faces_connectivity is not None

        if not self._mesh_updated():
            return

        nodal_coordinates, faces_connectivity = self._decouple_faces_connectivity()
        nodal_coordinates[:, 1] += 2
        self.points.SetData(numpy_to_vtk(nodal_coordinates[:, 1:]))
        self.points.Modified()

        nodes = np.array(list(self.mesh.nodes_from_points.values()))
        point_cells = create_cells(nodes)
        self.point_data.SetVerts(point_cells)
        self.point_colors.SetNumberOfTuples(len(nodes))
        self.point_colors.Fill(0)
        vtk_to_numpy(self.point_colors)[:, 3] = 255
        self._point_ids = np.array(self.mesh.nodes_from_points.keys())

        lines_linearized = linearize_1d_cells(self.mesh.lines_connectivity)
        line_cells = create_cells(lines_linearized[:, 4:])
        self.line_data.SetLines(line_cells)
        self.line_colors.SetNumberOfTuples(len(lines_linearized))
        self.line_colors.Fill(0)
        vtk_to_numpy(self.line_colors)[:, 3] = 255
        self._line_ids = lines_linearized[:, 1].flatten()

        faces_triangulated = triangulate_2d_cells(faces_connectivity)
        face_cells = create_cells(faces_triangulated[:, 4:])
        self.surface_data.SetPolys(face_cells)
        self.surface_colors.SetNumberOfTuples(len(faces_triangulated))
        self.surface_colors.Fill(255)
        self._cell_surface_ids = faces_triangulated[:, 1]
        self._nodal_surface_ids = np.zeros(shape=len(nodal_coordinates), dtype=int)
        self._nodal_surface_ids[faces_connectivity[:, 4:]] = faces_connectivity[:, 1, None]

        self._add_nodal_texture_info(nodal_coordinates, faces_connectivity)

    def update_caches(self):
        point_colors_hash = GeometryCachedInfo.array_hash(self.point_colors)
        if point_colors_hash != self.cached_info.point_colors_hash:
            self.cached_info.point_colors_hash = point_colors_hash
            self.point_colors.Modified()

        line_colors_hash = GeometryCachedInfo.array_hash(self.line_colors)
        if line_colors_hash != self.cached_info.line_colors_hash:
            self.cached_info.line_colors_hash = line_colors_hash
            self.line_colors.Modified()

        surface_colors_hash = GeometryCachedInfo.array_hash(self.surface_colors)
        if surface_colors_hash != self.cached_info.surface_colors_hash:
            self.cached_info.surface_colors_hash = surface_colors_hash
            self.surface_colors.Modified()

        texture_coords_hash = GeometryCachedInfo.array_hash(self.texture_coords)
        if texture_coords_hash != self.cached_info.texture_coords_hash:
            self.cached_info.texture_coords_hash = texture_coords_hash
            self.texture_coords.Modified()

        mesh_id = id(self.mesh)
        if mesh_id != self.cached_info.mesh_id:
            self.cached_info.mesh_id = mesh_id
            # Don't need to modify anything, but might in the future

        section_plane_hash = hash(self.section_plane)
        if section_plane_hash != self.cached_info.section_plane_hash:
            self.cached_info.section_plane_hash = section_plane_hash

    def pick(self, x: int, y: int, renderer: vtkRenderer) -> PickedGeometry:
        self.hardware_picker.Pick(x, y, 0, renderer)
        cell_id = self.hardware_picker.GetCellId()

        match self.hardware_picker.GetActor():
            case self.surface_actor:
                ids = self._cell_surface_ids
                if 0 < cell_id < len(ids):
                    return PickedGeometry(picked_surfaces={ids[cell_id]})

            case self.line_actor:
                ids = self._line_ids
                if 0 < cell_id < len(ids):
                    return PickedGeometry(picked_lines={ids[cell_id]})

            case self.point_actor:
                ids = self._point_ids
                if 0 < cell_id < len(ids):
                    return PickedGeometry(picked_points={ids[cell_id]})
            case _:
                ...

        return PickedGeometry()

    def area_pick(self, x0: int, y0: int, x1: int, y1: int, renderer: vtkRenderer) -> PickedGeometry:
        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None
        assert self.mesh.faces_connectivity is not None
        assert self.mesh.solids_connectivity is not None

        coordinates = self.mesh.nodal_coordinates[:, 1:]
        lines_only_connectivity = self.mesh.lines_connectivity[:, 4:]
        faces_only_connectivity = self.mesh.faces_connectivity[:, 4:]

        if self.section_plane is None:
            nodes_mask = np.ones(len(coordinates), dtype=bool)
        else:
            nodes_mask = self._masked_nodes.copy()
            visible_node_ids = self._node_ids
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

        lines_mask = nodes_mask[lines_only_connectivity].any(axis=1)
        faces_mask = nodes_mask[faces_only_connectivity].any(axis=1)
        nodes = self.mesh.nodal_coordinates[nodes_mask, 1].astype(int)

        return PickedGeometry(
            picked_points={self.mesh.points_from_nodes[i] for i in nodes if i in self.mesh.points_from_nodes},
            picked_lines=set(self.mesh.lines_connectivity[lines_mask, 1]),
            picked_surfaces=set(self.mesh.faces_connectivity[faces_mask, 1]),
        )

    def _decouple_faces_connectivity(self):
        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None
        assert self.mesh.faces_connectivity is not None

        seen = np.zeros(shape=len(self.mesh.nodal_coordinates), dtype=bool)
        nodes_stack = [self.mesh.nodal_coordinates]
        connectivity = self.mesh.faces_connectivity.copy()
        existing_nodes = len(self.mesh.nodal_coordinates)

        for surface_elements in self.mesh.elements_from_surface.values():
            # Find the nodes that have already appeared in previous surfaces
            surface_nodes = self.mesh.faces_connectivity[surface_elements, 4:]
            repeated_mask = seen[surface_nodes]
            repeated_nodes, inverse_indices = np.unique(
                surface_nodes[repeated_mask],
                return_inverse=True,
            )
            new_nodes = np.arange(len(repeated_nodes)) + existing_nodes

            # Copy the repetitons in such a way that the surfaces do not share a common node
            nodes_stack.append(self.mesh.nodal_coordinates[repeated_nodes])
            rows, cols = np.where(repeated_mask)
            connectivity[surface_elements[rows], 4 + cols] = new_nodes[inverse_indices]

            # Update values for the next iterations
            existing_nodes += len(repeated_nodes)
            seen[surface_nodes] = True

        return np.vstack(nodes_stack), connectivity

    def _add_nodal_texture_info(self, nodal_coordinates: np.ndarray, faces_connectivity: np.ndarray):
        assert self.mesh is not None

        texture_coordinates = np.zeros(shape=(len(nodal_coordinates), 2))
        for surface_id, surface_elements in self.mesh.elements_from_surface.items():
            node_indices = np.unique(faces_connectivity[surface_elements, 4:])
            surface_normals = self.mesh.normals_surface.get(surface_id)

            if surface_normals is not None:
                normal = np.average(surface_normals, axis=0).round(6)
            else:
                normal = None

            texture_coordinates[node_indices] = self._generate_tcoords(
                nodal_coordinates[node_indices, 1:],
                normal=normal,
            )

        min_t = texture_coordinates.min()
        max_t = texture_coordinates.max()
        texture_coordinates -= min_t
        if min_t != max_t:
            texture_coordinates /= max_t - min_t
        texture_coordinates[:, 0] /= len(GeometryTextures)
        self.texture_coords.SetNumberOfTuples(len(texture_coordinates))
        vtk_to_numpy(self.texture_coords)[:] = texture_coordinates

        self.surface_data.GetPointData().RemoveArray("Normals")
        add_normals = vtkPolyDataNormals()
        add_normals.SplittingOff()
        add_normals.SetInputData(self.surface_data)
        add_normals.Update()
        normals = add_normals.GetOutput().GetPointData().GetNormals()
        self.surface_data.GetPointData().SetNormals(normals)

        self.surface_data.GetPointData().RemoveArray("Tangents")
        add_tangents = vtkPolyDataTangents()
        add_tangents.SetInputData(self.surface_data)
        add_tangents.Update()
        tangents = add_tangents.GetOutput().GetPointData().GetTangents()
        self.surface_data.GetPointData().SetTangents(tangents)

        self.surface_data.Modified()

    def clear_textures(self):
        uv = vtk_to_numpy(self.surface_data.GetPointData().GetTCoords())
        uv[:] = uv % GeometryTextures.span()

    def set_surface_texture(self, texture: GeometryTextures, surfaces: Iterable[int]):
        surfaces = list(surfaces)
        if not surfaces:
            return

        texture = GeometryTextures(texture)
        uv = vtk_to_numpy(self.surface_data.GetPointData().GetTCoords())
        u = uv[:, 0]
        mask = np.isin(self._nodal_surface_ids, surfaces)
        if mask.size:
            u[mask] = u[mask] % GeometryTextures.span() + texture.bias()
            self.surface_data.GetPointData().GetTCoords().Modified()  # move it to update cache

    def set_point_color(self, color: Color):
        rgb = color.to_rgb()
        for i in range(3):
            self.point_colors.FillComponent(i, rgb[i])

    def set_line_color(self, color: Color):
        rgb = color.to_rgb()
        for i in range(3):
            self.line_colors.FillComponent(i, rgb[i])

    def set_surface_color(self, color: Color):
        rgb = color.to_rgb()
        for i in range(3):
            self.surface_colors.FillComponent(i, rgb[i])

    def set_point_size(self, size: int):
        self.point_actor.GetProperty().SetPointSize(size)

    def set_line_thickness(self, thickness):
        self.line_actor.GetProperty().SetLineWidth(thickness)

    def paint_points(self, color: Color, points: Iterable[int]):
        if self.mesh is None:
            return

        points = list(points)
        if not points:
            return

        point_ids = self._point_ids
        point_colors = vtk_to_numpy(self.point_colors)

        mask = np.isin(point_ids, points)
        point_colors[mask, :3] = color.to_rgb()

    def paint_lines(self, color: Color, lines: Iterable[int]):
        if self.mesh is None:
            return

        lines = list(lines)
        if not lines:
            return

        line_ids = self._line_ids
        line_colors = vtk_to_numpy(self.line_colors)

        mask = np.isin(line_ids, lines)
        line_colors[mask, :3] = color.to_rgb()

    def paint_surfaces(self, color: Color, surfaces: Iterable[int]):
        if self.mesh is None:
            return

        surfaces = list(surfaces)
        if not surfaces:
            return

        surface_ids = self._cell_surface_ids
        surface_colors = vtk_to_numpy(self.surface_colors)

        mask = np.isin(surface_ids, surfaces)
        surface_colors[mask, :3] = color.to_rgb()

    def set_points_visibility(self, visible: bool):
        self.point_actor.SetVisibility(visible)

    def set_lines_visibility(self, visible: bool):
        self.line_actor.SetVisibility(visible)

    def set_surfaces_visibility(self, visible: bool):
        self.surface_actor.SetVisibility(visible)

    def hide_points(self, points: Sequence[int] | None = None):
        if points is None:
            vtk_to_numpy(self.point_colors)[:, 3] = 0
        else:
            self._set_point_cells_visibility(points, visible=False)

    def show_points(self, points: Sequence[int] | None = None):
        if points is None:
            vtk_to_numpy(self.point_colors)[:, 3] = 255
        else:
            self._set_point_cells_visibility(points, visible=True)

    def hide_lines(self, lines: Sequence[int] | None = None):
        if lines is None:
            vtk_to_numpy(self.line_colors)[:, 3] = 0
        else:
            self._set_line_cells_visibility(lines, visible=False)

    def show_lines(self, lines: Sequence[int] | None = None):
        if lines is None:
            vtk_to_numpy(self.line_colors)[:, 3] = 255
        else:
            self._set_line_cells_visibility(lines, visible=True)

    def hide_surfaces(self, surfaces: Sequence[int] | None = None):
        if surfaces is None:
            vtk_to_numpy(self.surface_colors)[:, 3] = 0
        else:
            self._set_surface_cells_visibility(surfaces, visible=False)

    def show_surfaces(self, surfaces: Sequence[int] | None = None):
        if surfaces is None:
            vtk_to_numpy(self.surface_colors)[:, 3] = 255
        else:
            self._set_surface_cells_visibility(surfaces, visible=True)

    def _set_point_cells_visibility(self, points: Sequence[int], *, visible: bool):
        if self.mesh is None:
            return

        point_ids = self._point_ids
        point_colors = vtk_to_numpy(self.point_colors)

        alpha = 255 if visible else 0
        mask = np.isin(point_ids, points)
        point_colors[mask, 3] = alpha

    def _set_line_cells_visibility(self, lines: Sequence[int], *, visible: bool):
        if self.mesh is None:
            return

        line_ids = self._line_ids
        line_colors = vtk_to_numpy(self.line_colors)

        alpha = 255 if visible else 0
        mask = np.isin(line_ids, lines)
        line_colors[mask, 3] = alpha

    def _set_surface_cells_visibility(self, surfaces: Sequence[int], *, visible: bool):
        if self.mesh is None:
            return

        surface_ids = self._cell_surface_ids
        surface_colors = vtk_to_numpy(self.surface_colors)

        alpha = 255 if visible else 0
        mask = np.isin(surface_ids, surfaces)
        surface_colors[mask, 3] = alpha

    def _generate_tcoords(
        self,
        coords: np.ndarray,
        normal: np.ndarray | None = None,
    ):
        centered = coords - coords.mean(axis=0)
        _, s, Vh = svd(centered, full_matrices=False, check_finite=False)

        if normal is not None:
            n = np.asarray(normal, dtype=float)
            n = n / np.linalg.norm(n)
            Vh = Vh[np.argsort(np.abs(Vh @ n))]

        uv = centered @ np.asarray(Vh)[:2].T

        if s[2] > 1e-6:  # it is probably a cylinder, so use cylindrical projection
            max_v = np.abs(uv[:, 1]).max()
            normalized_v = uv[:, 1] / max_v
            uv[:, 1] = max_v * np.arcsin(normalized_v)

        return uv

    def _mesh_updated(self):
        if id(self.mesh) != self.cached_info.mesh_id:
            return True

        if hash(self.section_plane) != self.cached_info.section_plane_hash:  # noqa: SIM103
            return True

        return False
