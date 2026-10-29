import numpy as np

from vibra import app
from vibra.interface.loading_window import LoadingWindow
from vibra.utils.subprocess.structural_stresses_handler import recover_structural_stresses_in_subprocess


def process_structural_stresses(time_domain: bool = False):
    post = app().project.get_structural_postprocessing()

    if app().config.user_preferences.run_analysis_in_subprocess:
        if not isinstance(post.nodal_averaged_stresses_frequency, np.ndarray):
            stresses = recover_structural_stresses_in_subprocess(
                app().project.working_directory,
                post.get_nodal_stresses_frequency_shape()
            )

            if stresses is None:
                return False
            
            post.nodal_averaged_stresses_frequency = stresses

        if time_domain:
            LoadingWindow(post.compute_structural_stresses_time).run()

    else:
        def recover_stresses():
            post.compute_structural_stresses_frequency()
            if time_domain:
                post.compute_structural_stresses_time()

        LoadingWindow(recover_stresses).run()

    return True