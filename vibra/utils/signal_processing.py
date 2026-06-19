

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def process_ifft_from_one_sided_spectrum_signal(frequencies: np.ndarray, Xf_data: np.ndarray, dc_included: bool=False):
    """
    If n is even, the length of the transformed axis is (n/2)+1. If n is odd, the length is (n+1)/2.
    """

    N_f = len(Xf_data)

    # reinsert the DC component
    if not dc_included:
        N_f += 1

    # create the auxilar vector Xf
    Xf = np.zeros(N_f, dtype=complex)

    # adjust the one-sided spectrum scale
    Xf[1:] = Xf_data / 2

    # process the sampling frequency and time increment
    f_max = np.max(frequencies)
    f_s = 2 * f_max
    dt = 1 / f_s

    # process the ifft from signal Xf
    x_t = np.fft.irfft(Xf)# * (2*(N-1))
    N_t = len(x_t)

    # corrects the signal amplitude
    x_t *= N_t

    # create the time vector
    time = np.arange(N_t, dtype=float) * dt

    return time, x_t


def process_multiple_iffts_from_one_sided_spectrum_signals(frequencies: np.ndarray, Xf_data: np.ndarray, dc_included: bool=False):
    """
    If n is even, the length of the transformed axis is (n/2)+1. If n is odd, the length is (n+1)/2.
    """

    rows, N_f = Xf_data.shape

    # reinsert the DC component
    if not dc_included:
        N_f += 1

    # create the auxilar vector Xf
    Xf = np.zeros((rows, N_f), dtype=complex)

    # adjust the one-sided spectrum scale
    Xf[:, 1:] = Xf_data / 2

    # process the sampling frequency and time increment
    f_max = np.max(frequencies)
    f_s = 2 * f_max
    dt = 1 / f_s

    # process the ifft from signal Xf
    x_t = np.fft.irfft(Xf, axis=1)# * (2*(N-1))
    N_t = x_t[0, :].size

    # corrects the signal amplitude
    x_t *= N_t

    # create the time vector
    time_vector = np.arange(N_t, dtype=float) * dt

    return time_vector, x_t


def extend_signal(x_data: np.ndarray, N_rep: int):
    return np.tile(x_data[:-1], N_rep)


def process_one_sided_spectrum(x_data: np.ndarray, dt: float):

    # create the frequencies vector
    freq_vector = np.fft.rfftfreq(len(x_data), dt)

    # process the one-sided spectrum
    Xf_data = np.fft.rfft(x_data) / len(x_data)

    # adjust the one-sided spectrum amplitude
    Xf_data[1:] *= 2

    return freq_vector, Xf_data


def process_two_sided_spectrum(x_data: np.ndarray, dt: float):

    # create the frequencies vector
    freq_vector = np.fft.fftfreq(len(x_data), dt)

    # process the one-sided spectrum
    Xf_data = np.fft.fft(x_data) / len(x_data)
    
    freq_vector = np.fft.fftshift(freq_vector)
    Xf_data = np.fft.fftshift(Xf_data)

    check_if_signal_energy_is_conserved(x_data, Xf_data)

    return freq_vector, Xf_data


def get_window_and_correction_factor(window_type: str, correction_type: str, N: int):

    if window_type == "rectangular":
        window_type = "boxcar"

    if window_type not in ["hann", "flattop", "boxcar", "hamming"]:
        return 1, 1

    # create the window
    window = signal.get_window(window_type, N)

    if correction_type == "amplitude":
        correction_factors = {  
            "boxcar" : 1,
            "hann" : 2,
            "flattop" : 4.18,
            "hamming" : 1.85  
            }

    else:
        correction_factors = {  
            "boxcar" : 1,
            "hann" : np.sqrt(8/3),
            "flattop" : 2.26,
            "hamming" : 1.59
            }

    return window, correction_factors.get(window_type)


def check_if_signal_energy_is_conserved(x_data: np.ndarray, Xf_data: np.ndarray):
    x_rms = np.sqrt(np.sum(x_data**2) / len(x_data))
    Xf_rms = np.sqrt(np.sum(np.abs(Xf_data * np.conjugate(Xf_data))))

    if round(x_rms, 8) != round(Xf_rms, 8):
        message = "Both domains do not have the same rms/energy values.\n"
        message += f"RMS value (x_data): {round(x_rms,8)} \n"
        message += f"RMS value (Xf_data): {round(Xf_rms,8)}"
        print(message)


def plot(x, y, x_label, y_label, title, label="", absolute=False):

    fig = plt.figure(figsize=[8, 6])
    ax = fig.add_subplot(1,1,1)

    if absolute:
        y = np.abs(y)

    ax.plot(x, y, color=[0,0,1], linewidth = 1, label = label)

    ax.set_xlabel(x_label, fontsize = 11, fontweight = 'bold')
    ax.set_ylabel(y_label, fontsize = 11, fontweight = 'bold')
    ax.set_title(title, fontsize = 12, fontweight = 'bold')

    plt.grid()
    plt.show()


def plot_original_and_windowed_spectrums(freq: np.ndarray, Xf: np.ndarray, Xf_w: np.ndarray):
    fig = plt.figure(figsize=[8, 6])
    ax = fig.add_subplot(1,1,1)

    ax.semilogy(freq, np.abs(Xf), color=[0,0,1], linewidth = 1, label = "non-windowed signal")
    ax.semilogy(freq, np.abs(Xf_w), color=[1,0,0], linewidth = 1, label = "windowed signal")

    ax.set_xlabel("Frequency [Hz]", fontsize = 11, fontweight = 'bold')
    ax.set_ylabel("Amplitude [--]", fontsize = 11, fontweight = 'bold')
    ax.set_title("", fontsize = 12, fontweight = 'bold')

    plt.legend()
    plt.grid()
    plt.show()


def example_of_simulated_signal(df_req, window_type: str="hann", correction_type: str="energy"):

    # angular resolution
    d_theta = 1

    # points to complete one revolution
    Np = int(360 / d_theta) + 1

    # number of male lobes
    N_lobes = 4

    # rotational frequency
    f_rot = 5296 / 60

    # revolution time
    T_rev = 1 / f_rot

    # time step
    dt = T_rev / (Np - 1)

    # sampling period for required frequency resolution
    T_req = 1 / df_req

    # number of revolutions to 'reach' the required frequency resolution
    N_rev = int(np.ceil(T_req/T_rev))

    # signal time block
    T = N_rev * T_rev

    # number of time steps
    N = int(T / dt)

    # create the time vector
    time = np.arange(0, N+1) * dt

    # amplitudes
    amplitudes = [4, 6, 3, 1, 0.5, 0.2, 0.1, 0.05, 0.01]

    # phases
    phases = np.random.randint(0, 360, len(amplitudes)) * (np.pi / 180)

    # compose the signal
    x_data = 0.
    for i in range(len(amplitudes)):
        n = i + 1
        omega = 2 * np.pi * f_rot * N_lobes * n
        x_data += amplitudes[i] * np.sin(omega * time + phases[i])

    # create a noise signal
    average = 0.0
    std_deviation = 0.0
    noise = average + std_deviation * np.random.randn(x_data.size)

    # add noise to signal
    x_data += noise

    # create the window
    window, correction_factor = get_window_and_correction_factor(window_type, correction_type, x_data.size)
    x_windowed = x_data * window

    freq, Xf = process_one_sided_spectrum(x_data[:-1], dt)
    freq, Xf_w = process_one_sided_spectrum(x_windowed[:-1], dt)
    # freq, Xf = process_two_sided_spectrum(x_data[:-1], dt)

    # apply signal correction factor
    Xf_w[1:] *= correction_factor

    plot_original_and_windowed_spectrums(freq, Xf, Xf_w)
    plot(time, x_data, "Time [s]", "Amplitude [--]", "Waveform signal")
    # plot(time, x_windowed, "Time [s]", "Amplitude [--]", "Windowed waveform signal")


if __name__ == "__main__":
    example_of_simulated_signal(5.0, window_type="hann", correction_type="amplitude")