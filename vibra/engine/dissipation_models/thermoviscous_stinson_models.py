from vibra import app
from vibra.interface.loading_bar import load_function

import numpy as np
from scipy.special import jv
# import matplotlib.pyplot as plt

# fmt: off

class ThermoviscousStinsonModels:

    def __init__(self, model):
        super().__init__()

        self.model = model
        self.properties = model.properties

        self.thermoviscous_stinson_model = dict()

    def set_external_model(self, model):
        self.external_model = model

    def process_effective_properties(self, frequencies):

        self.thermoviscous_stinson_model = dict()
        if frequencies[0] == 0:
            freq = frequencies[1:]
        else:
            freq = frequencies

        omega = 2 * np.pi * freq

        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "thermoviscous_stinson_model":

                # surfaces_from_volume = self.project.model.mesh.surfaces_from_volumes[volume_id]
                fluid = self.properties.get_fluid(volume = volume_id)

                if data["section_type"] in ["Rectangular duct", "Quadrangular duct"]:
                    rho_eff, C_eff = self.get_rectangular_section_effective_properties(omega, fluid, data)

                if data["section_type"] in ["Slit duct"]:
                    rho_eff, C_eff = self.get_rectangular_slit_section_effective_properties(omega, fluid, data)

                elif data["section_type"] in ["Circular duct"]:
                    rho_eff, C_eff = self.get_circular_section_effective_properties(omega, fluid, data)

                else:
                    continue

                self.thermoviscous_stinson_model[volume_id] = {   
                                                                "section_type" : data["section_type"],
                                                                "rho_eff" : rho_eff,
                                                                "C_eff" : C_eff   
                                                               }

                # data = np.array([np.arange(len(C_eff)), C_eff])
                # np.savetxt("complex_sound.dat", data.T, delimiter=";")


    def get_rectangular_section_effective_properties(self, omega, fluid, data):

        C_0 = fluid.speed_of_sound
        rho_0 = fluid.fluid_density

        k = omega / C_0

        P_0 = fluid.pressure
        rho_0 = fluid.fluid_density
        C_0 = fluid.speed_of_sound
        gamma = fluid.isentropic_exponent
        Cp = fluid.specific_heat_Cp
        mu = fluid.dynamic_viscosity
        k_t = fluid.thermal_conductivity
        k_0 = gamma * P_0
        Pr = mu * Cp / k_t

        width = data["width"]
        height = data["height"]
        area = width * height

        # EQUAÇÕES DOS DUTOS DE SEÇÃO RETANGULAR E/OU QUADRADA
        Y1 = np.arange(0, 501)        # contador da série ajustado para até 501
        Y2 = np.arange(0, 501)        # contador da série ajustado para até 501
        akn = (Y1 + 0.5)*(np.pi / width)    # constante para os modos no duto
        bmn = (Y2 + 0.5)*(np.pi / height)    # constante para os modos no duto
        
        SUM_d_n = np.zeros(len(omega), dtype=complex)
        SUM_k_n = np.zeros(len(omega), dtype=complex)

        for i, w in enumerate(omega):
            SUM_d_n[i] = sum(1/((akn**2)*bmn**2*(akn**2+bmn**2 - 1j*w*rho_0/mu)))
            SUM_k_n[i] = sum(1/((akn**2)*bmn**2*(akn**2+bmn**2 - 1j*w*Pr*rho_0/mu)))

        # Effective complex density (thermoviscous losses in duct)
        rho_eff = (-mu*((width)**2)*((height)**2)) / (4 * 1j * omega * SUM_d_n)

        # Effective complex bulk modulus (thermoviscous losses in duct)
        K_eff = (mu*k_0*((width)**2)*((height)**2)) / (gamma*mu*((width)**2)*((height)**2) + 4 * 1j * (gamma-1) * Pr * rho_0 * omega * SUM_k_n)

        # Complex speed of sound
        C_eff = np.sqrt(K_eff / rho_eff)

        # # Complex wave number of duct
        # kc = omega*np.sqrt(rho_eff / K_eff)

        # # characteristic acoustic impedance of duct
        # Zc = np.sqrt(K_eff * rho_eff) / area

        return rho_eff, C_eff


    def get_rectangular_slit_section_effective_properties(self, omega, fluid, data):

        C_0 = fluid.speed_of_sound
        rho_0 = fluid.fluid_density

        k = omega / C_0

        P_0 = fluid.pressure
        rho_0 = fluid.fluid_density
        C_0 = fluid.speed_of_sound
        gamma = fluid.isentropic_exponent
        Cp = fluid.specific_heat_Cp
        mu = fluid.dynamic_viscosity
        k_t = fluid.thermal_conductivity
        k_0 = gamma * P_0
        Pr = mu * Cp / k_t

        width = data["width"]
        height = data["height"]
        area = width * height

        # EQUAÇÕES DOS DUTOS TIPO FENDA
        Gp = np.sqrt(1j * omega * rho_0 / mu)
        Gk = np.sqrt(1j * omega * rho_0 * Pr / mu)

        # Effective complex density (thermoviscous losses in slit duct)
        rho_eff = rho_0 * (1/(1-(np.tanh(height/2*Gp) / (height/2*Gp))))

        # Effective complex bulk modulus (thermoviscous losses in slit duct)
        K_eff = k_0*(1/(1+(gamma-1)*(np.tanh(height/2*Gk)/(height/2*Gk))))

        # Effective complex speed of sound
        C_eff = np.sqrt(K_eff / rho_eff)
        # C_eff = np.real(np.sqrt(K_eff / rho_eff))

        # # Complex wave number of duct
        # kc = omega*np.sqrt(rho_eff / K_eff)

        # # characteristic acoustic impedance of duct
        # Zc = np.sqrt(K_eff * rho_eff) / area

        return rho_eff, C_eff


    def get_circular_section_effective_properties(self, omega, fluid, data):

            C_0 = fluid.speed_of_sound
            rho_0 = fluid.fluid_density

            k = omega / C_0

            P_0 = fluid.pressure
            rho_0 = fluid.fluid_density
            C_0 = fluid.speed_of_sound
            gamma = fluid.isentropic_exponent
            Cp = fluid.specific_heat_Cp
            mu = fluid.dynamic_viscosity
            k_t = fluid.thermal_conductivity
            k_0 = gamma * P_0
            Pr = mu * Cp / k_t

            diameter = data["diameter"]
            # length = data["length"]
            radius = diameter / 2
            area = np.pi * (diameter**2) / 4

            # Effective complex density (thermoviscous losses in duct)
            rho_eff = rho_0*(1-2*1j*(radius*np.sqrt(1j*omega*rho_0/mu))**-1*(jv(1, 1j*radius*np.sqrt(1j*omega*rho_0/mu))/jv(0, 1j*radius*np.sqrt(1j*omega*rho_0/mu))))**-1

            # Effective complex bulk modulus (thermoviscous losses in duct)
            K_eff = k_0*(1 + 2*1j*(gamma-1)*(radius*np.sqrt(1j*omega*rho_0*Pr/mu))**-1*(jv(1, 1j*radius*np.sqrt(1j*omega*rho_0*Pr/mu))/jv(0, 1j*radius*np.sqrt(1j*omega*rho_0*Pr/mu))))**-1
            
            # Effective complex speed of sound
            C_eff = np.sqrt(K_eff / rho_eff)
            # C_eff = np.real(np.sqrt(K_eff / rho_eff))

            # # Complex wave number of duct
            # kc = omega*np.sqrt(rho_eff / K_eff)

            # # characteristic acoustic impedance of duct
            # Zc = np.sqrt(K_eff * rho_eff) / area

            return rho_eff, C_eff


# ############### Modelo de Stinson de perdas visco-térmicas para dutos de seção transversal retangular e/ou quadrada ######
# # Stinson, M. R., The propagation of plane sound waves in narrow and wide circular tubes, and generalization to uniform tubes of arbitrary cross-sectional shape. The Journal of the Acoustical Society of America, 1991.
# # Outra referência a ser consultada Wei, S.; Li, L.; Zhigang, C.; Linyong, L.; Xiaopeng, F., A parameter design method for multifrequency perfect sound-absorbing metasurface with critical coupled Helmholtz resonator. Journal of low frequency noise, vibration and active control, 2021.


# # PARÂMETROS TERMOACÚSTICOS
# T_amb = 20                     # temperatura do ambiente [°C]
# T = 273.15+T_amb               # temperatura do meio em Kelvin [K]
# F = np.arange(1, 4001)         # vetor de frequência em [Hz]
# co = 331.0+0.6*T_amb           # velocidade do som no ar [m/s] a 20 graus
# eta = 1.8134e-5                # coef. de viscosi. dinâmica do ar [N.s/m^2] ou [Pa.s]
# po = 1.21                      # densidade do ar [kg/m^3] a 20^o [C] e pressão de 1atm
# k_f = 0.026                    # condutividade térmica [W/mK]
# m_molar = 28.965               # massa molar [kg/K.mol]
# R_a = 287.05                   # constante específica do gás [J/kg.K]
# c_epx = 0.0034                 # coeficiente de expansão térmica do gás [1/K]
# C_p = 1007                     # calor específico a pressão constante [J/kgK]
# gamma = 1.410                  # razão de calor específico do ar [-]
# C_v = C_p/gamma                # calor específico a volume constante [J/kgK]
# Pr = 0.71                      # número de Prandtl [-]
# Po = 101325                    # pressão atmosférica [N/m^2] ou [Pa]
# nu = eta / po                  # viscosidade cinemática do ar [m^2/s]
# nu_1 = k_f/(po*C_v)            # constante [m^3.K/J]
# Zo = po*co                     # impedância do meio {Rayls}
# ko = gamma*Po                  # módulo de compressibilidade na condição adiabática [Pa]

# # PARÂMETROS GEOMÉTRICOS DA ÁREA DE SEÇÃO TRANSVERSAL DO DUTO RETANGULAR E/OU QUADRADA
# a = 13e-3                      # largura da seção transversal [m]
# b = 1.8e-3                     # altura da seção transversal [m]
# Lef = 50e-3                    # comprimento do duto [m]
# S = a*b                        # área de seção transv. do duto [m^2]

# #VETORES DE VALORES#
# pt_v = np.empty(0)
# kt_v = np.empty(0)
# kc_v = np.empty(0)
# Zef_v = np.empty(0)
# cp_v = np.empty(0)
# w_v = np.empty(0)
# kef_v = np.empty(0)

# for f in F:
#     w = 2*np.pi*f                # frequência angular [rad/s]
#     w_v = np.append(w_v, w)     
#     k = w/co                     # vetor de onda [rad/m]

# # EQUAÇÕES DOS DUTOS DE SEÇÃO RETANGULAR E/OU QUADRADA
#     Y1 = np.arange(0, 501)        # contador da série ajustado para até 501
#     Y2 = np.arange(0, 501)        # contador da série ajustado para até 501
#     akn = (Y1+(0.5))*(np.pi/a)    # constante para os modos no duto
#     bmn = (Y2+(0.5))*(np.pi/b)    # constante para os modos no duto
    
#     SUM_d_n = 0
#     SUM_k_n = 0

#     for s in range(0, len(Y1)):
#         SUM_d_n += ((akn[s]**2)*bmn[s]**2*(akn[s]**2+bmn[s]**2-1j*w*po/eta))**-1
#         SUM_k_n += ((akn[s]**2)*bmn[s]**2*(akn[s]**2+bmn[s]**2-1j*w*Pr*po/eta))**-1

#     pt = (-eta*((a)**2)*((b)**2))/(4*1j*w*SUM_d_n)                                                # densidade efetiva complexa (perdas viscosas no duto)
#     pt_v = np.append(pt_v, pt)
#     kt = (eta*ko*((a)**2)*((b)**2))/(gamma*eta*((a)**2)*((b)**2)+4*1j*(gamma-1)*Pr*po*w*SUM_k_n)  # bulk modulus efetivo complexo (perdas térmicas no duto)
#     kt_v = np.append(kt_v, kt)
#     kc = w*np.sqrt(pt/kt)       # número de onda complexo no duto
#     kc_v = np.append(kc_v, kc)
#     Zc = np.sqrt(kt*pt)/(S)     # impedância característica complexa no duto




# ############### Modelo de Stinson de perdas visco-térmicas para dutos de seção tipo fenda ######
# # Stinson, M. R., The propagation of plane sound waves in narrow and wide circular tubes, and generalization to uniform tubes of arbitrary cross-sectional shape. The Journal of the Acoustical Society of America, 1991.


# # PARÂMETROS TERMOACÚSTICOS
# T_amb = 20                     # temperatura do ambiente [°C]
# T = 273.15+T_amb               # temperatura do meio em Kelvin [K]
# F = np.arange(1, 4001)         # vetor de frequência em [Hz]
# co = 331.0+0.6*T_amb           # velocidade do som no ar [m/s] a 20 graus
# eta = 1.8134e-5                # coef. de viscosi. dinâmica do ar [N.s/m^2] ou [Pa.s]
# po = 1.21                      # densidade do ar [kg/m^3] a 20^o [C] e pressão de 1atm
# k_f = 0.026                    # condutividade térmica [W/mK]
# m_molar = 28.965               # massa molar [kg/K.mol]
# R_a = 287.05                   # constante específica do gás [J/kg.K]
# c_epx = 0.0034                 # coeficiente de expansão térmica do gás [1/K]
# C_p = 1007                     # calor específico a pressão constante [J/kgK]
# gamma = 1.410                  # razão de calor específico do ar [-]
# C_v = C_p/gamma                # calor específico a volume constante [J/kgK]
# Pr = 0.71                      # número de Prandtl [-]
# Po = 101325                    # pressão atmosférica [N/m^2] ou [Pa]
# nu = eta / po                  # viscosidade cinemática do ar [m^2/s]
# nu_1 = k_f/(po*C_v)            # constante [m^3.K/J]
# Zo = po*co                     # impedância do meio {Rayls}
# ko = gamma*Po                  # módulo de compressibilidade na condição adiabática [Pa]

# # PARÂMETROS GEOMÉTRICOS DA ÁREA DE SEÇÃO TRANSVERSAL DO DUTO TIPO FENDA
# Lf = 20e-3                     # largura da seção transversal [m]
# h = 2e-3                       # altura da seção transversal [m]
# Lef = 50e-3                    # comprimento do duto tipo fenda [m]
# Sf = Lf*h                      # área de seção transv. do duto tipo fenda [m^2]

# #VETORES DE VALORES#
# pss_v = np.empty(0)
# kss_v = np.empty(0)
# kc_v = np.empty(0)
# Zef_v = np.empty(0)
# cp_v = np.empty(0)
# w_v = np.empty(0)
# kef_v = np.empty(0)

# for f in F:
#     w = 2*np.pi*f                # frequência angular [rad/s]
#     w_v = np.append(w_v, w)     
#     k = w/co                     # vetor de onda [rad/m]

# # EQUAÇÕES DOS DUTOS TIPO FENDA
#     Gp = np.sqrt(1j*w*po/eta)                           # parametro
#     Gk = np.sqrt(1j*w*po*Pr/eta)                        # parâmetro
#     pss = po*(1-(tanh(h/2*Gp)/(h/2*Gp)))**-1            # densidade efetiva complexa (perdas viscosas no duto tipo fenda)
#     pss_v = np.append(pss_v, pss)
#     kss = ko*(1+(gamma-1)*(tanh(h/2*Gk)/(h/2*Gk)))**-1  # bulk modulus efetivo complexo (perdas térmicas no duto tipo fenda)
#     kss_v = np.append(kss_v, kss)
#     kc = w*np.sqrt(pss/kss)              # número de onda no duto tipo fenda
#     kc_v = np.append(kc_v, kc)
#     cef_v = np.real(np.sqrt(kss/pss))   # velocidade de fase no duto tipo fenda
#     Zs = np.sqrt(kss*pss)/(Sf)          # impedância característica no duto tipo fenda



# ############### Modelo de Stinson de perdas visco-térmicas para dutos de seção transversal circular ######
# # Stinson, M. R., The propagation of plane sound waves in narrow and wide circular tubes, and generalization to uniform tubes of arbitrary cross-sectional shape. The Journal of the Acoustical Society of America, 1991.


# # PARÂMETROS TERMOACÚSTICOS
# T_amb = 20                     # temperatura do ambiente [°C]
# T = 273.15+T_amb               # temperatura do meio em Kelvin [K]
# F = np.arange(1, 4001)         # vetor de frequência em [Hz]
# co = 331.0+0.6*T_amb           # velocidade do som no ar [m/s] a 20 graus
# eta = 1.8134e-5                # coef. de viscosi. dinâmica do ar [N.s/m^2] ou [Pa.s]
# po = 1.21                      # densidade do ar [kg/m^3] a 20^o [C] e pressão de 1atm
# k_f = 0.026                    # condutividade térmica [W/mK]
# m_molar = 28.965               # massa molar [kg/K.mol]
# R_a = 287.05                   # constante específica do gás [J/kg.K]
# c_epx = 0.0034                 # coeficiente de expansão térmica do gás [1/K]
# C_p = 1007                     # calor específico a pressão constante [J/kgK]
# gamma = 1.410                  # razão de calor específico do ar [-]
# C_v = C_p/gamma                # calor específico a volume constante [J/kgK]
# Pr = 0.71                      # número de Prandtl [-]
# Po = 101325                    # pressão atmosférica [N/m^2] ou [Pa]
# nu = eta / po                  # viscosidade cinemática do ar [m^2/s]
# nu_1 = k_f/(po*C_v)            # constante [m^3.K/J]
# Zo = po*co                     # impedância do meio {Rayls}
# ko = gamma*Po                  # módulo de compressibilidade na condição adiabática [Pa]

# # PARÂMETROS GEOMÉTRICOS DA ÁREA DE SEÇÃO TRANSVERSAL DO DUTO CIRCULAR
# d = 5e-3                      # diâmetro da seção transversal [m]
# r = d/2                        # raio da seção transversal [m]
# Lef = 50e-3                    # comprimento do duto [m]
# S = np.pi*r**2                 # área de seção transv. do duto [m^2]

# #VETORES DE VALORES#
# pt_v = np.empty(0)
# kt_v = np.empty(0)
# kc_v = np.empty(0)
# Zef_v = np.empty(0)
# cp_v = np.empty(0)
# w_v = np.empty(0)
# kef_v = np.empty(0)

# for f in F:
#     w = 2*np.pi*f                # frequência angular [rad/s]
#     w_v = np.append(w_v, w)     
#     k = w/co                     # vetor de onda [rad/m]
    
#     p_v = po*(1-2*1j*(r*np.sqrt(1j*w*po/eta))**-1*(sp.jv(1, 1j*r*np.sqrt(1j*w*po/eta))/sp.jv(0, 1j*r*np.sqrt(1j*w*po/eta))))**-1                         # densidade efetiva complexa (perdas viscosas no duto) 
#     pt_v = np.append(pt_v, p_v)
#     k_v = ko*(1 + 2*1j*(gamma-1)*(r*np.sqrt(1j*w*po*Pr/eta))**-1*(sp.jv(1, 1j*r*np.sqrt(1j*w*po*Pr/eta))/sp.jv(0, 1j*r*np.sqrt(1j*w*po*Pr/eta))))**-1    # bulk modulus efetivo complexo (perdas térmicas no duto)
#     kt_v = np.append(kt_v, k_v)
#     kc = w*np.sqrt(p_v/k_v)       # número de onda no duto
#     kc_v = np.append(kc_v, kc)
#     Zc = np.sqrt(k_v*p_v)/(S)     # impedância característica no duto

# fmt: on