#BIBLIOTECAS#
import numpy as np
from numpy import sqrt, tanh
import matplotlib.pyplot as plt
import matplotlib.colors


############### Modelo de Stinson de perdas visco-térmicas para dutos de seção tipo fenda ######
# Stinson, M. R., The propagation of plane sound waves in narrow and wide circular tubes, and generalization to uniform tubes of arbitrary cross-sectional shape. The Journal of the Acoustical Society of America, 1991.


# PARÂMETROS TERMOACÚSTICOS
T_amb = 20                     # temperatura do ambiente [°C]
T = 273.15+T_amb               # temperatura do meio em Kelvin [K]
F = np.arange(1, 4001)         # vetor de frequência em [Hz]
co = 331.0+0.6*T_amb           # velocidade do som no ar [m/s] a 20 graus
eta = 1.8134e-5                # coef. de viscosi. dinâmica do ar [N.s/m^2] ou [Pa.s]
po = 1.21                      # densidade do ar [kg/m^3] a 20^o [C] e pressão de 1atm
k_f = 0.026                    # condutividade térmica [W/mK]
m_molar = 28.965               # massa molar [kg/K.mol]
R_a = 287.05                   # constante específica do gás [J/kg.K]
c_epx = 0.0034                 # coeficiente de expansão térmica do gás [1/K]
C_p = 1007                     # calor específico a pressão constante [J/kgK]
gamma = 1.410                  # razão de calor específico do ar [-]
C_v = C_p/gamma                # calor específico a volume constante [J/kgK]
Pr = 0.71                      # número de Prandtl [-]
Po = 101325                    # pressão atmosférica [N/m^2] ou [Pa]
nu = eta / po                  # viscosidade cinemática do ar [m^2/s]
nu_1 = k_f/(po*C_v)            # constante [m^3.K/J]
Zo = po*co                     # impedância do meio {Rayls}
ko = gamma*Po                  # módulo de compressibilidade na condição adiabática [Pa]

# PARÂMETROS GEOMÉTRICOS DA ÁREA DE SEÇÃO TRANSVERSAL DO DUTO TIPO FENDA
Lf = 20e-3                     # largura da seção transversal [m]
h = 2e-3                       # altura da seção transversal [m]
Lef = 50e-3                    # comprimento do duto tipo fenda [m]
Sf = Lf*h                      # área de seção transv. do duto tipo fenda [m^2]

#VETORES DE VALORES#
pss_v = np.empty(0)
kss_v = np.empty(0)
kc_v = np.empty(0)
Zef_v = np.empty(0)
cp_v = np.empty(0)
w_v = np.empty(0)
kef_v = np.empty(0)

for f in F:
    w = 2*np.pi*f                # frequência angular [rad/s]
    w_v = np.append(w_v, w)     
    k = w/co                     # vetor de onda [rad/m]

# EQUAÇÕES DOS DUTOS TIPO FENDA
    Gp = np.sqrt(1j*w*po/eta)                           # parametro
    Gk = np.sqrt(1j*w*po*Pr/eta)                        # parâmetro
    pss = po*(1-(tanh(h/2*Gp)/(h/2*Gp)))**-1            # densidade efetiva complexa (perdas viscosas no duto tipo fenda)
    pss_v = np.append(pss_v, pss)
    kss = ko*(1+(gamma-1)*(tanh(h/2*Gk)/(h/2*Gk)))**-1  # bulk modulus efetivo complexo (perdas térmicas no duto tipo fenda)
    kss_v = np.append(kss_v, kss)
    kc = w*np.sqrt(pss/kss)              # número de onda no duto tipo fenda
    kc_v = np.append(kc_v, kc)
    cef_v = np.real(np.sqrt(kss/pss))   # velocidade de fase no duto tipo fenda
    Zs = np.sqrt(kss*pss)/(Sf)          # impedância característica no duto tipo fenda


#Plotagem
plt.figure(figsize=(14, 8))  
plt.plot(F, np.real(pss_v), 'k', linewidth=3)
plt.grid(False)
plt.xlabel('Frequência - [Hz]', fontname='Times New Roman', fontsize=25)
plt.ylabel('Densidade efetiva - 'r'$\rho_{ef}$ ', fontname='Times New Roman', fontsize=35)
plt.xticks(np.arange(1, 4001, 400), fontname='Times New Roman', fontsize=25)
plt.legend(['Real'], fontsize=22)


plt.figure(figsize=(14, 8))  
plt.plot( F, np.imag(pss_v), 'b', linewidth=3)
plt.grid(False)
plt.xlabel('Frequência - [Hz]', fontname='Times New Roman', fontsize=25)
plt.ylabel('Densidade efetiva - ' r'$\rho_{ef}$ ', fontname='Times New Roman', fontsize=35)
plt.xticks(np.arange(1, 4001, 400), fontname='Times New Roman', fontsize=25)
plt.legend(['Imaginária'], fontsize=22) 


plt.figure(figsize=(14, 8))  
plt.plot(F, np.real(kss_v/ko), 'k', linewidth=3)
plt.grid(False)
plt.xlabel('Frequência - [Hz]', fontname='Times New Roman', fontsize=25)
plt.ylabel('Bulk modulus efetivo - ' r'$k_{ef}$ ', fontname='Times New Roman', fontsize=35)
plt.xticks(np.arange(1, 4001, 400), fontname='Times New Roman', fontsize=25)
plt.legend(['Real'], fontsize=22)


plt.figure(figsize=(14, 8))  
plt.plot( F, np.imag(kss_v/ko), 'b', linewidth=3)
plt.grid(False)
plt.xlabel('Frequência - [Hz]', fontname='Times New Roman', fontsize=25)
plt.ylabel('Bulk modulus efetivo - ' r'$k_{ef}$ ', fontname='Times New Roman', fontsize=35)
plt.xticks(np.arange(1, 4201, 400), fontname='Times New Roman', fontsize=25)
plt.legend(['Imaginária'], fontsize=22)


plt.figure(figsize=(14, 8))  
plt.plot(F, np.real(kc_v/k), 'm', linewidth=3)
plt.grid(False)
plt.xlabel('Frequência - [Hz]', fontname='Times New Roman', fontsize=25)
plt.ylabel('Número de onda - ' r'$k_{c}$ ', fontname='Times New Roman', fontsize=35)
plt.xticks(np.arange(1, 4001, 400), fontname='Times New Roman', fontsize=25)
plt.legend(['Real'], fontsize=22)


plt.figure(figsize=(14, 8))  
plt.plot( F, np.imag(kc_v/k), 'r', linewidth=3)
plt.grid(False)
plt.xlabel('Frequência - [Hz]', fontname='Times New Roman', fontsize=25)
plt.ylabel('Número de onda - ' r'$k_{c}$ ', fontname='Times New Roman', fontsize=35)
plt.xticks(np.arange(1, 4001, 400), fontname='Times New Roman', fontsize=25)
plt.legend(['Imaginária'], fontsize=22)
plt.show() 



