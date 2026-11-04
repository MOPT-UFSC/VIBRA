from vtkmodules.vtkCommonDataModel import vtkCellData
from vtkmodules.vtkFiltersCore import vtkPolyDataTangents
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from collections.abc import Iterable

import numpy as np
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkIntArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkPropAssembly

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.utils.interface_utils import SectionPlane


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

    def _configure_actors_parameters(self):
        self.surface_colors.SetName("color")
        self.texture_coords.SetName("tcoords")
        self.surface_ids.SetName("ids")
        self.surface_data.SetPoints(self.points)
        self.surface_data.GetCellData().SetScalars(self.surface_colors)
        self.surface_data.GetCellData().AddArray(self.surface_ids)
        self.surface_mapper.SetInputData(self.surface_data)
        self.surface_actor.SetMapper(self.surface_mapper)
        self.AddPart(self.surface_actor)

    def build_mesh(self):
        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None
        assert self.mesh.faces_connectivity is not None

        self.points.SetData(numpy_to_vtk(self.mesh.nodal_coordinates[:, 1:]))
        self.points.Modified()

        faces_triangulated = self._triangulate_2d_cells(self.mesh.faces_connectivity)
        face_cells = self._create_cells(faces_triangulated[:, 4:])
        self.surface_data.SetPolys(face_cells)
        self.surface_colors.SetNumberOfTuples(len(faces_triangulated))
        self.surface_mapper.Modified()
        self.surface_colors.Fill(255)
        self.surface_ids.SetNumberOfTuples(len(faces_triangulated))
        vtk_to_numpy(self.surface_ids)[:] = faces_triangulated[:, 0]

        add_normals = vtkPolyDataNormals()
        add_normals.SplittingOff()
        add_normals.
        add_normals.SetInputData(self.surface_data)
        add_normals.Update()

        self.surface_data.DeepCopy(add_normals.GetOutput())
        
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
