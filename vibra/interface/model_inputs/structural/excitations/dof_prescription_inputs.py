
from collections import defaultdict
from enum import IntEnum
from os.path import basename
from pathlib import Path

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QLabel, QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.engine.analysis_info import AnalysisID
from vibra.interface import error_title
from vibra.interface.common.common_interface import save_table_values, update_analysis_setup_in_file, update_entities_selection
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.structural.definitions.enums import StandardTabType
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator

# from vibra.utils.utils import are_there_values_different_from_zero
from vibra.interface.ui_generated.model.structural.excitations.dof_prescription_inputs_ui import DofPrescriptionInputs_UI


class ElementFormulation(IntEnum):
    ELEMENT_2D = 0
    ELEMENT_3D = 1


class DOFSetup(IntEnum):
    VALUE = 0
    FREE = 1
    FIXED = 2


class AssignmentType(IntEnum):
    SURFACES = 0
    LINES = 1
    POINTS = 2
    NODES = 3
    MULTIPLE = 4


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
        self._initialize()
        self._create_list_line_edits()
        self._configure_validators()
        self._config_widgets()
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

    def _create_list_line_edits(self):

        self.constant_values_line_edits = {
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

        self.comboBox_element_type.setEnabled(False)
        self.treeWidget_prescribed_dof.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        for i, w in enumerate([80, 100, 120, 120]):
            self.treeWidget_prescribed_dof.setColumnWidth(i, w)
            self.treeWidget_prescribed_dof.headerItem().setTextAlignment(i, Qt.AlignCenter)

        for line_edit in self.table_line_edits.values():
            font = line_edit.font()
            font.setPointSize(8)
            line_edit.setFont(font)

    def _configure_validators(self):
        for line_edit_real, line_edit_imag in self.constant_values_line_edits.values():
            line_edit_real.setValidator(StrictDoubleValidator(-1e16, 1e16, 8))
            line_edit_imag.setValidator(StrictDoubleValidator(-1e16, 1e16, 8))

    def _create_connections(self):

        # QComboBox connections
        self.comboBox_assignment_type.currentIndexChanged.connect(self.assignment_type_callback)
        self.comboBox_data_type.currentIndexChanged.connect(self.update_combo_box_units_callback)
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_callback)
        self.comboBox_displacement_ux.currentIndexChanged.connect(self.displacement_ux_callback)
        self.comboBox_displacement_uy.currentIndexChanged.connect(self.displacement_uy_callback)
        self.comboBox_displacement_uz.currentIndexChanged.connect(self.displacement_uz_callback)
        self.comboBox_rotation_rx.currentIndexChanged.connect(self.rotation_rx_callback)
        self.comboBox_rotation_ry.currentIndexChanged.connect(self.rotation_ry_callback)
        self.comboBox_rotation_rz.currentIndexChanged.connect(self.rotation_rz_callback)

        # QPushButton connections
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

        # QTabWidget connection
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)

        # QTreeWidget connections
        self.treeWidget_prescribed_dof.itemClicked.connect(self.item_clicked_callback)
        self.treeWidget_prescribed_dof.itemDoubleClicked.connect(self.item_double_clicked_callback)
        self.treeWidget_prescribed_dof.itemSelectionChanged.connect(self.item_selection_clicked_callback)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

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

    def assignment_type_callback(self):
        if self.comboBox_assignment_type.currentIndex() == AssignmentType.NODES:
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

        line_edit_real, line_edit_imag = self.constant_values_line_edits.get(unit_label, (None, None))
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
        for lineEdit_real, lineEdit_imag in self.constant_values_line_edits.values():
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

        multiple_selection = sum([len(entities) > 0 for entities in (surfaces, lines, points, nodes)]) >= 2

        if self.tabWidget_main.currentIndex() == StandardTabType.LIST and multiple_selection:
            self.lineEdit_selection_id.setText("mult. entities")
            self.comboBox_assignment_type.setCurrentIndex(AssignmentType.MULTIPLE)
            view = self.comboBox_assignment_type.view()
            view.setRowHidden(4, False)
            return

        if surfaces:

            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_assignment_type.setCurrentIndex(AssignmentType.SURFACES)

            if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
                return

            if len(surfaces) == 1:
                surface_id = next(iter(surfaces))
                data = self.properties._get_property("prescribed_dof", surface=surface_id)
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
                data = self.properties._get_property("prescribed_dof", line=line_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(line_id=line_id)

        elif points:
            
            text = ", ".join([str(i) for i in points])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_assignment_type.setCurrentIndex(AssignmentType.POINTS)

            if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
                return

            if len(points) == 1:
                point_id = next(iter(points))
                data = self.properties._get_property("prescribed_dof", point=point_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(point_id=point_id)

        elif nodes:
            
            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_assignment_type.setCurrentIndex(AssignmentType.NODES)

            if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
                return

            if len(nodes) == 1:
                node_id = next(iter(nodes))
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

            values = data.get("values", [])
            self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)

            for index, (unit_label, (lineEdit_real, lineEdit_imag)) in enumerate(self.constant_values_line_edits.items()):
    
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

    def constant_values_attribution(self, selection: str, selected_ids: list[int]):

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
                "real_values" : real_values,
                "imag_values" : imag_values,
                "integrate" : self.comboBox_data_type.currentIndex(),
            }

            match selection:
                case "surfaces":
                    self.properties._set_property("prescribed_dof", data, surface=selected_id)

                case "lines":
                    self.properties._set_property("prescribed_dof", data, line=selected_id)

                case "points": 
                    self.properties._set_property("prescribed_dof", data, point=selected_id)

                case "nodes":
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
                if lineEdit.text() == "":
                    return None, None

                imported_table_path = lineEdit.text()
                imported_values = DataImporter.read_data_in_file(imported_table_path)[0].data

            else:
                imported_data = DataImporter.import_single_file(
                    "imported_table_folder", ["csv", "dat", "txt", "xlsx", "xls"], f"Choose a table to import the {dof_label} data"
                )
                if not imported_data:
                    return None, None

                imported_values = imported_data.data
                imported_table_path = imported_data.path

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

    def table_values_attribution(self, selection: str, selected_ids: list[int]):

        etype_index = self.comboBox_element_type.currentIndex()
        element_type = self.element_types[etype_index]

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

        table_names = []
        table_paths = []

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

            match selection:
                case "surfaces":
                    self.properties._set_property("prescribed_dof", data, surface=selected_id)

                case "lines":
                    self.properties._set_property("prescribed_dof", data, line=selected_id)

                case "points": 
                    self.properties._set_property("prescribed_dof", data, point=selected_id)

                case "nodes":
                    self.properties._set_property("prescribed_dof", data, node=selected_id)
                
        if self.comboBox_data_type.currentIndex() != DataType.DISPLACEMENT:
            self.update_analysis_setup_to_filter_zero_frequency()

        self.reset_table_variables()

    def remove_duplicated_attributions(self, selected_ids: list, selection: str):

        table_names = []
        nodes_to_remove = []
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

    def apply_callback(self, close_window: bool=False):

        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == StandardTabType.LIST:
            return

        input_ids = self.lineEdit_selection_id.text()
        assignment_type = self.comboBox_assignment_type.currentIndex()
        selection = self.assignment_types.get(assignment_type)

        selected_ids, error_data = self.model.check_selected_ids(
            input_ids,
            selection,
            domain="structural",
        )

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        update_entities_selection(self.lineEdit_selection_id, selection, selected_ids)
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

        if tab_index == StandardTabType.CONSTANT_DATA:
            if self.constant_values_attribution(selection, selected_ids):
                return

        if tab_index == StandardTabType.TABULAR_DATA:
            if self.table_values_attribution(selection, selected_ids):
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

        properties = {
            "surface": self.properties.surface_properties,
            "line": self.properties.line_properties,
            "point": self.properties.point_properties,
            "node": self.properties.nodal_properties,
        }

        self.treeWidget_prescribed_dof.clear()
       
        for key, property in properties.items():
            for (prop_label, *args), data in property.items():

                if prop_label != "prescribed_dof":
                    continue


                if not isinstance(data, dict):
                    continue

                values = data.get("values")
                element_type = data.get("element_type")

                if values is None:
                    continue

                dofs_mask = [not value is None for value in values]
                if sum(dofs_mask) == 6:
                    continue

                n_int = data.get("integrate", 0)
                element_type = data.get("element_type")
                dof_labels = str(self.get_dofs_labels(dofs_mask, n_int))

                new = QTreeWidgetItem([
                    f"{args[0]}", 
                    key, 
                    element_type, 
                    dof_labels, 
                    ])

                for i in range(4):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_prescribed_dof.addTopLevelItem(new)

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
            view.setRowHidden(4, True)
            self.comboBox_assignment_type.setCurrentIndex(AssignmentType.SURFACES)

        self.lineEdit_selection_id.setText("")
        self.treeWidget_prescribed_dof.clearSelection()

    def item_selection_clicked_callback(self):
        self.item_clicked_callback(None)

    def item_clicked_callback(self, item):

        self.pushButton_remove.setDisabled(False)

        selected_items = self.treeWidget_prescribed_dof.selectedItems()
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
            points = entities_mapping.get("point"),
            )

        # app().main_window.selection.set_mesh_selection(
        #     nodes = entities_mapping.get("node"),
        # )

    def item_double_clicked_callback(self, item):
        self.item_clicked_callback(item)

    def remove_conflicting_excitations(self, selected_ids: int | list, selection: str, all_dof_free: bool=False):

        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        properties = ["nodal_loads", "prescribed_dof"]

        for selected_id in selected_ids:
            for _property in properties:
                if all_dof_free and _property == "nodal_loads":
                    continue

                self.remove_property_from(_property, selected_id, selection)

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

        selected_items = self.treeWidget_prescribed_dof.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            selected_id = int(item.text(0))
            selection = item.text(1)

            if selection == "surface":
                self.properties._remove_surface_property("prescribed_dof", selected_id)

            elif selection == "line":
                self.properties._remove_line_property("prescribed_dof", selected_id)

            elif selection == "point":
                self.properties._remove_point_property("prescribed_dof", selected_id)

            elif selection == "node":
                self.properties._remove_nodal_property("prescribed_dof", selected_id)

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
                line_edit_real, line_edit_imag = self.constant_values_line_edits.get(key)
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