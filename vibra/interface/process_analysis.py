from vibra import app
from vibra.interface.exception_message import ErrorMessage

class ProcessAnalysis:
    def __init__(self):
        super().__init__()

        self.project = app().project

    def process_acoustic_modal_analysis(self):
        try:
            self.project.solve_acoustic_modal_analysis()
            if self.project.model.stop_processing:
                return
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            app().main_window.configure_results_render_widget()

    def process_structural_modal_analysis(self):
        try:
            self.project.solve_structural_modal_analysis()
            if self.project.model.stop_processing:
                return
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            app().main_window.configure_results_render_widget()

    def process_acoustic_harmonic_analysis(self, is_resume: bool = False):
        try:
            self.project.solve_acoustic_harmonic_analysis(is_resume)
            if self.project.model.stop_processing:
                return
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            app().main_window.configure_results_render_widget()

    def process_structural_harmonic_analysis(self):
        try:
            self.project.solve_structural_harmonic_analysis()
            if self.project.model.stop_processing:
                return
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            app().main_window.configure_results_render_widget()