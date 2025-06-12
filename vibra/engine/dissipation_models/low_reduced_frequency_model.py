from vibra import app
from vibra.interface.loading_window import LoadingWindow

import logging
import numpy as np

from collections import defaultdict
from scipy.special import jv

class LowReducedFrequencyModel:

    def __init__(self, model):
        super().__init__()

        self.model = model
        self.mesh = model.mesh
        self.properties = model.properties

        self.low_reduced_frequency_model = dict()


    def get_low_reduced_frequency_model_data(self, modal=False):
        """ """

        self.lrf_model_data = dict()
        self.low_reduced_frequency_properties = dict()

        if modal:
            return

        for key, data in self.properties.group_properties.items():
            property, group_id = key
            if property == "lrf_eq_model":

                d = data["diameter"]
                surface_ids = data["surface_ids"]
                selection_radius = data["selection_radius"]
                averaged = data["averaged"]
                filter_type = data["filter_type"]

                LoadingWindow(self.mesh.get_elements_and_nodes_from_sphere).run(
                    surface_ids,
                    selection_radius,
                    averaged=averaged,
                    filter_type=filter_type,
                )

                selected_elements = self.mesh.selected_elements
                for element_id in selected_elements:
                    volume_id = self.mesh.volume_from_element[element_id]
                    fluid, _ = self.properties._get_property("fluid", volume=volume_id)

                    c_0, rho_0, mu, gamma, Pr, P_0 = fluid.get_lrf_properties()
                    properties = [d, c_0, rho_0, mu, gamma, Pr, P_0]

                    self.lrf_model_data[element_id] = properties

        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "lrf_eq_model":

                d = data["diameter"]
                fluid, _ = self.properties._get_property("fluid", volume=volume_id)
                c_0, rho_0, mu, gamma, Pr, P_0 = fluid.get_lrf_properties()

                properties = [d, c_0, rho_0, mu, gamma, Pr, P_0]

                for element_id in self.mesh.elements_from_volume[volume_id]:
                    self.lrf_model_data[element_id] = properties


    def process_effective_properties(self, frequencies: np.ndarray):
        """ """

        if frequencies is None:
            return dict()

        self.get_low_reduced_frequency_model_data()

        logging.info( "Processing lrf properties (2/2)... [20/100]")
        
        aux = defaultdict(list)
        self.low_reduced_frequency_properties = dict()

        if self.lrf_model_data:

            if float(0) in frequencies:
                freq = frequencies[1:]
            else:
                freq = frequencies

            omega = 2 * np.pi * freq
            
            for element_index, parameters in self.lrf_model_data.items():
                aux[str(parameters)].append(element_index)
            
            for str_parameters, element_indexes in aux.items():

                parameters = [float(str_parameter) for str_parameter in str_parameters[1:-1].split(",")]
                diameter, C_0, rho_0, mu, gamma, Pr, P_0 = parameters  

                radius = diameter / 2               
                s = radius * (np.sqrt( omega * rho_0 / mu))

                G_rho = s * ((1j)**(3/2))
                G_bulk = 1j * s * ((1j*Pr)**(1/2)) 

                rho_eff = - rho_0 * (jv(0, G_rho)) / (jv(2, G_rho))
                K0_eff = (P_0 * gamma) / (gamma + (gamma - 1) * jv(2, G_bulk) / jv(0, G_bulk))

                C_eff = np.sqrt(K0_eff / rho_eff)

                if float(0) in frequencies:
                    rho_eff = np.insert(rho_eff, 0, rho_0)
                    C_eff = np.insert(C_eff, 0, C_0)      

                for element_index in element_indexes:
                    self.low_reduced_frequency_properties[element_index] = {  
                                                                            "rho_eff" : rho_eff,
                                                                            "C_eff" : C_eff
                                                                            }
