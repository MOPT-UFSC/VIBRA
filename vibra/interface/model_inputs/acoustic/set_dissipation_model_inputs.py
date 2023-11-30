import configparser
import os
from pathlib import Path

import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from vibra.interface.general.call_double_confirmation_input import CallDoubleConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.interface_functions import get_main_window

window_title_1 = "ERROR"
window_title_2 = "WARNING"


class DissipationModelInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path("data/ui_files/model/acoustic/dissipation_model_inputs.ui"), self)

        icon_path = str(Path("data/icons/logo_vibra.png"))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set the dissipation model")

        self.main_window = get_main_window()
        self.main_window.set_input_widget(self)
        self.project = self.main_window.project

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.exec()

    def _reset_variables(self):
        self.typed_ids = []
        self.model = ""
        self.speed_of_sound_factor = 0
        self.fluid_density_factor = 0

    def _define_qt_variables(self):
        # QLineEdit objects
        self.lineEdit_selection_id = self.findChild(QLineEdit, "lineEdit_selection_id")
        self.lineEdit_fluid_density_complex_factor = self.findChild(
            QLineEdit, "lineEdit_fluid_density_complex_factor"
        )
        self.lineEdit_speed_of_sound_complex_factor = self.findChild(
            QLineEdit, "lineEdit_speed_of_sound_complex_factor"
        )
        # QPushButton objects
        self.pushButton_confirm_proportional_damping = self.findChild(
            QPushButton, "pushButton_confirm_proportional_damping"
        )
        # QTabWidget objects
        self.tabWidget_dissipation_model = self.findChild(QTabWidget, "tabWidget_dissipation_model")
        self.tab_proportional_damping = self.tabWidget_dissipation_model.findChild(
            QWidget, "tab_proportional_damping"
        )
        self.current_tab = self.tabWidget_dissipation_model.currentIndex()

    def _create_connections(self):
        #
        self.pushButton_confirm_proportional_damping.clicked.connect(self.set_dissipation_model)

    def check_dissipation_model_entries(self):
        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.typed_ids = self.check_input_volume_id(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return True

        tab_index = self.tabWidget_dissipation_model.currentIndex()
        if tab_index == 0:
            self.model = "proportional damping"
            #
            lineEdit = self.lineEdit_speed_of_sound_complex_factor
            self.speed_of_sound_factor = self.check_inputs(
                lineEdit, "Speed of sound complex factor", only_positive=True
            )
            if self.stop:
                lineEdit.setFocus()
                return True
            #
            lineEdit = self.lineEdit_fluid_density_complex_factor
            self.fluid_density_factor = self.check_inputs(
                lineEdit, "Fluid density complex factor", only_positive=True
            )
            if self.stop:
                lineEdit.setFocus()
                return True
        else:
            print("Not implemented dissipation model.")

    def set_dissipation_model(self):
        if self.check_dissipation_model_entries():
            return

        data = {
            "entity_ids": self.typed_ids,
            "model": self.model,
            "speed of sound factor": self.speed_of_sound_factor,
            "fluid density factor": self.fluid_density_factor,
        }

        self.project.set_dissipation_model(data)
        # print(f"The dissipation model has been attributed to volumes: {self.typed_ids}")
        self.close()

    def check_input_volume_id(self, lineEdit, single_ID=False):
        try:
            title = "Invalid entry to the Surface ID"
            message = ""
            tokens = lineEdit.strip().split(",")
            self.volume_ids = self.project.model.mesh.nodes_from_volumes.keys()

            try:
                tokens.remove("")
            except:
                pass

            _size = len(self.volume_ids)
            list_ids = list(map(int, tokens))

            if len(list_ids) == 0:
                message = "An empty input field for the Surface ID has been detected. Please, enter a valid Surface ID to proceed."

            elif len(list_ids) >= 1:
                if single_ID and len(list_ids) > 1:
                    message = "Multiple Selected IDs"
                else:
                    try:
                        for _id in list_ids:
                            if _id not in self.volume_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                                message += f"The input value(s) must be integer(s) number(s) N such that 1 <= N <= {_size}."
                                break
                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                        message += f"The input value(s) must be integer(s) number(s) N such that 1 <= N <= {_size}."
                        message += f"\n\n{str(error_log)}"

        except Exception as log_error:
            message = "Wrong input for the Selected ID's. "
            message += f"\n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([title, message, window_title_1])
            return True, []

        if single_ID:
            return False, list_ids[0]
        else:
            return False, list_ids

    def check_inputs(self, lineEdit, label, only_positive=False, zero_included=True, _float=True):
        self.stop = False
        message = ""
        title = "Invalid input to the analysis setup"
        window_title = "ERROR"
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
            PrintMessageInput([title, message, window_title])
            self.stop = True
            return None
        return out
