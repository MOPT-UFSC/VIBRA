
import numpy as np

class DataManager:
    def __init__():
        pass

def get_spectral_data_from_array(data: np.ndarray, return_frequencies: bool=False):
    """
    This function returns two vectors containing the spectral data of interest.
    The first one is the frequencies vector and the second is the vector of 
    complex values.
    
    Parameters
    ----------
    data : np.ndarray
        The array that gathers spectral data.

    return_frequencies: bool, optional
        It controls whether the frequencies vector will be returned.
    """        
    complex_values = data[:, 1] + 1j * data[:, 2]

    if return_frequencies:
        frequencies = data[:, 0]
        return frequencies, complex_values

    return complex_values


def is_frequencies_vector_equally_distributed(frequencies: list | np.ndarray, decimals: int = 10):

    f_min = frequencies[0]
    f_max = frequencies[-1]
    f_step = (f_max - f_min) / (len(frequencies) - 1)

    shifted_freqs = [value for value in frequencies[1:]]
    shifted_freqs.append(f_max + f_step)
    deltas = np.round(np.array(shifted_freqs) - np.array(frequencies), decimals)

    return np.unique(deltas).size == 1