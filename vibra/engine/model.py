import os
import logging
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy.special import jv

from vibra import app
from vibra.engine.porous_materials.porous_materials_models import PorousMaterialModels
from vibra.engine.mesher.geometry_setup import GeometrySetup
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

        self.surfaces_areas = dict()
        self.lrf_eq_data = dict()
        self.lrf_properties = dict()
        self.porous_material_properties = dict()

        self.geometry_path = Path("")

        self.properties = ModelProperties()

    def set_geometry_path(self, path):
        self.geometry_path = Path(path)

    def set_properties(self, properties):
        self.properties = properties

    def set_mesh_setup(self, mesh_setup):
        self.mesh_setup = mesh_setup

    def process_visual_geometry_mesh(self):
        self.mesh = Mesh.from_cad(self.geometry_path, dimension=2, size_factor=0.15)
        self.surfaces_areas = self.mesh.get_model_areas(self.geometry_path)
        self.generated_mesh = False

    def process_mesh(self):
        if not self.geometry_path.exists():
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

        if self.mesh is None:
            self.mesh = Mesh.from_cad(self.geometry_path)

        # self.geometry_path = Path("data/examples/script_files/script_hex_elements.txt")
        # self.mesh = Mesh.from_cad(self.geometry_path, gmsh_gui=True, **self.mesh_setup)

        self.mesh.update_parameters(**self.mesh_setup)
        self.generated_mesh = True

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
                selected_elements, _ = self.get_elements_and_nodes_from_sphere( surface_ids, 
                                                                                selection_radius,
                                                                                averaged = averaged,
                                                                                filter_type = filter_type )
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

        if len(self.lrf_properties) == 0:
            return False, None, None
        
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

        # elements = list(self.porous_material_properties.keys())
        # print(f"Size - prop: {len(self.porous_material_properties)}")
        # mesh_widget = app().main_window.viewer_tabs.mesh_widget
        # mesh_widget.select_multiple_volumes(elements)

    def is_porous_material_model_active(self, surface_id):

        if len(self.porous_material_properties) == 0:
            return False, None, None

        for key, data in self.properties.volume_properties.items():
            prop, volume_id = key
            if prop == "porous_material_model":
                surfaces_from_volume = self.mesh.surfaces_from_volumes[volume_id]

                if surface_id in surfaces_from_volume:
                    elements = self.mesh.elements_from_volume[volume_id]
                    rho_eff = self.porous_material_properties[elements[0]]["rho_eff"]
                    C_eff = self.porous_material_properties[elements[0]]["C_eff"]
                    return True, rho_eff, C_eff

        return False, None, None

    def get_average_nodal_coordinates(self, surface_ids, averaged=False):

        nodal_coordinates = self.mesh.nodal_coordinates
        self.stop, self.surface_ids = self.check_input_surface_id(surface_ids)

        if self.stop:
            return []

        rows = []
        for surface_id in self.surface_ids:
            if averaged:
                for row in self.mesh.nodes_from_surfaces[surface_id]:
                    rows.append(row)
            else:
                _nodes = list(self.mesh.nodes_from_surfaces[surface_id])
                rows.append(_nodes)

        center_coords = list()
        if rows:
            if averaged:
                avg_coords = np.average(nodal_coordinates[rows, 1:], axis=0)   
                center_coords.append(avg_coords)
            else:
                for row in rows:
                    avg_coords = np.average(nodal_coordinates[row, 1:], axis=0)
                    center_coords.append(avg_coords)

        return center_coords

    def get_elements_and_nodes_from_sphere(self, surface_ids, selection_radius, averaged=False, filter_type=0, export_data=False):

        list_center_coords = self.get_average_nodal_coordinates(surface_ids, averaged=averaged)
        if len(list_center_coords) == 0:
            return [], []

        selected_elements = []
        nodes_inside_sphere = []
        node_indexes = self.mesh.nodal_coordinates[:,0]
        nodal_coordinates = self.mesh.nodal_coordinates[:,1:]
        element_indexes = np.array(list(self.mesh.solid_elements_center.keys()), dtype=int)
        elements_center_coordinates = np.array(list(self.mesh.solid_elements_center.values()), dtype=float)
        for center_coords in list_center_coords:
            
            if filter_type == 0: # filters the elements inside sphere based on elements coordinates center
                
                diff_elem = np.linalg.norm(elements_center_coordinates - center_coords, axis=1) 
                diff_nodes = np.linalg.norm(nodal_coordinates - center_coords, axis=1)
                mask_elem = diff_elem <= selection_radius
                mask_nodes = diff_nodes <= selection_radius
            
                if sum(mask_nodes):
                    for node_id in node_indexes[mask_nodes]:
                        if node_id not in nodes_inside_sphere:
                            nodes_inside_sphere.append(node_id)
            
                if sum(mask_elem):
                    for element_id in element_indexes[mask_elem]:
                        if element_id not in selected_elements:
                            selected_elements.append(element_id)

            else: # filters the elements inside sphere based on nodal coordinates

                diff_nodes = np.linalg.norm(nodal_coordinates - center_coords, axis=1) 
                mask_nodes = diff_nodes <= selection_radius
                if sum(mask_nodes):
                    for node_id in node_indexes[mask_nodes]:
                        if node_id not in nodes_inside_sphere:
                            nodes_inside_sphere.append(node_id)
                            for element_id in self.mesh.solid_elements_from_nodes[node_id]:
                                if element_id not in selected_elements:
                                    selected_elements.append(element_id)

        if export_data:
            # list_nodes = np.array(nodes_inside_sphere, dtype=int).reshape(-1,1)
            # list_elements = np.array(selected_elements, dtype=int).reshape(-1,1)
            list_nodes = np.array(nodes_inside_sphere).reshape(-1,1)
            list_elements = np.array(selected_elements).reshape(-1,1)
            connectivity = self.mesh.solids_connectivity[:, 4:]
            rows = len(list_elements)
            cols = connectivity.shape[1]
            data_elem = np.zeros((rows, cols+1), dtype=int)
            data_elem[:, 0] = selected_elements
            data_elem[:, 1:] = connectivity[selected_elements, :]

            np.savetxt("nodes_inside_sphere.dat", list_nodes, delimiter=";", fmt='%i')
            np.savetxt("selected_elements.dat", list_elements, delimiter=";", fmt='%i')
            np.savetxt("selected_elements_data.dat", data_elem, delimiter=";", fmt="%i")
            print(f"Number of nodes: {len(nodes_inside_sphere)}")
            print(f"Number of elements: {len(selected_elements)}")

        return selected_elements, nodes_inside_sphere

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

    def check_input_surface_id(self, selected_ids, single_ID=False):
        try:
            title = "Invalid entry to the Surface ID"
            message = ""
            if isinstance(selected_ids, str):
                tokens = selected_ids.strip().split(",")
                try:
                    tokens.remove("")
                except:
                    pass
                list_ids = list(map(int, tokens))
            elif isinstance(selected_ids, list):
                list_ids = selected_ids
            elif isinstance(selected_ids, (tuple, np.ndarray)):
                list_ids = list(selected_ids)

            self.surface_ids = self.mesh.nodes_from_surfaces.keys()
            _size = len(self.surface_ids)

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
            PrintMessageInput([window_title_1, title, message])
            return True, []

        if single_ID:
            return False, list_ids[0]
        else:
            return False, list_ids

    def check_input_volume_id(self, selected_ids, single_ID=False):
        try:
            title = "Invalid entry to the Volume ID"
            message = ""
            if isinstance(selected_ids, str):
                tokens = selected_ids.strip().split(",")
                try:
                    tokens.remove("")
                except:
                    pass
                list_ids = list(map(int, tokens))
            elif isinstance(selected_ids, list):
                list_ids = selected_ids
            elif isinstance(selected_ids, (tuple, np.ndarray)):
                list_ids = list(selected_ids)
            
            self.volume_ids = self.mesh.nodes_from_volumes.keys()
            _size = len(self.volume_ids)

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
            PrintMessageInput([window_title_1, title, message])
            return True, []

        if single_ID:
            return False, list_ids[0]
        else:
            return False, list_ids