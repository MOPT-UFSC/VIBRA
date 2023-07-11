from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from vibra.interface.viewer_3d.actors.solids_actor import SolidsActor
from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget
from vibra.interface.tabs.mesh_info_bar import MeshInfoBar

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
        self.solids_actor.GetProperty().EdgeVisibilityOn()
        self.renderer.AddActor(self.solids_actor)

        self.renderer.ResetCamera()
        self.show_faces()

    #
    def show_points(self):
        self.solids_actor.GetProperty().SetRepresentationToPoints()
        self.update()

    def show_lines(self):
        self.solids_actor.GetProperty().SetRepresentationToWireframe()
        self.update()

    def show_faces(self):
        self.solids_actor.GetProperty().SetRepresentationToSurface()
        self.update()

    #
    def remove_actors(self):
        self.renderer.RemoveActor(self.solids_actor)
        self.solids_actor = None

    def _actors_exists(self):
        actors = [
            self.solids_actor,
        ]
        return all([actor is not None for actor in actors])
    
    def _get_info_tab(self):
        pass