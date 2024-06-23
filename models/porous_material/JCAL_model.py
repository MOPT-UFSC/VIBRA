import numpy as np
import matplotlib.pyplot as plt


############### MODELO JCAL - Jhonson-Champoux-Allard-Lafarge ###############
# Parâmetros termoacústicos
T_amb = 20                         # temperatura ambiente [°C]
T = 273.15 + T_amb                 # temperatura do meio em Kelvin [K]
co = 331.0 + 0.6 * T_amb           # velocidade do som no ar [m/s] a 20 graus 
po = 1.21                           # densidade do ar [kg/m^3]
Po = 101320                         # pressão ambiente [Pa]
gamma = 1.4                         # razão calor específico do ar [ - ]
Pr = 0.71                           # número de Prandtl [ ]
eta = 1.84e-5                       # viscosidade dinâmica do ar [N.s/m^2] ou [Pa.s]
C_p = 1007                          # calor específico a pressão constante [J/kgK]
k_f = 0.026                         # condutividade térmica [W/mK]
f = np.arange(50, 10001)            # vetor frequência [Hz]
w = 2 * np.pi * f                   # frequência angular [rad/s]
k = w / co                          # número de onda
Zo = po * co                        # impedância acústica do ar [Rayls]

# Parâmetros macroscópicos do material poroso (espuma de melamina)
rf = 12627                           # resistividade ao fluxo [Ns/m^4]
por = 0.9                            # porosidade [%]
tor = 1.0                            # tortuosidade [-]
ccv = 91e-6                          # comprimento característico viscoso [m]
cct = 148e-6                         # comprimento característico térmico [m]
rho2 = 10                            # densidade do material fibroso [Kg/m^3]
L = 50e-3                            # espessura do material poroso [m]
q = eta / rf                         # permeabilidade estática viscosa [m^2]
qo = q * tor                         # permeabilidade estática térmica [m^2]

# Inicialização dos arrays para armazenar os resultados
peq = np.zeros(len(f), dtype=complex)
keq = np.zeros(len(f), dtype=complex)
Zcr = np.zeros(len(f), dtype=complex)
kcr = np.zeros(len(f), dtype=complex)
Cm = np.zeros(len(f), dtype=complex)
Zsr = np.zeros(len(f), dtype=complex)
Rr = np.zeros(len(f), dtype=complex)
alphar = np.zeros(len(f))

# Cálculos para cada frequência
for o in range(len(f)):
    # Densidade complexa que descreve as perdas viscosas
    peq[o] = ((tor * po) / por) * (1 + ((rf * por) / (1j * w[o] * po * tor)) * np.sqrt(1 + ((1j * 4 * tor**2 * eta * po * w[o]) / (rf**2 * ccv**2 * por**2))))

    # Módulo de compressibilidade efetivo que descreve as perdas térmicas
    keq[o] = ((gamma * Po) / por) / (gamma - (gamma - 1) * (1 - 1j * ((por * k_f) / (w[o] * C_p * qo * po)) * np.sqrt(1 + ((1j * 4 * w[o] * C_p * po * qo**2) / (por**2 * k_f * cct**2))))**-1)

    # Impedância característica complexa do material poroso
    Zcr[o] = np.sqrt(peq[o] * keq[o])

    # Número de onda complexa no material poroso
    kcr[o] = w[o] * np.sqrt(peq[o] / keq[o])

    # Velocidade do som complexa no material poroso
    Cm[o] = np.sqrt(keq[o] / peq[o])

    # Impedância de superfície complexa do material poroso
    Zsr[o] = -1j * (Zcr[o]) * (1 / np.tan(kcr[o] * L))

    # Coeficiente de reflexão do material rígido
    Rr[o] = (Zsr[o] - Zo) / (Zsr[o] + Zo)

    # Coeficiente de absorção sonora
    alphar[o] = 1 - np.abs(Rr[o])**2

# Plotagem
plt.figure()
plt.plot(f, alphar, 'k', linewidth=3)
plt.grid(True)
plt.xlim([100, 10000])
plt.ylim([0, 1])
plt.xlabel('Frequência - [Hz]')
plt.ylabel(r'$\alpha(\omega)$ [-]')
plt.legend(['JCAL - model'])
plt.show()