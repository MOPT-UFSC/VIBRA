from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem, QAbstractItemView
from PySide6.QtCore import Qt, QPoint, QItemSelectionModel
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.data_filter.change_frequency_data_handler import ChangeFrequencyDataRangeInput
from vibra.interface.ui_generated.model.setup.acoustic.specific_impedance_inputs_ui import SpecificImpedanceInputs_UI

import numpy as np

error_title = "Error"


class SpecificImpedanceInputs(SpecificImpedanceInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.project = app().project
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
        #
        self.pushButton_change_frequency_setup.setDisabled(True)
        #
        for i, w in enumerate([80, 80]):
            self.treeWidget_specific_impedance.setColumnWidth(i, w)
            self.treeWidget_specific_impedance.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_load_table.clicked.connect(self.load_specific_impedance_table)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_specific_impedance.itemClicked.connect(self.on_click_item)
        self.treeWidget_specific_impedance.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)

    def tab_event_callback(self):
        current_tab = self.tabWidget_main.currentIndex()
        tab_list = current_tab == 2

        if self.last_tab == 2 or tab_list:
            app().main_window.clear_selection()
            self.clear_line_edit_selection_id()

        if tab_list:
            self.treeWidget_specific_impedance.clearSelection()
            self.pushButton_remove.setDisabled(True)
        
        self.lineEdit_selection_id.setDisabled(tab_list)
        self.pushButton_attribute.setDisabled(tab_list)

        self.last_tab = current_tab

    def on_click_item(self, item):
        self.tree_item_clicked = True

        surface_ids = self.get_selected_surfaces_from_tree_widget_specific_impedance()

        if not surface_ids:
            return
        
        app().main_window.set_geometry_selection(surfaces=surface_ids)
        
        self.pushButton_remove.setEnabled(True)
        self.set_selection_text(surface_ids)

        self.tree_item_clicked = False

    def on_doubleclick_item(self, item):
        self.on_click_item(item)
    
    def get_selected_surfaces_from_tree_widget_specific_impedance(self) -> list:
        selected_items = self.treeWidget_specific_impedance.selectedItems()

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
        if self.tabWidget_main.currentIndex() == 2:
            self.verify_if_selected_surfaces_are_in_tree_widget_specific_impedance()
            return
        
        surfaces = app().main_window.selected_geometry_surfaces

        if surfaces:
            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)

        if len(surfaces) == 1:
            surface_id = list(surfaces)[0]
            self.load_property_data(surface_id)

    def load_property_data(self, surface_id: int):
        data = self.properties._get_property("specific_impedance", surface=surface_id)
        if not isinstance(data, dict):
            return

        if "table_paths" in data.keys():
            self.tabWidget_main.setCurrentIndex(1)
            self.lineEdit_table_path.setText(data.get("table_paths")[0])
        else:
            self.tabWidget_main.setCurrentIndex(0)
            self.lineEdit_real_value.setText(f"{data.get('real_values')[0]}")
    
    def verify_if_selected_surfaces_are_in_tree_widget_specific_impedance(self):
        if self.tree_item_clicked:
            return

        selected_surfaces = app().main_window.selected_geometry_surfaces

        if not selected_surfaces:
            return

        self.clear_line_edit_selection_id()
        self.treeWidget_specific_impedance.clearSelection()
        self.pushButton_remove.setDisabled(True)

        map_id_to_model_index = self.get_tree_widget_specific_impedance_items_map()
        selected_ids = set(map_id_to_model_index.keys())
        selected_surfaces_in_tree_widget = selected_surfaces.intersection(selected_ids)

        if not selected_surfaces_in_tree_widget:
            return
        
        self.pushButton_remove.setEnabled(True)
        
        model_selector = self.treeWidget_specific_impedance.selectionModel()

        for surface_id in selected_surfaces_in_tree_widget:
            model_index = map_id_to_model_index[surface_id]

            model_selector.select(model_index, QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)

        self.treeWidget_specific_impedance.setSelectionMode(QAbstractItemView.SingleSelection)
        self.set_selection_text(selected_surfaces_in_tree_widget)

    def get_tree_widget_specific_impedance_items_map(self) -> dict:
        map_id_to_model_index = dict()

        index = self.treeWidget_specific_impedance.indexAt(QPoint(0, 0))
        while index.isValid():
            item = self.treeWidget_specific_impedance.itemFromIndex(index)
            surface_id = item.text(0)

            map_id_to_model_index[int(surface_id)] = index

            index = self.treeWidget_specific_impedance.indexBelow(index)
        
        return map_id_to_model_index


    def load_model_info(self):
        self.treeWidget_specific_impedance.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "specific_impedance":

                if "anechoic_termination" in data.keys():
                    continue

                if "table_names" in data.keys():
                    str_value = "Table of values"
                else:
                    real_values = np.array(data["real_values"])
                    imag_values = np.array(data["imag_values"])
                    complex_values = real_values + 1j * imag_values
                    str_value = str(complex_values)

                new = QTreeWidgetItem([str(surface_id), str_value])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_specific_impedance.addTopLevelItem(new)

        self.update_tabs_visibility()

    def attribute_callback(self):
        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == 0:
            self.check_constant_values()
        elif tab_index == 1:
            self.check_table_values()

    def check_complex_entries(self, lineEdit_real, lineEdit_imag):
        self.stop = False
        title = "Invalid entry to the specific impedance"
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                message = "Wrong input for real part of specific impedance."
                PrintMessageInput([error_title, title, message])
                self.lineEdit_real_value.setFocus()
                self.stop = True
                return
        else:
            real_F = 0

        if lineEdit_imag.text() != "":
            try:
                imag_F = float(lineEdit_imag.text())
            except Exception:
                message = "Wrong input for imaginary part of specific impedance."
                PrintMessageInput([error_title, title, message])
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

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(
                                                               input_ids, 
                                                               selection = "surfaces",
                                                               single_id = False,
                                                               )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        self.remove_conflicting_excitations(surface_ids)

        specific_impedance = self.check_complex_entries(
                                                        self.lineEdit_real_value, 
                                                        self.lineEdit_imag_value
                                                        )

        if specific_impedance is not None:

            real_values = [np.real(specific_impedance)]
            imag_values = [np.imag(specific_impedance)]

            data = {
                    "real_values" : real_values,
                    "imag_values" : imag_values,
                    }

            for surface_id in surface_ids:
                self.properties._set_property("specific_impedance", data, surface=surface_id)

            self.actions_to_finalize()

        else:
            title = "Additional inputs required"
            message = "You must enter the specific impedance to"
            message += "proceed with the attribution."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_real_value.setFocus()

    def load_table(self, lineEdit : QLineEdit, direct_load=False):
        title = "Error reached while loading 'specific impedance' table"
        imported_file = None

        try:
            if direct_load:
                imported_table_path = lineEdit.text()
                imported_file = DataImporter.read_data_in_file(imported_table_path).data

            else:
                imported_data = DataImporter.import_single_file("imported_table_folder",
                    ["csv", "dat", "txt", "xlsx", "xls"], "Choose a table to import the specific impedance")
                                
                if not imported_data:
                    return

                imported_file = imported_data.data
                lineEdit.setText(imported_data.path)

            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have three columns in the form: frequencies, real and imaginary values."
                PrintMessageInput([error_title, title, message])
                return None

            return imported_file

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            lineEdit.setFocus()
            return None, None

    def save_table_values(self, table_name: str, imported_values: np.ndarray):

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

        self.update_analysis_setup_in_file(_frequencies)

        real_values = imported_values[:, 1]
        imag_values = imported_values[:, 2]

        data = np.array([_frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def update_analysis_setup_in_file(self, frequencies: np.ndarray):

        analysis_setup = app().file.read_analysis_setup_from_file()
        if analysis_setup is None:
            analysis_setup = dict()

        f_min = frequencies[0]
        f_max = frequencies[-1]
        f_step = frequencies[1] - frequencies[0] 

        analysis_setup["f_min"] = float(f_min)
        analysis_setup["f_max"] = float(f_max)
        analysis_setup["f_step"] = float(f_step)

        app().project.set_analysis_setup(analysis_setup)
        app().file.write_analysis_setup_in_file(analysis_setup)

    def load_specific_impedance_table(self):
        self.imported_values = self.load_table(self.lineEdit_table_path)

    def check_table_values(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(
                                                               input_ids, 
                                                               selection = "surfaces",
                                                               single_id = False,
                                                               )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        self.remove_conflicting_excitations(surface_ids)

        if self.lineEdit_table_path.text() != "":

            if self.imported_values is None:
                self.imported_values = self.load_table( self.lineEdit_table_path, 
                                                        direct_load = True )
                
            for surface_id in surface_ids:

                if isinstance(self.imported_values, np.ndarray):
                    if self.imported_values.shape[1] >= 3:

                        table_name = f"specific_impedance_at_surface_{surface_id}"
                        if self.save_table_values(table_name, self.imported_values):
                            self.lineEdit_table_path.setFocus()
                            self.imported_values = None
                            return

                else:
                    return

                if self.imported_values is None:
                    return

                complex_values = self.imported_values[:, 1] + 1j * self.imported_values[:, 2]
                table_path = self.lineEdit_table_path.text()

                data = {
                        "table_names" : [table_name],
                        "table_paths" : [table_path],
                        "values" : [complex_values],
                        }

                self.properties._set_property("specific_impedance", data, surface=surface_id)

            self.actions_to_finalize()

        else:
            title = "Additional inputs required"
            message = "You must inform at least one specific impedance\n"
            message += "table path before confirming the input!"
            PrintMessageInput([error_title, title, message])
            self.lineEdit_table_path.setFocus()

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().file.write_imported_table_data_in_file()

    def remove_conflicting_excitations(self, surface_ids: int | list):

        if isinstance(surface_ids, int):
            surface_ids = [surface_ids]

        labels = [
                  "specific_impedance",
                  "incident_plane_wave",
                  ]

        for surface_id in surface_ids:
            for label in labels:
                table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_id : list):
        table_names = self.properties.get_property_related_table_names("specific_impedance", surface_id, "surfaces")
        self.process_table_file_removal(table_names)

    def remove_callback(self):
        selected_items = self.treeWidget_specific_impedance.selectedItems()

        if not selected_items:
            return

        for item in selected_items:
            surface_id = int(item.text(0))
            self.remove_table_files_from_surfaces(surface_id)

            data = self.properties._get_property("specific_impedance", surface=surface_id)
            if "anechoic_termination" in data.keys():
                continue

            self.properties._remove_surface_property("specific_impedance", surface_id)

        self.clear_line_edit_selection_id()
        self.pushButton_remove.setDisabled(True)

        app().main_window.clear_selection()
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Specific impedance resetting"
        message = "Would you like to remove the all applied specific impedances from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            surface_ids = list()
            for (property, *args), data in self.properties.surface_properties.items():
                if property == "specific_impedance":
                    if "anechoic_termination" in data.keys():
                        continue
                    surface_ids.append(args[0])

            self.remove_table_files_from_surfaces(surface_ids)
            for surface_id in surface_ids:
                self.properties._remove_surface_property("specific_impedance", surface_id)

            self.actions_to_finalize()

    def actions_to_finalize(self):
        self.load_model_info()
        self.check_model_frequency_controls()
        app().main_window.update_info_text()
        app().file.write_model_properties_in_file()
        app().file.write_imported_table_data_in_file()
        app().main_window.update_symbols()

    def change_frequency_setup(self):
        if self.imported_values is not None:
            self.hide()
            obj = ChangeFrequencyDataRangeInput(self.imported_values)
            if obj.filter_data is not None:
                self.imported_values = obj.filter_data

    def check_model_frequency_controls(self):

        for key, data in self.properties.surface_properties.items():
            property, _ = key
            if property in ["acoustic_pressure", "surface_velocity", "specific_impedance", "reciprocating_compressor_excitation"]:
                if "table_names" in data.keys():
                    return

        if isinstance(self.project.analysis_setup, dict):
            analysis_setup = self.project.analysis_setup
            self.project.set_analysis_setup(analysis_setup)
            app().file.write_analysis_setup_in_file(analysis_setup)

    def reset_input_fields(self):
        self.lineEdit_real_value.setText("")
        self.lineEdit_imag_value.setText("")
        self.lineEdit_table_path.setText("")

    def update_tabs_visibility(self):

        for key, data in self.properties.surface_properties.items():
            property, *args = key
            if property == "specific_impedance":
                if "anechoic_termination" in data.keys():
                    continue
                self.tabWidget_main.setTabVisible(2, True)
                return

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_main.setTabVisible(2, False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Control:
            self.treeWidget_specific_impedance.setSelectionMode(QAbstractItemView.MultiSelection)
        elif event.key() == Qt.Key_Shift:
            self.treeWidget_specific_impedance.setSelectionMode(QAbstractItemView.ContiguousSelection)
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.treeWidget_specific_impedance.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)