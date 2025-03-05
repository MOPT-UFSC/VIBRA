import logging
from time import time
from moviepy.editor import ImageSequenceClip
from PIL import Image
from pathlib import Path

import numpy as np
from molde.render_widgets import AnimatedRenderWidget
from PySide6.QtWidgets import QVBoxLayout, QFileDialog, QWidget

from vibra import app

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
        self.current_widget = None

        self.main_window.section_plane.value_changed.connect(self.update_section_plane)
        
        self.section_plane_active = False
        self.show_plane_actor = True
        self.section_plane_args = tuple()

        self.analysis_actor = None
        self.edges_actor = None
        self.plane_actor = None
        self.hidden_part_actor = None
        self._bounds = (0, 0, 0, 0, 0, 0)

        self.create_axes()
        self.create_color_bar()
        self.create_scale_bar()
        self.update_plot()
    
    def configure_menu_widget(self, widget: QWidget):
        self.current_widget = widget

    def toggle_animation(self, *args, **kwargs):
        if self.playing_animation:
            self.stop_animation()
        else:
            self.start_animation(*args, **kwargs)

    def start_animation(self, *args, **kwargs):
        super().start_animation(*args, **kwargs)
        self.main_window.animation_toolbar.update_animate_button_icons(True)

    def stop_animation(self):
        super().stop_animation()
        self.main_window.animation_toolbar.update_animate_button_icons(False)
    
    def set_theme(self, *args, **kwargs):
        self.update_theme()
    
    def update_theme(self):
        user_preferences = app().config.user_preferences
        bkg_1 = user_preferences.renderer_background_color_1
        bkg_2 = user_preferences.renderer_background_color_2
        font_color = user_preferences.renderer_font_color

        if bkg_1 is None:
            raise ValueError('Missing value "bkg_1"')
        if bkg_2 is None:
            raise ValueError('Missing value "bkg_2"')
        if font_color is None:
            raise ValueError('Missing value "font_color"')

        self.renderer.GradientBackgroundOn()
        self.renderer.SetBackground(bkg_1.to_rgb_f())
        self.renderer.SetBackground2(bkg_2.to_rgb_f())

        if hasattr(self, "text_actor"):
            self.text_actor.GetTextProperty().SetColor(font_color.to_rgb_f())

        if hasattr(self, "colorbar_actor"):
            self.colorbar_actor.GetTitleTextProperty().SetColor(font_color.to_rgb_f())
            self.colorbar_actor.GetLabelTextProperty().SetColor(font_color.to_rgb_f())

        if hasattr(self, "scale_bar_actor"):
            self.scale_bar_actor.GetLegendTitleProperty().SetColor(font_color.to_rgb_f())
            self.scale_bar_actor.GetLegendLabelProperty().SetColor(font_color.to_rgb_f())
    
    def update_scale_bar_visibility(self):
        user_preferences = app().config.user_preferences

        if user_preferences.show_reference_scale_bar:
            self.enable_scale_bar()
        else:
            self.disable_scale_bar()
    
    def enable_scale_bar(self):
        self.scale_bar_actor.VisibilityOn()

    def disable_scale_bar(self):
        self.scale_bar_actor.VisibilityOff()
    
    def update_renderer_font_size(self):
        user_preferences = app().config.user_preferences
        font_size_px = int(user_preferences.renderer_font_size * 4/3)

        info_text_property = self.text_actor.GetTextProperty()
        info_text_property.SetFontSize(font_size_px)

        scale_bar_title_property = self.scale_bar_actor.GetLegendTitleProperty()
        scale_bar_label_property = self.scale_bar_actor.GetLegendLabelProperty()
        scale_bar_title_property.SetFontSize(font_size_px)
        scale_bar_label_property.SetFontSize(font_size_px)
    
        color_bar_title_property = self.colorbar_actor.GetTitleTextProperty()
        color_bar_label_property = self.colorbar_actor.GetLabelTextProperty()
        color_bar_title_property.SetFontSize(font_size_px)
        color_bar_label_property.SetFontSize(font_size_px)

    def current_frequency_index(self):
        if self.current_widget is not None:
            return self.current_widget.current_frequency_index()
        return 0

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
        
        index = self.current_frequency_index()
        if not (0 <= index < solver.solution.shape[1]):
            return
        
        if self.plane_actor is not None:
            self.show_plane_actor = self.plane_actor.GetVisibility()

        self.remove_all_actors()

        output_pressures, min_value, max_value = self.calculate_color_bar_plots()

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

        # mesh_visibility = self.control_bar.show_mesh_button.isChecked()
        # self.set_mesh_visibility(mesh_visibility)

        # if self.control_bar.show_mesh_button.isChecked():
        #     self.analysis_actor.VisibilityOn()
        #     self.analysis_actor.GetProperty().SetRepresentationToSurface()
        #     self.edges_actor.VisibilityOn()

        # if self.section_plane_active and self.section_plane_args:
        #     self.start_section_mode()
        #     self.apply_section_plane(*self.section_plane_args)
        #     if not self.show_plane_actor:
        #         self.plane_actor.VisibilityOff()
        #         self.update()
        # else:
        #     self.update()

        self.update_theme()

        if reset_camera:
            self.renderer.ResetCamera()

        self.update_section_plane()

        app().project.thumbnail = self.get_thumbnail()
    
    def calculate_color_bar_plots(self):
        solver = app().project.acoustic_harmonic_solver
        index = self.current_frequency_index()

        phase_deg = self.main_window.animation_toolbar.phase_slider.value()
        phi_sld = phase_deg * np.pi / 180

        current_pressures = solver.solution[:, index].copy()
        amplitudes = np.abs(current_pressures)
        phase = np.angle(current_pressures)
        output_pressures = amplitudes * np.cos(phase + phi_sld)

        min_value, max_value = solver.get_max_min_values_of_pressures(index)
        if self.current_widget is None or self.current_widget.comboBox_color_scale.currentIndex() == 0:
            min_value = 0
            output_pressures = np.abs(output_pressures)
        
        return output_pressures, min_value, max_value

    def update_hidden_plot(self):
        # in this case the update_plot function is fast enough
        self.update_plot(reset_camera=False)

    def update_animation(self, frame):
        if not self._actors_exists():
            return

        solver = app().project.acoustic_harmonic_solver
        if solver.solution is None:
            return

        index = self.current_frequency_index()
        if not (0 <= index < solver.solution.shape[1]):
            return

        t0 = time()

        logging.info(f"Rendering animation frame [{frame}/{self._animation_total_frames}]" + ProgressStatus(frame, self._animation_total_frames))

        current_pressures = solver.solution[:, index]
        amplitudes = np.abs(current_pressures)
        phase = np.angle(current_pressures)

        phi = np.linspace(0, 2 * np.pi, self._animation_total_frames, endpoint=False)
        output_pressures = amplitudes * np.cos(phase + phi[frame])

        min_value, max_value = solver.get_max_min_values_of_pressures(index)
        if self.current_widget is None or self.current_widget.comboBox_color_scale.currentIndex() == 0:
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

        index = self.current_frequency_index()
        if not (0 <= index < solver.solution.shape[1]):
            return

        nodal_solution = solver.solution[:, index].copy()
        amplitudes = np.abs(nodal_solution)
        phase = np.angle(nodal_solution)

        deg_angles = np.linspace(0, 360, self._animation_fps, endpoint=False)
        min_value, max_value = solver.get_max_min_values_of_pressures(index)

        if self.current_widget is None or self.current_widget.comboBox_color_scale.currentIndex() == 0:
            min_value = 0
            max_value = np.max(np.abs([min_value, max_value]))

        for step, deg_angle in enumerate(deg_angles):
            phi = deg_angle * np.pi / 180
            output_pressures = amplitudes * np.cos(phase + phi)

            if self.current_widget is None or self.current_widget.comboBox_color_scale.currentIndex() == 0:
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
        return
        if not self._actors_exists():
            return

        self.control_bar.show_mesh_button.setChecked(False)
        self.analysis_actor.VisibilityOn()
        self.analysis_actor.GetProperty().SetRepresentationToPoints()
        self.edges_actor.VisibilityOff()
        self.update()

    def show_lines(self):
        return
        if not self._actors_exists():
            return

        self.control_bar.show_mesh_button.setChecked(True)
        self.analysis_actor.VisibilityOn()
        self.analysis_actor.GetProperty().SetRepresentationToSurface()
        self.edges_actor.VisibilityOn()
        self.update()

    def show_faces(self):
        return
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
            show_plane = not section_plane.keep_section_plane
            self._apply_section_plane(position, rotation, inverted, show_plane)

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
                output_pressures, min_value, max_value = self.calculate_color_bar_plots()
                self.analysis_actor.plot_color_bar(output_pressures, min_value, max_value)
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
