import os
import logging
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy.special import jv

from vibra import app
from vibra.interface.loading_bar import load_function
from vibra.engine.porous_materials.porous_materials_models import PorousMaterialModels
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.properties.model_properties import ModelProperties
from vibra.errors import IncompleteSetupError
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.progress_status import ProgressStatus

window_title_1 = "Error"
window_title_2 = "Warning"


class ModelStatus:
    materials_setted: bool
    width_setted: bool
    solution_executed: bool


class Model:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):

        self.mesh = None
        self.mesh_setup = None
        self.generated_mesh = False

        self.analysis_data = None
        self.solid_acoustic_element = None
        self.surface_acoustic_element = None
        self.solid_structural_element = None
        self.surface_structural_element = None

        self.geometry_paths = list()

        self.lrf_eq_data = dict()
        self.lrf_properties = dict()
        self.porous_material_properties = dict()

        self.properties = ModelProperties()

    def set_geometry_path(self, paths : list):
        self.geometry_paths = paths

    def set_properties(self, properties):
        self.properties = properties

    def set_mesh_setup(self, mesh_setup):
        self.mesh_setup = mesh_setup

    def process_visual_geometry_mesh(self, paths):

        try:

            self.mesh = Mesh.from_cad(paths, dimension=2, size_factor=0.15)
            # self.mesh.get_model_areas(self.geometry_paths)
            self.generated_mesh = False

        except Exception as error_log:
            title = "Error while processing geometry"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])        


    def process_mesh(self):
        if len(self.geometry_paths) == 0:
            message = "Geometry not defined"
            context = ( "The geometry file has not been defined yet."
                        "You should to import a supported CAD file format to proceed."
                        "\n\n"
                        "Suported file formats: *.iges and *.step" )
            raise IncompleteSetupError(message, context=context)

        if self.mesh_setup is None:
            message = "Mesh setup not defined"
            context = ( "The mesh setup has not been defined yet."
                        "You should to configure the mesher to proceed." )
            raise IncompleteSetupError(message, context=context)

        # if self.mesh is None:
        #     self.mesh = Mesh.from_cad(self.geometry_paths)

        self.mesh.load_cad(self.geometry_paths, **self.mesh_setup)
        self.generated_mesh = True

        logging.info("Processing Mesh..." + ProgressStatus(95, 100))
        self.mesh._process_solid_elements_connected_to_nodes()

        # logging.info("Processing Mesh..." + ProgressStatus(95, 100))
        # self.mesh._process_element_average_coordinates()

        # logging.info("Renumbering nodes..." + ProgressStatus(90, 100))
        # self.mesh._process_nodes_reordering()

    def set_material(self, material, **kwargs):
        self.properties.set_material(material, **kwargs)

    def set_fluid(self, fluid, **kwargs):
        self.properties.set_fluid(fluid, **kwargs)

    def set_mesh(self, mesh):
        self.mesh = mesh
        self.generated_mesh = True

    def get_volume(self, **kwargs):
        """ This method returns the volume based on kwargs. """
        volume = kwargs.get("volume", None)
        if volume is None:
            try:
                element = kwargs.get("element", None) 
                volume = self.mesh.volume_from_element[element]
            except:
                # temporary solution to allow running external mesh file
                volume = 1
        return volume

    def get_fluid(self, **kwargs):
        """ This method returns the fluid relative to an element or volume and the volume id itself. """
        volume = self.get_volume(**kwargs)
        fluid = self.properties.get_fluid(volume=volume)
        return fluid, volume

    def get_fluid_properties(self, proportional_damping=False, **kwargs):
        """ This method returns the fluid properties """
        fluid, volume = self.get_fluid(**kwargs)
        dynamic_viscosity = fluid.dynamic_viscosity
        if proportional_damping:
            c_0 = self.properties.get_speed_of_sound(fluid, volume=volume)
            rho_0 = self.properties.get_fluid_density(fluid, volume=volume)
        else:
            c_0 = fluid.speed_of_sound
            rho_0 = fluid.fluid_density
        return rho_0, c_0, dynamic_viscosity

    def set_acoustic_element(self, element):
        self.solid_acoustic_element, self.surface_acoustic_element = element

    def set_structural_element(self, element):
        self.solid_structural_element, self.surface_structural_element = element

    def get_acoustic_global_dofs_from_nodes(self, nodes):
        if self.solid_acoustic_element is None:
            return list()
        _dofs_per_node = self.solid_acoustic_element.DOF_PER_NODE
        _nodes = nodes.reshape(-1, 1)
        global_dofs = _dofs_per_node * _nodes + np.arange(_dofs_per_node)
        return np.array(global_dofs.flatten(), dtype=int)

    def get_structural_global_dofs_from_nodes(self, nodes):
        if self.solid_structural_element is None:
            return list()
        _dofs_per_node = self.solid_structural_element.DOF_PER_NODE
        _nodes = nodes.reshape(-1, 1)
        global_dofs = _dofs_per_node * _nodes + np.arange(_dofs_per_node)
        return np.array(global_dofs.flatten(), dtype=int)

    def get_lrf_eq_data(self, modal=False):
        """ """

        self.lrf_eq_data = dict()
        self.lrf_properties = dict()

        if modal:
            return

        for key, data in self.properties.group_properties.items():
            property, group_id = key
            if property == "lrf_eq_model":
                #
                d = data["diameter"]
                surface_ids = data["surface_ids"]
                selection_radius = data["selection_radius"]
                averaged = data["averaged"]
                filter_type = data["filter_type"]

                post_process = load_function(self.mesh.get_elements_and_nodes_from_sphere, app().main_window)
                selected_elements, _ = post_process(surface_ids, 
                                                    selection_radius,
                                                    averaged = averaged,
                                                    filter_type = filter_type)

                # selected_elements, _ = self.mesh.get_elements_and_nodes_from_sphere( surface_ids, 
                #                                                                 selection_radius,
                #                                                                 averaged = averaged,
                #                                                                 filter_type = filter_type )

                for element_id in selected_elements:
                    #
                    fluid, _ = self.get_fluid(element=element_id)
                    c_0, rho_0, mu, gamma, Pr, P_0 = fluid.get_lrf_properties()
                    properties = [d, c_0, rho_0, mu, gamma, Pr, P_0]
                    #
                    if element_id not in list(self.lrf_eq_data.keys()):
                        #
                        self.lrf_eq_data[element_id] = properties
        
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "lrf_eq_model":
                #
                d = data["diameter"]
                fluid, _ = self.get_fluid(volume=volume_id)
                c_0, rho_0, mu, gamma, Pr, P_0 = fluid.get_lrf_properties()
                #
                properties = [d, c_0, rho_0, mu, gamma, Pr, P_0]
                self.set_lrf_eq_data([volume_id], properties)
        
        return self.lrf_eq_data

    def set_lrf_eq_data(self, volume_ids, properties):
        """ """
        if isinstance(volume_ids, int):
            volume_ids = [volume_ids]
        for volume_id in volume_ids:
            for element_id in self.mesh.elements_from_volume[volume_id]:
                self.lrf_eq_data[element_id] = properties

    def process_lrf_properties(self, frequencies):
        """ """

        if frequencies is None:
            return dict()

        logging.info( "Processing lrf properties (2/2)..." + ProgressStatus(20, 100))
        
        aux = defaultdict(list)
        self.lrf_properties = dict()
        if self.lrf_eq_data:

            if float(0) in frequencies:
                freqs = frequencies[1:]
            else:
                freqs = frequencies
            
            for element_index, parameters in self.lrf_eq_data.items():
                aux[str(parameters)].append(element_index)
            
            for str_parameters, element_indexes in aux.items():
                parameters = [float(str_parameter) for str_parameter in str_parameters[1:-1].split(",")]
                diameter, c_local, rho_local, mu, gamma, Pr, pressure = parameters  
                
                omegas = 2 * (np.pi) * freqs
                s = (diameter/2) * ((omegas*rho_local/mu)**(1/2))

                rho_ef = -rho_local * (jv(0, (1j**(3/2))*s)) / (jv(2, (1j**(3/2))*s))
                K0_ef = (pressure*gamma) / (gamma + (gamma - 1) * jv(2, (1j**(3/2))*s*(Pr**(1/2))) / jv(0, (1j**(3/2))*s*(Pr**(1/2))))
                c_ef = np.sqrt(K0_ef / rho_ef)

                if float(0) in frequencies:
                    rho_ef = np.insert(rho_ef, 0, rho_local)
                    c_ef = np.insert(c_ef, 0, c_local)      
                #
                for element_index in element_indexes:
                    self.lrf_properties[element_index] = {  "rho_eff" : rho_ef,
                                                            "C_eff" : c_ef   }

    def is_lrf_eq_model_active(self, surface_id):
        
        _volume_id = self.mesh.volume_from_surface[surface_id]
        for key, _ in self.properties.volume_properties.items():
            prop, volume_id = key
            if prop == "lrf_eq_model" and volume_id == _volume_id[0]:
                elements = self.mesh.elements_from_volume[volume_id]
                rho_eff = self.lrf_properties[elements[0]]["rho_eff"]
                C_eff = self.lrf_properties[elements[0]]["C_eff"]
                return True, rho_eff, C_eff

        return False, None, None

    def process_porous_material_properties(self, frequencies):

        model = PorousMaterialModels(self)
        model.process_effective_properties(frequencies)

        self.porous_material_properties = dict()
        for volume_id, data in model.porous_material_model.items():
            for element_id in self.mesh.elements_from_volume[volume_id]:
                self.porous_material_properties[element_id] = data
            # print(len(self.mesh.elements_from_volume[volume_id]))

    def is_porous_material_model_active(self, surface_id):

        for key, data in self.properties.volume_properties.items():
            prop, volume_id = key
            if prop == "porous_material_model":

                if volume_id in self.mesh.surfaces_from_volumes.keys():
                    surfaces_from_volume = self.mesh.surfaces_from_volumes[volume_id]

                    if surface_id in surfaces_from_volume:
                        elements = self.mesh.elements_from_volume[volume_id]
                        rho_eff = self.porous_material_properties[elements[0]]["rho_eff"]
                        C_eff = self.porous_material_properties[elements[0]]["C_eff"]
                        return True, rho_eff, C_eff

        return False, None, None

    # Properties can be accessed from outside, so this "indirection layer" is not needed
    def set_dissipation_model_data(self, data, volume=None):
        self.properties.set_dissipation_model(data, volume=volume)

    def set_porous_material_model_data(self, data, surface=None, volume=None):
        self.properties.set_porous_material_model_data(data, surface=surface, volume=volume)

    def set_lrf_eq_model_data(self, data, group=None, volume=None):
        self.properties.set_lrf_eq_model_data(data, group=group, volume=volume)

    def set_structural_boundary_condition(self, data, line, surface):
        self.properties.set_structural_boundary_condition(data, line, surface)

    def set_structural_load(self, data, line, surface):
        self.properties.set_structural_load(data, line, surface)

    def set_acoustic_pressure(self, data, surface):
        self.properties.set_acoustic_pressure(data, surface)

    def set_mass_flow_rate(self, data, surface):
        self.properties.set_mass_flow_rate(data, surface)

    def set_volume_velocity(self, data, surface):
        self.properties.set_volume_velocity(data, surface)

    def set_surface_velocity(self, data, surface):
        self.properties.set_surface_velocity(data, surface)

    def set_specific_impedance(self, data, surface):
        self.properties.set_specific_impedance(data, surface)