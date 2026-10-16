
from vibra import app
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.acoustic.acoustic_properties_gradient_inputs import AcousticPropertiesGradientInputs
from vibra.interface.model_inputs.acoustic.acoustic_transfer_element_inputs import AcousticTransferElementInputs
from vibra.interface.model_inputs.acoustic.dissipation_models.porous_material_model_inputs import PorousMaterialModelInputs
from vibra.interface.model_inputs.acoustic.dissipation_models.proportional_damping_inputs import ProportionalDampingInput
from vibra.interface.model_inputs.acoustic.dissipation_models.viscous_thermal_loss_model_inputs import ViscousThermalLossModelInputs
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
from vibra.interface.model_inputs.fluid.set_fluid_inputs import SetFluidInputs
from vibra.interface.model_inputs.general.element_options_inputs import ElementOptionsInputs
from vibra.interface.model_inputs.general.mesher_setup_inputs import MesherSetupInputs
from vibra.interface.model_inputs.general.volume_suppression_inputs import VolumeSuppressionInputs
from vibra.interface.model_inputs.material.set_material_inputs import MaterialInputs
from vibra.interface.model_inputs.structural.excitations.distributed_loads_inputs import DistributedLoadsInputs
from vibra.interface.model_inputs.structural.excitations.distributed_mass_inputs import DistributedMassInputs
from vibra.interface.model_inputs.structural.excitations.dof_prescription_inputs import DofPrescriptionInputs
from vibra.interface.model_inputs.structural.excitations.nodal_loads_inputs import NodalLoadsInputs
from vibra.interface.model_inputs.structural.excitations.normal_pressure_load_inputs import NormalPressureLoadInputs
from vibra.interface.model_inputs.structural.surface_thickness_inputs import SurfaceThicknessInputs


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
        app().main_window.action_model_workspace_callback()
        self.process_input(ElementOptionsInputs)

    def set_material(self):
        self.process_input(MaterialInputs)

    def set_fluid(self):
        self.process_input(SetFluidInputs)

    def set_surface_thickness(self):
        self.process_input(SurfaceThicknessInputs)

    def prescribe_structural_dof(self):
        self.process_input(DofPrescriptionInputs)

    def set_nodal_loads(self):
        self.process_input(NodalLoadsInputs)

    def set_distributed_loads(self):
        self.process_input(DistributedLoadsInputs)

    def set_distributed_mass(self):
        self.process_input(DistributedMassInputs)

    def set_normal_pressure_load(self):
        self.process_input(NormalPressureLoadInputs)

    def set_acoustic_pressure(self):
        self.process_input(AcousticPressureInputs)

    def set_mass_source(self):
        self.process_input(MassSourceInputs)

    def set_surface_velocity(self):
        self.process_input(SurfaceVelocityInputs)

    def set_incident_plane_wave(self):
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
        self.process_input(AnechoicTerminationInputs)

    def set_absorption_surface(self):
        self.process_input(AbsorptionSurfaceInputs)

    def set_proportional_damping_for_acoustic_model(self):
        self.process_input(ProportionalDampingInput)

    def set_perforated_plate_model(self):
        self.process_input(PerforatedPlateModelInputs)

    def set_porous_material_model(self):
        self.process_input(PorousMaterialModelInputs)

    def set_viscous_thermal_model(self):
        self.process_input(ViscousThermalLossModelInputs)

    def set_degrees_of_freedom_decoupling(self):
        self.process_input(DegreesOfFreedomDecouplingInputs)

    def set_volume_suppression(self):
        if not self.model_setup_items.item_child_volume_suppression.isDisabled():
            self.process_input(VolumeSuppressionInputs)

    def set_acoustic_properties_grandient(self):
        self.process_input(AcousticPropertiesGradientInputs)

    def set_acoustic_transfer_element_setup(self):
        self.process_input(AcousticTransferElementInputs)

    def empty_project_action_message(self):
        title = "EMPTY PROJECT"
        message = "Please, you should create a new project or load an already existing one before start to set up the model. "
        message += "It is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = "ERROR"
        PrintMessageInput([window_title, title, message])
