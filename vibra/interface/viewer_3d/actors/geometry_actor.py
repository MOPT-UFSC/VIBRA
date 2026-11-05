from collections.abc import Iterable

import numpy as np
from scipy.linalg import svd
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkIntArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals, vtkPolyDataTangents
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkPropAssembly

from vibra import TEXTURE_DIR
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.utils.interface_utils import SectionPlane
from vibra.utils.time_utils import function_timer
from vibra.utils.vtk_utils import read_texture


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
        self.surface_colors.SetNumberOfTuples(0)
        self.surface_ids.SetNumberOfTuples(0)
        self.surface_colors.Modified()

    def _create_variables(self):
        self.points = vtkPoints()

        self.surface_colors = vtkUnsignedCharArray()
        self.texture_coords = vtkFloatArray()
        self.surface_ids = vtkIntArray()
        self.surface_data = vtkPolyData()
        self.surface_mapper = vtkPolyDataMapper()
        self.surface_actor = vtkActor()

        self.diffuse_texture = read_texture(TEXTURE_DIR / "diffuse.jpg")

    def _configure_actors_parameters(self):
        self.surface_colors.SetName("color")
        self.surface_colors.SetNumberOfComponents(4)
        self.texture_coords.SetName("tcoords")
        self.surface_ids.SetName("ids")
        self.surface_data.SetPoints(self.points)
        self.surface_data.GetCellData().SetScalars(self.surface_colors)
        self.surface_data.GetCellData().AddArray(self.surface_ids)
        self.surface_mapper.SetInputData(self.surface_data)
        self.surface_actor.SetMapper(self.surface_mapper)
        self.surface_actor.SetTexture(self.diffuse_texture)
        self.AddPart(self.surface_actor)

    @function_timer
    def build_mesh(self):
        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None
        assert self.mesh.faces_connectivity is not None

        bias = 0
        nodal_coordinates = []
        faces_connectivity = []
        texture_coordinates = []

        # remaps the connectivity for each surface to keep a single
        # normal and tcoord for each point in the visual mesh
        for surface_elements in self.mesh.elements_from_surface.values():
            nodes, connectivity = self._reduce_connectivity(
                self.mesh.nodal_coordinates,
                self.mesh.faces_connectivity[surface_elements],
            )
            tcoords = self._generate_tcoords(nodes)
            nodal_coordinates.append(nodes)
            faces_connectivity.append(connectivity + bias)
            texture_coordinates.append(tcoords)
            bias += len(nodes)

        nodal_coordinates = np.vstack(nodal_coordinates)
        faces_connectivity = np.vstack(faces_connectivity)
        texture_coordinates = np.vstack(texture_coordinates)

        nodal_coordinates[:, 1] += 5

        self.points.SetData(numpy_to_vtk(nodal_coordinates[:, 1:]))
        self.points.Modified()

        faces_triangulated = self._triangulate_2d_cells(faces_connectivity)
        face_cells = self._create_cells(faces_triangulated[:, 4:])
        self.surface_data.SetPolys(face_cells)
        self.surface_colors.SetNumberOfTuples(len(faces_triangulated))
        self.surface_mapper.Modified()
        self.surface_colors.Fill(255)

        self.surface_ids.SetNumberOfTuples(len(faces_triangulated))
        vtk_to_numpy(self.surface_ids)[:] = faces_triangulated[:, 0]

        min_t = texture_coordinates.min()
        max_t = texture_coordinates.max()
        if min_t == max_t:
            texture_coordinates *= 0
        else:
            texture_coordinates = (texture_coordinates - min_t) / (max_t - min_t)
        texture_coordinates[:, 0] /= 4
        texture_coordinates[:, 0] += 0.25 * 0
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
        self.surface_mapper.Modified()

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

    def _generate_tcoords(self, nodal_coordinates: np.ndarray):
        coords = nodal_coordinates[:, 1:]
        centered = coords - coords.mean(axis=0)
        _, _, Vh = svd(centered, full_matrices=False)
        uv = centered @ np.asarray(Vh)[:2].T
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

    def _explode_cells(self, connectivity: np.ndarray, reorderings: Iterable[Iterable[int]]) -> np.ndarray:
        column_order = [
            [0, 1, 2, 3] + [i + 4 for i in reordering]
            for reordering in reorderings
        ]  # fmt: skip

        stacked = []
        for order in column_order:
            connect = connectivity[:, order]
            stacked.append(connect)

        return np.concatenate(stacked)
