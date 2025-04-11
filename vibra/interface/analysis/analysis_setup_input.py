from pathlib import Path

import numpy as np
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QTabWidget

from vibra import app, UI_DIR
from vibra.interface.general.print_message_input import PrintMessageInput
from molde import load_ui

window_title = "Error"


class AnalysisSetupInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.project = app().project

        self.analysis_data = self.project.analysis_data
        self.analysis_id = self.analysis_data["analysis_id"]
        self.model = app().project.model

        """
        |--------------------------------------------------------------------|
        |                    Analysis ID codification                        |
        |--------------------------------------------------------------------|
        |    0 - Structural - Harmonic analysis through direct method        |
        |    1 - Structural - Harmonic analysis through mode superposition   |
        |    2 - Structural - Modal analysis                                 |
        |    3 - Acoustic - Harmonic analysis through direct method          |
        |    4 - Acoustic - Modal analysis                                   |
        |    5 - Coupled - Harmonic analysis through direct method           |
        |    6 - Coupled - Harmonic analysis through mode superposition      |
        |--------------------------------------------------------------------|
        """
        app().main_window.close_dialogs()
        app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self._create_connections()

        self.load_analysis_data()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.frequencies = []
        self.complete = False
        self.solve_analysis = False
        self.keep_window_open = True

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Analysis setup")

    def _create_connections(self):
        self.pushButton_enter_setup.clicked.connect(self.enter_setup_callback)
        self.pushButton_run_analysis.clicked.connect(self.check_run)

    def _update_fmin(self):
        df = self.lineEdit_fstep.text()
        self.lineEdit_fmin.setText(df)

    def load_analysis_data(self):
        analysis_setup = app().project.analysis_data
        
        f_min = analysis_setup.get("f_min", 2)
        f_max = analysis_setup.get("f_max", 600)
        f_step = analysis_setup.get("f_step", 2)
        self.analysis_id = analysis_setup.get("analysis_id", None)
        global_damping = analysis_setup.get("global_damping", (0., 0., 0., 0.))

        self.load_damping_inputs(self.analysis_id, global_damping)
        self.load_frequency_setup_inputs(f_min, f_max, f_step)

    def load_damping_inputs(self, analysis_id: int, global_damping: tuple | list):
        if analysis_id in [0, 1, 5, 6] and sum(global_damping):

            if global_damping[0]:
                self.lineEdit_av.setText(str(global_damping[0]))

            if global_damping[1]:
                self.lineEdit_bv.setText(str(global_damping[1]))

            if global_damping[2]:
                self.lineEdit_ah.setText(str(global_damping[2]))

            if global_damping[3]:
                self.lineEdit_bh.setText(str(global_damping[3]))

    def load_frequency_setup_inputs(self, f_min: float, f_max: float, f_step: float):
        self.lineEdit_fmin.setText(str(round(f_min, 6)))
        self.lineEdit_fmax.setText(str(round(f_max, 6)))
        self.lineEdit_fstep.setText(str(round(f_step, 6)))

        key = app().project.model.properties.check_if_there_are_tables_at_the_model()

        self.lineEdit_fmin.setDisabled(key)
        self.lineEdit_fmax.setDisabled(key)
        self.lineEdit_fstep.setDisabled(key)        

    def enter_setup_callback(self):
        analysis_setup = app().file.read_analysis_setup_from_file()
        if analysis_setup is None:
            analysis_setup = dict()

        analysis_setup["analysis_id"] = self.analysis_id

        f_min = f_max = f_step = 0.

        if self.analysis_id in [0, 1, 3, 5, 6]:

            if self.analysis_id in [1, 6]:
                number_of_modes = self.check_inputs(self.lineEdit_modes, "'number of modes'")
                if self.stop:
                    self.lineEdit_modes.setFocus()
                    return True

            f_min = self.check_inputs(self.lineEdit_fmin, "'minimum frequency'", zero_included=True, _float=True)
            if self.stop:
                self.lineEdit_fmin.setFocus()
                return True

            f_max = self.check_inputs(self.lineEdit_fmax, "'maximum frequency'", _float=True)
            if self.stop:
                self.lineEdit_fmax.setFocus()
                return True

            f_step = self.check_inputs(self.lineEdit_fstep, "'frequency resolution (df)'", _float=True)
            if self.stop:
                self.lineEdit_fstep.setFocus()
                return True

            if f_max < f_min + f_step:
                self.hide()
                title = "Invalid frequency setup"
                message = "The maximum frequency (fmax) must be greater than \n"
                message += "the sum between minimum frequency (fmin) and \n"
                message += "frequency resolution (df)."
                PrintMessageInput([window_title, title, message])
                return True
            
            analysis_setup["f_min"] = f_min
            analysis_setup["f_max"] = f_max
            analysis_setup["f_step"] = f_step

        alpha_v = beta_v = alpha_h = beta_h = 0.0
        
        if self.analysis_id in [0, 1, 5, 6]:    

            alpha_v = self.check_inputs(self.lineEdit_av, "'proportional viscous damping (alpha_v)'", zero_included=True, _float=True)
            if self.stop:
                self.lineEdit_av.setFocus()
                return True

            beta_v = self.check_inputs(self.lineEdit_bv, "'proportional viscous damping (beta_v)'", zero_included=True,  _float=True)
            if self.stop:
                self.lineEdit_bv.setFocus()
                return True

            alpha_h = self.check_inputs(self.lineEdit_ah, "'proportional hysteretic damping (alpha_h)'", zero_included=True, _float=True)
            if self.stop:
                self.lineEdit_ah.setFocus()
                return True

            beta_h = self.check_inputs(self.lineEdit_bh, "'proportional hysteretic damping (beta_h)'", zero_included=True,  _float=True)
            if self.stop:
                self.lineEdit_bh.setFocus()
                return True

        analysis_setup["global_damping"] = [alpha_v, beta_v, alpha_h, beta_h]
        # self.model.set_global_damping(analysis_setup)

        if app().project.model.properties.check_if_there_are_tables_at_the_model():
            self.frequencies = self.model.frequencies
        else:
            self.model.set_frequency_setup(analysis_setup)

        if self.analysis_id in [1, 6]:
            analysis_setup["modes"] = number_of_modes

        app().file.write_analysis_setup_in_file(analysis_setup)

        self.project.set_analysis_data(analysis_setup)
        self.project.create_solver()

        self.complete = True
        app().main_window.analysis_toolbar.update_pushbutton_run_analysis()
        self.close()

        return False

    def check_inputs(self, lineEdit, label, only_positive=True, zero_included=False, _float=False):
        self.stop = False
        message = ""
        title = "Invalid input to the analysis setup"
        if lineEdit.text() != "":
            try:
                if _float:
                    out = float(lineEdit.text())
                else:
                    out = int(lineEdit.text())

                if only_positive:
                    if zero_included:
                        if out < 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is allowed."
                    else:
                        if out <= 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is not allowed."

            except Exception as _err:
                message = "Dear user, you have typed and invalid value at the \n"
                message += f"{label} input field.\n\n"
                message += str(_err)

        else:
            if zero_included:
                return float(0)
            else:
                message = f"Insert some value at the {label} input field."

        if message != "":
            self.hide()
            PrintMessageInput([window_title, title, message])
            self.stop = True
            return None
        return out

    def check_run(self):
        if self.enter_setup_callback():
            return
        self.solve_analysis = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_run()
        elif event.key() == Qt.Key_Escape:
            self.close()