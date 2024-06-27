from vibra import app

import numpy as np
import matplotlib.pyplot as plt

class PorousMaterialModels:

    def __init__(self):
        super().__init__()

        self.project = app().main_window.project
        self.properties = self.project.model.properties

        self.model_data_for_DB = None
        self.model_data_for_DBM = None

        self.porous_material_model = dict()

    def set_Delany_Bazley_data(self, data):
        self.model_data_for_DB = data

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

                self.porous_material_model[volume_id] = {   "model" : data["model"],
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

        # aux = np.ones_like(Z_eff, dtype=complex)
        # C_eff = C_0*aux
        # rho_eff = rho_0*aux

        # print(rho_eff)
        # print(C_eff)

        return rho_eff, C_eff

    def get_JCA_effective_properties(self, omega, fluid, data):

        """ This method returns the Jhonson-Champoux-Allard porous material model
            effective properties.
        """

        porosity = data["porosity"]
        tortuosity = data["tortuosity"]
        tcl = data["thermal_characteristic_length"]
        vcl = data["viscous_characteristic_length"]
        flow_resistivity = data["flow_resistivity"]

        P_0 = fluid.pressure
        rho_0 = fluid.fluid_density
        C_0 = fluid.speed_of_sound
        Z_0 = rho_0 * C_0
        gamma = fluid.isentropic_exponent
        Cp = fluid.specific_heat_Cp
        mu = fluid.dynamic_viscosity
        k_t = fluid.thermal_conductivity

        # Densidade complexa que descreve as perdas viscosas
        rho_eff = ((rho_0 * tortuosity) / porosity) * (1 + ((flow_resistivity * porosity) / (1j * omega * rho_0 * tortuosity)) * np.sqrt(1 + ((1j * 4 * (tortuosity**2) * mu * omega* rho_0) / ((porosity * vcl * flow_resistivity)**2))))

        # Módulo de compressibilidade efetivo que descreve as perdas térmicas
        K_eff = ((P_0 * gamma) / porosity) / (gamma - (gamma - 1) * ((1 + ((8 * k_t) / (1j * omega* rho_0 * Cp * tcl**2)) * np.sqrt(1 + (1j * omega * Cp * rho_0 * tcl**2) / (16 * k_t)))**-1))

        # # Impedância característica complexa do material poroso
        # Z_cr = np.sqrt(rho_eff * K_eff)

        # Velocidade do som complexa no material poroso
        C_eff = np.sqrt(K_eff / rho_eff)

        # # Número de onda complexa no material poroso
        # k_cr = omega / C_eff

        # # Impedância de superfície complexa do material poroso
        # Z_sr = -1j * (Z_cr) * np.cot(k_cr * h)

        # # Coeficiente de reflexão do material rígido
        # R_r = (Z_sr - Z_0) / (Z_sr + Z_0)

        # # Coeficiente de absorção sonora
        # alpha_r = 1 - np.abs(R_r)**2

        print(rho_eff)
        print(C_eff)
        # return

        return rho_eff, C_eff

    def get_JCAL_effective_properties(self, omega, fluid, data):

        """ This method returns the Jhonson-Champoux-Allard-Lafarge porous material model
            effective properties.
        """

        porosity = data["porosity"]
        tortuosity = data["tortuosity"]
        tcl = data["thermal_characteristic_length"]
        vcl = data["viscous_characteristic_length"]
        flow_resistivity = data["flow_resistivity"]

        q_viscous = mu / flow_resistivity
        q_thermal = q_viscous * tortuosity

        P_0 = fluid.pressure
        rho_0 = fluid.fluid_density
        C_0 = fluid.speed_of_sound
        Z_0 = rho_0 * C_0
        gamma = fluid.isentropic_exponent
        Cp = fluid.specific_heat_Cp
        mu = fluid.dynamic_viscosity
        k_t = fluid.thermal_conductivity

        # Densidade complexa que descreve as perdas viscosas
        rho_eff = ((tortuosity * rho_0) / porosity) * (1 + ((flow_resistivity * porosity) / (1j * omega * rho_0 * tortuosity)) * np.sqrt(1 + ((1j * 4 * tortuosity**2 * mu * rho_0 * omega) / (flow_resistivity**2 * vcl**2 * porosity**2))))

        # Módulo de compressibilidade efetivo que descreve as perdas térmicas
        K_eff = ((gamma * P_0) / porosity) / (gamma - (gamma - 1) * (1 - 1j * ((porosity * k_t) / (omega * Cp * q_thermal * rho_0)) * np.sqrt(1 + ((1j * 4 * omega * Cp * rho_0 * q_thermal**2) / (porosity**2 * k_t * tcl**2))))**-1)

        # # Impedância característica complexa do material poroso
        # Z_cr = np.sqrt(rho_eff * K_eff)

        # Velocidade do som complexa no material poroso
        C_eff = np.sqrt(K_eff / rho_eff)

        # # Número de onda complexa no material poroso
        # k_cr = omega / C_eff

        # # Impedância de superfície complexa do material poroso
        # Z_sr = -1j * (Z_cr) * np.cot(k_cr * h)

        # # Coeficiente de reflexão do material rígido
        # R_r = (Z_sr - Z_0) / (Z_sr + Z_0)

        # # Coeficiente de absorção sonora
        # alpha_r = 1 - np.abs(R_r)**2

        return rho_eff, C_eff