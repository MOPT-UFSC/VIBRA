import configparser
import os
from pathlib import Path

import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QPushButton, QTabWidget, QWidget
from vibra.interface.general.call_double_confirmation_input import CallDoubleConfirmationInput

from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.interface_functions import get_main_window

window_title_1 = "ERROR"
window_title_2 = "WARNING"


class LowReducedFrequencyEquivalentModelInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path("data/ui_files/model/acoustic/lrf_eq_model_inputs.ui"), self)

        icon_path = str(Path("data/icons/logo_vibra.png"))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set the low reduced frequency eq. model")

        self.main_window = get_main_window()
        self.main_window.set_input_widget(self)
        self.project = self.main_window.project
        self.main_window.viewer_tabs.show_geometry()

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
        # QComboBox objects
        self.comboBox_selection_type = self.findChild(QComboBox, 'comboBox_selection_type')
        # QLineEdit objects
        self.lineEdit_selection_id = self.findChild(QLineEdit, "lineEdit_selection_id")
        self.lineEdit_diameter = self.findChild(QLineEdit, "lineEdit_diameter")
        # QPushButton objects
        self.pushButton_confirm = self.findChild(QPushButton, "pushButton_confirm")
        self.pushButton_remove = self.findChild(QPushButton, "pushButton_remove")
        self.pushButton_reset = self.findChild(QPushButton, "pushButton_reset")
        # QTabWidget objects
        self.tabWidget_lrf_model = self.findChild(QTabWidget, "tabWidget_lrf_model")
        self.tab_setup = self.tabWidget_lrf_model.findChild(QWidget, "tab_setup")
        self.current_tab = self.tabWidget_lrf_model.currentIndex()

    def _create_connections(self):
        self.pushButton_confirm.clicked.connect(self.set_lrf_eq_model_data)
        self.pushButton_remove.clicked.connect(self.remove_lrf_eq_model_inputs)
        self.pushButton_reset.clicked.connect(self.reset_lrf_eq_model_inputs)
        #
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)

    def geometry_selection_callback(self, points, lines, faces, volumes):
        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_selection_type.setCurrentIndex(1)
        
        elif volumes:
            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_selection_type.setCurrentIndex(0)

        elif not any([points, lines, faces]):
            self.lineEdit_selection_id.setText("")

    def remove_lrf_eq_model_inputs(self):
        pass

    def reset_lrf_eq_model_inputs(self):
        pass

    def check_lrf_eq_model_entries(self):
        
        selection_id = self.lineEdit_selection_id.text()
        if self.comboBox_selection_type.currentIndex() == 0:
            self.stop, self.volume_ids = self.check_input_volume_id(selection_id)
        else:
            self.stop, self.surface_ids_ids = self.check_input_surface_id(selection_id)

        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return True
        
        #TODO: get volumes inside surfaces boundaries if selection by surfaces was enabled
        # tab_index = self.tabWidget_lrf_model.currentIndex()
        lineEdit = self.lineEdit_diameter
        self.diameter = self.check_inputs(lineEdit, "Diameter", only_positive=True)
        if self.stop:
            lineEdit.setFocus()
            return True

    def set_lrf_eq_model_data(self):
        
        if self.check_lrf_eq_model_entries():
            return
        
        index = self.comboBox_selection_type.currentIndex()
        if index == 0:

            data = {"diameter" : self.diameter}
            for _id in self.volume_ids:
                self.project.set_lrf_eq_model_data(data, volume=_id)

        else:

            data = {"diameter" : self.diameter}
            for _id in self.surface_ids:
                self.project.set_lrf_eq_model_data(data, surface=_id)

        # print(f"The lrf eq. model has been attributed to volumes: {self.typed_ids}")
        self.close()

    def check_input_surface_id(self, lineEdit, single_ID=False):
        try:
            title = "Invalid entry to the Surface ID"
            message = ""
            tokens = lineEdit.strip().split(",")
            self.surface_ids = self.project.model.mesh.nodes_from_surfaces.keys()

            try:
                tokens.remove("")
            except:
                pass

            _size = len(self.surface_ids)
            list_ids = list(map(int, tokens))

            if len(list_ids) == 0:
                message = "An empty input field for the Surface ID has been detected. Please, enter a valid Surface ID to proceed."

            elif len(list_ids) >= 1:
                if single_ID and len(list_ids) > 1:
                    message = "Multiple Selected IDs"
                else:
                    try:
                        for _id in list_ids:
                            if _id not in self.surface_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                                message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                                break
                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                        message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
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

    def check_input_volume_id(self, lineEdit, single_ID=False):
        try:
            title = "Invalid entry to the Volume ID"
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
                message = "An empty input field for the Volume ID has been detected. Please, enter a valid Volume ID to proceed."

            elif len(list_ids) >= 1:
                if single_ID and len(list_ids) > 1:
                    message = "Multiple Selected IDs"
                else:
                    try:
                        for _id in list_ids:
                            if _id not in self.volume_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                                message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                                break
                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                        message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
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

    def check_inputs(self, lineEdit, label, only_positive=True, zero_included=False, _float=True):
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
