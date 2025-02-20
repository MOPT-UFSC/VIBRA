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
from vibra.interface.model_inputs.acoustic.set_porous_material_model import SetPorousMaterialModel
from vibra.interface.model_inputs.acoustic.set_viscous_thermal_loss_model import SetViscousThermalLossModel
from vibra.interface.model_inputs.acoustic.set_acoustic_properties_gradient_input import SetAcousticPropertiesGradientInputs
from vibra.interface.model_inputs.acoustic.reciprocating_compressor_inputs import ReciprocatingCompressorInputs
from vibra.interface.model_inputs.acoustic.process_acoustic_transfer_element_data import ProcessAcousticTransferElementData
#
from vibra.interface.model_inputs.structural.surface_thickness_inputs import SurfaceThicknessInput
from vibra.interface.model_inputs.structural.prescribed_dofs_inputs import PrescribedDofsInputs
from vibra.interface.model_inputs.structural.structural_external_loads_inputs import StructuralExternalLoadsInputs
from vibra.interface.model_inputs.structural.structural_pressure_load_inputs import SetStructuralPressureLoadInputs
#
from vibra.interface.plots.acoustic.plot_acoustic_pressure_field import PlotAcousticPressureField
from vibra.interface.plots.acoustic.plot_acoustic_pressure_frequency_response_input import PlotAcousticPressureFrequencyResponseInput
from vibra.interface.plots.acoustic.plot_acoustic_frequency_response_function_input import PlotAcousticPressureFrequencyResponseFunctionInput
from vibra.interface.plots.acoustic.plot_specific_acoustic_impedance_input import PlotSpecificAcousticImpedanceInput
from vibra.interface.plots.acoustic.plot_transmission_loss_input import PlotTransmissionLossInput
from vibra.interface.plots.acoustic.plot_acoustic_mode_shape import PlotAcousticModeShape
#
from vibra.interface.plots.structural.plot_structural_frequency_response_input import PlotStructuralFrequencyResponseInput
from vibra.interface.plots.structural.plot_structural_mode_shape import PlotStructuralModeShape
from vibra.interface.plots.structural.plot_displacement_field import PlotDisplacementField
#
from vibra.interface.process_analysis import ProcessAnalysis

from vibra.interface.loading_bar import load_function
from vibra.interface.general.print_message_input import PrintMessageInput

from vibra import app

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
        self.project.none_project_action = False

    def process_input(self, working_class, *args, **kwargs):
        app().main_window.close_dialogs()
        read = working_class(*args, **kwargs)
        return read

    def import_geometry(self):
        if not self.model_setup_items.item_child_import_geometry.isDisabled():
            if self.main_window.import_geometry_dialog():
                self.model_setup_items.modify_items_access_after_geometry_importing()
            
    def mesh_setup(self):
        if not self.model_setup_items.item_child_mesh_setup.isDisabled():
            obj = self.process_input(MesherInputs)
            if obj.complete:
                self.model_setup_items.modify_items_access_after_geometry_importing()
            
    def generate_mesh(self):
        generate_mesh = load_function(app().project.generate_mesh, self.main_window)
        generate_mesh()

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
            self.process_input(SurfaceThicknessInput)
        
    def set_prescribed_dofs(self):
        if not self.model_setup_items.item_child_set_prescribed_dofs.isDisabled():
            self.process_input(PrescribedDofsInputs)
        
    def set_external_loads(self):
        if not self.model_setup_items.item_child_set_external_loads.isDisabled():
            self.process_input(StructuralExternalLoadsInputs)
    
    def set_pressure_load(self):
        if not self.model_setup_items.item_child_set_pressure_load.isDisabled():
            self.process_input(SetStructuralPressureLoadInputs)

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
            self.process_input(SetPorousMaterialModel)
        
    def set_viscous_thermal_model(self):
        if not self.model_setup_items.item_child_set_viscous_thermal_model.isDisabled():
            self.process_input(SetViscousThermalLossModel)
        
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
        if self.project.analysis_id in [2, 4]:
            return self.process_input(PlotStructuralModeShape)     

    def plot_displacement_field(self):
        if self.project.analysis_id in [0, 1]:
            return self.process_input(PlotDisplacementField)

    def plot_structural_frequency_response(self):
        if self.project.analysis_id in [0, 1]:
            return self.process_input(PlotStructuralFrequencyResponseInput)

    def plot_reaction_frequency_response(self):
        if self.projct:
            self.main_window.show_geometry_render_widget()

    def plot_stress_field(self):
        if not self.results_viewer_items.item_child_plot_stress_field.isDisabled():
            self.main_window.configure_structural_harmonic_analysis_render_widget(True)

    def plot_stress_frequency_response(self):
        if not self.results_viewer_items.item_child_plot_stress_frequency_response.isDisabled():
            self.main_window.show_geometry_render_widget() 

    def plot_acoustic_mode_shapes(self):
        if self.project.analysis_id in [4]:
            return self.process_input(PlotAcousticModeShape)

    def plot_acoustic_pressure_field(self):
        if self.project.analysis_id in [3]:
            return self.process_input(PlotAcousticPressureField)

    def plot_acoustic_pressure_frequency_response(self):
        if self.project.analysis_id in [3]:
            return self.process_input(PlotAcousticPressureFrequencyResponseInput)

    def plot_acoustic_pressure_frequency_response_function(self):
        if self.project.analysis_id in [3]:
            return self.process_input(PlotAcousticPressureFrequencyResponseFunctionInput)

    def plot_acoustic_delta_pressures(self):
        pass

    def plot_TL_NR(self):
       if self.project.analysis_id in [3]:
           return self.process_input(PlotTransmissionLossInput)
            
    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = "Please, you should create a new project or load an already existing one before start to set up the model. "
        message += "It is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([window_title, title, message])