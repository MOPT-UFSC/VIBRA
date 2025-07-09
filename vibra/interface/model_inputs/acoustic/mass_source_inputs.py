from PySide6.QtWidgets import QFileDialog, QLineEdit, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.ui_generated.model.setup.acoustic.mass_source_inputs_ui import MassSourceInputs_UI
from vibra.interface.model_inputs.data_filter.change_frequency_data_handler import ChangeFrequencyDataRangeInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

import os
import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class MassSourceInputs(MassSourceInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)

        self.project = app().project
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
        self.setWindowTitle("Acoustic pressure")

    def _initialize(self):
        self.imported_values = None
        self.keep_window_open = True

    def _configure_qt_variables(self):
        #
        self.lineEdit_nearest_node_id.setDisabled(True)
        self.lineEdit_node_coord_x.setDisabled(True)
        self.lineEdit_node_coord_y.setDisabled(True)
        self.lineEdit_node_coord_z.setDisabled(True)
        #
        self.pushButton_change_frequency_setup.setDisabled(True)
        #
        for i, w in enumerate([100, 120]):
            self.treeWidget_mass_source.setColumnWidth(i, w)
            self.treeWidget_mass_source.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_load_table.clicked.connect(self.load_acoustic_pressure_table)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_get_nearest_node.clicked.connect(self.compute_nearest_node_from_coordinate)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_mass_source.itemClicked.connect(self.on_click_item)
        self.treeWidget_mass_source.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)

    def geometry_selection_callback(self):

        points = app().main_window.selected_geometry_points
        nodes = app().main_window.selected_mesh_nodes

        text = ""

        if points:
            text = ", ".join([str(i) for i in points])
            
        elif nodes:
            text = ", ".join([str(i) for i in nodes])

        if text != "":
            self.lineEdit_selection_id.setText(text)

        if len(points) == 1:
            point_id = list(points)[0]
            self.load_property_data(point_id)

    def load_property_data(self, surface_id: int):

        if self.tabWidget_main.currentIndex() == 3:
            return

        data = self.model.properties._get_property("mass_source", surface=surface_id)

        if isinstance(data, dict):

            if "table_paths" in data.keys():
                self.tabWidget_main.setCurrentIndex(1)
                self.lineEdit_table_path.setText(data["table_paths"][0])
            else:
                self.tabWidget_main.setCurrentIndex(0)
                self.lineEdit_real_value.setText(str(data["real_values"][0]))
                self.lineEdit_imag_value.setText(str(data["imag_values"][0]))

    def attribution_type_callback(self):
        attribution_type = self.comboBox_attribution_type.currentIndex()
        if attribution_type == 0:
            app().main_window.action_model_workspace_callback()
        else:
            app().main_window.action_mesh_workspace_callback()

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

    def compute_nearest_node_from_coordinate(self):

        self.comboBox_attribution_type.setCurrentIndex(1)

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

        app().main_window.set_mesh_selection(nodes=[nearest_node])

    def tab_event_callback(self):
        if self.tabWidget_main.currentIndex() == 3:
            self.comboBox_attribution_type.setDisabled(True)
            app().main_window.set_mesh_selection()
            app().main_window.set_geometry_selection()
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_attribute.setDisabled(True)
        else:
            self.comboBox_attribution_type.setEnabled(True)
            self.lineEdit_selection_id.setDisabled(False)
            self.pushButton_attribute.setEnabled(True)

    def attribute_callback(self):
        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == 0:
            self.check_constant_values()
        elif tab_index == 1:
            self.check_table_values()

    def check_complex_entries(self, lineEdit_real, lineEdit_imag):
        self.stop = False
        title = "Invalid entry to the acoustic pressure"
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                message = "Wrong input for real part of acoustic pressure."
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
                message = "Wrong input for imaginary part of acoustic pressure."
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

    def check_constant_values(self):

        if self.comboBox_attribution_type.currentIndex() == 0:
            selection = "points"    
        else:
            selection = "nodes"

        input_ids = self.lineEdit_selection_id.text()
        selection_ids, error_data = self.mesh.check_selected_ids(
                                                                 input_ids, 
                                                                 selection = selection
                                                                 )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        self.remove_conflicting_excitations(selection_ids)

        acoustic_pressure = self.check_complex_entries(self.lineEdit_real_value, self.lineEdit_imag_value)

        if acoustic_pressure is not None:

            real_values = [np.real(acoustic_pressure)]
            imag_values = [np.imag(acoustic_pressure)]

            data = {
                    "real_values": real_values,
                    "imag_values": imag_values,
                    }

            for selection_id in selection_ids:
                if self.comboBox_attribution_type.currentIndex() == 0:
                    self.properties._set_property("mass_source", data, point=selection_id)
                else:
                    self.properties._set_property("mass_source", data, node=selection_id)

            self.actions_to_finalize()

        else:
            title = "Additional inputs required"
            message = "You must inform at least one non-zero value to mass source \n"
            message += "input fields before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_real_value.setFocus()

    def load_table(self, lineEdit : QLineEdit, direct_load=False):

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

                caption = "Choose a table to import the acoustic pressure"
                imported_table_path, check = QFileDialog.getOpenFileName(  None, 
                                                                            caption, 
                                                                            path, 
                                                                            "Files (*.csv; *.dat; *.txt)"
                                                                        )

                if not check:
                    return None

            lineEdit.setText(imported_table_path)
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

    def load_acoustic_pressure_table(self):
        self.imported_values = self.load_table(self.lineEdit_table_path)

    def check_table_values(self):

        if self.comboBox_attribution_type.currentIndex() == 0:
            selection_type = "points"    
        else:
            selection_type = "nodes"

        input_ids = self.lineEdit_selection_id.text()
        selection_ids, error_data = self.mesh.check_selected_ids(
                                                                 input_ids, 
                                                                 selection = selection_type
                                                                 )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        self.remove_conflicting_excitations(selection_ids)

        if self.lineEdit_table_path.text() != "":

            if self.imported_values is None:
                self.imported_values = self.load_table( self.lineEdit_table_path, 
                                                        direct_load = True )

            for selection_id in selection_ids:

                if isinstance(self.imported_values, np.ndarray):
                    if self.imported_values.shape[1] >= 3:

                        table_name = f"mass_source_at_{selection_type}_{selection_id}"
                        if self.save_table_values(table_name, self.imported_values):
                            self.lineEdit_table_path.setFocus()
                            self.imported_values = None
                            return

                else:
                    return

                if self.imported_values is None:
                    return

                complex_values = self.imported_values[:, 1] + 1j * self.imported_values[:, 2]
                table_path = self.lineEdit_table_path.text()

                data = {
                        "table_names" : [table_name],
                        "table_paths" : [table_path],
                        "values" : [complex_values],
                        }

                if self.comboBox_attribution_type.currentIndex() == 0:
                    self.properties._set_property("mass_source", data, point=selection_id)
                else:
                    self.properties._set_property("mass_source", data, node=selection_id)

            self.actions_to_finalize()

        else:
            title = "Additional inputs required"
            message = "You must inform a valid table path to the mass source \n"
            message += "data before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_table_path.setFocus()

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().file.write_imported_table_data_in_file()

    def remove_conflicting_excitations(self, surface_ids: int | list):

        if isinstance(surface_ids, int):
            surface_ids = [surface_ids]

        labels = ["mass_source"]

        for surface_id in surface_ids:
            for label in labels:
                table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_selection(self, surface_id : list, selection_type: str):
        table_names = self.properties.get_property_related_table_names("mass_source", surface_id, selection_type)
        self.process_table_file_removal(table_names)

    def remove_callback(self):

        if self.lineEdit_selection_id.text() != "":

            selection_id = int(self.lineEdit_selection_id.text())

            if self.comboBox_attribution_type.currentIndex() == 0:
                self.remove_table_files_from_selection(selection_id, "points")
                self.properties._remove_point_property("mass_source", selection_id)

            else:
                self.remove_table_files_from_selection(selection_id, "nodes")
                self.properties._remove_nodal_property("mass_source", selection_id)

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

            point_ids = list()
            for (property, *args) in self.properties.point_properties.keys():
                if property != "mass_source":
                    continue

                point_id = args[0]
                point_ids.append(point_id)

            node_ids = list()
            for (property, *args) in self.properties.point_properties.keys():
                if property != "mass_source":
                    continue

                node_id = args[0]
                node_ids.append(node_id)

            self.remove_table_files_from_selection(point_ids, "points")
            self.remove_table_files_from_selection(node_ids, "nodes")

            self.properties._reset_property("mass_source")
            self.actions_to_finalize()

    def actions_to_finalize(self):
        self.load_model_info()
        self.check_model_frequency_controls()
        self.main_window.update_info_text()
        app().file.write_model_properties_in_file()
        app().file.write_imported_table_data_in_file()
        app().main_window.set_mesh_selection()
        app().main_window.set_geometry_selection()
        app().main_window.update_symbols()

    def change_frequency_setup(self):
        if self.imported_values is not None:
            self.hide()
            obj = ChangeFrequencyDataRangeInput(self.imported_values)
            if obj.filter_data is not None:
                self.imported_values = obj.filter_data

    def check_model_frequency_controls(self):

        properties = [
                        "acoustic_pressure", 
                        "surface_velocity", 
                        "specific_impedance", 
                        "reciprocating_compressor_excitation",
                        "mass_source",
                        ]

        for key, data in self.properties.surface_properties.items():
            property, _ = key
            if property in properties:
                if "table_names" in data.keys():
                    return

        if isinstance(self.project.analysis_setup, dict):
            analysis_setup = self.project.analysis_setup
            self.project.set_analysis_setup(analysis_setup)
            app().file.write_analysis_setup_in_file(analysis_setup)

    def reset_input_fields(self):
        self.lineEdit_real_value.setText("")
        self.lineEdit_imag_value.setText("")
        self.lineEdit_table_path.setText("")

    def update_tabs_visibility(self):

        properties = [
                      self.properties.point_properties,
                      self.properties.nodal_properties
                      ]

        for _property in properties:
            for key in _property.keys():
                property, *args = key
                if property != "mass_source":
                    continue

                self.tabWidget_main.setTabVisible(3, True)
                return

        self.tabWidget_main.setCurrentIndex(0)    
        self.tabWidget_main.setTabVisible(3, False)

    def on_click_item(self, item):
        if item.text(0) != "":
            selection_id = int(item.text(0))
            self.lineEdit_selection_id.setText(item.text(0))
            if item.text(1)== "point":
                self.comboBox_attribution_type.setCurrentIndex(0)
                app().main_window.set_geometry_selection(points=[selection_id])
            else:
                self.comboBox_attribution_type.setCurrentIndex(1)
                app().main_window.set_mesh_selection(nodes=[selection_id])

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def load_model_info(self):

        properties = {
                      "point" : self.properties.point_properties,
                      "node" : self.properties.nodal_properties
                      }

        self.treeWidget_mass_source.clear()
        for selection_label, _property in properties.items():
            for key, data in _property.items():
                property, selection_id = key
                if property != "mass_source":
                    continue

                # print(key, data)

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
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            return

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)