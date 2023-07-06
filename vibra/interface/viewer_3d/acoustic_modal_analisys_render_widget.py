import numpy as np
from PyQt5.QtCore import QObjectCleanupHandler
from PyQt5.QtWidgets import (
    QAction,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from vibra.interface.viewer_3d.actors.analisys_actor import AnalisysActor
from vibra.interface.viewer_3d.actors.cutting_plane_actor import (
    CuttingPlaneActor,
)
from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget
from vibra.utils.math_functions import bounds_distance, lerp, rotation_matrices


class AcousticModalAnalisysRenderWidget(CommonRenderWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)

        self.project = project
        self.control_bar = self._create_control_bar()

        # replace the layout to add other usefull widgets
        QObjectCleanupHandler().add(self.layout())
        layout = QVBoxLayout()
        layout.addWidget(self.control_bar)
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)

        self.analisys_actor = None
        self.plane_actor = None
        self.bounds = (0, 0, 0, 0, 0, 0)

        self.create_axes()
        self.create_color_bar()
        self.update_plot()

    def current_shape_index(self):
        return self.frequencies.currentIndex()

    def update_plot(self):
        if self.project is None:
            return

        model = self.project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        solver = self.project.modal_solver
        if solver.modal_shape is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.modal_shape.shape[1]):
            return

        print(f"plot {index}")
        self.remove_actors()
        current_modal_shape = solver.modal_shape[:, index]
        self.analisys_actor = AnalisysActor(mesh)
        self.analisys_actor.plot_colorbar(current_modal_shape)
        self.renderer.AddActor(self.analisys_actor)
        self.colorbar.SetLookupTable(self.analisys_actor.lookup_table)

        self.bounds = self.analisys_actor.GetBounds()
        scale = bounds_distance(self.bounds)
        self.plane_actor = CuttingPlaneActor()
        self.plane_actor.VisibilityOff()
        self.plane_actor.SetScale(scale, scale, scale)
        self.renderer.AddActor(self.plane_actor)

        self.renderer.ResetCamera()
        self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.analisys_actor)
        self.renderer.RemoveActor(self.plane_actor)
        self.analisys_actor = None
        self.plane_actor = None

    def _create_control_bar(self):
        # TODO: Implement this in a isolated widget
        if self.project is None:
            return

        solver = self.project.modal_solver
        if solver.natural_frequencies is None:
            return

        control_bar = QWidget()
        layout = QHBoxLayout()
        self.frequencies = QComboBox()
        self.frequencies.activated.connect(self.update_plot)

        for i in solver.natural_frequencies:
            self.frequencies.addItem(f"{i} Hz")

        layout.addWidget(QLabel("Hola que tal"))
        layout.addWidget(self.frequencies)
        control_bar.setLayout(layout)
        return control_bar

    def _actors_exists(self):
        actors = [
            self.analisys_actor,
            self.plane_actor,
        ]

        return all([actor is not None for actor in actors])

    def _calculate_normal_vector(self, orientation):
        # https://forum.gamemaker.io/index.php?threads/solved-3d-rotations-with-a-shader-matrix-or-a-matrix-glsl-es.61064/

        orientation = np.array(orientation) * np.pi / 180
        rx, ry, rz = rotation_matrices(*orientation)

        normal = rz @ rx @ ry @ np.array([1, 0, 0, 1])
        return normal[:3]
