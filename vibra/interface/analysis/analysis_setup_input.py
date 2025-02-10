from pathlib import Path

import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QTabWidget

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.general.print_message_input import PrintMessageInput

window_title = "Error"


class AnalysisSetupInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = app().main_window
        self.project = app().project

        self.analysis_data = self.project.analysis_data
        self.analysis_id = self.analysis_data["analysis_id"]

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

        if self.analysis_id in [0, 5]:
            ui_path = UI_DIR / "analysis/structural/harmonic_analysis_direct_method.ui"

        elif self.analysis_id in [1, 6]:
            ui_path = UI_DIR / "analysis/structural/harmonic_analysis_mode_superposition_method.ui"

        elif self.analysis_id in [3]:
            ui_path = UI_DIR / "analysis/acoustic/harmonic_analysis_direct_method.ui"

        else:
            return

        uic.loadUi(ui_path, self)

        self.model = app().project.model

        self._config_window()
        self._reset_variables()

        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self)

        self.update_frequency_setup_inputs()
        self.update_damping_inputs()
        # self._update_fmin()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.main_window.vibra_icon)
        self.setWindowTitle("Analysis setup")

    def _reset_variables(self):
        self.keep_window_open = True
        self.complete = False
        self.solve_analysis = False
        self.frequencies = []
        self.global_damping = [0, 0, 0, 0]
        self.f_step = 0

    def _define_qt_variables(self):

        # QLabel
        self.label_title : QLabel
        self.label_subtitle : QLabel

        # QLineEdit
        if self.analysis_id in [1, 6]:
            self.lineEdit_modes : QLineEdit

        self.lineEdit_av : QLineEdit
        self.lineEdit_bv : QLineEdit
        self.lineEdit_ah : QLineEdit
        self.lineEdit_bh : QLineEdit

        self.lineEdit_fmin : QLineEdit
        self.lineEdit_fmax : QLineEdit
        self.lineEdit_fstep : QLineEdit

        # QPushButton
        self.pushButton_enter_setup : QPushButton
        self.pushButton_run_analysis : QPushButton

        # QTabWidget
        self.tabWidget : QTabWidget

    def _create_connections(self):
        #
        self.pushButton_enter_setup.clicked.connect(self.enter_setup_callback)
        self.pushButton_run_analysis.clicked.connect(self.check_run)

    def _update_fmin(self):
        df = self.lineEdit_fstep.text()
        self.lineEdit_fmin.setText(df)

    # def _load_analysis_data(self):

    #     analysis_setup = app().file.read_analysis_setup_from_file()
    #     if analysis_setup is None:
    #         return
        
    #     if "analysis_id" in analysis_setup.keys():

    #         analysis_id = analysis_setup["analysis_id"]

    #         if analysis_id in [0, 1]:
    #             title = "Structural Harmonic Analysis Setup"
    #         elif analysis_id == 2:
    #             title = "Structural Modal Analysis"
    #         elif analysis_id == 3:
    #             title = "Acoustic Harmonic Analysis Setup"
    #         elif analysis_id == 4:
    #             title = "Acoustic Modal Analysis"
    #         elif analysis_id in [5, 6]:
    #             title = "Coupled Harmonic Analysis Setup"

    #         if analysis_id in [0, 3, 5]:
    #             subtitle = "Direct Method"
    #         elif analysis_id in [1, 6]:
    #             subtitle = "Mode Superposition Method"

    #     self.label_title.setText(title)
    #     self.label_subtitle.setText(subtitle)

    def update_damping_inputs(self):
        if self.analysis_id not in [2, 3, 4]:
            if self.global_damping != [0, 0, 0, 0]:
                self.lineEdit_av.setText(str(self.global_damping[0]))
                self.lineEdit_bv.setText(str(self.global_damping[1]))
                self.lineEdit_ah.setText(str(self.global_damping[2]))
                self.lineEdit_bh.setText(str(self.global_damping[3]))

    def update_frequency_setup_inputs(self):

        if (self.model.f_min, self.model.f_max, self.model.f_step).count(None):
            f_min = 2
            f_max = 600
            f_step = 2

        else:

            f_min = self.model.f_min
            f_max = self.model.f_max
            f_step = self.model.f_step

            # if f_min == 0:
            #     f_min = f_step

        if f_step:

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

        if self.analysis_id not in [2, 4]:

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

        global_damping = [alpha_v, beta_v, alpha_h, beta_h]
        analysis_setup["global_damping"] = global_damping
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

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_run()
        elif event.key() == Qt.Key_Escape:
            self.close()