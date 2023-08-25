from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from vibra.interface.tabs.mesh_info_bar import MeshInfoBar
from vibra.interface.viewer_3d.actors.edges_actor import EdgesActor
from vibra.interface.viewer_3d.actors.solids_actor import SolidsActor
from vibra.interface.viewer_3d.render_widgets.common_render_widget import (
    CommonRenderWidget,
)
from vibra.utils.interface_functions import get_main_window

SHOW_POINTS = 0
SHOW_LINES = 1
SHOW_FACES = 2


class MeshRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal(list, list, list)

    def __init__(self, project, parent=None):
        super().__init__(parent)

        self.project = project
        self.view_mode = SHOW_FACES

        self.mesh_info = MeshInfoBar()

        # replace the layout to add other usefull widgets
        QObjectCleanupHandler().add(self.layout())
        layout = QVBoxLayout()
        layout.addWidget(self.mesh_info)
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.solids_actor = None
        self.edges_actor = None

        self.create_axes()
        self.update_plot()

    def update_plot(self):
        if self.project is None:
            return

        model = self.project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        self.update_theme()
        self.remove_actors()

        self.solids_actor = SolidsActor(mesh)
        self.renderer.AddActor(self.solids_actor)

        self.edges_actor = EdgesActor(self.solids_actor.data)
        self.edges_actor.GetProperty().SetColor(0, 0, 0)
        self.renderer.AddActor(self.edges_actor)

        self.renderer.ResetCamera()
        self.show_faces()

    #
    def show_points(self):
        self.view_mode = SHOW_POINTS
        self.solids_actor.GetProperty().SetRepresentationToPoints()
        self.solids_actor.VisibilityOn()
        self.edges_actor.VisibilityOff()
        self.update_theme()
        self.update()

    def show_lines(self):
        main_window = get_main_window()
        theme = main_window.user_config.theme
        self.view_mode = SHOW_LINES
        self.solids_actor.VisibilityOff()
        self.edges_actor.VisibilityOn()
        self.update_theme()
        self.update()

    def show_faces(self):
        self.view_mode = SHOW_FACES
        self.solids_actor.GetProperty().SetRepresentationToSurface()
        self.solids_actor.VisibilityOn()
        self.edges_actor.VisibilityOn()
        self.edges_actor.GetProperty().SetColor(0, 0, 0)
        self.update_theme()
        self.update()

    def set_theme(self, theme):
        super().set_theme(theme)

        if not self._actors_exists():
            return

        light_color = (1, 1, 1)
        dark_color = (0, 0, 0)

        # It it is showing faces, the colors are fixed
        # otherwise it should follow the theme
        if self.view_mode == SHOW_FACES:
            self.edges_actor.GetProperty().SetColor(dark_color)
            self.solids_actor.GetProperty().SetColor(light_color)

        elif theme == "light":
            self.edges_actor.GetProperty().SetColor(dark_color)
            self.solids_actor.GetProperty().SetColor(dark_color)

        elif theme == "dark":
            self.edges_actor.GetProperty().SetColor(light_color)
            self.solids_actor.GetProperty().SetColor(light_color)

    #
    def remove_actors(self):
        self.renderer.RemoveActor(self.solids_actor)
        self.renderer.RemoveActor(self.edges_actor)
        self.solids_actor = None
        self.edges_actor = None

    def _actors_exists(self):
        actors = [self.solids_actor, self.edges_actor]
        return all([actor is not None for actor in actors])

    def _get_info_tab(self):
        pass
