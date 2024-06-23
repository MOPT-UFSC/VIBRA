from vibra import app

import numpy as np

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

    def process_equivalent_properties(self, frequencies):

        self.porous_material_model = dict()
        if frequencies[0] == 0:
            freq = frequencies[1:]
        else:
            freq = frequencies

        omega = 2 * np.pi * freq    

        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "porous_material_model":

                surfaces_from_volume = self.project.model.mesh.surfaces_from_volumes[volume_id]

                fluid = self.properties.get_fluid(volume = volume_id)

                if data["model"] in ["Delany-Bazley", "Delany-Bazley-Miki"]:
                    rho_eq, C_eq = self.get_Delany_Bazley_equivalent_properties(omega, fluid, data)

                elif data["model"] == "Jhonson-Champoux-Allard":
                    rho_eq, C_eq = self.get_JCA_equivalent_properties(omega, fluid, data)

                elif data["model"] == "Jhonson-Champoux-Allard":
                    rho_eq, C_eq = self.get_JCAL_equivalent_properties(omega, fluid, data)

                self.porous_material_model[volume_id] = {   "model" : data["model"],
                                                            "surfaces_from_volume" : surfaces_from_volume,
                                                            "rho_eq" : rho_eq,
                                                            "C_eq" : C_eq   
                                                        }

    def get_Delany_Bazley_equivalent_properties(self, omega, fluid, data):

        """ This method returns the Delany-Bazley porous material model
            equivalent properties.
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
        # print(data)

        C_0 = fluid.speed_of_sound
        rho_0 = fluid.fluid_density

        frequencies = omega / (2 * np.pi)
        X = frequencies / flow_resistivity

        Z_eq = (rho_0 * C_0) * ( 1 + C1*(X**C2) - 1j*(C3*(X**C4)) )
        k_eq = (omega / C_0) * ( C5*(X**C6) + 1j*(1 + C7*(X**C8)) )

        C_eq = omega / k_eq
        rho_eq = Z_eq / C_eq

        # print(C_eq)
        # print(rho_eq)

        return rho_eq, C_eq

    def get_JCA_equivalent_properties(self, omega, fluid, data):

        """ This method returns the Jhonson-Champoux-Allard porous material model
            equivalent properties.
        """

        porosity = data["porosity"]
        tortuosity = data["tortuosity"]
        ctl = data["characteristic_thermal_length"]
        cvl = data["characteristic_viscous_length"]
        h = data["porous_material_length"]
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
        rho_eq = ((tortuosity * rho_0) / porosity) * (1 + ((flow_resistivity * porosity) / (1j * omega * rho_0 * tortuosity)) * np.sqrt(1 + ((1j * 4 * tortuosity**2 * mu * rho_0 * omega) / (flow_resistivity**2 * cvl**2 * porosity**2))))

        # Módulo de compressibilidade efetivo que descreve as perdas térmicas
        K_eq = ((gamma * P_0) / porosity) / (gamma - (gamma - 1) * (1 + (8 * k_t) / (1j * omega * Cp * ctl**2 * rho_0) * np.sqrt(1 + (1j * omega * Cp * rho_0 * ctl**2) / (16 * k_t)))**-1)

        # Impedância característica complexa do material poroso
        Z_cr = np.sqrt(rho_eq * K_eq)

        # Velocidade do som complexa no material poroso
        C_eq = np.sqrt(K_eq / rho_eq)

        # Número de onda complexa no material poroso
        k_cr = omega / C_eq

        # Impedância de superfície complexa do material poroso
        Z_sr = -1j * (Z_cr) * np.cot(k_cr * h)

        # Coeficiente de reflexão do material rígido
        R_r = (Z_sr - Z_0) / (Z_sr + Z_0)

        # Coeficiente de absorção sonora
        alpha_r = 1 - np.abs(R_r)**2

        return rho_eq, C_eq

    def get_JCAL_equivalent_properties(self, omega, fluid, data):

        """ This method returns the Jhonson-Champoux-Allard-Lafarge porous material model
            equivalent properties.
        """

        porosity = data["porosity"]
        tortuosity = data["tortuosity"]
        ctl = data["characteristic_thermal_length"]
        cvl = data["characteristic_viscous_length"]
        h = data["porous_material_length"]
        # rho_f = data["fibrous_material_density"]
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
        rho_eq = ((tortuosity * rho_0) / porosity) * (1 + ((flow_resistivity * porosity) / (1j * omega * rho_0 * tortuosity)) * np.sqrt(1 + ((1j * 4 * tortuosity**2 * mu * rho_0 * omega) / (flow_resistivity**2 * cvl**2 * porosity**2))))

        # Módulo de compressibilidade efetivo que descreve as perdas térmicas
        # K_eq = ((gamma * P_0) / porosity) / (gamma - (gamma - 1) * (1 + (8 * k_t) / (1j * omega * Cp * ctl**2 * rho_0) * np.sqrt(1 + (1j * omega * Cp * rho_0 * ctl**2) / (16 * k_t)))**-1)
        K_eq = ((gamma * P_0) / porosity) / (gamma - (gamma - 1) * (1 - 1j * ((porosity * k_t) / (omega * Cp * q_thermal * rho_0)) * np.sqrt(1 + ((1j * 4 * omega * Cp * rho_0 * q_thermal**2) / (porosity**2 * k_t * ctl**2))))**-1)

        # Impedância característica complexa do material poroso
        Z_cr = np.sqrt(rho_eq * K_eq)

        # Velocidade do som complexa no material poroso
        C_eq = np.sqrt(K_eq / rho_eq)

        # Número de onda complexa no material poroso
        k_cr = omega / C_eq

        # Impedância de superfície complexa do material poroso
        Z_sr = -1j * (Z_cr) * np.cot(k_cr * h)

        # Coeficiente de reflexão do material rígido
        R_r = (Z_sr - Z_0) / (Z_sr + Z_0)

        # Coeficiente de absorção sonora
        alpha_r = 1 - np.abs(R_r)**2

        return rho_eq, C_eq