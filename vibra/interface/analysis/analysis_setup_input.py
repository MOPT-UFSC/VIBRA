from pathlib import Path

import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QTabWidget

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.general.print_message_input import PrintMessageInput

window_title_1 = "Error"


class AnalysisSetupInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = app().main_window
        self.project = self.main_window.project

        self.analysis_data = self.project.analysis_data
        self.analysis_id = self.analysis_data["analysis_id"]
        self.imported_table_state = self.main_window.project.imported_table_state

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

        if self.analysis_id in [1, 6]:
            ui_path = UI_DIR / "analysis/structural/harmonic_analysis_mode_superposition_method.ui"
        elif self.analysis_id in [0, 5]:
            ui_path = UI_DIR / "analysis/structural/harmonic_analysis_direct_method.ui"
        elif self.analysis_id in [3]:
            ui_path = UI_DIR / "analysis/acoustic/harmonic_analysis_direct_method.ui"
        else:
            return

        uic.loadUi(ui_path, self)

        self._config_window()
        self._reset_variables()
        self._load_analysis_data()
        self._define_qt_variables()
        self._create_connections()
        self._update_fmin()

        ConfigWidgetAppearance(self)

        self.update_frequency_setup_input_texts()
        self.update_damping_input_texts()
        self.exec_()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.main_window.vibra_icon)
        self.setWindowTitle("Analysis setup")

    def _reset_variables(self):
        self.complete = False
        self.solve_analysis = False
        self.frequencies = []
        self.global_damping = [0, 0, 0, 0]
        self.f_step = 0

    def _define_qt_variables(self):
        # QLabel
        self.label_title : QLabel
        self.label_subtitle : QLabel

        if self.analysis_id == 1:
            self.lineEdit_modes : QLineEdit

        self.lineEdit_av : QLineEdit
        self.lineEdit_bv : QLineEdit
        self.lineEdit_ah : QLineEdit
        self.lineEdit_bh : QLineEdit

        self.lineEdit_fmin : QLineEdit
        self.lineEdit_fmax : QLineEdit
        self.lineEdit_fstep : QLineEdit

        self.pushButton_confirm_close : QPushButton
        self.pushButton_confirm_run_analysis : QPushButton

        self.tabWidget : QTabWidget
        self.currentTab = self.tabWidget.currentIndex()

    def _create_connections(self):
        self.pushButton_confirm_close.clicked.connect(self.check_exit)
        self.pushButton_confirm_run_analysis.clicked.connect(self.check_run)
        self.tabWidget.currentChanged.connect(self.tabEvent)

    def _update_fmin(self):
        df = self.lineEdit_fstep.text()
        self.lineEdit_fmin.setText(df)

    def _load_analysis_data(self):
        data = self.project.analysis_data

        if "analysis_type" in data.keys():
            title = data["analysis_type"] + " Setup"

        if "analysis_method_label" in data.keys():
            subtitle = data["analysis_method_label"]

        self.label_title.setText(title)
        self.label_subtitle.setText(subtitle)

        if "f_min" in data.keys():
            self.f_min = data["f_min"]

        if "f_max" in data.keys():
            self.f_max = data["f_max"]

        if "f_step" in data.keys():
            self.f_step = data["f_step"]

        if "global_damping" in data.keys():
            self.global_damping = data["global_damping"]

        if "modes" in data.keys():
            self.modes = data["modes"]

        if "imported_table" in data.keys():
            _bool = data["imported_table"]
            self.lineEdit_fmax.setDisabled(_bool)
            self.lineEdit_fmin.setDisabled(_bool)
            self.lineEdit_fstep.setDisabled(_bool)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_run()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def tabEvent(self):
        self.currentTab = self.tabWidget.currentIndex()

    def update_damping_input_texts(self):
        if self.analysis_id not in [2, 3, 4]:
            if self.global_damping != [0, 0, 0, 0]:
                self.lineEdit_av.setText(str(self.global_damping[0]))
                self.lineEdit_bv.setText(str(self.global_damping[1]))
                self.lineEdit_ah.setText(str(self.global_damping[2]))
                self.lineEdit_bh.setText(str(self.global_damping[3]))

    def update_frequency_setup_input_texts(self):
        if self.f_step != 0:
            self.lineEdit_fmin.setText(str(self.f_min))
            self.lineEdit_fmax.setText(str(self.f_max))
            self.lineEdit_fstep.setText(str(self.f_step))
            if self.project.imported_table_state:
                self.lineEdit_fmin.setDisabled(True)
                self.lineEdit_fmax.setDisabled(True)
                self.lineEdit_fstep.setDisabled(True)

    def check_exit(self):
        input_fmin = input_fmax = input_fstep = 0
        if self.analysis_id not in [2, 4]:
            if self.analysis_id == 1:
                self.modes = self.check_inputs(self.lineEdit_modes, "'number of modes'")
                if self.stop:
                    self.lineEdit_modes.setFocus()
                    return True

            input_fmin = self.check_inputs(self.lineEdit_fmin, "'minimum frequency'", zero_included=False, _float=True)
            if self.stop:
                self.lineEdit_fmin.setFocus()
                return True

            input_fmax = self.check_inputs(self.lineEdit_fmax, "'maximum frequency'", _float=True)
            if self.stop:
                self.lineEdit_fmax.setFocus()
                return True

            input_fstep = self.check_inputs(self.lineEdit_fstep, "'frequency resolution (df)'", _float=True)
            if self.stop:
                self.lineEdit_fstep.setFocus()
                return True

            if input_fmax < input_fmin + input_fstep:
                title = "Invalid frequency setup"
                message = "The maximum frequency (fmax) must be greater than \n"
                message += "the sum between minimum frequency (fmin) and \n"
                message += "frequency resolution (df)."
                PrintMessageInput([window_title_1, title, message])
                return True

        alpha_v = beta_v = alpha_h = beta_h = 0.0

        if self.analysis_id in [0, 1, 5, 6]:
            alpha_v = self.check_inputs(
                self.lineEdit_av,
                "'proportional viscous damping (alpha_v)'",
                zero_included=True,
                _float=True,
            )
            if self.stop:
                self.lineEdit_av.setFocus()
                return True

            beta_v = self.check_inputs(
                self.lineEdit_bv,
                "'proportional viscous damping (beta_v)'",
                zero_included=True,
                _float=True,
            )
            if self.stop:
                self.lineEdit_bv.setFocus()
                return True

            alpha_h = self.check_inputs(
                self.lineEdit_ah,
                "'proportional hysteretic damping (alpha_h)'",
                zero_included=True,
                _float=True,
            )
            if self.stop:
                self.lineEdit_ah.setFocus()
                return True

            beta_h = self.check_inputs(
                self.lineEdit_bh,
                "'proportional hysteretic damping (beta_h)'",
                zero_included=True,
                _float=True,
            )
            if self.stop:
                self.lineEdit_bh.setFocus()
                return True

        self.global_damping = [alpha_v, beta_v, alpha_h, beta_h]

        # TODO: in the future it will be necessary check all existing tables to avoid frequencies "misalignments"
        self.frequencies = np.arange(input_fmin, input_fmax + input_fstep, input_fstep)

        self.analysis_data["f_min"] = input_fmin
        self.analysis_data["f_max"] = input_fmax
        self.analysis_data["f_step"] = input_fstep
        self.analysis_data["frequencies"] = self.frequencies
        # self.analysis_data["global_damping"] = self.global_damping

        # if not self.analysis_id in [3, 4]:
        #     self.project.set_modes_sigma(self.modes)

        self.project.set_analysis_data(self.analysis_data)
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
            PrintMessageInput([window_title_1, title, message])
            self.stop = True
            return None
        return out

    def check_run(self):
        if self.check_exit():
            return
        self.solve_analysis = True
