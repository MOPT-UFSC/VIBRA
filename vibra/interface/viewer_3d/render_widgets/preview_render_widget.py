from typing import override

import numpy as np
from molde.colors import color_names
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget
from PySide6.QtGui import QResizeEvent
from vtkmodules.vtkRenderingCore import vtkHardwarePicker

from vibra.engine.model import Model
from vibra.interface.viewer_3d import sources
from vibra.interface.viewer_3d.actors.mesh_actor import MeshActor, PickedMesh
from vibra.interface.viewer_3d.actors.symbols_actor import SymbolsActor
from vibra.utils.interface_utils import MeshRendererConfig, SectionPlane, VisualizationFilter
from vibra.utils.time_utils import context_timer, function_timer


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

        self.model = None
        self.section_plane = None
        self.mesh_config = MeshRendererConfig()
        self.visualization_filter = VisualizationFilter().all_true()
        self.picked_mesh = PickedMesh()
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

    @function_timer
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

        self.mesh_actor.paint_nodes(self.mesh_config.selected_nodes_color, self.picked_mesh.picked_nodes)
        self.mesh_actor.paint_face_elements(self.mesh_config.selected_surfaces_color, self.picked_mesh.picked_faces)
        self.mesh_actor.paint_solid_elements(self.mesh_config.selected_volumes_color, self.picked_mesh.picked_solids)

        self.mesh_actor.update_caches()

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
            self.picked_mesh = self.mesh_actor.area_pick(x0, y0, x1, y1, self.renderer)
        else:
            self.picked_mesh = self.mesh_actor.pick(x1, y1, self.renderer)

        self.update_visualization()
