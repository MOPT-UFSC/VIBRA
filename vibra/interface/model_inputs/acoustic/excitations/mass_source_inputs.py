from collections import defaultdict
from enum import IntEnum
from traceback import print_exception

import numpy as np
from PySide6.QtCore import QItemSelectionModel, QPoint, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.extensions import SUPPORTED_SPREADSHEET_EXTENSIONS, SUPPORTED_TEXT_EXTENSIONS
from vibra.interface import error_title
from vibra.interface.common.common_interface import update_analysis_setup_in_file
from vibra.interface.data.data_manager import get_spectral_data_from_array
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.acoustic.definitions.enums import StandardTabType
from vibra.interface.ui_generated.model.acoustic.excitations.mass_source_inputs_ui import MassSourceInputs_UI
from vibra.interface.user_input.data_handler.file_dialog_service import FileDialogService
from vibra.interface.user_input.data_handler.file_handlers.file_handler import FileHandler


class AssignmentType(IntEnum):
    NODES = 0
    POINTS = 1
    LINES = 2
    SURFACES = 3
    VOLUMES = 4


class TabIndex(IntEnum):
    CONSTANT_DATA = StandardTabType.CONSTANT_DATA
    TABULAR_DATA = StandardTabType.TABULAR_DATA
    ADVANCED_SEARCH = 2
    LIST = 3


class MassSourceInputs(MassSourceInputs_UI):
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
        self.selection_type = {
                               0 : "nodes",
                               1 : "points",
                               2 : "lines",
                               3 : "surfaces",
                               4 : "volumes"
                               }
        self.last_tab = self.treeWidget_mass_source.currentIndex()
        self.tree_item_clicked = False

    def _configure_qt_variables(self):
        #
        self.lineEdit_nearest_node_id.setDisabled(True)
        self.lineEdit_node_coord_x.setDisabled(True)
        self.lineEdit_node_coord_y.setDisabled(True)
        self.lineEdit_node_coord_z.setDisabled(True)

        for i, w in enumerate([100, 120]):
            self.treeWidget_mass_source.setColumnWidth(i, w)
            self.treeWidget_mass_source.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_load_table.clicked.connect(self.load_mass_source_table)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_get_nearest_node.clicked.connect(self.compute_nearest_node_from_coordinate)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_mass_source.itemClicked.connect(self.on_click_item)
        self.treeWidget_mass_source.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

    def geometry_selection_callback(self):

        volumes = app().main_window.selection.geometry_volumes
        surfaces = app().main_window.selection.geometry_surfaces
        lines = app().main_window.selection.geometry_lines
        points = app().main_window.selection.geometry_points
        nodes = app().main_window.selection.mesh_nodes

        tab_list = self.tabWidget_main.currentIndex() == TabIndex.LIST

        if tab_list:
            self.verify_if_selected_items_are_in_tree_mass_source_inputs()
            return

        text = ""
        if volumes:
            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(AssignmentType.VOLUMES)

        elif surfaces:
            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(AssignmentType.SURFACES)

        elif lines:
            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(AssignmentType.LINES)

        elif points:
            text = ", ".join([str(i) for i in points])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(AssignmentType.POINTS)

        elif nodes:
            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(AssignmentType.NODES)

        if len(nodes) == 1:
            node_id = list(nodes)[0]
            self.load_property_data(node_id, "nodes")

        elif len(points) == 1:
            point_id = list(points)[0]
            self.load_property_data(point_id, "points")

        elif len(lines) == 1:
            line_id = list(lines)[0]
            self.load_property_data(line_id, "lines")

        elif len(surfaces) == 1:
            surface_id = list(surfaces)[0]
            self.load_property_data(surface_id, "surfaces")

        elif len(volumes) == 1:
            volume_id = list(volumes)[0]
            self.load_property_data(volume_id, "volumes")

        if len(volumes):
            self.comboBox_inherit_fluid_from.clear()
            self.comboBox_inherit_fluid_from.addItem("Each volume")

        elif len(nodes) + len(points) + len(lines) + len(surfaces):
            self.check_fluid_inheritance()

    def load_property_data(self, selection_id: int, selection_type: str):

        if selection_type == "points":
            data = self.model.properties._get_property("mass_source", point=selection_id)
        elif selection_type == "lines":
            data = self.model.properties._get_property("mass_source", line=selection_id)
        elif selection_type == "surfaces":
            data = self.model.properties._get_property("mass_source", surface=selection_id)
        elif selection_type == "volumes":
            data = self.model.properties._get_property("mass_source", volume=selection_id)
        else:
            data = self.model.properties._get_property("mass_source", node=selection_id)

        if isinstance(data, dict):

            if "table_paths" in data.keys():
                self.tabWidget_main.setCurrentIndex(TabIndex.TABULAR_DATA)
                self.lineEdit_table_path.setText(data["table_paths"][0])

            else:
                self.tabWidget_main.setCurrentIndex(TabIndex.CONSTANT_DATA)
                self.lineEdit_real_value.setText(str(data["real_values"][0]))
                self.lineEdit_imag_value.setText(str(data["imag_values"][0]))
    
    def verify_if_selected_items_are_in_tree_mass_source_inputs(self):
        if self.tree_item_clicked:
            return

        selected_volumes = {(volume_id, "volume") for volume_id in app().main_window.selection.geometry_volumes}
        selected_surfaces = {(surface_id, "surface") for surface_id in app().main_window.selection.geometry_surfaces}
        selected_points = {(point_id, "point") for point_id  in app().main_window.selection.geometry_points}
        selected_nodes = {(node_id, "node")  for node_id in app().main_window.selection.mesh_nodes}
        selected_lines = {(line_id, "line") for line_id in app().main_window.selection.geometry_lines}
        selected_items = [selected_volumes, selected_surfaces, selected_points, selected_nodes, selected_lines]

        if not any(selected_items):
            return

        self.clear_line_edit_selection_id()
        self.treeWidget_mass_source.clearSelection()
        self.pushButton_remove.setDisabled(True)

        map_id_to_model_index = self.get_tree_widget_viscous_thermal_model_items_map()
        selected_ids = set(map_id_to_model_index.keys())

        selected_items_in_tree_widget = set()
        for selected_item in selected_items:
            selected_items_in_tree_widget = selected_items_in_tree_widget.union(selected_ids.intersection(selected_item))

        if not selected_items_in_tree_widget:
            return

        self.pushButton_remove.setEnabled(True)
        model_selector = self.treeWidget_mass_source.selectionModel()

        selected_items_in_tree_widget_map = defaultdict(list)

        for selected_item in selected_items_in_tree_widget:
            model_index = map_id_to_model_index[selected_item]

            selected_id, selected_type = selected_item
            selected_items_in_tree_widget_map[selected_type + "s"].append(selected_id)

            model_selector.select(model_index, QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)

        self.treeWidget_mass_source.setSelectionMode(QAbstractItemView.SingleSelection)
        self.set_selection_text(selected_items_in_tree_widget_map)

    def get_tree_widget_viscous_thermal_model_items_map(self) -> dict:
        map_id_to_model_index = dict()

        index = self.treeWidget_mass_source.indexAt(QPoint(0, 0))
        while index.isValid():
            item = self.treeWidget_mass_source.itemFromIndex(index)
            selected_id = int(item.text(0))
            selected_type = item.text(1)

            map_id_to_model_index[(selected_id, selected_type)] = index

            index = self.treeWidget_mass_source.indexBelow(index)
        
        return map_id_to_model_index


    def attribution_type_callback(self):

        attribution_type = self.comboBox_attribution_type.currentIndex()
        if attribution_type == AssignmentType.NODES:
            app().main_window.action_mesh_workspace_callback()
        else:
            app().main_window.action_model_workspace_callback()

        if attribution_type in [AssignmentType.NODES, AssignmentType.POINTS]:
            self.comboBox_inherit_fluid_from.setEnabled(True)
            self.label_mass_source_unit.setText("[kg/s]")

        elif attribution_type == AssignmentType.LINES:
            self.comboBox_inherit_fluid_from.setEnabled(True)
            self.label_mass_source_unit.setText("[kg/m.s]")

        elif attribution_type == AssignmentType.SURFACES:
            self.comboBox_inherit_fluid_from.setEnabled(True)
            self.label_mass_source_unit.setText("[kg/m².s]")

        else:
            self.comboBox_inherit_fluid_from.clear()
            self.comboBox_inherit_fluid_from.setDisabled(True)
            self.comboBox_inherit_fluid_from.addItem("Each volume")
            self.label_mass_source_unit.setText("[kg/m³.s]")

        selection_data = self.check_selection_data(False)

        if selection_data is None:
            self.comboBox_inherit_fluid_from.clear()
            self.comboBox_inherit_fluid_from.setDisabled(True)
            self.lineEdit_selection_id.setFocus()
            return

        self.check_fluid_inheritance()

    def check_volumes_from_selection(self, data: dict, print_message: bool = False):

        volume_ids_sets = list()
        non_repeated_volume_ids = set()

        last_size = 0
        current_size = 0
        multiple_selection = False

        for vol_ids in data.values():
            if len(vol_ids) == 1:
                non_repeated_volume_ids |= set(vol_ids)

            sorted_vol_ids = list(np.sort(vol_ids))               
            if sorted_vol_ids in volume_ids_sets:
               continue
            
            current_size = len(sorted_vol_ids)
            volume_ids_sets.append(sorted_vol_ids)
            if last_size:
                if last_size != current_size:
                    multiple_selection = True    

            last_size = current_size      

        if not multiple_selection:
            try:
                volume_sets = np.array(volume_ids_sets, dtype=int)
                if len(np.unique(volume_sets, axis=0)) != 1:
                    multiple_selection = True

                if non_repeated_volume_ids and not multiple_selection:
                    if len(np.unique(non_repeated_volume_ids)) != 1:
                        multiple_selection = True

            except Exception as error_log:
                print_exception(error_log)
                multiple_selection = True

        if multiple_selection:
            self.comboBox_inherit_fluid_from.clear()
            self.comboBox_inherit_fluid_from.setDisabled(True)
            self.comboBox_inherit_fluid_from.addItem("Invalid selection")

            app().main_window.selection.clear_selection()

            if print_message:
                self.hide()
                title = "Invalid selection detected"
                message = "The current selection resulted in improper mapping between selected "
                message += "between selected entities and the volumes. To univocally assign fluids "
                message += "for mass source calculation, select groups of entities associated "
                message += "with the same volume or volume sets."
                PrintMessageInput([error_title, title, message])

            return True

        return False

    def update_inheritance_combo_box_data(self, data: dict, print_message: bool = False):

        if self.check_volumes_from_selection(data, print_message):
            return True

        combo_box = self.comboBox_inherit_fluid_from
        combo_box.clear()
        combo_box.setDisabled(True)

        def check_item_text(item_text: str) -> bool:
            for i in range(combo_box.count()):
                if item_text == combo_box.itemText(i):
                    return True
            return False

        for vol_ids in data.values():
            for vol_id in vol_ids:
                item_text = f"Volume - {vol_id}"
                if check_item_text(item_text):
                    continue
                combo_box.addItem(item_text)

            if len(vol_ids) > 1:
                combo_box.setEnabled(True)

        return False

    def check_fluid_inheritance(
                                self, 
                                selection_ids: list | None = None, 
                                selection_type: str | None = None, 
                                print_message: bool = False
                                ):

        if selection_type is None:
            selection_data = self.check_selection_data()
            if selection_data is None:
                return

            selection_ids, selection_type = selection_data

        if selection_type == "points":
            volumes_from_points = self.mesh.get_volumes_from_selected_points(selection_ids)
            return self.update_inheritance_combo_box_data(volumes_from_points, print_message)

        elif selection_type == "nodes":
            volumes_from_nodes = self.mesh.get_volumes_from_selected_nodes(selection_ids)
            return self.update_inheritance_combo_box_data(volumes_from_nodes, print_message)

        elif selection_type == "lines":
            volumes_from_lines = self.mesh.get_volumes_from_selected_lines(selection_ids)
            return self.update_inheritance_combo_box_data(volumes_from_lines, print_message)

        elif selection_type == "surfaces":
            volumes_from_surfaces = self.mesh.get_volumes_from_selected_surfaces(selection_ids)
            return self.update_inheritance_combo_box_data(volumes_from_surfaces, print_message)

        return False

    def check_inputs(
                     self, 
                     lineEdit: QLineEdit, 
                     label: str, 
                     _float: bool=True, 
                     only_positive: bool=False, 
                     zero_included: bool=True
                     ):

        message = ""

        title = "Invalid value typed"
        input_str = lineEdit.text()

        if input_str != "":

            input_str = input_str.replace(",", ".")

            try:
                if _float:
                    out = float(input_str)
                else:
                    out = int(input_str)

                if only_positive:
                    if zero_included:
                        if out < 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\nNote: zero value is allowed."
                    else:
                        if out <= 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\nNote: zero value is not allowed."

            except Exception as _err:
                message = f"You have typed an invalid value at the {label} input field.\n\n"
                message += str(_err)

        else:
            message = f"Insert some value at the {label} input field."

        if message != "":
            self.hide()
            lineEdit.setFocus()
            PrintMessageInput([error_title, title, message])
            return None
        else:
            return out

    def compute_nearest_node_from_coordinate(self):

        self.comboBox_attribution_type.setCurrentIndex(AssignmentType.NODES)

        coord_x = self.check_inputs(self.lineEdit_point_coord_x, "Point coord. x")
        if coord_x is None:
            return

        coord_y = self.check_inputs(self.lineEdit_point_coord_y, "Point coord. x")
        if coord_y is None:
            return

        coord_z = self.check_inputs(self.lineEdit_point_coord_z, "Point coord. x")
        if coord_z is None:
            return

        # point coordinates
        point_coords = np.array([coord_x, coord_y, coord_z], dtype=float)

        nearest_node, nearest_coords = self.mesh.get_nearest_node_from_coordinate(point_coords)
        if nearest_node is None:
            return

        self.lineEdit_nearest_node_id.setText(f"{nearest_node}")
        self.lineEdit_node_coord_x.setText(f"{nearest_coords[0] : .6f}")
        self.lineEdit_node_coord_y.setText(f"{nearest_coords[1] : .6f}")
        self.lineEdit_node_coord_z.setText(f"{nearest_coords[2] : .6f}")

        app().main_window.selection.set_mesh_selection(nodes=[nearest_node])

    def tab_event_callback(self):
        current_tab = self.tabWidget_main.currentIndex()
        tab_list = current_tab == TabIndex.LIST

        if self.last_tab == TabIndex.LIST or tab_list:
            app().main_window.selection.clear_selection()
            self.lineEdit_selection_id.clear()

        if tab_list:
            self.pushButton_remove.setDisabled(True)
            self.treeWidget_mass_source.clearSelection()
    
        self.comboBox_attribution_type.setDisabled(tab_list)
        self.lineEdit_selection_id.setDisabled(tab_list)
        self.pushButton_apply.setDisabled(tab_list)
        self.pushButton_apply_and_close.setDisabled(tab_list)

        self.comboBox_attribution_type.setVisible(not tab_list)
        self.comboBox_inherit_fluid_from.setVisible(not tab_list)
        self.label_10.setVisible(not tab_list)
        
        self.last_tab = current_tab

    def apply_callback(self, close_window: bool = False):
        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == StandardTabType.LIST:
            return

        selection_data = self.check_selection_data()
        if selection_data is None:
            return

        selection_ids, selection_type = selection_data
        if self.check_fluid_inheritance(selection_ids, selection_type, True):
            return

        self.remove_conflicting_excitations(selection_ids, selection_type)

        if tab_index == TabIndex.CONSTANT_DATA:
            if self.constant_data_assignment(selection_type, selection_ids):
                return

        elif tab_index == TabIndex.TABULAR_DATA:
            if self.tabular_data_assignment(selection_type, selection_ids):
                return

        self.actions_to_finalize(close_window)

    def check_selection_data(self, print_message: bool = True):

        attribution_type = self.comboBox_attribution_type.currentIndex()
        selection_type = self.selection_type.get(attribution_type)

        input_ids = self.lineEdit_selection_id.text()
        selection_ids, error_data = self.mesh.check_selected_ids(
                                                                 input_ids, 
                                                                 selection = selection_type
                                                                 )

        if error_data is not None:
            if print_message:
                self.hide()
                self.lineEdit_selection_id.setFocus()
                PrintMessageInput(error_data)
            return None

        return (selection_ids, selection_type)

    def check_complex_entries(self, lineEdit_real, lineEdit_imag):
        self.stop = False
        title = "Invalid entry to the acoustic pressure"
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                message = "Wrong input for real part of acoustic pressure."
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
                message = "Wrong input for imaginary part of acoustic pressure."
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

    def constant_data_assignment(self, selection_type: str, selection_ids: list[int]):
        
        mass_source = self.check_complex_entries(self.lineEdit_real_value, self.lineEdit_imag_value)

        if mass_source is None:
            self.hide()
            title = "Additional inputs required"
            message = "You must enter a non-zero value to the mass source input fields to proceed with the assignment."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_real_value.setFocus()
            return True

        real_values = [np.real(mass_source)]
        imag_values = [np.imag(mass_source)]
        
        if selection_type in ["points", "nodes", "lines", "surfaces"]:
            current_text = self.comboBox_inherit_fluid_from.currentText()
            vol_id = int(current_text.split(" - ")[1])
            data = {"real_values": real_values, "imag_values": imag_values, "volume_id": vol_id}

        else:
            data = {
                "real_values": real_values,
                "imag_values": imag_values,
            }

        for selection_id in selection_ids:
            if selection_type == "points":
                self.properties._set_property("mass_source", data, point=selection_id)
            elif selection_type == "nodes":
                self.properties._set_property("mass_source", data, node=selection_id)
            elif selection_type == "lines":
                self.properties._set_property("mass_source", data, line=selection_id)
            elif selection_type == "surfaces":
                self.properties._set_property("mass_source", data, surface=selection_id)
            else:
                self.properties._set_property("mass_source", data, volume=selection_id)

    def load_table(self, lineEdit : QLineEdit, direct_load=False):
        title = "Error reached while loading 'mass source' table"

        try:
            if direct_load:
                imported_path = lineEdit.text()

            else:
                extensions = SUPPORTED_SPREADSHEET_EXTENSIONS + SUPPORTED_TEXT_EXTENSIONS
                imported_path = FileDialogService.open_file(file_extensions=extensions,
                                                            caption="Choose a table to import the mass source",
                                                            last_folder="imported_table_folder")

            imported_data = FileHandler.read(imported_path)

            if imported_data is None:
                return

            if not direct_load:
                lineEdit.setText(str(imported_data.path))

            imported_values = imported_data.data

            if imported_values.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum data must "
                message += "have three columns in the form: frequencies, real and imaginary values."
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
            return None

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
        imag_values = imported_values[:, 2]

        data = np.array([_frequencies, real_values, imag_values], dtype=float).T
        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def load_mass_source_table(self):
        self.imported_values = self.load_table(self.lineEdit_table_path)

    def tabular_data_assignment(self, selection_type: str, selection_ids: list[int]):

        if self.lineEdit_table_path.text() == "":
            self.hide()
            title = "Additional inputs required"
            message = "You must enter the mass source table path to proceed with the assignment."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_table_path.setFocus()
            return True

        if self.imported_values is None:
            self.imported_values = self.load_table(self.lineEdit_table_path, direct_load=True)

        for selection_id in selection_ids:
            if isinstance(self.imported_values, np.ndarray):
                if self.imported_values.shape[1] >= 3:
                    table_name = f"mass_source_at_{selection_type}_{selection_id}"
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

            if selection_type in ["points", "nodes", "lines", "surfaces"]:
                current_text = self.comboBox_inherit_fluid_from.currentText()
                vol_id = int(current_text.split(" - ")[1])
                data = {"table_names": [table_name], "table_paths": [table_path], "values": [complex_values], "volume_id": vol_id}

            else:
                data = {
                    "table_names": [table_name],
                    "table_paths": [table_path],
                    "values": [complex_values],
                }

            if selection_type == "points":
                self.properties._set_property("mass_source", data, point=selection_id)
            elif selection_type == "nodes":
                self.properties._set_property("mass_source", data, node=selection_id)
            elif selection_type == "lines":
                self.properties._set_property("mass_source", data, line=selection_id)
            elif selection_type == "surfaces":
                self.properties._set_property("mass_source", data, surface=selection_id)
            else:
                self.properties._set_property("mass_source", data, volume=selection_id)

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().project.update_model_properties_file()

    def remove_conflicting_excitations(self, selection_ids: int | list, selection_type: str):

        if isinstance(selection_ids, int):
            selection_ids = [selection_ids]

        labels = [
            "acoustic_pressure",
            "surface_velocity",
            "incident_plane_wave",
            "compressor_excitation_spectrum",
            "compressor_excitation_waveform",
            "reciprocating_compressor_excitation",
            "mass_source",
            ]

        for label in labels:
            for selection_id in selection_ids:
                table_names = self.properties.get_property_related_table_names(label, selection_id, selection_type)
                if selection_type == "nodes":
                    self.properties._remove_nodal_property(label, selection_id)
                elif selection_type == "points":
                    self.properties._remove_point_property(label, selection_id)
                elif selection_type == "lines":
                    self.properties._remove_line_property(label, selection_id)
                elif selection_type == "surfaces":
                    self.properties._remove_surface_property(label, selection_id)
                elif selection_type == "volumes":
                    self.properties._remove_volume_property(label, selection_id)

                self.process_table_file_removal(table_names)

    def remove_table_files_from_selection(self, selection_id : list, selection_type: str):
        table_names = self.properties.get_property_related_table_names("mass_source", selection_id, selection_type)
        self.process_table_file_removal(table_names)

    def remove_callback(self):
        selected_items = self.get_selected_items_from_tree_widget_mass_source()

        if not selected_items:
            return

        for selected_type, selected_ids in selected_items.items():
            self.remove_table_files_from_selection(selected_ids, selected_type)

            for selected_id in selected_ids:
                if selected_type == "nodes":
                    self.properties._remove_nodal_property("mass_source", selected_id)

                elif selected_type == "points":
                    self.properties._remove_point_property("mass_source", selected_id)

                elif selected_type == "lines":
                        self.properties._remove_line_property("mass_source", selected_id)

                elif selected_type == "surfaces":
                    self.properties._remove_surface_property("mass_source", selected_id)

                else:
                    self.properties._remove_volume_property("mass_source", selected_id)

        self.clear_line_edit_selection_id()
        self.pushButton_remove.setDisabled(True)
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Mass source resetting"
        message = "Would you like to remove the all applied mass sources from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            properties_to_reset = { 
                                   "nodes" : self.properties.nodal_properties,
                                   "points" : self.properties.point_properties,
                                   "lines" : self.properties.line_properties,
                                   "surfaces" : self.properties.surface_properties,
                                   "volumes" : self.properties.volume_properties,
                                   }

            for selection_type, _properties in properties_to_reset.items():

                selection_ids = list()
                for (property, *args) in _properties.keys():
                    if property != "mass_source":
                        continue
    
                    selection_ids.append(args[0])

                for selection_id in selection_ids:
                    self.remove_table_files_from_selection(selection_id, selection_type)

            self.properties._reset_property("mass_source")
            self.actions_to_finalize()

    def actions_to_finalize(self, close_window: bool = False):
        self.load_model_info()
        self.comboBox_inherit_fluid_from.clear()
        app().main_window.update_info_text()
        app().project.update_model_properties_file()
        app().main_window.selection.clear_selection()
        app().main_window.update_symbols()

        if close_window:
            self.close()

    def reset_input_fields(self):
        self.lineEdit_real_value.setText("")
        self.lineEdit_imag_value.setText("")
        self.lineEdit_table_path.setText("")

    def update_tabs_visibility(self):

        properties = [
            self.properties.nodal_properties,
            self.properties.point_properties,
            self.properties.line_properties,
            self.properties.surface_properties,
            self.properties.volume_properties,
        ]

        for m_property in properties:
            for key in m_property.keys():
                property, *args = key
                if property != "mass_source":
                    continue

                self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
                return

        self.tabWidget_main.setCurrentIndex(TabIndex.CONSTANT_DATA)    
        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)

    def on_click_item(self, item):
        self.tree_item_clicked = True

        selected_items = self.get_selected_items_from_tree_widget_mass_source()

        if not selected_items:
            return

        self.pushButton_remove.setEnabled(True)
        self.set_selection_text(selected_items)

        nodes = selected_items.pop("nodes") if "nodes" in selected_items else set()

        app().main_window.selection.set_mesh_selection(nodes=nodes)
        app().main_window.selection.set_geometry_selection(**selected_items)

        self.tree_item_clicked = False

    def on_doubleclick_item(self, item):
        self.on_click_item(item)
    
    def get_selected_items_from_tree_widget_mass_source(self) -> dict:
        _selected_items = self.treeWidget_mass_source.selectedItems()

        if not _selected_items:
            return dict()

        selected_items = defaultdict(set)

        for item in _selected_items:
            selected_id = item.text(0)
            selected_type = item.text(1) + "s"

            selected_items[selected_type].add(int(selected_id))
        
        return selected_items
    
    def set_selection_text(self, selected_items: dict):
        selection_text = ""

        for selected_type, selected_ids in selected_items.items():
            selection_text += selected_type.capitalize() + ": "

            selected_ids = map(str, selected_ids)
            selected_ids = list(selected_ids)
            selected_ids.sort()

            selection_text += ", ".join(selected_ids) + " "

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)
    
    def clear_line_edit_selection_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")

    def load_model_info(self):

        model_properties = {
                            "node" : self.properties.nodal_properties,
                            "point" : self.properties.point_properties,
                            "line" : self.properties.line_properties,
                            "surface" : self.properties.surface_properties,
                            "volume" : self.properties.volume_properties,
                            }

        self.treeWidget_mass_source.clear()
        for selection_label, m_property in model_properties.items():
            for key, data in m_property.items():
                property, selection_id = key
                if property != "mass_source":
                    continue

                if "table_names" in data.keys():
                    str_value = "Table of values"
                else:
                    real_values = np.array(data["real_values"])
                    imag_values = np.array(data["imag_values"])
                    complex_values = real_values + 1j * imag_values
                    str_value = str(complex_values)

                new = QTreeWidgetItem([str(selection_id), selection_label, str_value])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_mass_source.addTopLevelItem(new)

        self.update_tabs_visibility()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Control:
            self.treeWidget_mass_source.setSelectionMode(QAbstractItemView.MultiSelection)
        elif event.key() == Qt.Key_Shift:
            self.treeWidget_mass_source.setSelectionMode(QAbstractItemView.ContiguousSelection)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.treeWidget_mass_source.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)