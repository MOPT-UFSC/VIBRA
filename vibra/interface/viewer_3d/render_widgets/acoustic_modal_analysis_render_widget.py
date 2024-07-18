import numpy as np
from PyQt5.QtCore import QObjectCleanupHandler
from PyQt5.QtWidgets import *

from molde.render_widgets import AnimatedRenderWidget


# from vibra.interface.modal_analysis_bar import AcousticModalAnalysisBar
from vibra.interface.analysis_bars.acoustic_analysis_bar import (
    AcousticModalAnalysisBar,
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
from vibra.utils.math_functions import bounds_distance, lerp, rotation_matrices
from vibra import app


class AcousticModalAnalysisRenderWidget(AnimatedRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = app().main_window
        self.control_bar = AcousticModalAnalysisBar()

        self.control_bar.value_changed.connect(self.update_deformation)
        self.control_bar.show_mesh_button.stateChanged.connect(self.set_mesh_visibility)
        self.control_bar.phase_slider.valueChanged.connect(self.stop_animation)
        self.control_bar.play_pause_button.clicked.connect(self.toggle_animation)
        self.main_window.theme_changed.connect(self.set_theme)

        # replace the layout to add other usefull widgets
        QObjectCleanupHandler().add(self.layout())
        layout = QVBoxLayout()
        layout.addWidget(self.control_bar)
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

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
        solver = self.main_window.project.acoustic_modal_solver
        if solver is None:
            return
        self.control_bar.set_frequencies(solver.natural_frequencies)

    def update_plot(self, reset_camera=True):
        # Remember of updating the frequencies before running this

        if self.main_window.project is None:
            return

        model = self.main_window.project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        solver = self.main_window.project.acoustic_modal_solver
        if solver is None:
            return

        if solver.modal_shape is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.modal_shape.shape[1]):
            return

        self.remove_actors()

        phase = self.control_bar.phase_slider.value()

        current_modal_shape = solver.modal_shape[:, index].copy()
        if self.control_bar.absolute_button.isChecked():
            current_modal_shape = np.abs(current_modal_shape)
        current_modal_shape /= np.max(np.abs(current_modal_shape))

        min_value = np.min(current_modal_shape)
        max_value = np.max(current_modal_shape)

        if self.control_bar.real_part_button.isChecked():
            if np.abs(min_value) != np.abs(max_value):
                min_value = -np.max(np.abs([min_value, max_value]))
                max_value = np.max(np.abs([min_value, max_value]))

        current_modal_shape *= np.cos(phase * np.pi / 180)
        if self.control_bar.absolute_button.isChecked():
            current_modal_shape = np.abs(current_modal_shape)

        self.analysis_actor = AnalysisActor(mesh)
        self.analysis_actor.plot_colorbar(current_modal_shape, min_value, max_value)
        self.colorbar_actor.SetLookupTable(self.analysis_actor.lookup_table)
        self.renderer.AddActor(self.analysis_actor)

        self.edges_actor = EdgesActor(self.analysis_actor.data)
        self.edges_actor.GetProperty().SetColor(0, 0, 0)
        self.renderer.AddActor(self.edges_actor)

        # Add a very subtle transparent actor to represent the whole 
        # structure even if part of it is hidden
        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.hidden_part_actor = FacesActor(mesh, allow_hidding=False)
        self.hidden_part_actor.SetVisibility(has_hidden_part)
        self.hidden_part_actor.GetProperty().SetOpacity(0.05)
        self.hidden_part_actor.GetProperty().LightingOff()
        self.hidden_part_actor.PickableOff()
        self.renderer.AddActor(self.hidden_part_actor)

        self.bounds = self.analysis_actor.GetBounds()
        scale = bounds_distance(self.bounds)
        self.plane_actor = CuttingPlaneActor(self.analysis_actor.GetBounds())
        self.plane_actor.VisibilityOff()
        self.plane_actor.SetScale(scale, scale, scale)
        self.renderer.AddActor(self.plane_actor)

        mesh_visibility = self.control_bar.show_mesh_button.isChecked()
        self.set_mesh_visibility(mesh_visibility)

        if self.control_bar.show_mesh_button.isChecked():
            self.analysis_actor.VisibilityOn()
            self.analysis_actor.GetProperty().SetRepresentationToSurface()
            self.edges_actor.VisibilityOn()

        if reset_camera:
            self.renderer.ResetCamera()
        self.update()
        self.main_window.project.thumbnail = self.get_thumbnail()

    def update_hidden_plot(self):
        # in this case the update_plot function is fast enough
        self.update_plot()

    def update_deformation(self):
        if not self._actors_exists():
            return

        solver = self.main_window.project.acoustic_modal_solver
        if solver.modal_shape is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.modal_shape.shape[1]):
            return

        phase = self.control_bar.phase_slider.value()
        current_modal_shape = solver.modal_shape[:, index].copy()
        if self.control_bar.absolute_button.isChecked():
            current_modal_shape = np.abs(current_modal_shape)
        current_modal_shape /= np.max(np.abs(current_modal_shape))

        min_value = np.min(current_modal_shape)
        max_value = np.max(current_modal_shape)

        if self.control_bar.real_part_button.isChecked():
            if np.abs(min_value) != np.abs(max_value):
                min_value = -np.max(np.abs([min_value, max_value]))
                max_value = np.max(np.abs([min_value, max_value]))

        current_modal_shape *= np.cos(phase * np.pi / 180)
        if self.control_bar.absolute_button.isChecked():
            current_modal_shape = np.abs(current_modal_shape)

        self.analysis_actor.plot_colorbar(current_modal_shape, min_value, max_value)
        self.colorbar_actor.SetLookupTable(self.analysis_actor.lookup_table)
        self.update()

    def update_animation(self, frame):
        if not self._actors_exists():
            return

        solver = self.main_window.project.acoustic_modal_solver
        if solver.modal_shape is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.modal_shape.shape[1]):
            return

        t = frame / (self._animation_total_frames - 1)
        phase = lerp(0, 360, t)

        current_modal_shape = solver.modal_shape[:, index].copy()
        if self.control_bar.absolute_button.isChecked():
            current_modal_shape = np.abs(current_modal_shape)
        current_modal_shape /= np.max(np.abs(current_modal_shape))

        min_value = np.min(current_modal_shape)
        max_value = np.max(current_modal_shape)

        if self.control_bar.real_part_button.isChecked():
            if np.abs(min_value) != np.abs(max_value):
                min_value = -np.max(np.abs([min_value, max_value]))
                max_value = np.max(np.abs([min_value, max_value]))

        current_modal_shape *= np.cos(phase * np.pi / 180)
        if self.control_bar.absolute_button.isChecked():
            current_modal_shape = np.abs(current_modal_shape)

        self.analysis_actor.plot_colorbar(current_modal_shape, min_value, max_value)
        self.colorbar_actor.SetLookupTable(self.analysis_actor.lookup_table)
        self.update()

    def set_mesh_visibility(self, condition):
        if not self._actors_exists():
            return

        if condition:
            self.show_lines()
        else:
            self.show_faces()

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

    def start_cutting_mode(self):
        if not self._actors_exists():
            return
        self.plane_actor.VisibilityOn()

    def stop_cutting_mode(self):
        if not self._actors_exists():
            return
        self.plane_actor.VisibilityOff()
        self.analysis_actor.disable_cut()

    def configure_cutting_plane(self, position, orientation):
        if not self._actors_exists():
            return

        x = lerp(self.bounds[0], self.bounds[1], position[0] / 100)
        y = lerp(self.bounds[2], self.bounds[3], position[1] / 100)
        z = lerp(self.bounds[4], self.bounds[5], position[2] / 100)
        self.plane_actor.SetPosition(x, y, z)
        self.plane_actor.SetOrientation(orientation)

        self.plane_actor.GetProperty().SetColor(0, 0.333, 0.867)
        self.plane_actor.GetProperty().SetOpacity(0.8)
        self.update()

    def apply_cutting_plane(self, position, orientation, invert=False):
        if not self._actors_exists():
            return

        x = lerp(self.bounds[0], self.bounds[1], position[0] / 100)
        y = lerp(self.bounds[2], self.bounds[3], position[1] / 100)
        z = lerp(self.bounds[4], self.bounds[5], position[2] / 100)
        normal = self._calculate_normal_vector(orientation)
        if invert:
            normal = -normal
        self.analysis_actor.apply_cut((x, y, z), normal)

        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)

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

    def _actors_exists(self):
        actors = [
            self.analysis_actor,
            self.edges_actor,
            self.plane_actor,
        ]

        return all([actor is not None for actor in actors])

    def _calculate_normal_vector(self, orientation):
        # https://forum.gamemaker.io/index.php?threads/solved-3d-rotations-with-a-shader-matrix-or-a-matrix-glsl-es.61064/

        orientation = np.array(orientation) * np.pi / 180
        rx, ry, rz = rotation_matrices(*orientation)

        normal = rz @ rx @ ry @ np.array([1, 0, 0, 1])
        return normal[:3]
