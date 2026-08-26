from collections import defaultdict
from enum import IntEnum
from os.path import basename

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.interface import error_title
from vibra.interface.common.common_interface import InputDataType, check_input_entries, update_analysis_setup_in_file
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.structural.definitions.enums import StandardTabType
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.ui_generated.model.structural.excitations.normal_pressure_load_inputs_ui import NormalPressureLoadInputs_UI


class AssignmentType(IntEnum):
    SURFACES = 0
    LINES = 1
    MULTIPLE = 2


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
        self._config_widgets()
        self._configure_validators()
        self._create_connections()

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

    def _configure_validators(self):
        self.lineEdit_left_value.setValidator(StrictDoubleValidator(-1e16, 1e16, 8))
        self.lineEdit_right_value.setValidator(StrictDoubleValidator(-1e16, 1e16, 8))

    def _config_widgets(self):

        self.comboBox_element_type.setEnabled(False)
        self.treeWidget_normal_pressure_loads.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        for i, w in enumerate([100, 120, 160]):
            self.treeWidget_normal_pressure_loads.setColumnWidth(i, w)
            self.treeWidget_normal_pressure_loads.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):

        # QComboBox connections
        self.comboBox_assignment_type.currentIndexChanged.connect(self.assignment_type_callback)
        self.comboBox_data_type.currentIndexChanged.connect(self.data_type_callback)
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_callback)

        # QPushButton connections
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_load_table.clicked.connect(self.load_pressure_table)
        self.pushButton_reset.clicked.connect(self.reset_callback)

        # QTabWidget connection
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)

        # QTreeWidget connections
        self.treeWidget_normal_pressure_loads.itemClicked.connect(self.item_clicked_callback)
        self.treeWidget_normal_pressure_loads.itemDoubleClicked.connect(self.item_double_clicked_callback)
        self.treeWidget_normal_pressure_loads.itemSelectionChanged.connect(self.item_selection_clicked_callback)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

        self.update_element_type_based_on_geometry_information()
        self.geometry_selection_callback()

    def geometry_selection_callback(self):

        faces = app().main_window.selection.geometry_surfaces

        if faces:

            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_assignment_type.setCurrentIndex(AssignmentType.SURFACES)

            if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
                return

            if len(faces) == 1:
                surface_id = next(iter(faces))
                data = self.properties._get_property("normal_pressure_load", surface=surface_id)
                self.update_input_fields(data)

    def update_input_fields(self, data: dict | None):

        if data is None:
            return

        self.reset_input_fields()

        if "table_paths" in data:
            table_paths = data["table_paths"]
            self.lineEdit_table_path.setText(table_paths[0])
            self.tabWidget_main.setCurrentIndex(StandardTabType.TABULAR_DATA)

        else:

            if "real_values" in data:
                left_value = data.get("real_values")[0]
                right_value = data.get("imag_values")[0]
                self.comboBox_data_type.setCurrentIndex(InputDataType.REAL_IMAGINARY)

            else:
                left_value = data.get("amplitude_values")[0]
                right_value = data.get("phase_values")[0]
                self.comboBox_data_type.setCurrentIndex(InputDataType.MAGNITUDE_PHASE)

            self.lineEdit_left_value.setText(str(left_value))
            self.lineEdit_right_value.setText(str(right_value))
            self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)

    def assignment_type_callback(self):
        app().main_window.action_model_workspace_callback()

    def element_type_callback(self):
        return

    def data_type_callback(self):
        real_imaginary = self.comboBox_data_type.currentIndex() == InputDataType.REAL_IMAGINARY
        self.label_dtype_left.setText("Real" if real_imaginary else "Magnitude")
        self.label_dtype_right.setText("Imaginary" if real_imaginary else "Phase")

        label_text = "[N/m²]" if real_imaginary else "[N/m², deg]"
        self.label_unit.setText(label_text)

    def update_element_type_based_on_geometry_information(self):
        volume_exists = self.mesh.are_there_volumes_in_geometry()
        self.comboBox_element_type.setCurrentIndex(int(volume_exists))

    def constant_values_attribution(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(input_ids, selection="surfaces")

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        self.remove_conflicting_excitations(surface_ids, "surfaces")

        element_type = self.element_types[self.comboBox_element_type.currentIndex()]
        real_imag_input = self.comboBox_data_type.currentIndex() == InputDataType.REAL_IMAGINARY

        pressure_load = check_input_entries(self.lineEdit_left_value.text(), self.lineEdit_right_value.text(), "Pressure load")

        if pressure_load is None:
            return True

        condition_1 = element_type == "2d_element" and pressure_load.count(None) == 2
        condition_2 = element_type == "3d_element" and pressure_load.count(None) == 2

        if condition_1 or condition_2:
            title = "Additional inputs required"
            message = "You must enter a non-zero normal pressure load value before confirming the assignment."
            PrintMessageInput([error_title, title, message])
            return

        left_values = [pressure_load[0]]
        right_values = [pressure_load[1]]

        for surface_id in surface_ids:

            data = {
                "element_type": element_type,
                "real_values" if real_imag_input else "amplitude_values": left_values,
                "imag_values" if real_imag_input else "phase_values": right_values,
            }

            self.properties._set_property("normal_pressure_load", data, surface=surface_id)

    def load_table(self, lineEdit : QLineEdit, load_label : str, direct_load = False):

        title = "Error while loading table"

        try:
            if direct_load:
                if lineEdit.text() == "":
                    return None, None

                imported_table_path = lineEdit.text()
                imported_values = DataImporter.read_data_in_file(imported_table_path)[0].data

            else:

                imported_data = DataImporter.import_single_file("imported_table_folder",
                    ["csv", "dat", "txt", "xlsx", "xls"], f"Choose a table to import the {load_label} data")

                if not imported_data:
                    return None, None

                imported_values = imported_data.data
                lineEdit.setText(imported_data.path)
                imported_table_path = imported_data.path

            if imported_values.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum "
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([error_title, title, message])
                lineEdit.setFocus()
                return None, None

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

    def save_table_files(self, selected_id: int, imported_values: np.ndarray):

        frequencies = imported_values[:, 0]

        if frequencies[0] == 0:
            frequencies[0] = 1e-6

        if frequencies[0] == 1e-6:
            frequencies[0] = 0

        if app().project.model.change_analysis_frequency_setup(list(frequencies)):

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

        if self.comboBox_data_type.currentIndex() == InputDataType.REAL_IMAGINARY:
            complex_values = imported_values[:, 1] + 1j * imported_values[:, 2]
        else:
            complex_values = imported_values[:, 1] * np.exp(1j * imported_values[:, 2] * np.pi / 180)

        # real values vector
        real_values = np.real(complex_values)

        # imaginary values vector
        imag_values = np.imag(complex_values)

        data = np.array([frequencies, real_values, imag_values], dtype=float).T

        update_analysis_setup_in_file(frequencies)

        self.properties.add_imported_tables("structural", table_name, data)

        return table_name, data

    def table_values_attribution(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(input_ids, selection="surfaces")

        if error_data is not None:
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
                title = "Additional inputs required"
                message = "You must enter the normal pressure load table path before confirming the assignment."
                PrintMessageInput([error_title, title, message]) 
                return True

            data = {
                "element_type": element_type,
                "table_names": table_names,
                "table_paths": table_paths,
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

        if tab_index == StandardTabType.TABULAR_DATA:
            if self.table_values_attribution():
                return

        self.actions_to_finalize(close_window)

    def load_model_info(self):

        self.treeWidget_normal_pressure_loads.clear()
        for (property, *args), data in self.properties.surface_properties.items():

            if property != "normal_pressure_load":
                continue

            if not isinstance(data, dict):
                continue

            if "table_names" in data:
                str_value = "Table"
            else:
                values = data["values"][0]
                str_value = f"{values : .6e}"

            new = QTreeWidgetItem([str(args[0]), "surface", str_value])
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
            for (property, _) in current_property:
                if property != "normal_pressure_load":
                    continue

                self.tabWidget_main.setTabVisible(StandardTabType.LIST, True)
                return

        self.tabWidget_main.setTabVisible(StandardTabType.LIST, False)
        self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)
        self.lineEdit_left_value.setFocus()

    def tab_event_callback(self):
        list_tab = self.tabWidget_main.currentIndex() == StandardTabType.LIST
        self.comboBox_assignment_type.setDisabled(list_tab)
        self.comboBox_data_type.setDisabled(list_tab)
        self.lineEdit_selection_id.setDisabled(list_tab)
        self.pushButton_apply.setDisabled(list_tab)
        self.pushButton_apply_and_close.setDisabled(list_tab)
        self.pushButton_remove.setDisabled(True)

        if list_tab:
            app().main_window.selection.set_geometry_selection()
        
        self.lineEdit_selection_id.setText("")
        self.treeWidget_normal_pressure_loads.clearSelection()

    def item_selection_clicked_callback(self):
        self.item_clicked_callback(None)

    def item_clicked_callback(self, item):

        self.pushButton_remove.setDisabled(False)

        selected_items = self.treeWidget_normal_pressure_loads.selectedItems()
        if not selected_items:
            self.lineEdit_selection_id.clear()
            self.pushButton_remove.setDisabled(True)
            return

        entities_mapping = defaultdict(list)
        for _item in selected_items:
            entity = _item.text(1)
            entities_mapping[entity].append(int(_item.text(0)))

        if not entities_mapping:
            return

        app().main_window.selection.set_geometry_selection(
            surfaces = entities_mapping.get("surface"),
            )

    def item_double_clicked_callback(self, item):
        self.item_clicked_callback(item)

    def remove_conflicting_excitations(self, selected_ids: int | list, selection: str):

        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        if selection == "surfaces":
            remove_function = self.properties._remove_surface_property

        properties = ["nodal_loads", "prescribed_dof"]

        for selected_id in selected_ids:
            for property in properties:
                remove_function(property, selected_id)

    def remove_callback(self):

        selected_items = self.treeWidget_normal_pressure_loads.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            selected_id = int(item.text(0))
            selection = item.text(1)

            if selection == "surface":
                self.properties._remove_surface_property("normal_pressure_load", selected_id)

        self.actions_to_finalize()

        app().main_window.selection.set_geometry_selection()
        app().main_window.selection.set_mesh_selection()

    def reset_callback(self):

        title = "Normal pressure load reset"
        message = "Would you like to remove the all normal pressure loads from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if obj._cancel:
            return

        if obj._continue:
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
        self.lineEdit_left_value.setText("")
        self.lineEdit_right_value.setText("")
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
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)