
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
            property, surface_ids = key
            if property == "perforated_plate_model":
                if data["formulation"] == "circular_hole":

                    normalized_impedances = self.get_transfer_impedance_for_circular_holes(omega, data)
                    if normalized_impedances is None:
                        continue
                
                    z_orifice, z_end, z_nl_urms, z_ud, Z_0 = normalized_impedances

                else:
                    continue

                self.perforated_plate_impedance_data[surface_ids] = {   
                                                                     "formulation" : data["formulation"],
                                                                     "z_orifice" : z_orifice,
                                                                     "z_end" : z_end,
                                                                     "z_nl_urms" : z_nl_urms,
                                                                     "z_ud" : z_ud,
                                                                     "Z_0" : Z_0,
                                                                     }

    def get_transfer_impedance_for_circular_holes(self, omega: np.ndarray, pp_data: dict, **kwargs):
        """
        """

        t_p = pp_data.get("plate_thickness", 0)
        sigma = pp_data.get("porosity", 0)
        a = pp_data.get("hole_diameter", 0) / 2
        Cd_lin = pp_data.get("linear_discharge_coefficient", 1)
        Cd_nl = pp_data.get("non_linear_discharge_coefficient", 0.76)
        f_nl = pp_data.get("non_linear_correction_factor", 0)

        pp_fluid = pp_data.get("fluid_data")
        if not isinstance(pp_fluid, dict):
            return None

        rho_0 = pp_fluid.get("fluid_density")
        c_0 = pp_fluid.get("speed_of_sound")
        mu_0 = pp_fluid.get("dynamic_viscosity")
        gamma = pp_fluid.get("isentropic_exponent")
        Cp = pp_fluid.get("specific_heat_Cp")
        k_t = pp_fluid.get("thermal_conductivity")

        Z_0 = rho_0 * c_0
        Pr = mu_0 * Cp / k_t

        # viscous wave number
        k_v = a * np.sqrt(-1j * omega * rho_0 / mu_0)
        
        # thermal wave number
        k_th = a * np.sqrt(-1j * omega * rho_0 * Pr / mu_0)

        # viscous function for circular holes
        Gamma_v = jv(2, k_v) / jv(0, k_v)
        
        # thermal function for circular holes
        Gamma_th = jv(2, k_th) / jv(0, k_th)

        # complex wave number
        k_c = (omega / c_0) * ((gamma - (gamma-1)*Gamma_th) / Gamma_v)**(1/2)

        # normalized transfer impedance
        z_c = 1 / ((gamma - (gamma-1)*Gamma_th) * Gamma_v)**(1/2)

        # normalized orifice transfer impedance
        z_orifice = -1j * 2 * z_c * np.sin(k_c * t_p / 2) / (sigma * Cd_lin)
        # z_orifice = -1j * omega * t_p / (c_0 * sigma * Cd_lin * Gamma_v)

        # end correction - equivalent piston
        delta = (8*a) / (3*np.pi)

        # hole interation - Fok's function
        x = np.sqrt(sigma)
        Phi = 1 - 1.41*x + 0.34*(x**3) + 0.07*(x**5) - 0.02*(x**6) + 0.03*(x**7) - 0.016*(x**8)
        # Phi = 1 - 1.4092*x + 0.33818*(x**3) + 0.0679*(x**5) - 0.02287*(x**6) + 0.03015*(x**7) - 0.01641*(x**8)

        # normalized transfer impedance to account for the end effects
        z_end =  -1j * (2 * delta * Phi * omega) / (c_0 * sigma * Cd_lin * Gamma_v)

        # normalized tranfer impedance to account non-linear and mean flow effects
        z_nl_urms = ((1 - sigma**2) * f_nl) / (2 * c_0 * ((sigma * Cd_nl)**2))

        # user-defined normalized transfer impedance
        z_ud = 0.
        if "table_names" in pp_data.keys():
            values = pp_data.get("values")[0]
            if isinstance(values, list) and len(values) == 1:
                z_ud = values[0]

        return (z_orifice, z_end, z_nl_urms, z_ud, Z_0)