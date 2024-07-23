import logging
from threading import Lock
from time import time

import numpy as np
from PyQt5.QtCore import QObjectCleanupHandler
from PyQt5.QtWidgets import *

from molde.render_widgets import AnimatedRenderWidget

from vibra.interface.analysis_bars.structural_analysis_bar import (
    StructuralModalAnalysisBar,
)
from vibra.interface.viewer_3d.actors.analysis_actor import AnalysisActor
from vibra.interface.viewer_3d.actors.cutting_plane_actor import (
    CuttingPlaneActor,
)
from vibra.interface.viewer_3d.actors.edges_actor import EdgesActor
from vibra.interface.viewer_3d.actors.faces_actor import FacesActor

# from vibra.interface.viewer_3d.render_widgets.common_render_widget import (
#     CommonRenderWidget,
# )
from vibra.utils.interface_functions import get_main_window
from vibra.utils.math_functions import lerp
from vibra import app


class StructuralModalAnalysisRenderWidget(AnimatedRenderWidget):
    # many parts of this class is shared by AcousticModalAnalysisRenderWidget
    # and probably with other analysis classes, so it may be a good idea to
    # make a superclass that controls all the common stuff.

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = app().main_window
        self.control_bar = StructuralModalAnalysisBar()
        self.control_bar.value_changed.connect(self.update_deformations)
        self.control_bar.show_mesh_button.stateChanged.connect(self.set_mesh_visibility)
        self.control_bar.phase_slider.sliderPressed.connect(self.stop_animation)
        self.control_bar.play_pause_button.clicked.connect(self.toggle_animation)
        self.main_window.theme_changed.connect(self.set_theme)

        # replace the layout to add other usefull widgets
        QObjectCleanupHandler().add(self.layout())
        layout = QVBoxLayout()
        layout.addWidget(self.control_bar)
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.cutting_plane_active = False
        self.cutting_plane_args = tuple()

        self.analysis_actor = None
        self.edges_actor = None
        self.plane_actor = None
        self.hidden_part_actor = None
        self.bounds = (0, 0, 0, 0, 0, 0)

        self.create_axes()
        self.create_color_bar()
        self.update_frequencies()
        self.update_plot()

    def toggle_animation(self, *args, **kwargs):
        if self.playing_animation:
            self.stop_animation()
        else:
            self.start_animation()

    def start_animation(self):
        super().start_animation()
        self.control_bar.use_pause_icon()

    def stop_animation(self):
        super().stop_animation()
        self.control_bar.use_play_icon()

    def current_shape_index(self):
        return self.control_bar.frequency_box.currentIndex()

    def update_frequencies(self):
        solver = self.main_window.project.structural_modal_solver
        if solver is None:
            return
        self.control_bar.set_frequencies(solver.natural_frequencies)

    def update_plot(self, reset_camera=True):
        if self.main_window.project is None:
            return

        model = self.main_window.project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        solver = self.main_window.project.structural_modal_solver
        if solver is None:
            return

        if solver.modal_shape is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.modal_shape.shape[1]):
            return

        self.remove_actors()

        self.analysis_actor = AnalysisActor(mesh)

        self.edges_actor = EdgesActor(self.analysis_actor.data)
        self.edges_actor.GetProperty().SetColor(0, 0, 0)

        # Add a very subtle transparent actor to represent the whole 
        # structure even if part of it is hidden
        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.hidden_part_actor = FacesActor(mesh, allow_hidding=False)
        self.hidden_part_actor.SetVisibility(has_hidden_part)
        self.hidden_part_actor.GetProperty().SetOpacity(0.05)
        self.hidden_part_actor.GetProperty().LightingOff()
        self.hidden_part_actor.PickableOff()
        self.renderer.AddActor(self.hidden_part_actor)

        self.plane_actor = CuttingPlaneActor(self.analysis_actor.GetBounds())
        self.plane_actor.VisibilityOff()

        self.update_deformations()
        self.renderer.AddActor(self.analysis_actor)
        self.renderer.AddActor(self.edges_actor)
        self.renderer.AddActor(self.plane_actor)

        mesh_visibility = self.control_bar.show_mesh_button.isChecked()
        self.set_mesh_visibility(mesh_visibility)

        if self.cutting_plane_active and self.cutting_plane_args:
            self.start_cutting_mode()
            self.apply_cutting_plane(*self.cutting_plane_args)
        else:
            self.update()

        if reset_camera:
            self.renderer.ResetCamera()
        self.main_window.project.thumbnail = self.get_thumbnail()

    def update_hidden_plot(self):
        # in this case the update_plot function is fast enough
        self.update_plot(reset_camera=False)

    def update_deformations(self):
        if not self._actors_exists():
            return

        solver = self.main_window.project.structural_modal_solver
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
        displacements, color_scalars, min_value, max_value = self._calculate_displacements(
            index, phase
        )

        self.analysis_actor.disable_cut()
        self.analysis_actor.apply_deformation(displacements, phase, magnification_factor)
        self.edges_actor.extract_data(self.analysis_actor.data)

        self.analysis_actor.plot_colorbar(color_scalars, min_value, max_value)
        self.colorbar_actor.SetLookupTable(self.analysis_actor.lookup_table)
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
        if not self._actors_exists():
            return

        self.control_bar.show_mesh_button.setChecked(False)
        self.analysis_actor.VisibilityOn()
        self.analysis_actor.GetProperty().SetRepresentationToPoints()
        self.edges_actor.VisibilityOff()
        self.update()

    def show_lines(self):
        if not self._actors_exists():
            return

        self.control_bar.show_mesh_button.setChecked(True)
        self.analysis_actor.VisibilityOn()
        self.analysis_actor.GetProperty().SetRepresentationToSurface()
        self.edges_actor.VisibilityOn()
        self.update()

    def show_faces(self):
        if not self._actors_exists():
            return

        self.control_bar.show_mesh_button.setChecked(False)
        self.analysis_actor.VisibilityOn()
        self.analysis_actor.GetProperty().SetRepresentationToSurface()
        self.edges_actor.VisibilityOff()
        self.update()

    #
    def start_cutting_mode(self):
        if not self._actors_exists():
            return
        self.cutting_plane_active = True
        self.plane_actor.VisibilityOn()
        self.hidden_part_actor.VisibilityOn()

    def stop_cutting_mode(self):
        if not self._actors_exists():
            return
        self.cutting_plane_active = False
        self.plane_actor.VisibilityOff()
        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.hidden_part_actor.SetVisibility(has_hidden_part)
        self.analysis_actor.disable_cut()
        self.edges_actor.disable_cut()
        self.update()

    def configure_cutting_plane(self, position, orientation):
        if not self._actors_exists():
            return

        self.plane_actor.configure_cutting_plane(position, orientation)
        self.update()

    def apply_cutting_plane(self, position, orientation, invert=False):
        if not self._actors_exists():
            return

        self.cutting_plane_args = (position, orientation, invert)
        xyz = self.plane_actor.calculate_x_y_z_position(position)
        normal = self.plane_actor.calculate_normal_vector(orientation)
        if invert:
            normal = -normal
        self.analysis_actor.apply_cut(xyz, normal)
        self.edges_actor.apply_cut(xyz, normal)

        self.plane_actor.VisibilityOn()
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.plane_actor.configure_cutting_plane(position, orientation)

        self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.analysis_actor)
        self.renderer.RemoveActor(self.edges_actor)
        self.renderer.RemoveActor(self.plane_actor)
        self.renderer.RemoveActor(self.hidden_part_actor)
        self.analysis_actor = None
        self.edges_actor = None
        self.plane_actor = None
        self.hidden_part_actor = None

    def update_animation(self, frame):
        if not self._actors_exists():
            return

        solver = self.main_window.project.structural_modal_solver
        if solver.modal_shape is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.modal_shape.shape[1]):
            return

        # Map the frames from 0 to 1
        t = frame / (self._animation_total_frames - 1)
        phase = lerp(0, 360, t)
        displacements, color_scalars, min_value, max_value = self._calculate_displacements(
            index, phase
        )
        magnification_factor = self.control_bar.magnification_factor_slider.value()

        self.analysis_actor.apply_deformation(displacements, phase, magnification_factor)
        self.analysis_actor.plot_colorbar(color_scalars, min_value, max_value)
        # self.edges_actor.extract_data(self.analysis_actor.data)
        self.update()

    def _actors_exists(self):
        actors = [
            self.analysis_actor,
            self.edges_actor,
            self.plane_actor,
        ]

        return all([actor is not None for actor in actors])

    def _calculate_displacements(self, index, phase):
        solver = self.main_window.project.structural_modal_solver
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
