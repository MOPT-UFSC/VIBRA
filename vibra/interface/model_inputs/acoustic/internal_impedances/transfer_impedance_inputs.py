import logging
import warnings
from copy import deepcopy

import numpy as np
from PySide6.QtCore import QItemSelectionModel, QPoint, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.interface import error_title
from vibra.interface.common.common_interface import update_analysis_setup_in_file
from vibra.interface.data.data_manager import get_spectral_data_from_array
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.model_inputs.acoustic.definitions.enums import StandardTabType
from vibra.interface.ui_generated.model.acoustic.internal_impedances.transfer_impedance_inputs_ui import TransferImpedanceInputs_UI
from vibra.utils.bidict import bidict


class TransferImpedanceInputs(TransferImpedanceInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._configure_qt_variables()
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
        self.assignment_complete = False
        self.keep_window_open = True
        self.ti_data = dict()
        self.last_tab = self.tabWidget_main.currentIndex()
        self.tree_item_clicked = False
        self.decoupling_map = bidict()

    def _configure_qt_variables(self):
        for i in range(2):
            self.treeWidget_transfer_impedance.headerItem().setTextAlignment(i, Qt.AlignCenter)

        self.treeWidget_transfer_impedance.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _create_connections(self):
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_load_table.clicked.connect(self.load_transfer_impedance_table)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_transfer_impedance.itemClicked.connect(self.on_click_item)
        self.treeWidget_transfer_impedance.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.geometry_selection_callback()
    
    def geometry_selection_callback(self):
        current_tab = self.tabWidget_main.currentIndex()

        if current_tab == StandardTabType.LIST:
            self.verify_if_selected_surfaces_are_in_tree_widget_transfer_impedance()
            return
        
        if current_tab != StandardTabType.CONSTANT_DATA:
            return

        surfaces = app().main_window.selection.geometry_surfaces
        if surfaces:
            surface_ids = list(surfaces)
            surface_ids.sort()

            text = ", ".join([str(i) for i in surface_ids])
            self.lineEdit_selection_id.setText(text)

            if len(surface_ids) == 1:
                pp_data = self.properties._get_property("transfer_impedance", surface=surface_ids[0])
                if pp_data is None:
                    return

                self.load_property_data(pp_data)

    def load_property_data(self, pp_data: dict):

        if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
            return
        
        if not isinstance(pp_data, dict):
            return
        
        if "table_paths" in pp_data.keys():
            self.tabWidget_main.setCurrentIndex(StandardTabType.TABULAR_DATA)
            self.lineEdit_table_path.setText(pp_data["table_paths"][0])
        else:
            self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)
            self.lineEdit_real_value.setText(str(pp_data["real_values"][0]))
            self.lineEdit_imag_value.setText(str(pp_data["imag_values"][0]))
        
    def verify_if_selected_surfaces_are_in_tree_widget_transfer_impedance(self):
        if self.tree_item_clicked:
            return

        selected_surfaces = app().main_window.selection.geometry_surfaces

        if not selected_surfaces:
            return

        self.clear_line_edit_selection_id()
        self.treeWidget_transfer_impedance.clearSelection()
        self.pushButton_remove.setDisabled(True)

        map_id_to_model_index = self.get_tree_widget_transfer_impedance_items_map()
        selected_ids = set(map_id_to_model_index.keys())
        selected_surfaces_in_tree_widget = selected_surfaces.intersection(selected_ids)

        if not selected_surfaces_in_tree_widget:
            return
        
        self.pushButton_remove.setEnabled(True)
        
        model_selector = self.treeWidget_transfer_impedance.selectionModel()

        for surface_id in selected_surfaces_in_tree_widget:
            model_index = map_id_to_model_index[surface_id]

            model_selector.select(model_index, QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)

        self.treeWidget_transfer_impedance.setSelectionMode(QAbstractItemView.SingleSelection)
        self.set_selection_text(selected_surfaces_in_tree_widget)

    def get_tree_widget_transfer_impedance_items_map(self) -> dict:
        map_id_to_model_index = dict()

        index = self.treeWidget_transfer_impedance.indexAt(QPoint(0, 0))
        while index.isValid():
            item = self.treeWidget_transfer_impedance.itemFromIndex(index)
            surface_id = int(item.text(0))

            map_id_to_model_index[int(surface_id)] = index

            decoupling_data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_id)
            if isinstance(decoupling_data, dict):
                new_surface_id = decoupling_data.get("new_surface_id")

                map_id_to_model_index[new_surface_id] = index
                self.decoupling_map[surface_id] = new_surface_id

            index = self.treeWidget_transfer_impedance.indexBelow(index)
        
        return map_id_to_model_index

    def check_selected_surfaces(self):

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
            return list()

        if self.check_selection_type(surface_ids):
            return list()

        surface_ids.sort()

        return surface_ids

    def apply_callback(self, close_window: bool = False):

        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == StandardTabType.LIST:
            return

        surface_ids = self.check_selected_surfaces()
        if not surface_ids:
            return

        self.remove_conflicting_excitations(surface_ids)

        if tab_index == StandardTabType.CONSTANT_DATA:
            if self.constant_data_assignment(surface_ids):
                return

        elif tab_index == StandardTabType.TABULAR_DATA:
            if self.tabular_data_assignment(surface_ids):
                return

        self.hide()
        self.actions_to_finalize(close_window)

    def constant_data_assignment(self, surface_ids: int | tuple[int]):
        
        real_value = self.check_inputs(self.lineEdit_real_value, "Real part of transfer impedance", only_positive=False)
        imag_value = self.check_inputs(self.lineEdit_imag_value, "Imaginary part of transfer impedance", only_positive=False)

        if (real_value, imag_value).count(None):
            return True

        if real_value + imag_value == 0:
            self.hide()
            title = "Additional inputs required"
            message = "You must enter a non-zero transfer impedance value to proceed with the assignment."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_real_value.setFocus()
            return True

        self.ti_data.update(
            {
                "real_values": [real_value],
                "imag_values": [imag_value],
            }
        )

        for surface_id in surface_ids:
            self.properties._set_property("transfer_impedance", deepcopy(self.ti_data), surface=surface_id)
            self.decouple_degrees_of_freedom(surface_id)

        self.assignment_complete = True
        self.clear_line_edit_selection_id()

    def load_table(self, lineEdit : QLineEdit, direct_load=False):

        title = "Error reached while loading 'specific impedance' table"
        imported_values = None

        try:
            if direct_load:
                imported_table_path = lineEdit.text()
                imported_values = DataImporter.read_data_in_file(imported_table_path)[0].data
            else:
                imported_data = DataImporter.import_single_file("imported_table_folder",
                    ["csv", "dat", "txt", "xlsx", "xls"], "Choose a table to import the specific impedance")

                if not imported_data:
                    return None

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

            return _imported_values

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            lineEdit.setFocus()
            return None, None

    def save_table_values(self, table_name: str, imported_values: np.ndarray):

        mask = imported_values[:, 0] > 0
        _imported_values = imported_values[mask, :]
        _frequencies = _imported_values[:, 0]

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
        imag_values = imported_values[:, 2]

        data = np.array([_frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def load_transfer_impedance_table(self):
        self.imported_values = self.load_table(self.lineEdit_table_path)

    def tabular_data_assignment(self, surface_ids: int | tuple[int]):

        if self.lineEdit_table_path.text() == "":
            self.hide()
            title = "Additional inputs required"
            message = "You must enter the transfer impedance table path to proceed with the assignment."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_table_path.setFocus()
            return True

        if self.imported_values is None:
            self.imported_values = self.load_table(self.lineEdit_table_path, direct_load = True)

        if self.imported_values is None:
            return True

        for surface_id in surface_ids:
            self.include_transfer_impedance_table_data(surface_id)
            self.properties._set_property("transfer_impedance", deepcopy(self.ti_data), surface=surface_id)
            self.decouple_degrees_of_freedom(surface_id)

        self.assignment_complete = True
        self.clear_line_edit_selection_id()

    def tab_event_callback(self):
        current_tab = self.tabWidget_main.currentIndex()
        tab_list = current_tab == StandardTabType.LIST

        if self.last_tab == StandardTabType.LIST or tab_list:
            app().main_window.selection.clear_selection()
            self.clear_line_edit_selection_id()

        self.last_tab = current_tab

        if tab_list:
            self.pushButton_remove.setDisabled(True)
            self.lineEdit_selection_id.setDisabled(True)
            self.treeWidget_transfer_impedance.clearSelection()

            return

        self.geometry_selection_callback()
        self.lineEdit_selection_id.setEnabled(True)

    def on_click_item(self, item: QTreeWidgetItem):
        self.tree_item_clicked = True

        surface_ids = self.get_selected_surfaces_from_tree_widget_transfer_impedance()
        if not surface_ids:
            return

        app().main_window.selection.set_geometry_selection(surfaces=surface_ids)

        for surface_id in surface_ids:
            decoupling_data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_id)

            if isinstance(decoupling_data, dict):
                new_surface_id = decoupling_data.get("new_surface_id")
                if new_surface_id is None:
                    continue

                self.decoupling_map[surface_id] = new_surface_id

        self.pushButton_remove.setEnabled(True)
        self.set_selection_text(surface_ids)

        self.tree_item_clicked = False

    def on_doubleclick_item(self, item: QTreeWidgetItem):
        self.on_click_item(item)

    def get_selected_surfaces_from_tree_widget_transfer_impedance(self) -> list:
        selected_items = self.treeWidget_transfer_impedance.selectedItems()
        if not selected_items:
            return list()
        
        return [int(item.text(0)) for item in selected_items]
    
    def set_selection_text(self, selected_surfaces: list | set):
        selected_surfaces_decoupled = list()

        for selected_surface in selected_surfaces:
            decouple_surface = self.decoupling_map.get(selected_surface)
            if decouple_surface is None:
                decouple_pair = [selected_surface, "Awaiting uncoupling"]

            else:
                decouple_pair = [selected_surface, decouple_surface]
                decouple_pair.sort()
                       
            decouple_pair = tuple(decouple_pair)
            selected_surfaces_decoupled.append(str(decouple_pair))

        selection_text = ", ".join(selected_surfaces_decoupled)

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)
    
    def clear_line_edit_selection_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")
                
    def clear_all_inputs(self):
        self.lineEdit_real_value.clear()
        self.lineEdit_imag_value.clear()
        self.lineEdit_table_path.clear()

    def check_selection_type(self, surface_ids: list[int]):

        title = "Invalid selection detected"

        for surface_id in surface_ids:
            if len(self.mesh.volumes_from_surface[surface_id]) != 2:
                self.hide()
                message = f"The selected surface ID #{surface_id} does not correspond to an inside surface "
                message += "(surfaces that connect two neighboohrs volumes). The transfer impedance "
                message += "assignment will be ignored until all requirements are met."
                PrintMessageInput([error_title, title, message])
                self.ti_data.clear()
                return True

    def load_model_info(self):

        self.treeWidget_transfer_impedance.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "transfer_impedance":

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
                self.treeWidget_transfer_impedance.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        for key, _ in self.properties.surface_properties.items():
            property, _ = key
            if property == "transfer_impedance":
                self.tabWidget_main.setTabVisible(StandardTabType.LIST, True)
                return

        self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)
        self.tabWidget_main.setTabVisible(StandardTabType.LIST, False)

    def load_user_defined_transfer_impedance(self):
        self.imported_values = self.load_table(self.lineEdit_user_defined_transfer_impedance_path)

    def include_transfer_impedance_table_data(self, surface_id: int | list[int]):

        if isinstance(surface_id, int):
            table_name = f"user_defined_transfer_impedance_at_surface_{surface_id}"
        else:
            table_name = f"user_defined_transfer_impedance_between_surfaces_{surface_id[0]}_{surface_id[1]}"

        if self.save_table_values(table_name, self.imported_values):
            self.lineEdit_table_path.setFocus()
            self.imported_values = None
            self.ti_data.clear()
            return

        # complex values computed from tabular data
        complex_values = get_spectral_data_from_array(self.imported_values)

        # table path from imported tabular data
        table_path = self.lineEdit_table_path.text()

        self.ti_data["table_names"] = [table_name]
        self.ti_data["table_paths"] = [table_path]
        self.ti_data["values"] = [complex_values]

    def decouple_degrees_of_freedom(self, surface_id: int):

        volumes_from_surface = self.mesh.volumes_from_surface.get(surface_id)
        if volumes_from_surface is None:
            return 

        volume_id = volumes_from_surface[0]
        data = {"volume_to_decouple" : volume_id}
        self.properties._set_property("degrees_of_freedom_decoupling", data, surface=surface_id)

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().project.update_model_properties_file()

    def remove_conflicting_excitations(self, surface_ids: int | list[int]):

        if isinstance(surface_ids, int):
            surface_ids = [surface_ids]

        labels = [
            "perforated_plate_model", 
            "interior_impedance",
            ]

        for surface_id in surface_ids:
            for label in labels:
                table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_ids : int | tuple[int]):
        table_names = self.properties.get_property_related_table_names("transfer_impedance", surface_ids, "surfaces")
        self.process_table_file_removal(table_names)

    def remove_all_surface_properties_from_surface(self, new_surface_ids: list[int]):
        if not new_surface_ids:
            return

        surface_properties = deepcopy(self.properties.surface_properties)
        for new_surface_id in new_surface_ids:
            for (property, surf_id) in surface_properties.keys():
                if surf_id == new_surface_id:
                    self.properties._remove_surface_property(property, new_surface_id)

    def remove_all_line_properties_boundind_surface(self, new_surface_ids: list[int]):
        if not new_surface_ids:
            return

        line_properties = deepcopy(self.properties.line_properties)
        for new_surface_id in new_surface_ids:
            lines_from_surface = self.mesh.lines_from_surface.get(new_surface_id)
            if lines_from_surface is None:
                continue

            for line_from_surface in lines_from_surface:
                for (property, line_id) in line_properties.keys():
                    if line_from_surface == line_id:
                        self.properties._remove_line_property(property, line_id)

    def remove_callback(self):
        input_ids = self.get_selected_surfaces_from_tree_widget_transfer_impedance()

        if not input_ids:
            return

        surface_ids, error_data = self.mesh.check_selected_ids(
                                                                input_ids, 
                                                                selection = "surfaces", 
                                                                )
        
        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        self.remove_table_files_from_surfaces(surface_ids)

        for surface_id in surface_ids:
            self.properties._remove_surface_property("transfer_impedance", surface_id)

            data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_id)

            if isinstance(data, dict):
                new_surface_id = data.get("new_surface_id")
                if isinstance(new_surface_id, int):   
                    self.remove_all_surface_properties_from_surface([new_surface_id])
                    self.remove_all_line_properties_boundind_surface([new_surface_id]) 

                self.properties._remove_surface_property("degrees_of_freedom_decoupling", surface_id)

                app().project.project_writer.delete_mesh_data()
                app().project.project_writer.delete_results_data()
                # self.restore_mesh_data_modified_by_decoupling()
                
        self.clear_line_edit_selection_id()
        self.pushButton_remove.setDisabled(True)

        app().main_window.selection.clear_selection()
        self.actions_to_finalize()
        self.restore_mesh_data_modified_by_decoupling()

    def reset_callback(self):

        surface_ids = list()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "transfer_impedance":
                surface_ids.append(surface_id)

        if not surface_ids:
            return

        self.hide()

        title = "Transfer impedance resetting"
        message = "Would you like to remove the transfer impedance from the acoustic model?"

        buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        new_surface_ids = list()
        for surf_id in surface_ids:
            self.remove_table_files_from_surfaces(surf_id)
            data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surf_id)
            if isinstance(data, dict):
                new_surface_id = data.get("new_surface_id")
                if isinstance(new_surface_id, int):
                    new_surface_ids.append(new_surface_id)
                    self.properties._remove_surface_property("degrees_of_freedom_decoupling", surf_id)

        self.remove_all_surface_properties_from_surface(new_surface_ids)
        self.remove_all_line_properties_boundind_surface(new_surface_ids)
        self.properties._reset_property("transfer_impedance")

        self.actions_to_finalize()
        self.restore_mesh_data_modified_by_decoupling()

    def actions_to_finalize(self, close_window: bool = False):

        def callback():

            logging.info("Processing the post-assignment actions... [10/100]")
            self.load_model_info()

            logging.info("Processing the post-assignment actions... [20/100]")
            app().main_window.analysis_toolbar.reset_solution()

            logging.info("Processing the post-assignment actions... [30/100]")
            app().project.project_writer.delete_mesh_data()

            logging.info("Processing the post-assignment actions... [60/100]")
            app().project.update_model_properties_file()

            logging.info("Processing the post-assignment actions... [70/100]")
            app().main_window.recompute_hidden_volumes()

            logging.info("Processing the post-assignment actions... [80/100]")
            app().main_window.update_info_text()

            logging.info("Processing the post-assignment actions... [90/100]")
            app().main_window.update_symbols()

            logging.info("Processing the post-assignment actions... [95/100]")
            app().main_window.selection.set_geometry_selection()

        LoadingWindow(callback).run()

        if close_window:
            self.close()

    def process_decoupling_actions(self):

        def callback():
            logging.info("Processing degress of freedom decoupling... [10/100]")
            self.model.process_degrees_of_freedom_decoupling()

            logging.info("Processing degress of freedom decoupling... [70/100]")
            app().project.write_to_working_dir()

            # the degrees of freedom modifies the surfaces properties
            logging.info("Processing degress of freedom decoupling... [80/100]")
            app().project.update_model_properties_file()

            logging.info("Processing degress of freedom decoupling... [85/100]")
            app().main_window.update_mesh_information()

            logging.info("Processing degress of freedom decoupling... [90/100]")
            app().main_window.update_geometry_information()
        
            logging.info("Processing degress of freedom decoupling... [95/100]")
            app().main_window.update_plots()

        LoadingWindow(callback).run()

    def restore_mesh_data_modified_by_decoupling(self):

        if self.mesh.cache_nodal_coordinates is None:
            return

        self.mesh.restore_data_from_cache()
        self.mesh.process_upwards_adjacencies_from_entities()

        # if self.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):
        #     self.mesh.cache_mesh_information()

        self.process_decoupling_actions()

    def check_inputs(self, line_edit: QLineEdit, label: str, only_positive: bool=True):

        title = "Invalid value typed"
        message = ""
        
        input_str = line_edit.text()

        if input_str == "":
            return 0.

        input_str = input_str.replace(",", ".")

        try:

            out = float(input_str)

            if only_positive and out < 0:
                message = f"Insert a positive value to the {label}."
                message += "\n\nNote: zero value is not allowed."

        except Exception as error_log:
            message = f"You have typed an invalid value at the {label} input field.\n\n"
            message += str(error_log)

        if message != "":
            self.hide()
            line_edit.setFocus()
            PrintMessageInput([error_title, title, message])
            return None

        return out

    def process_degress_of_freedom_decoupling(self):

        if not self.assignment_complete:
            return False

        if not self.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):
            return False

        if not app().project.model.is_there_a_valid_mesh():
            self.hide()
            app().main_window.input_ui.mesh_setup()
            app().main_window.set_input_widget(self)
            return False

        if self.mesh.cache_nodal_coordinates is None:
            # self.mesh.cache_mesh_information()
            pass

        else:
            self.mesh.restore_data_from_cache()
            self.mesh.process_upwards_adjacencies_from_entities()
            # self.mesh.cache_mesh_information()

        self.process_decoupling_actions()

        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Control:
            self.treeWidget_transfer_impedance.setSelectionMode(QAbstractItemView.MultiSelection)
        elif event.key() == Qt.Key_Shift:
            self.treeWidget_transfer_impedance.setSelectionMode(QAbstractItemView.ContiguousSelection)
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.treeWidget_transfer_impedance.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        self.hide()

        try:
            warnings.filterwarnings('default')
        except TypeError:
            pass

        if self.process_degress_of_freedom_decoupling():
            return

        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)

        return super().closeEvent(a0)

# fmt: on