import numpy as np
from molde.colors.color import Color
from molde.render_widgets import CommonRenderWidget
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonDataModel import vtkSelectionNode
from vtkmodules.vtkRenderingCore import vtkHardwarePicker, vtkHardwareSelector

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
                Color(255, 0, 0),
                0.5,
            )
        self.add_actors(self.symbols)

    def update_model(self, model: Model | None):
        self.model = model
        self.mesh_actor.model = model

    def update_section_plane(self, section_plane: SectionPlaneConfig | None):
        self.section_plane = section_plane
        self.mesh_actor.section_plane = section_plane

    @function_timer
    def update_plot(self):
        self.mesh_actor.update()
        self.symbols.build()

        self.renderer.ResetCamera()
        with context_timer("render"):
            self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.renderer.ResetCamera()

    def click(self, x, y):
        return
        self.picker.Pick(x, y, 0, self.renderer)

        actor = self.picker.GetActor()
        cell_id = self.picker.GetCellId()

        if cell_id < 0:
            print("no cell")
            return

        match actor:
            case self.mesh_actor.surface_actor:
                tag = self.mesh_actor.mesh.faces_connectivity[cell_id][1]
                self.mesh_actor.set_color(Color(0, 0, 0))
                self.mesh_actor.paint_surfaces(color=Color(255, 0, 0), surfaces=[tag])

            case self.mesh_actor.section_actor:
                print("solid")

            case _:
                return

        self.update()
