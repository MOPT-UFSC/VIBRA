from vibra import app
from vibra.interface.exception_message import ErrorMessage

class ProcessAnalysis:
    def __init__(self):
        super().__init__()

        self.main_window = app().main_window
        self.project = app().project

    def process_acoustic_modal_analysis(self):
        try:
            self.project.solve_acoustic_modal_analysis()
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            self.main_window.configure_results_render_widget(True)

    def process_structural_modal_analysis(self):
        try:
            self.project.solve_structural_modal_analysis()
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            self.main_window.configure_results_render_widget(True)

    def process_acoustic_harmonic_analysis(self):
        try:
            self.project.solve_acoustic_harmonic_analysis()
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            self.main_window.configure_results_render_widget(True)

    def process_structural_harmonic_analysis(self):
        try:
            self.project.solve_structural_harmonic_analysis()
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            self.main_window.configure_results_render_widget(True)
