
from vibra.engine.properties.fluid import Fluid

import numpy as np
from scipy.special import jv

class PerforatedPlate:
    def __init__(self, **kwargs):
        self.plate_thickness = kwargs.get("plate_thickness", 0)
        self.porosity = kwargs.get("porosity", 0)
        self.hole_diameter = kwargs.get("hole_diameter", 0)
        self.discharge_coefficient = kwargs.get("discharge_coefficient", 0.76)
        self.cavity_thickness = kwargs.get("cavity_thickness", 0)
        # self.fluid = kwargs.get("fluid")

    def get_transfer_impedance_for_circular_holes(self, fluid: Fluid, omega: np.ndarray, U_rms=0, **kwargs):

        t_p = self.plate_thickness
        sigma = self.porosity
        a = self.hole_diameter / 2
        C_d = self.discharge_coefficient

        rho_0 = fluid.fluid_density
        c_0 = fluid.fluid_density
        mu_0 = fluid.dynamic_viscosity

        x = (sigma)**(1/2)
        k_s = 1j * rho_0 * omega / mu_0
        Phi = 1 - 1.41*x + 0.34*(x**3) + 0.07*(x**5) - 0.02*(x**6) + 0.03*(x**7) - 0.016*(x**8)
        Z_trans_n = (t_p + (16*a*Phi / (3*np.pi))) * ((1j*omega) / ((c_0*sigma)*(1 - (2*jv(1, k_s * a)) / ((k_s*a*jv(0, k_s*a))))))
        Z_trans_n += 1.2 * (1 - sigma**2) * U_rms / (2 * c_0 * ((sigma * C_d)**2))

        return Z_trans_n * (rho_0 * c_0)