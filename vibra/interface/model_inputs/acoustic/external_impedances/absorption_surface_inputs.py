import numpy as np
from PySide6.QtCore import QItemSelectionModel, QPoint, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.interface import error_title
from vibra.interface.common.common_interface import update_analysis_setup_in_file
from vibra.interface.data.data_manager import get_spectral_data_from_array
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.acoustic.definitions.enums import StandardTabType
from vibra.interface.ui_generated.model.acoustic.external_impedances.absorption_surface_inputs_ui import AbsorptionSurfaceInputs_UI


class AbsorptionSurfaceInputs(AbsorptionSurfaceInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties
        
        self._config_window()
        self._initialize()
        self._configure_qt_variables()
        self._create_connections()

        self.load_model_info()
        self.geometry_selection_callback()

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

    def _configure_qt_variables(self):
        for i, w in enumerate([120]):
            self.treeWidget_absorption_surface.setColumnWidth(i, w)
            self.treeWidget_absorption_surface.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_load_table.clicked.connect(self.load_specific_impedance_table)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_absorption_surface.itemClicked.connect(self.on_click_item)
        self.treeWidget_absorption_surface.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

    def tab_event_callback(self):
        current_tab = self.tabWidget_main.currentIndex()
        tab_list = current_tab == StandardTabType.LIST

        if self.last_tab == StandardTabType.LIST or tab_list:
            app().main_window.selection.clear_selection()
            self.clear_line_edit_selection_id()

        if tab_list:
            self.pushButton_remove.setDisabled(True)
            self.treeWidget_absorption_surface.clearSelection()

        self.lineEdit_selection_id.setDisabled(tab_list)
        self.pushButton_apply.setDisabled(tab_list)
        self.pushButton_apply_and_close.setDisabled(tab_list)

        self.last_tab = current_tab

    def on_click_item(self, item):
        self.tree_item_clicked = True

        surface_ids = self.get_selected_surfaces_from_tree_widget_absorption_surface()

        if not surface_ids:
            return
            
        app().main_window.selection.set_geometry_selection(surfaces=surface_ids)

        self.pushButton_remove.setEnabled(True)
        self.set_selection_text(surface_ids)

        self.tree_item_clicked = False

    def on_doubleclick_item(self, item):
        self.on_click_item(item)
    
    def get_selected_surfaces_from_tree_widget_absorption_surface(self) -> list:
        selected_items = self.treeWidget_absorption_surface.selectedItems()

        if not selected_items:
            return list()
        
        return [int(item.text(0)) for item in selected_items]
    
    def set_selection_text(self, selected_surfaces: list | set):
        selected_surfaces = list(selected_surfaces)
        selected_surfaces.sort()

        selected_surfaces = map(str, selected_surfaces)
        selection_text = ", ".join(selected_surfaces)

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)
    
    def clear_line_edit_selection_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")

    def geometry_selection_callback(self):
        if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
            self.verify_if_selected_surfaces_are_in_tree_widget_absorption_surface()
            return

        surfaces = app().main_window.selection.geometry_surfaces

        if surfaces:
            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)

        if len(surfaces) == 1:
            surface_id = list(surfaces)[0]
            self.load_property_data(surface_id)

    def load_property_data(self, surface_id: int):
        data = self.properties._get_property("absorption_surface", surface=surface_id)
        if not isinstance(data, dict):
            return

        if "table_paths" in data.keys():
            self.tabWidget_main.setCurrentIndex(StandardTabType.TABULAR_DATA)
            self.lineEdit_table_path.setText(data.get("table_paths")[0])
        else:
            self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)
            self.lineEdit_real_value.setText(f"{data.get('real_values')[0]}")
    
    def verify_if_selected_surfaces_are_in_tree_widget_absorption_surface(self):
        if self.tree_item_clicked:
            return

        selected_surfaces = app().main_window.selection.geometry_surfaces

        if not selected_surfaces:
            return

        self.clear_line_edit_selection_id()
        self.treeWidget_absorption_surface.clearSelection()
        self.pushButton_remove.setDisabled(True)

        map_id_to_model_index = self.get_tree_widget_absorption_surface_items_map()
        selected_ids = set(map_id_to_model_index.keys())
        selected_surfaces_in_tree_widget = selected_surfaces.intersection(selected_ids)

        if not selected_surfaces_in_tree_widget:
            return
        
        self.pushButton_remove.setEnabled(True)
        
        model_selector = self.treeWidget_absorption_surface.selectionModel()

        for surface_id in selected_surfaces_in_tree_widget:
            model_index = map_id_to_model_index[surface_id]

            model_selector.select(model_index, QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)

        self.treeWidget_absorption_surface.setSelectionMode(QAbstractItemView.SingleSelection)
        self.set_selection_text(selected_surfaces_in_tree_widget)

    def get_tree_widget_absorption_surface_items_map(self) -> dict:
        map_id_to_model_index = dict()

        index = self.treeWidget_absorption_surface.indexAt(QPoint(0, 0))
        while index.isValid():
            item = self.treeWidget_absorption_surface.itemFromIndex(index)
            surface_id = item.text(0)

            map_id_to_model_index[int(surface_id)] = index

            index = self.treeWidget_absorption_surface.indexBelow(index)
        
        return map_id_to_model_index

    def load_model_info(self):

        self.treeWidget_absorption_surface.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "absorption_surface":

                if "table_names" in data.keys():
                    str_value = "Table of values"
                else:
                    absorption_coefficient = np.array(data["real_values"])
                    str_value = str(absorption_coefficient)

                new = QTreeWidgetItem([str(surface_id), str_value])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_absorption_surface.addTopLevelItem(new)

        self.update_tabs_visibility()

    def apply_callback(self, close_window: bool = False):
        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == StandardTabType.LIST:
            return

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(input_ids, selection="surfaces", single_id=False)

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        self.remove_conflicting_excitations(surface_ids)

        if tab_index == StandardTabType.CONSTANT_DATA:
            if self.constant_data_assignment(surface_ids):
                return

        elif tab_index == StandardTabType.TABULAR_DATA:
            if self.tabular_data_assignment(surface_ids):
                return
            
        self.actions_to_finalize(close_window)

    def check_inputs(self, lineEdit: QLineEdit, label: str, zero_included: bool = True, only_positive: bool = True):

        self.stop = False
        message = ""

        title = "Invalid value typed"
        input_str = lineEdit.text()

        if input_str != "":

            input_str = input_str.replace(",", ".")

            try:

                value = float(input_str)

                if zero_included:
                    if value < 0:
                        message = f"Insert a positive or a zero value to the {label}."

                else:
                    if only_positive and value <= 0:
                        message = f"Insert a non-zero positive value to the {label}."

            except Exception as _err:
                message = f"You have typed an invalid value at the {label} input field.\n\n"
                message += str(_err)

        else:
            message = f"Insert some value at the {label} input field."

        if message != "":
            self.hide()
            PrintMessageInput([error_title, title, message])
            return None
        else:
            return value

    def constant_data_assignment(self, surface_ids: list[int]):

        absorption_coefficient = self.check_inputs(self.lineEdit_real_value, "Absorption coefficient", zero_included=False,)

        if absorption_coefficient is None:
            self.hide()
            title = "Additional inputs required"
            message = "You must enter an absorption surface value to proceed with the assignment."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_real_value.setFocus()
            return True

        real_values = [absorption_coefficient]
        imag_values = [None]

        data = {
            "real_values" : real_values,
            "imag_values" : imag_values,
            }

        for surface_id in surface_ids:
            self.properties._set_property("absorption_surface", data, surface=surface_id)      

    def load_table(self, lineEdit : QLineEdit, direct_load=False):

        title = "Error reached while loading 'absorption surface' table"
        imported_values = None

        try:
            if direct_load:
                imported_table_path = lineEdit.text()
                imported_values = DataImporter.read_data_in_file(imported_table_path)[0].data

            else:
                imported_data = DataImporter.import_single_file("imported_table_folder",
                    ["csv", "dat", "txt", "xlsx", "xls"], "Choose a table to import the absorption surface")
                
                if not imported_data:
                    return None

                imported_values = imported_data.data
                lineEdit.setText(imported_data.path)

            if imported_values.shape[1] < 2:
                message = "The imported table has insufficient number of columns. The absorption coefficient"
                message += " data must have two columns in the form: frequencies and real values."
                PrintMessageInput([error_title, title, message])
                return None

            # filter the zero-frequency component
            mask = imported_values[:, 0] > 0
            _imported_values = imported_values[mask, :]

            return _imported_values

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            lineEdit.setFocus()
            return None, None

    def save_table_values(self, table_name: str, imported_values: np.ndarray):

        # define the frequencies vector
        _frequencies = imported_values[:, 0]

        if app().project.model.change_analysis_frequency_setup(list(_frequencies)):
            self.hide()
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        update_analysis_setup_in_file(_frequencies)

        # real values vector
        real_values = imported_values[:, 1]

        # imaginary values vector
        # imag_values = imported_values[:, 2]

        # TODO: check the spectral content of the absorption surface
        data = np.array([_frequencies, real_values], dtype=float).T
        # data = np.array([_frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def load_specific_impedance_table(self):
        self.imported_values = self.load_table(self.lineEdit_table_path)

    def tabular_data_assignment(self, surface_ids: list[int]):

        if self.lineEdit_table_path.text() == "":
            self.hide()
            title = "Additional inputs required"
            message = "You must enter the absorption surface table path to proceed with the assignment."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_table_path.setFocus()
            return True

        if self.imported_values is None:
            self.imported_values = self.load_table(self.lineEdit_table_path, direct_load=True)

        for surface_id in surface_ids:

            if isinstance(self.imported_values, np.ndarray):
                if self.imported_values.shape[1] >= 3:

                    table_name = f"specific_impedance_at_surface_{surface_id}"
                    if self.save_table_values(table_name, self.imported_values):
                        self.lineEdit_table_path.setFocus()
                        self.imported_values = None
                        return True

            else:
                return True

            if self.imported_values is None:
                return True

            # complex values computed from tabular data
            complex_values = get_spectral_data_from_array(self.imported_values)

            # table path from imported tabular data
            table_path = self.lineEdit_table_path.text()

            data = {
                "table_names": [table_name],
                "table_paths" : [table_path],
                "values" : [complex_values],
            }

            self.properties._set_property("absorption_surface", data, surface=surface_id)

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().project.update_model_properties_file()

    def remove_conflicting_excitations(self, surface_ids: int | list):

        if isinstance(surface_ids, int):
            surface_ids = [surface_ids]

        labels = [
            "absorption_surface",
            "specific_impedance",
            "incident_plane_wave",
            ]

        for surface_id in surface_ids:
            for label in labels:
                table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_id : list):
        table_names = self.properties.get_property_related_table_names("absorption_surface", surface_id, "surfaces")
        self.process_table_file_removal(table_names)

    def remove_callback(self):
        selected_surfaces = self.get_selected_surfaces_from_tree_widget_absorption_surface()
    
        if not selected_surfaces:
            return
        
        for surface_id in selected_surfaces:
            self.remove_table_files_from_surfaces(surface_id)
            self.properties._remove_surface_property("absorption_surface", surface_id)

        self.clear_line_edit_selection_id()
        self.pushButton_remove.setDisabled(True)

        app().main_window.selection.clear_selection()
        self.actions_to_finalize()

    def reset_callback(self):

        surface_ids = list()
        for (property, *args) in self.properties.surface_properties.keys():
            if property == "absorption_surface":
                surface_ids.append(args[0])

        if not surface_ids:
            return

        self.hide()

        title = "Absorption surface reset"
        message = "Would you like to remove the all applied absorption surfaces from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        self.remove_table_files_from_surfaces(surface_ids)
        for surface_id in surface_ids:
            self.properties._remove_surface_property("absorption_surface", surface_id)

        self.actions_to_finalize()

    def actions_to_finalize(self, close_window: bool = False):
        self.load_model_info()
        app().main_window.update_info_text()
        app().project.update_model_properties_file()
        app().main_window.update_symbols()

        if close_window:
            self.close()

    def reset_input_fields(self):
        self.lineEdit_real_value.setText("")
        self.lineEdit_table_path.setText("")

    def update_tabs_visibility(self):

        for key in self.properties.surface_properties.keys():
            property, *args = key
            if property != "absorption_surface":
                continue

            self.tabWidget_main.setTabVisible(StandardTabType.LIST, True)
            return

        self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)
        self.tabWidget_main.setTabVisible(StandardTabType.LIST, False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Control:
            self.treeWidget_absorption_surface.setSelectionMode(QAbstractItemView.MultiSelection)
        elif event.key() == Qt.Key_Shift:
            self.treeWidget_absorption_surface.setSelectionMode(QAbstractItemView.ContiguousSelection)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.treeWidget_absorption_surface.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)