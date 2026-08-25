from collections import defaultdict
from enum import IntEnum

import numpy as np
from PySide6.QtCore import QItemSelectionModel, QPoint, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.interface import error_title
from vibra.interface.common.common_interface import update_analysis_setup_in_file
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.acoustic.definitions.enums import StandardTabType
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.ui_generated.model.acoustic.excitations.surface_velocity_inputs_ui import SurfaceVelocityInputs_UI


class DataType(IntEnum):
    REAL_IMAGINARY = 0
    AMPLITUDE_PHASE = 1


class SurfaceVelocityInputs(SurfaceVelocityInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._config_widgets()
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
        self.imported_values = None
        self.keep_window_open = True
        self.last_tab = self.tabWidget_main.currentIndex()
        self.tree_item_clicked = False

    def _configure_validators(self):
        self.lineEdit_left_value.setValidator(StrictDoubleValidator(-1e16, 1e16, 8))
        self.lineEdit_right_value.setValidator(StrictDoubleValidator(-1e16, 1e16, 8))

    def _create_connections(self):

        # QComboBox connection
        self.comboBox_data_type.currentIndexChanged.connect(self.data_type_callback)

        # QPushButton connections
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_load_table.clicked.connect(self.load_surface_velocity_table)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)

        # QTabWidget connection
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)

        # QTreeWidget connection
        self.treeWidget_surface_velocity.itemClicked.connect(self.item_clicked_callback)
        self.treeWidget_surface_velocity.itemDoubleClicked.connect(self.item_double_clicked_callback)
        self.treeWidget_surface_velocity.itemSelectionChanged.connect(self.item_selection_clicked_callback)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

        self.geometry_selection_callback()

    def _config_widgets(self):

        self.treeWidget_surface_velocity.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        for i, w in enumerate([120]):
            self.treeWidget_surface_velocity.setColumnWidth(i, w)
            self.treeWidget_surface_velocity.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def geometry_selection_callback(self):
        # if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
        #     self.verify_if_selected_surfaces_are_in_tree_widget_surface_velocity()
        #     return
        
        faces = app().main_window.selection.geometry_surfaces

        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)

            if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
                return

            if len(faces) == 1:
                surface_id = next(iter(faces))
                self.load_property_data(surface_id)

    def load_property_data(self, surface_id: int):

        data = self.properties._get_property("surface_velocity", surface=surface_id)
        if not isinstance(data, dict):
            return

        if "table_paths" in data:
            self.lineEdit_table_path.setText(data["table_paths"][0])
            self.tabWidget_main.setCurrentIndex(StandardTabType.TABULAR_DATA)

        else:

            if "real_values" in data:
                left_value = data.get("real_values")[0]
                right_value = data.get("imag_values")[0]
                self.comboBox_data_type.setCurrentIndex(DataType.REAL_IMAGINARY)

            else:
                left_value = data.get("amplitude_values")[0]
                right_value = data.get("phase_values")[0]
                self.comboBox_data_type.setCurrentIndex(DataType.AMPLITUDE_PHASE)

            self.lineEdit_left_value.setText(str(left_value if left_value is not None else 0.0))
            self.lineEdit_right_value.setText(str(right_value if right_value is not None else 0.0))
            self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)

    def data_type_callback(self):
        real_imaginary = self.comboBox_data_type.currentIndex() == DataType.REAL_IMAGINARY
        self.label_dtype_left.setText("Real" if real_imaginary else "Amplitude")
        self.label_dtype_right.setText("Imaginary" if real_imaginary else "Phase")

        label_text = "[m/s]" if real_imaginary else "[m/s, deg]"
        self.label_unit.setText(label_text)

    def tab_event_callback(self):
        current_tab = self.tabWidget_main.currentIndex()
        tab_list = current_tab == StandardTabType.LIST

        if self.last_tab == StandardTabType.LIST or tab_list:
            app().main_window.selection.clear_selection()
            self.clear_line_edit_selection_id()

        if tab_list:
            self.pushButton_remove.setDisabled(True)
            self.treeWidget_surface_velocity.clearSelection()
        
        self.lineEdit_selection_id.setDisabled(tab_list)
        self.pushButton_apply.setDisabled(tab_list)
        self.pushButton_apply_and_close.setDisabled(tab_list)

        self.last_tab = current_tab

    def apply_callback(self, close_window: bool = False):
        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == StandardTabType.LIST:
            return

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(input_ids, selection="surfaces", single_id=False)

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        self.remove_conflicting_excitations(surface_ids)

        if tab_index == StandardTabType.CONSTANT_DATA:
            if self.constant_data_assignment(surface_ids):
                return

        if tab_index == StandardTabType.TABULAR_DATA:
            if self.tabular_data_assignment(surface_ids):
                return

        self.actions_to_finalize(close_window)

    def check_input_entries(self, input_left: str, input_right: str, label: str):

        value_left = None
        if input_left != "":
            try:
                input_left = input_left.replace(",", ".")
                value_left = float(input_left)

            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([error_title, title, message])
                return

        value_right = None
        if input_right != "":
            try:
                input_right = input_right.replace(",", ".")
                value_right = float(input_right)

            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for imaginary part of {label}."
                PrintMessageInput([error_title, title, message])
                return

        output = [value_left, value_right] 

        return output

    def constant_data_assignment(self, surface_ids: list[int]):

        surface_velocity = self.check_input_entries(
            self.lineEdit_left_value.text(), 
            self.lineEdit_right_value.text(), 
            "surface velocity",
            )

        if surface_velocity is None:
            return True

        if surface_velocity is None:
            title = "Additional inputs required"
            message = "You must enter a non-zero surface velocity value to proceed with the assignment."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_left_value.setFocus()
            return True

        left_values = [surface_velocity[0]]
        right_values = [surface_velocity[1]]
        real_imag_input = self.comboBox_data_type.currentIndex() == DataType.REAL_IMAGINARY

        data = {
            "real_values" if real_imag_input else "amplitude_values": left_values,
            "imag_values" if real_imag_input else "phase_values": right_values,
            "data_type": "real_imaginary" if real_imag_input else "amplitude_phase",
            "element_integration": True,
        }

        for surface_id in surface_ids:
            self.properties._set_property("surface_velocity", data, surface=surface_id)

    def load_table(self, lineEdit : QLineEdit, direct_load=False):

        title = "Error reached while loading 'surface velocity' table"

        try:
            if direct_load:
                imported_table_path = lineEdit.text()
                imported_values = DataImporter.read_data_in_file(imported_table_path)[0].data

            else:
                imported_data = DataImporter.import_single_file("imported_table_folder",
                    ["csv", "dat", "txt", "xlsx", "xls"], "Choose a table to import the surface velocity")
                                
                if not imported_data:
                    return

                imported_values = imported_data.data
                lineEdit.setText(imported_data.path)

            if imported_values.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have three columns in the form: frequencies, real and imaginary values."
                PrintMessageInput([error_title, title, message])
                return None
            
            # filter the zero-frequency component
            mask = imported_values[:, 0] > 0
            _imported_values = imported_values[mask, :]

            if self.comboBox_data_type.currentIndex() == DataType.REAL_IMAGINARY:
                complex_values = _imported_values[:, 1] + 1j * _imported_values[:, 2]
            else:
                complex_values = _imported_values[:, 1] * np.exp(1j * _imported_values[:, 2] * np.pi / 180)

            return complex_values

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            lineEdit.setFocus()
            return

    def save_table_values(self, table_name: str, imported_values: np.ndarray):

        # define the frequencies vector
        frequencies = imported_values[:, 0]

        if app().project.model.change_analysis_frequency_setup(list(frequencies)):
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        update_analysis_setup_in_file(frequencies)

        if self.comboBox_data_type.currentIndex() == DataType.REAL_IMAGINARY:
            complex_values = imported_values[:, 1] + 1j * imported_values[:, 2]
        else:
            complex_values = imported_values[:, 1] * np.exp(1j * imported_values[:, 2] * np.pi / 180)

        # real values vector
        real_values = np.real(complex_values)

        # imaginary values vector
        imag_values = np.imag(complex_values)

        data = np.array([frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def load_surface_velocity_table(self):
        self.imported_values = self.load_table(self.lineEdit_table_path)

    def tabular_data_assignment(self, surface_ids: list[int]):

        self.remove_conflicting_excitations(surface_ids)

        if self.lineEdit_table_path.text() == "":
            title = "Additional inputs required"
            message = "You must enter the surface velocity table path to proceed with the assignment."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_table_path.setFocus()
            return True

        if self.imported_values is None:
            self.imported_values = self.load_table(self.lineEdit_table_path, direct_load = True)

        for surface_id in surface_ids:

            if isinstance(self.imported_values, np.ndarray):
                if self.imported_values.shape[1] >= 3:

                    table_name = f"surface_velocity_at_surface_{surface_id}"
                    if self.save_table_values(table_name, self.imported_values):
                        self.lineEdit_table_path.setFocus()
                        self.imported_values = None
                        return

            else:
                return True

            if self.imported_values is None:
                return True

            # table path from imported tabular data
            table_path = self.lineEdit_table_path.text()

            data = {
                "table_names" : [table_name],
                "table_paths" : [table_path],
                "element_integration" : True,
                }

            self.properties._set_property("surface_velocity", data, surface=surface_id)

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().project.update_model_properties_file()

    def remove_conflicting_excitations(self, surface_ids: int | list):

        if isinstance(surface_ids, int):
            surface_ids = [surface_ids]

        labels = [
            "acoustic_pressure",
            "surface_velocity",
            "incident_plane_wave",
            "compressor_excitation_spectrum",
            "compressor_excitation_waveform",
            "reciprocating_compressor_excitation",
            "mass_source",
            ]

        for surface_id in surface_ids:
            for label in labels:
                table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_id : int | list):
        table_names = self.properties.get_property_related_table_names("surface_velocity", surface_id, "surfaces")
        self.process_table_file_removal(table_names)

    def remove_callback(self):

        selected_items = self.treeWidget_surface_velocity.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            selected_id = int(item.text(0))
            selection = item.text(1)

            if selection == "surface":
                self.properties._remove_surface_property("surface_velocity", selected_id)

        self.clear_line_edit_selection_id()
        self.pushButton_remove.setDisabled(True)

        app().main_window.selection.clear_selection()
        self.actions_to_finalize()

    def reset_callback(self):

        title = "Surface velocity reset"
        message = "Would you like to remove the all applied surface velocities from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            surface_ids = []
            for (property, *args) in self.properties.surface_properties:
                if property != "surface_velocity":
                    continue

                surface_id = args[0]
                surface_ids.append(surface_id)

            self.remove_table_files_from_surfaces(surface_ids)

            self.properties._reset_property("surface_velocity")
            self.actions_to_finalize()

    def actions_to_finalize(self, close_window: bool = False):
        self.load_model_info()
        app().project.update_model_properties_file()
        app().main_window.update_info_text()
        app().main_window.update_symbols()

        if close_window:
            self.close()

    def reset_input_fields(self):
        self.lineEdit_left_value.setText("")
        self.lineEdit_right_value.setText("")
        self.lineEdit_table_path.setText("")

    def update_tabs_visibility(self):

        for key in self.properties.surface_properties:
            property, *args = key
            if property != "surface_velocity":
                continue

            self.tabWidget_main.setTabVisible(StandardTabType.LIST, True)
            return

        self.tabWidget_main.setTabVisible(StandardTabType.LIST, False)
        self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)    
        self.lineEdit_left_value.setFocus()

    def item_clicked_callback(self, item):

        self.pushButton_remove.setEnabled(True)

        selected_items = self.treeWidget_surface_velocity.selectedItems()
        if not selected_items:
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

    def item_selection_clicked_callback(self):
        self.item_clicked_callback(None)
    
    def clear_line_edit_selection_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")

    def load_model_info(self):
        self.treeWidget_surface_velocity.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property != "surface_velocity":
                continue

            if not isinstance(data, dict):
                continue

            if "table_names" in data:
                str_value = "Table of values"
            else:
                values = data["values"][0]
                str_value = str(values)

            new = QTreeWidgetItem([str(surface_id), "surface", str_value])
            for i in range(3):
                new.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_surface_velocity.addTopLevelItem(new)

        self.update_tabs_visibility()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    # def keyReleaseEvent(self, event):
    #     if event.key() == Qt.Key_Control:
    #         self.treeWidget_surface_velocity.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)


    ## TODO: remove if deprecated

    def set_selection_text(self, selected_surfaces: list | set):
        selected_surfaces = list(selected_surfaces)
        selected_surfaces.sort()

        selected_surfaces = map(str, selected_surfaces)
        selection_text = ", ".join(selected_surfaces)

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)


    def verify_if_selected_surfaces_are_in_tree_widget_surface_velocity(self):
        if self.tree_item_clicked:
            return

        selected_surfaces = app().main_window.selection.geometry_surfaces

        if not selected_surfaces:
            return

        self.clear_line_edit_selection_id()
        self.treeWidget_surface_velocity.clearSelection()
        self.pushButton_remove.setDisabled(True)

        map_id_to_model_index = self.get_tree_widget_surface_velocity_items_map()
        selected_ids = set(map_id_to_model_index.keys())
        selected_surfaces_in_tree_widget = selected_surfaces.intersection(selected_ids)

        if not selected_surfaces_in_tree_widget:
            return
        
        self.pushButton_remove.setEnabled(True)
        
        model_selector = self.treeWidget_surface_velocity.selectionModel()

        for surface_id in selected_surfaces_in_tree_widget:
            model_index = map_id_to_model_index[surface_id]

            model_selector.select(model_index, QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)

        self.treeWidget_surface_velocity.setSelectionMode(QAbstractItemView.SingleSelection)
        self.set_selection_text(selected_surfaces_in_tree_widget)


    def get_tree_widget_surface_velocity_items_map(self) -> dict:
        map_id_to_model_index = dict()

        index = self.treeWidget_surface_velocity.indexAt(QPoint(0, 0))
        while index.isValid():
            item = self.treeWidget_surface_velocity.itemFromIndex(index)
            surface_id = item.text(0)

            map_id_to_model_index[int(surface_id)] = index

            index = self.treeWidget_surface_velocity.indexBelow(index)
        
        return map_id_to_model_index