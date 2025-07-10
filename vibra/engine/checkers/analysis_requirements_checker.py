
from vibra import app
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class AnalysisRequirementsChecker:
    def __init__(self):

        self.model = app().project.model
        self.properties = app().project.model.properties

        self.surface_ids = self.model.mesh.geometry_information["surfaces"]
        self.volume_ids = self.model.mesh.geometry_information["volumes"]

    def check_materials(self, surface_thickness=True):

        volumes_without_material = list()
        for volume_id in self.volume_ids:
            prop_data = self.properties._get_property("material", volume=volume_id)
            if prop_data is None:
                volumes_without_material.append(volume_id)

        surfaces_without_material = list()
        for surface_id in self.surface_ids:
            prop_data = self.properties._get_property("material", surface=surface_id)
            if prop_data is None:
                surfaces_without_material.append(surface_id)

        surfaces_without_material, _, shell_without_thickness = self.check_material_and_surface_thickness()
        if volumes_without_material:
            if len(volumes_without_material) != len(self.volume_ids):
                title = "Invalid model setup"
                message = f"You should assign one material for volumes {volumes_without_material} "
                message += "to proceed with the analysis solution."
                app().main_window.action_model_workspace_callback()
                app().main_window.set_geometry_selection(volumes=volumes_without_material)
                PrintMessageInput([window_title_1, title, message])
                return True

        if len(volumes_without_material) == len(self.volume_ids):
            if len(surfaces_without_material) == len(self.surface_ids):
                title = "Invalid model setup"
                if len(self.volume_ids):
                    message = f"You should assign one material for all volumes or some surfaces "
                else:
                    message = f"You should assign one material to some surfaces "
                message += "to proceed with the analysis solution."
                # app().main_window.set_geometry_selection(surfaces=shell_without_material)
                PrintMessageInput([window_title_1, title, message])
                return True

            if shell_without_thickness:
                title = "Invalid model setup"
                if len(shell_without_thickness) == len(self.surface_ids):
                    message = f"You should assign at least one material and thickness for one surface "
                else:
                    message = f"You should assign a thickness for the already assigned surface materials "
                    app().main_window.set_geometry_selection(surfaces=shell_without_thickness)
                message += "to proceed with the analysis solution."
                PrintMessageInput([window_title_1, title, message])
                return True

        return False

    def check_fluids(self):

        volumes_without_fluid = list()
        for volume_id in self.volume_ids:
            prop_data = self.properties._get_property("fluid", volume=volume_id)
            if prop_data is None:
                volumes_without_fluid.append(volume_id)

        surfaces_without_fluid = list()
        for surface_id in self.surface_ids:
            prop_data = self.properties._get_property("fluid", surface=surface_id)
            if prop_data is None:
                surfaces_without_fluid.append(surface_id)

        if self.volume_ids:

            if volumes_without_fluid:
                title = "Invalid model setup"
                message = f"You should assign one fluid for volumes {volumes_without_fluid} "
                message += "to proceed with the analysis solution."
                app().main_window.action_model_workspace_callback()
                app().main_window.set_geometry_selection(volumes=volumes_without_fluid)
                PrintMessageInput([window_title_1, title, message])
                return True

            else:
                if surfaces_without_fluid:
                    title = "Invalid model setup"
                    message = f"You should assign one fluid for surfaces {surfaces_without_fluid} "
                    message += "to proceed with the analysis solution."
                    app().main_window.action_model_workspace_callback()
                    app().main_window.set_geometry_selection(surfaces=surfaces_without_fluid)
                    PrintMessageInput([window_title_1, title, message])
                    return True

                return False

        else:
            title = "Invalid geometry for acoustic analysis"
            message = f"The selected geometry file does not contain "
            message += "volumes, therefore, it is invalid for acoustic analysis."
            PrintMessageInput([window_title_1, title, message])
            return True

    def check_material_and_surface_thickness(self):

        shell_without_material = list()
        surface_without_material = list()
        shell_without_thickness = list()
        for surface_id in self.surface_ids:
            mat_data = self.properties._get_property("material", surface=surface_id)
            st_data = self.properties._get_property("surface_thickness", surface=surface_id)
            if mat_data is None:
                surface_without_material.append(surface_id)
                if isinstance(st_data, dict):
                    shell_without_material.append(surface_id)
            elif isinstance(mat_data, Material) and st_data is None:
                shell_without_thickness.append(surface_id)

        return surface_without_material, shell_without_material, shell_without_thickness

    def check_acoustic_harmonic_excitations(self):

        prop_labels = [
                       "acoustic_pressure", 
                       "surface_velocity",
                       "mass_flow_rate",
                       "incident_plane_wave",
                       "compressor_excitation",
                       "mass_source",
                       ]

        properties = [
                      self.properties.surface_properties,
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
        PrintMessageInput([window_title_1, title, message])

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
                    if np.sum(values):
                        return False

        title = "Invalid model excitation"    
        message = "Enter a valid structural model excitation to proceed "
        message += "with the structural harmonic analysis solution."
        PrintMessageInput([window_title_1, title, message])

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