import numpy as np

def generate_table_of_constant_values(filename: str, value: float | complex, f_step: float=5, f_min: float=5, f_max: float=600):
    """ 
    This function create an array of constant complex values and save it in a text file.

    Parameters
    ----------

    filename : str
        The complete filename including the file extension

    value : float or complex
        The constant value of table 

    f_step : float, optional
        The frequency step of frequency vector data
    
    f_min: float, optional
        The minimum frequency of frequency vector data
    
    f_max: float, optional
        The maximum frequency of frequency vector data

    """

    freq = np.arange(f_min, f_max+f_step, f_step, dtype=int)
    values = np.ones_like(freq, dtype=complex) * value

    data = np.array([freq, np.real(values), np.imag(values)]).T
    # data = np.round(data, 8)

    path = f"data/examples/tables/{filename}"
    np.savetxt(path, data, delimiter=",")

if __name__ == "__main__":
    filename = "incident_plane_wave.dat"
    value = 1
    f_step, f_min, f_max = 5, 10, 1400
    generate_table_of_constant_values(filename, value, f_step=f_step, f_min=f_min, f_max=f_max)