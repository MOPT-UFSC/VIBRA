
from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QFileDialog, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.model_inputs.data_filter.change_frequency_data_handler import ChangeFrequencyDataRangeInput
from vibra.interface.general.print_message_input import PrintMessageInput

from os.path import basename
from pathlib import Path

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class StructuralExternalLoadsInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/structural_external_loads_input.ui"
        uic.loadUi(ui_path, self)

        self.model = app().project.model
        self.properties = app().project.model.properties

        app().main_window.set_input_widget(self)
        app().main_window.viewer_tabs.show_geometry()

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        self._config_widgets()
        self.geometry_selection_callback()
        self.load_model_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Set structural external loads")

    def _initialize(self):

        self.keep_window_open = True

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

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_averaged_constant_values: QCheckBox
        self.checkBox_averaged_table_values: QCheckBox

        # QComboBox
        self.comboBox_attribution_type: QComboBox
        self.comboBox_element_type: QComboBox
        self.comboBox_load_distribution_constant_values: QComboBox
        self.comboBox_load_distribution_table_values: QComboBox

        # QLabel
        self.label_Fx_constant: QLabel
        self.label_Fy_constant: QLabel
        self.label_Fz_constant: QLabel
        self.label_Mx_constant: QLabel
        self.label_My_constant: QLabel
        self.label_Mz_constant: QLabel
        #
        self.label_Fx_unit: QLabel
        self.label_Fy_unit: QLabel
        self.label_Fz_unit: QLabel
        self.label_Mx_unit: QLabel
        self.label_My_unit: QLabel
        self.label_Mz_unit: QLabel
        #
        self.label_Fx_table: QLabel
        self.label_Fy_table: QLabel
        self.label_Fz_table: QLabel
        self.label_Mx_table: QLabel
        self.label_My_table: QLabel
        self.label_Mz_table: QLabel

        # QLineEdit
        self.lineEdit_selection_id: QLineEdit
        self.lineEdit_real_Fx: QLineEdit
        self.lineEdit_real_Fy: QLineEdit
        self.lineEdit_real_Fz: QLineEdit
        self.lineEdit_real_Mx: QLineEdit
        self.lineEdit_real_My: QLineEdit
        self.lineEdit_real_Mz: QLineEdit
        #
        self.lineEdit_imag_Fx: QLineEdit
        self.lineEdit_imag_Fy: QLineEdit
        self.lineEdit_imag_Fz: QLineEdit
        self.lineEdit_imag_Mx: QLineEdit
        self.lineEdit_imag_My: QLineEdit
        self.lineEdit_imag_Mz: QLineEdit
        #
        self.lineEdit_path_table_Fx: QLineEdit
        self.lineEdit_path_table_Fy: QLineEdit
        self.lineEdit_path_table_Fz: QLineEdit
        self.lineEdit_path_table_Mx: QLineEdit
        self.lineEdit_path_table_My: QLineEdit
        self.lineEdit_path_table_Mz: QLineEdit
        #
        self._create_list_lineEdits()

        # QPushButton
        self.pushButton_attribute: QPushButton
        self.pushButton_exit: QPushButton
        self.pushButton_load_Fx_table: QPushButton
        self.pushButton_load_Fy_table: QPushButton
        self.pushButton_load_Fz_table: QPushButton
        self.pushButton_load_Mx_table: QPushButton
        self.pushButton_load_My_table: QPushButton
        self.pushButton_load_Mz_table: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_external_loads: QTreeWidget

    def _create_list_lineEdits(self):

        self.list_lineEdit_constant_values = [  
                                              [self.lineEdit_real_Fx, self.lineEdit_imag_Fx],
                                              [self.lineEdit_real_Fy, self.lineEdit_imag_Fy],
                                              [self.lineEdit_real_Fz, self.lineEdit_imag_Fz],
                                              [self.lineEdit_real_Mx, self.lineEdit_imag_Mx],
                                              [self.lineEdit_real_My, self.lineEdit_imag_My],
                                              [self.lineEdit_real_Mz, self.lineEdit_imag_Mz],
                                              ]

        self.list_lineEdit_table_values = [ 
                                           self.lineEdit_path_table_Fx,
                                           self.lineEdit_path_table_Fy,
                                           self.lineEdit_path_table_Fz,
                                           self.lineEdit_path_table_Mx,
                                           self.lineEdit_path_table_My,
                                           self.lineEdit_path_table_Mz,
                                           ]

    def _config_widgets(self):
        #
        for i, w in enumerate([60, 100, 160]):
            self.treeWidget_external_loads.setColumnWidth(i, w)
            self.treeWidget_external_loads.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_callback)
        self.comboBox_load_distribution_constant_values.currentIndexChanged.connect(self.update_controls_for_constant_values)
        self.comboBox_load_distribution_table_values.currentIndexChanged.connect(self.update_controls_for_table_values)
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_load_Fx_table.clicked.connect(self.load_Fx_table)
        self.pushButton_load_Fy_table.clicked.connect(self.load_Fy_table)
        self.pushButton_load_Fz_table.clicked.connect(self.load_Fz_table)
        self.pushButton_load_Mx_table.clicked.connect(self.load_Mx_table)
        self.pushButton_load_My_table.clicked.connect(self.load_My_table)
        self.pushButton_load_Mz_table.clicked.connect(self.load_Mz_table)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_external_loads.itemClicked.connect(self.on_click_item)
        self.treeWidget_external_loads.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.update_controls_for_constant_values()
        self.update_controls_for_table_values()

    def geometry_selection_callback(self):

        faces = app().main_window.selected_geometry_surfaces
        lines = app().main_window.selected_geometry_lines
        points = app().main_window.selected_geometry_points
        nodes = app().main_window.selected_mesh_nodes

        if faces:

            self.comboBox_attribution_type.setCurrentIndex(0)

            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)

            if len(faces) == 1:
                surface_id = list(faces)[0]
                data = self.properties._get_property("external_loads", surface=surface_id)
                self.update_input_fields(data)

        elif lines:
            
            self.comboBox_attribution_type.setCurrentIndex(1)

            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)

            if len(lines) == 1:
                line_id = list(lines)[0]
                data = self.properties._get_property("external_loads", line=line_id)
                self.update_input_fields(data)

        elif points:
            
            self.comboBox_attribution_type.setCurrentIndex(2)

            text = ", ".join([str(i) for i in points])
            self.lineEdit_selection_id.setText(text)

            if len(points) == 1:
                point_id = list(points)[0]
                data = self.properties._get_property("external_loads", point=point_id)
                self.update_input_fields(data)

        elif nodes:
            
            self.comboBox_attribution_type.setCurrentIndex(3)

            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)

            if len(nodes) == 1:
                node_id = list(nodes)[0]
                data = self.properties._get_property("external_loads", node=node_id)
                self.update_input_fields(data)

    def update_input_fields(self, data: dict):

        if isinstance(data, dict):

            self.reset_input_fields()
            values = data.get("values", None)

            if "table_paths" in data.keys():
                table_paths = data["table_paths"]
                for index, lineEdit_table in enumerate(self.list_lineEdit_table_values):
                    table_path = table_paths[index]
                    if table_path is not None:                   
                        lineEdit_table.setText(table_path)

            else:
                for index, [lineEdit_real, lineEdit_imag] in enumerate(self.list_lineEdit_constant_values):

                    if data["element_type"] == "3d_element" and index >= 3:
                        continue
                    
                    elif index <= 5 and values[index] is not None:
                        lineEdit_real.setText(str(np.real(values[index])))
                        lineEdit_imag.setText(str(np.imag(values[index])))

    def attribution_type_callback(self):
        if self.comboBox_attribution_type.currentIndex() == 3:
            app().main_window.viewer_tabs.show_mesh()
        else:
            app().main_window.viewer_tabs.show_geometry()

    def element_type_callback(self):

        key = self.comboBox_element_type.currentIndex() == 0

        self.label_Mx_constant.setEnabled(key)
        self.label_My_constant.setEnabled(key)
        self.label_Mz_constant.setEnabled(key)

        self.label_Mx_unit.setEnabled(key)
        self.label_My_unit.setEnabled(key)
        self.label_Mz_unit.setEnabled(key)

        self.label_Mx_table.setEnabled(key)
        self.label_My_table.setEnabled(key)
        self.label_Mz_table.setEnabled(key)

        self.lineEdit_real_Mx.setEnabled(key)
        self.lineEdit_real_My.setEnabled(key)
        self.lineEdit_real_Mz.setEnabled(key)

        self.lineEdit_imag_Mx.setEnabled(key)
        self.lineEdit_imag_My.setEnabled(key)
        self.lineEdit_imag_Mz.setEnabled(key)

        self.pushButton_load_Mx_table.setEnabled(key)
        self.pushButton_load_My_table.setEnabled(key)
        self.pushButton_load_Mz_table.setEnabled(key)

    def check_complex_entries(self, real_input: str, imag_input: str, label: str):

        _real = None
        if real_input != "":
            try:
                _real = float(real_input)

            except Exception:
                self.hide()
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([window_title_1, title, message])
                return True, None

        _imag = None
        if imag_input != "":
            try:
                _imag = float(imag_input)

            except Exception:
                self.hide()
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for imaginary part of {label}."
                PrintMessageInput([window_title_1, title, message])
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

        if attribution_type == 0:
            selection = "surfaces"

        elif attribution_type == 1:
            selection = "lines"

        elif attribution_type == 2:
            selection = "points"

        else:
            selection = "nodes"

        selected_ids = app().project.model.mesh.check_selected_ids(
                                                                   input_ids, 
                                                                   selection = selection
                                                                   )

        if selected_ids is None:
            self.lineEdit_selection_id.setFocus()
            return

        self.remove_duplicated_attributions(selected_ids, selection)
        self.remove_conflicting_excitations(selected_ids, selection)

        if self.comboBox_element_type.currentIndex() == 0:
            element_type = "2d_element"
        else:
            element_type = "3d_element"

        stop, Fx= self.check_complex_entries(self.lineEdit_real_Fx.text(), self.lineEdit_imag_Fx.text(), "Fx")
        if stop:
            return

        stop, Fy= self.check_complex_entries(self.lineEdit_real_Fy.text(), self.lineEdit_imag_Fy.text(), "Fy")
        if stop:
            return

        stop, Fz= self.check_complex_entries(self.lineEdit_real_Fz.text(), self.lineEdit_imag_Fz.text(), "Fz")
        if stop:
            return

        external_loads = [Fx, Fy, Fz]

        if self.comboBox_element_type.currentIndex() == 0:
            
            stop, rx= self.check_complex_entries(self.lineEdit_real_Mx.text(), self.lineEdit_imag_Mx.text(), "rx")
            if stop:
                return

            stop, ry= self.check_complex_entries(self.lineEdit_real_My.text(), self.lineEdit_imag_My.text(), "ry")
            if stop:
                return

            stop, Mz= self.check_complex_entries(self.lineEdit_real_Mz.text(), self.lineEdit_imag_Mz.text(), "Mz")
            if stop:
                return

            external_loads.extend([rx, ry, Mz])

        condition_1 = self.comboBox_element_type.currentIndex() == 0 and external_loads.count(None) < 6
        condition_2 = self.comboBox_element_type.currentIndex() == 1 and external_loads.count(None) < 3

        if condition_1 or condition_2:

            real_values = [value if value is None else np.real(value) for value in external_loads]
            imag_values = [value if value is None else np.imag(value) for value in external_loads]

            nodal_attribution = bool(self.comboBox_load_distribution_constant_values.currentIndex())
            key_avg = self.checkBox_averaged_constant_values.isChecked()

            for selected_id in selected_ids:

                data = {
                        "element_type" : element_type,
                        "values" : external_loads,
                        "real_values" : real_values,
                        "imag_values" : imag_values,
                        "nodal_attribution": nodal_attribution,
                        "averaged": key_avg,
                        }

                if attribution_type == 0:
                    self.properties._set_property("external_loads", data, surface=selected_id)

                elif attribution_type == 1:
                    self.properties._set_property("external_loads", data, line=selected_id)

                elif attribution_type == 2:
                    self.properties._set_property("external_loads", data, point=selected_id)

                elif attribution_type == 3:
                    self.properties._set_property("external_loads", data, node=selected_id)

            self.actions_to_finalize()

        else:
            title = "Additional inputs required"
            message = "It is necessary to enter at least one prescribed dof "
            message += "before confirming the property assignment."
            PrintMessageInput([window_title_1, title, message])

    def load_table(self, lineEdit : QLineEdit, load_label : str, direct_load = False):

        title = "Error while loading table"

        try:
            if direct_load:
                imported_table_path = lineEdit.text()

            else:

                last_path = app().config.get_last_folder_for("imported table folder")
                if last_path is None:
                    path = str(Path().home())
                else:
                    path = last_path

                caption = f"Choose a table to import the {load_label} data"
                imported_table_path, check = QFileDialog.getOpenFileName(  
                                                                         None, 
                                                                         caption, 
                                                                         path, 
                                                                         "Files (*.csv; *.dat; *.txt)"
                                                                         )

                if not check:
                    return None, None

            lineEdit.setText(imported_table_path)
            app().config.write_last_folder_path_in_file("imported table folder", imported_table_path)

            imported_file = np.loadtxt(imported_table_path, delimiter=",")
            imported_filename = basename(imported_table_path)

            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum "
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([window_title_1, title, message])
                lineEdit.setFocus()
                return None, None

            imported_values = imported_file[:, 1] + 1j * imported_file[:, 2]
            self.frequencies = imported_file[:, 0]
        
            if app().project.model.change_analysis_frequency_setup(list(self.frequencies)):

                self.lineEdit_reset(lineEdit)

                title = "Project frequency setup cannot be modified"
                message = f"The following imported table of values has a frequency setup\n"
                message += "different from the others already imported ones. The current\n"
                message += "project frequency setup is not going to be modified."
                message += f"\n\n{imported_filename}"
                PrintMessageInput([window_title_1, title, message])
                return None, None

            # else:

            #     f_min = self.frequencies[0]
            #     f_max = self.frequencies[-1]
            #     f_step = self.frequencies[1] - self.frequencies[0] 

            #     frequency_setup = { "f_min" : f_min,
            #                         "f_max" : f_max,
            #                         "f_step" : f_step }

            #     app().project.model.set_frequency_setup(frequency_setup)

            return imported_values, imported_table_path

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
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

        table_name = f"external_load_{load_label}_from_{selection[:-1]}_{selected_id}"

        real_values = np.real(values)
        imag_values = np.imag(values)
        data = np.array([self.frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("structural", table_name, data)
        self.update_analysis_setup_in_file(self.frequencies)

        return table_name, data

    # def save_table_values(self, table_name: str, imported_values: np.ndarray):

    #     mask = imported_values[:, 0] > 0
    #     _imported_values = imported_values[mask, :]
    #     _frequencies = _imported_values[:, 0]

    #     if app().project.model.change_analysis_frequency_setup(list(_frequencies)):
    #         self.hide()
    #         title = "Project frequency setup cannot be modified"
    #         message = "The following imported table of values has a frequency setup "
    #         message += "different from the others already imported ones. The current "
    #         message += "project frequency setup is not going to be modified."
    #         message += f"\n\n{table_name}"
    #         PrintMessageInput([window_title_1, title, message])
    #         return True

    #     self.update_analysis_setup_in_file(_frequencies)

    #     real_values = _imported_values[:, 1]
    #     imag_values = _imported_values[:, 2]

    #     data = np.array([_frequencies, real_values, imag_values], dtype=float).T

    #     self.properties.add_imported_tables("acoustic", table_name, data)

    #     return False

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

        app().project.set_analysis_data(analysis_setup)
        app().file.write_analysis_setup_in_file(analysis_setup)

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

        selected_ids = app().project.model.mesh.check_selected_ids(
                                                                   input_ids, 
                                                                   selection = selection
                                                                   )

        if selected_ids is None:
            self.lineEdit_selection_id.setFocus()
            return

        self.remove_duplicated_attributions(selected_ids, selection)
        self.remove_conflicting_excitations(selected_ids, selection)

        if self.comboBox_element_type.currentIndex() == 0:
            element_type = "2d_element"
        else:
            element_type = "3d_element"

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

        nodal_attribution = bool(self.comboBox_load_distribution_table_values.currentIndex())
        key_avg = self.checkBox_averaged_table_values.isChecked()

        for selected_id in selected_ids:
            
            if self.Fx_table_values is not None:
                self.Fx_table_name, self.Fx_array = self.save_table_files("Fx", selected_id, selection, self.Fx_table_values, self.Fx_table_path)

            if self.Fy_table_values is not None:
                self.Fy_table_name, self.Fy_array = self.save_table_files("Fy", selected_id, selection, self.Fy_table_values, self.Fy_table_path)

            if self.Fz_table_values is not None:
                self.Fz_table_name, self.Fz_array = self.save_table_files("Fz", selected_id, selection, self.Fz_table_values, self.Fz_table_path)

            table_names = [self.Fx_table_name, self.Fy_table_name, self.Fz_table_name]
            table_paths = [self.Fx_table_path, self.Fy_table_path, self.Fz_table_path]
            external_loads = [self.Fx_table_values, self.Fy_table_values, self.Fz_table_values]

            if self.comboBox_element_type.currentIndex() == 0:

                if self.Mx_table_values is not None:
                    self.Mx_table_name, self.Mx_array = self.save_table_files("Mx", selected_id, selection, self.Mx_table_values, self.Mx_table_path)

                if self.My_table_values is not None:
                    self.My_table_name, self.Mx_array = self.save_table_files("My", selected_id, selection, self.My_table_values, self.My_table_path)

                if self.Mz_table_values is not None:
                    self.Mz_table_name, self.Mx_array = self.save_table_files("Mz", selected_id, selection, self.Mz_table_values, self.Mz_table_path)

                table_names.extend([self.Mx_table_name, self.My_table_name, self.Mz_table_name])
                table_paths.extend([self.Mx_table_path, self.My_table_path, self.Mz_table_path])
                external_loads.extend([self.Mx_table_values, self.My_table_values, self.Mz_table_values])

            condition_1 = self.comboBox_element_type.currentIndex() == 0 and table_names.count(None) == 6
            condition_2 = self.comboBox_element_type.currentIndex() == 1 and table_names.count(None) == 3

            if condition_1 or condition_2:
                title = "Additional inputs required"
                message = "It is necessary to enter at least one external load "
                message += "before confirming the property assignment."
                PrintMessageInput([window_title_1, title, message]) 
                return

            data = {
                    "element_type" : element_type,
                    "table_names" : table_names,
                    "table_paths" : table_paths,
                    "values" : external_loads,
                    "nodal_attribution": nodal_attribution,
                    "averaged": key_avg,
                    }

            if attribution_type == 0:
                self.properties._set_property("external_loads", data, surface=selected_id)

            elif attribution_type == 1:
                self.properties._set_property("external_loads", data, line=selected_id)

            elif attribution_type == 2:
                self.properties._set_property("external_loads", data, point=selected_id)

            elif attribution_type == 3:
                self.properties._set_property("external_loads", data, node=selected_id)

        self.actions_to_finalize()

    def remove_duplicated_attributions(self, selected_ids: list, selection: str):

        table_names = list()
        nodes_to_remove = list()
        for selected_id in selected_ids:

            if selection == "surfaces":

                nodes_from_surface = self.model.mesh.nodes_from_surfaces[selected_id]
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "external_loads" and node_id in nodes_from_surface:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for line_id in app().project.model.mesh.lines_from_surface[selected_id]:
                    data = self.properties._get_property("external_loads", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("external_loads", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("external_loads", line_id, "lines"))

                    for point_id in app().project.model.mesh.points_from_line[line_id]:
                        data = self.properties._get_property("external_loads", point=point_id)
                        if isinstance(data, dict):
                            self.properties._remove_point_property("external_loads", point_id)
                            table_names.extend(self.properties.get_property_related_table_names("external_loads", point_id, "points"))

            elif selection == "lines":

                nodes_from_line = self.model.mesh.nodes_from_lines[selected_id]
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "external_loads" and node_id in nodes_from_line:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for surface_id in app().project.model.mesh.surface_from_line[selected_id]:
                    data = self.properties._get_property("external_loads", surface=surface_id)
                    if isinstance(data, dict):
                        self.properties._remove_surface_property("external_loads", surface_id)
                        table_names.extend(self.properties.get_property_related_table_names("external_loads", surface_id, "surfaces"))

                for point_id in app().project.model.mesh.points_from_line[selected_id]:
                    data = self.properties._get_property("external_loads", point=point_id)
                    if isinstance(data, dict):
                        self.properties._remove_point_property("external_loads", point_id)
                        table_names.extend(self.properties.get_property_related_table_names("external_loads", point_id, "points"))

            elif selection == "points":

                nodes_from_point = self.model.mesh.nodes_from_points[selected_id]
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "external_loads" and node_id in nodes_from_point:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for line_id in app().project.model.mesh.line_from_point[selected_id]:
                    data = self.properties._get_property("external_loads", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("external_loads", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("external_loads", line_id, "lines"))

                    for surface_id in self.model.mesh.surface_from_line[line_id]:
                        data = self.properties._get_property("external_loads", surface=surface_id)
                        if isinstance(data, dict):
                            self.properties._remove_surface_property("external_loads", surface_id)
                            table_names.extend(self.properties.get_property_related_table_names("external_loads", surface_id, "surfaces"))

            elif selection == "nodes":

                point_id = selected_id + 1
                data = self.properties._get_property("external_loads", point=point_id)
                if isinstance(data, dict):
                    self.properties._remove_point_property("external_loads", point_id)
                    table_names.extend(self.properties.get_property_related_table_names("external_loads", point_id, "points"))

                for line_id in app().project.model.mesh.line_from_point[point_id]:
                    data = self.properties._get_property("external_loads", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("external_loads", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("external_loads", line_id, "lines"))

                    for surface_id in self.model.mesh.surface_from_line[line_id]:
                        data = self.properties._get_property("external_loads", surface=surface_id)
                        if isinstance(data, dict):
                            self.properties._remove_surface_property("external_loads", surface_id)
                            table_names.extend(self.properties.get_property_related_table_names("external_loads", surface_id, "surfaces"))

            for node_id in nodes_to_remove:
                self.properties._remove_nodal_property("external_loads", node_id)
                table_names.extend(self.properties.get_property_related_table_names("external_loads", node_id, "nodes"))

            self.process_table_file_removal(table_names)

    def attribute_callback(self):
        index = self.tabWidget_main.currentIndex()
        if index == 0:
            self.constant_values_attribution()
        elif index == 1:
            self.table_values_attribution()

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

    def load_model_info(self):

        self.treeWidget_external_loads.clear()
        for (property, *args), data in self.properties.surface_properties.items():

            if property == "external_loads":
                values = data["values"]
                constrained_loads_mask = [False if value is None else True for value in values]
                new = QTreeWidgetItem([str(args[0]), "Surface", str(self.text_label(constrained_loads_mask))])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_external_loads.addTopLevelItem(new)

        for (property, *args), data in self.properties.line_properties.items():

            if property == "external_loads":
                values = data["values"]
                constrained_loads_mask = [False if value is None else True for value in values]
                new = QTreeWidgetItem([str(args[0]), "Line", str(self.text_label(constrained_loads_mask))])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_external_loads.addTopLevelItem(new)

        for (property, *args), data in self.properties.point_properties.items():

            if property == "external_loads":
                values = data["values"]
                constrained_loads_mask = [False if value is None else True for value in values]
                new = QTreeWidgetItem([str(args[0]), "Point", str(self.text_label(constrained_loads_mask))])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_external_loads.addTopLevelItem(new)

        for (property, *args), data in self.properties.nodal_properties.items():

            if property == "external_loads":
                values = data["values"]
                constrained_loads_mask = [False if value is None else True for value in values]
                new = QTreeWidgetItem([str(args[0]), "Node", str(self.text_label(constrained_loads_mask))])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_external_loads.addTopLevelItem(new)

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
                if property == "external_loads":
                    self.tabWidget_main.setTabVisible(2, True)
                    return

        self.tabWidget_main.setTabVisible(2, False)
        self.tabWidget_main.setCurrentIndex(0)
        self.lineEdit_real_Fx.setFocus()
        app().main_window.set_geometry_selection()

    def tab_event_callback(self):

        if self.tabWidget_main.currentIndex() == 3:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_attribute.setDisabled(True)

        else:

            text = self.lineEdit_selection_id.text()
            if " - " in text:
                selected_id = text.split(" - ")[1]
                self.lineEdit_selection_id.setText(selected_id)

            self.lineEdit_selection_id.setDisabled(False)
            self.pushButton_attribute.setEnabled(True)

    def update_controls_for_constant_values(self):
        key = bool(self.comboBox_load_distribution_constant_values.currentIndex())
        self.checkBox_averaged_constant_values.setChecked(key)
        self.checkBox_averaged_constant_values.setEnabled(key)

    def update_controls_for_table_values(self):
        key = bool(self.comboBox_load_distribution_table_values.currentIndex())
        self.checkBox_averaged_table_values.setChecked(key)
        self.checkBox_averaged_table_values.setEnabled(key)

    def on_click_item(self, item):

        selected_id = item.text(0)
        selection = item.text(1)
        self.pushButton_remove.setDisabled(False)

        if selection != "":

            text = f"{selection} - {selected_id}"

            if selection == "Surface":
                app().main_window.set_geometry_selection(surfaces = [int(selected_id)])

            elif selection == "Line":
                app().main_window.set_geometry_selection(lines = [int(selected_id)])

            elif selection == "Point":
                app().main_window.set_geometry_selection(points = [int(selected_id)])

            elif selection == "Node":
                app().main_window.set_mesh_selection(nodes=[int(selected_id)])

            if selection == "Node":
                app().main_window.viewer_tabs.show_mesh()

            else:
                app().main_window.viewer_tabs.show_geometry()

            self.lineEdit_selection_id.setText(text)

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

        properties = ["external_load", "prescribed_dofs"]

        for selected_id in selected_ids:
            for property in properties:
                table_names = self.properties.get_property_related_table_names(property, selected_id, selection)
                remove_function(property, selected_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from(self, selected_id : list, selection: str):
        table_names = self.properties.get_property_related_table_names("external_loads", selected_id, selection)
        self.process_table_file_removal(table_names)

    def remove_callback(self):

        text = self.lineEdit_selection_id.text()

        if text != "" and " - " in text:

            selection, _selected_id = text.split(" - ")
            selected_id = int(_selected_id)

            if selection == "Surface":
                self.properties._remove_surface_property("external_loads", selected_id)

            elif selection == "Line":
                self.properties._remove_line_property("external_loads", selected_id)

            elif selection == "Point":
                self.properties._remove_point_property("external_loads", selected_id)

            elif selection == "Node":
                self.properties._remove_nodal_property("external_loads", selected_id)

            self.remove_table_files_from(selected_id, f"{selection.lower()}s")
            self.actions_to_finalize()

            app().main_window.set_geometry_selection()
            app().main_window.set_mesh_selection()

    def reset_callback(self):

        self.hide()

        title = "Prescribed DOFs resetting"
        message = "Would you like to remove the all prescribed DOFs from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if obj._cancel:
            return

        if obj._continue:

            for (property, *args) in self.properties.surface_properties.keys():
                if property == "external_loads":
                    self.remove_table_files_from(args[0], "surfaces")

            for (property, *args) in self.properties.line_properties.keys():
                if property == "external_loads":
                    self.remove_table_files_from(args[0], "lines")

            for (property, *args) in self.properties.point_properties.keys():
                if property == "external_loads":
                    self.remove_table_files_from(args[0], "points")

            for (property, *args) in self.properties.nodal_properties.keys():
                if property == "external_loads":
                    self.remove_table_files_from(args[0], "nodes")

            self.properties._reset_property("external_loads")
            self.actions_to_finalize()

            app().main_window.set_geometry_selection()
            app().main_window.set_mesh_selection()

    def actions_to_finalize(self):
        self.load_model_info()
        self.reset_input_fields()
        app().main_window.viewer_tabs.update_info_text()
        app().file.write_model_properties_in_file()
        app().file.write_imported_table_data_in_file()
        # app().main_window.viewer_tabs.mesh_widget.symbols_actor.build()

    def change_frequency_setup(self):
        if self.imported_values is not None:
            self.hide()
            obj = ChangeFrequencyDataRangeInput(self.imported_values)
            if obj.filter_data is not None:
                self.imported_values = obj.filter_data

    def check_model_frequency_controls(self):

        for key, data in self.properties.surface_properties.items():
            property, _ = key
            if property in ["external_load", "prescribed_dofs"]:
                if "table_names" in data.keys():
                    return

        if isinstance(app().project.analysis_data, dict):
            analysis_data = app().project.analysis_data
            app().project.set_analysis_data(analysis_data)
            app().file.write_analysis_setup_in_file(analysis_data)

    def reset_input_fields(self):

        self.lineEdit_selection_id.setText("")

        for lineEdit_real, lineEdit_imag in self.list_lineEdit_constant_values:
            lineEdit_real.setText("")
            lineEdit_imag.setText("")

        for lineEdit_table in self.list_lineEdit_table_values:
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