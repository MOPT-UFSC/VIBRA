import os
import logging
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy.special import jv

from vibra.engine.mesher.geometry_setup import GeometrySetup
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.properties.model_properties import ModelProperties
from vibra.errors import IncompleteSetupError
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.progress_status import ProgressStatus

window_title = "Error"


class ModelStatus:
    materials_setted: bool
    width_setted: bool
    solution_executed: bool


class Model:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        #
        self.geometry_path = Path("")
        self.mesh = None
        self.mesh_setup = None
        self.generated_mesh = False
        self.surfaces_areas = dict()

        self.analysis_data = None
        self.solid_acoustic_element = None
        self.surface_acoustic_element = None
        self.solid_structural_element = None
        self.surface_structural_element = None
        self.reset_lrf_eq_model()
        self.properties = ModelProperties()

    def set_geometry_path(self, path):
        self.geometry_path = Path(path)

    def set_properties(self, properties):
        self.properties = properties

    def set_mesh_setup(self, mesh_setup):
        self.mesh_setup = mesh_setup

    def process_visual_geometry_mesh(self):
        self.mesh = Mesh.from_cad(self.geometry_path, dimension=2, size_factor=0.2)
        self.surfaces_areas = self.mesh.get_model_areas(self.geometry_path)
        self.generated_mesh = False

    def process_mesh(self):
        if not self.geometry_path.exists():
            message = "Geometry not defined"
            context = (
                "The geometry file has not been defined yet."
                "You should to import a supported CAD file format to proceed."
                "\n\n"
                "Suported file formats: *.iges and *.step"
            )
            raise IncompleteSetupError(message, context=context)

        if self.mesh_setup is None:
            message = "Mesh setup not defined"
            context = (
                "The mesh setup has not been defined yet."
                "You should to configure the mesher to proceed."
            )
            raise IncompleteSetupError(message, context=context)

        if self.mesh is None:
            self.mesh = Mesh.from_cad(self.geometry_path)

        # self.geometry_path = Path("data/examples/script_files/script_hex_elements.txt")
        # self.mesh = Mesh.from_cad(self.geometry_path, gmsh_gui=True, **self.mesh_setup)

        self.mesh.update_parameters(**self.mesh_setup)
        self.generated_mesh = True

        logging.info("Renumbering nodes..." + ProgressStatus(90, 100))
        self.mesh._process_nodes_reordering()

    def set_material(self, material, **kwargs):
        self.properties.set_material(material, **kwargs)

    def set_fluid(self, fluid, **kwargs):
        self.properties.set_fluid(fluid, **kwargs)

    def set_mesh(self, mesh):
        self.mesh = mesh
        self.generated_mesh = True

    def get_fluid_properties(self, proportional_damping=False, **kwargs):
        """ This method returns the fluid properties """
        # volume_id = self.mesh.elements_from_volumes[el_index]
        # fluid = self.properties.get_fluid(volume=volume_id)
        # c_0 = fluid.speed_of_sound
        element = kwargs.get("element", None)
        volume = kwargs.get("volume", None)

        if element is not None:
            try:
                volume = self.mesh.volume_from_element[element]
            except:
                # temporary solution to allow running external mesh file
                volume = 1

        fluid = self.properties.get_fluid(volume=volume)
        dynamic_viscosity = fluid.dynamic_viscosity
        if proportional_damping:
            c_0 = self.properties.get_speed_of_sound(fluid, volume=volume)
            rho_0 = self.properties.get_fluid_density(fluid, volume=volume)
        else:
            c_0 = fluid.speed_of_sound
            rho_0 = fluid.fluid_density
        # if volume not in [1, 8]:
        #     print(volume, element, proportional_damping, c_0, rho_0, dynamic_viscosity)
        return rho_0, c_0, dynamic_viscosity

    def set_acoustic_element(self, element):
        self.solid_acoustic_element, self.surface_acoustic_element = element

    def set_structural_element(self, element):
        self.solid_structural_element, self.surface_structural_element = element

    def get_acoustic_global_dofs_from_nodes(self, nodes):
        if self.solid_acoustic_element is None:
            return []
        _dofs_per_node = self.solid_acoustic_element.DOF_PER_NODE
        _nodes = nodes.reshape(-1, 1)
        global_dofs = _dofs_per_node * _nodes + np.arange(_dofs_per_node)
        return np.array(global_dofs.flatten(), dtype=int)

    def get_structural_global_dofs_from_nodes(self, nodes):
        if self.solid_structural_element is None:
            return []
        _dofs_per_node = self.solid_structural_element.DOF_PER_NODE
        _nodes = nodes.reshape(-1, 1)
        global_dofs = _dofs_per_node * _nodes + np.arange(_dofs_per_node)
        return np.array(global_dofs.flatten(), dtype=int)

    def reset_lrf_eq_model(self):
        self.lrf_eq_data = dict()
        self.lrf_properties = dict()

    def get_lrf_eq_data(self):
        """ """
        self.lrf_eq_data = dict()
        # TODO: enable the elements selection by surfaces boundaries
        # for key, data in self.properties.surface_properties.items():
        #     property, surface_id = key
        #     if property == "lrf_eq_model":
        #         for surface_id in data["surface_ids"]:
        #             fluid = self.properties.get_fluid(surface=surface_id)
        #             for element_id in self.model.mesh.elements_from_surfaces[surface_id]:
        #                 # fluid = self.properties.get_fluid(element=element_id)
        #                 if element_id not in list(lrf_eq_data.keys()):
        #                     lrf_eq_data[element_id] = {"diameter" : data["diameter"],
        #                                                "c_0" : fluid.speed_of_sound,
        #                                                "rho_0" : fluid.fluid_density,
        #                                                "mu" : fluid.dynamic_viscosity,
        #                                                "gamma" : fluid.isentropic_exponent,
        #                                                "prandtl" : fluid.prandtl_number,
        #                                                "pressure" : fluid.pressure_state}
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "lrf_eq_model":
                #
                fluid = self.properties.get_fluid(volume=volume_id)
                #
                d = data["diameter"]
                c_0 = fluid.speed_of_sound
                rho_0 = fluid.fluid_density
                mu = fluid.dynamic_viscosity
                gamma = fluid.isentropic_exponent
                Pr = fluid.prandtl_number
                P_0 = fluid.pressure_state
                #
                properties = [d, c_0, rho_0, mu, gamma, Pr, P_0]
                self.set_lrf_eq_data([volume_id], properties)
        
        return self.lrf_eq_data

    def set_lrf_eq_data(self, volume_ids, properties):
        """ """
        if isinstance(volume_ids, int):
            volume_ids = [volume_ids]
        for volume_id in volume_ids:
            for element_id in self.mesh.elements_from_volumes[volume_id]:
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
                c_ef_2 = K0_ef/rho_ef

                if float(0) in frequencies:
                    rho_ef = np.insert(rho_ef, 0, rho_local)
                    c_ef_2 = np.insert(c_ef_2, 0, c_local**2)                
                #
                for element_index in element_indexes:
                    self.lrf_properties[element_index] = {  "rho_ef" : rho_ef,
                                                            "c_ef_2" : c_ef_2   }

    def check_if_lrf_eq_model_is_active(self, surface_id):
        if len(self.lrf_properties) == 0:
            return False, None
        
        _volume_id = self.mesh.volume_from_surface[surface_id]
        for key, _ in self.properties.volume_properties.items():
            prop, volume_id = key
            if prop == "lrf_eq_model" and volume_id == _volume_id[0]:
                elements = self.mesh.elements_from_volumes[volume_id]
                rho_eff = self.lrf_properties[elements[0]]["rho_ef"]
                return True, rho_eff
        return False, None

    # Properties can be accessed from outside, so this "indirection layer" is not needed
    def set_dissipation_model_data(self, data):
        self.properties.set_dissipation_model(data)

    def set_lrf_eq_model_data(self, data, surface=None, volume=None):
        self.properties.set_lrf_eq_model_data(data, surface=surface, volume=volume)

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

    def check_input_surface_id(self, str_selected_ids, single_ID=False):
        try:
            title = "Invalid entry to the Surface ID"
            message = ""
            tokens = str_selected_ids.strip().split(",")
            self.surface_ids = self.mesh.nodes_from_surfaces.keys()

            try:
                tokens.remove("")
            except:
                pass

            _size = len(self.surface_ids)
            list_ids = list(map(int, tokens))

            if len(list_ids) == 0:
                message = "An empty input field for the Surface ID has been detected. Please, enter a valid Surface ID to proceed."

            elif len(list_ids) >= 1:
                if single_ID and len(list_ids) > 1:
                    message = "Multiple Selected IDs"
                else:
                    try:
                        for _id in list_ids:
                            if _id not in self.surface_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                                message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                                break
                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                        message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                        message += f"\n\n{str(error_log)}"

        except Exception as log_error:
            message = "Wrong input for the Selected ID's. "
            message += f"\n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([title, message, window_title])
            return True, []

        if single_ID:
            return False, list_ids[0]
        else:
            return False, list_ids

    def check_input_volume_id(self, str_selected_ids, single_ID=False):
        try:
            title = "Invalid entry to the Volume ID"
            message = ""
            tokens = str_selected_ids.strip().split(",")
            self.volume_ids = self.mesh.nodes_from_volumes.keys()

            try:
                tokens.remove("")
            except:
                pass

            _size = len(self.volume_ids)
            list_ids = list(map(int, tokens))

            if len(list_ids) == 0:
                message = "An empty input field for the Volume ID has been detected. Please, enter a valid Volume ID to proceed."

            elif len(list_ids) >= 1:
                if single_ID and len(list_ids) > 1:
                    message = "Multiple Selected IDs"
                else:
                    try:
                        for _id in list_ids:
                            if _id not in self.volume_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                                message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                                break
                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                        message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                        message += f"\n\n{str(error_log)}"

        except Exception as log_error:
            message = "Wrong input for the Selected ID's. "
            message += f"\n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([title, message, window_title])
            return True, []

        if single_ID:
            return False, list_ids[0]
        else:
            return False, list_ids