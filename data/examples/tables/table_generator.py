import numpy as np

f_min = 2
f_max = 600
df = 2

frequencies = np.arange(f_min, f_max+df, df)
value = 2.037183e3

real = value * np.ones(len(frequencies), dtype=float)
imag = np.zeros(len(frequencies), dtype=float)

data = np.array([frequencies, real, imag], dtype=float)

unit = "N/m2"
header = f"Frequency [Hz], real [{unit}], imaginary [{unit}]"

filename = 'distributed_load_table_2037p183N_m2.dat'
np.savetxt(filename, data.T, delimiter=",", header=header)
teste = np.loadtxt(filename,delimiter=",")

# f = open(filename)
# header_r = f.readline()
# last_col_name = header.split(',')[-1]
# np.savetxt('load_Fx.dat', data, delimiter=",", header=header)
# np.savetxt('acoustic_pressure_table.dat', data, delimiter=",", header=header)
# np.savetxt('volume_velocity_table.dat', data, delimiter=",", header=header)
# np.savetxt('specific_impedance_table.dat', data, delimiter=",", header=header)