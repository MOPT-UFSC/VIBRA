import os
from math import pi
from pathlib import Path

import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vibra import app, UI_DIR
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.model_inputs.data_filter.change_frequency_data_handler import ChangeFrequencyDataRangeInput
from vibra.interface.general.print_message_input import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"


class PrescribedDofsInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/prescribed_dofs_input.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.project = app().project
        self.model = self.project.model
        self.properties = app().project.model.properties

        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        self._config_widgets()
        self.geometry_selection_callback()
        self.load_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Set boundary condition")

    def _initialize(self):

        self.keep_window_open = True

        # self.list_Nones = [None, None, None]
        self.list_Nones = [None, None, None, None, None, None]
        self.dofs_labels = np.array(['Ux','Uy','Uz','Rx','Ry','Rz'])

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

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_angular_data_type: QComboBox
        self.comboBox_element_type: QComboBox
        self.comboBox_linear_data_type: QComboBox
        self.comboBox_selection_type: QComboBox

        # QLineEdit
        self.lineEdit_selection_id: QLineEdit
        self.lineEdit_real_ux: QLineEdit
        self.lineEdit_real_uy: QLineEdit
        self.lineEdit_real_uz: QLineEdit
        self.lineEdit_real_rx: QLineEdit
        self.lineEdit_real_ry: QLineEdit
        self.lineEdit_real_rz: QLineEdit
        self.lineEdit_real_alldofs: QLineEdit
        #
        self.lineEdit_imag_ux: QLineEdit
        self.lineEdit_imag_uy: QLineEdit
        self.lineEdit_imag_uz: QLineEdit
        self.lineEdit_imag_rx: QLineEdit
        self.lineEdit_imag_ry: QLineEdit
        self.lineEdit_imag_rz: QLineEdit
        #
        self.lineEdit_imag_alldofs: QLineEdit
        self.lineEdit_path_table_ux: QLineEdit
        self.lineEdit_path_table_uy: QLineEdit
        self.lineEdit_path_table_uz: QLineEdit
        self.lineEdit_path_table_rx: QLineEdit
        self.lineEdit_path_table_ry: QLineEdit
        self.lineEdit_path_table_rz: QLineEdit
        #
        self._create_list_lineEdits()

        # QPushButton
        self.pushButton_attribute: QPushButton
        self.pushButton_exit: QPushButton
        self.pushButton_load_ux_table: QPushButton
        self.pushButton_load_uy_table: QPushButton
        self.pushButton_load_uz_table: QPushButton
        self.pushButton_load_rx_table: QPushButton
        self.pushButton_load_ry_table: QPushButton
        self.pushButton_load_rz_table: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_prescribed_dofs: QTreeWidget

    def _create_list_lineEdits(self):
        self.list_lineEdit_constant_values = [  [self.lineEdit_real_ux, self.lineEdit_imag_ux],
                                                [self.lineEdit_real_uy, self.lineEdit_imag_uy],
                                                [self.lineEdit_real_uz, self.lineEdit_imag_uz],
                                                [self.lineEdit_real_rx, self.lineEdit_imag_rx],
                                                [self.lineEdit_real_ry, self.lineEdit_imag_ry],
                                                [self.lineEdit_real_rz, self.lineEdit_imag_rz]  ]

        self.list_lineEdit_table_values = [ self.lineEdit_path_table_ux,
                                            self.lineEdit_path_table_uy,
                                            self.lineEdit_path_table_uz,
                                            self.lineEdit_path_table_rx,
                                            self.lineEdit_path_table_ry,
                                            self.lineEdit_path_table_rz ]

    def _config_widgets(self):
        #
        for i, w in enumerate([80, 60]):
            self.treeWidget_prescribed_dofs.setColumnWidth(i, w)
            self.treeWidget_prescribed_dofs.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
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


    def geometry_selection_callback(self):

        self.reset_input_fields()
        faces = app().main_window.selected_geometry_surfaces

        if faces:

            # self.comboBox_attribution_type.setCurrentIndex(1)

            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)

            if len(faces) == 1:
                surface_id = list(faces)[0]

                data = self.properties._get_property("prescribed_dofs", surface=surface_id)
                if isinstance(data, dict):

                    values = data.get("values", None)

                    if "table_paths" in data.keys():
                        table_paths = data["table_paths"]
                        for index, lineEdit_table in enumerate(self.list_lineEdit_table_values):
                            table_path = table_paths[index]
                            if table_path is not None:                   
                                lineEdit_table.setText(table_path)

                    else:
                        for index, [lineEdit_real, lineEdit_imag] in enumerate(self.list_lineEdit_constant_values):
                            if values[index] is not None:
                                lineEdit_real.setText(str(np.real(values[index])))
                                lineEdit_imag.setText(str(np.imag(values[index])))

    def element_type_callback(self):

        key = self.comboBox_element_type.currentIndex() == 0

        self.lineEdit_real_rx.setEnabled(key)
        self.lineEdit_real_ry.setEnabled(key)
        self.lineEdit_real_rz.setEnabled(key)

        self.lineEdit_imag_rx.setEnabled(key)
        self.lineEdit_imag_ry.setEnabled(key)
        self.lineEdit_imag_rz.setEnabled(key)

        self.pushButton_load_rx_table.setEnabled(key)
        self.pushButton_load_ry_table.setEnabled(key)
        self.pushButton_load_rz_table.setEnabled(key)

    def check_complex_entries(self, real_input: str, imag_input: str, label: str):

        _real = None
        if real_input != "":
            try:
                _real = float(real_input)

            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([window_title_1, title, message])
                real_input.setFocus()
                return True, None

        _imag = None
        if imag_input != "":
            try:
                _imag = float(imag_input)

            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for imaginary part of {label}."
                PrintMessageInput([window_title_1, title, message])
                imag_input.setFocus()
                return True, None

        if _real is None and _imag is None:
            values = None
        elif _real is None:
            values = 1j * _imag
        elif _imag is None:
            values = complex(_real)
        else:
            values = _real + 1j * _imag

        if label == "all_dofs":
            if self.comboBox_element_type.currentIndex() == 0:
                output = [values, values, values, values, values, values]
            else:
                output = [values, values, values]
        else:
            output = values

        return False, output

    def constant_values_attribution(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_ids = self.model.mesh.check_selected_ids(
                                                         input_ids, 
                                                         selection = "surfaces"
                                                         )

        if surface_ids is None:
            self.lineEdit_selection_id.setFocus()
            return

        if self.lineEdit_real_alldofs.text() != "" or self.lineEdit_imag_alldofs.text() != "":
            stop, prescribed_dofs = self.check_complex_entries(self.lineEdit_real_alldofs.text(), self.lineEdit_imag_alldofs.text(), "all_dofs")
            if stop:
                return

        else:

            stop, ux= self.check_complex_entries(self.lineEdit_real_ux.text(), self.lineEdit_imag_ux.text(), "ux")
            if stop:
                return

            stop, uy= self.check_complex_entries(self.lineEdit_real_uy.text(), self.lineEdit_imag_uy.text(), "uy")
            if stop:
                return

            stop, uz= self.check_complex_entries(self.lineEdit_real_uz.text(), self.lineEdit_imag_uz.text(), "uz")
            if stop:
                return

            element_type = "solid_element"
            prescribed_dofs = [ux, uy, uz]

            if self.comboBox_element_type.currentIndex() == 0:
             
                stop, rx= self.check_complex_entries(self.lineEdit_real_rx.text(), self.lineEdit_imag_rx.text(), "rx")
                if stop:
                    return

                stop, ry= self.check_complex_entries(self.lineEdit_real_ry.text(), self.lineEdit_imag_ry.text(), "ry")
                if stop:
                    return

                stop, rz= self.check_complex_entries(self.lineEdit_real_rz.text(), self.lineEdit_imag_rz.text(), "rz")
                if stop:
                    return
                
                element_type = "face_element"
                prescribed_dofs.extend([rx, ry, rz])

        condition_1 = self.comboBox_element_type.currentIndex() == 0 and prescribed_dofs.count(None) == 6
        condition_2 = self.comboBox_element_type.currentIndex() == 1 and prescribed_dofs.count(None) == 3

        if condition_1 or condition_2:

            self.remove_conflicting_excitations(surface_ids)

            real_values = [value if value is None else np.real(value) for value in prescribed_dofs]
            imag_values = [value if value is None else np.imag(value) for value in prescribed_dofs]

            for surface_id in surface_ids:

                data = {
                        "element_type" : element_type,
                        "values" : prescribed_dofs,
                        "real_values" : real_values,
                        "imag_values" : imag_values
                        }

                self.model.properties._set_property("prescribed_dofs", data, surface=surface_id)

            self.actions_to_finalize()

            print(f"[Set Prescribed DOF] - defined at surface(s) {surface_ids}")  

        else:
            title = "Additional inputs required"
            message = "You must inform at least one prescribed dof\n"
            message += "before confirming the input!"
            PrintMessageInput([window_title_1, title, message])

    def load_table(self, lineEdit : QLineEdit, dof_label : str, direct_load = False):

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

                caption = f"Choose a table to import the {dof_label} nodal load"
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
            imported_filename = os.path.basename(imported_table_path)

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

    def integrate_and_save_table_files(self, dof_label: str, node_id: int, values: np.ndarray, linear=False, angular=False):

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

        table_name = f"prescribed_dof_{dof_label}_node_{node_id}"

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
        surface_ids = self.model.mesh.check_selected_ids(
                                                         input_ids, 
                                                         selection = "surfaces"
                                                         )

        if surface_ids is None:
            self.lineEdit_selection_id.setFocus()
            return

        self.remove_conflicting_excitations(surface_ids)

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

        for surface_id in surface_ids:
            
            if self.ux_table_values is not None:
                self.ux_table_name, self.ux_array = self.integrate_and_save_table_files("Ux", surface_id, self.ux_table_values, self.ux_table_path, linear = True)

            if self.uy_table_values is not None:
                self.uy_table_name, self.uy_array = self.integrate_and_save_table_files("Uy", surface_id, self.uy_table_values, self.uy_table_path, linear = True)

            if self.uz_table_values is not None:
                self.uz_table_name, self.uz_array = self.integrate_and_save_table_files("Uz", surface_id, self.uz_table_values, self.uz_table_path, linear = True)

            element_type = "solid_element"
            table_names = [self.ux_table_name, self.uy_table_name, self.uz_table_name]
            table_paths = [self.ux_table_path, self.uy_table_path, self.uz_table_path]
            prescribed_dofs = [self.ux_table_values, self.uy_table_values, self.uz_table_values]

            if self.comboBox_element_type.currentIndex() == 0:

                if self.rx_table_values is not None:
                    self.rx_table_name, self.rx_array = self.integrate_and_save_table_files("Rx", surface_id, self.rx_table_values, self.rx_table_path, angular = True)

                if self.ry_table_values is not None:
                    self.ry_table_name, self.rx_array = self.integrate_and_save_table_files("Ry", surface_id, self.ry_table_values, self.ry_table_path, angular = True)

                if self.rz_table_values is not None:
                    self.rz_table_name, self.rx_array = self.integrate_and_save_table_files("Rz", surface_id, self.rz_table_values, self.rz_table_path, angular = True)

                element_type = "face_element"
                table_names.extend([self.rx_table_name, self.ry_table_name, self.rz_table_name])
                table_paths.extend([self.rx_table_path, self.ry_table_path, self.rz_table_path])
                prescribed_dofs.extend([self.rx_table_values, self.ry_table_values, self.rz_table_values])

            condition_1 = self.comboBox_element_type.currentIndex() == 0 and table_names.count(None) == 6
            condition_2 = self.comboBox_element_type.currentIndex() == 1 and table_names.count(None) == 3

            if condition_1 or condition_2:
                title = "Additional inputs required"
                message = "You must inform at least one prescribed dof "
                message += "table path before confirming the input!"
                PrintMessageInput([window_title_1, title, message]) 
                return 

            data = {
                    "element_type" : element_type,
                    "table_names" : table_names,
                    "table_paths" : table_paths,
                    "values" : prescribed_dofs
                    }

            self.properties._set_property("prescribed_dofs", data, surface=surface_id)

        self.actions_to_finalize()

        print(f"[Set Prescribed DOF] - defined at node(s) {surface_ids}")

    def attribute_callback(self):
        index = self.tabWidget_main.currentIndex()
        if index == 0:
            self.constant_values_attribution()
        elif index == 1:
            self.table_values_attribution()

    def text_label(self, mask):

        text = ""
        labels = self.dofs_labels[mask]

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

    def load_info(self):

        self.treeWidget_prescribed_dofs.clear()
        for (property, *args), data in self.properties.surface_properties.items():

            if property == "prescribed_dofs":
                values = data["values"]
                constrained_dofs_mask = [False if value is None else True for value in values]
                new = QTreeWidgetItem([str(args[0]), str(self.text_label(constrained_dofs_mask))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_prescribed_dofs.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        for (property, _) in self.properties.surface_properties.keys():
            if property == "prescribed_dofs":
                self.tabWidget_main.setTabVisible(2, True)
                return

        self.tabWidget_main.setTabVisible(2, False)

    def tab_event_callback(self):

        if self.tabWidget_main.currentIndex() == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_attribute.setDisabled(True)

        else:
            self.lineEdit_selection_id.setDisabled(False)
            self.pushButton_attribute.setEnabled(True)

    def on_click_item(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            surface_id = int(item.text(0))
            self.lineEdit_selection_id.setText(item.text(0))
            app().main_window.set_geometry_selection(surfaces=[surface_id])

    def on_double_click_item(self, item):
        self.on_click_item(item)

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().file.write_imported_table_data_in_file()

    def remove_conflicting_excitations(self, surface_ids: int | list):

        if isinstance(surface_ids, int):
            surface_ids = [surface_ids]

        labels = ["prescribed_dofs", "external_load"]

        for surface_id in surface_ids:
            for label in labels:
                table_names = self.properties.get_surface_related_table_names(label, surface_id)
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_id : list):
        table_names = self.properties.get_surface_related_table_names("acoustic_pressure", surface_id)
        self.process_table_file_removal(table_names)

    def remove_callback(self):

        if self.lineEdit_selection_id.text() != "":

            surface_id = int(self.lineEdit_selection_id.text())

            self.properties._remove_surface_property("surface_thickness", surface_id)
            self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Surface thickness resetting"
        message = "Would you like to remove the all applied surface thickness from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            surface_ids = list()
            for (property, *args) in self.properties.surface_properties.keys():
                if property == "surface_thickness":

                    surface_id = args[0]
                    surface_ids.append(surface_id)

            self.properties._reset_property("surface_thickness")
            self.actions_to_finalize()

    def actions_to_finalize(self):
        self.load_info()
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
            if property in ["prescribed_dofs", "external_load"]:
                if "table_names" in data.keys():
                    return

        if isinstance(self.project.analysis_data, dict):
            analysis_data = self.project.analysis_data
            self.project.set_analysis_data(analysis_data)
            app().file.write_analysis_setup_in_file(analysis_data)

    def reset_input_fields(self):
        self.lineEdit_selection_id.setText("")
        for [lineEdit_real, lineEdit_imag] in self.list_lineEdit_constant_values:
            lineEdit_real.setText("")
            lineEdit_imag.setText("")
        for lineEdit_table in self.list_lineEdit_table_values:
            lineEdit_table.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)