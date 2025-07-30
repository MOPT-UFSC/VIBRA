from vibra.interface.model_inputs.structural.material.set_material_inputs import MaterialInputs
from vibra.interface.model_inputs.acoustic.fluid.set_fluid_inputs import SetFluidInputs
from vibra.interface.mesh.set_mesh_setup_inputs import MeshSetupInputs
#
from vibra.interface.model_inputs.acoustic.acoustic_pressure_inputs import AcousticPressureInputs
from vibra.interface.model_inputs.acoustic.mass_flow_rate_inputs import MassFlowRateInputs
from vibra.interface.model_inputs.acoustic.mass_source_inputs import MassSourceInputs
from vibra.interface.model_inputs.acoustic.surface_velocity_inputs import SurfaceVelocityInputs
from vibra.interface.model_inputs.acoustic.incident_plane_wave_inputs import IncidentPlaneWaveInputs
from vibra.interface.model_inputs.acoustic.specific_impedance_inputs import SpecificImpedanceInputs
from vibra.interface.model_inputs.acoustic.transfer_impedance_inputs import TransferImpedanceInputs
from vibra.interface.model_inputs.acoustic.anechoic_termination_inputs import AnechoicTerminationInputs
from vibra.interface.model_inputs.acoustic.absorption_surface_inputs import AbsorptionSurfaceInputs
from vibra.interface.model_inputs.acoustic.proportional_damping_inputs import ProportionalDampingInput
from vibra.interface.model_inputs.acoustic.porous_material_model_inputs import PorousMaterialModelInputs
from vibra.interface.model_inputs.acoustic.viscous_thermal_loss_model_inputs import ViscousThermalLossModelInputs
from vibra.interface.model_inputs.acoustic.perforated_plate_model_inputs import PerforatedPlateModelInputs
from vibra.interface.model_inputs.acoustic.acoustic_properties_gradient_inputs import AcousticPropertiesGradientInputs
from vibra.interface.model_inputs.acoustic.reciprocating_compressor_inputs import ReciprocatingCompressorInputs
from vibra.interface.model_inputs.acoustic.acoustic_transfer_element_inputs import AcousticTransferElementInputs
from vibra.interface.model_inputs.acoustic.degrees_of_freedom_decoupling_inputs import DegreesOfFreedomDecouplingInputs
#
from vibra.interface.model_inputs.structural.surface_thickness_inputs import SurfaceThicknessInputs
from vibra.interface.model_inputs.structural.dofs_prescription_inputs import DofsPrescriptionInputs
from vibra.interface.model_inputs.structural.nodal_loads_inputs import NodalLoadsInputs
from vibra.interface.model_inputs.structural.normal_pressure_load_inputs import NormalPressureLoadInputs
from vibra.interface.model_inputs.structural.distributed_loads_inputs import DistributedLoadsInputs
#
from vibra.interface.plots.acoustic.acoustic_pressure_field_inputs import AcousticPressureFieldInputs
from vibra.interface.plots.acoustic.acoustic_pressure_frequency_response_inputs import AcousticPressureFrequencyResponseInputs
from vibra.interface.plots.acoustic.acoustic_frequency_response_function_inputs import AcousticPressureFrequencyResponseFunctionInputs
from vibra.interface.plots.acoustic.allowable_pulsations_for_reciprocating_compressor import AllowablePulsationsForReciprocatingCompressorInputs
from vibra.interface.plots.acoustic.specific_acoustic_impedance_inputs import SpecificAcousticImpedanceInputs
from vibra.interface.plots.acoustic.particle_velocity_frequency_response_inputs import ParticleVelocityFrequencyResponseInputs
from vibra.interface.plots.acoustic.transmission_loss_inputs import TransmissionLossInputs
from vibra.interface.plots.acoustic.acoustic_mode_shape_inputs import AcousticModeShapeInputs
#
from vibra.interface.plots.structural.structural_frequency_response_inputs import PlotStructuralFrequencyResponseInputs
from vibra.interface.plots.structural.structural_mode_shape_inputs import PlotStructuralModeShapeInputs
from vibra.interface.plots.structural.displacement_field_inputs import PlotDisplacementFieldInputs
#
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.general.print_message_input import PrintMessageInput

from vibra import app
from vibra.engine import AnalysisID

import logging

window_title_1 = "Error"
window_title_2 = "Warning"

class InputUi:
    def __init__(self, parent=None):

        self.main_window = app().main_window
        self.project = app().project

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
        if not self.model_setup_items.item_child_mesh_setup.isDisabled():
            self.main_window.action_model_workspace_callback()
            obj = self.process_input(MeshSetupInputs)
            if obj.complete:
                self.model_setup_items.modify_items_access_after_geometry_importing()
 
    def generate_mesh(self):
        LoadingWindow(app().project.generate_mesh).run()
        self.main_window.action_mesh_workspace_callback()
        self.model_setup_items.item_child_generate_mesh.setDisabled(True)
        nodes = list(app().project.model.mesh.nodes_collapsed_elements)
        app().main_window.set_mesh_selection(nodes=nodes)

    def set_material(self):
        if not self.model_setup_items.item_child_material.isDisabled():
            self.process_input(MaterialInputs)   

    def set_fluid(self):
        if not self.model_setup_items.item_child_fluid.isDisabled():
            self.process_input(SetFluidInputs)
        
    def set_surface_thickness(self):
        if not self.model_setup_items.item_child_surface_thickness.isDisabled():
            self.process_input(SurfaceThicknessInputs)
        
    def prescribe_structural_dofs(self):
        if not self.model_setup_items.item_child_prescribed_dofs.isDisabled():
            self.process_input(DofsPrescriptionInputs)
        
    def set_nodal_loads(self):
        if not self.model_setup_items.item_child_nodal_loads.isDisabled():
            self.process_input(NodalLoadsInputs)
        
    def set_distributed_loads(self):
        if not self.model_setup_items.item_child_distributed_loads.isDisabled():
            self.process_input(DistributedLoadsInputs)
    
    def set_normal_pressure_load(self):
        if not self.model_setup_items.item_child_normal_pressure_load.isDisabled():
            self.process_input(NormalPressureLoadInputs)

    def set_acoustic_pressure(self):
        if not self.model_setup_items.item_child_acoustic_pressure.isDisabled():
            self.process_input(AcousticPressureInputs)
        
    def set_mass_flow_rate(self):
        if not self.model_setup_items.item_child_mass_flow_rate.isDisabled():
            self.process_input(MassFlowRateInputs)

    def set_mass_source(self):
        if not self.model_setup_items.item_child_mass_source.isDisabled():
            self.process_input(MassSourceInputs)

    def set_surface_velocity(self):
        if not self.model_setup_items.item_child_surface_velocity.isDisabled():
            self.process_input(SurfaceVelocityInputs)

    def set_incident_plane_wave(self):
        if not self.model_setup_items.item_child_incident_plane_wave.isDisabled():
            self.process_input(IncidentPlaneWaveInputs)

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

    def add_reciprocating_compressor_excitation(self):
        self.process_input(ReciprocatingCompressorInputs)

    def plot_structural_mode_shapes(self):
        if self.project.analysis_id in [
            AnalysisID.STRUCTURAL_MODAL,
            AnalysisID.ACOUSTIC_MODAL,
        ]:
            return self.process_input(PlotStructuralModeShapeInputs)     

    def plot_displacement_field(self):
        if self.project.analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
        ]:
            return self.process_input(PlotDisplacementFieldInputs)

    def plot_structural_frequency_response(self):
        if self.project.analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
        ]:
            return self.process_input(PlotStructuralFrequencyResponseInputs)

    def plot_reaction_frequency_response(self):
        if self.projct:
            self.main_window.show_geometry_render_widget()

    def plot_stress_field(self):
        if not self.results_viewer_items.item_child_stress_field.isDisabled():
            self.main_window.configure_results_render_widget()

    def plot_stress_frequency_response(self):
        if not self.results_viewer_items.item_child_stress_frequency_response.isDisabled():
            self.main_window.show_geometry_render_widget() 

    def plot_acoustic_mode_shapes(self):
        if self.project.analysis_id == AnalysisID.ACOUSTIC_MODAL:
            return self.process_input(AcousticModeShapeInputs)

    def plot_acoustic_pressure_field(self):
        if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AcousticPressureFieldInputs)

    def plot_acoustic_pressure_frequency_response(self):
        if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AcousticPressureFrequencyResponseInputs)

    def plot_acoustic_pressure_frequency_response_function(self):
        if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AcousticPressureFrequencyResponseFunctionInputs)

    def plot_allowable_pulsation_criteria_for_reciprocating_compressor(self):
        if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(AllowablePulsationsForReciprocatingCompressorInputs)

    def plot_TL_NR(self):
       if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
           return self.process_input(TransmissionLossInputs)

    def plot_particle_velocity(self):
       if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
           return self.process_input(ParticleVelocityFrequencyResponseInputs)

    def plot_acoustic_specific_impedance_from_surface(self):
       if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
           return self.process_input(SpecificAcousticImpedanceInputs)

    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = "Please, you should create a new project or load an already existing one before start to set up the model. "
        message += "It is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([window_title, title, message])