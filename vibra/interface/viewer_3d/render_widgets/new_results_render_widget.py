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


class NewResultsRenderWidget(VibraRenderWidget):
    def __init__(self):
        super().__init__()

        self.postprocessed_data = PostprocessedData()
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

        self._update_nodes_appearance()
        self._update_edges_appearance()
        self._update_surfaces_appearance()
        self._update_solids_appearance()

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
        if (plot_setup is None) or isinstance(plot_setup, NoPlotSetup):
            self.plot_setup = NoPlotSetup()
        else:
            assert isinstance(plot_setup, PlotSetup)
            self.plot_setup = plot_setup

        match self.plot_setup:
            case NoPlotSetup():
                self.postprocessed_data = PostprocessedData()

            case PressureFieldPlotSetupFrequency():
                self._postprocess_pressure_field_frequency_domain()

            case PressureFieldPlotSetupTime():
                self._postprocess_pressure_field_time_domain()

            case AllowablePulsationForScrewCompressorsPlotSetup():
                self._postprocess_allowable_pulsation_for_screw_compressor()

            case DisplacementFieldPlotSetupFrequency():
                self._postprocess_displacement_field_frequency_domain()

            case DisplacementFieldPlotSetupTime():
                self._postprocess_displacement_field_time_domain()

            case StressFieldPlotSetupFrequency():
                self._postprocess_stress_field_frequency_domain()

            case StressFieldPlotSetupTime():
                self._postprocess_stress_field_time_domain()

            case _:
                raise NotImplementedError(f'Plot setup "{self.plot_setup}" not implemented.')

    def _postprocess_pressure_field_frequency_domain(self):
        logger.info("Postprocessing the pressure field (frequency domain)... [0/100]")
        assert isinstance(self.plot_setup, PressureFieldPlotSetupFrequency)
        assert self.model is not None

        postprocessor = AcousticPostprocessing(self.model)
        analysis_id = self.model.analysis_id
        data = postprocessor.compute_acoustic_pressures_for_3d_plot_frequency(
            self.plot_setup.index,
            self.plot_setup.phase,
            self.plot_setup.plot_type,
            unit_factor=self.plot_setup.unit_factor,
            is_modal=analysis_id.is_modal(),
        )

        logger.info("Postprocessing the pressure field (frequency domain)... [20/100]")
        if data is None:
            self.postprocessed_data = None
            return

        logger.info("Postprocessing the pressure field (frequency domain)... [40/100]")
        color_scalars, min_value, max_value, _ = data
        acoustic_nodes = self.model.domains_processor.nodes_of_domain.get("acoustic")

        logger.info("Postprocessing the pressure field (frequency domain)... [60/100]")
        _color_scalars = np.zeros(len(self.model.mesh.nodal_coordinates), dtype=float)
        _color_scalars[acoustic_nodes] = color_scalars

        logger.info("Postprocessing the pressure field (frequency domain)... [80/100]")
        self.postprocessed_data = PostprocessedData(
            color_scalars=_color_scalars,
            domain_nodes=acoustic_nodes,
            min_color=min_value,
            max_color=max_value,
        )

        logger.info("Postprocessing the pressure field (frequency domain)... [100/100]")

    def _postprocess_pressure_field_time_domain(self):
        logger.info("Postprocessing the pressure field (time domain)... [0/100]")
        assert isinstance(self.plot_setup, PressureFieldPlotSetupTime)
        assert self.model is not None

        postprocessor = AcousticPostprocessing(self.model)

        data = postprocessor.compute_acoustic_pressures_for_3d_plot_time(
            self.plot_setup.time_index,
            self.plot_setup.plot_type,
            unit_factor=self.plot_setup.unit_factor,
            n_div=self.plot_setup.n_div,
            spectral_lines=self.plot_setup.spectral_lines,
            reduced_loop_time=self.plot_setup.reduced_loop_time,
        )

        logger.info("Postprocessing the pressure field (time domain)... [20/100]")
        if data is None:
            self.postprocessed_data = None
            return

        logger.info("Postprocessing the pressure field (time domain)... [40/100]")
        _, color_scalars, min_value, max_value = data
        acoustic_nodes = self.model.domains_processor.nodes_of_domain.get("acoustic")

        logger.info("Postprocessing the pressure field (time domain)... [60/100]")
        _color_scalars = np.zeros(len(self.model.mesh.nodal_coordinates), dtype=float)
        _color_scalars[acoustic_nodes] = color_scalars

        logger.info("Postprocessing the pressure field (time domain)... [80/100]")
        self.postprocessed_data = PostprocessedData(
            color_scalars=_color_scalars,
            domain_nodes=acoustic_nodes,
            min_color=min_value,
            max_color=max_value,
        )

        logger.info("Postprocessing the pressure field (time domain)... [100/100]")

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
            self.postprocessed_data = None
            return

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
        self.postprocessed_data = PostprocessedData(
            color_scalars=_color_scalars,
            domain_nodes=acoustic_nodes,
            min_color=min_value,
            max_color=max_value,
        )

        logger.info("Postprocessing the allowable pulsation for screw compressors... [100/100]")

    def _postprocess_displacement_field_frequency_domain(self):
        logger.info("Postprocessing the displacement field (frequency domain)... [0/100]")
        assert isinstance(self.plot_setup, DisplacementFieldPlotSetupFrequency)
        assert self.model is not None

        postprocessor = StructuralPostprocessing(self.model)
        analysis_id = self.model.analysis_id

        data = postprocessor.compute_displacements_for_3d_plot_frequency(
            self.plot_setup.index,
            self.plot_setup.phase,
            self.plot_setup.plot_type,
            n_diff=self.plot_setup.n_diff,
            unit_factor=self.plot_setup.unit_factor,
            is_modal=analysis_id.is_modal(),
        )

        logger.info("Postprocessing the displacement field (frequency domain)... [20/100]")
        if data is None:
            self.postprocessed_data = None
            return

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
        self.postprocessed_data = PostprocessedData(
            deformed_coordinates=deformed_coords,
            color_scalars=_color_scalars,
            domain_nodes=structural_nodes,
            min_color=min_value,
            max_color=max_value,
        )

        logger.info("Postprocessing the displacement field (frequency domain)... [100/100]")

    def _postprocess_displacement_field_time_domain(self):
        logger.info("Postprocessing the displacement field (time domain)... [0/100]")
        assert isinstance(self.plot_setup, DisplacementFieldPlotSetupTime)
        assert self.model is not None

        postprocessor = StructuralPostprocessing(self.model)

        data = postprocessor.compute_displacements_for_3d_plot_time(
            self.plot_setup.time_index,
            self.plot_setup.plot_type,
            unit_factor=self.plot_setup.unit_factor,
            n_diff=self.plot_setup.n_diff,
            n_div=self.plot_setup.n_div,
            spectral_lines=self.plot_setup.spectral_lines,
            reduced_loop_time=self.plot_setup.reduced_loop_time,
        )

        logger.info("Postprocessing the displacement field (time domain)... [20/100]")
        if data is None:
            self.postprocessed_data = None
            return

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
        self.postprocessed_data = PostprocessedData(
            deformed_coordinates=deformed_coords,
            color_scalars=_color_scalars,
            domain_nodes=structural_nodes,
            min_color=min_value,
            max_color=max_value,
        )

        logger.info("Postprocessing the displacement field (time domain)... [100/100]")

    def _postprocess_stress_field_frequency_domain(self):
        logger.info("Postprocessing the stress field (frequency domain)... [0/100]")
        assert isinstance(self.plot_setup, StressFieldPlotSetupFrequency)
        assert self.model is not None

        postprocessor = StructuralPostprocessing(self.model)
        analysis_id = self.model.analysis_id

        displacement_data = postprocessor.compute_displacements_for_3d_plot_frequency(
            self.plot_setup.index,
            self.plot_setup.phase,
            self.plot_setup.plot_type,
            n_diff=self.plot_setup.n_diff,
            is_modal=analysis_id.is_modal(),
            stress_plot=True,
        )

        logger.info("Postprocessing the stress field (frequency domain)... [20/100]")
        if displacement_data is None:
            self.postprocessed_data = None
            return

        logger.info("Postprocessing the stress field (frequency domain)... [40/100]")
        displacements, max_disp = displacement_data

        if StressType(self.plot_setup.stress_type).is_normal_or_shear_stress():
            stress_data = postprocessor.compute_structural_stresses_for_3d_plot_frequency(
                self.plot_setup.index,
                self.plot_setup.phase,
                self.plot_setup.stress_type,
                self.plot_setup.plot_type,
                unit_factor=self.plot_setup.unit_factor,
            )
        else:
            stress_data = postprocessor.compute_advanced_structural_stresses_for_3d_plot_frequency(
                self.plot_setup.index,
                self.plot_setup.phase,
                self.plot_setup.stress_type,
                self.plot_setup.plot_type,
                unit_factor=self.plot_setup.unit_factor,
            )

        logger.info("Postprocessing the stress field (frequency domain)... [60/100]")
        if stress_data is None:
            self.postprocessed_data = None
            return

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
        self.postprocessed_data = PostprocessedData(
            deformed_coordinates=deformed_coords,
            color_scalars=_color_scalars,
            domain_nodes=structural_nodes,
            min_color=min_value,
            max_color=max_value,
        )

        logger.info("Postprocessing the stress field (frequency domain)... [100/100]")

    def _postprocess_stress_field_time_domain(self):
        logger.info("Postprocessing the stress field (time domain)... [0/100]")
        assert isinstance(self.plot_setup, StressFieldPlotSetupTime)
        assert self.model is not None

        postprocessor = StructuralPostprocessing(self.model)

        displacement_data = postprocessor.compute_displacements_for_3d_plot_time(
            self.plot_setup.time_index,
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
            self.postprocessed_data = None
            return

        logger.info("Postprocessing the stress field (time domain)... [40/100]")
        time_vector, displacements, max_disp = displacement_data

        if StressType(self.plot_setup.stress_type).is_normal_or_shear_stress():
            stress_data = postprocessor.compute_structural_stresses_for_3d_plot_time(
                self.plot_setup.time_index,
                time_vector,
                self.plot_setup.stress_type,
                self.plot_setup.plot_type,
                unit_factor=self.plot_setup.unit_factor,
                n_div=self.plot_setup.n_div,
                spectral_lines=self.plot_setup.spectral_lines,
            )
        else:
            stress_data = postprocessor.compute_advanced_structural_stresses_for_3d_plot_time(
                self.plot_setup.time_index,
                self.plot_setup.stress_type,
                self.plot_setup.plot_type,
                unit_factor=self.plot_setup.unit_factor,
                n_div=self.plot_setup.n_div,
                spectral_lines=self.plot_setup.spectral_lines,
            )

        logger.info("Postprocessing the stress field (time domain)... [60/100]")
        if stress_data is None:
            self.postprocessed_data = None
            return

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
        self.postprocessed_data = PostprocessedData(
            deformed_coordinates=deformed_coords,
            color_scalars=_color_scalars,
            domain_nodes=structural_nodes,
            min_color=min_value,
            max_color=max_value,
        )

        logger.info("Postprocessing the stress field (time domain)... [100/100]")

    def _update_nodes_appearance(self):
        self.results_actor.set_nodes_visibility(visible=self.visualization_filter.points)
        if not self.visualization_filter.points:
            return

        self.results_actor.set_node_color(self.user_preferences.nodes_points_color)
        self.results_actor.set_nodes_size(self.user_preferences.nodes_size)

    def _update_edges_appearance(self):
        self.results_actor.set_edges_visibility(visible=self.visualization_filter.lines)
        if not self.visualization_filter.lines:
            return

        self.results_actor.set_edge_color(self.user_preferences.edges_color)
        self.results_actor.set_edge_thickness(self.user_preferences.edges_thickness)

    def _update_surfaces_appearance(self):
        self.results_actor.set_surfaces_visibility(visible=self.visualization_filter.faces)
        if not self.visualization_filter.faces:
            return

        self.results_actor.set_surface_color(self.user_preferences.faces_color)

    def _update_solids_appearance(self):
        self.results_actor.set_solids_visibility(visible=self.visualization_filter.faces)
        if not self.visualization_filter.faces:
            return

        self.results_actor.set_volume_color(self.user_preferences.volumes_color)
