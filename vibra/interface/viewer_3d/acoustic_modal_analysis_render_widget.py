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

from vibra.interface.viewer_3d.actors.analysis_actor import AnalysisActor
from vibra.interface.viewer_3d.actors.cutting_plane_actor import (
    CuttingPlaneActor,
)
from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget
from vibra.interface.modal_analysis_bar import ModalanalysisBar
from vibra.utils.math_functions import bounds_distance, rotation_matrices


class AcousticModalanalysisRenderWidget(CommonRenderWidget):
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
        self.setContentsMargins(0, 0, 0, 0)

        self.analysis_actor = None
        self.plane_actor = None
        self.bounds = (0, 0, 0, 0, 0, 0)

        self.create_axes()
        self.create_color_bar()
        self.update_plot()

    def current_shape_index(self):
        return self.control_bar.frequency_box.currentIndex()

    def update_plot(self):
        if self.project is None:
            return

        model = self.project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        solver = self.project.acoustic_modal_solver
        if solver.modal_shape is None:
            return

        # Apenas comentei essa linha pois estava com bug
        # index = 2
        index = self.current_shape_index()
        if not (0 <= index < solver.modal_shape.shape[1]):
            return

        self.update_theme()
        self.remove_actors()

        current_modal_shape = solver.modal_shape[:, index]
        if self.control_bar.absolute_button.isChecked():
            current_modal_shape = np.abs(current_modal_shape)

        self.analysis_actor = AnalysisActor(mesh)
        self.analysis_actor.plot_colorbar(current_modal_shape)
        self.renderer.AddActor(self.analysis_actor)
        self.colorbar.SetLookupTable(self.analysis_actor.lookup_table)

        self.bounds = self.analysis_actor.GetBounds()
        scale = bounds_distance(self.bounds)
        self.plane_actor = CuttingPlaneActor()
        self.plane_actor.VisibilityOff()
        self.plane_actor.SetScale(scale, scale, scale)
        self.renderer.AddActor(self.plane_actor)

        self.renderer.ResetCamera()
        self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.analysis_actor)
        self.renderer.RemoveActor(self.plane_actor)
        self.analysis_actor = None
        self.plane_actor = None

    def _create_control_bar(self):
        # TODO: Implement this in a isolated widget
        # if self.project is None:
        #     return

        solver = self.project.acoustic_modal_solver
        self.natural_frequencies = solver.natural_frequencies
        if self.natural_frequencies is None:
            return

        control_bar = ModalanalysisBar()
        # layout = control_bar.layout()
        # self.frequencies = QComboBox()
        control_bar.mode_box.activated.connect(self.update_plot)
        control_bar.frequency_box.activated.connect(self.update_plot)
        control_bar.real_part_button.clicked.connect(self.update_plot)
        control_bar.absolute_button.clicked.connect(self.update_plot)

        for i, freq in enumerate(self.natural_frequencies):
            # control_bar.mode_box.addItem(f"Mode: {i}")
            control_bar.frequency_box.addItem(f" Mode {i + 1}: {round(freq, 6)} Hz")

        # layout.addWidget(QLabel("Hola que tal"))
        # layout.addWidget(self.frequencies)
        # control_bar.setLayout(layout)
        return control_bar

    def _actors_exists(self):
        actors = [
            self.analysis_actor,
            self.plane_actor,
        ]

        return all([actor is not None for actor in actors])

    def _calculate_normal_vector(self, orientation):
        # https://forum.gamemaker.io/index.php?threads/solved-3d-rotations-with-a-shader-matrix-or-a-matrix-glsl-es.61064/

        orientation = np.array(orientation) * np.pi / 180
        rx, ry, rz = rotation_matrices(*orientation)

        normal = rz @ rx @ ry @ np.array([1, 0, 0, 1])
        return normal[:3]
