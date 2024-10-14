from vibra import app

import numpy as np
# import matplotlib.pyplot as plt

# fmt: off

class PorousMaterialModels:

    def __init__(self, model):
        super().__init__()

        self.model = model
        self.properties = model.properties

        self.model_data_for_DB = None
        self.model_data_for_DBM = None

        self.porous_material_model = dict()

    def set_external_model(self, model):
        self.external_model = model

    def process_effective_properties(self, frequencies):

        self.porous_material_model = dict()
        if frequencies[0] == 0:
            freq = frequencies[1:]
        else:
            freq = frequencies

        omega = 2 * np.pi * freq

        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "porous_material_model":

                # surfaces_from_volume = self.project.model.mesh.surfaces_from_volumes[volume_id]
                fluid = self.properties.get_fluid(volume = volume_id)

                if data["model"] in ["Delany-Bazley", "Delany-Bazley-Miki"]:
                    rho_eff, C_eff = self.get_Delany_Bazley_Miki_effective_properties(omega, fluid, data)

                elif data["model"] == "Jhonson-Champoux-Allard":
                    rho_eff, C_eff = self.get_JCA_effective_properties(omega, fluid, data)

                elif data["model"] == "Jhonson-Champoux-Allard-Lafarge":
                    rho_eff, C_eff = self.get_JCAL_effective_properties(omega, fluid, data)

                else:
                    continue

                self.porous_material_model[volume_id] = {   
                                                         "model" : data["model"],
                                                         "rho_eff" : rho_eff,
                                                         "C_eff" : C_eff   
                                                         }

                # data = np.array([np.arange(len(C_eff)), C_eff])
                # np.savetxt("complex_sound.dat", data.T, delimiter=";")

    def get_Delany_Bazley_Miki_effective_properties(self, omega, fluid, data):

        """ This method returns the Delany-Bazley or Delany-Bazley-Miki porous
            material model effective properties.
        """

        C1 = data["C1"]
        C2 = data["C2"]
        C3 = data["C3"]
        C4 = data["C4"]
        C5 = data["C5"]
        C6 = data["C6"]
        C7 = data["C7"]
        C8 = data["C8"]

        flow_resistivity = data["flow_resistivity"]

        C_0 = fluid.speed_of_sound
        rho_0 = fluid.fluid_density

        frequencies = omega / (2 * np.pi)
        X = frequencies / flow_resistivity

        Z_eff = (rho_0 * C_0) * ( 1 + C1*(X**C2) - 1j*(C3*(X**C4)) )
        k_eff = (-1j) * (omega / C_0) * ( C5*(X**C6) + 1j*(1 + C7*(X**C8)) )

        C_eff = omega / k_eff
        rho_eff = Z_eff / C_eff

        return rho_eff, C_eff

    def get_JCA_effective_properties(self, omega, fluid, data):

        """ This method returns the Jhonson-Champoux-Allard porous material model
            effective properties.
        """

        por = data["porosity"]
        tor = data["tortuosity"]
        Lv = data["viscous_characteristic_length"]
        Lt = data["thermal_characteristic_length"]
        Rf = data["flow_resistivity"]

        P_0 = fluid.pressure
        rho_0 = fluid.fluid_density
        C_0 = fluid.speed_of_sound
        gamma = fluid.isentropic_exponent
        Cp = fluid.specific_heat_Cp
        mu = fluid.dynamic_viscosity
        k_t = fluid.thermal_conductivity
        Pr = mu * Cp / k_t

        # Effective density - visco-inertial effects
        rho_eff = ((rho_0 * tor) / por) * (1 + ((Rf * por) / (1j * omega * rho_0 * tor)) * np.sqrt(1 + 1j * ((4 * omega * (tor**2) * mu * rho_0) / ((por * Lv * Rf)**2))))

        # Thermal effects
        K_eff = ((P_0 * gamma) / por) / (gamma - (gamma - 1) * ((1 + ((8 * mu) / (1j * omega* rho_0 * Pr * Lt**2)) * np.sqrt(1 + (1j * omega * rho_0 * Pr * Lt**2) / (16 * mu)))**-1))

        # Complex speed of sound
        C_eff = np.sqrt(K_eff / rho_eff)

        # # Impedância característica complexa do material poroso
        # Z_cr = np.sqrt(rho_eff * K_eff)       

        # # Impedância de superfície complexa do material poroso
        # Z_sr = -1j * (Z_cr) * np.cot(k_cr * h)

        # # Coeficiente de reflexão do material rígido
        # R_r = (Z_sr - Z_0) / (Z_sr + Z_0)

        # # Coeficiente de absorção sonora
        # alpha_r = 1 - np.abs(R_r)**2

        return rho_eff, C_eff

    def get_JCAL_effective_properties(self, omega, fluid, data):

        """ This method returns the Jhonson-Champoux-Allard-Lafarge porous material model
            effective properties.
        """

        por = data["porosity"]
        tor = data["tortuosity"]
        Lv = data["viscous_characteristic_length"]
        Lt = data["thermal_characteristic_length"]
        Rf = data["flow_resistivity"]

        P_0 = fluid.pressure
        rho_0 = fluid.fluid_density
        C_0 = fluid.speed_of_sound
        Z_0 = rho_0 * C_0
        gamma = fluid.isentropic_exponent
        Cp = fluid.specific_heat_Cp
        mu = fluid.dynamic_viscosity
        k_t = fluid.thermal_conductivity

        q_viscous = mu / Rf
        q_thermal = q_viscous * tor

        # Effective density - visco-inertial effects
        rho_eff = ((tor * rho_0) / por) * (1 + ((Rf * por) / (1j * omega * rho_0 * tor)) * np.sqrt(1 + ((1j * 4 * tor**2 * mu * rho_0 * omega) / (Rf**2 * Lv**2 * por**2))))

        # Thermal effects
        K_eff = ((gamma * P_0) / por) / (gamma - (gamma - 1) * (1 - 1j * ((por * k_t) / (omega * Cp * q_thermal * rho_0)) * np.sqrt(1 + ((1j * 4 * omega * Cp * rho_0 * q_thermal**2) / (por**2 * k_t * Lt**2))))**-1)

        # Complex speed of sound
        C_eff = np.sqrt(K_eff / rho_eff)

        # # Impedância característica complexa do material poroso
        # Z_cr = np.sqrt(rho_eff * K_eff)

        # # Número de onda complexa no material poroso
        # k_cr = omega / C_eff

        # # Impedância de superfície complexa do material poroso
        # Z_sr = -1j * (Z_cr) * np.cot(k_cr * h)

        # # Coeficiente de reflexão do material rígido
        # R_r = (Z_sr - Z_0) / (Z_sr + Z_0)

        # # Coeficiente de absorção sonora
        # alpha_r = 1 - np.abs(R_r)**2

        return rho_eff, C_eff

# fmt: on