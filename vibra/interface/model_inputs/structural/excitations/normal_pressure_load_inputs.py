from os.path import basename

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.interface import error_title
from vibra.interface.common.common_interface import update_analysis_setup_in_file
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.structural.definitions.enums import StandardTabType
from vibra.interface.ui_generated.model.structural.excitations.normal_pressure_load_inputs_ui import NormalPressureLoadInputs_UI


class NormalPressureLoadInputs(NormalPressureLoadInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._create_connections()

        self._config_widgets()
        self.geometry_selection_callback()
        self.load_model_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.keep_window_open = True
        self.element_types = ["2d_element", "3d_element"]
        self.reset_table_variables()

    def reset_table_variables(self):
        self.pressure_table_values = None
        self.pressure_table_path = None

    def _config_widgets(self):
        #
        self.comboBox_element_type.setEnabled(False)
        #
        for i, w in enumerate([60, 100, 160]):
            self.treeWidget_normal_pressure_loads.setColumnWidth(i, w)
            self.treeWidget_normal_pressure_loads.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_callback)
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_load_table.clicked.connect(self.load_pressure_table)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_normal_pressure_loads.itemClicked.connect(self.on_click_item)
        self.treeWidget_normal_pressure_loads.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        self.update_element_type_based_on_geometry_information()

    def geometry_selection_callback(self):

        faces = app().main_window.selection.geometry_surfaces

        if faces:

            self.comboBox_attribution_type.setCurrentIndex(0)

            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)

            if len(faces) == 1:
                surface_id = list(faces)[0]
                data = self.properties._get_property("normal_pressure_load", surface=surface_id)
                self.update_input_fields(data)

    def update_input_fields(self, data: dict):
        return

        if isinstance(data, dict):

            self.reset_input_fields()
            values = data.get("values", None)

            if "table_paths" in data.keys():
                table_paths = data["table_paths"]
                for index, lineEdit_table in enumerate(self.list_lineEdit_table_values):
                    table_path = table_paths[index]
                    if table_path is not None:                   
                        lineEdit_table.setText(table_path)

            else:
                for index, [lineEdit_real, lineEdit_imag] in enumerate(self.list_lineEdit_constant_values):

                    if data["element_type"] == "3d_element" and index >= 3:
                        continue
                    
                    elif index <= 5 and values[index] is not None:
                        lineEdit_real.setText(str(np.real(values[index])))
                        lineEdit_imag.setText(str(np.imag(values[index])))

    def attribution_type_callback(self):
        app().main_window.action_model_workspace_callback()

    def element_type_callback(self):
        return

    def update_element_type_based_on_geometry_information(self):
        volume_exists = self.mesh.are_there_volumes_in_geometry()
        self.comboBox_element_type.setCurrentIndex(int(volume_exists))

    def check_complex_entries(self, real_input: str, imag_input: str, label: str):

        _real = None
        if real_input != "":
            try:
                _real = float(real_input)

            except Exception:
                self.hide()
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([error_title, title, message])
                return True, None

        _imag = None
        if imag_input != "":
            try:
                _imag = float(imag_input)

            except Exception:
                self.hide()
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for imaginary part of {label}."
                PrintMessageInput([error_title, title, message])
                return True, None

        if _real is None and _imag is None:
            values = None
        elif _real is None:
            values = 1j * _imag
        elif _imag is None:
            values = complex(_real)
        else:
            values = _real + 1j * _imag

        output = values

        return False, output

    def constant_values_attribution(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(input_ids, selection="surfaces")

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        self.remove_conflicting_excitations(surface_ids, "surfaces")

        index = self.comboBox_element_type.currentIndex()
        element_type = self.element_types[index]

        stop, value = self.check_complex_entries(self.lineEdit_real_value.text(), self.lineEdit_imag_value.text(), "Pressure load")

        if stop:
            return True

        pressure_load = [value]

        condition_1 = element_type == "2d_element" and pressure_load.count(None) == 1
        condition_2 = element_type == "3d_element" and pressure_load.count(None) == 1

        if condition_1 or condition_2:
            self.hide()
            title = "Additional inputs required"
            message = "You must enter a non-zero normal pressure load value before confirming the assignment."
            PrintMessageInput([error_title, title, message])
            return

        real_values = [value if value is None else np.real(value) for value in pressure_load]
        imag_values = [value if value is None else np.imag(value) for value in pressure_load]

        for surface_id in surface_ids:

            data = {
                "element_type": element_type,
                "values": pressure_load,
                "real_values": real_values,
                "imag_values": imag_values,
            }

            self.properties._set_property("normal_pressure_load", data, surface=surface_id)

    def load_table(self, lineEdit : QLineEdit, load_label : str, direct_load = False):

        title = "Error while loading table"
        imported_file = None

        try:
            if direct_load:
                if lineEdit.text() == "":
                    return None, None

                imported_table_path = lineEdit.text()
                imported_file = DataImporter.read_data_in_file(imported_table_path)[0].data

            else:

                imported_data = DataImporter.import_single_file("imported_table_folder",
                    ["csv", "dat", "txt", "xlsx", "xls"], f"Choose a table to import the {load_label} data")

                if not imported_data:
                    return None, None

                imported_file = imported_data.data
                lineEdit.setText(imported_data.path)
                imported_table_path = imported_data.path

            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum "
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([error_title, title, message])
                lineEdit.setFocus()
                return None, None

            imported_values = imported_file[:, 1] + 1j * imported_file[:, 2]
            self.frequencies = imported_file[:, 0]

            return imported_values, imported_table_path

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            lineEdit.setFocus()
            return None, None

    def lineEdit_reset(self, lineEdit: QLineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def load_pressure_table(self):
        self.pressure_table_values, self.pressure_table_path = self.load_table(self.lineEdit_table_path, "Pressure load")
        if  self.pressure_table_path is None:
            self.lineEdit_reset(self.lineEdit_table_path)

    def save_table_files(self, selected_id: int, values: np.ndarray):

        if self.frequencies[0] == 0:
            self.frequencies[0] = float(1e-6)

        if self.frequencies[0] == float(1e-6):
            self.frequencies[0] = 0

        if app().project.model.change_analysis_frequency_setup(list(self.frequencies)):

            self.hide()
            lineEdit = self.lineEdit_table_path
            imported_filename = basename(lineEdit.text())
            self.lineEdit_reset(lineEdit)

            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\nFile name: {imported_filename}"
            PrintMessageInput([error_title, title, message])

            return None, None

        table_name = f"normal_pressure_from_surface_{selected_id}"

        real_values = np.real(values)
        imag_values = np.imag(values)
        data = np.array([self.frequencies, real_values, imag_values], dtype=float).T

        update_analysis_setup_in_file(self.frequencies)
        self.properties.add_imported_tables("structural", table_name, data)

        return table_name, data

    def table_values_attribution(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(input_ids, selection="surfaces")

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        self.remove_conflicting_excitations(surface_ids, "surfaces")

        index = self.comboBox_element_type.currentIndex()
        element_type = self.element_types[index]

        if self.pressure_table_path is None:
            self.pressure_table_values, self.pressure_table_path = self.load_table(self.lineEdit_table_path, "Pressure load", direct_load = True)

        for surface_id in surface_ids:
            
            if self.pressure_table_values is not None:
                self.pressure_table_name, self.pressure_array = self.save_table_files(surface_id, self.pressure_table_values)
                if self.pressure_array is None:
                    return True

            table_names = [self.pressure_table_name]
            table_paths = [self.pressure_table_path]
            pressure_load = [self.pressure_table_values]

            condition_1 = element_type == "2d_element" and table_names.count(None) == 1
            condition_2 = element_type == "3d_element" and table_names.count(None) == 1

            if condition_1 or condition_2:
                self.hide()
                title = "Additional inputs required"
                message = "You must enter the normal pressure load table path before confirming the assignment."
                PrintMessageInput([error_title, title, message]) 
                return True

            data = {
                "element_type": element_type,
                "table_names": table_names,
                "table_paths": table_paths,
                "values": pressure_load,
            }

            self.properties._set_property("normal_pressure_load", data, surface=surface_id)

        self.reset_table_variables()

    def apply_callback(self, close_window: bool=False):

        if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
            return

        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == StandardTabType.CONSTANT_DATA:
            if self.constant_values_attribution():
                return

        elif tab_index == StandardTabType.TABULAR_DATA:
            if self.table_values_attribution():
                return

        self.actions_to_finalize(close_window)

    def load_model_info(self):

        self.treeWidget_normal_pressure_loads.clear()
        for (property, *args), data in self.properties.surface_properties.items():

            if property == "normal_pressure_load":
                values = data["values"][0]
                if isinstance(values, complex):
                    str_values = str(values)
                else:
                    str_values = "Table"
                new = QTreeWidgetItem([str(args[0]), "Surface", str_values])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_normal_pressure_loads.addTopLevelItem(new)

        for (property, *args), data in self.properties.line_properties.items():

            if property == "normal_pressure_load":
                values = data["values"]
                new = QTreeWidgetItem([str(args[0]), "Line", ""])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_normal_pressure_loads.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        properties_to_check = [
                               self.properties.surface_properties,
                               self.properties.line_properties,
                               ]

        for current_property in properties_to_check:
            for (property, _) in current_property.keys():
                if property == "normal_pressure_load":
                    self.tabWidget_main.setTabVisible(StandardTabType.LIST, True)
                    return

        self.tabWidget_main.setTabVisible(StandardTabType.LIST, False)
        self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)
        self.lineEdit_real_value.setFocus()
        app().main_window.selection.set_geometry_selection()

    def tab_event_callback(self):
        list_tab = self.tabWidget_main.currentIndex() == StandardTabType.LIST
        self.lineEdit_selection_id.setDisabled(list_tab)
        self.pushButton_apply.setDisabled(list_tab)
        self.pushButton_apply_and_close.setDisabled(list_tab)
        self.pushButton_remove.setDisabled(True)

        if list_tab:
            self.lineEdit_selection_id.setText("")
            return

        else:
            text = self.lineEdit_selection_id.text()
            if "-" in text:
                selected_id = text.split("-")[1]
                self.lineEdit_selection_id.setText(selected_id)

    def on_click_item(self, item):

        selected_id = item.text(0)
        selection = item.text(1)
        self.pushButton_remove.setDisabled(False)

        if selection != "":

            text = f"{selection} - {selected_id}"

            if selection == "Surface":
                app().main_window.selection.set_geometry_selection(surfaces = [int(selected_id)])

            else:
                return

            self.lineEdit_selection_id.setText(text)

    def on_double_click_item(self, item):
        self.on_click_item(item)

    def process_table_file_removal(self, table_names: list):

        if len(table_names) == 0:
            return

        for table_name in table_names:
            self.properties.remove_imported_tables("structural", table_name)

        app().project.update_model_properties_file()

    def remove_conflicting_excitations(self, selected_ids: int | list, selection: str):

        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        if selection == "surfaces":
            remove_function = self.properties._remove_surface_property

        properties = ["nodal_loads", "prescribed_dof"]

        for selected_id in selected_ids:
            for property in properties:
                table_names = self.properties.get_property_related_table_names(property, selected_id, selection)
                remove_function(property, selected_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from(self, selected_id : list, selection: str):
        table_names = self.properties.get_property_related_table_names("normal_pressure_load", selected_id, selection)
        self.process_table_file_removal(table_names)

    def remove_callback(self):

        text = self.lineEdit_selection_id.text()

        if text != "" and " - " in text:

            selection, _selected_id = text.split(" - ")
            selected_id = int(_selected_id)

            if selection == "Surface":
                self.properties._remove_surface_property("normal_pressure_load", selected_id)

            elif selection == "Line":
                self.properties._remove_line_property("normal_pressure_load", selected_id)

            self.remove_table_files_from(selected_id, f"{selection.lower()}s")
            self.actions_to_finalize()

            app().main_window.selection.set_geometry_selection()
            app().main_window.selection.set_mesh_selection()

    def reset_callback(self):

        self.hide()

        title = "Normal pressure load resetting"
        message = "Would you like to remove the all normal pressure loads from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if obj._cancel:
            return

        if obj._continue:

            for (property, *args) in self.properties.surface_properties.keys():
                if property == "normal_pressure_load":
                    self.remove_table_files_from(args[0], "surfaces")

            self.properties._reset_property("normal_pressure_load")
            self.actions_to_finalize()

            app().main_window.selection.set_geometry_selection()
            app().main_window.selection.set_mesh_selection()

    def actions_to_finalize(self, close_window: bool = False):
        self.load_model_info()
        self.reset_input_fields()
        app().main_window.update_info_text()
        app().project.update_model_properties_file()
        app().main_window.update_symbols()

        if close_window:
            self.close()

    def reset_input_fields(self):
        self.lineEdit_selection_id.setText("")
        self.lineEdit_real_value.setText("")
        self.lineEdit_imag_value.setText("")
        self.lineEdit_table_path.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)