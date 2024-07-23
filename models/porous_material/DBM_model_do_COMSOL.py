import numpy as np
import matplotlib.pyplot as plt

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
rf = 12627                         # resistividade ao fluxo [Ns/m^4]
L = 50e-3                          # espessura do material poroso [m]

# Constantes do modelo Delany-Bazley
C1 = 0.0978
C2 = 0.7
C3 = 0.189
C4 = 0.595
C5 = 0.0571
C6 = 0.754
C7 = 0.087
C8 = 0.732

# Vetor de frequências
f = np.arange(50, 10001)           # vetor frequência [Hz]
w = 2 * np.pi * f                  # frequência angular [rad/s]

# Inicialização dos arrays para armazenar os resultados
alpha_DB70 = np.zeros(len(f))

# Cálculos para cada frequência
for t in range(len(f)):
    # Determinando a variável X
    X = po * f[t] / rf

    # Impedância característica do meio poroso
    Z_DB = Zo * (1 + C1 * X ** (-C2) - 1j * C3 * X ** (-C4))

    # Número de onda do meio poroso
    k_DB = (w[t] / co) * (1 + C5 * X ** (-C6) - 1j * C7 * X ** (-C8))

    # Impedância de superfície modelo Delany-Bazley
    Z_DB = -1j * Z_DB / np.tan(k_DB * L)

    # Coeficiente de absorção modelo Delany-Bazley
    alpha_DB70[t] = 1 - np.abs((Z_DB - Zo) / (Z_DB + Zo)) ** 2

# Plotagem
plt.figure()
plt.plot(f, alpha_DB70, 'k', linewidth=3)
plt.grid(True)
plt.xlim([100, 10000])
plt.xlabel('Frequência - [Hz]')
plt.ylabel(r'$\alpha(\omega)$ [-]')
plt.legend(['Delany-Bazley-Miki - model'])
plt.show()