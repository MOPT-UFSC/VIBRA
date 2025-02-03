import logging
from time import time
from moviepy.editor import ImageSequenceClip
from PIL import Image
from pathlib import Path

import numpy as np
from molde.render_widgets import AnimatedRenderWidget
from PyQt5.QtCore import QObjectCleanupHandler
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog

from vibra import app
# from vibra.interface.modal_analysis_bar import AcousticModalAnalysisBar
from vibra.interface.analysis_bars.acoustic_analysis_bar import (
    AcousticModalAnalysisBar,
)
from vibra.interface.viewer_3d.actors.analysis_actor import AnalysisActor
from vibra.interface.viewer_3d.actors.hollow_analysis_actor import HollowAnalysisActor
from vibra.interface.viewer_3d.actors.section_plane_actor import (
    SectionPlaneActor,
)
from vibra.interface.viewer_3d.actors.edges_actor import EdgesActor
from vibra.interface.viewer_3d.actors.faces_actor import FacesActor
# from vibra.interface.viewer_3d.render_widgets.common_render_widget import (
#     CommonRenderWidget,
# )
from vibra.utils.progress_status import ProgressStatus
from vibra import VIBRA_DIR


class AcousticHarmonicAnalysisRenderWidget(AnimatedRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = app().main_window
        self.control_bar = AcousticModalAnalysisBar()
        self.control_bar.value_changed.connect(self.update_plot)
        self.control_bar.show_mesh_button.stateChanged.connect(self.set_mesh_visibility)
        self.control_bar.phase_slider.valueChanged.connect(self.stop_animation)
        self.control_bar.play_pause_button.clicked.connect(self.toggle_animation)
        self.control_bar.create_video_button.clicked.connect(self.save_video)
        self.main_window.theme_changed.connect(self.set_theme)
        self.main_window.section_plane.value_changed.connect(self.update_section_plane)

        # replace the layout to add other usefull widgets
        QObjectCleanupHandler().add(self.layout())
        layout = QVBoxLayout()
        layout.addWidget(self.control_bar)
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.section_plane_active = False
        self.show_plane_actor = True
        self.section_plane_args = tuple()

        self.analysis_actor = None
        self.edges_actor = None
        self.plane_actor = None
        self.hidden_part_actor = None
        self.bounds = (0, 0, 0, 0, 0, 0)

        self.create_axes()
        self.create_color_bar()
        self.create_scale_bar()
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
        solver = app().project.acoustic_harmonic_solver
        if solver is None:
            return
        self.control_bar.set_frequencies(solver.frequencies)

    def update_plot(self, reset_camera=False):

        if app().project is None:
            return

        model = app().project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        solver = app().project.acoustic_harmonic_solver
        if solver is None:
            return

        if solver.solution is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.solution.shape[1]):
            return
        
        if self.plane_actor is not None:
            self.show_plane_actor = self.plane_actor.GetVisibility()

        self.remove_all_actors()

        phase_deg = self.control_bar.phase_slider.value()
        phi_sld = phase_deg * np.pi / 180

        current_pressures = solver.solution[:, index].copy()
        amplitudes = np.abs(current_pressures)
        phase = np.angle(current_pressures)
        output_pressures = amplitudes * np.cos(phase + phi_sld)

        min_value, max_value = solver.get_max_min_values_of_pressures(index)
        if self.control_bar.absolute_button.isChecked():
            min_value = 0
            output_pressures = np.abs(output_pressures)

        self.analysis_actor = HollowAnalysisActor(mesh)
        self.analysis_actor.plot_color_bar(output_pressures, min_value, max_value)
        self.colorbar_actor.SetLookupTable(self.analysis_actor.color_table)
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

        self.plane_actor = SectionPlaneActor(self.analysis_actor.GetBounds())
        self.plane_actor.VisibilityOff()
        self.renderer.AddActor(self.plane_actor)

        mesh_visibility = self.control_bar.show_mesh_button.isChecked()
        self.set_mesh_visibility(mesh_visibility)

        if self.control_bar.show_mesh_button.isChecked():
            self.analysis_actor.VisibilityOn()
            self.analysis_actor.GetProperty().SetRepresentationToSurface()
            self.edges_actor.VisibilityOn()

        # if self.section_plane_active and self.section_plane_args:
        #     self.start_section_mode()
        #     self.apply_section_plane(*self.section_plane_args)
        #     if not self.show_plane_actor:
        #         self.plane_actor.VisibilityOff()
        #         self.update()
        # else:
        #     self.update()

        if reset_camera:
            self.renderer.ResetCamera()

        self.update_section_plane()

        app().project.thumbnail = self.get_thumbnail()

    def update_hidden_plot(self):
        # in this case the update_plot function is fast enough
        self.update_plot(reset_camera=False)

    def update_animation(self, frame):
        if not self._actors_exists():
            return

        solver = app().project.acoustic_harmonic_solver
        if solver.solution is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.solution.shape[1]):
            return

        t0 = time()

        current_pressures = solver.solution[:, index]
        amplitudes = np.abs(current_pressures)
        phase = np.angle(current_pressures)

        phi = np.linspace(0, 2 * np.pi, self._animation_fps, endpoint=False)
        output_pressures = amplitudes * np.cos(phase + phi[frame])

        min_value, max_value = solver.get_max_min_values_of_pressures(index)
        if self.control_bar.absolute_button.isChecked():
            min_value = 0
            output_pressures = np.abs(output_pressures)

        # dt = time() - t0
        # print(f"Elapsed time to process A: {round(dt, 4)} s")

        # t0 = time()
        self.analysis_actor.plot_color_bar(output_pressures, min_value, max_value)
        # dt = time() - t0
        # print(f"Elapsed time to process B: {round(dt, 4)} s")

        # t0 = time()
        self.colorbar_actor.SetLookupTable(self.analysis_actor.color_table)
        # dt = time() - t0
        # print(f"Elapsed time to process C: {round(dt, 4)} s")

        # t0 = time()
        self.update()
        # dt = time() - t0
        # print(f"Elapsed time to process D: {round(dt, 4)} s")

    def save_video(self):
        file_path, check = QFileDialog.getSaveFileName(
                                                        self,
                                                        "Save As",
                                                        filter = "All Files ();; Video (*.mp4);; GIF (*.gif);;",
                                                    )
        
        if not check:
            return
        
        self.generate_video(file_path)
    
        
    def process_animation_frames(self):
        """This method processes the animation frames for one complete
        animation cycle. The animation controls are frame per cycle
        and the number cycles.

        """

        self.animation_data = dict()

        if not self._actors_exists():
            return

        solver = app().project.acoustic_harmonic_solver
        if solver.solution is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.solution.shape[1]):
            return

        nodal_solution = solver.solution[:, index].copy()
        amplitudes = np.abs(nodal_solution)
        phase = np.angle(nodal_solution)

        deg_angles = np.linspace(0, 360, self._animation_fps, endpoint=False)
        min_value, max_value = solver.get_max_min_values_of_pressures(index)

        if self.control_bar.absolute_button.isChecked():
            min_value = 0
            max_value = np.max(np.abs([min_value, max_value]))

        for step, deg_angle in enumerate(deg_angles):
            phi = deg_angle * np.pi / 180
            output_pressures = amplitudes * np.cos(phase + phi)

            if self.control_bar.absolute_button.isChecked():
                output_pressures = np.abs(output_pressures)

            self.animation_data[deg_angle] = output_pressures

            logging.info(
                "Processing the animation frames..." + ProgressStatus(step, len(deg_angles))
            )

        # self.analysis_actor.plot_color_bar(self.animation_data, min_value, max_value)
        # self.colorbar_actor.SetLookupTable(self.analysis_actor.color_table)
        # self.update()

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

    def update_section_plane(self):
        if not self._actors_exists():
            return

        section_plane = self.main_window.section_plane

        if not section_plane.cutting:
            self._disable_section_plane()
            return

        position = section_plane.get_position()
        rotation = section_plane.get_rotation()
        inverted = section_plane.get_inverted()

        if section_plane.editing:
            self.plane_actor.configure_section_plane(position, rotation)
            self.plane_actor.VisibilityOn()
            self.plane_actor.GetProperty().SetColor(0, 0.333, 0.867)
            self.plane_actor.GetProperty().SetOpacity(0.8)
            self.update()
        else:
            self._apply_section_plane(position, rotation, inverted, section_plane.isVisible())

    def _disable_section_plane(self):
        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.hidden_part_actor.SetVisibility(has_hidden_part)
        self.plane_actor.VisibilityOff()
        self.analysis_actor.disable_cut()
        self.edges_actor.disable_cut()
        self.update()

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True):
        if isinstance(self.analysis_actor, HollowAnalysisActor):
            mesh = app().project.model.mesh
            if mesh is None:
                return

            if mesh.solids_connectivity.size > 0:
                self.remove_actors(self.analysis_actor)
                self.analysis_actor = AnalysisActor(mesh)
                self.add_actors(self.analysis_actor)

        self.plane_actor.configure_section_plane(position, rotation)
        xyz = self.plane_actor.calculate_xyz_position(position)
        normal = self.plane_actor.calculate_normal_vector(rotation)
        if inverted:
            normal = -normal

        self.analysis_actor.apply_cut(xyz, normal)
        self.edges_actor.apply_cut(xyz, normal)

        self.hidden_part_actor.VisibilityOn()
        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.update()

    # def start_section_mode(self):
    #     if not self._actors_exists():
    #         return
    #     self.section_plane_active = True
    #     self.hidden_part_actor.VisibilityOn()
    #     self.update()

    # def stop_section_mode(self):
    #     if not self._actors_exists():
    #         return
    #     self.section_plane_active = False
    #     has_hidden_part = bool(self.main_window.hidden_surfaces)
    #     self.hidden_part_actor.SetVisibility(has_hidden_part)
    #     self.plane_actor.VisibilityOff()
    #     self.analysis_actor.disable_cut()
    #     self.edges_actor.disable_cut()
    #     self.update()

    # def configure_section_plane(self, position, orientation, *args, **kwargs):
    #     if not self._actors_exists():
    #         return

    #     self.plane_actor.configure_section_plane(position, orientation)
    #     self.update()

    # def apply_section_plane(self, position, orientation, invert=False):
    #     if not self._actors_exists():
    #         return

    #     self.section_plane_args = (position, orientation, invert)
    #     xyz = self.plane_actor.calculate_xyz_position(position)
    #     normal = self.plane_actor.calculate_normal_vector(orientation)
    #     if invert:
    #         normal = -normal
    #     self.analysis_actor.apply_cut(xyz, normal)
    #     self.edges_actor.apply_cut(xyz, normal)

    #     self.plane_actor.VisibilityOn()
    #     self.plane_actor.configure_section_plane(position, orientation)
    #     self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
    #     self.plane_actor.GetProperty().SetOpacity(0.2)

    #     self.update()

    def remove_all_actors(self):
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
