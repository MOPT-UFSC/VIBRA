from collections.abc import Iterable
from enum import IntEnum, auto

import numpy as np
from scipy.linalg import svd
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals, vtkPolyDataTangents
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkPropAssembly

from vibra import TEXTURE_DIR
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.utils.interface_utils import SectionPlane
from vibra.utils.time_utils import function_timer
from vibra.utils.vtk_utils import read_texture


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


class GeometryActor(vtkPropAssembly):
    def __init__(self, model: Model | None):
        super().__init__()

        self.model = model
        self.section_plane: SectionPlane | None = None

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

    def clear_data(self):
        self.surface_data.SetPolys(vtkCellArray())
        self.edge_colors.SetNumberOfTuples(0)
        self.edge_colors.Modified()
        self.surface_colors.SetNumberOfTuples(0)
        self.surface_colors.Modified()
        self._node_surface_ids = np.array([], dtype=int)
        self._cell_surface_ids = np.array([], dtype=int)

    def _create_variables(self):
        self.points = vtkPoints()
        self.texture_coords = vtkFloatArray()

        self.edge_colors = vtkUnsignedCharArray()
        self.edge_data = vtkPolyData()
        self.edge_mapper = vtkPolyDataMapper()
        self.edge_actor = vtkActor()

        self.surface_colors = vtkUnsignedCharArray()
        self.surface_data = vtkPolyData()
        self.surface_mapper = vtkPolyDataMapper()
        self.surface_actor = vtkActor()

        self._line_ids = np.array([], dtype=int)
        self._node_surface_ids = np.array([], dtype=int)
        self._cell_surface_ids = np.array([], dtype=int)

        self.diffuse_texture = read_texture(TEXTURE_DIR / "diffuse.jpg")

    def _configure_actors_parameters(self):
        self.texture_coords.SetName("tcoords")

        self.edge_colors.SetName("color")
        self.edge_colors.SetNumberOfComponents(3)
        self.edge_data.SetPoints(self.points)
        self.edge_data.GetCellData().SetScalars(self.edge_colors)
        self.edge_mapper.SetInputData(self.edge_data)
        self.edge_mapper.SetResolveCoincidentTopologyToShiftZBuffer()
        self.edge_actor.SetMapper(self.edge_mapper)
        self.edge_actor.GetProperty().SetRepresentationToWireframe()
        self.edge_actor.GetProperty().SetLineWidth(7)
        self.edge_actor.GetProperty().SetColor(1, 1, 1)
        self.AddPart(self.edge_actor)

        self.surface_colors.SetName("color")
        self.surface_colors.SetNumberOfComponents(4)
        self.surface_data.SetPoints(self.points)
        self.surface_data.GetCellData().SetScalars(self.surface_colors)
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

        nodal_coordinates, faces_connectivity = self._decouple_faces_connectivity()
        nodal_coordinates[:, 1] += 2
        self._nodal_surface_ids = np.zeros(shape=len(nodal_coordinates), dtype=int)
        self._nodal_surface_ids[faces_connectivity[:, 4:]] = faces_connectivity[:, 1, None]
        self.points.SetData(numpy_to_vtk(nodal_coordinates[:, 1:]))
        self.points.Modified()

        lines_linearized = self._linearize_1d_cells(self.mesh.lines_connectivity)
        line_cells = self._create_cells(lines_linearized[:, 4:])
        self._line_ids = lines_linearized[:, 1].flatten()
        self.edge_colors.SetNumberOfTuples(len(lines_linearized))
        self.edge_colors.Fill(0)
        self.edge_data.SetLines(line_cells)

        faces_triangulated = self._triangulate_2d_cells(faces_connectivity)
        face_cells = self._create_cells(faces_triangulated[:, 4:])
        self._cell_surface_ids = faces_triangulated[:, 1]
        self.surface_data.SetPolys(face_cells)
        self.surface_colors.SetNumberOfTuples(len(faces_triangulated))
        self.surface_mapper.Modified()
        self.surface_colors.Fill(255)

        self._add_nodal_texture_info(nodal_coordinates, faces_connectivity)

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
        self.surface_data.GetPointData().SetTCoords(numpy_to_vtk(texture_coordinates))

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

    @function_timer
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

    def _reduce_connectivity(
        self,
        nodal_coordinates: np.ndarray,
        surface_connectivity: np.ndarray,
        mapping: np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:

        old_indices = np.unique(surface_connectivity[:, 4:])
        new_indices = np.arange(len(old_indices))

        if mapping is None:
            mapping = np.zeros(np.max(surface_connectivity[:, 4:]) + 1, dtype=int)
        mapping[old_indices] = new_indices

        new_coordinates = nodal_coordinates[old_indices]
        new_connectivity = surface_connectivity.copy()
        new_connectivity[:, 4:] = mapping[surface_connectivity[:, 4:]]

        return new_coordinates, new_connectivity

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

    def _create_cells(self, connectivity: np.ndarray) -> vtkCellArray:
        if connectivity.ndim == 1:
            connectivity = connectivity.reshape(-1, 1)

        helper = np.insert(connectivity, 0, connectivity.shape[1], axis=1)
        vtk_id_array = numpy_to_vtkIdTypeArray(helper.ravel())
        cell_array = vtkCellArray()
        cell_array.SetCells(connectivity.shape[0], vtk_id_array)
        return cell_array

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

    def _linearize_1d_cells(self, connectivity: np.ndarray) -> np.ndarray:
        n_nodes = connectivity[:, 4:].shape[1]
        match n_nodes:
            case 0:
                return np.zeros(shape=(0, 4 + 2), dtype=int)
            case 2:
                return connectivity
            case 3:
                reorderings = [[0, 2], [2, 1]]
            case _:
                raise NotImplementedError(f"Exploding to 1D cells is not supported for {n_nodes}-node cells")
        return self._explode_cells(connectivity, reorderings)

    def _explode_cells(self, connectivity: np.ndarray, reorderings: Iterable[Iterable[int]]) -> np.ndarray:
        column_order = [
            [0, 1, 2, 3] + [i + 4 for i in reordering]
            for reordering in reorderings
        ]  # fmt: skip

        stacked = []
        for order in column_order:
            connect = connectivity[:, order]
            stacked.append(connect)

        return np.vstack(stacked)
