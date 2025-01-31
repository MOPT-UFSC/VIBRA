import logging
from threading import Lock
from time import time

import numpy as np
from molde.render_widgets import AnimatedRenderWidget
from PyQt5.QtCore import QObjectCleanupHandler
from PyQt5.QtWidgets import *

from vibra import app
from vibra.interface.analysis_bars.structural_analysis_bar import (
    StructuralModalAnalysisBar,
)
from ..actors.ghost_actor import GhostActor
from ..actors.analysis_actor import AnalysisActor
from ..actors.hollow_analysis_actor import HollowAnalysisActor
from ..actors.section_plane_actor import SectionPlaneActor
from ..actors.edges_actor import EdgesActor
from ..actors.faces_actor import FacesActor
from vibra.utils.math_functions import lerp
from .common_analysis_render_widget import CommonAnalysisRenderWidget


class StructuralModalAnalysisRenderWidget(CommonAnalysisRenderWidget):
    # Some parts of the common functions are already implemented
    # inside CommonAnalysisRenderWidget, but there are still room
    # for improvement.

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = app().main_window
        self.control_bar = StructuralModalAnalysisBar()
        self.control_bar.value_changed.connect(self.update_color_and_deformation)
        self.control_bar.show_mesh_button.stateChanged.connect(self.set_mesh_visibility)
        self.control_bar.phase_slider.sliderPressed.connect(self.stop_animation)
        self.control_bar.play_pause_button.clicked.connect(self.toggle_animation)
        self.control_bar.create_video_button.clicked.connect(self.export_animation_to_file)
        self.main_window.theme_changed.connect(self.set_theme)
        self.main_window.section_plane.value_changed.connect(self.update_section_plane)

        # replace the layout to add other usefull widgets
        QObjectCleanupHandler().add(self.layout())
        layout = QVBoxLayout()
        layout.addWidget(self.control_bar)
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.show_plane_actor = True
        self.section_plane_active = False
        self.section_plane_args = tuple()

        self.analysis_actor: AnalysisActor | HollowAnalysisActor = None
        self.edges_actor: EdgesActor = None
        self.plane_actor: SectionPlaneActor = None
        self.ghost_actor: GhostActor = None
        self.bounds = (0, 0, 0, 0, 0, 0)

        self.create_axes()
        self.create_color_bar()
        self.create_scale_bar()
        self.update_frequencies()
        self.update_plot()

    def start_animation(self):
        super().start_animation()
        self.control_bar.use_pause_icon()

    def stop_animation(self):
        super().stop_animation()
        self.control_bar.use_play_icon()

    def current_shape_index(self):
        return self.control_bar.frequency_box.currentIndex()

    def update_frequencies(self):
        solver = app().project.structural_modal_solver
        if solver is None:
            return
        self.control_bar.set_frequencies(solver.natural_frequencies)

    def update_plot(self, *args, **kwargs):
        solver = app().project.structural_modal_solver
        if solver is None:
            return

        if solver.modal_shape is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.modal_shape.shape[1]):
            return

        super().update_plot(*args, **kwargs)

    def update_hidden_plot(self):
        self.update_plot(reset_camera=False)

    def update_color_and_deformation(self):
        if not self._actors_exists():
            return

        solver = app().project.structural_modal_solver
        if solver.modal_shape is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.modal_shape.shape[1]):
            return

        # Do not update the deformation directly if an animation is running.
        # This makes the magnification factor work much smothly.
        if self.playing_animation:
            return

        phase = self.control_bar.phase_slider.value()
        magnification_factor = self.control_bar.magnification_factor_slider.value()
        displacements, color_scalars, min_value, max_value = self._calculate_displacements(index, phase)

        self.analysis_actor.apply_deformation(displacements, phase, magnification_factor)
        self.ghost_actor.apply_deformation(displacements, phase, magnification_factor)
        self.edges_actor.extract_data(self.analysis_actor.data)

        self.analysis_actor.plot_color_bar(color_scalars, min_value, max_value)
        self.colorbar_actor.SetLookupTable(self.analysis_actor.color_table)
        self.update()

    def set_mesh_visibility(self, condition):
        if not self._actors_exists():
            return

        if condition:
            self.show_lines()
        else:
            self.show_faces()

    #
    def show_points(self):
        return

    def show_lines(self):
        return

    def show_faces(self):
        return

    def update_animation(self, frame):
        if not self._actors_exists():
            return

        solver = app().project.structural_modal_solver
        if solver.modal_shape is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.modal_shape.shape[1]):
            return

        # Map the frames from 0 to 1
        t = frame / (self._animation_total_frames - 1)
        phase = lerp(0, 360, t)
        displacements, color_scalars, min_value, max_value = self._calculate_displacements(index, phase)
        magnification_factor = self.control_bar.magnification_factor_slider.value()

        self.analysis_actor.apply_deformation(displacements, phase, magnification_factor)
        self.ghost_actor.apply_deformation(displacements, phase, magnification_factor)
        self.analysis_actor.plot_color_bar(color_scalars, min_value, max_value)
        # self.edges_actor.extract_data(self.analysis_actor.data)
        self.update()

    def _calculate_displacements(self, index, phase):
        solver = app().project.structural_modal_solver
        if solver.modal_shape is None:
            return

        current_modal_shape = solver.modal_shape[:, index].reshape(-1, 3).copy()

        if self.control_bar.sum_button.isChecked():
            values_1 = np.linalg.norm(current_modal_shape, axis=1).copy()
            displacements = current_modal_shape.copy()

        elif self.control_bar.response_ux_button.isChecked():
            values_1 = current_modal_shape[:, 0]
            displacements = current_modal_shape * np.array([1.0, 0.0, 0.0])

        elif self.control_bar.response_uy_button.isChecked():
            values_1 = current_modal_shape[:, 1]
            displacements = current_modal_shape * np.array([0.0, 1.0, 0.0])

        elif self.control_bar.response_uz_button.isChecked():
            values_1 = current_modal_shape[:, 2]
            displacements = current_modal_shape * np.array([0.0, 0.0, 1.0])
        #
        max_abs = np.max(np.abs(values_1))
        values_1 /= max_abs
        #
        min_value = round(min(values_1), 1)
        max_value = round(max(values_1), 1)
        #

        if self.control_bar.update_coloring.isChecked():
            mod_values = displacements * np.cos(phase * np.pi / 180)

            if self.control_bar.sum_button.isChecked():
                values_2 = np.linalg.norm(mod_values, axis=1).copy()

            elif self.control_bar.response_ux_button.isChecked():
                values_2 = mod_values[:, 0]

            elif self.control_bar.response_uy_button.isChecked():
                values_2 = mod_values[:, 1]

            elif self.control_bar.response_uz_button.isChecked():
                values_2 = mod_values[:, 2]

            values_2 /= max_abs
            if not self.control_bar.sum_button.isChecked():
                if np.abs(min_value) != np.abs(max_value):
                    min_value = -np.max(np.abs([min_value, max_value]))
                    max_value = np.max(np.abs([min_value, max_value]))
        else:
            values_2 = values_1.copy()

        color_scalars = values_2

        return displacements, color_scalars, min_value, max_value
