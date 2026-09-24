from dataclasses import dataclass
from typing import override

import numpy as np
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget
from PySide6.QtGui import QResizeEvent
from vtkmodules.vtkRenderingCore import vtkHardwarePicker

from vibra.engine.model import Model
from vibra.engine.postprocessing.acoustic_postprocessing import AcousticPostprocessing
from vibra.engine.postprocessing.structural_postprocessing import StructuralPostprocessing
from vibra.interface.viewer_3d import plot_setup
from vibra.interface.viewer_3d.actors.mesh_actor import MeshActor, PickedMesh
from vibra.interface.viewer_3d.actors.results_actor import ResultsActor
from vibra.utils.interface_utils import MeshRendererConfig, SectionPlane, VisualizationFilter
from vibra.utils.time_utils import context_timer, function_timer


@dataclass(kw_only=True, frozen=True)
class PostprocessedData3D:
    deformed_coordinates: np.ndarray | None = None
    color_scalars: np.ndarray | None = None
    domain_nodes: np.ndarray | None = None
    min_color: float = 0
    max_color: float = 0


class PreviewRenderWidget(CommonRenderWidget):
    def __init__(self):
        super().__init__()
        self.create_axes()
        self.set_interactor_style(BoxSelectionInteractorStyle())

        self.picker = vtkHardwarePicker()
        self.picker.SetPixelTolerance(0)
        self.picker.SnapToMeshPointOff()

        self.mouse_click = (0, 0)
        self.left_clicked.connect(self.click_start)
        self.left_released.connect(self.click)

        self.postprocessed_data_3d: PostprocessedData3D | None = None
        self.hide_out_of_range: bool = False
        self.colormap: str = "viridis"
        self.user_min_color: float | None = None
        self.user_max_color: float | None = None
        self.plot_setup = plot_setup.NoPlotSetup()

        self.model: Model | None = None
        self.section_plane: SectionPlane | None = None
        self.mesh_config = MeshRendererConfig()
        self.visualization_filter = VisualizationFilter().all_true()
        self.picked_mesh = PickedMesh()
        self.create_actors()

    def create_actors(self):
        self.mesh_actor = MeshActor(self.model)
        # self.add_actors(self.mesh_actor)

        self.results_actor = ResultsActor(self.model)
        self.add_actors(self.results_actor)

    def set_model(self, model: Model | None):
        self.model = model
        self.mesh_actor.model = model
        self.results_actor.model = model

    def set_section_plane(self, section_plane: SectionPlane | None):
        self.section_plane = section_plane
        self.mesh_actor.section_plane = section_plane
        self.results_actor.section_plane = section_plane

    def set_visualization_filter(self, visualization_filter: VisualizationFilter | None):
        if visualization_filter is None:
            visualization_filter = VisualizationFilter(faces=True, symbols=True)
        self.visualization_filter = visualization_filter

    def set_mesh_render_config(self, config: MeshRendererConfig | None):
        if config is None:
            config = MeshRendererConfig()
        self.mesh_config = config

    def set_plot_setup(self, setup: plot_setup.PlotSetup | None):
        if self.model is None:
            self.postprocessed_data_3d = None
            return

        if setup == self.plot_setup:
            return

        self.plot_setup = setup
        analysis_id = self.model.analysis_id

        match self.plot_setup:
            case plot_setup.NoPlotSetup():
                self.postprocessed_data_3d = None

            case plot_setup.PressureFieldPlotSetupFrequency():
                assert self.model.mesh is not None
                assert self.model.mesh.nodal_coordinates is not None

                postprocessor = AcousticPostprocessing(self.model)
                data = postprocessor.compute_acoustic_pressure_field(
                    self.plot_setup.index,
                    self.plot_setup.phase,
                    self.plot_setup.plot_type,
                    unit_factor=self.plot_setup.unit_factor,
                    is_modal=analysis_id.is_modal(),
                )

                if data is None:
                    return

                color_scalars, min_value, max_value, complex_result = data
                acoustic_nodes = self.model.domains_processor.nodes_of_domain.get("acoustic")

                _color_scalars = np.zeros(len(self.model.mesh.nodal_coordinates), dtype=float)
                _color_scalars[acoustic_nodes] = color_scalars
                self.postprocessed_data_3d = PostprocessedData3D(
                    color_scalars=_color_scalars,
                    domain_nodes=acoustic_nodes,
                    min_color=min_value,
                    max_color=max_value,
                )

            case plot_setup.DisplacementFieldPlotSetupFrequency():
                assert self.model.mesh is not None
                assert self.model.mesh.nodal_coordinates is not None

                postprocessor = StructuralPostprocessing(self.model)
                data = postprocessor.compute_structural_response_field(
                    self.plot_setup.index,
                    self.plot_setup.phase,
                    self.plot_setup.plot_type,
                    n_diff=self.plot_setup.n_diff,
                    unit_factor=self.plot_setup.unit_factor,
                    is_modal=analysis_id.is_modal(),
                )

                if data is None:
                    return

                displacements, color_scalars, min_value, max_value, complex_result = data
                structural_nodes = self.model.domains_processor.nodes_of_domain.get("structural")
                deformed_coords = self.model.mesh.nodal_coordinates[:, 1:].copy()
                deformed_coords[structural_nodes, :] += (self.plot_setup.magnification_factor / (10 * max_value)) * displacements
                _color_scalars = np.zeros(len(self.model.mesh.nodal_coordinates), dtype=float)
                _color_scalars[structural_nodes] = color_scalars
                self.postprocessed_data_3d = PostprocessedData3D(
                    deformed_coordinates=deformed_coords,
                    color_scalars=_color_scalars,
                    domain_nodes=structural_nodes,
                    min_color=min_value,
                    max_color=max_value,
                )

            case _:
                raise NotImplementedError(f'Plot setup "{self.plot_setup}" not implemented.')

    @function_timer
    @override
    def update_plot(self, reset_camera: bool = False):
        self.mesh_actor.update()
        self.results_actor.update()

        self.update_visualization()

        if reset_camera:
            self.picked_mesh.clear()
            self.renderer.ResetCamera()

        with context_timer("render"):
            self.update()

    @function_timer
    def update_visualization(self):
        self.renderer.SetBackground(self.mesh_config.background_bottom.to_rgb_f())
        self.renderer.SetBackground2(self.mesh_config.background_top.to_rgb_f())

        self.mesh_actor.set_node_color(self.mesh_config.nodes_color)
        self.mesh_actor.set_edge_color(self.mesh_config.edges_color)
        self.mesh_actor.set_surface_color(self.mesh_config.surfaces_color)
        self.mesh_actor.set_volume_color(self.mesh_config.volumes_color)
        self.mesh_actor.set_nodes_size(self.mesh_config.nodes_size)
        self.mesh_actor.set_edge_width(self.mesh_config.edges_thickness)
        self.mesh_actor.set_nodes_visibility(visible=self.visualization_filter.points)
        self.mesh_actor.set_edges_visibility(visible=self.visualization_filter.lines)
        self.mesh_actor.set_surfaces_visibility(visible=self.visualization_filter.faces)
        self.mesh_actor.set_solids_visibility(visible=self.visualization_filter.faces)
        self.mesh_actor.paint_nodes(self.mesh_config.selected_nodes_color, self.picked_mesh.picked_nodes)
        self.mesh_actor.paint_face_elements(self.mesh_config.selected_surfaces_color, self.picked_mesh.picked_faces)
        self.mesh_actor.paint_solid_elements(self.mesh_config.selected_volumes_color, self.picked_mesh.picked_solids)
        self.mesh_actor.update_caches()

        self.results_actor.set_node_color(self.mesh_config.nodes_color)
        self.results_actor.set_edge_color(self.mesh_config.edges_color)
        self.results_actor.set_surface_color(self.mesh_config.surfaces_color)
        self.results_actor.set_volume_color(self.mesh_config.volumes_color)
        self.results_actor.set_nodes_size(self.mesh_config.nodes_size)
        self.results_actor.set_edge_width(self.mesh_config.edges_thickness)
        self.results_actor.set_nodes_visibility(visible=self.visualization_filter.points)
        self.results_actor.set_edges_visibility(visible=self.visualization_filter.lines)
        self.results_actor.set_surfaces_visibility(visible=self.visualization_filter.faces)
        self.results_actor.set_solids_visibility(visible=self.visualization_filter.faces)
        self.results_actor.paint_nodes(self.mesh_config.selected_nodes_color, self.picked_mesh.picked_nodes)
        self.results_actor.paint_face_elements(self.mesh_config.selected_surfaces_color, self.picked_mesh.picked_faces)
        self.results_actor.paint_solid_elements(self.mesh_config.selected_volumes_color, self.picked_mesh.picked_solids)

        pp = self.postprocessed_data_3d

        if (pp is not None) and (pp.deformed_coordinates is not None):
            self.results_actor.set_coordinates(pp.deformed_coordinates)
        else:
            self.results_actor.reset_coordinates()

        if (pp is not None) and (pp.color_scalars is not None):
            self.results_actor.set_color_scalars(
                pp.color_scalars,
                pp.min_color if (self.user_min_color is None) else self.user_min_color,
                pp.max_color if (self.user_min_color is None) else self.user_min_color,
                hide_out_of_range=self.hide_out_of_range,
                colormap=self.colormap,
            )
        else:
            self.results_actor.reset_color_scalars()

        if (pp is not None) and (pp.domain_nodes is not None):
            self.results_actor.hide_results()
            self.results_actor.show_results(pp.domain_nodes)  # pyright: ignore[reportArgumentType]
        else:
            self.results_actor.show_results()

        self.results_actor.update_caches()

    @override
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.renderer.ResetCamera()

    def click_start(self, x: int, y: int):
        self.mouse_click = (x, y)

    @function_timer
    def click(self, x1: int, y1: int):
        x0, y0 = self.mouse_click
        dist = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

        if dist > 10:
            self.picked_mesh = self.results_actor.area_pick(x0, y0, x1, y1, self.renderer)
        else:
            self.picked_mesh = self.results_actor.pick(x1, y1, self.renderer)

        self.update_visualization()
