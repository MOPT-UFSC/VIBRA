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

        ui_path = UI_DIR / "analysis/structural/structural_modal_analysis_input.ui"
        uic.loadUi(ui_path, self)

        self.setWindowIcon(app().main_window.vibra_icon)

        self.lineEdit_number_modes = self.findChild(QLineEdit, "lineEdit_number_modes")
        self.lineEdit_input_sigma_factor = self.findChild(QLineEdit, "lineEdit_input_sigma_factor")

        self.modes = int(self.lineEdit_number_modes.text())
        self.sigma_factor = float(self.lineEdit_input_sigma_factor.text())
        self.sigma_factor = (2 * pi * self.sigma_factor) ** 2

        self.pushButton_run_analysis_setup = self.findChild(
            QPushButton, "pushButton_run_analysis_setup"
        )
        self.pushButton_run_analysis_advanced = self.findChild(
            QPushButton, "pushButton_run_analysis_advanced"
        )
        self.pushButton_run_analysis_setup.clicked.connect(self.confirm)
        self.pushButton_run_analysis_advanced.clicked.connect(self.confirm)

        self.complete = False
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def check(self):

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
                self.sigma_factor = (2 * pi * float(self.lineEdit_input_sigma_factor.text())) ** 2
            except Exception:
                message = "Invalid input value for sigma factor."
                PrintMessageInput([window_title_1, title, message])
                return True

        return False

    def confirm(self):
        if self.check():
            return
        self.complete = True
        app().main_window.analysis_toolbar.analysis_finished.emit()
        self.close()

    def button_clicked(self):
        self.check()
