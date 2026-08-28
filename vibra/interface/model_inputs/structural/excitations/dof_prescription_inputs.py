
from collections import defaultdict
from enum import IntEnum
from os.path import basename
from pathlib import Path

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLabel, QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.engine.analysis_info import AnalysisID
from vibra.extensions import SUPPORTED_SPREADSHEET_EXTENSIONS, SUPPORTED_TEXT_EXTENSIONS
from vibra.interface import error_title
from vibra.interface.common.common_interface import save_table_values, update_analysis_setup_in_file
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.structural.definitions.enums import StandardTabType

# from vibra.utils.utils import are_there_values_different_from_zero
from vibra.interface.ui_generated.model.structural.excitations.dof_prescription_inputs_ui import DofPrescriptionInputs_UI
from vibra.interface.user_input.data_handler.file_dialog_service import FileDialogService
from vibra.interface.user_input.data_handler.file_handlers.file_handler import FileHandler


class ElementFormulation(IntEnum):
    ELEMENT_2D = 0
    ELEMENT_3D = 1


class DOFSetup(IntEnum):
    VALUE = 0
    FREE = 1
    FIXED = 2


class AssignmetType(IntEnum):
    SURFACES = 0
    LINES = 1
    POINTS = 2
    NODES = 3


class DataType(IntEnum):
    DISPLACEMENT = 0
    VELOCITY = 1
    ACCELERATION = 2


class DofPrescriptionInputs(DofPrescriptionInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self._config_window()
        self._config_widgets()
        self._initialize()
        self._create_connections()
        self.load_model_info()

        while self.keep_window_open:
            self.exec()

    @property
    def model(self):
        return app().project.model

    @property
    def mesh(self):
        return app().project.model.mesh

    @property
    def properties(self):
        return app().project.model.properties

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

        self.ux_table_values = None
        self.uy_table_values = None
        self.uz_table_values = None
        self.rx_table_values = None
        self.ry_table_values = None
        self.rz_table_values = None

        self.ux_table_path = None
        self.uy_table_path = None
        self.uz_table_path = None
        self.rx_table_path = None
        self.ry_table_path = None
        self.rz_table_path = None

    def _create_line_edits(self):

        self.constant_line_edits = {
            "Ux": [self.lineEdit_real_ux, self.lineEdit_imag_ux],
            "Uy": [self.lineEdit_real_uy, self.lineEdit_imag_uy],
            "Uz": [self.lineEdit_real_uz, self.lineEdit_imag_uz],
            "Rx": [self.lineEdit_real_rx, self.lineEdit_imag_rx],
            "Ry": [self.lineEdit_real_ry, self.lineEdit_imag_ry],
            "Rz": [self.lineEdit_real_rz, self.lineEdit_imag_rz],
        }

        self.table_line_edits = {
            "Ux": self.lineEdit_path_table_ux,
            "Uy": self.lineEdit_path_table_uy,
            "Uz": self.lineEdit_path_table_uz,
            "Rx": self.lineEdit_path_table_rx,
            "Ry": self.lineEdit_path_table_ry,
            "Rz": self.lineEdit_path_table_rz,
        }

        self.dof_setup_combo_boxes = {
            "Ux": self.comboBox_displacement_ux,
            "Uy": self.comboBox_displacement_uy,
            "Uz": self.comboBox_displacement_uz,
            "Rx": self.comboBox_rotation_rx,
            "Ry": self.comboBox_rotation_ry,
            "Rz": self.comboBox_rotation_rz,
        }

    def _config_widgets(self):
        #
        self.comboBox_element_type.setEnabled(False)
        #
        for i, w in enumerate([110, 150, 100]):
            self.treeWidget_prescribed_dof.setColumnWidth(i, w)
            self.treeWidget_prescribed_dof.headerItem().setTextAlignment(i, Qt.AlignCenter)
        #
        self._create_line_edits()
        #
        for line_edit in self.table_line_edits.values():
            font = line_edit.font()
            font.setPointSize(8)
            line_edit.setFont(font)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_data_type.currentIndexChanged.connect(self.update_combo_box_units_callback)
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_callback)
        self.comboBox_displacement_ux.currentIndexChanged.connect(self.displacement_ux_callback)
        self.comboBox_displacement_uy.currentIndexChanged.connect(self.displacement_uy_callback)
        self.comboBox_displacement_uz.currentIndexChanged.connect(self.displacement_uz_callback)
        self.comboBox_rotation_rx.currentIndexChanged.connect(self.rotation_rx_callback)
        self.comboBox_rotation_ry.currentIndexChanged.connect(self.rotation_ry_callback)
        self.comboBox_rotation_rz.currentIndexChanged.connect(self.rotation_rz_callback)
        #
        self.pushButton_all_dof_fixed.clicked.connect(self.set_all_dof_fixed_callback)
        self.pushButton_all_dof_free.clicked.connect(self.set_all_dof_free_callback)
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_load_ux_table.clicked.connect(self.load_ux_table)
        self.pushButton_load_uy_table.clicked.connect(self.load_uy_table)
        self.pushButton_load_uz_table.clicked.connect(self.load_uz_table)
        self.pushButton_load_rx_table.clicked.connect(self.load_rx_table)
        self.pushButton_load_ry_table.clicked.connect(self.load_ry_table)
        self.pushButton_load_rz_table.clicked.connect(self.load_rz_table)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_prescribed_dof.itemClicked.connect(self.on_click_item)
        self.treeWidget_prescribed_dof.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.update_element_type_based_on_geometry_information()
        self.set_all_dof_free_callback()
        self.update_combo_box_units_callback()
        self.geometry_selection_callback()

    def update_combo_box_units_callback(self):

        suffixes = ["", "/s", "/s²"]
        directions = ["x", "y", "z", "x", "y", "z"]
        data_types = ["{}<sub>{}</sub>:", "d{}<sub>{}</sub> / dt:", "d²{}<sub>{}</sub> / dt²:"]

        index = self.comboBox_data_type.currentIndex()
        unit_den = suffixes[index]
        label_width = int(40 + 10 * index)

        for i, (key, combo_box) in enumerate(self.dof_setup_combo_boxes.items()):
            unit_num = "m" if i < 3 else "rad"
            combo_box.blockSignals(True)
            combo_box.setItemText(0, f"Value ({unit_num}{unit_den})")
            combo_box.blockSignals(False)

            label_unit_constant: QLabel = self.__getattribute__(f"label_{key}_constant")
            label_unit_table: QLabel = self.__getattribute__(f"label_{key}_table")

            dof_type = "u" if i < 3 else "\u03b8"
            label_text = data_types[index].format(dof_type, directions[i])

            label_unit_constant.setText(label_text)
            label_unit_constant.setFixedWidth(label_width)

            label_unit_table.setText(label_text)
            label_unit_table.setFixedWidth(label_width)

    def attribution_type_callback(self):
        if self.comboBox_attribution_type.currentIndex() == 3:
            app().main_window.action_mesh_workspace_callback()
        else:
            app().main_window.action_model_workspace_callback()

    def element_type_callback(self):

        element_2d = self.comboBox_element_type.currentIndex() == ElementFormulation.ELEMENT_2D

        self.comboBox_rotation_rx.setVisible(element_2d)
        self.comboBox_rotation_ry.setVisible(element_2d)
        self.comboBox_rotation_rz.setVisible(element_2d)

        self.label_Rx_constant.setVisible(element_2d)
        self.label_Ry_constant.setVisible(element_2d)
        self.label_Rz_constant.setVisible(element_2d)

        # self.label_Rx_unit.setVisible(element_2d)
        # self.label_Ry_unit.setVisible(element_2d)
        # self.label_Rz_unit.setVisible(element_2d)
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

    def combo_box_callback(self, unit_label: str):

        combo_box = self.dof_setup_combo_boxes[unit_label]
        value_based = combo_box.currentIndex() == DOFSetup.VALUE

        line_edit_real, line_edit_imag = self.constant_line_edits.get(unit_label, (None, None))
        if (line_edit_real, line_edit_imag).count(None) == 2:
            return

        line_edit_real.setText("")
        line_edit_imag.setText("")
        line_edit_real.setEnabled(value_based)   
        line_edit_imag.setEnabled(value_based)

        if value_based:
            return

        if combo_box.currentIndex() == DOFSetup.FIXED:
            line_edit_real.setText("fixed")
            line_edit_imag.setText("fixed")

        elif combo_box.currentIndex() == DOFSetup.FREE:
            line_edit_real.setText("free")
            line_edit_imag.setText("free")

    def displacement_ux_callback(self):
        self.combo_box_callback("Ux")

    def displacement_uy_callback(self):
        self.combo_box_callback("Uy")

    def displacement_uz_callback(self):
        self.combo_box_callback("Uz")

    def rotation_rx_callback(self):
        self.combo_box_callback("Rx")

    def rotation_ry_callback(self):
        self.combo_box_callback("Ry")

    def rotation_rz_callback(self):
        self.combo_box_callback("Rz")

    def set_all_dof_fixed_callback(self):
        self.set_index_for_all_dof_combo_boxes(DOFSetup.FIXED)

    def set_all_dof_free_callback(self):
        self.set_index_for_all_dof_combo_boxes(DOFSetup.FREE)
        # reset the constant values lineEdits
        for lineEdit_real, lineEdit_imag in self.constant_line_edits.values():
            lineEdit_real.setText("free")
            lineEdit_imag.setText("free")

    def set_index_for_all_dof_combo_boxes(self, index: int):

        self.comboBox_displacement_ux.setCurrentIndex(index)
        self.comboBox_displacement_uy.setCurrentIndex(index)
        self.comboBox_displacement_uz.setCurrentIndex(index)

        if self.comboBox_element_type.currentIndex() == ElementFormulation.ELEMENT_2D:
            self.comboBox_rotation_rx.setCurrentIndex(index)
            self.comboBox_rotation_ry.setCurrentIndex(index)
            self.comboBox_rotation_rz.setCurrentIndex(index)

    def geometry_selection_callback(self):

        surfaces = app().main_window.selection.geometry_surfaces
        lines = app().main_window.selection.geometry_lines
        points = app().main_window.selection.geometry_points
        nodes = app().main_window.selection.mesh_nodes

        if surfaces:

            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(0)

            if len(surfaces) == 1:
                surface_id = list(surfaces)[0]
                data = self.properties._get_property("prescribed_dof", surface=surface_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(surface_id=surface_id)

        elif lines:

            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(1)

            if len(lines) == 1:
                line_id = list(lines)[0]
                data = self.properties._get_property("prescribed_dof", line=line_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(line_id=line_id)

        elif points:
            
            text = ", ".join([str(i) for i in points])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(2)

            if len(points) == 1:
                point_id = list(points)[0]
                data = self.properties._get_property("prescribed_dof", point=point_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(point_id=point_id)

        elif nodes:
            
            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(3)

            if len(nodes) == 1:
                node_id = list(nodes)[0]
                data = self.properties._get_property("prescribed_dof", node=node_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(node_id=node_id)

    def update_input_fields(self, data: dict | None):

        if data is None:
            return

        if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
            return

        self.reset_input_fields()

        element_type = data.get("element_type", None)
        if element_type == "2d_element":
            self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
        else:
            self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_3D)

        self.comboBox_data_type.setCurrentIndex(data.get("integrate", 0))

        if "table_paths" in data.keys():
    
            self.tabWidget_main.setCurrentIndex(StandardTabType.TABULAR_DATA)
            table_paths = data["table_paths"]
            for index, lineEdit_table in enumerate(self.table_line_edits.values()):
                if element_type == "3d_element" and index >= 3:
                    continue

                table_path = table_paths[index]
                if table_path is not None:                   
                    lineEdit_table.setText(table_path)
                    lineEdit_table.setToolTip(table_path)

        else:

            values = data.get("values", list())
            self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)

            for index, (unit_label, (lineEdit_real, lineEdit_imag)) in enumerate(self.constant_line_edits.items()):
    
                if element_type == "3d_element" and index >= 3:
                    continue

                if values[index] is None:
                    self.dof_setup_combo_boxes[unit_label].setCurrentIndex(DOFSetup.FREE)

                elif isinstance(values[index], complex):
                    if values[index] == complex(0):
                        self.dof_setup_combo_boxes[unit_label].setCurrentIndex(DOFSetup.FIXED)
                    else:
                        self.dof_setup_combo_boxes[unit_label].setCurrentIndex(DOFSetup.VALUE)

                if isinstance(values[index], complex):
                    if values[index] == complex(0):
                        continue

                    lineEdit_real.setText(str(np.real(values[index])))
                    lineEdit_imag.setText(str(np.imag(values[index])))

    def update_element_type_based_on_geometry_information(self):
        volume_exists = self.mesh.are_there_volumes_in_geometry()
        self.comboBox_element_type.setCurrentIndex(int(volume_exists))

    def check_complex_entries(self, line_edit_real: QLineEdit, line_edit_imag: QLineEdit, label: str):

        _real = None
        input_real = line_edit_real.text()

        if input_real != "":
            if input_real == "fixed":
                _real = 0.

            elif input_real != "free":
                try:
                    real_input = input_real.replace(",", ".")
                    _real = float(real_input)

                except Exception:
                    app().main_window.hide_dialogs()
                    title = f"Invalid entry to the {label}"
                    message = f"Wrong input for real part of {label}."
                    PrintMessageInput([error_title, title, message])
                    return True, None

        _imag = None
        input_imag = line_edit_imag.text()

        if input_imag != "":
            if input_imag == "fixed":
                _imag = 0.

            elif input_imag != "free":
                try:
                    input_imag = input_imag.replace(",", ".")
                    _imag = float(input_imag)

                except Exception:
                    app().main_window.hide_dialogs()
                    title = f"Invalid entry to the {label}"
                    message = f"Wrong input for imaginary part of {label}."
                    PrintMessageInput([error_title, title, message])
                    return True, None

        if (_real, _imag).count(None) == 2:
            if line_edit_real.isEnabled() and line_edit_imag.isEnabled():
                app().main_window.hide_dialogs()
                title = "Empty fields detected"
                message = "Enter a value in the real and/or imaginary "
                message += "part input field to proceed."
                PrintMessageInput([error_title, title, message])
                return True, None
            else:
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
        selection = self.assignment_types.get(attribution_type)
        selected_ids, error_data = self.mesh.check_selected_ids(input_ids, selection=selection, single_id=False)

        if error_data is not None:
            app().main_window.hide_dialogs()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        etype_index = self.comboBox_element_type.currentIndex()
        element_type = self.element_types[etype_index]

        stop, ux = self.check_complex_entries(self.lineEdit_real_ux, self.lineEdit_imag_ux, "ux")
        if stop:
            return True

        stop, uy = self.check_complex_entries(self.lineEdit_real_uy, self.lineEdit_imag_uy, "uy")
        if stop:
            return True

        stop, uz = self.check_complex_entries(self.lineEdit_real_uz, self.lineEdit_imag_uz, "uz")
        if stop:
            return True

        prescribed_dof = [ux, uy, uz]

        if element_type == "2d_element":

            stop, rx = self.check_complex_entries(self.lineEdit_real_rx, self.lineEdit_imag_rx, "rx")
            if stop:
                return True

            stop, ry = self.check_complex_entries(self.lineEdit_real_ry, self.lineEdit_imag_ry, "ry")
            if stop:
                return True

            stop, rz = self.check_complex_entries(self.lineEdit_real_rz, self.lineEdit_imag_rz, "rz")
            if stop:
                return True

            prescribed_dof.extend([rx, ry, rz])
                
        condition_1 = element_type == "2d_element" and prescribed_dof.count(None) == 6
        condition_2 = element_type == "3d_element" and prescribed_dof.count(None) == 3
        all_dof_free = condition_1 or condition_2

        self.remove_duplicated_attributions(selected_ids, selection)
        self.remove_conflicting_excitations(selected_ids, selection, all_dof_free=all_dof_free)

        if all_dof_free:
            return

        real_values = [value if value is None else np.real(value) for value in prescribed_dof]
        imag_values = [value if value is None else np.imag(value) for value in prescribed_dof]

        for selected_id in selected_ids:

            data = {
                "element_type" : element_type,
                "values" : prescribed_dof,
                "real_values" : real_values,
                "imag_values" : imag_values,
                "integrate" : self.comboBox_data_type.currentIndex(),
            }

            if attribution_type == AssignmetType.SURFACES:
                self.properties._set_property("prescribed_dof", data, surface=selected_id)

            elif attribution_type == AssignmetType.LINES:
                self.properties._set_property("prescribed_dof", data, line=selected_id)

            elif attribution_type == AssignmetType.POINTS:
                self.properties._set_property("prescribed_dof", data, point=selected_id)

            elif attribution_type == AssignmetType.NODES:
                self.properties._set_property("prescribed_dof", data, node=selected_id)

        if self.comboBox_data_type.currentIndex() != DataType.DISPLACEMENT:
            self.update_analysis_setup_to_filter_zero_frequency()

    def update_analysis_setup_to_filter_zero_frequency(self):
        if self.model.analysis_id == AnalysisID.STRUCTURAL_HARMONIC:
            analysis_setup = self.model.modify_analysis_setup_to_filter_zero_frequency(self.model.analysis_setup)
            app().project.configure_analysis(analysis_setup)

    def load_table(self, lineEdit : QLineEdit, dof_label : str, direct_load = False):
        try:
            if direct_load:
                imported_path = lineEdit.text()

            else:
                extensions = SUPPORTED_SPREADSHEET_EXTENSIONS + SUPPORTED_TEXT_EXTENSIONS
                imported_path = FileDialogService.open_file(file_extensions=extensions,
                                                            caption=f"Choose a table to import the {dof_label} data",
                                                            last_folder="imported_table_folder")

            imported_data = FileHandler.read(imported_path)

            if imported_data is None:
                return None, None

            imported_values = imported_data.data
            imported_table_path = str(imported_data.path)

            if not direct_load:
                lineEdit.setText(imported_table_path)
                lineEdit.setToolTip(imported_table_path)

            if imported_values.shape[1] < 3:
                title = "Error while loading table"
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

    def integrate_and_save_table_files(self, dof_label: str, selected_id: int, selection: str, values: np.ndarray):

        if self.frequencies[0] == 0:
            self.frequencies[0] = float(1e-6)

        # n_diff = self.comboBox_data_type.currentIndex()
        # if n_diff:
        #     values /= (1j*2*np.pi*self.frequencies)**n_diff

        if self.frequencies[0] == float(1e-6):
            self.frequencies[0] = 0

        if app().project.model.change_analysis_frequency_setup(list(self.frequencies)):

            app().main_window.hide_dialogs()
            lineEdit = self.table_line_edits.get(dof_label)
            imported_filename = basename(lineEdit.text())
            self.lineEdit_reset(lineEdit)

            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\nFile name: {imported_filename}"
            PrintMessageInput([error_title, title, message])

            return None, None

        table_name = f"prescribed_dof_{dof_label}_from_{selection[:-1]}_{selected_id}"

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
            app().main_window.hide_dialogs()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        element_type = "3d_element" if self.comboBox_element_type.currentIndex() else "2d_element"

        for i, label in enumerate(["ux", "uy", "uz", "rx", "ry", "rz"]):
            if element_type == "3d_element" and i >= 3:
                break

            line_edit = self.__getattribute__(f"lineEdit_path_table_{label}")
            if isinstance(line_edit, QLineEdit):
                if line_edit.text() == "":
                    continue

                if Path(line_edit.text()).exists:
                    _table_path = self.__getattribute__(f"{label}_table_path")
                    _table_values = self.__getattribute__(f"{label}_table_values")
                    _table_values, _table_path = self.load_table(line_edit, label.capitalize(), direct_load = True)

        table_names = list()
        table_paths = list()

        for selected_id in selected_ids:

            for i, label in enumerate(["ux", "uy", "uz", "rx", "ry", "rz"]):
                _table_name = None
                if element_type == "3d_element" and i >= 3:
                    break

                _table_path = self.__getattribute__(f"{label}_table_path")
                _table_values = self.__getattribute__(f"{label}_table_values")

                if isinstance(_table_values, np.ndarray):
                    _table_name = "prescribed_dof_{}_from_{}_{}".format(label, str(selection[:-1]), str(selected_id))
                    if save_table_values(_table_name, _table_values, "structural"):
                        return

                table_names.append(_table_name)
                table_paths.append(_table_path)

            condition_1 = element_type == "2d_element" and table_names.count(None) == 6
            condition_2 = element_type == "3d_element" and table_names.count(None) == 3

            if condition_1 or condition_2:
                app().main_window.hide_dialogs()
                title = "Additional inputs required"
                message = "You must enter at least one prescribed dof table path before confirming the assignment."
                PrintMessageInput([error_title, title, message]) 
                return True

            self.remove_duplicated_attributions(selected_ids, selection)
            self.remove_conflicting_excitations(selected_ids, selection)

            data = {
                "element_type" : element_type,
                "table_names" : table_names,
                "table_paths" : table_paths,
                "integrate" : self.comboBox_data_type.currentIndex(),
            }

            if attribution_type == AssignmetType.SURFACES:
                self.properties._set_property("prescribed_dof", data, surface=selected_id)

            elif attribution_type == AssignmetType.LINES:
                self.properties._set_property("prescribed_dof", data, line=selected_id)

            elif attribution_type == AssignmetType.POINTS:
                self.properties._set_property("prescribed_dof", data, point=selected_id)

            elif attribution_type == AssignmetType.NODES:
                self.properties._set_property("prescribed_dof", data, node=selected_id)
                
        if self.comboBox_data_type.currentIndex() != DataType.DISPLACEMENT:
            self.update_analysis_setup_to_filter_zero_frequency()

        self.reset_table_variables()

    def remove_duplicated_attributions(self, selected_ids: list, selection: str):

        table_names = list()
        nodes_to_remove = list()
        for selected_id in selected_ids:

            if selection == "surfaces":

                nodes_from_surface = self.mesh.get_nodes_from_surface(selected_id)
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "prescribed_dof" and node_id in nodes_from_surface:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for line_id in self.mesh.lines_from_surface[selected_id]:
                    data = self.properties._get_property("prescribed_dof", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("prescribed_dof", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dof", line_id, "lines"))

                    for point_id in self.mesh.points_from_line[line_id]:
                        data = self.properties._get_property("prescribed_dof", point=point_id)
                        if isinstance(data, dict):
                            self.properties._remove_point_property("prescribed_dof", point_id)
                            table_names.extend(self.properties.get_property_related_table_names("prescribed_dof", point_id, "points"))

            elif selection == "lines":

                nodes_from_line = self.mesh.get_nodes_from_line(selected_id)
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "prescribed_dof" and node_id in nodes_from_line:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for surface_id in self.mesh.surfaces_from_line[selected_id]:
                    data = self.properties._get_property("prescribed_dof", surface=surface_id)
                    if isinstance(data, dict):
                        self.properties._remove_surface_property("prescribed_dof", surface_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dof", surface_id, "surfaces"))

                for point_id in self.mesh.points_from_line[selected_id]:
                    data = self.properties._get_property("prescribed_dof", point=point_id)
                    if isinstance(data, dict):
                        self.properties._remove_point_property("prescribed_dof", point_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dof", point_id, "points"))

            elif selection == "points":

                nodes_from_point = self.mesh.nodes_from_points[selected_id]
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "prescribed_dof" and node_id in nodes_from_point:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for line_id in self.mesh.lines_from_point[selected_id]:
                    data = self.properties._get_property("prescribed_dof", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("prescribed_dof", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dof", line_id, "lines"))

                    for surface_id in self.mesh.surfaces_from_line[line_id]:
                        data = self.properties._get_property("prescribed_dof", surface=surface_id)
                        if isinstance(data, dict):
                            self.properties._remove_surface_property("prescribed_dof", surface_id)
                            table_names.extend(self.properties.get_property_related_table_names("prescribed_dof", surface_id, "surfaces"))

            elif selection == "nodes":

                point_id = selected_id + 1
                data = self.properties._get_property("prescribed_dof", point=point_id)
                if isinstance(data, dict):
                    self.properties._remove_point_property("prescribed_dof", point_id)
                    table_names.extend(self.properties.get_property_related_table_names("prescribed_dof", point_id, "points"))

                for line_id in self.mesh.lines_from_point[point_id]:
                    data = self.properties._get_property("prescribed_dof", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("prescribed_dof", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dof", line_id, "lines"))

                    for surface_id in self.mesh.surfaces_from_line[line_id]:
                        data = self.properties._get_property("prescribed_dof", surface=surface_id)
                        if isinstance(data, dict):
                            self.properties._remove_surface_property("prescribed_dof", surface_id)
                            table_names.extend(self.properties.get_property_related_table_names("prescribed_dof", surface_id, "surfaces"))

            for node_id in nodes_to_remove:
                self.properties._remove_nodal_property("prescribed_dof", node_id)
                table_names.extend(self.properties.get_property_related_table_names("prescribed_dof", node_id, "nodes"))

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

    def get_dofs_labels(self, dofs_mask: list[bool], n_int: int):

        def dof_label(dof_index: str, n_int: int):
            dof_type = "U" if dof_index < 3 else "\u03b8"
            directions = ["x", "y", "z", "x", "y", "z"]
            data_types = ["{}{}", "d{}{}/dt", "d²{}{}/dt²"]
            # data_types = ["{}<sub>{}</sub>", "d{}<sub>{}</sub>/dt", "d²{}<sub>{}</sub>/dt²"]
            return data_types[n_int].format(dof_type, directions[dof_index])

        n_dofs = len(dofs_mask)
        dof_labels = np.array([dof_label(i, n_int) for i in range(n_dofs)])[dofs_mask]

        return ", ".join([label for label in dof_labels])

    def add_model_info_in_tree_widget(self, entity: str):

        properties = {
            "surface": self.properties.surface_properties,
            "line": self.properties.line_properties,
            "point": self.properties.point_properties,
            "node": self.properties.nodal_properties,
        }

        _property = properties.get(entity)
        if _property is None:
            return

        for (property, *args), data in _property.items():
            if property != "prescribed_dof":
                continue

            if not isinstance(data, dict):
                continue

            values = data.get("values")
            if values is None:
                continue

            dofs_mask = [not value is None for value in values]
            if sum(dofs_mask) == 6:
                continue

            n_int = data.get("integrate", 0)
            element_type = data.get("element_type")
            dof_labels = str(self.get_dofs_labels(dofs_mask, n_int))

            new = QTreeWidgetItem([f"{entity.capitalize()}-{args[0]}", dof_labels, element_type])
            for i in range(3):
                new.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_prescribed_dof.addTopLevelItem(new)

    def load_model_info(self):

        self.treeWidget_prescribed_dof.clear()

        self.add_model_info_in_tree_widget("surface")
        self.add_model_info_in_tree_widget("line")
        self.add_model_info_in_tree_widget("point")
        self.add_model_info_in_tree_widget("node")
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
                if property != "prescribed_dof":
                    continue

                # if not are_there_values_different_from_zero(data.get("values")):
                #     continue

                self.tabWidget_main.setTabVisible(StandardTabType.LIST, True)
                return

        self.lineEdit_real_ux.setFocus()
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

    def remove_conflicting_excitations(self, selected_ids: int | list, selection: str, all_dof_free: bool=False):

        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        properties = ["nodal_loads", "prescribed_dof"]

        for selected_id in selected_ids:
            for _property in properties:
                if all_dof_free and _property == "nodal_loads":
                    continue

                table_names = self.properties.get_property_related_table_names(_property, selected_id, selection)
                self.remove_property_from(_property, selected_id, selection)
                self.process_table_file_removal(table_names)

    def remove_table_files_from(self, selected_id : list, selection: str):
        table_names = self.properties.get_property_related_table_names("prescribed_dof", selected_id, selection)
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
            self.remove_property_from("prescribed_dof", selected_id, selection)
            self.actions_to_finalize()

            app().main_window.selection.set_geometry_selection()
            app().main_window.selection.set_mesh_selection()

    def reset_callback(self):

        app().main_window.hide_dialogs()

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

            for key, _property in properties.items():
                for (property_label, *args), data in _property.items():
                    if property_label != "prescribed_dof":
                        continue
    
                    entities_to_remove[key].append(args[0])

            for selection, selected_ids in entities_to_remove.items():
                for selected_id in selected_ids:
                    table_name = self.properties.get_property_related_table_names("prescribed_dof", selected_id, selection)
                    self.process_table_file_removal(table_name)

            self.properties._reset_property("prescribed_dof")
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

    def reset_input_fields(self, reset_all: bool = False):

        if reset_all:
            self.lineEdit_selection_id.setText("")

        for key, combo_box in self.dof_setup_combo_boxes.items():
            if combo_box.currentIndex() == DOFSetup.VALUE:
                line_edit_real, line_edit_imag = self.constant_line_edits.get(key)
                line_edit_real.setText("")
                line_edit_imag.setText("")

        for lineEdit_table in self.table_line_edits.values():
            lineEdit_table.setText("")
            lineEdit_table.setToolTip("")

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