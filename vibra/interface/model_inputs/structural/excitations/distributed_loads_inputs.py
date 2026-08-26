
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
from vibra.interface.ui_generated.model.structural.excitations.distributed_loads_inputs_ui import DistributedLoadsInputs_UI


class ElementFormulation(IntEnum):
    ELEMENT_2D = 0
    ELEMENT_3D = 1


class AssignmentType(IntEnum):
    SURFACES = 0
    LINES = 1
    MULTIPLE = 2


class DistributedLoadsInputs(DistributedLoadsInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._create_list_line_edits()
        self._configure_validators()
        self._create_connections()

        self._config_widgets()
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

    def _configure_validators(self):
        for line_edit_real, line_edit_imag in self.constant_values_line_edits:
            line_edit_real.setValidator(StrictDoubleValidator(-1e16, 1e16, 8))
            line_edit_imag.setValidator(StrictDoubleValidator(-1e16, 1e16, 8))

    def reset_table_variables(self):

        self.Fx_table_values = None
        self.Fy_table_values = None
        self.Fz_table_values = None

        self.Fx_array = None
        self.Fy_array = None
        self.Fz_array = None

        self.Fx_table_path = None
        self.Fy_table_path = None
        self.Fz_table_path = None

        self.Fx_table_name = None
        self.Fy_table_name = None
        self.Fz_table_name = None

    def _create_list_line_edits(self):
        self.constant_values_line_edits = [
            [self.lineEdit_left_Fx, self.lineEdit_right_Fx],
            [self.lineEdit_left_Fy, self.lineEdit_right_Fy],
            [self.lineEdit_left_Fz, self.lineEdit_right_Fz],
        ]

        self.table_line_edits = {
            "Fx": self.lineEdit_path_table_Fx,
            "Fy": self.lineEdit_path_table_Fy,
            "Fz": self.lineEdit_path_table_Fz,
        }

        self.unit_labels = {
            "Fx": self.label_unit_Fx,
            "Fy": self.label_unit_Fy,
            "Fz": self.label_unit_Fz,
        }

    def _config_widgets(self):

        self.comboBox_element_type.setEnabled(False)
        self.treeWidget_distributed_loads.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        for i, w in enumerate([60, 80, 100, 100]):
            self.treeWidget_distributed_loads.setColumnWidth(i, w)
            self.treeWidget_distributed_loads.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):

        # QComboBox connections
        self.comboBox_assignment_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_data_type.currentIndexChanged.connect(self.data_type_callback)
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_callback)

        # QPushButton connections
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_load_Fx_table.clicked.connect(self.load_Fx_table)
        self.pushButton_load_Fy_table.clicked.connect(self.load_Fy_table)
        self.pushButton_load_Fz_table.clicked.connect(self.load_Fz_table)
        self.pushButton_reset.clicked.connect(self.reset_callback)

        # QTabWidget connections
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)

        # QTreeWidget connections
        self.treeWidget_distributed_loads.itemClicked.connect(self.item_clicked_callback)
        self.treeWidget_distributed_loads.itemDoubleClicked.connect(self.item_double_clicked_callback)
        self.treeWidget_distributed_loads.itemSelectionChanged.connect(self.item_selection_clicked_callback)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

        self.update_element_type_based_on_geometry_information()
        self.geometry_selection_callback()

    def geometry_selection_callback(self):

        surfaces = app().main_window.selection.geometry_surfaces
        lines = app().main_window.selection.geometry_lines

        if self.tabWidget_main.currentIndex() == StandardTabType.LIST and (lines and surfaces):
            self.lineEdit_selection_id.setText("mult. entities")
            self.comboBox_assignment_type.setCurrentIndex(AssignmentType.MULTIPLE)
            view = self.comboBox_assignment_type.view()
            view.setRowHidden(2, False)
            return

        if surfaces:
            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_assignment_type.setCurrentIndex(AssignmentType.SURFACES)

            if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
                return

            if len(surfaces) == 1:
                surface_id = next(iter(surfaces))
                data = self.properties._get_property("distributed_loads", surface=surface_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(surface_id=surface_id)

        elif lines:
            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_assignment_type.setCurrentIndex(AssignmentType.LINES)

            if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
                return

            if len(lines) == 1:
                line_id = next(iter(lines))
                data = self.properties._get_property("distributed_loads", line=line_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(line_id=line_id)

    def update_input_fields(self, data: dict | None):

        if data is None:
            return

        self.reset_input_fields()

        element_type = data.get("element_type")
        if element_type == "2d_element":
            self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
        else:
            self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_3D)

        values = data.get("values", None)
        if "table_paths" in data:
            table_paths = data["table_paths"]
            for index, lineEdit_table in enumerate(self.table_line_edits.values()):
                table_path = table_paths[index]
                if table_path is not None:                   
                    lineEdit_table.setText(table_path)

            self.tabWidget_main.setCurrentIndex(StandardTabType.TABULAR_DATA)

        else:

            if "real_values" in data:
                left_values = data.get("real_values")
                right_values = data.get("imag_values")
                self.comboBox_data_type.setCurrentIndex(InputDataType.REAL_IMAGINARY)

            else:
                left_values = data.get("amplitude_values")
                right_values = data.get("phase_values")
                self.comboBox_data_type.setCurrentIndex(InputDataType.MAGNITUDE_PHASE)

            for index, [line_edit_left, line_edit_right] in enumerate(self.constant_values_line_edits):

                if element_type == "3d_element" and index >= 3:
                    continue

                elif index <= 5 and values[index] is not None:
                    line_edit_left.setText(str(left_values[index]))
                    line_edit_right.setText(str(right_values[index]))

            self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)

    def update_formulation_callback(self, **kwargs):

        surface_id = kwargs.get("surface_id", None)
        line_id = kwargs.get("line_id", None)

        if isinstance(surface_id, int):
            data = self.properties._get_property("surface_thickness", surface=surface_id)
            if isinstance(data, dict):
                self.comboBox_element_type.setCurrentIndex(0)
                return
            
        if isinstance(line_id, int):
            for node_id in self.mesh.get_nodes_from_line(line_id):
                for surface_id in self.mesh.get_surfaces_from_node(node_id):
                    data = self.properties._get_property("surface_thickness", surface=surface_id)
                    if isinstance(data, dict):
                        self.comboBox_element_type.setCurrentIndex(0)
                        return

    def attribution_type_callback(self):

        surface_assignment = self.comboBox_assignment_type.currentIndex() == AssignmentType.SURFACES
        load_label = "F{} / area:".format if surface_assignment else "F{} / length:".format

        self.label_constant_Fx.setText(load_label("x"))
        self.label_constant_Fy.setText(load_label("y"))
        self.label_constant_Fz.setText(load_label("z"))

        self.label_table_Fx.setText(load_label("x"))
        self.label_table_Fy.setText(load_label("y"))
        self.label_table_Fz.setText(load_label("z"))

        self.data_type_callback()

    def element_type_callback(self):
        return

    def data_type_callback(self):
        real_imaginary = self.comboBox_data_type.currentIndex() == InputDataType.REAL_IMAGINARY
        self.label_dtype_left.setText("Real" if real_imaginary else "Amplitude")
        self.label_dtype_right.setText("Imaginary" if real_imaginary else "Phase")

        unit = "N/m²" if self.comboBox_assignment_type.currentIndex() == AssignmentType.SURFACES else "N/m"

        for widget in self.unit_labels.values():
            label_text = f"[{unit}]" if real_imaginary else f"[{unit}, deg]"
            widget.setText(label_text)

    def update_element_type_based_on_geometry_information(self):
        volume_exists = self.mesh.are_there_volumes_in_geometry()
        self.comboBox_element_type.setCurrentIndex(int(volume_exists))

    def constant_values_attribution(self):

        input_ids = self.lineEdit_selection_id.text()
        assignment_type = self.comboBox_assignment_type.currentIndex()

        selection = "surfaces" if assignment_type == AssignmentType.SURFACES else "lines"
        unit = "N/m²" if assignment_type == AssignmentType.SURFACES else "N/m"

        selected_ids, error_data = self.mesh.check_selected_ids(input_ids, selection=selection, single_id=False)

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        self.remove_conflicting_excitations(selected_ids, selection)

        element_type = self.element_types[self.comboBox_element_type.currentIndex()]
        real_imag_input = self.comboBox_data_type.currentIndex() == InputDataType.REAL_IMAGINARY

        Fx = check_input_entries(self.lineEdit_left_Fx.text(), self.lineEdit_right_Fx.text(), "Fx")
        if Fx is None:
            return True

        Fy = check_input_entries(self.lineEdit_left_Fy.text(), self.lineEdit_right_Fy.text(), "Fy")
        if Fy is None:
            return True

        Fz = check_input_entries(self.lineEdit_left_Fz.text(), self.lineEdit_right_Fz.text(), "Fz")
        if Fz is None:
            return True

        distributed_loads = [Fx, Fy, Fz]

        all_values = []
        for values in distributed_loads:
            all_values.extend(values)

        condition_1 = element_type == "2d_element" and all_values.count(None) == 12
        condition_2 = element_type == "3d_element" and all_values.count(None) == 6

        if condition_1 or condition_2:
            title = "Additional inputs required"
            message = "You must to enter at least one distributed load value before confirming the assignment."
            PrintMessageInput([error_title, title, message])
            return True

        left_values = [value_a for (value_a, _) in distributed_loads]
        right_values = [value_b for (_, value_b) in distributed_loads]

        for selected_id in selected_ids:

            data = {
                "element_type": element_type,
                "real_values" if real_imag_input else "amplitude_values": left_values,
                "imag_values" if real_imag_input else "phase_values": right_values,
                "unit": unit,
            }

            if assignment_type == AssignmentType.SURFACES:
                self.properties._set_property("distributed_loads", data, surface=selected_id)

            elif assignment_type == AssignmentType.LINES:
                self.properties._set_property("distributed_loads", data, line=selected_id)

    def load_table(self, lineEdit : QLineEdit, load_label: str, direct_load = False):

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

    def load_Fx_table(self):
        self.Fx_table_values, self.Fx_table_path = self.load_table(self.lineEdit_path_table_Fx, "Fx")
        if  self.Fx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Fx)

    def load_Fy_table(self):
        self.Fy_table_values, self.Fy_table_path = self.load_table(self.lineEdit_path_table_Fy, "Fy")
        if self.Fy_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Fy)
            
    def load_Fz_table(self):
        self.Fz_table_values, self.Fz_table_path = self.load_table(self.lineEdit_path_table_Fz, "Fz")
        if self.Fz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Fz)

    def save_table_files(self, load_label: str, selected_id: int, selection: str, imported_values: np.ndarray):

        frequencies = imported_values[:, 0]

        if frequencies[0] == 0:
            frequencies[0] = 1e-6

        if frequencies[0] == 1e-6:
            frequencies[0] = 0

        if self.model.change_analysis_frequency_setup(list(frequencies)):

            lineEdit = self.table_line_edits[load_label]
            imported_filename = basename(lineEdit.text())
            self.lineEdit_reset(lineEdit)

            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup"
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\nFile name: {imported_filename}"
            PrintMessageInput([error_title, title, message])

            return None, None

        table_name = f"distributed_loads_{load_label}_from_{selection[:-1]}_{selected_id}"

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
        surfaces_assignment = self.comboBox_assignment_type.currentIndex() == AssignmentType.SURFACES

        selection = "surfaces" if surfaces_assignment else "lines"
        unit = "N/m²" if surfaces_assignment else "N/m"

        selected_ids, error_data = self.mesh.check_selected_ids(input_ids, selection=selection, single_id=False)

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        self.remove_conflicting_excitations(selected_ids, selection)

        index = self.comboBox_element_type.currentIndex()
        element_type = self.element_types[index]

        if self.Fx_table_path is None:
            self.Fx_table_values, self.Fx_table_path = self.load_table(self.lineEdit_path_table_Fx, "Fx", direct_load = True)

        if self.Fy_table_path is None:
            self.Fy_table_values, self.Fy_table_path = self.load_table(self.lineEdit_path_table_Fy, "Fy", direct_load = True)

        if self.Fz_table_path is None:
            self.Fz_table_values, self.Fz_table_path = self.load_table(self.lineEdit_path_table_Fz, "Fz", direct_load = True)

        for selected_id in selected_ids:
            
            if self.Fx_table_values is not None:
                self.Fx_table_name, self.Fx_array = self.save_table_files("Fx", selected_id, selection, self.Fx_table_values)
                if self.Fx_array is None:
                    return True

            if self.Fy_table_values is not None:
                self.Fy_table_name, self.Fy_array = self.save_table_files("Fy", selected_id, selection, self.Fy_table_values)
                if self.Fy_array is None:
                    return True

            if self.Fz_table_values is not None:
                self.Fz_table_name, self.Fz_array = self.save_table_files("Fz", selected_id, selection, self.Fz_table_values)
                if self.Fz_array is None:
                    return True

            table_names = [self.Fx_table_name, self.Fy_table_name, self.Fz_table_name]
            table_paths = [self.Fx_table_path, self.Fy_table_path, self.Fz_table_path]

            condition_1 = element_type == "2d_element" and table_names.count(None) == 3
            condition_2 = element_type == "3d_element" and table_names.count(None) == 3

            if condition_1 or condition_2:
                title = "Additional inputs required"
                message = "You must to enter at leat one distributed load table path before confirming the assignment."
                PrintMessageInput([error_title, title, message]) 
                return True

            data = {
                "element_type" : element_type,
                "table_names" : table_names,
                "table_paths" : table_paths,
                "unit" : unit,
            }

            if surfaces_assignment:
                self.properties._set_property("distributed_loads", data, surface=selected_id)

            else:
                self.properties._set_property("distributed_loads", data, line=selected_id)

        self.reset_table_variables()

    def apply_callback(self, close_window: bool=False):

        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == StandardTabType.LIST:
            return

        if tab_index == StandardTabType.CONSTANT_DATA:
            if self.constant_values_attribution():
                return

        else:
            if self.table_values_attribution():
                return

        self.actions_to_finalize(close_window)

    def text_label(self, mask):

        load_labels = np.array(['Fx','Fy','Fz'])
        labels = load_labels[mask]

        if list(mask).count(True) == 3:
            return "[{}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 2:
            return "[{}, {}]".format(*labels)
        elif list(mask).count(True) == 1:
            return "[{}]".format(*labels)

    def load_model_info(self):

        properties = {
            "line" : self.properties.line_properties,
            "surface" : self.properties.surface_properties,
        }

        self.treeWidget_distributed_loads.clear()

        for key, property in properties.items():
            for (prop_label, *args), data in property.items():

                if prop_label != "distributed_loads":
                    continue

                if not isinstance(data, dict):
                    continue

                values = data.get("values", [])
                element_type = data.get("element_type")

                active_values = []
                for value in values:
                    if value is not None:
                        active_values.append(value)

                dof_labels = str(self.text_label([bool(value) for value in values]))

                new = QTreeWidgetItem([
                    f"{args[0]}", 
                    key, 
                    element_type, 
                    dof_labels, 
                    ", ".join([str(val) for val in active_values]),
                    ])

                for i in range(5):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_distributed_loads.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        properties_to_check = [
            self.properties.surface_properties,
            self.properties.line_properties,
            self.properties.point_properties,
            self.properties.nodal_properties,
        ]

        for current_property in properties_to_check:
            for (property, _) in current_property:
                if property != "distributed_loads":
                    continue

                self.tabWidget_main.setTabVisible(StandardTabType.LIST, True)
                return

        self.tabWidget_main.setTabVisible(StandardTabType.LIST, False)
        self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)
        self.lineEdit_left_Fx.setFocus()

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
        else:
            view = self.comboBox_assignment_type.view()
            view.setRowHidden(2, True)
            self.comboBox_assignment_type.setCurrentIndex(AssignmentType.SURFACES)

        self.lineEdit_selection_id.setText("")
        self.treeWidget_distributed_loads.clearSelection()

    def item_selection_clicked_callback(self):
        self.item_clicked_callback(None)

    def item_clicked_callback(self, item):

        self.pushButton_remove.setDisabled(False)

        selected_items = self.treeWidget_distributed_loads.selectedItems()
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
            lines = entities_mapping.get("line"),
            )

    def item_double_clicked_callback(self, item):
        self.item_clicked_callback(item)

    def remove_conflicting_excitations(self, selected_ids: int | list, selection: str):

        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        if selection == "surfaces":
            remove_function = self.properties._remove_surface_property

        elif selection == "lines":
            remove_function = self.properties._remove_line_property

        properties = ["distributed_loads", "prescribed_dof"]

        for selected_id in selected_ids:
            for property in properties:
                remove_function(property, selected_id)

    def remove_callback(self):

        selected_items = self.treeWidget_distributed_loads.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            selected_id = int(item.text(0))
            selection = item.text(1)

            if selection == "surface":
                self.properties._remove_surface_property("distributed_loads", selected_id)

            elif selection == "line":
                self.properties._remove_line_property("distributed_loads", selected_id)

        self.actions_to_finalize()

        app().main_window.selection.set_geometry_selection()
        app().main_window.selection.set_mesh_selection()

    def reset_callback(self):

        title = "Distributed loads reset"
        message = "Would you like to remove the all distributed loads from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if obj._cancel:
            return

        if obj._continue:
            self.properties._reset_property("distributed_loads")
            self.actions_to_finalize()

            app().main_window.selection.set_geometry_selection()
            app().main_window.selection.set_mesh_selection()

    def actions_to_finalize(self, close_window: bool = False):
        self.load_model_info()
        self.reset_input_fields(reset_all=True)
        app().main_window.update_info_text()
        app().project.update_model_properties_file()
        app().main_window.update_symbols()

        if close_window:
            self.close()

    def reset_input_fields(self, reset_all=False):

        if reset_all:
            self.lineEdit_selection_id.setText("")

        for lineEdit_left, lineEdit_right in self.constant_values_line_edits:
            lineEdit_left.setText("")
            lineEdit_right.setText("")

        for lineEdit_table in self.table_line_edits.values():
            lineEdit_table.setText("")

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