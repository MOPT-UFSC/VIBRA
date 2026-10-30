from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum, auto

import numpy as np
import xxhash
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkDataArray, vtkUnsignedCharArray

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.properties.model_properties import ModelProperties
from vibra.interface.viewer_3d.coloring.color_table import ColorTable
from vibra.utils.interface_utils import SectionPlane
from vibra.utils.time_utils import function_timer

from .mesh_actor import MeshActor


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


class ResultsActor(MeshActor):
    def __init__(self, model: Model | None):
        super().__init__(model)
        self.cached_info = CachedInfo()

    @property
    def properties(self) -> ModelProperties | None:
        if self.model is None:
            return

        return self.model.properties

    def clear_data(self):
        super().clear_data()

        self.cached_info = CachedInfo()
        self.result_colors.SetNumberOfTuples(0)
        self.result_colors.Modified()

    def _create_variables(self):
        super()._create_variables()

        self.visualization_mode = VisualizationMode.SHOW_RESULTS
        self.result_colors = vtkUnsignedCharArray()

    def _configure_actors_parameters(self):
        super()._configure_actors_parameters()

        self.result_colors.SetName("result_color")
        self.result_colors.SetNumberOfComponents(4)

        self.edge_mapper.SetScalarModeToUsePointData()

        self.surface_data.GetPointData().SetScalars(self.result_colors)
        self.surface_mapper.SetScalarModeToUsePointData()

        self.volume_data.GetPointData().SetScalars(self.result_colors)
        self.volume_mapper.SetScalarModeToUsePointData()

    def build_mesh_without_section_plane(self):
        super().build_mesh_without_section_plane()

        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None

        self.result_colors.SetNumberOfTuples(len(self.mesh.nodal_coordinates))
        self.result_colors.Fill(255)

    def build_mesh_with_section_plane(self):
        super().build_mesh_with_section_plane()

        assert self.mesh is not None
        assert self.mesh.nodal_coordinates is not None

        self.result_colors.SetNumberOfTuples(len(self.mesh.nodal_coordinates))
        self.result_colors.Fill(255)

    def update_caches(self):
        super().update_caches()

        result_colors_hash = CachedInfo.array_hash(self.result_colors)
        if result_colors_hash != self.cached_info.result_colors_hash:
            self.cached_info.result_colors_hash = result_colors_hash
            self.result_colors.Modified()

    def show_results_mode(self):
        self.visualization_mode = VisualizationMode.SHOW_RESULTS
        self.node_mapper.SetScalarModeToUsePointData()
        self.edge_mapper.ScalarVisibilityOn()
        self.surface_mapper.SetScalarModeToUsePointData()
        self.volume_mapper.SetScalarModeToUsePointData()

    def show_entities_mode(self):
        self.visualization_mode = VisualizationMode.SHOW_ENTITIES
        self.node_mapper.SetScalarModeToUseCellData()
        self.edge_mapper.ScalarVisibilityOff()
        self.surface_mapper.SetScalarModeToUseCellData()
        self.volume_mapper.SetScalarModeToUseCellData()

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
        colormap="viridis",
    ):
        color_table = ColorTable(values, min_value, max_value, colormap)
        color_table.Build()

        mapped = color_table.MapScalars(numpy_to_vtk(values), 0, -1)
        results_color = vtk_to_numpy(self.result_colors)
        if len(results_color) == len(values):
            results_color[:, :3] = vtk_to_numpy(mapped)[:, :3]

    def reset_color_scalars(self):
        self.result_colors.Fill(255)

    def hide_results(self, nodes: Sequence[int] | None = None):
        if nodes is None:
            vtk_to_numpy(self.result_colors)[:, 3] = 0
        else:
            self._set_results_nodes_visibility(nodes, visible=False)

    def show_results(self, nodes: Sequence[int] | None = None):
        if nodes is None:
            vtk_to_numpy(self.result_colors)[:, 3] = 255
        else:
            self._set_results_nodes_visibility(nodes, visible=True)

    def _set_results_nodes_visibility(self, nodes: Sequence[int], *, visible: bool):
        if self.mesh is None:
            return

        result_colors = vtk_to_numpy(self.result_colors)
        alpha = 255 if visible else 0
        result_colors[nodes, 3] = alpha
