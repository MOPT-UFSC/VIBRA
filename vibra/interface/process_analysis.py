from vibra import app
from vibra.interface.exception_message import ErrorMessage


class ProcessAnalysis:
    def __init__(self):
        super().__init__()

    def process_acoustic_modal_analysis(self):
        try:
            app().new_project.solve_acoustic_modal_analysis()
            if app().new_project.model.stop_processing:
                return
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            app().main_window.configure_results_render_widget()

    def process_structural_modal_analysis(self):
        try:
            app().new_project.solve_structural_modal_analysis()
            if app().new_project.model.stop_processing:
                return
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            app().main_window.configure_results_render_widget()

    def process_acoustic_harmonic_analysis(self, is_resume: bool = False):
        try:
            app().new_project.solve_acoustic_harmonic_analysis(is_resume)
            if app().new_project.model.stop_processing:
                return
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            app().main_window.configure_results_render_widget()

    def process_structural_harmonic_analysis(self):
        try:
            app().new_project.solve_structural_harmonic_analysis()
            if app().new_project.model.stop_processing:
                return
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            app().main_window.configure_results_render_widget()
