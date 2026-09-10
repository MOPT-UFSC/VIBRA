from typing import override

import numpy as np
from molde.colors import Color, color_names
from molde.render_widgets import CommonRenderWidget
from PySide6.QtGui import QResizeEvent
from vtkmodules.vtkRenderingCore import vtkHardwarePicker

from vibra.engine.model import Model
from vibra.interface.viewer_3d import sources
from vibra.interface.viewer_3d.actors.mesh_actor import MeshActor
from vibra.interface.viewer_3d.actors.symbols_actor import SymbolsActor
from vibra.utils.interface_utils import MeshRendererConfig, SectionPlane, VisualizationFilter
from vibra.utils.time_utils import context_timer, function_timer


class PreviewRenderWidget(CommonRenderWidget):
    def __init__(self):
        super().__init__()
        self.create_axes()

        self.picker = vtkHardwarePicker()
        self.picker.SetPixelTolerance(0)
        self.picker.SnapToMeshPointOff()

        self.left_released.connect(self.click)

        self.model = None
        self.section_plane = None
        self.mesh_config = MeshRendererConfig()
        self.visualization_filter = VisualizationFilter().all_true()
        self.create_actors()

    def create_actors(self):
        self.mesh_actor = MeshActor(self.model)
        self.add_actors(self.mesh_actor)

        self.symbols = SymbolsActor(self.renderer.GetActiveCamera())
        for i in range(10):
            self.symbols.add_entity(
                sources.create_impedance_source,
                (0, np.cos(i), np.sin(i)),
                (0, 0, 1),
                color_names.BLUE,
                0.5,
            )
        self.symbols.PickableOff()
        self.add_actors(self.symbols)

    def set_model(self, model: Model | None):
        self.model = model
        self.mesh_actor.model = model

    def set_section_plane(self, section_plane: SectionPlane | None):
        self.section_plane = section_plane
        self.mesh_actor.section_plane = section_plane

    def set_visualization_filter(self, visualization_filter: VisualizationFilter | None):
        if visualization_filter is None:
            visualization_filter = VisualizationFilter(faces=True, symbols=True)
        self.visualization_filter = visualization_filter

    @function_timer
    @override
    def update_plot(self, reset_camera: bool = False):
        self.mesh_actor.update()
        self.symbols.build()

        self.update_visualization()

        if reset_camera:
            self.renderer.ResetCamera()

        with context_timer("render"):
            self.update()

    def update_visualization(self):
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

    @override
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.renderer.ResetCamera()

    @function_timer
    def click(self, x, y):
        if (model := self.model) is None:
            return

        if (mesh := model.mesh) is None:
            return

        something_picked = self.picker.Pick(x, y, 0, self.renderer)
        self.update_visualization()  # Keep it after the pick

        if not something_picked:
            self.mesh_actor.update_caches()
            self.update()
            return

        match self.mesh_actor.picked_dim_tag(self.picker):
            case 0, tag:
                self.mesh_actor.paint_nodes(self.mesh_config.selected_nodes_color, [tag])

            case 2, tag:
                assert mesh.faces_connectivity is not None
                surface = mesh.faces_connectivity[tag, 1]
                self.mesh_actor.paint_surfaces(self.mesh_config.selected_surfaces_color, [surface])

            case 3, tag:
                assert mesh.solids_connectivity is not None
                volume = mesh.solids_connectivity[tag, 1]
                self.mesh_actor.paint_volumes(self.mesh_config.selected_volumes_color, [volume])

            case _:
                pass

        self.mesh_actor.update_caches()
        self.update()
