
from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.general.print_message_input import PrintMessageInput

#
from vibra.interface.model_inputs.acoustic.acoustic_properties_gradient_inputs import AcousticPropertiesGradientInputs
from vibra.interface.model_inputs.acoustic.acoustic_transfer_element_inputs import AcousticTransferElementInputs
from vibra.interface.model_inputs.acoustic.dissipation_models.porous_material_model_inputs import PorousMaterialModelInputs
from vibra.interface.model_inputs.acoustic.dissipation_models.proportional_damping_inputs import ProportionalDampingInput
from vibra.interface.model_inputs.acoustic.dissipation_models.viscous_thermal_loss_model_inputs import ViscousThermalLossModelInputs

#
from vibra.interface.model_inputs.acoustic.excitations.acoustic_pressure_inputs import AcousticPressureInputs
from vibra.interface.model_inputs.acoustic.excitations.compressor_excitation_spectrum_inputs import CompressorExcitationSpectrumInputs
from vibra.interface.model_inputs.acoustic.excitations.compressor_excitation_waveform_inputs import CompressorExcitationWaveformInputs
from vibra.interface.model_inputs.acoustic.excitations.incident_plane_wave_inputs import IncidentPlaneWaveInputs
from vibra.interface.model_inputs.acoustic.excitations.mass_source_inputs import MassSourceInputs
from vibra.interface.model_inputs.acoustic.excitations.reciprocating_compressor_inputs import ReciprocatingCompressorInputs
from vibra.interface.model_inputs.acoustic.excitations.surface_velocity_inputs import SurfaceVelocityInputs
from vibra.interface.model_inputs.acoustic.external_impedances.absorption_surface_inputs import AbsorptionSurfaceInputs
from vibra.interface.model_inputs.acoustic.external_impedances.anechoic_termination_inputs import AnechoicTerminationInputs
from vibra.interface.model_inputs.acoustic.external_impedances.specific_impedance_inputs import SpecificImpedanceInputs
from vibra.interface.model_inputs.acoustic.internal_impedances.perforated_plate_model_inputs import PerforatedPlateModelInputs
from vibra.interface.model_inputs.acoustic.internal_impedances.transfer_impedance_inputs import TransferImpedanceInputs
from vibra.interface.model_inputs.dof_decoupling.degrees_of_freedom_decoupling_inputs import DegreesOfFreedomDecouplingInputs
from vibra.interface.model_inputs.general.element_options_inputs import ElementOptionsInputs
from vibra.interface.model_inputs.fluid.set_fluid_inputs import SetFluidInputs
from vibra.interface.model_inputs.material.set_material_inputs import MaterialInputs
from vibra.interface.model_inputs.general.mesher_setup_inputs import MesherSetupInputs
from vibra.interface.model_inputs.structural.excitations.distributed_loads_inputs import DistributedLoadsInputs
from vibra.interface.model_inputs.structural.excitations.distributed_mass_inputs import DistributedMassInputs

#
from vibra.interface.model_inputs.structural.excitations.dof_prescription_inputs import DofPrescriptionInputs
from vibra.interface.model_inputs.structural.excitations.nodal_loads_inputs import NodalLoadsInputs
from vibra.interface.model_inputs.structural.excitations.normal_pressure_load_inputs import NormalPressureLoadInputs
from vibra.interface.model_inputs.structural.surface_thickness_inputs import SurfaceThicknessInputs
from vibra.interface.plots.acoustic.acoustic_pressure_frf_inputs import AcousticPressureFRFInputs
from vibra.interface.plots.acoustic.acoustic_waves_decomposition_inputs import AcousticWavesDecompositionInputs
from vibra.interface.plots.acoustic.acoustic_impedance_inputs import AcousticImpedanceInputs
from vibra.interface.plots.acoustic.acoustic_mode_shape_inputs import AcousticModeShapeInputs

#
from vibra.interface.plots.acoustic.acoustic_pressure_field_inputs import AcousticPressureFieldInputs
from vibra.interface.plots.acoustic.acoustic_pressure_frequency_response_inputs import AcousticPressureFrequencyResponseInputs
from vibra.interface.plots.acoustic.acoustic_pressure_waveform_2d_plot_inputs import AcousticPressureWaveform2DPlotInputs
from vibra.interface.plots.acoustic.acoustic_pressure_waveform_3d_plot_inputs import AcousticPressureWaveform3DPlotInputs
from vibra.interface.plots.acoustic.allowable_pulsation_3d_plot_for_screw_compressor_inputs import AllowablePulsations3DPlotForScrewCompressorInputs
from vibra.interface.plots.acoustic.acoustic_shaking_forces_inputs import AcousticShakingForcesInputs
from vibra.interface.plots.acoustic.allowable_pulsations_for_reciprocating_compressor import AllowablePulsationsForReciprocatingCompressorInputs
from vibra.interface.plots.acoustic.allowable_pulsations_2d_plot_for_screw_compressor_inputs import AllowablePulsations2DPlotForScrewCompressorInputs
from vibra.interface.plots.acoustic.particle_velocity_inputs import ParticleVelocityInputs

#
from vibra.interface.plots.acoustic.surface_absorption_coefficient_inputs import SurfaceAbsorptionCoefficientInputs
from vibra.interface.plots.acoustic.transmission_loss_inputs import TransmissionLossInputs
from vibra.interface.plots.structural.structural_response_fields_inputs import StructuralResponseFieldsInputs

#
from vibra.interface.plots.structural.structural_frequency_response_inputs import PlotStructuralFrequencyResponseInputs
from vibra.interface.plots.structural.structural_mode_shape_inputs import PlotStructuralModeShapeInputs


class InputUi:
    def __init__(self, parent=None):
        self.model_setup_items = app().main_window.model_setup_widget.model_setup_items
        self.results_viewer_items = app().main_window.results_viewer_widget.results_viewer_items

        self._reset()

    def _reset(self):
        pass

    def process_input(self, working_class, *args, **kwargs):
        app().main_window.close_dialogs()
        read = working_class(*args, **kwargs)
        return read

    def mesh_setup(self):
        if self.model_setup_items.item_child_mesh_setup.isDisabled():
            return

        app().main_window.action_model_workspace_callback()
        obj = self.process_input(MesherSetupInputs)
        if obj.complete:
            self.model_setup_items.expand_menu_items()

    def advanced_element_options(self):
        if not self.model_setup_items.item_child_element_options.isDisabled():
            app().main_window.action_model_workspace_callback()
            self.process_input(ElementOptionsInputs)

    def set_material(self):
        if not self.model_setup_items.item_child_material.isDisabled():
            self.process_input(MaterialInputs)

    def set_fluid(self):
        if not self.model_setup_items.item_child_fluid.isDisabled():
            self.process_input(SetFluidInputs)

    def set_surface_thickness(self):
        if not self.model_setup_items.item_child_surface_thickness.isDisabled():
            self.process_input(SurfaceThicknessInputs)

    def prescribe_structural_dof(self):
        if not self.model_setup_items.item_child_prescribed_dof.isDisabled():
            self.process_input(DofPrescriptionInputs)

    def set_nodal_loads(self):
        if not self.model_setup_items.item_child_nodal_loads.isDisabled():
            self.process_input(NodalLoadsInputs)

    def set_distributed_loads(self):
        if not self.model_setup_items.item_child_distributed_loads.isDisabled():
            self.process_input(DistributedLoadsInputs)

    def set_distributed_mass(self):
        if not self.model_setup_items.item_child_distributed_mass.isDisabled():
            self.process_input(DistributedMassInputs)

    def set_normal_pressure_load(self):
        if not self.model_setup_items.item_child_normal_pressure_load.isDisabled():
            self.process_input(NormalPressureLoadInputs)

    def set_acoustic_pressure(self):
        if not self.model_setup_items.item_child_acoustic_pressure.isDisabled():
            self.process_input(AcousticPressureInputs)

    def set_mass_source(self):
        if not self.model_setup_items.item_child_mass_source.isDisabled():
            self.process_input(MassSourceInputs)

    def set_surface_velocity(self):
        if not self.model_setup_items.item_child_surface_velocity.isDisabled():
            self.process_input(SurfaceVelocityInputs)

    def set_incident_plane_wave(self):
        if not self.model_setup_items.item_child_incident_plane_wave.isDisabled():
            self.process_input(IncidentPlaneWaveInputs)

    def compressor_excitation_waveform(self):
        self.process_input(CompressorExcitationWaveformInputs)

    def compressor_excitation_spectrum(self):
        self.process_input(CompressorExcitationSpectrumInputs)

    def add_reciprocating_compressor_excitation(self):
        self.process_input(ReciprocatingCompressorInputs)

    def set_specific_impedance(self):
        self.process_input(SpecificImpedanceInputs)

    def set_transfer_impedance(self):
        self.process_input(TransferImpedanceInputs)

    def set_anechoic_termination(self):
        if not self.model_setup_items.item_child_anechoic_termination.isDisabled():
            self.process_input(AnechoicTerminationInputs)

    def set_absorption_surface(self):
        if not self.model_setup_items.item_child_absorption_surface.isDisabled():
            self.process_input(AbsorptionSurfaceInputs)

    def set_proportional_damping_for_acoustic_model(self):
        if not self.model_setup_items.item_child_proportional_damping.isDisabled():
            self.process_input(ProportionalDampingInput)

    def set_perforated_plate_model(self):
        if not self.model_setup_items.item_child_perforated_plate_model.isDisabled():
            self.process_input(PerforatedPlateModelInputs)

    def set_porous_material_model(self):
        if not self.model_setup_items.item_child_porous_material_model.isDisabled():
            self.process_input(PorousMaterialModelInputs)

    def set_viscous_thermal_model(self):
        if not self.model_setup_items.item_child_viscous_thermal_model.isDisabled():
            self.process_input(ViscousThermalLossModelInputs)

    def set_degrees_of_freedom_decoupling(self):
        if not self.model_setup_items.item_child_degrees_of_freedom_decoupling.isDisabled():
            self.process_input(DegreesOfFreedomDecouplingInputs)

    def set_acoustic_properties_grandient(self):
        if not self.model_setup_items.item_child_acoustic_properties_gradient.isDisabled():
            self.process_input(AcousticPropertiesGradientInputs)

    def set_acoustic_transfer_element_setup(self):
        if not self.model_setup_items.item_child_acoustic_transfer_element_setup.isDisabled():
            self.process_input(AcousticTransferElementInputs)

    def plot_structural_mode_shapes(self):
        if app().project.model.analysis_id in [AnalysisID.STRUCTURAL_MODAL, AnalysisID.ACOUSTIC_MODAL]:
            return self.process_input(PlotStructuralModeShapeInputs)

    def plot_displacement_field(self):
        if app().project.model.analysis_id == AnalysisID.STRUCTURAL_HARMONIC:
            return self.process_input(StructuralResponseFieldsInputs)

    def plot_structural_frequency_response(self):
        if app().project.model.analysis_id == AnalysisID.STRUCTURAL_HARMONIC:
            return self.process_input(PlotStructuralFrequencyResponseInputs)

    def plot_reaction_frequency_response(self):
        if self.projct:
            app().main_window.show_geometry_render_widget()

    def plot_stress_field(self):
        if not self.results_viewer_items.item_child_stress_field.isDisabled():
            app().main_window.configure_results_render_widget()

    def plot_stress_frequency_response(self):
        if not self.results_viewer_items.item_child_stress_frequency_response.isDisabled():
            app().main_window.show_geometry_render_widget()

    def plot_acoustic_mode_shapes(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_MODAL:
            return self.process_input(AcousticModeShapeInputs)

    def plot_acoustic_pressure_field(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AcousticPressureFieldInputs)

    def plot_acoustic_pressure_frequency_response(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AcousticPressureFrequencyResponseInputs)

    def plot_acoustic_pressure_frequency_response_function(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AcousticPressureFRFInputs)

    def plot_acoustic_shaking_forces(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AcousticShakingForcesInputs)

    def plot_acoustic_pressure_waveform_2d(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AcousticPressureWaveform2DPlotInputs)

    def plot_acoustic_pressure_waveform_3d(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AcousticPressureWaveform3DPlotInputs)

    def plot_allowable_pulsation_criteria_for_reciprocating_compressor(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AllowablePulsationsForReciprocatingCompressorInputs)

    def plot_allowable_pulsation_2d_for_screw_compressor(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AllowablePulsations2DPlotForScrewCompressorInputs)

    def plot_allowable_pulsation_3d_for_screw_compressor(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AllowablePulsations3DPlotForScrewCompressorInputs)

    def plot_TL_NR(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(TransmissionLossInputs)

    def plot_particle_velocity(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(ParticleVelocityInputs)

    def plot_acoustic_impedance(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AcousticImpedanceInputs)

    def plot_absorption_coefficient_from_surface(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(SurfaceAbsorptionCoefficientInputs)

    def decompose_acoustic_pressure_waves(self):
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AcousticWavesDecompositionInputs)

    def empty_project_action_message(self):
        title = "EMPTY PROJECT"
        message = "Please, you should create a new project or load an already existing one before start to set up the model. "
        message += "It is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = "ERROR"
        PrintMessageInput([window_title, title, message])
