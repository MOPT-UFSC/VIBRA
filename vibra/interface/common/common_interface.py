
from vibra import app

import numpy as np


def update_analysis_setup_in_file(frequencies: np.ndarray):

    analysis_setup = app().file.read_analysis_setup_from_file()

    analysis_setup.update(
        {
        "frequency_spacing" : "tabular",
        "f_min" : float(frequencies[0]),
        "f_max" : float(frequencies[-1]),
        "f_step" : float(frequencies[1] - frequencies[0]),
        "frequencies" : None,
        "solution_steps_mask" : list(),
        }
        )

    app().project.set_analysis_setup(analysis_setup)
    app().file.write_analysis_setup_in_file(analysis_setup)