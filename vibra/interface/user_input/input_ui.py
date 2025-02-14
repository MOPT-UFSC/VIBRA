from vibra.interface.analysis.analysis_setup_input import AnalysisSetupInput
from vibra.interface.analysis.analysis_type_input import AnalysisTypeInput
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
from vibra.interface.plots.acoustic.plot_acoustic_pressure_frequency_response_input import PlotAcousticPressureFrequencyResponseInput
from vibra.interface.plots.acoustic.plot_acoustic_frequency_response_function_input import PlotAcousticFrequencyResponseFunctionInput
from vibra.interface.plots.acoustic.plot_specific_acoustic_impedance_input import PlotSpecificAcousticImpedanceInput
from vibra.interface.plots.acoustic.plot_transmission_loss_input import PlotTransmissionLossInput
#
from vibra.interface.plots.structural.plot_structural_frequency_response_input import PlotStructuralFrequencyResponseInput
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

        self.menu_items = app().main_window.menu_widget
        self.results_viewer_items = app().main_window.results_viewer_items

        self._reset()

    def _reset(self):
        self.project.none_project_action = False

    def process_input(self, working_class, *args, **kwargs):
        app().main_window.close_dialogs()
        read = working_class(*args, **kwargs)
        return read

    def call_geometry_editor(self):
        main_window = self.main_window
        main_window.show_geometry_render_widget()

    def set_material(self):
        self.process_input(SetMaterialInput)   

    def set_fluid(self):
        self.process_input(SetFluidInput)

    def set_acoustic_pressure(self):
        self.process_input(AcousticPressureInput)

    def set_specific_impedance(self):
        self.process_input(SpecificImpedanceInput)

    def add_reciprocating_compressor_excitation(self):
        self.process_input(ReciprocatingCompressorInputs)

    def analysis_setup(self):
        analysis_setup = AnalysisSetupInput()
        self.item_child_analysis_setup.setDisabled(False)

        if analysis_setup.complete:
            self.item_child_run_analysis.setDisabled(False)

        if analysis_setup.solve_analysis:
            self.run_analysis()

    def plot_structural_mode_shapes(self):
        if not self.results_viewer_items.item_child_plot_structural_mode_shapes.isDisabled():
            self.main_window.configure_structural_modal_analysis_render_widget()     

    def plot_displacement_field(self):
        if not self.results_viewer_items.item_child_plot_displacement_field.isDisabled():
            self.main_window.configure_structural_harmonic_analysis_render_widget(True)

    def plot_structural_frequency_response(self):
        if not self.results_viewer_items.item_child_plot_structural_frequency_response.isDisabled():
            self.process_input(PlotStructuralFrequencyResponseInput)

    def plot_reaction_frequency_response(self):
        if not self.results_viewer_items.item_child_plot_reaction_frequency_response.isDisabled():
            self.main_window.show_geometry_render_widget()

    def plot_stress_field(self):
        if not self.results_viewer_items.item_child_plot_stress_field.isDisabled():
            self.main_window.configure_structural_harmonic_analysis_render_widget(True)

    def plot_stress_frequency_response(self):
        if not self.results_viewer_items.item_child_plot_stress_frequency_response.isDisabled():
            self.main_window.show_geometry_render_widget() 

    def plot_acoustic_mode_shapes(self):
        if not self.results_viewer_items.item_child_plot_acoustic_mode_shapes.isDisabled():
            self.main_window.configure_acoustic_modal_analysis_render_widget(True)

    def plot_acoustic_pressure_field(self):
        if not self.results_viewer_items.item_child_plot_acoustic_pressure_field.isDisabled():
            self.main_window.configure_acoustic_harmonic_analysis_render_widget(True)

    def plot_acoustic_pressure_frequency_response(self):
        if not self.results_viewer_items.item_child_plot_acoustic_pressure_frequency_response.isDisabled():
            self.process_input(PlotAcousticPressureFrequencyResponseInput)

    def plot_acoustic_frequency_response_function(self):
        if not self.results_viewer_items.item_child_plot_acoustic_pressure_frequency_response_function.isDisabled():
            self.process_input(PlotAcousticFrequencyResponseFunctionInput)

    def plot_acoustic_delta_pressures(self):
        pass

    def plot_transmission_loss(self):
       if not self.results_viewer_items.item_child_plot_TL_NR.isDisabled():
           self.process_input(PlotTransmissionLossInput)
            
    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = "Please, you should create a new project or load an already existing one before start to set up the model. "
        message += "It is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([window_title, title, message])