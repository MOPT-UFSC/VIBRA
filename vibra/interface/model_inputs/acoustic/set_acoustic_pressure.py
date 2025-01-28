# fmt: off

from PySide6.QtWidgets import QCheckBox, QDialog, QFileDialog, QLineEdit, QPushButton, QRadioButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.model_inputs.data_filter.change_frequency_data_handler import ChangeFrequencyDataRangeInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

from molde import load_ui

import os
import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class AcousticPressureInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/acoustic_pressure_input.ui"
        load_ui(ui_path, self, UI_DIR)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()

        self.project = app().main_window.project
        self.model = app().main_window.project.model
        self.mesh = app().main_window.project.model.mesh
        self.properties = app().main_window.project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

        self.load_info()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.typed_ids = list()
        self.keep_window_open = True
        self.imported_values = None

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_averaged_constant_values : QCheckBox
        self.checkBox_averaged_table_values : QCheckBox

        # QLineEdit
        self.lineEdit_selection_id : QLineEdit
        self.lineEdit_real_value : QLineEdit
        self.lineEdit_imag_value : QLineEdit
        self.lineEdit_table_path : QLineEdit

        # QPushButton
        self.pushButton_constant_value_confirm : QPushButton
        self.pushButton_change_frequency_setup : QPushButton
        self.pushButton_load_table : QPushButton
        self.pushButton_remove_bc_confirm : QPushButton
        self.pushButton_reset : QPushButton
        self.pushButton_table_values_confirm : QPushButton
        #
        self.pushButton_change_frequency_setup.setDisabled(True)

        # QRadioButton
        self.radioButton_nodal_attribution_constant : QRadioButton
        self.radioButton_element_integration_constant : QRadioButton
        self.radioButton_element_integration_table : QRadioButton
        self.radioButton_nodal_attribution_table : QRadioButton
        #
        self.radioButton_element_integration_constant.setDisabled(True)
        self.radioButton_element_integration_table.setDisabled(True)

        # QTabWidget
        self.tabWidget_acoustic_pressure : QTabWidget

        # QTreeWidget
        self.treeWidget_acoustic_pressure : QTreeWidget
        self.treeWidget_acoustic_pressure.setColumnWidth(1, 20)
        self.treeWidget_acoustic_pressure.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.pushButton_constant_value_confirm.clicked.connect(self.check_constant_values)
        self.pushButton_remove_bc_confirm.clicked.connect(self.remove_bc_from_selection)
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)
        self.pushButton_load_table.clicked.connect(self.load_acoustic_pressure_table)
        self.pushButton_reset.clicked.connect(self.check_reset)
        #
        self.radioButton_nodal_attribution_constant.clicked.connect(self.update_controls_for_constant_value)
        self.radioButton_element_integration_constant.clicked.connect(self.update_controls_for_constant_value)
        self.radioButton_nodal_attribution_table.clicked.connect(self.update_controls_for_table_of_values)
        self.radioButton_element_integration_table.clicked.connect(self.update_controls_for_table_of_values)
        #
        self.tabWidget_acoustic_pressure.currentChanged.connect(self.tabEvent_acoustic_pressure)
        self.treeWidget_acoustic_pressure.itemClicked.connect(self.on_click_item)
        self.treeWidget_acoustic_pressure.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)

    def tabEvent_acoustic_pressure(self):
        index = self.tabWidget_acoustic_pressure.currentIndex()
        if index == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)

    def on_click_item(self, item):
        if item.text(0) != "":
            surface_id = int(item.text(0))
            self.lineEdit_selection_id.setText(item.text(0))
            app().main_window.set_geometry_selection(surfaces=[surface_id])

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def load_info(self):
        self.treeWidget_acoustic_pressure.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "acoustic_pressure":
                real_values = np.array(data["real_values"])
                imag_values = np.array(data["imag_values"])
                complex_values = real_values + 1j * imag_values
                new = QTreeWidgetItem([str(surface_id), str(self.text_label(complex_values))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_acoustic_pressure.addTopLevelItem(new)
        self.update_tabs_visibility()

    def geometry_selection_callback(self):

        faces = self.main_window.selected_geometry_surfaces

        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)

    def check_complex_entries(self, lineEdit_real, lineEdit_imag):
        self.stop = False
        title = "Invalid entry to the acoustic pressure"
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                message = "Wrong input for real part of acoustic pressure."
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
                message = "Wrong input for imaginary part of acoustic pressure."
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
        stop, self.typed_ids = self.mesh.check_selected_ids(lineEdit_selection_id, selection="surfaces")
        if stop:
            self.lineEdit_selection_id.setFocus()
            return

        for _id in self.typed_ids:
            self.properties._remove_surface_property("mass_flow_rate", _id)
            self.properties._remove_surface_property("volume_velocity", _id)
            self.properties._remove_surface_property("surface_velocity", _id)
            self.properties._remove_surface_property("compressor_excitation", _id)

        acoustic_pressure = self.check_complex_entries(self.lineEdit_real_value, self.lineEdit_imag_value)

        if stop:
            return

        if acoustic_pressure is not None:

            real_values = [np.real(acoustic_pressure)]
            imag_values = [np.imag(acoustic_pressure)]

            nodal_attribution = self.radioButton_nodal_attribution_constant.isChecked()
            key_avg = self.checkBox_averaged_constant_values.isChecked()

            data = {
                    "real_values": real_values,
                    "imag_values": imag_values,
                    "nodal_attribution": nodal_attribution,
                    "averaged": key_avg,
                    }

            for _id in self.typed_ids:
                self.project.set_acoustic_pressure(data, _id)

            self.main_window.viewer_tabs.update_info_text()
            app().main_window.file.write_model_properties_in_file()

            print(f"[Set acoustic pressure] - defined at surface(s) {self.typed_ids}")
            self.close()

        else:
            title = "Additional inputs required"
            message = "You must inform at least one acoustic pressure\n"
            message += "before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_real_value.setFocus()

    def load_table(self, lineEdit : QLineEdit, direct_load=False):

        title = "Error reached while loading 'acoustic pressure' table"

        try:
            if direct_load:
                imported_table_path = lineEdit.text()

            else:

                last_path = app().config.get_last_folder_for("imported table folder")
                if last_path is None:
                    path = os.path.expanduser("~")
                else:
                    path = last_path

                caption = "Choose a table to import the acoustic pressure"
                imported_table_path, check = QFileDialog.getOpenFileName(  None, 
                                                                            caption, 
                                                                            path, 
                                                                            "Files (*.csv; *.dat; *.txt)"
                                                                        )

                if not check:
                    return None

            lineEdit.setText(imported_table_path)
            app().config.write_last_folder_path_in_file("imported table folder", imported_table_path)

            imported_file = np.loadtxt(imported_table_path, delimiter=",")

            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have three columns in the form: frequencies, real and imaginary values."
                PrintMessageInput([window_title_1, title, message])
                return None

            return imported_file

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            lineEdit.setFocus()
            return None

    def change_project_frequency_setup(self, frequencies : np.ndarray):

        if isinstance(frequencies, np.ndarray):
            f_min = frequencies[0]
            f_max = frequencies[-1]
            f_step = frequencies[1] - frequencies[0]
            actual_frequencies = frequencies
            frequencies = list(frequencies)

        analysis_data = self.main_window.project.analysis_data
        if analysis_data is None:
            self.project.set_frequencies(actual_frequencies, f_min, f_max, f_step, True)
            return

        else:

            imported_table = False
            model_frequencies = list()
            if "frequencies" in analysis_data.keys():
                if isinstance(analysis_data["frequencies"], np.ndarray):
                    model_frequencies = list(analysis_data["frequencies"])
            
                if "imported_table" in analysis_data.keys():
                    imported_table = analysis_data["imported_table"]

        if model_frequencies != frequencies:
            if imported_table:

                if self.are_there_other_active_tables():

                    self.hide()
                    table_path = self.lineEdit_table_path.text()
                    table_name = os.path.basename(table_path)

                    title = "Project frequency setup cannot be modified"
                    message = f"The following imported table of values has a frequency setup "
                    message += "different from the others already imported ones. The current "
                    message += "project frequency setup is not going to be modified."
                    message += f"\n\nTable name: {table_name}"
                    PrintMessageInput([window_title_2, title, message])
                    return True
            
            self.project.set_frequencies(actual_frequencies, f_min, f_max, f_step, True)

    def are_there_other_active_tables(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        stop, self.typed_ids = self.mesh.check_selected_ids(lineEdit_selection_id, selection="surfaces")
        if stop:
            self.lineEdit_selection_id.setFocus()
            return

        for (property, surface_id), data in self.properties.surface_properties.items():
            if isinstance(data, dict):
                if surface_id in self.typed_ids:
                    if property == "acoustic_pressure":
                        continue
                    else:
                        if "table_name" in data.keys():
                            return True

                else:
                    if "table_name" in data.keys():
                        return True

        return False

    def load_acoustic_pressure_table(self):
        self.imported_values = self.load_table(self.lineEdit_table_path)

    def check_table_values(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        stop, self.typed_ids = self.mesh.check_selected_ids(lineEdit_selection_id, selection="surfaces")
        if stop:
            self.lineEdit_selection_id.setFocus()
            return

        for _id in self.typed_ids:
            self.properties._remove_surface_property("mass_flow_rate", _id)
            self.properties._remove_surface_property("volume_velocity", _id)
            self.properties._remove_surface_property("surface_velocity", _id)
            self.properties._remove_surface_property("compressor_excitation", _id)

        if self.lineEdit_table_path.text() != "":

            if self.imported_values is None:
                self.imported_values = self.load_table( self.lineEdit_table_path, 
                                                        direct_load = True )

            if isinstance(self.imported_values, np.ndarray):
                if self.imported_values.shape[1] >= 3:

                    frequencies = self.imported_values[:, 0]
                    if self.change_project_frequency_setup(frequencies):
                        self.lineEdit_table_path.setFocus()
                        self.imported_values = None
                        return
                    
            else:
                return

            if self.imported_values is None:
                return

            real_values = list(self.imported_values[:, 1])
            imag_values = list(self.imported_values[:, 2])
            table_path = self.lineEdit_table_path.text()

            nodal_attribution = self.radioButton_nodal_attribution_table.isChecked()
            key_avg = self.checkBox_averaged_constant_values.isChecked()

            data = {
                    "real_values": real_values,
                    "imag_values": imag_values,
                    "nodal_attribution": nodal_attribution,
                    "averaged": key_avg,
                    "table_name": os.path.basename(table_path),
                    }

            for _id in self.typed_ids:
                self.project.set_acoustic_pressure(data, _id)

            self.main_window.viewer_tabs.update_info_text()
            app().main_window.file.write_model_properties_in_file()

            print(f"[Set acoustic pressure] - defined at surface(s) {self.typed_ids}")
            self.close()

        else:
            title = "Additional inputs required"
            message = "You must inform at least one acoustic pressure\n"
            message += "table path before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_table_path.setFocus()

    def get_list_table_names_from_selected_surfaces(self, list_ids):
        list_table_names = list()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "acoustic_pressure":
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
                if property == "acoustic_pressure" and picked_id == surface_id:

                    self.properties._remove_surface_property("acoustic_pressure", picked_id)
                    self.load_info()
                    self.lineEdit_selection_id.setText("")
                    break

            app().main_window.file.write_model_properties_in_file()
            self.check_model_frequency_controls()

    def check_reset(self):

        surface_ids = list()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "acoustic_pressure":
                surface_ids.append(surface_id)

        if surface_ids:

            title = "Resetting of all applied acoustic pressures"
            message = "Would you like to remove the all acoustic pressures from model?"
            
            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:

                self.properties._reset_property("acoustic_pressure")
                app().main_window.file.write_model_properties_in_file()
                self.check_model_frequency_controls()

                title = "Acoustic pressure resetting process complete"
                message = "All acoustic pressure applied to the acoustic "
                message += "model have been removed from the model."

                PrintMessageInput([window_title_2, title, message])

                self.close()

    def change_frequency_setup(self):
        if self.imported_values is not None:
            self.hide()
            obj = ChangeFrequencyDataRangeInput(self.imported_values)
            if obj.filter_data is not None:
                self.imported_values = obj.filter_data

    def check_model_frequency_controls(self):

        for key, data in self.properties.surface_properties.items():
            property, _ = key
            if property in ["acoustic_pressure", "surface_velocity", "specific_impedance", "mass_flow_rate"]:
                if "table_name" in data.keys():
                    return

        if isinstance(self.project.analysis_data, dict):
            analysis_data = self.project.analysis_data
            analysis_data["imported_table"] = False
            self.project.set_analysis_data(analysis_data)
            app().main_window.file.write_analysis_setup_in_file(analysis_data)

    def reset_input_fields(self):
        self.lineEdit_real_value.setText("")
        self.lineEdit_imag_value.setText("")
        self.lineEdit_table_path.setText("")

    def update_controls_for_constant_value(self):
        _bool = self.radioButton_element_integration_constant.isChecked()
        self.checkBox_averaged_constant_values.setChecked(not _bool)
        self.checkBox_averaged_constant_values.setDisabled(_bool)

    def update_controls_for_table_of_values(self):
        _bool = self.radioButton_element_integration_table.isChecked()
        self.checkBox_averaged_table_values.setChecked(not _bool)
        self.checkBox_averaged_table_values.setDisabled(_bool)

    def update_tabs_visibility(self):
        surface_ids = list()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "acoustic_pressure":
                surface_ids.append(surface_id)

        if len(surface_ids) == 0:
            self.tabWidget_acoustic_pressure.setTabVisible(2, False)
        else:
            self.tabWidget_acoustic_pressure.setTabVisible(2, True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_acoustic_pressure.currentIndex() == 0:
                self.check_constant_values()
            if self.tabWidget_acoustic_pressure.currentIndex() == 1:
                self.check_table_values()
        elif event.key() == Qt.Key_Delete:
            if self.tabWidget_acoustic_pressure.currentIndex() == 2:
                self.remove_bc_from_selection()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            return

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)

# fmt: on