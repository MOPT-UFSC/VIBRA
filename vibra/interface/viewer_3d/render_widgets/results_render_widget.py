import logging
from threading import Lock
from time import time
from typing import Literal

import numpy as np
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import AnimatedRenderWidget
from PySide6.QtWidgets import QFileDialog
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPointData

from vibra import app
from vibra.engine.postprocessing import (
    compute_acoustic_harmonic_field,
    compute_acoustic_modal_field,
    compute_structural_harmonic_field,
    compute_structural_modal_field,
)
from vibra.interface.loading_bar import load_function
from vibra.utils.math_functions import lerp

from ..actors import (
    AnalysisActor,
    EdgesActor,
    GhostActor,
    HollowAnalysisActor,
    SectionPlaneActor,
)
from .model_info_text import (
    analysis_info_text,
)

# Just for type hints
AnalysisType = Literal[
    "",
    "structural_modal",
    "structural_harmonic",
    "acoustic_modal",
    "acoustic_harmonic",
]


class ResultsRenderWidget(AnimatedRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_interactor_style(BoxSelectionInteractorStyle())

        app().main_window.theme_changed.connect(self.update_theme)
        app().main_window.section_plane.value_changed.connect(self.update_section_plane)
        app().main_window.visualization_changed.connect(self.visualization_changed_callback)

        self.current_analysis: AnalysisType = ""
        self._animation_cached_data = dict()
        self._animation_cache_lock = Lock()
        self.min_value = 0
        self.max_value = 0
        self.frequency_index = None
        self.mode_index = None

        self.remove_all_actors()
        self.create_axes()
        self.create_color_bar()
        self.create_scale_bar()
        self.update_plot()

    def configure_analysis(self, analysis: AnalysisType):
        self.current_analysis = analysis

    def update_theme(self):
        user_preferences = app().config.user_preferences
        bkg_1 = user_preferences.renderer_background_color_1
        bkg_2 = user_preferences.renderer_background_color_2
        font_color = user_preferences.renderer_font_color

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

    def update_plot(self, reset_camera=False):
        mesh = app().project.model.mesh
        if mesh is None:
            return

        self.remove_all_actors()

        self.analysis_actor = HollowAnalysisActor(mesh)
        self.edges_actor = EdgesActor(self.analysis_actor.data)
        self.ghost_actor = GhostActor(mesh)
        self.plane_actor = SectionPlaneActor(self.analysis_actor.GetBounds())

        self.add_actors(
            self.analysis_actor,
            self.edges_actor,
            self.ghost_actor,
            self.plane_actor,
        )

        has_hidden_part = bool(app().main_window.hidden_surfaces)
        self.ghost_actor.SetVisibility(has_hidden_part)
        self.plane_actor.VisibilityOff()

        with self.update_lock:
            self.update_theme()
            self.visualization_changed_callback()
            self.update_section_plane()
            self.update_color_and_deformation()

        if reset_camera:
            self.renderer.ResetCamera()
        else:
            self.update()

        if self.isVisible():
            app().project.thumbnail = self.get_thumbnail()

    def update_hidden_plot(self):
        self.update_info_text()
        self.update_colorbar_unit()
        self.update_plot(reset_camera=False)

    def clear_cache(self):
        logging.info("Clearing animation cache")
        with self._animation_cache_lock:
            timestamp = time()
            self.timestamp = timestamp
            self._animation_cached_data.clear()
            self.min_value = 0
            self.max_value = 0
        return timestamp

    def cache_animation_frames(self):
        # Everytime the cache is cleared we store the timestamp
        # to check if the cache is still valid.
        # The only time "timestamp != self.timestamp" is when
        # the cache was cleared from another thread, so we do not
        # need to continue the processing

        timestamp = self.clear_cache()

        for frame in range(self._animation_total_frames):
            logging.info(f"Caching animation frames [{frame}/{self._animation_total_frames}]")

            with self._animation_cache_lock:
                if self.timestamp != timestamp:
                    break
                self.cache_frame(frame)

    def cache_frame(self, frame):
        t = frame / (self._animation_total_frames - 1)
        phase = lerp(0, 2 * np.pi, t)

        with self.update_lock:
            self.update_color_and_deformation(phase, clear_cache=False)

        point_data = vtkPointData()
        point_position = vtkPoints()
        point_data.DeepCopy(self.analysis_actor.data.GetPointData())
        point_position.DeepCopy(self.analysis_actor.data.GetPoints())
        self._animation_cached_data[frame] = (
            point_data,
            point_position,
        )

    def start_animation(self, *args, **kwargs):
        super().start_animation(*args, **kwargs)

    def stop_animation(self, *args, **kwargs):
        app().main_window.animation_toolbar.pushButton_animate.setChecked(False)
        app().main_window.animation_toolbar.update_animate_button_icons(False)
        super().stop_animation(*args, **kwargs)

    def update_animation(self, frame):
        if self.current_analysis == "":
            self.stop_animation()
            return

        if self._animation_cache_lock.locked():
            return

        if not self._animation_cached_data:
            load = load_function(self.cache_animation_frames, app().main_window)
            load()

        if frame in self._animation_cached_data:
            logging.info(f"Rendering animation frame [{frame}/{self._animation_total_frames}]")
            point_data, point_position = self._animation_cached_data[frame]
            self.analysis_actor.data.GetPointData().DeepCopy(point_data)
            self.analysis_actor.data.GetPoints().DeepCopy(point_position)
            self.update()
        else:
            # It will only enter here if something wrong happened
            # in the function that caches the frames
            logging.warning(f"Cache miss on update_animation function for frame {frame}")
            self.cache_frame(frame)

    def update_color_and_deformation(self, phase=None, clear_cache=True):
        if not self.actors_exists():
            return

        if clear_cache:
            self.clear_cache()

        animation_toolbar = app().main_window.animation_toolbar
        magnification_factor = animation_toolbar.magnification_factor_slider.value() / 16

        displacements = None
        colormap = app().config.user_preferences.color_map

        if phase is None:
            phase = np.radians(animation_toolbar.phase_slider.value())

        if self.current_analysis == "":
            return

        elif self.current_analysis == "structural_modal":
            analysis_widget = app().main_window.results_viewer_widget.plot_structural_modal
            self.mode_index = analysis_widget.current_mode_index()
            displacement_type = analysis_widget.get_plot_type()

            data = compute_structural_modal_field(
                app().project.structural_modal_solver,
                self.mode_index,
                phase,
                displacement_type,
            )
            displacements, color_scalars, min_value, max_value = data
            if self.clear_cache:
                self.min_value = min_value
                self.max_value = max_value

        elif self.current_analysis == "structural_harmonic":
            analysis_widget = app().main_window.results_viewer_widget.plot_structural_harmonic
            self.frequency_index = analysis_widget.current_frequency_index()
            displacement_type = analysis_widget.get_plot_type()

            data = compute_structural_harmonic_field(
                app().project.structural_harmonic_solver,
                self.frequency_index,
                phase,
                displacement_type,
            )
            displacements, color_scalars, min_value, max_value = data
            if self.clear_cache:
                self.min_value = min_value
                self.max_value = max_value

        elif self.current_analysis == "acoustic_modal":
            analysis_widget = app().main_window.results_viewer_widget.plot_acoustic_modal
            self.mode_index = analysis_widget.current_mode_index()
            plot_type = analysis_widget.get_plot_type()

            data = compute_acoustic_modal_field(
                app().project.acoustic_modal_solver,
                self.mode_index,
                phase,
                plot_type,
            )
            if data is None:
                return

            color_scalars, min_value, max_value = data
            if self.clear_cache:
                self.min_value = min_value
                self.max_value = max_value

        elif self.current_analysis == "acoustic_harmonic":
            analysis_widget = app().main_window.results_viewer_widget.plot_acoustic_harmonic
            self.frequency_index = analysis_widget.current_frequency_index()
            plot_type = analysis_widget.get_plot_type()

            data = compute_acoustic_harmonic_field(
                app().project.acoustic_harmonic_solver,
                self.frequency_index,
                phase,
                plot_type,
            )
            if data is None:
                return
            color_scalars, min_value, max_value = data
            if self.clear_cache:
                self.min_value = min_value
                self.max_value = max_value

        else:
            raise ValueError(f"Unknown analysis: {self.current_analysis}")

        if displacements is not None:
            self.analysis_actor.apply_deformation(
                displacements,
                magnification_factor,
                max_value,
            )
            self.edges_actor.extract_data(self.analysis_actor.data)

        self.analysis_actor.plot_color_bar(color_scalars, min_value, max_value, colormap)
        self.colorbar_actor.SetLookupTable(self.analysis_actor.color_table)
        self.update()

    def update_section_plane(self):
        if not self.actors_exists():
            return

        section_plane = app().main_window.section_plane

        if not section_plane.cutting:
            has_hidden_part = bool(app().main_window.hidden_surfaces)
            self.ghost_actor.SetVisibility(has_hidden_part)
            self.plane_actor.VisibilityOff()
            self.analysis_actor.disable_cut()
            self.edges_actor.disable_cut()
            self.update()
            return

        position = section_plane.get_position()
        rotation = section_plane.get_rotation()
        inverted = section_plane.get_inverted()

        if section_plane.editing:
            self.plane_actor.configure_section_plane(position, rotation)
            self.plane_actor.VisibilityOn()
            self.plane_actor.GetProperty().SetColor(0, 0.333, 0.867)
            self.plane_actor.GetProperty().SetOpacity(0.8)
        else:
            show_plane = not section_plane.keep_section_plane
            self._apply_section_plane(position, rotation, inverted, show_plane)

        self.update()

    def visualization_changed_callback(self):
        if not self.actors_exists():
            return

        visualization = app().main_window.visualization_filter
        has_hidden_part = bool(app().main_window.hidden_surfaces)

        self.edges_actor.SetVisibility(visualization.lines)
        self.analysis_actor.SetVisibility(visualization.faces)
        self.ghost_actor.SetVisibility(has_hidden_part)

        self.update()

    def export_animation_to_file(self):
        file_path, check = QFileDialog.getSaveFileName(
            self,
            "Save As",
            filter="All Files ();; Video (*.mp4);; GIF (*.gif);;",
        )

        if not check:
            return

        self.save_video(file_path)

    def actors_exists(self):
        return len(self._widget_actors) > 0

    def remove_all_actors(self):
        self.analysis_actor: None | AnalysisActor | HollowAnalysisActor = None
        self.edges_actor: None | EdgesActor = None
        self.ghost_actor: None | GhostActor = None
        self.plane_actor: None | SectionPlaneActor = None
        return super().remove_all_actors()

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True):
        mesh = app().project.model.mesh
        actor_is_hollow = isinstance(self.analysis_actor, HollowAnalysisActor)
        mesh_is_hollow = mesh.solids_connectivity.size <= 0

        self.clear_cache()

        if actor_is_hollow and not mesh_is_hollow:
            self.remove_actors(self.analysis_actor)
            self.analysis_actor = AnalysisActor(mesh)
            self.add_actors(self.analysis_actor)
            self.update_color_and_deformation()

        xyz, normal = self.plane_actor.configure_section_plane(position, rotation)
        if inverted:
            normal = -normal

        self.analysis_actor.apply_cut(xyz, normal)
        self.edges_actor.apply_cut(xyz, normal)
        self.update()

        self.ghost_actor.VisibilityOn()
        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)

    def update_info_text(self):
        text = ""
        if self.current_analysis == "" or (self.frequency_index is None and self.mode_index is None):
            return

        if self.current_analysis in ["structural_harmonic", "acoustic_harmonic"]:
            text += analysis_info_text(self.frequency_index + 1)

        if self.current_analysis in ["structural_modal", "acoustic_modal"]:
            text += analysis_info_text(self.mode_index)

        self.set_info_text(text)
        self.update()

    def update_colorbar_unit(self):
        if self.current_analysis == "":
            return

        unit = {
            "structural_modal": "--",
            "structural_harmonic": "m",
            "acoustic_modal": "--",
            "acoustic_harmonic": "Pa",
        }

        self.colorbar_actor.SetTitle(f"Unit: [{unit[self.current_analysis]}]")
        self.update()

    def update_renderer_font_size(self):
        user_preferences = app().config.user_preferences
        font_size_px = int(user_preferences.renderer_font_size * 4 / 3)

        info_text_property = self.text_actor.GetTextProperty()
        info_text_property.SetFontSize(font_size_px)

        scale_bar_title_property = self.scale_bar_actor.GetLegendTitleProperty()
        scale_bar_label_property = self.scale_bar_actor.GetLegendLabelProperty()
        scale_bar_title_property.SetFontSize(font_size_px)
        scale_bar_label_property.SetFontSize(font_size_px)
