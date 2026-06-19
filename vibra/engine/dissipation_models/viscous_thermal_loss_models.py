import logging
from typing import TYPE_CHECKING

from vibra.engine.properties.fluid import Fluid
from vibra.interface.model_inputs.acoustic.dissipation_models.circular_duct_data import CircularDuctData
from vibra.interface.model_inputs.acoustic.dissipation_models.rectangular_duct_data import RectangularDuctData

if TYPE_CHECKING:
    from vibra.engine.model import Model

from collections import defaultdict

import numpy as np
from scipy.special import jv


class ViscousThermalLossModels:

    def __init__(self, model: "Model"):
        super().__init__()

        self.model = model
        self.properties = model.properties

        self.effective_properties = dict()

        self.map_model_id_to_models: defaultdict[int, RectangularDuctData|CircularDuctData] = defaultdict()
        self.map_model_id_to_volumes: defaultdict[int, list[int]] = defaultdict(list)

    def process_effective_properties(self, frequencies: np.ndarray | None = None):

        self.effective_properties.clear()
        if not self.properties.is_the_volume_property_present_in_the_model("viscous_thermal_model"):
            return

        if frequencies is None:
            frequencies = self.model.frequencies

        if frequencies is None:
            return

        if isinstance(frequencies, list):
            frequencies = np.array(frequencies, dtype=float)

        if len(frequencies) == 0:
            return

        if frequencies[0] == 0:
            freq = frequencies[1:]
        else:
            freq = frequencies

        omega = 2 * np.pi * freq

        self.map_existing_viscous_thermal_loss_models()
        map_volumes_to_effective_properties = defaultdict()

        for model_id, volume_ids in self.map_model_id_to_volumes.items():
            for volume_id in volume_ids:
                data = self.map_model_id_to_models.get(model_id)
                if data is None:
                    continue

                fluid: Fluid = self.properties._get_property("fluid", volume = volume_id)
                section_type = data.section_type
                formulation = data.formulation

                key = (fluid.identifier, model_id)
                rho_eff, C_eff = None, None

                if key in map_volumes_to_effective_properties:
                    rho_eff, C_eff = map_volumes_to_effective_properties[key]

                elif section_type in ["Rectangular duct", "Quadrangular duct"]:
                    rho_eff, C_eff = self.get_rectangular_section_effective_properties(omega, fluid, data)

                elif section_type in ["Narrow slit duct"]:
                    rho_eff, C_eff = self.get_narrow_slit_section_effective_properties(omega, fluid, data)

                elif section_type in ["Circular duct"]:
                    if formulation == "Stinson model":
                        rho_eff, C_eff = self.get_circular_section_effective_properties_for_Stinson_model(omega, fluid, data)
                    else:
                        rho_eff, C_eff = self.get_circular_section_effective_properties_for_LRF_model(omega, fluid, data)

                else:
                    continue

                map_volumes_to_effective_properties[key] = (rho_eff, C_eff)

                self.effective_properties[volume_id] = {
                    "section_type" : section_type,
                    "rho_eff" : rho_eff,
                    "C_eff" : C_eff,
                }

    def get_rectangular_section_effective_properties(self, omega: np.ndarray, fluid: Fluid, data: RectangularDuctData, fast_integration: bool=True):

        P_0 = fluid.pressure  # noqa: F841
        rho_0 = fluid.fluid_density
        C_0 = fluid.speed_of_sound
        gamma = fluid.isentropic_exponent
        Cp = fluid.specific_heat_Cp
        mu = fluid.dynamic_viscosity
        k_t = fluid.thermal_conductivity
        Pr = mu * Cp / k_t

        # isentropic bulk modulus
        # K_s = gamma * P_0
        K_s = rho_0 * C_0**2

        width = data.width
        height = data.height
        number_of_terms = data.number_of_terms
        # area = width * height

        a = width / 2
        b = height / 2
 
        n = np.arange(0, number_of_terms)
        m = np.arange(0, number_of_terms)
        a_n = (n + 0.5)*(np.pi / a)
        b_m = (m + 0.5)*(np.pi / b)

        aux_rho = np.zeros(len(omega), dtype=complex)
        aux_comp = np.zeros(len(omega), dtype=complex)

        if fast_integration:

            # define the common terms for the double integration
            an_bn = np.zeros((number_of_terms, number_of_terms), dtype=complex)
            an2_bn2 = np.zeros((number_of_terms, number_of_terms), dtype=complex)
            for n, an in enumerate(a_n):
                an_bn[:, n] = (an*b_m)**2
                an2_bn2[:, n] = an**2 + b_m**2

            # efficient way to compute the double integration
            for i, w in enumerate(omega):
                aux_rho[i] = np.sum(1 / (an_bn*(an2_bn2 + 1j*w*rho_0/mu)))
                aux_comp[i] = np.sum(1 / (an_bn*(an2_bn2 + 1j*w*rho_0*Pr/mu)))

        else:

            # compute the double integration using an internal loop
            for i, w in enumerate(omega):
                sum_rho = 0.
                sum_comp = 0.

                for n, an in enumerate(a_n):
                    sum_rho += sum(1 / (((an*b_m)**2)*(an**2 + b_m**2 + 1j*w*rho_0/mu)))
                    sum_comp += sum(1 / (((an*b_m)**2)*(an**2 + b_m**2 + 1j*w*rho_0*Pr/mu)))

                aux_rho[i] = sum_rho
                aux_comp[i] = sum_comp

        # Effective complex density (viscous-thermal losses in duct)
        rho_eff = mu * (((a*b)**2) / (4*1j*omega)) * (1/aux_rho)

        # Effective complex bulk modulus (viscous-thermal losses in duct)
        K_eff = K_s / (gamma - (gamma-1) * ((4*1j*omega*Pr*rho_0) / (mu*(a*b)**2)) * aux_comp)

        # Complex speed of sound
        C_eff = np.sqrt(K_eff / rho_eff)

        # # Complex wave number of duct
        # kc = omega*np.sqrt(rho_eff / K_eff)

        # # characteristic acoustic impedance of duct
        # Zc = np.sqrt(K_eff * rho_eff) / area

        return rho_eff, C_eff


    def get_narrow_slit_section_effective_properties(self, omega: np.ndarray, fluid: Fluid, data: RectangularDuctData):

        P_0 = fluid.pressure  # noqa: F841
        rho_0 = fluid.fluid_density
        C_0 = fluid.speed_of_sound
        gamma = fluid.isentropic_exponent
        Cp = fluid.specific_heat_Cp
        mu = fluid.dynamic_viscosity
        k_t = fluid.thermal_conductivity
        Pr = mu * Cp / k_t

        # isentropic bulk modulus
        # K_s = gamma * P_0
        K_s = rho_0 * C_0**2

        height = data.height

        G_rho = (height / 2) * np.sqrt(1j * omega * rho_0 / mu)
        G_bulk = (height / 2) * np.sqrt(1j * omega * rho_0 * Pr / mu)

        # Effective complex density (viscous-thermal losses in narrow slit duct)
        rho_eff =  rho_0 / (1 - (np.tanh(G_rho) / G_rho))

        # Effective complex bulk modulus (viscous-thermal losses in narrow slit duct)
        K_eff = K_s / (1 + (gamma-1) * (np.tanh(G_bulk) / G_bulk))

        # Effective complex speed of sound
        C_eff = np.sqrt(K_eff / rho_eff)
        # C_eff = np.real(np.sqrt(K_eff / rho_eff)) ??

        # # Complex wave number of duct
        # kc = omega*np.sqrt(rho_eff / K_eff)

        # # characteristic acoustic impedance of duct
        # Zc = np.sqrt(K_eff * rho_eff) / area

        return rho_eff, C_eff

    def get_circular_section_effective_properties_for_Stinson_model(self, omega: np.ndarray, fluid: Fluid, data: CircularDuctData):

        P_0 = fluid.pressure  # noqa: F841
        rho_0 = fluid.fluid_density
        C_0 = fluid.speed_of_sound
        gamma = fluid.isentropic_exponent
        Cp = fluid.specific_heat_Cp
        mu = fluid.dynamic_viscosity
        k_t = fluid.thermal_conductivity
        Pr = mu * Cp / k_t

        # isentropic bulk modulus
        # K_s = gamma * P_0
        K_s = rho_0 * C_0**2

        diameter = data.diameter

        radius = diameter / 2
        # area = np.pi * (diameter**2) / 4

        G_rho = radius * np.sqrt(-1j * omega * rho_0 / mu)
        G_bulk = radius * np.sqrt(-1j * omega * rho_0 * Pr / mu)
        # G_bulk = radius * Pr * np.sqrt(-1j * omega * rho_0 / mu)

        invalid_values = False

        array_r0 = jv(0, G_rho)
        if (0 in array_r0) or np.isnan(array_r0).any() or np.isinf(array_r0).any():
            invalid_values = True

        array_r1 = jv(1, G_rho)
        if np.isnan(array_r1).any() or np.isinf(array_r1).any():
            invalid_values = True

        array_b0 = jv(0, G_bulk)
        if (0 in array_b0) or np.isnan(array_b0).any() or np.isinf(array_b0).any():
            invalid_values = True

        array_b1 = jv(1, G_bulk)
        if np.isnan(array_b1).any() or np.isinf(array_b1).any():
            invalid_values = True

        if invalid_values:
            message = "\nInvalid values were found during the calculation of the Bessel function 'jv' for the \n" \
            "effective properties of the circular section using the Stinson model. The viscous-thermal \n" \
            "effect will be disabled, and the normal fluid properties will be used instead.\n"

            logging.info(message)
            print(message)

            aux_ones = np.ones_like(omega, dtype=float)
            rho_eff = rho_0 * aux_ones
            C_eff = C_0 * aux_ones

            return rho_eff, C_eff

        # Effective complex density (viscous-thermal losses in duct)
        rho_eff = rho_0 / (1 - (2 / G_rho) * (jv(1, G_rho) / jv(0, G_rho)))

        # Effective complex bulk modulus (viscous-thermal losses in duct)
        K_eff = K_s / (1 + (gamma-1) * (2 / G_bulk) * (jv(1, G_bulk) / jv(0, G_bulk)))

        # Effective complex speed of sound
        C_eff = np.sqrt(K_eff / rho_eff)

        # # Complex wave number of duct
        # kc = omega*np.sqrt(rho_eff / K_eff)

        # # characteristic acoustic impedance of duct
        # Zc = np.sqrt(K_eff * rho_eff) / area

        return rho_eff, C_eff


    def get_circular_section_effective_properties_for_LRF_model(self, omega: np.ndarray, fluid: Fluid, data: CircularDuctData):

        P_0 = fluid.pressure  # noqa: F841
        rho_0 = fluid.fluid_density
        C_0 = fluid.speed_of_sound
        gamma = fluid.isentropic_exponent
        Cp = fluid.specific_heat_Cp
        mu = fluid.dynamic_viscosity
        k_t = fluid.thermal_conductivity
        Pr = mu * Cp / k_t

        # isentropic bulk modulus
        # K_s = gamma * P_0
        K_s = rho_0 * C_0**2

        diameter = data.diameter

        radius = diameter / 2
        s = radius * (np.sqrt( omega * rho_0 / mu))

        G_rho = s * ((1j)**(3/2))
        G_bulk = s * ((1j)**(3/2)) * np.sqrt(Pr) 

        invalid_values = False

        array_r2 = jv(2, G_rho)
        if (0 in array_r2) or np.isnan(array_r2).any() or np.isinf(array_r2).any():
            invalid_values = True

        array_r0 = jv(0, G_rho)
        if np.isnan(array_r0).any() or np.isinf(array_r0).any():
            invalid_values = True

        array_b0 = jv(0, G_bulk)
        if (0 in array_b0) or np.isnan(array_b0).any() or np.isinf(array_b0).any():
            invalid_values = True

        array_b2 = jv(2, G_bulk)
        if np.isnan(array_b2).any() or np.isinf(array_b2).any():
            invalid_values = True

        if invalid_values:
            message = "\nInvalid values were found during the calculation of the Bessel function 'jv' for the \n" \
            "effective properties of the circular section using the LRF model. The viscous-thermal \n" \
            "effect will be disabled, and the normal fluid properties will be used instead.\n"

            logging.info(message)
            print(message)

            aux_ones = np.ones_like(omega, dtype=float)
            rho_eff = rho_0 * aux_ones
            C_eff = C_0 * aux_ones

            return rho_eff, C_eff

        # Effective complex density (viscous-thermal losses in duct)
        rho_eff = - rho_0 * (jv(0, G_rho)) / (jv(2, G_rho))

        # Effective complex bulk modulus (viscous-thermal losses in duct)
        K_eff = K_s / (gamma + (gamma - 1) * jv(2, G_bulk) / jv(0, G_bulk))

        # Effective complex speed of sound
        C_eff = np.sqrt(K_eff / rho_eff)

        return rho_eff, C_eff
    
    def map_existing_viscous_thermal_loss_models(self):
        self.map_model_id_to_volumes.clear()
        self.map_model_id_to_models.clear()

        models = list()
        for key, data in self.properties.volume_properties.items():

            property, volume_id = key
            if property == "viscous_thermal_model":
                
                model = None
                section_type = data["section_type"]

                if section_type in ["Rectangular duct", "Quadrangular duct", "Narrow slit duct"]:
                    model = RectangularDuctData.set_data(data)
                else:
                    model = CircularDuctData.set_data(data)

                if model not in models:
                    models.append(model)
                
                model_id = models.index(model) + 1
                self.map_model_id_to_models[model_id] = model
                self.map_model_id_to_volumes[model_id].append(volume_id)