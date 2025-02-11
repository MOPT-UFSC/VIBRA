from math import pi
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vibra import app, UI_DIR
from vibra.interface.general.print_message_input import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"


class StructuralModalAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "analysis/structural/modal_analysis_input.ui"
        uic.loadUi(ui_path, self)

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
        if isinstance(analysis_setup, dict):
            if analysis_setup.get("analysis_id", None) in [2, 4]:
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
                                "analysis_id" : 2,
                                "analysis_type": "Structural Modal Analysis",
                                "modes" : self.modes,
                                "sigma_factor" : self.sigma_factor
                                }

        self.setup_defined = True
    def confirm(self):
        if self.check():
            return
        self.complete = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()
        self.close()

    def run_analysis(self):

        if self.enter_setup_callback():
            return

        self.proceed_solution = True

    def button_clicked(self):
        self.check_analysis_inputs()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.run_analysis()
        elif event.key() == Qt.Key_Escape:
            self.close()

# class StructuralModalAnalysisInput(QDialog):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         ui_path = UI_DIR / "analysis/structural/structural_modal_analysis_input.ui"
#         uic.loadUi(ui_path, self)

#         self.setWindowIcon(app().main_window.vibra_icon)

#         self.lineEdit_number_modes = self.findChild(QLineEdit, "lineEdit_number_modes")
#         self.lineEdit_input_sigma_factor = self.findChild(QLineEdit, "lineEdit_input_sigma_factor")

#         self.modes = int(self.lineEdit_number_modes.text())
#         self.sigma_factor = float(self.lineEdit_input_sigma_factor.text())
#         self.sigma_factor = (2 * pi * self.sigma_factor) ** 2

#         self.pushButton_run_analysis_setup = self.findChild(
#             QPushButton, "pushButton_run_analysis_setup"
#         )
#         self.pushButton_run_analysis_advanced = self.findChild(
#             QPushButton, "pushButton_run_analysis_advanced"
#         )
#         self.pushButton_run_analysis_setup.clicked.connect(self.confirm)
#         self.pushButton_run_analysis_advanced.clicked.connect(self.confirm)

#         self.complete = False
#         self.exec_()

#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
#             self.confirm()
#         elif event.key() == Qt.Key_Escape:
#             self.close()

#     def check(self):

#         title = "Invalid input value"
#         if self.lineEdit_number_modes.text() == "":
#             message = "Invalid a value to the number of modes."
#             PrintMessageInput([window_title_1, title, message])
#             return True

#         else:

#             try:
#                 self.modes = int(self.lineEdit_number_modes.text())
#             except Exception:
#                 message = "Invalid input value for number of modes."
#                 PrintMessageInput([window_title_1, title, message])
#                 return True
            
#             try:
#                 self.sigma_factor = (2 * pi * float(self.lineEdit_input_sigma_factor.text())) ** 2
#             except Exception:
#                 message = "Invalid input value for sigma factor."
#                 PrintMessageInput([window_title_1, title, message])
#                 return True

#         return False

#     def confirm(self):
#         if self.check():
#             return
#         self.complete = True
#         self.close()

#     def button_clicked(self):
#         self.check()
