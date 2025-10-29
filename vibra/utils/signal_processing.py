import numpy as np


def extend_signal(x_data: np.ndarray, N_rep: int):
    return np.tile(x_data[:-1], N_rep)


def process_one_sided_spectrum(x_data: np.ndarray, dt: float):

    # process the one-sided spectrum
    X_f = np.fft.rfft(x_data) / len(x_data)

    # adjust the one-sided spectrum amplitude
    X_f[1:] *= 2

    # create the frequencies vector
    freq_vector = np.fft.rfftfreq(len(x_data), dt)
    
    return freq_vector, X_f
