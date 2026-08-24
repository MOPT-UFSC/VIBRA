
from collections import defaultdict
from enum import IntEnum
from os.path import basename

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem

from vibra import app, SUPPORTED_SPREADSHEET_EXTENSIONS, SUPPORTED_TEXT_EXTENSIONS
from vibra.interface import error_title
from vibra.interface.common.common_interface import update_analysis_setup_in_file
from vibra.interface.user_input.data_handler.file_handlers.file_handler import FileHandler
from vibra.interface.user_input.data_handler.file_dialog_service import FileDialogService
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.structural.definitions.enums import StandardTabType
from vibra.interface.ui_generated.model.structural.excitations.nodal_loads_inputs_ui import NodalLoadsInputs_UI


class ElementFormulation(IntEnum):
    ELEMENT_2D = 0
    ELEMENT_3D = 1


class AssignmetType(IntEnum):
    SURFACES = 0
    LINES = 1
    POINTS = 2
    NODES = 3


class NodalLoadsInputs(NodalLoadsInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._create_list_lineEdits()
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
        self.assignment_types = {
            0 : "surfaces",
            1 : "lines",
            2 : "points",
            3 : "nodes",
        }
        self.reset_table_variables()

    def reset_table_variables(self):

        self.Fx_table_values = None
        self.Fy_table_values = None
        self.Fz_table_values = None
        self.Mx_table_values = None
        self.My_table_values = None
        self.Mz_table_values = None

        self.Fx_array = None
        self.Fy_array = None
        self.Fz_array = None
        self.Mx_array = None
        self.My_array = None
        self.Mz_array = None

        self.Fx_table_path = None
        self.Fy_table_path = None
        self.Fz_table_path = None
        self.Mx_table_path = None
        self.My_table_path = None
        self.Mz_table_path = None

        self.Fx_table_name = None
        self.Fy_table_name = None
        self.Fz_table_name = None
        self.Mx_table_name = None
        self.My_table_name = None
        self.Mz_table_name = None

    def _create_list_lineEdits(self):

        self.list_lineEdit_constant_values = [
            [self.lineEdit_real_Fx, self.lineEdit_imag_Fx],
            [self.lineEdit_real_Fy, self.lineEdit_imag_Fy],
            [self.lineEdit_real_Fz, self.lineEdit_imag_Fz],
            [self.lineEdit_real_Mx, self.lineEdit_imag_Mx],
            [self.lineEdit_real_My, self.lineEdit_imag_My],
            [self.lineEdit_real_Mz, self.lineEdit_imag_Mz],
        ]

        self.table_lineEdits = {
            "Fx": self.lineEdit_path_table_Fx,
            "Fy": self.lineEdit_path_table_Fy,
            "Fz": self.lineEdit_path_table_Fz,
            "Mx": self.lineEdit_path_table_Mx,
            "My": self.lineEdit_path_table_My,
            "Mz": self.lineEdit_path_table_Mz,
        }

    def _config_widgets(self):
        #
        self.comboBox_element_type.setEnabled(False)
        #
        for i, w in enumerate([110, 150, 100]):
            self.treeWidget_nodal_loads.setColumnWidth(i, w)
            self.treeWidget_nodal_loads.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_callback)
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_load_Fx_table.clicked.connect(self.load_Fx_table)
        self.pushButton_load_Fy_table.clicked.connect(self.load_Fy_table)
        self.pushButton_load_Fz_table.clicked.connect(self.load_Fz_table)
        self.pushButton_load_Mx_table.clicked.connect(self.load_Mx_table)
        self.pushButton_load_My_table.clicked.connect(self.load_My_table)
        self.pushButton_load_Mz_table.clicked.connect(self.load_Mz_table)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_nodal_loads.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_loads.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.geometry_selection_callback()
        self.update_element_type_based_on_geometry_information()

    def geometry_selection_callback(self):

        faces = app().main_window.selection.geometry_surfaces
        lines = app().main_window.selection.geometry_lines
        points = app().main_window.selection.geometry_points
        nodes = app().main_window.selection.mesh_nodes

        if faces:

            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(0)

            if len(faces) == 1:
                surface_id = list(faces)[0]
                data = self.properties._get_property("nodal_loads", surface=surface_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(surface_id=surface_id)

        elif lines:

            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(1)

            if len(lines) == 1:
                line_id = list(lines)[0]
                data = self.properties._get_property("nodal_loads", line=line_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(line_id=line_id)

        elif points:

            text = ", ".join([str(i) for i in points])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(2)

            if len(points) == 1:
                point_id = list(points)[0]
                data = self.properties._get_property("nodal_loads", point=point_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(point_id=point_id)

        elif nodes:

            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(3)

            if len(nodes) == 1:
                node_id = list(nodes)[0]
                data = self.properties._get_property("nodal_loads", node=node_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(node_id=node_id)

    def update_input_fields(self, data: dict | None):

        if data is None:
            return

        self.reset_input_fields()

        element_type = data.get("element_type", None)
        if element_type == "2d_element":
            self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
        else:
            self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_3D)

        values = data.get("values", None)
        if "table_paths" in data.keys():
            table_paths = data["table_paths"]
            for index, lineEdit_table in enumerate(self.table_lineEdits.values()):
                if element_type == "3d_element" and index >= 3:
                    continue

                table_path = table_paths[index]
                if table_path is not None:                   
                    lineEdit_table.setText(table_path)

        else:
            for index, [lineEdit_real, lineEdit_imag] in enumerate(self.list_lineEdit_constant_values):
                if element_type == "3d_element" and index >= 3:
                    continue

                elif index <= 5 and values[index] is not None:
                    lineEdit_real.setText(str(np.real(values[index])))
                    lineEdit_imag.setText(str(np.imag(values[index])))

    def attribution_type_callback(self):
        if self.comboBox_attribution_type.currentIndex() == 3:
            app().main_window.action_mesh_workspace_callback()
        else:
            app().main_window.action_model_workspace_callback()

    def element_type_callback(self):

        element_2d = self.comboBox_element_type.currentIndex() == ElementFormulation.ELEMENT_2D

        self.label_Mx_constant.setVisible(element_2d)
        self.label_My_constant.setVisible(element_2d)
        self.label_Mz_constant.setVisible(element_2d)

        self.label_Mx_unit.setVisible(element_2d)
        self.label_My_unit.setVisible(element_2d)
        self.label_Mz_unit.setVisible(element_2d)

        self.label_Mx_table.setVisible(element_2d)
        self.label_My_table.setVisible(element_2d)
        self.label_Mz_table.setVisible(element_2d)

        self.lineEdit_real_Mx.setVisible(element_2d)
        self.lineEdit_real_My.setVisible(element_2d)
        self.lineEdit_real_Mz.setVisible(element_2d)

        self.lineEdit_imag_Mx.setVisible(element_2d)
        self.lineEdit_imag_My.setVisible(element_2d)
        self.lineEdit_imag_Mz.setVisible(element_2d)

        self.pushButton_load_Mx_table.setVisible(element_2d)
        self.pushButton_load_My_table.setVisible(element_2d)
        self.pushButton_load_Mz_table.setVisible(element_2d)

        self.lineEdit_path_table_Mx.setVisible(element_2d)
        self.lineEdit_path_table_My.setVisible(element_2d)
        self.lineEdit_path_table_Mz.setVisible(element_2d)

    def update_element_type_based_on_geometry_information(self):
        volume_exists = self.mesh.are_there_volumes_in_geometry()
        self.comboBox_element_type.setCurrentIndex(int(volume_exists))

    def check_complex_entries(self, real_input: str, imag_input: str, label: str):

        _real = None
        if real_input != "":
            try:
                real_input = real_input.replace(",", ".")
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
                imag_input = imag_input.replace(",", ".")
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
        attribution_type = self.comboBox_attribution_type.currentIndex()
        selection = self.assignment_types.get(attribution_type)

        selected_ids, error_data = self.mesh.check_selected_ids(input_ids, selection=selection, single_id=False)

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        index = self.comboBox_element_type.currentIndex()
        element_type = self.element_types[index]

        stop, Fx = self.check_complex_entries(self.lineEdit_real_Fx.text(), self.lineEdit_imag_Fx.text(), "Fx")
        if stop:
            return True

        stop, Fy = self.check_complex_entries(self.lineEdit_real_Fy.text(), self.lineEdit_imag_Fy.text(), "Fy")
        if stop:
            return True

        stop, Fz = self.check_complex_entries(self.lineEdit_real_Fz.text(), self.lineEdit_imag_Fz.text(), "Fz")
        if stop:
            return True

        nodal_loads = [Fx, Fy, Fz]

        if element_type == "2d_element":
            
            stop, rx = self.check_complex_entries(self.lineEdit_real_Mx.text(), self.lineEdit_imag_Mx.text(), "rx")
            if stop:
                return True

            stop, ry = self.check_complex_entries(self.lineEdit_real_My.text(), self.lineEdit_imag_My.text(), "ry")
            if stop:
                return True

            stop, Mz = self.check_complex_entries(self.lineEdit_real_Mz.text(), self.lineEdit_imag_Mz.text(), "Mz")
            if stop:
                return True

            nodal_loads.extend([rx, ry, Mz])

        condition_1 = element_type == "2d_element" and nodal_loads.count(None) == 6
        condition_2 = element_type == "3d_element" and nodal_loads.count(None) == 3

        if condition_1 or condition_2:
            self.hide()
            title = "Additional inputs required"
            message = "You must enter at least one nodal loads value before confirming the assignment."
            PrintMessageInput([error_title, title, message])
            return True

        self.remove_duplicated_attributions(selected_ids, selection)
        self.remove_conflicting_excitations(selected_ids, selection)

        real_values = [value if value is None else np.real(value) for value in nodal_loads]
        imag_values = [value if value is None else np.imag(value) for value in nodal_loads]

        key_avg = self.checkBox_averaged_constant_values.isChecked()

        for selected_id in selected_ids:
            data = {
                "element_type": element_type,
                "values": nodal_loads,
                "real_values": real_values,
                "imag_values": imag_values,
                "nodal_attribution": True,
                "averaged": key_avg,
            }

            if attribution_type == AssignmetType.SURFACES:
                self.properties._set_property("nodal_loads", data, surface=selected_id)

            elif attribution_type == AssignmetType.LINES:
                self.properties._set_property("nodal_loads", data, line=selected_id)

            elif attribution_type == AssignmetType.POINTS:
                self.properties._set_property("nodal_loads", data, point=selected_id)

            elif attribution_type == AssignmetType.NODES:
                self.properties._set_property("nodal_loads", data, node=selected_id)

    def load_table(self, lineEdit : QLineEdit, load_label : str, direct_load = False):
        title = "Error while loading table"

        try:
            if direct_load:
                imported_path = lineEdit.text()

            else:
                extensions = SUPPORTED_SPREADSHEET_EXTENSIONS + SUPPORTED_TEXT_EXTENSIONS
                imported_path = FileDialogService.open_file(file_extensions=extensions,
                                                            caption=f"Choose a table to import the {load_label} data",
                                                            last_folder="imported_table_folder")

            imported_data = FileHandler.read(imported_path)

            if imported_data is None:
                return None, None

            if not direct_load:
                lineEdit.setText(str(imported_data.path))

            imported_file = imported_data.data
            imported_table_path = str(imported_data.path)
            imported_filename = basename(imported_table_path)

            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum "
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([error_title, title, message])
                lineEdit.setFocus()
                return None, None

            imported_values = imported_file[:, 1] + 1j * imported_file[:, 2]
            self.frequencies = imported_file[:, 0]
        
            if app().project.model.change_analysis_frequency_setup(list(self.frequencies)):

                self.lineEdit_reset(lineEdit)

                title = "Project frequency setup cannot be modified"
                message = "The following imported table of values has a frequency setup "
                message += "different from the others already imported ones. The current "
                message += "project frequency setup is not going to be modified."
                message += f"\n\n{imported_filename}"
                PrintMessageInput([error_title, title, message])
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
            
    def load_Mx_table(self):
        self.Mx_table_values, self.Mx_table_path = self.load_table(self.lineEdit_path_table_Mx, "Mx")
        if self.Mx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Mx)
            
    def load_My_table(self):
        self.My_table_values, self.My_table_path = self.load_table(self.lineEdit_path_table_My, "My")
        if self.My_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_My)
            
    def load_Mz_table(self):
        self.Mz_table_values, self.Mz_table_path = self.load_table(self.lineEdit_path_table_Mz, "Mz")
        if self.Mz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Mz)

    def save_table_files(self, load_label: str, selected_id: int, selection: str, values: np.ndarray):
        if self.frequencies[0] == 0:
            self.frequencies[0] = float(1e-6)

        if self.frequencies[0] == float(1e-6):
            self.frequencies[0] = 0

        if app().project.model.change_analysis_frequency_setup(list(self.frequencies)):

            self.hide()
            lineEdit = self.table_lineEdits[load_label]
            imported_filename = basename(lineEdit.text())
            self.lineEdit_reset(lineEdit)

            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\nFile name: {imported_filename}"
            PrintMessageInput([error_title, title, message])

            return None, None

        table_name = f"nodal_loads_{load_label}_from_{selection[:-1]}_{selected_id}"

        real_values = np.real(values)
        imag_values = np.imag(values)
        data = np.array([self.frequencies, real_values, imag_values], dtype=float).T

        update_analysis_setup_in_file(self.frequencies)
        self.properties.add_imported_tables("structural", table_name, data)

        return table_name, data

    def table_values_attribution(self):

        input_ids = self.lineEdit_selection_id.text()
        attribution_type = self.comboBox_attribution_type.currentIndex()
        selection = self.assignment_types.get(attribution_type)

        selected_ids, error_data = self.mesh.check_selected_ids(input_ids, selection=selection, single_id=False)

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        index = self.comboBox_element_type.currentIndex()
        element_type = self.element_types[index]

        if self.Fx_table_path is None:
            self.Fx_table_values, self.Fx_table_path = self.load_table(self.lineEdit_path_table_Fx, "Fx", direct_load = True)

        if self.Fy_table_path is None:
            self.Fy_table_values, self.Fy_table_path = self.load_table(self.lineEdit_path_table_Fy, "Fy", direct_load = True)

        if self.Fz_table_path is None:
            self.Fz_table_values, self.Fz_table_path = self.load_table(self.lineEdit_path_table_Fz, "Fz", direct_load = True)

        if self.Mx_table_path is None:
            self.Mx_table_values, self.Mx_table_path = self.load_table(self.lineEdit_path_table_Mx, "Mx", direct_load = True)

        if self.My_table_path is None:
            self.My_table_values, self.My_table_path = self.load_table(self.lineEdit_path_table_My, "My", direct_load = True)

        if self.Mz_table_path is None:
            self.Mz_table_values, self.Mz_table_path = self.load_table(self.lineEdit_path_table_Mz, "Mz", direct_load = True)

        key_avg = self.checkBox_averaged_table_values.isChecked()

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
            nodal_loads = [self.Fx_table_values, self.Fy_table_values, self.Fz_table_values]

            if element_type == "2d_element":

                if self.Mx_table_values is not None:
                    self.Mx_table_name, self.Mx_array = self.save_table_files("Mx", selected_id, selection, self.Mx_table_values)
                    if self.Mx_array is None:
                        return True

                if self.My_table_values is not None:
                    self.My_table_name, self.Mx_array = self.save_table_files("My", selected_id, selection, self.My_table_values)
                    if self.My_array is None:
                        return True

                if self.Mz_table_values is not None:
                    self.Mz_table_name, self.Mx_array = self.save_table_files("Mz", selected_id, selection, self.Mz_table_values)
                    if self.Mz_array is None:
                        return True

                table_names.extend([self.Mx_table_name, self.My_table_name, self.Mz_table_name])
                table_paths.extend([self.Mx_table_path, self.My_table_path, self.Mz_table_path])
                nodal_loads.extend([self.Mx_table_values, self.My_table_values, self.Mz_table_values])

            condition_1 = element_type == "2d_element" and table_names.count(None) == 6
            condition_2 = element_type == "3d_element" and table_names.count(None) == 3

            if condition_1 or condition_2:
                self.hide()
                title = "Additional inputs required"
                message = "You must enter at least one nodal loads table path before confirming the assignment."
                PrintMessageInput([error_title, title, message]) 
                return True
           
            self.remove_duplicated_attributions(selected_ids, selection)
            self.remove_conflicting_excitations(selected_ids, selection)

            data = {
                "element_type": element_type,
                "table_names": table_names,
                "table_paths": table_paths,
                "values": nodal_loads,
                "nodal_attribution": True,
                "averaged": key_avg,
            }

            if attribution_type == AssignmetType.SURFACES:
                self.properties._set_property("nodal_loads", data, surface=selected_id)

            elif attribution_type == AssignmetType.LINES:
                self.properties._set_property("nodal_loads", data, line=selected_id)

            elif attribution_type == AssignmetType.POINTS:
                self.properties._set_property("nodal_loads", data, point=selected_id)

            elif attribution_type == AssignmetType.NODES:
                self.properties._set_property("nodal_loads", data, node=selected_id)

        self.reset_table_variables()

    def remove_duplicated_attributions(self, selected_ids: list, selection: str):

        table_names = list()
        nodes_to_remove = list()
        for selected_id in selected_ids:

            if selection == "surfaces":

                nodes_from_surface = self.model.mesh.get_nodes_from_surface(selected_id)
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "nodal_loads" and node_id in nodes_from_surface:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for line_id in self.mesh.lines_from_surface[selected_id]:
                    data = self.properties._get_property("nodal_loads", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("nodal_loads", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("nodal_loads", line_id, "lines"))

                    for point_id in self.mesh.points_from_line[line_id]:
                        data = self.properties._get_property("nodal_loads", point=point_id)
                        if isinstance(data, dict):
                            self.properties._remove_point_property("nodal_loads", point_id)
                            table_names.extend(self.properties.get_property_related_table_names("nodal_loads", point_id, "points"))

            elif selection == "lines":

                nodes_from_line = self.model.mesh.get_nodes_from_line(selected_id)
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "nodal_loads" and node_id in nodes_from_line:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for surface_id in self.mesh.surfaces_from_line[selected_id]:
                    data = self.properties._get_property("nodal_loads", surface=surface_id)
                    if isinstance(data, dict):
                        self.properties._remove_surface_property("nodal_loads", surface_id)
                        table_names.extend(self.properties.get_property_related_table_names("nodal_loads", surface_id, "surfaces"))

                for point_id in self.mesh.points_from_line[selected_id]:
                    data = self.properties._get_property("nodal_loads", point=point_id)
                    if isinstance(data, dict):
                        self.properties._remove_point_property("nodal_loads", point_id)
                        table_names.extend(self.properties.get_property_related_table_names("nodal_loads", point_id, "points"))

            elif selection == "points":

                nodes_from_point = self.model.mesh.nodes_from_points[selected_id]
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "nodal_loads" and node_id in nodes_from_point:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for line_id in self.mesh.lines_from_point[selected_id]:
                    data = self.properties._get_property("nodal_loads", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("nodal_loads", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("nodal_loads", line_id, "lines"))

                    for surface_id in self.model.mesh.surfaces_from_line[line_id]:
                        data = self.properties._get_property("nodal_loads", surface=surface_id)
                        if isinstance(data, dict):
                            self.properties._remove_surface_property("nodal_loads", surface_id)
                            table_names.extend(self.properties.get_property_related_table_names("nodal_loads", surface_id, "surfaces"))

            elif selection == "nodes":

                point_id = selected_id + 1
                data = self.properties._get_property("nodal_loads", point=point_id)
                if isinstance(data, dict):
                    self.properties._remove_point_property("nodal_loads", point_id)
                    table_names.extend(self.properties.get_property_related_table_names("nodal_loads", point_id, "points"))

                for line_id in self.mesh.lines_from_point[point_id]:
                    data = self.properties._get_property("nodal_loads", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("nodal_loads", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("nodal_loads", line_id, "lines"))

                    for surface_id in self.model.mesh.surfaces_from_line[line_id]:
                        data = self.properties._get_property("nodal_loads", surface=surface_id)
                        if isinstance(data, dict):
                            self.properties._remove_surface_property("nodal_loads", surface_id)
                            table_names.extend(self.properties.get_property_related_table_names("nodal_loads", surface_id, "surfaces"))

            for node_id in nodes_to_remove:
                self.properties._remove_nodal_property("nodal_loads", node_id)
                table_names.extend(self.properties.get_property_related_table_names("nodal_loads", node_id, "nodes"))

            self.process_table_file_removal(table_names)

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

    def text_label(self, mask):

        if len(mask) == 6:
            load_labels = np.array(['Fx','Fy','Fz','Mx','My','Mz'])

        elif len(mask) == 3:
            load_labels = np.array(['Fx','Fy','Fz'])

        labels = load_labels[mask]

        text = ""
        if list(mask).count(True) == 6:
            text = "[{}, {}, {}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 5:
            text = "[{}, {}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 4:
            text = "[{}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(*labels)
        elif list(mask).count(True) == 1:
            text = "[{}]".format(*labels)

        return text

    def add_model_info_in_treeWidget(self, entity: str):

        properties = {
                        "surface" : self.properties.surface_properties,
                        "line" : self.properties.line_properties,
                        "point" : self.properties.point_properties,
                        "node" : self.properties.nodal_properties,
                      }

        _property = properties.get(entity)
        if _property is None:
            return
        
        for (property, *args), data in _property.items():
            if property != "nodal_loads":
                continue

            values = data["values"]
            element_type = data["element_type"]
            constrained_dof_mask = [False if value is None else True for value in values]
            dof_labels = str(self.text_label(constrained_dof_mask))

            new = QTreeWidgetItem([f"{entity.capitalize()}-{args[0]}", dof_labels, element_type])
            for i in range(3):
                new.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_nodal_loads.addTopLevelItem(new)

    def load_model_info(self):

        self.treeWidget_nodal_loads.clear()

        self.add_model_info_in_treeWidget("surface")
        self.add_model_info_in_treeWidget("line")
        self.add_model_info_in_treeWidget("point")
        self.add_model_info_in_treeWidget("node")

        self.update_tabs_visibility()


    def update_tabs_visibility(self):

        properties_to_check = [
                               self.properties.surface_properties,
                               self.properties.line_properties,
                               self.properties.point_properties,
                               self.properties.nodal_properties,
                               ]

        for current_property in properties_to_check:
            for (property, _) in current_property.keys():
                if property == "nodal_loads":
                    self.tabWidget_main.setTabVisible(StandardTabType.LIST, True)
                    return

        self.lineEdit_real_Fx.setFocus()
        self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)
        self.tabWidget_main.setTabVisible(StandardTabType.LIST, False)
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

        self.pushButton_remove.setEnabled(True)

        if item.text(0) != "":

            selection, _selected_id = item.text(0).split("-")
            selected_id = int(_selected_id)

            if selection == "Surface":
                app().main_window.selection.set_geometry_selection(surfaces = [int(selected_id)])

            elif selection == "Line":
                app().main_window.selection.set_geometry_selection(lines = [int(selected_id)])

            elif selection == "Point":
                app().main_window.selection.set_geometry_selection(points = [int(selected_id)])

            elif selection == "Node":
                app().main_window.selection.set_mesh_selection(nodes=[int(selected_id)])

            if selection == "Node":
                app().main_window.action_mesh_workspace_callback()

            else:
                app().main_window.action_model_workspace_callback()

            self.lineEdit_selection_id.setText(item.text(0))

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

        properties = ["nodal_loads", "prescribed_dof"]

        for selected_id in selected_ids:
            for property in properties:
                table_names = self.properties.get_property_related_table_names(property, selected_id, selection)
                self.remove_property_from(property, selected_id, selection)
                self.process_table_file_removal(table_names)

    def remove_table_files_from(self, selected_id : int, selection: str):
        table_names = self.properties.get_property_related_table_names("nodal_loads", selected_id, selection)
        self.process_table_file_removal(table_names)

    def remove_property_from(self, property: str, selected_ids: int | list, selection: str):
        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        if "surface" in selection:
            remove_function = self.properties._remove_surface_property
        elif "line" in selection:
            remove_function = self.properties._remove_line_property
        elif "point" in selection:
            remove_function = self.properties._remove_point_property
        elif "node" in selection:
            remove_function = self.properties._remove_nodal_property
        else:
            return

        for selected_id in selected_ids:
            remove_function(property, selected_id)

    def remove_callback(self):

        text = self.lineEdit_selection_id.text()

        if "-" in text:

            _selection, _selected_id = text.split("-")
            selection = _selection.lower()
            selected_id = int(_selected_id)

            self.remove_table_files_from(selected_id, f"{selection}s")
            self.remove_property_from("nodal_loads", selected_id, selection)
            self.actions_to_finalize()

            app().main_window.selection.set_geometry_selection()
            app().main_window.selection.set_mesh_selection()

    def reset_callback(self):

        self.hide()

        title = "Nodal loads resetting"
        message = "Would you like to remove the all external loads from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if obj._cancel:
            return

        if obj._continue:

            properties = {
                "surfaces" : self.properties.surface_properties,
                "lines" : self.properties.line_properties,
                "points" : self.properties.point_properties,
                "nodes" : self.properties.nodal_properties,
                }

            entities_to_remove = defaultdict(list)

            for key, _property in properties.items():
                for (property_label, *args), data in _property.items():
                    if property_label != "nodal_loads":
                        continue
    
                    entities_to_remove[key].append(args[0])

            for selection, selected_ids in entities_to_remove.items():
                for selected_id in selected_ids:
                    table_name = self.properties.get_property_related_table_names("nodal_loads", selected_id, selection)
                    self.process_table_file_removal(table_name)

            self.properties._reset_property("nodal_loads")
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

        for lineEdit_real, lineEdit_imag in self.list_lineEdit_constant_values:
            lineEdit_real.setText("")
            lineEdit_imag.setText("")

        for lineEdit_table in self.table_lineEdits.values():
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
        return super().closeEvent(a0)
    
    #TODO: remove soon
    def update_formulation_callback(self, **kwargs):
        return

        surface_id = kwargs.get("surface_id", None)
        line_id = kwargs.get("line_id", None)
        point_id = kwargs.get("point_id", None)
        node_id = kwargs.get("node_id", None)

        if isinstance(surface_id, int):
            data = self.properties._get_property("surface_thickness", surface=surface_id)
            if isinstance(data, dict):
                self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
                return
            
        if isinstance(line_id, int):
            for node_id in self.mesh.get_nodes_from_line(line_id):
                for surface_id in self.mesh.get_surfaces_from_node(node_id):
                    data = self.properties._get_property("surface_thickness", surface=surface_id)
                    if isinstance(data, dict):
                        self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
                        return

        if isinstance(point_id, int):
            node_id = self.mesh.nodes_from_points.get(point_id)
            if node_id is None:
                return

            for surface_id in self.mesh.get_surfaces_from_node(node_id):
                data = self.properties._get_property("surface_thickness", surface=surface_id)
                if isinstance(data, dict):
                    self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
                    return

        if isinstance(node_id, int):
            for surface_id in self.mesh.get_surfaces_from_node(node_id):
                data = self.properties._get_property("surface_thickness", surface=surface_id)
                if isinstance(data, dict):
                    self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
                    return
