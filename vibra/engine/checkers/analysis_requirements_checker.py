
from vibra import app
from vibra.interface.general.print_message_input import PrintMessageInput
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

        volumes_without_material = self.properties.get_entities_without_property("material", volumes=self.volume_ids)
        if volumes_without_material:
            if len(volumes_without_material) != len(self.volume_ids):
                title = "Invalid model setup"
                message = f"You should assign one material for volumes {volumes_without_material} "
                message += "to proceed with the analysis solution."
                app().main_window.workspace_updating_for_model_setup()
                app().main_window.set_geometry_selection(volumes=volumes_without_material)
                PrintMessageInput([error_title, title, message])
                return True

        surfaces_without_material = self.properties.get_entities_without_property("material", surfaces=self.surface_ids)
        if surfaces_without_material:
            if len(surfaces_without_material) != len(self.surface_ids):
                title = "Invalid model setup"
                message = f"You should assign one material for surfaces {surfaces_without_material} "
                message += "to proceed with the analysis solution."
                app().main_window.workspace_updating_for_model_setup()
                app().main_window.set_geometry_selection(surfaces=surfaces_without_material)
                PrintMessageInput([error_title, title, message])
                return True

        surfaces_without_thickness = self.properties.get_entities_without_property("surface_thickness", surfaces=self.surface_ids)
        if surfaces_without_thickness:
            if len(surfaces_without_thickness) != len(self.surface_ids):
                title = "Invalid model setup"
                message = f"You should assign the surface thickness for surfaces {surfaces_without_thickness} "
                message += "to proceed with the analysis solution."
                app().main_window.workspace_updating_for_model_setup()
                app().main_window.set_geometry_selection(surfaces=surfaces_without_thickness)
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
            app().main_window.set_geometry_selection(volumes=volumes_without_fluid)
            PrintMessageInput([error_title, title, message])
            return True

        else:
            if surfaces_without_fluid:
                title = "Invalid model setup"
                message = f"You should assign one fluid for surfaces {surfaces_without_fluid} "
                message += "to proceed with the analysis solution."
                app().main_window.action_model_workspace_callback()
                app().main_window.set_geometry_selection(surfaces=surfaces_without_fluid)
                PrintMessageInput([error_title, title, message])
                return True

            return False           

    def check_acoustic_harmonic_excitations(self):

        prop_labels = [
                       "acoustic_pressure", 
                       "surface_velocity",
                       "mass_flow_rate",
                       "incident_plane_wave",
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
                       "prescribed_dofs", 
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
                if prop_label in prop_labels:
                    values = [0 if value is None else value for value in data["values"]]
                    if np.array(sum(values)).any():
                        return False

        title = "Invalid model excitation"    
        message = "Enter a valid structural model excitation to proceed "
        message += "with the structural harmonic analysis solution."
        PrintMessageInput([error_title, title, message])

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

    def check_acoustic_modal_analysis(self):

        if self.check_fluids():
            return True

    def check_structural_modal_analysis(self):

        if self.check_materials():
            return True