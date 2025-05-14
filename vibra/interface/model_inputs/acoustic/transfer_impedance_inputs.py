from PySide6.QtWidgets import QComboBox, QDialog, QFileDialog, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app, UI_DIR
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow

from molde import load_ui
from copy import deepcopy

import os, warnings
import numpy as np

# fmt: off

window_title_1 = "Error"
window_title_2 = "Warning"

class TransferImpedanceInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/transfer_impedance_inputs.ui"
        load_ui(ui_path, self, ui_path.parent)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.action_model_workspace_callback()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._define_qt_variables()
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
        self.imported_values = None
        self.setup_complete = False
        self.keep_window_open = True
        self.transfer_impedance_data = dict()

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_selection_type : QComboBox

        # QLineEdit
        self.lineEdit_selection_id : QLineEdit
        self.lineEdit_real_value : QLineEdit
        self.lineEdit_imag_value : QLineEdit
        self.lineEdit_table_path : QLineEdit

        # QPushButton
        self.pushButton_attribute : QPushButton
        self.pushButton_exit : QPushButton
        self.pushButton_change_frequency_setup : QPushButton
        self.pushButton_load_table : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton
        #
        self.pushButton_change_frequency_setup.setDisabled(True)

        # QTabWidget
        self.tabWidget_main : QTabWidget

        # QTreeWidget
        self.treeWidget_transfer_impedance : QTreeWidget
        self.treeWidget_transfer_impedance.setColumnWidth(1, 20)
        self.treeWidget_transfer_impedance.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_load_table.clicked.connect(self.load_transfer_impedance_table)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tabEvent_callback)
        #
        self.treeWidget_transfer_impedance.itemClicked.connect(self.on_click_item)
        self.treeWidget_transfer_impedance.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)

    def _config_widgets(self):
        for i, w in enumerate([120]):
            self.treeWidget_transfer_impedance.setColumnWidth(i, w)
            self.treeWidget_transfer_impedance.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def geometry_selection_callback(self):

        surfaces = self.main_window.selected_geometry_surfaces

        if surfaces:

            if len(surfaces) == 1:
                surface_ids = int(list(surfaces)[0])
            elif len(surfaces) == 2:
                surface_ids = tuple(surfaces)
            else:
                return

            self.update_selection_type_based_on_surface_ids(surface_ids)
            pp_data = self.properties._get_property("transfer_impedance", surface=surface_ids)
            if pp_data is None:
                return

            self.load_property_data(pp_data)

    def update_selection_type_based_on_surface_ids(self, surface_ids: int | tuple[int]):

        if isinstance(surface_ids, int | np.int64):
            if len(self.mesh.volumes_from_surface[surface_ids]) == 2:
                self.update_selected_ids(surface_ids)
                self.comboBox_selection_type.setCurrentIndex(0)

        elif isinstance(surface_ids, tuple):
            if len(surface_ids) == 2:
                volumes_from_surface_A = self.mesh.volumes_from_surface[surface_ids[0]]
                volumes_from_surface_B = self.mesh.volumes_from_surface[surface_ids[1]]
                if len(volumes_from_surface_A) == len(volumes_from_surface_B) == 1:
                    self.update_selected_ids(surface_ids)
                    self.comboBox_selection_type.setCurrentIndex(1)

        else:
            return

    def update_selected_ids(self, surface_ids: int | tuple[int]):

        if isinstance(surface_ids, int | np.int64):
            surface_ids = [surface_ids]

        text = ", ".join([str(i) for i in surface_ids])
        self.lineEdit_selection_id.setText(text)

    def load_property_data(self, pp_data: dict):

        if self.tabWidget_main.currentIndex() == 2:
            return

        if isinstance(pp_data, dict):
            if "table_paths" in pp_data.keys():
                self.tabWidget_main.setCurrentIndex(1)
                self.lineEdit_table_path.setText(pp_data["table_paths"][0])
            else:
                self.tabWidget_main.setCurrentIndex(0)
                self.lineEdit_real_value.setText(str(pp_data["real_values"][0]))
                self.lineEdit_imag_value.setText(str(pp_data["imag_values"][0]))

    def check_selected_surfaces(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_ids = self.mesh.check_selected_ids(
                                                    input_ids, 
                                                    selection = "surfaces", 
                                                    single_id = False,
                                                    )

        if surface_ids is None:
            self.lineEdit_selection_id.setFocus()
            return None

        if self.check_selection_type(surface_ids):
            return None

        if not self.transfer_impedance_data:
            return None
        
        return surface_ids

    def attribute_callback(self):

        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == 2:
            return

        surface_ids = self.check_selected_surfaces()
        if surface_ids is None:
            return
        
        self.remove_conflicting_excitations(surface_ids)

        if tab_index == 0:
            self.process_assignment_for_constant_values(surface_ids)

        elif tab_index == 1:
            self.process_assignment_for_table_values(surface_ids)

    def check_complex_entries(self, lineEdit_real, lineEdit_imag):
        self.stop = False
        title = "Invalid entry to the specific impedance"
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                message = "Wrong input for real part of specific impedance."
                PrintMessageInput([window_title_1, title, message])
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
                PrintMessageInput([window_title_1, title, message])
                self.lineEdit_imag_value.setFocus()
                self.stop = True
                return
        else:
            imag_F = 0

        if real_F == 0 and imag_F == 0:
            return None
        else:
            return real_F + 1j * imag_F

    def process_assignment_for_constant_values(self, surface_ids: int | tuple[int]):

        transfer_impedance = self.check_complex_entries(
                                                        self.lineEdit_real_value, 
                                                        self.lineEdit_imag_value
                                                        )

        if transfer_impedance is None:
            self.hide()
            title = "Additional inputs required"
            message = "You must enter the transfer impedance to "
            message += "proceed with the attribution."
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_real_value.setFocus()
            return

        real_values = [np.real(transfer_impedance)]
        imag_values = [np.imag(transfer_impedance)]

        self.transfer_impedance_data.update({
                                            "real_values" : real_values,
                                            "imag_values" : imag_values,
                                            })

        if self.transfer_impedance_data.get("coupling_type") == "inside_surfaces":
            for surface_id in surface_ids:
                self.properties._set_property("transfer_impedance",self.transfer_impedance_data, surface=surface_id)
                self.decouple_degrees_of_freedom(surface_id)

        else:
            self.properties._set_property("transfer_impedance",self.transfer_impedance_data, surface=tuple(surface_ids))

        self.setup_complete = True
        self.actions_to_finalize()

    def load_table(self, lineEdit : QLineEdit, direct_load=False):

        title = "Error reached while loading 'specific impedance' table"

        try:
            if direct_load:
                imported_table_path = lineEdit.text()

            else:

                last_path = app().config.get_last_folder_for("imported_table_folder")
                if last_path is None:
                    path = os.path.expanduser("~")
                else:
                    path = last_path

                caption = "Choose a table to import the specific impedance"
                imported_table_path, check = QFileDialog.getOpenFileName( 
                                                                        None, 
                                                                        caption, 
                                                                        path, 
                                                                        "Files (*.csv; *.dat; *.txt)"
                                                                        )

                if not check:
                    return None

            lineEdit.setText(imported_table_path)
            imported_file = np.loadtxt(imported_table_path, delimiter=",")

            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have three columns in the form: frequencies, real and imaginary values."
                PrintMessageInput([window_title_1, title, message])
                return None

            return imported_file

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
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
            PrintMessageInput([window_title_1, title, message])
            return True

        self.update_analysis_setup_in_file(_frequencies)

        real_values = _imported_values[:, 1]
        imag_values = _imported_values[:, 2]

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

    def load_transfer_impedance_table(self):
        self.imported_values = self.load_table(self.lineEdit_table_path)

    def process_assignment_for_table_values(self, surface_ids: int | tuple[int]):

        if self.lineEdit_table_path.text() == "":
            self.hide()
            title = "Additional inputs required"
            message = "You must inform at least one specific impedance\n"
            message += "table path before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_table_path.setFocus()
            return

        if self.imported_values is None:
            self.imported_values = self.load_table( self.lineEdit_table_path, 
                                                    direct_load = True )
            
        if self.imported_values is None:
            return

        if self.transfer_impedance_data.get("coupling_type") == "inside_surfaces":
            for surface_id in surface_ids:
                self.include_transfer_impedance_table_data(surface_id)
                self.properties._set_property("transfer_impedance",self.transfer_impedance_data, surface=surface_id)
                self.decouple_degrees_of_freedom(surface_id)

        else:
            self.include_transfer_impedance_table_data(surface_ids)
            self.properties._set_property("transfer_impedance",self.transfer_impedance_data, surface=tuple(surface_ids))

        self.setup_complete = True
        self.actions_to_finalize()

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().file.write_imported_table_data_in_file()

    def remove_conflicting_excitations(self, surface_ids: int | list):

        if isinstance(surface_ids, int):
            surface_ids = [surface_ids]

        labels = ["transfer_impedance"]

        for surface_id in surface_ids:
            for label in labels:
                table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_id : list):
        table_names = self.properties.get_property_related_table_names("transfer_impedance", surface_id, "surfaces")
        self.process_table_file_removal(table_names)

    def tabEvent_callback(self):
        if self.tabWidget_main.currentIndex() == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_attribute.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)
            self.pushButton_attribute.setEnabled(True)

    def on_click_item(self, item):

        text = item.text(0).replace("(", "").replace(")", "").replace(",", "")
        str_surface_ids = text.split()

        surface_ids = [int(surf_id) for surf_id in str_surface_ids]
        app().main_window.set_geometry_selection(surfaces=surface_ids)

        self.lineEdit_selection_id.setText(item.text(0))
        self.pushButton_remove.setEnabled(True)

    def on_doubleclick_item(self, item):
        self.on_click_item(item)
                
    def clear_all_inputs(self):
        self.lineEdit_real_value.setText("")
        self.lineEdit_imag_value.setText("")
        self.lineEdit_table_path.setText("")

    def check_selection_type(self, surface_ids: list[int]):

        title = "Invalid selection detected"

        selection_type = self.comboBox_selection_type.currentText()
        if selection_type == "Inside surfaces":
            for surface_id in surface_ids:
                if len(self.mesh.volumes_from_surface[surface_id]) != 2:
                    self.hide()
                    message = f"The selected surface ID #{surface_id} does not correspond to an inside surface. "
                    message += "Inside surfaces are surfaces that connect two neighboohrs volumes. "
                    message += "The perforated plate attribution will be ignored until all requirements are met."
                    PrintMessageInput([window_title_1, title, message])
                    self.transfer_impedance_data.clear()
                    return True

        else:

            if len(surface_ids) != 2:
                self.hide()
                message = f"An invalid number of selected surfaces has been detected. To proceed, you must "
                message += "select a pair of outside surfaces. Outside surfaces are surfaces associated to only one volume. "
                message += "The perforated plate attribution will be ignored until all requirements are met."
                PrintMessageInput([window_title_1, title, message])
                self.transfer_impedance_data.clear()
                return True

            for surface_id in surface_ids:
                if len(self.mesh.volumes_from_surface[surface_id]) != 1:
                    self.hide()
                    message = f"The selected surface ID #{surface_id} does not correspond to an outside surface. "
                    message += "Outside surfaces are surfaces associated to only one volume. The perforated plate "
                    message += "attribution will be ignored until all requirements are met."
                    PrintMessageInput([window_title_1, title, message])
                    self.transfer_impedance_data.clear()
                    return True

        self.transfer_impedance_data["coupling_type"] = selection_type.lower().replace(" ", "_")

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
                self.tabWidget_main.setTabVisible(2, True)
                return

        self.tabWidget_main.setTabVisible(2, False)
        self.tabWidget_main.setCurrentIndex(0)

    def load_table(self, lineEdit : QLineEdit, direct_load: bool=False):

        title = "Error reached while loading 'acoustic pressure' table"

        try:
            if direct_load:
                imported_table_path = lineEdit.text()

            else:

                last_path = app().config.get_last_folder_for("imported_table_folder")
                if last_path is None:
                    path = os.path.expanduser("~")
                else:
                    path = last_path

                caption = "Choose a table to import the user-defined transfer impedance"
                imported_table_path, check = QFileDialog.getOpenFileName(  None, 
                                                                            caption, 
                                                                            path, 
                                                                            "Files (*.csv; *.dat; *.txt)"
                                                                        )

                if not check:
                    return None

            lineEdit.setText(imported_table_path)
            lineEdit.setToolTip(f"User-defined normalized transfer impedance table path: {imported_table_path}")
            app().config.write_last_folder_path_in_file("imported_table_folder", imported_table_path)

            imported_file = np.loadtxt(imported_table_path, delimiter=",")

            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have three columns in the form: frequencies, real and imaginary values."
                PrintMessageInput([window_title_1, title, message])
                return None

            return imported_file

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            lineEdit.setFocus()
            return None

    def load_user_defined_transfer_impedance(self):
        self.imported_values = self.load_table(self.lineEdit_user_defined_transfer_impedance_path)

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
            PrintMessageInput([window_title_1, title, message])
            return True

        self.update_analysis_setup_in_file(_frequencies)

        real_values = _imported_values[:, 1]
        imag_values = _imported_values[:, 2]

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

    # def attribute_callback(self):

    #     input_ids = self.lineEdit_selection_id.text()
    #     surface_ids = self.mesh.check_selected_ids(
    #                                                 input_ids, 
    #                                                 selection = "surfaces", 
    #                                                 single_id = False,
    #                                                 )

    #     if surface_ids is None:
    #         self.lineEdit_selection_id.setFocus()
    #         return

    #     self.check_selection_type(surface_ids)
    #     if not self.transfer_impedance_data:
    #         return

    #     self.remove_conflicting_excitations(surface_ids)

    #     if self.transfer_impedance_data.get("coupling_type") == "inside_surfaces":
    #         for surface_id in surface_ids:
    #             self.properties._set_property("transfer_impedance",self.transfer_impedance_data, surface=surface_id)
    #             self.decouple_degrees_of_freedom(surface_id)

    #     else:
    #         self.properties._set_property("transfer_impedance",self.transfer_impedance_data, surface=tuple(surface_ids))

    #     self.setup_complete = True
    #     self.actions_to_finalize()

    def include_transfer_impedance_table_data(self, surface_id: int | list[int]):

        if isinstance(surface_id, int):
            table_name = f"user_defined_transfer_impedance_at_surface_{surface_id}"
        else:
            table_name = f"user_defined_transfer_impedance_between_surfaces_{surface_id[0]}_{surface_id[1]}"

        if self.save_table_values(table_name, self.imported_values):
            self.lineEdit_table_path.setFocus()
            self.imported_values = None
            self.transfer_impedance_data.clear()
            return

        complex_values = self.imported_values[:, 1] + 1j * self.imported_values[:, 2]
        table_path = self.lineEdit_table_path.text()

        self.transfer_impedance_data["table_names"] = [table_name]
        self.transfer_impedance_data["table_paths"] = [table_path]
        self.transfer_impedance_data["values"] = [complex_values]

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
            app().file.write_imported_table_data_in_file()

    def remove_conflicting_excitations(self, surface_ids: int | list[int]):

        if self.comboBox_selection_type.currentText() == "Inside surfaces":
            if isinstance(surface_ids, int):
                surface_ids = [surface_ids]
        else:
            surface_ids = [tuple(surface_ids)]

        labels = ["transfer_impedance", "interior_impedance"]

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
        if self.lineEdit_selection_id.text() != "":

            input_ids = self.lineEdit_selection_id.text()
            input_ids = input_ids.replace("(", "").replace(")", "")

            surface_ids = self.mesh.check_selected_ids(
                                                        input_ids, 
                                                        selection = "surfaces", 
                                                        single_id = False,
                                                        )

            if len(surface_ids) == 1:
                surface_ids = surface_ids[0]

            elif len(surface_ids) == 2:
                surface_ids = tuple(surface_ids)

            else:
                return

            self.remove_table_files_from_surfaces(surface_ids)
            self.properties._remove_surface_property("transfer_impedance", surface_ids)

            app().project.reset_solutions()

            data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_ids)
            if isinstance(data, dict):
                new_surface_id = data.get("new_surface_id")
                if isinstance(new_surface_id, int):   
                    self.remove_all_surface_properties_from_surface([new_surface_id])
                    self.remove_all_line_properties_boundind_surface([new_surface_id]) 

                self.properties._remove_surface_property("degrees_of_freedom_decoupling", surface_ids)

                app().file.remove_mesh_data_from_project_file()
                app().file.remove_results_data_from_project_file()
                self.restore_mesh_data_modified_by_decoupling()

            self.actions_to_finalize()
            self.pushButton_remove.setDisabled(True)

    def reset_callback(self):

        surface_ids = list()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "transfer_impedance":
                surface_ids.append(surface_id)

        if not surface_ids:
            return

        self.hide()

        title = "Perforated plate model resetting"
        message = "Would you like to remove the perforated plate from the acoustic model?"

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

        self.properties._reset_property("transfer_impedance")
        app().project.reset_solutions()

        if new_surface_ids:
            self.remove_all_surface_properties_from_surface(new_surface_ids)
            self.remove_all_line_properties_boundind_surface(new_surface_ids)
            app().file.remove_mesh_data_from_project_file()
            app().file.remove_results_data_from_project_file()
            self.restore_mesh_data_modified_by_decoupling()

        self.actions_to_finalize()

    def restore_mesh_data_modified_by_decoupling(self):

        app().project.model.generated_mesh = False
        if self.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):
            return
        
        if self.mesh.cache_nodal_coordinates is None:
            return

        self.mesh.restore_data_from_cache()
        self.mesh.process_upwards_adjacencies_from_entities()
        app().project.model.generated_mesh = True

        app().file.write_mesh_data_in_file()
        app().file.write_geometry_data_in_file()
        app().main_window.update_mesh_information()
        app().main_window.update_geometry_information()
        app().main_window.update_plots()
        app().main_window.analysis_toolbar.pushButton_reset_solution.setDisabled(True)

    def actions_to_finalize(self):
        self.load_model_info()
        app().file.write_model_properties_in_file()
        app().file.write_imported_table_data_in_file()
        app().main_window.update_info_text()
        app().main_window.mesh_widget.update_symbols()
        app().main_window.set_geometry_selection()

    def check_inputs(self, lineEdit: QLineEdit, label, _float=True):

        self.stop = False
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

                if out <= 0:
                    message = f"Insert a positive value to the {label}."
                    message += "\n\nNote: zero value is not allowed."

            except Exception as _err:
                message = f"You have typed and invalid value at the {label} input field.\n\n"
                message += str(_err)

        else:
            message = f"Insert some value at the {label} input field."

        if message != "":
            self.hide()
            PrintMessageInput([window_title_1, title, message])
            return None
        else:
            return out
   
    def process_degress_of_freedom_decoupling(self):

        if not self.setup_complete:
            return False

        if not self.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):
            return False

        if not app().project.model.generated_mesh:
            self.hide()
            app().main_window.input_ui.mesh_setup()
            app().main_window.set_input_widget(self)
            return False

            # if not app().project.model.generated_mesh:
            #     return True
            # else:
            #     return False

        if self.mesh.cache_nodal_coordinates is None:
            self.mesh.cache_mesh_information()

        def process_decoupling():
            self.model.process_degrees_of_freedom_decoupling()
            app().file.write_model_properties_in_file()
            app().file.write_mesh_data_in_file()
            app().file.write_geometry_data_in_file()
            app().main_window.update_mesh_information()
            app().main_window.update_geometry_information()
            app().main_window.update_plots()

        LoadingWindow(process_decoupling).run()
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        self.hide()

        try:
            warnings.filterwarnings('default')
        except TypeError:
            pass

        if self.process_degress_of_freedom_decoupling():
            return

        self.keep_window_open = False
        return super().closeEvent(a0)

# fmt: on