
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