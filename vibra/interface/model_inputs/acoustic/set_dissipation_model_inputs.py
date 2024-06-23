
from PyQt5.QtWidgets import QComboBox, QDialog, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

import configparser
import os
from pathlib import Path

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class DissipationModelInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/dissipation_model_inputs.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)

        self.project = self.main_window.project
        self.model = self.project.model
        self.properties = self.model.properties

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.load_info()

        ConfigWidgetAppearance(self, tool_tip=True)

        while self.keep_window_open:
            self.exec()

    def _load_icons(self):
        self.vibra_icon = app().main_window.vibra_icon

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.vibra_icon)
        self.setWindowTitle("Set the dissipation model")

    def _initialize(self):
        self.typed_ids = []
        self.model = ""
        self.speed_of_sound_factor = 0
        self.fluid_density_factor = 0
        self.keep_window_open = True

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type : QComboBox

        # QLineEdit
        self.lineEdit_selected_id : QLineEdit
        self.lineEdit_fluid_density_complex_factor : QLineEdit
        self.lineEdit_speed_of_sound_complex_factor : QLineEdit

        # QPushButton
        self.pushButton_confirm_proportional_damping : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton

        # QTabWidget
        self.tabWidget_dissipation_model : QTabWidget

        # QTreeWidget
        self.treeWidget_dissipation_model : QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.update_attribution_type)
        #
        self.pushButton_confirm_proportional_damping.clicked.connect(self.set_dissipation_model)
        self.pushButton_remove.clicked.connect(self.remove_dissipation_model)
        self.pushButton_reset.clicked.connect(self.reset_dissipation_model)
        #
        self.tabWidget_dissipation_model.currentChanged.connect(self.tabEvent_dissipation_model)
        #
        self.treeWidget_dissipation_model.itemClicked.connect(self.on_click_item)
        self.treeWidget_dissipation_model.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)
        #
        self.update_attribution_type()

    def remove_dissipation_model(self):
        if self.lineEdit_selected_id.text() != "":
            volume_id = int(self.lineEdit_selected_id.text())
            self.properties._remove_volume_property("dissipation_model", volume_id)
            self.load_info()

    def reset_dissipation_model(self):

        volume_ids = list()
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "dissipation_model":
                volume_ids.append(volume_id)

        if volume_ids:

            self.hide()

            title = f"Dissipation model resetting"
            message = "Would you like to remove the dissipation model effects?"

            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:
                for volume_id in volume_ids:
                    self.properties._remove_volume_property("dissipation_model", volume_id)
                self.close()

    def tabEvent_dissipation_model(self):
        tab_index = self.tabWidget_dissipation_model.currentIndex()
        self.comboBox_attribution_type.setDisabled(bool(tab_index))
        if tab_index == 1:
            self.lineEdit_selected_id.setText("")
            self.lineEdit_selected_id.setDisabled(True)
        else:
            self.lineEdit_selected_id.setDisabled(False)

    def on_click_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        # self.remove_bc_from_selection()

    def update_attribution_type(self):

        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selected_id.setText("All bodies")
        elif index == 1:
            self.lineEdit_selected_id.setText("")

        self.lineEdit_selected_id.setEnabled(bool(index))
        # self.comboBox_attribution_type.setCurrentIndex(index)

    def update_tabs_visibility(self):

        volume_with_dissipation_model = list()
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "dissipation_model":
                volume_with_dissipation_model.append(volume_id)

        if volume_with_dissipation_model:
            self.tabWidget_dissipation_model.setTabVisible(1, True)
        else:
            self.tabWidget_dissipation_model.setTabVisible(1, False)

    def load_info(self):

        self.treeWidget_dissipation_model.clear()
        self.treeWidget_dissipation_model.setColumnWidth(0, 80)
        self.treeWidget_dissipation_model.setColumnWidth(1, 160)

        for key, data in self.properties.volume_properties.items():

            property, volume_id = key

            if property == "dissipation_model":

                model = data["model"]

                factors = list()
                factors.append(data["speed of sound factor"])
                factors.append(data["fluid density factor"])

                new = QTreeWidgetItem([str(volume_id), model, str(factors)])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_dissipation_model.addTopLevelItem(new)

        self.update_tabs_visibility()

    def geometry_selection_callback(self, points, lines, faces, volumes):
        """ """
        if volumes:

            if self.comboBox_attribution_type.currentIndex() == 0:
                return

            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selected_id.setText(text)

        elif not any([points, lines, faces]):
            return

    def check_dissipation_model_entries(self):

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

        if self.comboBox_attribution_type.currentIndex():

            lineEdit_selected_id = self.lineEdit_selected_id.text()
            self.stop, self.typed_ids = self.check_input_volume_id(lineEdit_selected_id)
            if self.stop:
                self.lineEdit_selected_id.setFocus()
                return True
            
            volume_ids = self.typed_ids

        else:

            volume_ids = list(self.project.model.mesh.nodes_from_volumes.keys())


        if self.check_dissipation_model_entries():
            return

        data = {
                "entity_ids": volume_ids,
                "model": self.model,
                "speed of sound factor": self.speed_of_sound_factor,
                "fluid density factor": self.fluid_density_factor,
                }

        for volume_id in volume_ids:
            if volume_id in list(self.project.model.mesh.nodes_from_volumes.keys()):
                self.project.set_dissipation_model(data, volume=volume_id)
        
        print(f"The dissipation model has been attributed to volumes: {volume_ids}")

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
            PrintMessageInput([window_title_1, title, message])
            return True, []

        if single_ID:
            return False, list_ids[0]
        else:
            return False, list_ids

    def check_inputs(self, lineEdit, label, only_positive=False, zero_included=True, _float=True):

        self.stop = False
        message = ""

        title = "Invalid input at dissipation model"
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

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)