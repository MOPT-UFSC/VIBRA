
from vibra import app
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material

import numpy as np

error_title = "Error"
warning_title = "Warning"


class AnalysisRequirementsChecker:
    def __init__(self):

        self.model = app().project.model
        self.properties = app().project.model.properties

        self.surface_ids = self.model.mesh.geometry_information["surfaces"]
        self.volume_ids = self.model.mesh.geometry_information["volumes"]

    def check_materials(self):

        if self.volume_ids:
            volumes_without_material = self.properties.get_entities_without_property("material", volumes=self.volume_ids)
            if volumes_without_material:
                title = "Invalid model setup"
                message = f"You should assign one material for volumes {volumes_without_material} "
                message += "to proceed with the analysis solution."
                app().main_window.workspace_updating_for_model_setup()
                app().main_window.selection.set_geometry_selection(volumes=volumes_without_material)
                PrintMessageInput([error_title, title, message])
                return True

        else:
            surfaces_without_material = self.properties.get_entities_without_property("material", surfaces=self.surface_ids)
            if surfaces_without_material:
                title = "Invalid model setup"
                message = f"You should assign one material for surfaces {surfaces_without_material} "
                message += "to proceed with the analysis solution."
                app().main_window.workspace_updating_for_model_setup()
                app().main_window.selection.set_geometry_selection(surfaces=surfaces_without_material)
                PrintMessageInput([error_title, title, message])
                return True

            surfaces_without_thickness = self.properties.get_entities_without_property("surface_thickness", surfaces=self.surface_ids)
            if surfaces_without_thickness:
                title = "Invalid model setup"
                message = f"You should assign the surface thickness for surfaces {surfaces_without_thickness} "
                message += "to proceed with the analysis solution."
                app().main_window.workspace_updating_for_model_setup()
                app().main_window.selection.set_geometry_selection(surfaces=surfaces_without_thickness)
                PrintMessageInput([error_title, title, message])
                return True

        return False

    def check_fluids(self):

        volumes_without_fluid = self.properties.get_entities_without_property("fluid", volumes=self.volume_ids)
        surfaces_without_fluid = self.properties.get_entities_without_property("fluid", surfaces=self.surface_ids)

        if not self.volume_ids:
            title = "Invalid geometry for acoustic analysis"
            message = f"The selected geometry file does not contain "
            message += "volumes, therefore, it is invalid for acoustic analysis."
            PrintMessageInput([error_title, title, message])
            return True

        if volumes_without_fluid:
            title = "Invalid model setup"
            message = f"You should assign one fluid for volumes {volumes_without_fluid} "
            message += "to proceed with the analysis solution."
            app().main_window.action_model_workspace_callback()
            app().main_window.selection.set_geometry_selection(volumes=volumes_without_fluid)
            PrintMessageInput([error_title, title, message])
            return True

        else:
            if surfaces_without_fluid:
                title = "Invalid model setup"
                message = f"You should assign one fluid for surfaces {surfaces_without_fluid} "
                message += "to proceed with the analysis solution."
                app().main_window.action_model_workspace_callback()
                app().main_window.selection.set_geometry_selection(surfaces=surfaces_without_fluid)
                PrintMessageInput([error_title, title, message])
                return True

            return False

    def check_frequency_varying_fluid_properties_for_modal_analysis(self):
        pm_exists = self.properties.is_the_volume_property_present_in_the_model("porous_material_model")
        vt_exists = self.properties.is_the_volume_property_present_in_the_model("viscous_thermal_model")

        if pm_exists or vt_exists:
            title = "Invalid model setup"
            message = "A frequency-varying fluid property was detected in the acoustic model. The modal "
            message += "analysis can only be solved for fluid properties that are constant or proportional "
            message += "to frequency. Consider reconfiguring the acoustic model to proceed with the "
            message += "acoustic modal analysis solution."
            PrintMessageInput([error_title, title, message])
            return True

        return False

    def check_acoustic_harmonic_excitations(self):

        prop_labels = [
                       "acoustic_pressure",
                       "surface_velocity",
                       "incident_plane_wave",
                       "compressor_excitation_spectrum",
                       "compressor_excitation_waveform",
                       "reciprocating_compressor_excitation",
                       "mass_source",
                       ]

        properties = [
                      self.properties.volume_properties,
                      self.properties.surface_properties,
                      self.properties.line_properties,
                      self.properties.point_properties,
                      self.properties.nodal_properties,
                      ]

        for property in properties:
            for (prop_label, *_), data in property.items():
                if prop_label in prop_labels:
                    if np.sum(data["values"]):
                        return False

        title = "Invalid model excitation"    
        message = "Enter a valid acoustic model excitation to proceed "
        message += "with the acoustic harmonic analysis solution."
        PrintMessageInput([error_title, title, message])

        return True

    def check_structural_harmonic_excitations(self):

        prop_labels = [
                       "prescribed_dof", 
                       "nodal_loads", 
                       "distributed_loads", 
                       "normal_pressure_load",
                       ]

        properties = [
                      self.properties.surface_properties, 
                      self.properties.line_properties, 
                      self.properties.point_properties, 
                      self.properties.nodal_properties,
                      ]

        for property in properties:
            for (prop_label, *_), data in property.items():
                if prop_label not in prop_labels:
                    continue

                values = [0 if value is None else value for value in data["values"]]
                if np.array(sum(values)).any():
                    return False

        title = "Invalid model excitation"    
        message = "Enter a valid structural model excitation to proceed "
        message += "with the structural harmonic analysis solution."
        PrintMessageInput([error_title, title, message])

        return True

    def check_nonzero_prescribed_dof_for_mode_superposition_method(self):

        properties = [
                      self.properties.surface_properties, 
                      self.properties.line_properties, 
                      self.properties.point_properties, 
                      self.properties.nodal_properties,
                      ]

        for property in properties:
            for (prop_label, *_), data in property.items():
                if prop_label != "prescribed_dof":
                    continue

                values = [0 if value is None else value for value in data["values"]]
                if np.array(sum(values)).any():
                    return False

        return True

    def check_acoustic_harmonic_analysis(self):

        if self.check_fluids():
            return True
        
        if self.check_acoustic_harmonic_excitations():
            return True

    def check_structural_harmonic_analysis(self):

        if self.check_materials():
            return True
        
        if self.check_structural_harmonic_excitations():
            return True

        if self.model.analysis_setup.get("analysis_method") == "mode_superposition":
            if self.check_mode_superposition_prescribed_dof_criterion():
                return True

    def check_acoustic_modal_analysis(self):

        if self.check_fluids():
            return True

        if self.check_frequency_varying_fluid_properties_for_modal_analysis():
            return True

    def check_structural_modal_analysis(self):

        if self.check_materials():
            return True
        
    def check_mode_superposition_prescribed_dof_criterion(self):

        if self.check_nonzero_prescribed_dof_for_mode_superposition_method():
            return False

        title = "Invalid model excitation for harmonic analysis"    
        message = "Harmonic analysis using the modal superposition method cannot be solved if "
        message += "there are any nonzero prescribed degrees of freedom. Would you like to solve "
        message += "the model using the direct method?"

        tool_tip = "Press this button to proceed with the harmonic \n"
        tool_tip += "analysis solution using the direct method"

        buttons_config = {
                        "left_button_label": "Cancel", 
                        "right_button_label": "Solve (direct)",
                        "right_toolTip" : tool_tip
                        }

        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config, window_title="Vibra")
        if read._cancel:
            return True

        if not read._continue:
            return True
        
        # change the analysis type
        analysis_setup = app().file.read_analysis_setup_from_file()
        if isinstance(analysis_setup, dict):
            analysis_setup["analysis_method"] = "direct"
            analysis_setup.pop("modes_number")

            app().file.write_analysis_setup_in_file(analysis_setup)
            app().project.model.set_analysis_setup(analysis_setup)