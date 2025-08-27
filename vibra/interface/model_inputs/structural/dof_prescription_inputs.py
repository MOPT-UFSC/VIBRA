
from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.ui_generated.model.setup.structural.dof_prescription_inputs_ui import DofPrescriptionInputs_UI
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.model_inputs.data_filter.change_frequency_data_handler import ChangeFrequencyDataRangeInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.utils import are_there_values_different_from_zero

import numpy as np
from enum import IntEnum
from os.path import basename
from collections import defaultdict


error_title = "Error"
warning_title = "Warning"


class ElementFormulation(IntEnum):
    ELEMENT_2D = 0
    ELEMENT_3D = 1


class DofPrescriptionInputs(DofPrescriptionInputs_UI):
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
        self._create_line_edits()
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

    def reset_table_variables(self):

        self.ux_table_values = None
        self.uy_table_values = None
        self.uz_table_values = None
        self.rx_table_values = None
        self.ry_table_values = None
        self.rz_table_values = None

        self.ux_array = None
        self.uy_array = None
        self.uz_array = None
        self.rx_array = None
        self.ry_array = None
        self.rz_array = None

        self.ux_table_path = None
        self.uy_table_path = None
        self.uz_table_path = None
        self.rx_table_path = None
        self.ry_table_path = None
        self.rz_table_path = None

        self.ux_table_name = None
        self.uy_table_name = None
        self.uz_table_name = None
        self.rx_table_name = None
        self.ry_table_name = None
        self.rz_table_name = None

    def _create_line_edits(self):

        self.constante_line_edits = [  
                                    [self.lineEdit_real_ux, self.lineEdit_imag_ux],
                                    [self.lineEdit_real_uy, self.lineEdit_imag_uy],
                                    [self.lineEdit_real_uz, self.lineEdit_imag_uz],
                                    [self.lineEdit_real_rx, self.lineEdit_imag_rx],
                                    [self.lineEdit_real_ry, self.lineEdit_imag_ry],
                                    [self.lineEdit_real_rz, self.lineEdit_imag_rz],
                                    ]

        self.table_line_edits = { 
                                "Ux" : self.lineEdit_path_table_ux,
                                "Uy" : self.lineEdit_path_table_uy,
                                "Uz" : self.lineEdit_path_table_uz,
                                "Rx" : self.lineEdit_path_table_rx,
                                "Ry" : self.lineEdit_path_table_ry,
                                "Rz" : self.lineEdit_path_table_rz,
                                }

    def _config_widgets(self):
        #
        self.comboBox_element_type.setEnabled(False)
        #
        for i, w in enumerate([110, 150, 100]):
            self.treeWidget_prescribed_dofs.setColumnWidth(i, w)
            self.treeWidget_prescribed_dofs.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_callback)
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_load_ux_table.clicked.connect(self.load_ux_table)
        self.pushButton_load_uy_table.clicked.connect(self.load_uy_table)
        self.pushButton_load_uz_table.clicked.connect(self.load_uz_table)
        self.pushButton_load_rx_table.clicked.connect(self.load_rx_table)
        self.pushButton_load_ry_table.clicked.connect(self.load_ry_table)
        self.pushButton_load_rz_table.clicked.connect(self.load_rz_table)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_prescribed_dofs.itemClicked.connect(self.on_click_item)
        self.treeWidget_prescribed_dofs.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.geometry_selection_callback()
        self.update_element_type_based_on_geometry_information()

    def geometry_selection_callback(self):

        faces = app().main_window.selected_geometry_surfaces
        lines = app().main_window.selected_geometry_lines
        points = app().main_window.selected_geometry_points
        nodes = app().main_window.selected_mesh_nodes

        if faces:

            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(0)

            if len(faces) == 1:
                surface_id = list(faces)[0]
                data = self.properties._get_property("prescribed_dofs", surface=surface_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(surface_id=surface_id)

        elif lines:

            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(1)

            if len(lines) == 1:
                line_id = list(lines)[0]
                data = self.properties._get_property("prescribed_dofs", line=line_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(line_id=line_id)

        elif points:
            
            text = ", ".join([str(i) for i in points])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(2)

            if len(points) == 1:
                point_id = list(points)[0]
                data = self.properties._get_property("prescribed_dofs", point=point_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(point_id=point_id)

        elif nodes:
            
            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(3)

            if len(nodes) == 1:
                node_id = list(nodes)[0]
                data = self.properties._get_property("prescribed_dofs", node=node_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(node_id=node_id)

    def update_input_fields(self, data: dict | None):

        if data is None:
            return
        
        values = data.get("values", list())
        if not are_there_values_different_from_zero(values):
            return

        self.reset_input_fields()

        element_type = data.get("element_type", None)
        if element_type == "2d_element":
            self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
        else:
            self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_3D)

        if "table_paths" in data.keys():
            table_paths = data["table_paths"]
            for index, lineEdit_table in enumerate(self.table_line_edits.values()):
                if data["element_type"] == "3d_element" and index >= 3:
                    continue

                table_path = table_paths[index]
                if table_path is not None:                   
                    lineEdit_table.setText(table_path)

        else:
            for index, [lineEdit_real, lineEdit_imag] in enumerate(self.constante_line_edits):
                if data["element_type"] == "3d_element" and index >= 3:
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

        self.label_Rx_constant.setVisible(element_2d)
        self.label_Ry_constant.setVisible(element_2d)
        self.label_Rz_constant.setVisible(element_2d)

        self.label_Rx_unit.setVisible(element_2d)
        self.label_Ry_unit.setVisible(element_2d)
        self.label_Rz_unit.setVisible(element_2d)

        self.label_angular.setVisible(element_2d)
        self.label_Rx_table.setVisible(element_2d)
        self.label_Ry_table.setVisible(element_2d)
        self.label_Rz_table.setVisible(element_2d)

        self.lineEdit_real_rx.setVisible(element_2d)
        self.lineEdit_real_ry.setVisible(element_2d)
        self.lineEdit_real_rz.setVisible(element_2d)

        self.lineEdit_imag_rx.setVisible(element_2d)
        self.lineEdit_imag_ry.setVisible(element_2d)
        self.lineEdit_imag_rz.setVisible(element_2d)

        self.pushButton_load_rx_table.setVisible(element_2d)
        self.pushButton_load_ry_table.setVisible(element_2d)
        self.pushButton_load_rz_table.setVisible(element_2d)

        self.lineEdit_path_table_rx.setVisible(element_2d)
        self.lineEdit_path_table_ry.setVisible(element_2d)
        self.lineEdit_path_table_rz.setVisible(element_2d)

        self.comboBox_angular_data_type.setVisible(element_2d)

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

        return False, values

    def constant_values_attribution(self):

        input_ids = self.lineEdit_selection_id.text()
        attribution_type = self.comboBox_attribution_type.currentIndex()

        if attribution_type == 0:
            selection = "surfaces"

        elif attribution_type == 1:
            selection = "lines"

        elif attribution_type == 2:
            selection = "points"

        else:
            selection = "nodes"

        selected_ids, error_data = self.mesh.check_selected_ids(
                                                                input_ids, 
                                                                selection = selection, 
                                                                single_id = False
                                                                )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return
        
        self.remove_duplicated_attributions(selected_ids, selection)
        self.remove_conflicting_excitations(selected_ids, selection)

        etype_index = self.comboBox_element_type.currentIndex()
        element_type = self.element_types[etype_index]

        stop, ux = self.check_complex_entries(self.lineEdit_real_ux.text(), self.lineEdit_imag_ux.text(), "ux")
        if stop:
            return

        stop, uy = self.check_complex_entries(self.lineEdit_real_uy.text(), self.lineEdit_imag_uy.text(), "uy")
        if stop:
            return

        stop, uz = self.check_complex_entries(self.lineEdit_real_uz.text(), self.lineEdit_imag_uz.text(), "uz")
        if stop:
            return

        prescribed_dofs = [ux, uy, uz]

        if element_type == "2d_element":

            stop, rx = self.check_complex_entries(self.lineEdit_real_rx.text(), self.lineEdit_imag_rx.text(), "rx")
            if stop:
                return

            stop, ry = self.check_complex_entries(self.lineEdit_real_ry.text(), self.lineEdit_imag_ry.text(), "ry")
            if stop:
                return

            stop, rz = self.check_complex_entries(self.lineEdit_real_rz.text(), self.lineEdit_imag_rz.text(), "rz")
            if stop:
                return

            prescribed_dofs.extend([rx, ry, rz])

        condition_1 = element_type == "2d_element" and prescribed_dofs.count(None) == 6
        condition_2 = element_type == "3d_element" and prescribed_dofs.count(None) == 3

        if condition_1 or condition_2:
            self.hide()
            title = "Additional inputs required"
            message = "It is necessary to enter at least one non-zero prescribed "
            message += "dof before confirming the property assignment."
            PrintMessageInput([error_title, title, message])
            return

        real_values = [value if value is None else np.real(value) for value in prescribed_dofs]
        imag_values = [value if value is None else np.imag(value) for value in prescribed_dofs]

        for selected_id in selected_ids:

            data = {
                    "element_type" : element_type,
                    "values" : prescribed_dofs,
                    "real_values" : real_values,
                    "imag_values" : imag_values
                    }

            if attribution_type == 0:
                self.model.properties._set_property("prescribed_dofs", data, surface=selected_id)

            elif attribution_type == 1:
                self.model.properties._set_property("prescribed_dofs", data, line=selected_id)

            elif attribution_type == 2:
                self.model.properties._set_property("prescribed_dofs", data, point=selected_id)

            elif attribution_type == 3:
                self.model.properties._set_property("prescribed_dofs", data, node=selected_id)

        self.actions_to_finalize()

    def load_table(self, lineEdit : QLineEdit, dof_label : str, direct_load = False):

        title = "Error while loading table"
        imported_file = None

        try:
            if direct_load:
                if lineEdit.text() == "":
                    return None, None

                imported_table_path = lineEdit.text()
                imported_file = DataImporter.read_data_in_file(imported_table_path).data
            else:
                imported_data = DataImporter.import_single_file("imported_table_folder",
                    ["csv", "dat", "txt", "xlsx", "xls"], f"Choose a table to import the {dof_label} data")
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

    def load_ux_table(self):
        self.ux_table_values, self.ux_table_path = self.load_table(self.lineEdit_path_table_ux, "Ux")
        if  self.ux_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_ux)

    def load_uy_table(self):
        self.uy_table_values, self.uy_table_path = self.load_table(self.lineEdit_path_table_uy, "Uy")
        if self.uy_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_uy)
            
    def load_uz_table(self):
        self.uz_table_values, self.uz_table_path = self.load_table(self.lineEdit_path_table_uz, "Uz")
        if self.uz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_uz)
            
    def load_rx_table(self):
        self.rx_table_values, self.rx_table_path = self.load_table(self.lineEdit_path_table_rx, "Rx")
        if self.rx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_rx)
            
    def load_ry_table(self):
        self.ry_table_values, self.ry_table_path = self.load_table(self.lineEdit_path_table_ry, "Ry")
        if self.ry_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_ry)
            
    def load_rz_table(self):
        self.rz_table_values, self.rz_table_path = self.load_table(self.lineEdit_path_table_rz, "Rz")
        if self.rz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_rz)

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

    def integrate_and_save_table_files(self, dof_label: str, selected_id: int, selection: str, values: np.ndarray, linear=False, angular=False):

        if self.frequencies[0] == 0:
            self.frequencies[0] = float(1e-6)

        if linear:
            index_lin = self.comboBox_linear_data_type.currentIndex()
            values /= ((1j*2*np.pi*self.frequencies)**index_lin)

        if angular:
            index_ang = self.comboBox_angular_data_type.currentIndex()
            values /= ((1j*2*np.pi*self.frequencies)**index_ang)

        if self.frequencies[0] == float(1e-6):
            self.frequencies[0] = 0

        if app().project.model.change_analysis_frequency_setup(list(self.frequencies)):

            self.hide()
            lineEdit = self.table_line_edits.get(dof_label)
            imported_filename = basename(lineEdit.text())
            self.lineEdit_reset(lineEdit)

            title = "Project frequency setup cannot be modified"
            message = f"The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\nFile name: {imported_filename}"
            PrintMessageInput([error_title, title, message])

            return None, None

        table_name = f"prescribed_dof_{dof_label}_from_{selection[:-1]}_{selected_id}"

        real_values = np.real(values)
        imag_values = np.imag(values)
        data = np.array([self.frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("structural", table_name, data)
        self.update_analysis_setup_in_file(self.frequencies)

        return table_name, data

    def table_values_attribution(self):

        input_ids = self.lineEdit_selection_id.text()
        attribution_type = self.comboBox_attribution_type.currentIndex()

        if attribution_type == 0:
            selection = "surfaces"

        elif attribution_type == 1:
            selection = "lines"

        elif attribution_type == 2:
            selection = "points"

        else:
            selection = "nodes"

        selected_ids, error_data = self.mesh.check_selected_ids(
                                                                input_ids, 
                                                                selection = selection, 
                                                                single_id = False
                                                                )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        self.remove_duplicated_attributions(selected_ids, selection)
        self.remove_conflicting_excitations(selected_ids, selection)

        element_type_index = self.comboBox_element_type.currentIndex()
        if element_type_index == 0:
            element_type = "2d_element"
        else:
            element_type = "3d_element"

        if self.ux_table_path is None:
            self.ux_table_values, self.ux_table_path = self.load_table(self.lineEdit_path_table_ux, "Ux", direct_load = True)

        if self.uy_table_path is None:
            self.uy_table_values, self.uy_table_path = self.load_table(self.lineEdit_path_table_uy, "Uy", direct_load = True)

        if self.uz_table_path is None:
            self.uz_table_values, self.uz_table_path = self.load_table(self.lineEdit_path_table_uz, "Uz", direct_load = True)

        if self.rx_table_path is None:
            self.rx_table_values, self.rx_table_path = self.load_table(self.lineEdit_path_table_rx, "Rx", direct_load = True)

        if self.ry_table_path is None:
            self.ry_table_values, self.ry_table_path = self.load_table(self.lineEdit_path_table_ry, "Ry", direct_load = True)

        if self.rz_table_path is None:
            self.rz_table_values, self.rz_table_path = self.load_table(self.lineEdit_path_table_rz, "Rz", direct_load = True)

        for selected_id in selected_ids:
            
            if self.ux_table_values is not None:
                self.ux_table_name, self.ux_array = self.integrate_and_save_table_files("Ux", selected_id, selection, self.ux_table_values, linear = True)

            if self.uy_table_values is not None:
                self.uy_table_name, self.uy_array = self.integrate_and_save_table_files("Uy", selected_id, selection, self.uy_table_values, linear = True)

            if self.uz_table_values is not None:
                self.uz_table_name, self.uz_array = self.integrate_and_save_table_files("Uz", selected_id, selection, self.uz_table_values, linear = True)

            table_names = [self.ux_table_name, self.uy_table_name, self.uz_table_name]
            table_paths = [self.ux_table_path, self.uy_table_path, self.uz_table_path]
            prescribed_dofs = [self.ux_table_values, self.uy_table_values, self.uz_table_values]

            if element_type_index == 0:

                if self.rx_table_values is not None:
                    self.rx_table_name, self.rx_array = self.integrate_and_save_table_files("Rx", selected_id, selection, self.rx_table_values, angular = True)

                if self.ry_table_values is not None:
                    self.ry_table_name, self.rx_array = self.integrate_and_save_table_files("Ry", selected_id, selection, self.ry_table_values, angular = True)

                if self.rz_table_values is not None:
                    self.rz_table_name, self.rx_array = self.integrate_and_save_table_files("Rz", selected_id, selection, self.rz_table_values, angular = True)

                table_names.extend([self.rx_table_name, self.ry_table_name, self.rz_table_name])
                table_paths.extend([self.rx_table_path, self.ry_table_path, self.rz_table_path])
                prescribed_dofs.extend([self.rx_table_values, self.ry_table_values, self.rz_table_values])

            condition_1 = element_type_index == 0 and table_names.count(None) == 6
            condition_2 = element_type_index == 1 and table_names.count(None) == 3

            if condition_1 or condition_2:
                self.hide()
                title = "Additional inputs required"
                message = "It is necessary to enter at least one prescribed dof "
                message += "before confirming the property assignment."
                PrintMessageInput([error_title, title, message]) 
                return 

            data = {
                    "element_type" : element_type,
                    "table_names" : table_names,
                    "table_paths" : table_paths,
                    "values" : prescribed_dofs
                    }

            if attribution_type == 0:
                self.model.properties._set_property("prescribed_dofs", data, surface=selected_id)

            elif attribution_type == 1:
                self.model.properties._set_property("prescribed_dofs", data, line=selected_id)

            elif attribution_type == 2:
                self.model.properties._set_property("prescribed_dofs", data, point=selected_id)

            elif attribution_type == 3:
                self.model.properties._set_property("prescribed_dofs", data, node=selected_id)

        self.reset_table_variables()
        self.actions_to_finalize()

    def remove_duplicated_attributions(self, selected_ids: list, selection: str):

        table_names = list()
        nodes_to_remove = list()
        for selected_id in selected_ids:

            if selection == "surfaces":

                nodes_from_surface = self.mesh.nodes_from_surfaces[selected_id]
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "prescribed_dofs" and node_id in nodes_from_surface:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for line_id in self.mesh.lines_from_surface[selected_id]:
                    data = self.properties._get_property("prescribed_dofs", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("prescribed_dofs", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", line_id, "lines"))

                    for point_id in self.mesh.points_from_line[line_id]:
                        data = self.properties._get_property("prescribed_dofs", point=point_id)
                        if isinstance(data, dict):
                            self.properties._remove_point_property("prescribed_dofs", point_id)
                            table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", point_id, "points"))

            elif selection == "lines":

                nodes_from_line = self.mesh.nodes_from_lines[selected_id]
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "prescribed_dofs" and node_id in nodes_from_line:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for surface_id in self.mesh.surfaces_from_line[selected_id]:
                    data = self.properties._get_property("prescribed_dofs", surface=surface_id)
                    if isinstance(data, dict):
                        self.properties._remove_surface_property("prescribed_dofs", surface_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", surface_id, "surfaces"))

                for point_id in self.mesh.points_from_line[selected_id]:
                    data = self.properties._get_property("prescribed_dofs", point=point_id)
                    if isinstance(data, dict):
                        self.properties._remove_point_property("prescribed_dofs", point_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", point_id, "points"))

            elif selection == "points":

                nodes_from_point = self.mesh.nodes_from_points[selected_id]
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "prescribed_dofs" and node_id in nodes_from_point:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for line_id in self.mesh.lines_from_point[selected_id]:
                    data = self.properties._get_property("prescribed_dofs", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("prescribed_dofs", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", line_id, "lines"))

                    for surface_id in self.mesh.surfaces_from_line[line_id]:
                        data = self.properties._get_property("prescribed_dofs", surface=surface_id)
                        if isinstance(data, dict):
                            self.properties._remove_surface_property("prescribed_dofs", surface_id)
                            table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", surface_id, "surfaces"))

            elif selection == "nodes":

                point_id = selected_id + 1
                data = self.properties._get_property("prescribed_dofs", point=point_id)
                if isinstance(data, dict):
                    self.properties._remove_point_property("prescribed_dofs", point_id)
                    table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", point_id, "points"))

                for line_id in self.mesh.lines_from_point[point_id]:
                    data = self.properties._get_property("prescribed_dofs", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("prescribed_dofs", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", line_id, "lines"))

                    for surface_id in self.mesh.surfaces_from_line[line_id]:
                        data = self.properties._get_property("prescribed_dofs", surface=surface_id)
                        if isinstance(data, dict):
                            self.properties._remove_surface_property("prescribed_dofs", surface_id)
                            table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", surface_id, "surfaces"))

            for node_id in nodes_to_remove:
                self.properties._remove_nodal_property("prescribed_dofs", node_id)
                table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", node_id, "nodes"))

            self.process_table_file_removal(table_names)

    def attribute_callback(self):
        index = self.tabWidget_main.currentIndex()
        if index == 0:
            self.constant_values_attribution()
        elif index == 1:
            self.table_values_attribution()

    def text_label(self, mask):

        if len(mask) == 6:
            dofs_labels = np.array(['Ux','Uy','Uz','Rx','Ry','Rz'])

        elif len(mask) == 3:
            dofs_labels = np.array(['Ux','Uy','Uz'])

        labels = dofs_labels[mask]

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
            if property != "prescribed_dofs":
                continue

            values = data["values"]
            if not are_there_values_different_from_zero(values):
                continue

            element_type = data["element_type"]
            constrained_dofs_mask = [False if value is None else True for value in values]
            dofs_labels = str(self.text_label(constrained_dofs_mask))

            new = QTreeWidgetItem([f"{entity.capitalize()}-{args[0]}", dofs_labels, element_type])
            for i in range(3):
                new.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_prescribed_dofs.addTopLevelItem(new)

    def load_model_info(self):

        self.treeWidget_prescribed_dofs.clear()

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
            for (property, _), data in current_property.items():
                if property == "prescribed_dofs":
                    values = data["values"]
                    if not are_there_values_different_from_zero(values):
                        continue

                    self.tabWidget_main.setTabVisible(2, True)
                    return

        self.lineEdit_real_ux.setFocus()
        self.tabWidget_main.setCurrentIndex(0)

        self.tabWidget_main.setTabVisible(2, False)
        app().main_window.set_geometry_selection()

    def tab_event_callback(self):

        list_tab = self.tabWidget_main.currentIndex() == 2
        self.lineEdit_selection_id.setDisabled(list_tab)
        self.pushButton_attribute.setDisabled(list_tab)
        self.pushButton_attribute.setDisabled(list_tab)

        if list_tab:
            self.lineEdit_selection_id.setText("")
            return

        else:
            text = self.lineEdit_selection_id.text()
            if "-" in text:
                selected_id = text.split("-")[1]
                self.lineEdit_selection_id.setText(selected_id)

    def on_click_item(self, item):

        self.pushButton_remove.setDisabled(False)

        if item.text(0) != "":

            selection, _selected_id = item.text(0).split("-")
            selected_id = int(_selected_id)

            if selection == "Surface":
                app().main_window.set_geometry_selection(surfaces = [int(selected_id)])

            elif selection == "Line":
                app().main_window.set_geometry_selection(lines = [int(selected_id)])

            elif selection == "Point":
                app().main_window.set_geometry_selection(points = [int(selected_id)])

            elif selection == "Node":
                app().main_window.set_mesh_selection(nodes=[int(selected_id)])

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

        app().file.write_imported_table_data_in_file()

    def remove_conflicting_excitations(self, selected_ids: int | list, selection: str):

        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        if selection == "surfaces":
            remove_function = self.properties._remove_surface_property

        elif selection == "lines":
            remove_function = self.properties._remove_line_property

        elif selection == "points":
            remove_function = self.properties._remove_point_property

        elif selection == "nodes":
            remove_function = self.properties._remove_nodal_property

        properties = ["nodal_loads", "prescribed_dofs"]

        for selected_id in selected_ids:
            for property in properties:
                table_names = self.properties.get_property_related_table_names(property, selected_id, selection)
                remove_function(property, selected_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from(self, selected_id : list, selection: str):
        table_names = self.properties.get_property_related_table_names("prescribed_dofs", selected_id, selection)
        self.process_table_file_removal(table_names)

    def remove_callback(self):

        text = self.lineEdit_selection_id.text()

        if "-" in text:

            selection, _selected_id = text.split("-")
            selected_id = int(_selected_id)

            if selection == "Surface":
                self.properties._remove_surface_property("prescribed_dofs", selected_id)

            elif selection == "Line":
                self.properties._remove_line_property("prescribed_dofs", selected_id)

            elif selection == "Point":
                self.properties._remove_point_property("prescribed_dofs", selected_id)

            elif selection == "Node":
                self.properties._remove_nodal_property("prescribed_dofs", selected_id)

            else:
                return

            self.remove_table_files_from(selected_id, f"{selection.lower()}s")
            self.actions_to_finalize()

            app().main_window.set_geometry_selection()
            app().main_window.set_mesh_selection()

    def reset_callback(self):

        self.hide()

        title = "DOF prescription reset"
        message = "Would you like to remove the all prescribed DOF from model?"

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

            for entity_label, _property in properties.items():
                for (property_label, *args), data in _property.items():
                    if property_label != "prescribed_dofs":
                        continue
    
                    if not are_there_values_different_from_zero(data.get("values")):
                        continue
    
                    entities_to_remove[entity_label].append(args[0])

            for entity, selected_ids in entities_to_remove.items():
                for selected_id in selected_ids:
                    if entity == "surfaces":
                        self.properties._remove_surface_property("prescribed_dofs", selected_id)
                    elif entity == "lines":
                        self.properties._remove_line_property("prescribed_dofs", selected_id)
                    elif entity == "points":
                        self.properties._remove_point_property("prescribed_dofs", selected_id)
                    elif entity == "nodes":
                        self.properties._remove_nodal_property("prescribed_dofs", selected_id)

            self.actions_to_finalize()

            app().main_window.set_geometry_selection()
            app().main_window.set_mesh_selection()

    def actions_to_finalize(self):
        self.load_model_info()
        self.reset_input_fields(reset_all=True)
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
            if property in ["nodal_loads", "prescribed_dofs"]:
                if "table_names" in data.keys():
                    return

        if isinstance(self.project.analysis_setup, dict):
            analysis_setup = self.project.analysis_setup
            self.project.set_analysis_setup(analysis_setup)
            app().file.write_analysis_setup_in_file(analysis_setup)

    def reset_input_fields(self, reset_all=False):

        if reset_all:
            self.lineEdit_selection_id.setText("")

        for lineEdit_real, lineEdit_imag in self.constante_line_edits:
            lineEdit_real.setText("")
            lineEdit_imag.setText("")

        for lineEdit_table in self.table_line_edits.values():
            lineEdit_table.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)

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
            for node_id in self.mesh.nodes_from_lines[line_id]:
                for surface_id in self.mesh.surfaces_from_node[node_id]:
                    data = self.properties._get_property("surface_thickness", surface=surface_id)
                    if isinstance(data, dict):
                        self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
                        return

        if isinstance(point_id, int):
            node_id = self.mesh.nodes_from_points.get(point_id)
            if node_id is None:
                return

            for surface_id in self.mesh.surfaces_from_node[node_id]:
                data = self.properties._get_property("surface_thickness", surface=surface_id)
                if isinstance(data, dict):
                    self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
                    return

        if isinstance(node_id, int):
            for surface_id in self.mesh.surfaces_from_node[node_id]:
                data = self.properties._get_property("surface_thickness", surface=surface_id)
                if isinstance(data, dict):
                    self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
                    return