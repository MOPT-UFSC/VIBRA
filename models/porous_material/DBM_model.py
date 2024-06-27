import numpy as np
import matplotlib.pyplot as plt

########## MODELO DBM - Delany-Bazley-Miki #######

# Observação - comparação dos modelos Delany-Bazley  e Delany-Bazley-Miki
# M. E. Delany and E. N. Bazley, Acoustical properties of fibrous absorbent materials, Applied Acoustics (3), 1970, pp. 105-116
# Y. Miki, Acoustical properties of porous materials - modifications of Delany-Bazley models - J. Acoust. Soc. Jpn. (E), 11 (1), 1990, pp. 19-24


# Parâmetros termoacústicos do ar
T_amb = 20                        # temperatura ambiente [°C]
T = 273.15 + T_amb                # temperatura do meio em Kelvin [K]
co = 331.0 + 0.6 * T_amb          # velocidade do som no ar [m/s] a 20 graus 
po = 1.21                          # densidade do ar [kg/m^3]
Po = 101320                        # pressão ambiente [Pa]
gamma = 1.4                       # razão calor específico do ar [ - ]
Pr = 0.71                         # número de Prandtl [ ]
eta = 1.84e-5                     # viscosidade dinâmica do ar [N.s/m^2] ou [Pa.s]
C_p = 1007                        # calor específico a pressão constante [J/kgK]
k_f = 0.026                       # condutividade térmica [W/mK]
f = np.arange(50, 10001)          # vetor frequência [Hz]
w = 2 * np.pi * f                 # frequência angular [rad/s]
k = w / co                        # número de onda
Zo = po * co                      # impedância acústica do ar [Rayls]

# Parâmetros macroscópicos do material poroso
rf = 25743
# rf = 12627                         # resistividade ao fluxo [Ns/m^4]
L = 50e-3                          # espessura do material poroso [m]

# Vetor de frequências
df = 5
f = np.arange(50, 1400+df, df)           # vetor frequência [Hz]
w = 2 * np.pi * f                  # frequência angular [rad/s]

# Inicialização dos arrays para armazenar os resultados
alpha_DB70 = np.zeros(len(f))
alpha_DB70_Mik90 = np.zeros(len(f))

# Cálculos para cada frequência
for o in range(len(f)):
    # Determinando a variável X e os limites de validade de ambos os modelos
    X = f[o] / rf         
    f_min = 0.01 * rf
    f_max = 1.00 * rf

    # Modelo Delany and Bazley
    Z_DB70 = Zo * (1 + 9.08 * (X * 1000) ** (-0.75) - 1j * 11.9 * (X * 1000) ** (-0.73))
    k_DB70 = w[o] / co * (-1j) * (10.3 * (X * 1000) ** (-0.59) + 1j * (1 + 10.8 * (X * 1000) ** (-0.70)))
    Z_DB = -1j * Z_DB70 / np.tan(k_DB70 * L)
    alpha_DB70[o] = 1 - np.abs((Z_DB - Zo) / (Z_DB + Zo)) ** 2

    # Expressões revisadas do modelo Delany e Bazley por MIki
    Z_DB70_Mik90 = Zo * (1 + 5.50 * (X * 1000) ** (-0.632) - 1j * 8.43 * (X * 1000) ** (-0.632))
    k_DB70_Mik90 = w[o] / co * (-1j) * (11.41 * (X * 1000) ** (-0.618) + 1j * (1 + 7.81 * (X * 1000) ** (-0.618)))
    Z_DB_M = -1j * Z_DB70_Mik90 / np.tan(k_DB70_Mik90 * L)
    alpha_DB70_Mik90[o] = 1 - np.abs((Z_DB_M - Zo) / (Z_DB_M + Zo)) ** 2


C1 = 0.0497
C2 = -0.754
C3 = 0.0758
C4 = -0.732
C5 = 0.1690
C6 = -0.595
C7 = 0.0858
C8 = -0.700

rho_0 = po
C_0 = co
omega = w
X = f / rf

Z_eq = (rho_0 * C_0) * ( 1 + C1*(X**C2) - 1j*(C3*(X**C4)) )
k_eq = (omega / C_0) * (-1j) * ( C5*(X**C6) + 1j*(1 + C7*(X**C8)) )

Z_DB = -1j * Z_eq / np.tan(k_eq * L)
alpha_DB = 1 - np.abs((Z_DB - rho_0*C_0) / (Z_DB + rho_0*C_0)) ** 2

# Plotagem
plt.figure()
plt.plot(f, alpha_DB70, 'k', linewidth=3)
plt.plot(f, alpha_DB, 'b', linewidth=3)
plt.plot(f, alpha_DB70_Mik90, 'r', linewidth=3)
plt.grid(True)
plt.xlim([100, 10000])
plt.xlabel('Frequência - [Hz]')
plt.ylabel(r'$\alpha(\omega)$ [-]')
plt.legend(['Delany-Bazley - model', "valid", 'Delany-Bazley-Miki - model'])
plt.show()