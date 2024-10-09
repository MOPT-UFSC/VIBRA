#BIBLIOTECAS#
import numpy as np
from numpy import sqrt, tanh
import matplotlib.pyplot as plt
import matplotlib.colors


############### Modelo de Stinson de perdas visco-térmicas para dutos de seção transversal retangular e/ou quadrada ######
# Stinson, M. R., The propagation of plane sound waves in narrow and wide circular tubes, and generalization to uniform tubes of arbitrary cross-sectional shape. The Journal of the Acoustical Society of America, 1991.
# Outra referência a ser consultada Wei, S.; Li, L.; Zhigang, C.; Linyong, L.; Xiaopeng, F., A parameter design method for multifrequency perfect sound-absorbing metasurface with critical coupled Helmholtz resonator. Journal of low frequency noise, vibration and active control, 2021.


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

# PARÂMETROS GEOMÉTRICOS DA ÁREA DE SEÇÃO TRANSVERSAL DO DUTO RETANGULAR E/OU QUADRADA
a = 13e-3                      # largura da seção transversal [m]
b = 1.8e-3                     # altura da seção transversal [m]
Lef = 50e-3                    # comprimento do duto [m]
S = a*b                        # área de seção transv. do duto [m^2]

#VETORES DE VALORES#
pt_v = np.empty(0)
kt_v = np.empty(0)
kc_v = np.empty(0)
Zef_v = np.empty(0)
cp_v = np.empty(0)
w_v = np.empty(0)
kef_v = np.empty(0)

for f in F:
    w = 2*np.pi*f                # frequência angular [rad/s]
    w_v = np.append(w_v, w)     
    k = w/co                     # vetor de onda [rad/m]

# EQUAÇÕES DOS DUTOS DE SEÇÃO RETANGULAR E/OU QUADRADA
    Y1 = np.arange(0, 501)        # contador da série ajustado para até 501
    Y2 = np.arange(0, 501)        # contador da série ajustado para até 501
    akn = (Y1+(0.5))*(np.pi/a)    # constante para os modos no duto
    bmn = (Y2+(0.5))*(np.pi/b)    # constante para os modos no duto
    
    SUM_d_n = 0
    SUM_k_n = 0

    for s in range(0, len(Y1)):
        SUM_d_n += ((akn[s]**2)*bmn[s]**2*(akn[s]**2+bmn[s]**2-1j*w*po/eta))**-1 
        SUM_k_n += ((akn[s]**2)*bmn[s]**2*(akn[s]**2+bmn[s]**2-1j*w*Pr*po/eta))**-1 
    pt = (-eta*((a)**2)*((b)**2))/(4*1j*w*SUM_d_n)                                                # densidade efetiva complexa (perdas viscosas no duto)
    pt_v = np.append(pt_v, pt)
    kt = (eta*ko*((a)**2)*((b)**2))/(gamma*eta*((a)**2)*((b)**2)+4*1j*(gamma-1)*Pr*po*w*SUM_k_n)  # bulk modulus efetivo complexo (perdas térmicas no duto)
    kt_v = np.append(kt_v, kt)
    kc = w*np.sqrt(pt/kt)       # número de onda complexo no duto
    kc_v = np.append(kc_v, kc)
    Zc = np.sqrt(kt*pt)/(S)     # impedância característica complexa no duto


#Plotagem
plt.figure(figsize=(14, 8))  
plt.plot(F, np.real(pt_v), 'k', linewidth=3)
plt.grid(False)
plt.xlabel('Frequência - [Hz]', fontname='Times New Roman', fontsize=25)
plt.ylabel('Densidade efetiva - 'r'$\rho_{ef}$ ', fontname='Times New Roman', fontsize=35)
plt.xticks(np.arange(1, 4001, 400), fontname='Times New Roman', fontsize=25)
plt.legend(['Real'], fontsize=22)


plt.figure(figsize=(14, 8))  
plt.plot( F, np.imag(pt_v), 'b', linewidth=3)
plt.grid(False)
plt.xlabel('Frequência - [Hz]', fontname='Times New Roman', fontsize=25)
plt.ylabel('Densidade efetiva - ' r'$\rho_{ef}$ ', fontname='Times New Roman', fontsize=35)
plt.xticks(np.arange(1, 4001, 400), fontname='Times New Roman', fontsize=25)
plt.legend(['Imaginária'], fontsize=22) 


plt.figure(figsize=(14, 8))  
plt.plot(F, np.real(kt_v/ko), 'k', linewidth=3)
plt.grid(False)
plt.xlabel('Frequência - [Hz]', fontname='Times New Roman', fontsize=25)
plt.ylabel('Bulk modulus efetivo - ' r'$k_{ef}$ ', fontname='Times New Roman', fontsize=35)
plt.xticks(np.arange(1, 4001, 400), fontname='Times New Roman', fontsize=25)
plt.legend(['Real'], fontsize=22)


plt.figure(figsize=(14, 8))  
plt.plot( F, np.imag(kt_v/ko), 'b', linewidth=3)
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



