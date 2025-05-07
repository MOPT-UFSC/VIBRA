from math import pi
from pathlib import Path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from vibra import app, UI_DIR
from vibra.engine import AnalysisID
from vibra.interface.general.print_message_input import PrintMessageInput
from molde import load_ui

window_title_1 = "Error"
window_title_2 = "Warning"


class AcousticModalAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "analysis/acoustic/acoustic_modal_analysis_input.ui"
        load_ui(ui_path, self, ui_path.parent)

        app().main_window.close_dialogs()
        app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._load_analysis_setup()
        self.exec()

    def _initialize(self):
        self.modes = None
        self.setup_defined = False
        self.proceed_solution = False

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _define_qt_variables(self):

        # QLineEdit
        self.lineEdit_number_modes: QLineEdit
        self.lineEdit_sigma_factor: QLineEdit

        # QPushButton
        self.pushButton_run_analysis: QPushButton
        self.pushButton_enter_setup: QPushButton

    def _create_connections(self):
        self.pushButton_run_analysis.clicked.connect(self.run_analysis)
        self.pushButton_enter_setup.clicked.connect(self.enter_setup_callback)

    def _load_analysis_setup(self):
        analysis_setup = app().file.read_analysis_setup_from_file()

        if not analysis_setup:
            return
        
        if isinstance(analysis_setup, dict):
            if analysis_setup["analysis_id"] in [
                AnalysisID.STRUCTURAL_MODAL,
                AnalysisID.ACOUSTIC_MODAL,
            ]:
                modes = analysis_setup["modes"]
                sigma = analysis_setup["sigma_factor"]
                self.lineEdit_number_modes.setText(str(modes))
                self.lineEdit_sigma_factor.setText(str(sigma))

    def check_analysis_inputs(self):

        title = "Invalid input value"

        if self.lineEdit_number_modes.text() == "":
            message = "Invalid a value to the number of modes."
            PrintMessageInput([window_title_1, title, message])
            return True

        else:

            try:
                self.modes = int(self.lineEdit_number_modes.text())
            except Exception:
                message = "Invalid input value for number of modes."
                PrintMessageInput([window_title_1, title, message])
                return True

            try:
                self.sigma_factor = float(self.lineEdit_sigma_factor.text())
            except Exception:
                message = "Invalid input value for sigma factor."
                PrintMessageInput([window_title_1, title, message])
                return True

        return False

    def enter_setup_callback(self):

        if self.check_analysis_inputs():
            return True

        self.analysis_setup = {
            "analysis_id": AnalysisID.ACOUSTIC_MODAL,
            "modes": self.modes,
            "sigma_factor": self.sigma_factor,
        }

        self.setup_defined = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()
        self.close()

    def confirm(self):
        self.proceed_solution = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()
        self.close()

    def run_analysis(self):

        if self.enter_setup_callback():
            return

        self.confirm()

    def button_clicked(self):
        self.check_analysis_inputs()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.run_analysis()
        elif event.key() == Qt.Key_Escape:
            self.close()