from vibra.interface.model_inputs.structural.material.set_material_input import SetMaterialInput
from vibra.interface.model_inputs.acoustic.fluid.set_fluid_input import SetFluidInput
from vibra.interface.mesh.mesher_inputs import MesherInputs
#
from vibra.interface.model_inputs.acoustic.set_acoustic_pressure import AcousticPressureInput
from vibra.interface.model_inputs.acoustic.set_mass_flow_rate_inputs import MassFlowRateInput
from vibra.interface.model_inputs.acoustic.set_surface_velocity_inputs import SurfaceVelocityInput
from vibra.interface.model_inputs.acoustic.set_specific_impedance_inputs import SpecificImpedanceInput
from vibra.interface.model_inputs.acoustic.set_anechoic_termination_inputs import SetAnechoicTerminationInputs
from vibra.interface.model_inputs.acoustic.set_dissipation_model_inputs import DissipationModelInput
from vibra.interface.model_inputs.acoustic.set_porous_material_model_inputs import SetPorousMaterialModelInputs
from vibra.interface.model_inputs.acoustic.set_viscous_thermal_loss_model import SetViscousThermalLossModel
from vibra.interface.model_inputs.acoustic.set_perforated_plate_model_inputs import SetPerforatedPlateModelInputs
from vibra.interface.model_inputs.acoustic.set_acoustic_properties_gradient_input import SetAcousticPropertiesGradientInputs
from vibra.interface.model_inputs.acoustic.reciprocating_compressor_inputs import ReciprocatingCompressorInputs
from vibra.interface.model_inputs.acoustic.process_acoustic_transfer_element_data import ProcessAcousticTransferElementData
#
from vibra.interface.model_inputs.structural.set_surface_thickness_inputs import SetSurfaceThicknessInput
from vibra.interface.model_inputs.structural.set_prescribed_dofs_inputs import SetPrescribedDofsInputs
from vibra.interface.model_inputs.structural.set_nodal_loads_inputs import SetNodalLoadsInputs
from vibra.interface.model_inputs.structural.set_normal_pressure_load_inputs import SetNormalPressureLoadInputs
from vibra.interface.model_inputs.structural.set_distributed_loads_inputs import SetDistributedLoadsInputs
# #
from vibra.interface.plots.acoustic.plot_acoustic_pressure_field import PlotAcousticPressureField
from vibra.interface.plots.acoustic.plot_acoustic_pressure_frequency_response_input import PlotAcousticPressureFrequencyResponseInput
from vibra.interface.plots.acoustic.plot_acoustic_frequency_response_function_input import PlotAcousticPressureFrequencyResponseFunctionInput
from vibra.interface.plots.acoustic.plot_specific_acoustic_impedance_input import PlotSpecificAcousticImpedanceInput
from vibra.interface.plots.acoustic.plot_particle_velocity_frequency_response_input import PlotParticleVelocityFrequencyResponseInput
from vibra.interface.plots.acoustic.plot_transmission_loss_input import PlotTransmissionLossInput
from vibra.interface.plots.acoustic.plot_acoustic_mode_shape import PlotAcousticModeShape
#
from vibra.interface.plots.structural.plot_structural_frequency_response_input import PlotStructuralFrequencyResponseInput
from vibra.interface.plots.structural.plot_structural_mode_shape import PlotStructuralModeShape
from vibra.interface.plots.structural.plot_displacement_field import PlotDisplacementField
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
            obj = self.process_input(MesherInputs)
            if obj.complete:
                self.model_setup_items.modify_items_access_after_geometry_importing()
 
    def generate_mesh(self):
        LoadingWindow(app().project.generate_mesh).run()
        self.main_window.action_mesh_workspace_callback()
        self.model_setup_items.item_child_generate_mesh.setDisabled(True)

    def set_material(self):
        if not self.model_setup_items.item_child_set_material.isDisabled():
            self.process_input(SetMaterialInput)   

    def set_fluid(self):
        if not self.model_setup_items.item_child_set_fluid.isDisabled():
            self.process_input(SetFluidInput)
        
    def set_surface_thickness(self):
        if not self.model_setup_items.item_child_set_surface_thickness.isDisabled():
            self.process_input(SetSurfaceThicknessInput)
        
    def set_prescribed_dofs(self):
        if not self.model_setup_items.item_child_set_prescribed_dofs.isDisabled():
            self.process_input(SetPrescribedDofsInputs)
        
    def set_nodal_loads(self):
        if not self.model_setup_items.item_child_set_nodal_loads.isDisabled():
            self.process_input(SetNodalLoadsInputs)
        
    def set_distributed_loads(self):
        if not self.model_setup_items.item_child_set_distributed_loads.isDisabled():
            self.process_input(SetDistributedLoadsInputs)
    
    def set_normal_pressure_load(self):
        if not self.model_setup_items.item_child_set_normal_pressure_load.isDisabled():
            self.process_input(SetNormalPressureLoadInputs)

    def set_acoustic_pressure(self):
        if not self.model_setup_items.item_child_set_acoustic_pressure.isDisabled():
            self.process_input(AcousticPressureInput)
        
    def set_mass_flow_rate(self):
        if not self.model_setup_items.item_child_set_mass_flow_rate.isDisabled():
            self.process_input(MassFlowRateInput)
        
    def set_surface_velocity(self):
        if not self.model_setup_items.item_child_set_surface_velocity.isDisabled():
            self.process_input(SurfaceVelocityInput)
        
    def set_anechoic_termination(self):
        if not self.model_setup_items.item_child_set_anechoic_termination.isDisabled():
            self.process_input(SetAnechoicTerminationInputs)
        
    def set_dissipation_model(self):
        if not self.model_setup_items.item_child_set_dissipation_model.isDisabled():
            self.process_input(DissipationModelInput)
        
    def set_porous_material_model(self):
        if not self.model_setup_items.item_child_set_porous_material_model.isDisabled():
            self.process_input(SetPorousMaterialModelInputs)
        
    def set_viscous_thermal_model(self):
        if not self.model_setup_items.item_child_set_viscous_thermal_model.isDisabled():
            self.process_input(SetViscousThermalLossModel)

    def set_perforated_plate_model(self):
        if not self.model_setup_items.item_child_set_perforated_plate_model.isDisabled():
            self.process_input(SetPerforatedPlateModelInputs)

    def set_acoustic_properties_grandient(self):
        if not self.model_setup_items.item_child_set_acoustic_properties_gradient.isDisabled():
            self.process_input(SetAcousticPropertiesGradientInputs)
        
    def set_acoustic_transfer_element_setup(self):
        if not self.model_setup_items.item_child_set_acoustic_transfer_element_setup.isDisabled():
            self.process_input(ProcessAcousticTransferElementData)

    def set_specific_impedance(self):
        self.process_input(SpecificImpedanceInput)

    def add_reciprocating_compressor_excitation(self):
        self.process_input(ReciprocatingCompressorInputs)

    def plot_structural_mode_shapes(self):
        if self.project.analysis_id in [
            AnalysisID.STRUCTURAL_MODAL,
            AnalysisID.ACOUSTIC_MODAL,
        ]:
            return self.process_input(PlotStructuralModeShape)     

    def plot_displacement_field(self):
        if self.project.analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
        ]:
            return self.process_input(PlotDisplacementField)

    def plot_structural_frequency_response(self):
        if self.project.analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
        ]:
            return self.process_input(PlotStructuralFrequencyResponseInput)

    def plot_reaction_frequency_response(self):
        if self.projct:
            self.main_window.show_geometry_render_widget()

    def plot_stress_field(self):
        if not self.results_viewer_items.item_child_plot_stress_field.isDisabled():
            self.main_window.configure_results_render_widget()

    def plot_stress_frequency_response(self):
        if not self.results_viewer_items.item_child_plot_stress_frequency_response.isDisabled():
            self.main_window.show_geometry_render_widget() 

    def plot_acoustic_mode_shapes(self):
        if self.project.analysis_id == AnalysisID.ACOUSTIC_MODAL:
            return self.process_input(PlotAcousticModeShape)

    def plot_acoustic_pressure_field(self):
        if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(PlotAcousticPressureField)

    def plot_acoustic_pressure_frequency_response(self):
        if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(PlotAcousticPressureFrequencyResponseInput)

    def plot_acoustic_pressure_frequency_response_function(self):
        if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return self.process_input(PlotAcousticPressureFrequencyResponseFunctionInput)

    def plot_acoustic_delta_pressures(self):
        pass

    def plot_TL_NR(self):
       if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
           return self.process_input(PlotTransmissionLossInput)
     
    def plot_particle_velocity(self):
       if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
           return self.process_input(PlotParticleVelocityFrequencyResponseInput)
                   
    def plot_acoustic_specific_impedance_from_surface(self):
       if self.project.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
           return self.process_input(PlotSpecificAcousticImpedanceInput)
     
    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = "Please, you should create a new project or load an already existing one before start to set up the model. "
        message += "It is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([window_title, title, message])