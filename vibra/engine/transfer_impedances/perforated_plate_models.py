
from vibra.engine.properties.fluid import Fluid
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np
from scipy.special import jv

class PerforatedPlateModels:
    def __init__(self, model: "Model", **kwargs):

        self.model = model
        self.properties = model.properties

        self.perforated_plate_impedance_data = dict()

    def process_acoustic_transfer_impedances(self, frequencies: np.ndarray):

        self.perforated_plate_impedance_data.clear()

        if frequencies[0] == 0:
            freq = frequencies[1:]
        else:
            freq = frequencies

        omega = 2 * np.pi * freq

        if not self.properties.is_the_surface_property_present_in_the_model("perforated_plate_model"):
            return

        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "perforated_plate_model":

                fluid = self.properties._get_property("fluid", surface = surface_id)
                if data["formulation"] == "circular_hole":
                    a, b, c, Z_0 = self.get_transfer_impedance_for_circular_holes(omega, fluid, data)

                else:
                    continue

                self.perforated_plate_impedance_data[surface_id] = {   
                                                                    "formulation" : data["formulation"],
                                                                    "a" : a,
                                                                    "b" : b,
                                                                    "c" : c,
                                                                    "Z_0" : Z_0,
                                                                    }

    def get_transfer_impedance_for_circular_holes(self, omega: np.ndarray, fluid: Fluid, pp_data: dict, **kwargs):
        """
        """

        t_p = pp_data.get("plate_thickness", 0)
        sigma = pp_data.get("porosity", 0)
        a = pp_data.get("hole_diameter", 0) / 2
        Cd_lin = pp_data.get("linear_discharge_coefficient", 1)
        Cd_nl = pp_data.get("non_linear_discharge_coefficient", 0.76)

        rho_0 = fluid.fluid_density
        c_0 = fluid.speed_of_sound
        mu_0 = fluid.dynamic_viscosity
        gamma = fluid.isentropic_exponent
        Cp = fluid.specific_heat_Cp
        k_t = fluid.thermal_conductivity

        Z_0 = rho_0*c_0
        Pr = mu_0 * Cp / k_t

        G_rho = a * np.sqrt(-1j * omega * rho_0 / mu_0)
        G_bulk = a * np.sqrt(-1j * omega * rho_0 * Pr / mu_0)

        x = np.sqrt(sigma)
        Phi = 1 - 1.41*x + 0.34*(x**3) + 0.07*(x**5) - 0.02*(x**6) + 0.03*(x**7) - 0.016*(x**8)

        Gamma_v = (1 - (2*jv(1, G_rho)) / (((G_rho) * jv(0, G_rho))))
        Gamma_th = (1 - (2*jv(1, G_bulk)) / (((G_bulk) * jv(0, G_bulk))))

        delta = (8*a) / (3*np.pi)
        k_c = (omega / c_0) * ((Gamma_th / Gamma_v)**(1/2))

        a = -(2 * 1j) * np.sin(k_c * t_p / 2) / (((gamma - (gamma-1) * Gamma_th) * Gamma_v)**(1/2))
        b = -(2 * delta * Phi * omega * 1j) / (c_0 * sigma * Cd_lin * Gamma_v)
        c = (1 - sigma**2) / (2 * c_0 * ((sigma * Cd_nl)**2))

        return a, b, c, Z_0