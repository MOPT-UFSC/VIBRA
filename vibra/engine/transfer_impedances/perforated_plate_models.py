
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

    def process_acoustic_transfer_impedances(self, frequencies: np.ndarray, solution: np.ndarray | None = None):

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
                    a, b, Z_0 = self.get_transfer_impedance_for_circular_holes(omega, fluid, data, solution)

                else:
                    continue

                self.perforated_plate_impedance_data[surface_id] = {   
                                                                    "formulation" : data["formulation"],
                                                                    "a" : a,
                                                                    "b" : b,
                                                                    "Z_0" : Z_0,
                                                                    }

    def get_transfer_impedance_for_circular_holes(self, omega: np.ndarray, fluid: Fluid, pp_data: dict, solution: np.ndarray | None, **kwargs):

        t_p = pp_data.get("plate_thickness", 0)
        sigma = pp_data.get("porosity", 0)
        a = pp_data.get("hole_diameter", 0) / 2
        C_d = pp_data.get("discharge_coefficient", 0.76)

        rho_0 = fluid.fluid_density
        c_0 = fluid.speed_of_sound
        mu_0 = fluid.dynamic_viscosity

        x = np.sqrt(sigma)
        k_s = np.sqrt(-1j * rho_0 * omega / mu_0)
        Phi = 1 - 1.41*x + 0.34*(x**3) + 0.07*(x**5) - 0.02*(x**6) + 0.03*(x**7) - 0.016*(x**8)

        a = (t_p + ((16*a*Phi) / (3*np.pi))) * ((1j*omega) / ((c_0*sigma) * (1 - (2*jv(1, k_s*a)) / (((k_s*a) * jv(0, k_s*a))))))
        b = 1.2 * (1 - sigma**2) / (2*c_0*((sigma*C_d)**2))
        Z_0 = rho_0*c_0

        return a, b, Z_0