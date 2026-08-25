from typing import override

import numpy as np
from molde.colors import Color, color_names
from molde.render_widgets import CommonRenderWidget
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonDataModel import vtkSelectionNode
from vtkmodules.vtkRenderingCore import vtkCellPicker, vtkHardwarePicker, vtkHardwareSelector

from vibra.engine.model import Model
from vibra.interface.viewer_3d import sources
from vibra.interface.viewer_3d.actors.mesh_actor import MeshActor
from vibra.interface.viewer_3d.actors.symbols_actor import SymbolsActor
from vibra.utils.preview_utils import SectionPlaneConfig
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

    def update_model(self, model: Model | None):
        self.model = model
        self.mesh_actor.model = model

    def update_section_plane(self, section_plane: SectionPlaneConfig | None):
        self.section_plane = section_plane
        self.mesh_actor.section_plane = section_plane

    @function_timer
    @override
    def update_plot(self):
        self.mesh_actor.update()
        self.symbols.build()

        self.renderer.ResetCamera()
        with context_timer("render"):
            self.update()

    @override
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.renderer.ResetCamera()

    @function_timer
    def click(self, x, y):
        if (model := self.model) is None:
            return

        if (mesh := model.mesh) is None:
            return

        something_picked = self.picker.Pick(x, y, 0, self.renderer)
        self.mesh_actor.set_color(color_names.WHITE)  # Keep it after the pick

        if not something_picked:
            self.mesh_actor.update_caches()
            self.update()
            return

        match self.mesh_actor.picked_dim_tag(self.picker):
            case 2, tag:
                assert mesh.faces_connectivity is not None
                surface = mesh.faces_connectivity[tag, 1]
                self.mesh_actor.paint_surfaces(Color(0, 0, 255), [surface])

            case 3, tag:
                assert mesh.solids_connectivity is not None
                volume = mesh.solids_connectivity[tag, 1]
                self.mesh_actor.paint_volumes(Color(255, 0, 0), [volume])

            case _:
                pass

        self.mesh_actor.update_caches()
        self.update()
