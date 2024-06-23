import configparser
import os
from pathlib import Path

import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from vibra import app, UI_DIR
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"


class VolumeVelocityInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/volume_velocity_input.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.project = self.main_window.project
        self.model = self.project.model
        self.properties = self.model.properties

        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()

        self._reset_variables()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.load_info()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.main_window.vibra_icon)
        self.setWindowTitle("Set volume velocity acoustic excitation")

    def _reset_variables(self):
        self.typed_ids = []
        self.remove_volume_velocity = False
        self.volume_velocity = None
        self.userPath = os.path.expanduser("~")
        self.new_load_path_table = ""
        self.project_path = self.project.file.project_path
        self.acoustic_bc_filename = self.project.file.acoustic_model_setup_filename
        self.acoustic_bc_info_path = os.path.join(self.project_path, self.acoustic_bc_filename)
        self.acoustic_folder_path = self.project.file.acoustic_imported_data_folder_path
        self.volume_velocity_tables_folder_path = os.path.join( self.acoustic_folder_path, 
                                                                "volume_velocity_files" )

    def _define_qt_variables(self):
        # QCheckBox objects
        self.checkBox_averaged_constant_values = self.findChild(QCheckBox, "checkBox_averaged_constant_values")
        self.checkBox_averaged_table_values = self.findChild(QCheckBox, "checkBox_averaged_table_values")
        # QLineEdit objects
        self.lineEdit_selection_id = self.findChild(QLineEdit, "lineEdit_selection_id")
        self.lineEdit_real_value = self.findChild(QLineEdit, "lineEdit_real_value")
        self.lineEdit_imag_value = self.findChild(QLineEdit, "lineEdit_imag_value")
        self.lineEdit_load_table_path = self.findChild(QLineEdit, "lineEdit_table_path")
        # QPushButton objects
        self.pushButton_load_table = self.findChild(QPushButton, "pushButton_load_table")
        self.pushButton_constant_value_confirm = self.findChild(QPushButton, "pushButton_constant_value_confirm")
        self.pushButton_table_values_confirm = self.findChild(QPushButton, "pushButton_table_values_confirm")
        self.pushButton_remove_bc_confirm = self.findChild(QPushButton, "pushButton_remove_bc_confirm")
        self.pushButton_reset = self.findChild(QPushButton, "pushButton_reset")
        #
        self.radioButton_element_integration_constant.setDisabled(True)
        self.radioButton_element_integration_table.setDisabled(True)
        # QRadioButton objects
        self.radioButton_nodal_attribution_constant = self.findChild(QRadioButton, "radioButton_nodal_attribution_constant")
        self.radioButton_element_integration_constant = self.findChild(QRadioButton, "radioButton_element_integration_constant")
        self.radioButton_element_integration_table = self.findChild(QRadioButton, "radioButton_element_integration_table")
        self.radioButton_nodal_attribution_table = self.findChild(QRadioButton, "radioButton_nodal_attribution_table")
        # QSpinBox object
        self.spinBox_skiprows = self.findChild(QSpinBox, "spinBox")
        # QTabWidget objects
        self.tabWidget_volume_velocity = self.findChild(QTabWidget, "tabWidget_volume_velocity")
        self.tab_constant_values = self.tabWidget_volume_velocity.findChild(QWidget, "tab_constant_values")
        self.tab_table_values = self.tabWidget_volume_velocity.findChild(QWidget, "tab_table_values")
        self.tab_remove = self.tabWidget_volume_velocity.findChild(QWidget, "tab_remove")
        self.current_tab = self.tabWidget_volume_velocity.currentIndex()
        # QTreeWidget objects
        self.treeWidget_volume_velocity = self.findChild(QTreeWidget, "treeWidget_volume_velocity")
        self.treeWidget_volume_velocity.setColumnWidth(1, 20)
        self.treeWidget_volume_velocity.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.pushButton_constant_value_confirm.clicked.connect(self.check_constant_values)
        self.pushButton_remove_bc_confirm.clicked.connect(self.remove_bc_from_selection)
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)
        self.pushButton_load_table.clicked.connect(self.load_volume_velocity_table)
        self.pushButton_reset.clicked.connect(self.check_reset)
        #
        self.radioButton_nodal_attribution_constant.clicked.connect(self.update_controls_for_constant_value)
        self.radioButton_element_integration_constant.clicked.connect(self.update_controls_for_constant_value)
        self.radioButton_nodal_attribution_table.clicked.connect(self.update_controls_for_table_of_values)
        self.radioButton_element_integration_table.clicked.connect(self.update_controls_for_table_of_values)
        #
        self.tabWidget_volume_velocity.currentChanged.connect(self.tabEvent_volume_velocity)
        self.treeWidget_volume_velocity.itemClicked.connect(self.on_click_item)
        self.treeWidget_volume_velocity.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)

    def tabEvent_volume_velocity(self):
        self.current_tab = self.tabWidget_volume_velocity.currentIndex()
        if self.current_tab == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)

    def on_click_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))
        self.remove_bc_from_selection()

    def load_info(self):
        self.treeWidget_volume_velocity.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "volume_velocity":
                real_values = np.array(data["real_values"])
                imag_values = np.array(data["imag_values"])
                complex_values = real_values + 1j * imag_values
                new = QTreeWidgetItem([str(surface_id), str(self.text_label(complex_values))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_volume_velocity.addTopLevelItem(new)
        self.update_tabs_visibility()

    def geometry_selection_callback(self, points, lines, faces):
        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)

        elif not any([points, lines, faces]):
            self.lineEdit_selection_id.setText("")

    def check_complex_entries(self, lineEdit_real, lineEdit_imag):
        self.stop = False
        title = "Invalid entry to the volume velocity"
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                message = "Wrong input for real part of volume velocity."
                PrintMessageInput([window_title_1, title, message])
                self.lineEdit_real_value.setFocus()
                self.stop = True
                return
        else:
            real_F = 0

        if lineEdit_imag.text() != "":
            try:
                imag_F = float(lineEdit_imag.text())
            except Exception:
                message = "Wrong input for imaginary part of volume velocity."
                PrintMessageInput([window_title_1, title, message])
                self.lineEdit_imag_value.setFocus()
                self.stop = True
                return
        else:
            imag_F = 0

        if real_F == 0 and imag_F == 0:
            return None
        else:
            return real_F + 1j * imag_F

    def check_constant_values(self):
        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.typed_ids = self.model.check_input_surface_id(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return

        for _id in self.typed_ids:
            self.properties._remove_surface_property("acoustic_pressure", _id)
            self.properties._remove_surface_property("compressor_excitation", _id)

        volume_velocity = self.check_complex_entries(
            self.lineEdit_real_value, self.lineEdit_imag_value
        )

        if self.stop:
            return

        if volume_velocity is not None:
            self.volume_velocity = volume_velocity
            real_values = [np.real(volume_velocity)]
            imag_values = [np.imag(volume_velocity)]

            nodal_attribution = self.radioButton_nodal_attribution_constant.isChecked()
            key_avg = self.checkBox_averaged_constant_values.isChecked()

            data = {
                "real_values": real_values,
                "imag_values": imag_values,
                "nodal_attribution": nodal_attribution,
                "averaged": key_avg,
            }

            for _id in self.typed_ids:
                self.project.set_volume_velocity(data, _id)

            self.properties.export_model_properties()

            print(f"[Set Volume Velocity] - defined at surface(s) {self.typed_ids}")
            # TODO: remove existing tables and update the render
            self.close()

        else:
            title = "Additional inputs required"
            message = "You must inform at least one volume velocity\n"
            message += "before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_real_value.setFocus()

    def load_table(self, lineEdit, direct_load=False):
        title = "Error reached while loading 'volume velocity' table"
        try:
            if direct_load:
                self.path_imported_table = lineEdit.text()
            else:
                window_label = "Choose a table to import the volume velocity"
                self.path_imported_table, _ = QFileDialog.getOpenFileName(
                    None, window_label, self.userPath, "Files (*.csv; *.dat; *.txt)"
                )

            if self.path_imported_table == "":
                return None, None

            imported_filename = os.path.basename(self.path_imported_table)
            lineEdit.setText(self.path_imported_table)

            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")

            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have three columns in the form: frequencies, real and imaginary values."
                PrintMessageInput([window_title_1, title, message])
                return None, None

            imported_values = imported_file[:, 1]

            if imported_file.shape[1] >= 3:
                self.frequencies = imported_file[:, 0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0]
                self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)

                # TODO: ensure that the table frequency setup governing the model setup
                if self.change_project_frequency_setup(imported_filename, list(self.frequencies)):
                    self.lineEdit_reset(self.lineEdit_load_table_path)
                    return None, None
                else:
                    self.project.set_frequencies(
                        self.frequencies, self.f_min, self.f_max, self.f_step
                    )

            return imported_values, imported_filename

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            lineEdit.setFocus()
            return None, None

    def lineEdit_reset(self, lineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def save_table_file(self, entity_id, values, filename):
        try:
            self.project.file.create_folders_acoustic("volume_velocity_files")

            real_values = np.real(values)
            imag_values = np.imag(values)
            abs_values = np.abs(values)
            data = np.array([self.frequencies, real_values, imag_values, abs_values]).T

            header = f"Vibra - imported table for volume velocity @ surface {entity_id} \n"
            header += f"\nSource filename: {filename}\n"
            header += "\nFrequency [Hz], real[m³/s], imaginary[m³/s], absolute[m³/s]"
            basename = f"volume_velocity_surface_{entity_id}.dat"

            new_path_table = os.path.join(self.volume_velocity_tables_folder_path, basename)
            np.savetxt(new_path_table, data, delimiter=",", header=header)
            return values, basename

        except Exception as log_error:
            title = "Error reached while saving table files"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return None, None

    def load_volume_velocity_table(self):
        self.imported_values, self.filename_volume_velocity = self.load_table(
            self.lineEdit_load_table_path
        )

    def check_table_values(self):
        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.typed_ids = self.model.check_input_surface_id(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return

        for _id in self.typed_ids:
            self.properties._remove_surface_property("acoustic_pressure", _id)
            self.properties._remove_surface_property("compressor_excitation", _id)

        list_table_names = self.get_list_table_names_from_selected_surfaces(self.typed_ids)
        if self.lineEdit_load_table_path != "":
            for _id in self.typed_ids:
                if self.filename_volume_velocity is None:
                    self.imported_values, self.filename_volume_velocity = self.load_table(
                        self.lineEdit_load_table_path, direct_load=True
                    )
                if self.imported_values is None:
                    return
                else:
                    self.volume_velocity, self.basename_volume_velocity = self.save_table_file(
                        _id, self.imported_values, self.filename_volume_velocity
                    )
                    if self.basename_volume_velocity in list_table_names:
                        list_table_names.remove(self.basename_volume_velocity)

                    real_values = list(np.real(self.volume_velocity))
                    imag_values = list(np.imag(self.volume_velocity))

                    nodal_attribution = self.radioButton_nodal_attribution_table.isChecked()
                    key_avg = self.checkBox_averaged_constant_values.isChecked()

                    data = {
                        "real_values": real_values,
                        "imag_values": imag_values,
                        "nodal_attribution": nodal_attribution,
                        "averaged": key_avg,
                        "table_name": self.basename_volume_velocity,
                    }

                self.project.set_volume_velocity(data, _id)

            self.properties.export_model_properties()

            self.process_table_file_removal(list_table_names)
            print(f"[Set Volume Velocity] - defined at surface(s) {self.typed_ids}")
            self.close()
        else:
            title = "Additional inputs required"
            message = "You must inform at least one volume velocity\n"
            message += "table path before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_load_table_path.setFocus()

    def get_list_table_names_from_selected_surfaces(self, list_ids):
        list_table_names = []
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "volume_velocity":
                if surface_id in list_ids:
                    if "table_name" in data.keys():
                        list_table_names.append(data["table_name"])
        return list_table_names

    def text_label(self, value):
        if value.shape[0] == 1:
            value_label = str(value)
        else:
            value_label = "Table"
        return "{}".format(value_label)

    def remove_bc_from_selection(self):
        if self.lineEdit_selection_id.text() != "":
            surface_properties = self.properties.surface_properties.copy()
            picked_id = int(self.lineEdit_selection_id.text())
            for key in surface_properties.keys():
                property, surface_id = key
                if property == "volume_velocity" and picked_id == surface_id:
                    # TODO: remove imported volume velocity tables
                    list_table_names = self.get_list_table_names_from_selected_surfaces([picked_id])
                    self.process_table_file_removal(list_table_names)
                    self.properties._remove_surface_property("volume_velocity", picked_id)
                    self.load_info()
                    self.lineEdit_selection_id.setText("")
                    return

    def process_table_file_removal(self, list_table_names):
        if list_table_names != []:
            for table_name in list_table_names:
                self.project.remove_acoustic_table_files_from_folder(
                    table_name, "volume_velocity_files"
                )

    def check_reset(self):
        surface_ids = []
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "volume_velocity":
                surface_ids.append(surface_id)

        if surface_ids:

            title = f"Resetting of all applied volume velocities"

            message = "Would you like to remove the volume velocity applied to the following surface(s)?\n\n"
            message += f"{surface_ids}"

            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            _list_table_names = []
            if read._continue:
                for key, data in self.properties.surface_properties.items():
                    property, surface_id = key
                    if property == "volume_velocity":
                        if "table_name" in data.keys():
                            table_name = data[table_name]
                        else:
                            table_name = None
                        if table_name is not None:
                            if table_name not in _list_table_names:
                                _list_table_names.append(table_name)

                self.properties._reset_property("volume_velocity")
                self.properties.export_model_properties()

                # TODO: remove imported tables
                self.process_table_file_removal(_list_table_names)

                title = "Volume velocity resetting process complete"
                message = "All volume velocity applied to the acoustic "
                message += "model have been removed from the model."
                PrintMessageInput([window_title_2, title, message])

                self.close()

    def reset_input_fields(self):
        self.lineEdit_real_value.setText("")
        self.lineEdit_imag_value.setText("")
        self.lineEdit_load_table_path.setText("")

    def update_controls_for_constant_value(self):
        _bool = self.radioButton_element_integration_constant.isChecked()
        self.checkBox_averaged_constant_values.setChecked(not _bool)
        self.checkBox_averaged_constant_values.setDisabled(_bool)

    def update_controls_for_table_of_values(self):
        _bool = self.radioButton_element_integration_table.isChecked()
        self.checkBox_averaged_table_values.setChecked(not _bool)
        self.checkBox_averaged_table_values.setDisabled(_bool)

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        if self.current_tab != 2:
            self.lineEdit_selection_id.setText(text[:-2])

    def update_tabs_visibility(self):
        surface_ids = []
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "volume_velocity":
                surface_ids.append(surface_id)

        if len(surface_ids) == 0:
            self.tabWidget_volume_velocity.setTabVisible(2, False)
        else:
            self.tabWidget_volume_velocity.setTabVisible(2, True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_volume_velocity.currentIndex() == 0:
                self.check_constant_values()
            if self.tabWidget_volume_velocity.currentIndex() == 1:
                self.check_table_values()
        elif event.key() == Qt.Key_Delete:
            if self.tabWidget_volume_velocity.currentIndex() == 2:
                self.remove_bc_from_selection()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            return

    def change_project_frequency_setup(self, table_name, frequencies):
        self.list_frequencies = []
        analysis_data = self.main_window.project.analysis_data
        if analysis_data is not None:
            if "frequencies" in analysis_data.keys():
                if isinstance(analysis_data["frequencies"], np.ndarray):
                    self.list_frequencies = list(analysis_data["frequencies"])

        if frequencies is None:
            return False
        if isinstance(frequencies, np.ndarray):
            frequencies = list(frequencies)
        update_freqs = False
        if (
            self.list_frequencies == []
            or not self.properties.check_if_there_are_tables_at_the_model()
        ):
            update_freqs = True
            self.list_frequencies = frequencies
        #
        self.main_window.project.update_import_table_state(update_freqs)
        if self.list_frequencies == frequencies:
            if update_freqs:
                self.frequencies = np.array(frequencies)
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0]
                # self.file.add_frequency_in_file(self.f_min, self.f_max, self.f_step)
                self.imported_table_frequency_setup = True
            return False

        else:
            title = "Project frequency setup cannot be modified"
            message = f"The following imported table of values has a frequency setup\n"
            message += "different from the others already imported ones. The current\n"
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([window_title_2, title, message])
            return True
