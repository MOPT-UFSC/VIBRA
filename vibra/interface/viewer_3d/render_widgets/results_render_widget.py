import logging
from threading import Lock
from time import time

import numpy as np
from molde.render_widgets import AnimatedRenderWidget
from PySide6.QtWidgets import QFileDialog
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPointData

from vibra import ICON_DIR, app
from vibra.engine import AnalysisID
from vibra.engine.postprocessing import AcousticPostprocessing, StructuralPostprocessing
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.plots.general.animation_widget import AnimationWidget
from vibra.interface.viewer_3d.render_tools import RenderTool, SelectionTool
from vibra.utils.interface_utils import VisualizationFilter
from vibra.utils.math_functions import lerp
from vibra.utils.time_utils import warn_delays

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


class ResultsRenderWidget(AnimatedRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        app().main_window.theme_changed.connect(self.update_theme)
        app().main_window.section_plane.value_changed.connect(self.update_section_plane)
        app().main_window.section_plane.value_changed.connect(self.update_color_and_deformation)
        app().main_window.visualization_changed.connect(self.visualization_changed_callback)

        self.visualization_filter = VisualizationFilter(
            faces=True,
            solids=True,
        )

        self._animation_cached_data = dict()
        self._animation_cache_lock = Lock()
        self.min_value = 0
        self.max_value = 0
        self.complex_result = False
        self.frequency_index = None
        self.mode_index = None

        self.set_default_render_tool()
        self.remove_all_actors()
        self.create_logos()
        self.create_axes()
        self.create_color_bar()
        self.create_scale_bar()
        self.update_plot()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_section_plane()

    def create_logos(self):
        if hasattr(self, "vibra_logo"):
            self.renderer.RemoveViewProp(self.vibra_logo)

        path = ICON_DIR / "logo_vibra_comp.png"
        self.vibra_logo = self.create_logo(path)
        self.vibra_logo.SetPosition(0.895, 0.91)
        self.vibra_logo.SetPosition2(0.10, 0.10)

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

    def update_plot(self, reset_camera: bool = False):
        mesh = app().project.model.mesh
        if mesh is None:
            return

        if app().project.solver is None:
            return

        logging.info("Updating the results render... [10/100]")
        self.remove_all_actors()

        logging.info("Updating the results render... [25/100]")
        self.analysis_actor = HollowAnalysisActor(mesh)

        logging.info("Updating the results render... [75/100]")
        self.edges_actor = EdgesActor(
            self.analysis_actor.data,
            visualization_filter=self.visualization_filter,
        )

        logging.info("Updating the results render... [80/100]")
        self.ghost_actor = GhostActor(mesh)

        logging.info("Updating the results render... [85/100]")
        self.plane_actor = SectionPlaneActor(self.analysis_actor.GetBounds())

        # Create empty variables to be used when switching actors
        self._cache_hollow_solids_actor: HollowAnalysisActor | None = self.analysis_actor
        self._cache_full_solids_actor: AnalysisActor | None = None

        self.add_actors(
            self.analysis_actor,
            self.edges_actor,
            self.ghost_actor,
            self.plane_actor,
        )

        visualization = self.visualization_filter
        self.ghost_actor.SetVisibility(visualization.ghost and app().main_window.has_hidden_part())
        self.plane_actor.VisibilityOff()

        logging.info("Updating the results render... [90/100]")
        with self.update_lock:
            self.update_theme()
            self.update_section_plane()
            self.visualization_changed_callback()
            self.update_color_and_deformation()
            self.update_info_text()
            self.update_colorbar_unit()

        if reset_camera:
            self.renderer.ResetCamera()

        logging.info("Updating the results render... [98/100]")
        self.update()

    def enable_scale_bar(self):
        self.scale_bar_actor.VisibilityOn()

    def disable_scale_bar(self):
        self.scale_bar_actor.VisibilityOff()

    def update_hidden_plot(self):
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

                if frame in self._animation_cached_data:
                    continue

                self.cache_frame(frame)

    @warn_delays
    def cache_frame(self, frame):
        t = frame / (self._animation_total_frames - 1)
        phase = lerp(0, 2 * np.pi, t)

        with self.update_lock:
            self.update_color_and_deformation(
                phase=phase,
                clear_cache=False,
            )

        point_data = vtkPointData()
        point_position = vtkPoints()
        point_data.DeepCopy(self.analysis_actor.data.GetPointData())
        point_position.DeepCopy(self.analysis_actor.data.GetPoints())
        self._animation_cached_data[frame] = (
            point_data,
            point_position,
        )
        if not self.complex_result:
            mirrored_frame = self._animation_total_frames - frame - 1
            self._animation_cached_data[mirrored_frame] = self._animation_cached_data[frame]

    def start_animation(self, *args, **kwargs):
        super().start_animation(*args, **kwargs)

    def stop_animation(self, *args, **kwargs):
        animation_widget = app().main_window.results_viewer_widget.get_animation_widget()
        if animation_widget is not None:
            animation_widget.pushButton_animate.setChecked(False)
            animation_widget.update_animate_button_icons(False)
        super().stop_animation(*args, **kwargs)

    def update_animation(self, frame):
        if not self.actors_exists():
            return

        if app().project.model.analysis_id == AnalysisID.NO_ANALYSIS:
            self.stop_animation()
            return

        if self._animation_cache_lock.locked():
            return

        if not self._animation_cached_data:
            LoadingWindow(self.cache_animation_frames).run()

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

    def update_color_and_deformation(self, phase: float = 0.0, clear_cache: bool = True):

        self.unit_label = "--"
        if not self.actors_exists():
            return

        if app().project.model.solution is None:
            return

        if clear_cache:
            self.clear_cache()

        displacements = None
        colormap = app().config.user_preferences.color_map
        analysis_id = app().project.model.analysis_id

        if analysis_id == AnalysisID.NO_ANALYSIS:
            return

        elif analysis_id == AnalysisID.STRUCTURAL_MODAL:
            analysis_widget = app().main_window.results_viewer_widget.plot_structural_modal
            self.mode_index = analysis_widget.current_mode_index()
            displacement_type = analysis_widget.get_plot_type()

            postprocessing = app().project.get_structural_postprocessing()
            if not isinstance(postprocessing, StructuralPostprocessing):
                return

            data = postprocessing.compute_structural_response_field(self.mode_index, phase, displacement_type, is_modal=True)
            if data is None:
                return

            displacements, color_scalars, min_value, max_value, self.complex_result = data
            if clear_cache:
                self.min_value = min_value
                self.max_value = max_value

        elif analysis_id == AnalysisID.STRUCTURAL_HARMONIC:
            analysis_widget = app().main_window.results_viewer_widget.plot_structural_harmonic
            self.frequency_index = analysis_widget.get_selected_frequency_index()
            n_diff = analysis_widget.get_number_of_differentiations()
            data_type = analysis_widget.get_data_type()
            self.unit_label = analysis_widget.get_plot_units()

            postprocessing = app().project.get_structural_postprocessing()
            if not isinstance(postprocessing, StructuralPostprocessing):
                return

            data = postprocessing.compute_structural_response_field(self.frequency_index, phase, data_type, n_diff)
            if data is None:
                return

            displacements, color_scalars, min_value, max_value, self.complex_result = data
            if clear_cache:
                self.min_value = min_value
                self.max_value = max_value

        elif analysis_id == AnalysisID.ACOUSTIC_MODAL:
            analysis_widget = app().main_window.results_viewer_widget.plot_acoustic_modal
            self.mode_index = analysis_widget.current_mode_index()
            plot_type = analysis_widget.get_plot_type()

            postprocessing = app().project.get_acoustic_postprocessing()
            if not isinstance(postprocessing, AcousticPostprocessing):
                return

            data = postprocessing.compute_acoustic_pressure_field(self.mode_index, phase, plot_type, is_modal=True)
            if data is None:
                return

            color_scalars, min_value, max_value, self.complex_result = data
            if clear_cache:
                self.min_value = min_value
                self.max_value = max_value

        elif analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            analysis_widget = app().main_window.results_viewer_widget.plot_acoustic_harmonic
            self.frequency_index = analysis_widget.get_selected_frequency_index()
            plot_type = analysis_widget.get_plot_type()
            self.unit_label = "Pa"

            postprocessing = app().project.get_acoustic_postprocessing()
            if not isinstance(postprocessing, AcousticPostprocessing):
                return

            data = postprocessing.compute_acoustic_pressure_field(self.frequency_index, phase, plot_type)
            if data is None:
                return

            color_scalars, min_value, max_value, self.complex_result = data
            if clear_cache:
                self.min_value = min_value
                self.max_value = max_value

        else:
            raise ValueError(f"Unknown analysis: {analysis_id}")

        if displacements is not None:
            animation_widget = app().main_window.results_viewer_widget.get_animation_widget()
            if isinstance(animation_widget, AnimationWidget):
                animation_widget.update_factor_label(max_value=max_value)
                magnification_factor = animation_widget.magnification_factor
            else:
                magnification_factor = 1

            self.analysis_actor.apply_deformation(displacements, magnification_factor, max_value)
            self.edges_actor.extract_data(self.analysis_actor.data)

        self.analysis_actor.plot_color_bar(color_scalars, min_value, max_value, colormap)
        self.colorbar_actor.SetLookupTable(self.analysis_actor.color_table)
        self.update()

    def visualization_changed_callback(self):
        if not self.actors_exists():
            return

        visualization = self.visualization_filter
        self.edges_actor.SetVisibility(visualization.lines)
        self.analysis_actor.SetVisibility(visualization.faces)
        self.ghost_actor.SetVisibility(visualization.ghost and app().main_window.has_hidden_part())

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

    def switch_to_hollow_actor(self):
        if not isinstance(self.analysis_actor, AnalysisActor):
            return

        mesh = app().project.model.mesh
        if mesh is None:
            return

        if not isinstance(self._cache_hollow_solids_actor, HollowAnalysisActor):
            self._cache_hollow_solids_actor = HollowAnalysisActor(mesh)

        self._cache_full_solids_actor = self.analysis_actor

        self.remove_actors(self.analysis_actor, self.edges_actor)
        self.analysis_actor = self._cache_hollow_solids_actor
        self.edges_actor = EdgesActor(
            self.analysis_actor.data,
            visualization_filter=self.visualization_filter,
        )
        self.update_color_and_deformation()
        self.visualization_changed_callback()
        self.add_actors(self.analysis_actor, self.edges_actor)

    def switch_to_solids_actor(self):
        if not isinstance(self.analysis_actor, HollowAnalysisActor):
            return

        mesh = app().project.model.mesh
        if mesh is None:
            return

        if not mesh.are_there_volumes_in_geometry():
            return

        if not isinstance(self._cache_full_solids_actor, AnalysisActor):
            self._cache_full_solids_actor = AnalysisActor(mesh)

        self._cache_hollow_solids_actor = self.analysis_actor

        self.remove_actors(self.analysis_actor, self.edges_actor)
        self.analysis_actor = self._cache_full_solids_actor
        self.edges_actor = EdgesActor(
            self.analysis_actor.data,
            visualization_filter=self.visualization_filter,
        )
        self.update_color_and_deformation()
        self.visualization_changed_callback()
        self.add_actors(self.analysis_actor, self.edges_actor)

    def update_section_plane(self):
        if not self.actors_exists():
            return

        if not self.isVisible():
            return

        section_plane = app().main_window.section_plane
        self.stop_animation()

        if not section_plane.cutting:
            self._disable_section_plane()
            return

        position = section_plane.get_position()
        rotation = section_plane.get_rotation()
        inverted = section_plane.get_inverted()
        is_mesh_field = section_plane.check_mesh_field_results.isChecked()

        if section_plane.editing:
            self.plane_actor.configure_section_plane(position, rotation)
            self.plane_actor.VisibilityOn()
            self.plane_actor.GetProperty().SetColor(0, 0.333, 0.867)
            self.plane_actor.GetProperty().SetOpacity(0.8)
        else:
            show_plane = not section_plane.keep_section_plane
            LoadingWindow(self._apply_section_plane).run(
                position,
                rotation,
                inverted,
                show_plane,
                is_mesh_field,
            )

        self.update()

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True, is_mesh_field=False):
        logging.info("Switching to solid actor... [50/100]")
        self.switch_to_solids_actor()

        logging.info("Configuring section plane... [60/100]")
        xyz, normal = self.plane_actor.configure_section_plane(position, rotation)
        if inverted:
            normal = -normal

        logging.info("Applying cut... [70/100]")
        visualization = self.visualization_filter
        if is_mesh_field:
            self.analysis_actor.apply_cut(xyz, normal)
            self.edges_actor.VisibilityOn()
            visualization.lines = True
            app().main_window.action_line_view.setChecked(True)
        else:
            self.analysis_actor.apply_cutter(xyz, normal)
            self.edges_actor.VisibilityOff()
            visualization.lines = False
            app().main_window.action_line_view.setChecked(False)

        self.edges_actor.apply_cut(xyz, normal)

        logging.info("Updating visualization... [80/100]")
        self.ghost_actor.SetVisibility(visualization.ghost)
        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)

        logging.info("Updating... [99/100]")
        self.update()

    def _disable_section_plane(self):
        visualization = self.visualization_filter
        self.ghost_actor.SetVisibility(visualization.ghost and app().main_window.has_hidden_part())
        self.plane_actor.VisibilityOff()

        self.analysis_actor.disable_cut()
        self.edges_actor.disable_cut()

        self.switch_to_hollow_actor()
        self.update()

    def update_info_text(self):
        if not app().project.is_there_a_valid_solution():
            return

        text = ""
        analysis_id = app().project.model.analysis_id

        if analysis_id == AnalysisID.NO_ANALYSIS:
            return

        if self.frequency_index is None and self.mode_index is None:
            return

        if AnalysisID(analysis_id).is_harmonic():
            text += analysis_info_text(self.frequency_index + 1)

        if AnalysisID(analysis_id).is_modal():
            text += analysis_info_text(self.mode_index)

        self.set_info_text(text)
        self.update()

    def update_colorbar_unit(self):
        if not hasattr(self, "colorbar_actor"):
            return

        self.colorbar_actor.SetTitle(f"Unit: [{self.unit_label}]")
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

        colorbar_title_property = self.colorbar_actor.GetTitleTextProperty()
        colorbar_label_property = self.colorbar_actor.GetLabelTextProperty()
        colorbar_title_property.SetFontSize(font_size_px)
        colorbar_label_property.SetFontSize(font_size_px)

    def add_render_tool(self, tool_class):
        if tool_class == SelectionTool:
            super().add_render_tool(RenderTool)
        else:
            super().add_render_tool(tool_class)

    def set_default_render_tool(self):
        tool = RenderTool()
        self.set_interactor_style(tool)
        tool.update_mouse_cursor_in_render_widgets(tool.current_cursor)
