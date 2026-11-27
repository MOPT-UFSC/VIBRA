from vibra.utils.time_utils import context_timer
import logging
from dataclasses import dataclass

import numpy as np
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor

from vibra.engine.model import Model
from vibra.engine.postprocessing.acoustic_postprocessing import AcousticPostprocessing
from vibra.engine.postprocessing.structural_postprocessing import StructuralPostprocessing
from vibra.interface.viewer_3d.actors.results_actor import ResultsActor
from vibra.interface.viewer_3d.plot_setup import (
    AllowablePulsationForScrewCompressorsPlotSetup,
    DisplacementFieldPlotSetupFrequency,
    DisplacementFieldPlotSetupTime,
    NoPlotSetup,
    PlotSetup,
    PressureFieldPlotSetupFrequency,
    PressureFieldPlotSetupTime,
    StressFieldPlotSetupFrequency,
    StressFieldPlotSetupTime,
    StressType,
)
from vibra.interface.viewer_3d.render_widgets.vibra_render_widget import VibraRenderWidget
from vibra.utils.interface_utils import SectionPlane
from vibra.utils.time_utils import function_timer

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
class PostprocessedData:
    deformed_coordinates: np.ndarray | None = None
    color_scalars: np.ndarray | None = None
    domain_nodes: np.ndarray | None = None
    min_color: float = 0
    max_color: float = 0


@dataclass(kw_only=True, frozen=True)
class FrameIndex:
    index: int
    total: int


class NewResultsRenderWidget(VibraRenderWidget):
    def __init__(self):
        super().__init__()

        self.postprocessed_data = PostprocessedData()
        self.frames_data: dict[int, PostprocessedData] = {}
        self.plot_setup: PlotSetup = NoPlotSetup()
        self.user_min_color = None
        self.user_max_color = None
        self.opacity = 1

        self.create_actors()

    def create_actors(self):
        self.create_axes()
        self.create_scale_bar()
        self.create_color_bar()

        self.results_actor = ResultsActor(self.model)
        self.add_actors(self.results_actor)

    def set_model(self, model: Model | None):
        super().set_model(model)
        self.results_actor.model = model

    def set_section_plane(self, section_plane: SectionPlane | None):
        super().set_section_plane(section_plane)
        self.results_actor.section_plane = section_plane

    def set_opacity(self, opacity: float):
        self.results_actor.set_opacity(opacity)
        self.render()

    @function_timer
    def update_plot(self, reset_camera: bool = False):
        logger.info("Updating the results render... [50/100]")
        if self.isVisible() or reset_camera:
            self._must_update = False
        else:
            self._must_update = True
            return

        logger.info("Updating the results render... [55/100]")
        self.results_actor.update()

        logger.info("Updating the results render... [70/100]")
        self.update_visualization()

        logger.info("Updating the results render... [80/100]")
        if reset_camera:
            self.renderer.ResetCamera()
        logger.info("Updating the results render... [85/100]")

        self.render()

    @function_timer
    def update_visualization(self):
        self.renderer.SetBackground(self.user_preferences.renderer_background_color_1.to_rgb_f())
        self.renderer.SetBackground2(self.user_preferences.renderer_background_color_2.to_rgb_f())

        self.results_actor.set_nodes_visibility(visible=self.visualization_filter.points)
        self.results_actor.set_edges_visibility(visible=self.visualization_filter.lines)
        self.results_actor.set_surfaces_visibility(visible=self.visualization_filter.faces)
        self.results_actor.set_solids_visibility(visible=self.visualization_filter.faces)

        self.results_actor.set_nodes_size(self.user_preferences.nodes_size)
        self.results_actor.set_nodes_size(self.user_preferences.nodes_size)

        if (self.entity_visibility_handler is not None) and self.entity_visibility_handler.has_hidden_entity():
            # This is terribly slow =(
            visible_nodes = self.entity_visibility_handler.get_visible_nodes()
            self.results_actor.hide_results()
            self.results_actor.show_results(list(visible_nodes))
        else:
            self.results_actor.show_results()

        pp = self.postprocessed_data
        self.results_actor.show_results_mode()

        if pp.deformed_coordinates is None:
            self.results_actor.reset_coordinates()
        else:
            self.results_actor.set_coordinates(pp.deformed_coordinates)

        if pp.color_scalars is None:
            self.results_actor.reset_color_scalars()
            self.colorbar_actor.VisibilityOff()
        else:
            min_color = pp.min_color
            if self.user_min_color:
                min_color = self.user_min_color

            max_color = pp.max_color
            if self.user_max_color is not None:
                max_color = self.user_max_color

            color_table = self.results_actor.set_color_scalars(
                pp.color_scalars,
                min_color,
                max_color,
                colormap=self.user_preferences.color_map,
            )
            self.colorbar_actor.SetLookupTable(color_table)
            self.colorbar_actor.VisibilityOn()

        self.results_actor.update_caches()
        self.render()

    def set_plot_setup(self, plot_setup: PlotSetup | None):
        self.clear_cache()

        if (plot_setup is None) or isinstance(plot_setup, NoPlotSetup):
            self.plot_setup = NoPlotSetup()
        else:
            assert isinstance(plot_setup, PlotSetup)
            self.plot_setup = plot_setup

        self.postprocessed_data = self._get_postprocessed_data()

    def show_frame(self, frame: int):
        data = self.frames_data.get(frame)
        if data is None:
            return

        self.results_actor.show_results_mode()

        if data.deformed_coordinates is None:
            self.results_actor.reset_coordinates()
        else:
            self.results_actor.set_coordinates(data.deformed_coordinates)

        if data.color_scalars is None:
            self.results_actor.reset_color_scalars()
            self.colorbar_actor.VisibilityOff()
        else:
            min_color = data.min_color
            if self.user_min_color:
                min_color = self.user_min_color

            max_color = data.max_color
            if self.user_max_color is not None:
                max_color = self.user_max_color

            color_table = self.results_actor.set_color_scalars(
                data.color_scalars,
                min_color,
                max_color,
                colormap=self.user_preferences.color_map,
            )
            self.colorbar_actor.SetLookupTable(color_table)
            self.colorbar_actor.VisibilityOn()

        self.results_actor.update_caches()
        with context_timer("render"):
            self.render()

    def clear_cache(self):
        self.frames_data.clear()

    def cache_frames(self, total_frames: int):
        for frame in range(total_frames):
            if frame in self.frames_data:
                continue
            data = self._get_postprocessed_data(frame, total_frames)
            self.frames_data[frame] = data

    def _get_postprocessed_data(self, frame: int | None = None, total_frames: int | None = None):
        phase = None
        if (frame is not None) and (total_frames is not None):
            phase = frame / total_frames * 2 * np.pi

        match self.plot_setup:
            case NoPlotSetup():
                return PostprocessedData()

            case PressureFieldPlotSetupFrequency():
                return self._postprocess_pressure_field_frequency_domain(phase)

            case PressureFieldPlotSetupTime():
                return self._postprocess_pressure_field_time_domain(frame)

            case AllowablePulsationForScrewCompressorsPlotSetup():
                return self._postprocess_allowable_pulsation_for_screw_compressor()

            case DisplacementFieldPlotSetupFrequency():
                return self._postprocess_displacement_field_frequency_domain(phase)

            case DisplacementFieldPlotSetupTime():
                return self._postprocess_displacement_field_time_domain(frame)

            case StressFieldPlotSetupFrequency():
                return self._postprocess_stress_field_frequency_domain(phase)

            case StressFieldPlotSetupTime():
                return self._postprocess_stress_field_time_domain(frame)

            case _:
                raise NotImplementedError(f'Plot setup "{self.plot_setup}" not implemented.')

    def _postprocess_pressure_field_frequency_domain(self, phase: float | None = None):
        logger.info("Postprocessing the pressure field (frequency domain)... [0/100]")
        assert isinstance(self.plot_setup, PressureFieldPlotSetupFrequency)
        assert self.model is not None

        postprocessor = AcousticPostprocessing(self.model)
        analysis_id = self.model.analysis_id
        phase = self.plot_setup.phase if (phase is None) else (phase)
        data = postprocessor.compute_acoustic_pressures_for_3d_plot_frequency(
            self.plot_setup.index,
            phase,
            self.plot_setup.plot_type,
            unit_factor=self.plot_setup.unit_factor,
            is_modal=analysis_id.is_modal(),
        )

        logger.info("Postprocessing the pressure field (frequency domain)... [20/100]")
        if data is None:
            return None

        logger.info("Postprocessing the pressure field (frequency domain)... [40/100]")
        color_scalars, min_value, max_value, _ = data
        acoustic_nodes = self.model.domains_processor.nodes_of_domain.get("acoustic")

        logger.info("Postprocessing the pressure field (frequency domain)... [60/100]")
        _color_scalars = np.zeros(len(self.model.mesh.nodal_coordinates), dtype=float)
        _color_scalars[acoustic_nodes] = color_scalars

        logger.info("Postprocessing the pressure field (frequency domain)... [80/100]")
        return PostprocessedData(
            color_scalars=_color_scalars,
            domain_nodes=acoustic_nodes,
            min_color=min_value,
            max_color=max_value,
        )

    def _postprocess_pressure_field_time_domain(self, time_index: int | None = None):
        logger.info("Postprocessing the pressure field (time domain)... [0/100]")
        assert isinstance(self.plot_setup, PressureFieldPlotSetupTime)
        assert self.model is not None

        postprocessor = AcousticPostprocessing(self.model)

        time_index = self.plot_setup.time_index if (time_index is None) else time_index
        data = postprocessor.compute_acoustic_pressures_for_3d_plot_time(
            time_index,
            self.plot_setup.plot_type,
            unit_factor=self.plot_setup.unit_factor,
            n_div=self.plot_setup.n_div,
            spectral_lines=self.plot_setup.spectral_lines,
            reduced_loop_time=self.plot_setup.reduced_loop_time,
        )

        logger.info("Postprocessing the pressure field (time domain)... [20/100]")
        if data is None:
            return None

        logger.info("Postprocessing the pressure field (time domain)... [40/100]")
        _, color_scalars, min_value, max_value = data
        acoustic_nodes = self.model.domains_processor.nodes_of_domain.get("acoustic")

        logger.info("Postprocessing the pressure field (time domain)... [60/100]")
        _color_scalars = np.zeros(len(self.model.mesh.nodal_coordinates), dtype=float)
        _color_scalars[acoustic_nodes] = color_scalars

        logger.info("Postprocessing the pressure field (time domain)... [80/100]")
        return PostprocessedData(
            color_scalars=_color_scalars,
            domain_nodes=acoustic_nodes,
            min_color=min_value,
            max_color=max_value,
        )

    def _postprocess_allowable_pulsation_for_screw_compressor(self):
        logger.info("Postprocessing the allowable pulsation for screw compressors... [0/100]")
        assert isinstance(self.plot_setup, AllowablePulsationForScrewCompressorsPlotSetup)
        assert self.model is not None

        postprocessor = AcousticPostprocessing(self.model)

        data = postprocessor.compute_allowable_pulsation_field_for_screw_compressor(
            n_div=self.plot_setup.n_div,
            spectral_lines=self.plot_setup.spectral_lines,
        )

        logger.info("Postprocessing the allowable pulsation for screw compressors... [20/100]")
        if data is None:
            return None

        logger.info("Postprocessing the allowable pulsation for screw compressors... [40/100]")
        color_scalars, min_value, max_value = data

        # apply the penalization factor, if necessary
        penalization_factor = self.plot_setup.penalization_factor / 100
        max_value *= 1 - penalization_factor

        logger.info("Postprocessing the allowable pulsation for screw compressors... [60/100]")
        acoustic_nodes = self.model.domains_processor.nodes_of_domain.get("acoustic")

        _color_scalars = np.zeros(len(self.model.mesh.nodal_coordinates), dtype=float)
        _color_scalars[acoustic_nodes] = color_scalars

        logger.info("Postprocessing the allowable pulsation for screw compressors... [80/100]")
        return PostprocessedData(
            color_scalars=_color_scalars,
            domain_nodes=acoustic_nodes,
            min_color=min_value,
            max_color=max_value,
        )

    def _postprocess_displacement_field_frequency_domain(self, phase: float | None = None):
        logger.info("Postprocessing the displacement field (frequency domain)... [0/100]")
        assert isinstance(self.plot_setup, DisplacementFieldPlotSetupFrequency)
        assert self.model is not None

        postprocessor = StructuralPostprocessing(self.model)
        analysis_id = self.model.analysis_id

        phase = self.plot_setup.phase if (phase is None) else phase
        data = postprocessor.compute_displacements_for_3d_plot_frequency(
            self.plot_setup.index,
            phase,
            self.plot_setup.plot_type,
            n_diff=self.plot_setup.n_diff,
            unit_factor=self.plot_setup.unit_factor,
            is_modal=analysis_id.is_modal(),
        )

        logger.info("Postprocessing the displacement field (frequency domain)... [20/100]")
        if data is None:
            return None

        logger.info("Postprocessing the displacement field (frequency domain)... [40/100]")
        displacements, color_scalars, min_value, max_value, _ = data
        structural_nodes = self.model.domains_processor.nodes_of_domain.get("structural")

        deformed_coords = self.model.mesh.nodal_coordinates[:, 1:].copy()
        max_value = max_value if max_value != 0 else 1.0
        magnification_factor = self.plot_setup.magnification_factor
        mult_factor = 1.0 if magnification_factor is None else magnification_factor / (10 * max_value)
        deformed_coords[structural_nodes, :] += mult_factor * displacements

        logger.info("Postprocessing the displacement field (frequency domain)... [60/100]")
        _color_scalars = np.zeros(len(self.model.mesh.nodal_coordinates), dtype=float)
        _color_scalars[structural_nodes] = color_scalars

        logger.info("Postprocessing the displacement field (frequency domain)... [80/100]")
        return PostprocessedData(
            deformed_coordinates=deformed_coords,
            color_scalars=_color_scalars,
            domain_nodes=structural_nodes,
            min_color=min_value,
            max_color=max_value,
        )

    def _postprocess_displacement_field_time_domain(self, time_index: int | None = None):
        logger.info("Postprocessing the displacement field (time domain)... [0/100]")
        assert isinstance(self.plot_setup, DisplacementFieldPlotSetupTime)
        assert self.model is not None

        postprocessor = StructuralPostprocessing(self.model)

        time_index = self.plot_setup.time_index if (time_index is None) else time_index
        data = postprocessor.compute_displacements_for_3d_plot_time(
            time_index,
            self.plot_setup.plot_type,
            unit_factor=self.plot_setup.unit_factor,
            n_diff=self.plot_setup.n_diff,
            n_div=self.plot_setup.n_div,
            spectral_lines=self.plot_setup.spectral_lines,
            reduced_loop_time=self.plot_setup.reduced_loop_time,
        )

        logger.info("Postprocessing the displacement field (time domain)... [20/100]")
        if data is None:
            return None

        logger.info("Postprocessing the displacement field (time domain)... [40/100]")
        _, displacements, color_scalars, min_value, max_value = data
        structural_nodes = self.model.domains_processor.nodes_of_domain.get("structural")

        deformed_coords = self.model.mesh.nodal_coordinates[:, 1:].copy()
        max_value = max_value if max_value != 0 else 1.0
        magnification_factor = self.plot_setup.magnification_factor
        mult_factor = 1.0 if magnification_factor is None else magnification_factor / (10 * max_value)
        deformed_coords[structural_nodes, :] += mult_factor * displacements

        logger.info("Postprocessing the displacement field (time domain)... [60/100]")
        _color_scalars = np.zeros(len(self.model.mesh.nodal_coordinates), dtype=float)
        _color_scalars[structural_nodes] = color_scalars

        logger.info("Postprocessing the displacement field (time domain)... [80/100]")
        return PostprocessedData(
            deformed_coordinates=deformed_coords,
            color_scalars=_color_scalars,
            domain_nodes=structural_nodes,
            min_color=min_value,
            max_color=max_value,
        )

    def _postprocess_stress_field_frequency_domain(self, phase: float | None = None):
        logger.info("Postprocessing the stress field (frequency domain)... [0/100]")
        assert isinstance(self.plot_setup, StressFieldPlotSetupFrequency)
        assert self.model is not None

        postprocessor = StructuralPostprocessing(self.model)
        analysis_id = self.model.analysis_id

        phase = self.plot_setup.phase if (phase is None) else phase
        displacement_data = postprocessor.compute_displacements_for_3d_plot_frequency(
            self.plot_setup.index,
            phase,
            self.plot_setup.plot_type,
            n_diff=self.plot_setup.n_diff,
            is_modal=analysis_id.is_modal(),
            stress_plot=True,
        )

        logger.info("Postprocessing the stress field (frequency domain)... [20/100]")
        if displacement_data is None:
            return None

        logger.info("Postprocessing the stress field (frequency domain)... [40/100]")
        displacements, max_disp = displacement_data

        if StressType(self.plot_setup.stress_type).is_normal_or_shear_stress():
            stress_data = postprocessor.compute_structural_stresses_for_3d_plot_frequency(
                self.plot_setup.index,
                phase,
                self.plot_setup.stress_type,
                self.plot_setup.plot_type,
                unit_factor=self.plot_setup.unit_factor,
            )
        else:
            stress_data = postprocessor.compute_advanced_structural_stresses_for_3d_plot_frequency(
                self.plot_setup.index,
                phase,
                self.plot_setup.stress_type,
                self.plot_setup.plot_type,
                unit_factor=self.plot_setup.unit_factor,
            )

        logger.info("Postprocessing the stress field (frequency domain)... [60/100]")
        if stress_data is None:
            return None

        logger.info("Postprocessing the stress field (frequency domain)... [80/100]")
        color_scalars, min_value, max_value, _ = stress_data
        structural_nodes = self.model.domains_processor.nodes_of_domain.get("structural")

        deformed_coords = self.model.mesh.nodal_coordinates[:, 1:].copy()
        max_disp = max_disp if max_disp != 0 else 1.0
        magnification_factor = self.plot_setup.magnification_factor
        mult_factor = 1.0 if magnification_factor is None else magnification_factor / (10 * max_disp)
        deformed_coords[structural_nodes, :] += mult_factor * displacements

        _color_scalars = np.zeros(len(self.model.mesh.nodal_coordinates), dtype=float)
        _color_scalars[structural_nodes] = color_scalars

        logger.info("Postprocessing the stress field (frequency domain)... [90/100]")
        return PostprocessedData(
            deformed_coordinates=deformed_coords,
            color_scalars=_color_scalars,
            domain_nodes=structural_nodes,
            min_color=min_value,
            max_color=max_value,
        )

    def _postprocess_stress_field_time_domain(self, time_index: int | None = None):
        logger.info("Postprocessing the stress field (time domain)... [0/100]")
        assert isinstance(self.plot_setup, StressFieldPlotSetupTime)
        assert self.model is not None

        postprocessor = StructuralPostprocessing(self.model)

        time_index = self.plot_setup.time_index if (time_index is None) else time_index
        displacement_data = postprocessor.compute_displacements_for_3d_plot_time(
            time_index,
            self.plot_setup.plot_type,
            unit_factor=self.plot_setup.unit_factor,
            n_diff=self.plot_setup.n_diff,
            n_div=self.plot_setup.n_div,
            spectral_lines=self.plot_setup.spectral_lines,
            reduced_loop_time=self.plot_setup.reduced_loop_time,
            stress_plot=True,
        )

        logger.info("Postprocessing the stress field (time domain)... [20/100]")
        if displacement_data is None:
            return None

        logger.info("Postprocessing the stress field (time domain)... [40/100]")
        time_vector, displacements, max_disp = displacement_data

        if StressType(self.plot_setup.stress_type).is_normal_or_shear_stress():
            stress_data = postprocessor.compute_structural_stresses_for_3d_plot_time(
                time_index,
                time_vector,
                self.plot_setup.stress_type,
                self.plot_setup.plot_type,
                unit_factor=self.plot_setup.unit_factor,
                n_div=self.plot_setup.n_div,
                spectral_lines=self.plot_setup.spectral_lines,
            )
        else:
            stress_data = postprocessor.compute_advanced_structural_stresses_for_3d_plot_time(
                time_index,
                self.plot_setup.stress_type,
                self.plot_setup.plot_type,
                unit_factor=self.plot_setup.unit_factor,
                n_div=self.plot_setup.n_div,
                spectral_lines=self.plot_setup.spectral_lines,
            )

        logger.info("Postprocessing the stress field (time domain)... [60/100]")
        if stress_data is None:
            return None

        logger.info("Postprocessing the stress field (time domain)... [80/100]")
        color_scalars, min_value, max_value, _ = stress_data
        structural_nodes = self.model.domains_processor.nodes_of_domain.get("structural")

        deformed_coords = self.model.mesh.nodal_coordinates[:, 1:].copy()
        max_disp = max_disp if max_disp != 0 else 1.0
        magnification_factor = self.plot_setup.magnification_factor
        mult_factor = 1.0 if magnification_factor is None else magnification_factor / (10 * max_disp)
        deformed_coords[structural_nodes, :] += mult_factor * displacements

        _color_scalars = np.zeros(len(self.model.mesh.nodal_coordinates), dtype=float)
        _color_scalars[structural_nodes] = color_scalars

        logger.info("Postprocessing the stress field (time domain)... [90/100]")
        return PostprocessedData(
            deformed_coordinates=deformed_coords,
            color_scalars=_color_scalars,
            domain_nodes=structural_nodes,
            min_color=min_value,
            max_color=max_value,
        )
