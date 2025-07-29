# fmt: off

from PySide6.QtWidgets import QFileDialog, QLineEdit, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app, UI_DIR
from vibra.interface.ui_generated.model.setup.acoustic.incident_plane_wave_inputs_ui import IncidentPlaneWaveInputs_UI
from vibra.interface.model_inputs.data_filter.change_frequency_data_handler import ChangeFrequencyDataRangeInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.data_importer import DataImporter

import os
import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class IncidentPlaneWaveInputs(IncidentPlaneWaveInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.action_model_workspace_callback()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties
        
        self._config_window()
        self._initialize()
        self._configure_qt_variables()
        self._create_connections()

        self.load_model_info()
        self.wave_direction_callback()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.imported_values = None
        self.keep_window_open = True

    def _create_connections(self):
        #
        self.comboBox_wave_direction.currentIndexChanged.connect(self.wave_direction_callback)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_load_table.clicked.connect(self.load_incident_pressure_table)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_incident_plane_wave.itemClicked.connect(self.on_click_item)
        self.treeWidget_incident_plane_wave.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)

    def _configure_qt_variables(self):
        #
        for i, w in enumerate([120, 160]):
            self.treeWidget_incident_plane_wave.setColumnWidth(i, w)
            self.treeWidget_incident_plane_wave.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def tab_event_callback(self):
        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_attribute.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)
            self.pushButton_attribute.setEnabled(True)

    def on_click_item(self, item):
        if item.text(0) != "":
            self.pushButton_remove.setEnabled(True)
            surface_id = int(item.text(0))
            self.lineEdit_selection_id.setText(item.text(0))
            app().main_window.set_geometry_selection(surfaces=[surface_id])

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def load_model_info(self):

        self.treeWidget_incident_plane_wave.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "incident_plane_wave":

                wave_vector = [round(value, 8) for value in data.get("wave_vector")]

                if "table_names" in data.keys():
                    str_value = "Table of values"
                else:
                    incident_pressure = np.array(data["real_values"])
                    str_value = str(incident_pressure)

                new = QTreeWidgetItem([str(surface_id), str(wave_vector), str_value])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_incident_plane_wave.addTopLevelItem(new)

        self.update_tabs_visibility()

    def geometry_selection_callback(self):

        surfaces = self.main_window.selected_geometry_surfaces

        if surfaces:
            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)
            surface_ids = [int(surf_id) for surf_id in surfaces]

            if len(surface_ids) != 1:
                self.lineEdit_component_x.setText("")
                self.lineEdit_component_y.setText("")
                self.lineEdit_component_z.setText("")
                return

            normal_vector = self.get_average_surface_normal(surface_ids[0])
            self.lineEdit_normal_x.setText(f"{normal_vector[0] : .4f}".replace(" ", ""))
            self.lineEdit_normal_y.setText(f"{normal_vector[1] : .4f}".replace(" ", ""))
            self.lineEdit_normal_z.setText(f"{normal_vector[2] : .4f}".replace(" ", ""))

            data = self.properties._get_property("incident_plane_wave", surface=surface_ids[0])
            if isinstance(data, dict):
                self.load_property_data(data)

            else:
                if self.comboBox_wave_direction.currentIndex() == 0:
                    wave_vector = -normal_vector
                    self.lineEdit_component_x.setText(f"{wave_vector[0] : .4f}".replace(" ", ""))
                    self.lineEdit_component_y.setText(f"{wave_vector[1] : .4f}".replace(" ", ""))
                    self.lineEdit_component_z.setText(f"{wave_vector[2] : .4f}".replace(" ", ""))

    def load_property_data(self, data: dict):

        wave_direction = data.get("wave_direction")
        if wave_direction == "normal":
            self.comboBox_wave_direction.setCurrentIndex(0)
        else:
            self.comboBox_wave_direction.setCurrentIndex(1)

        values = data.get("values")
        self.lineEdit_incident_pressure_real.setText(f"{np.real(values[0])}")
        self.lineEdit_incident_pressure_imag.setText(f"{np.imag(values[0])}")

        wave_vector = data.get("wave_vector")
        if wave_vector is None:
            return

        self.lineEdit_component_x.setText(f"{wave_vector[0] : .4f}".replace(" ", ""))
        self.lineEdit_component_y.setText(f"{wave_vector[1] : .4f}".replace(" ", ""))
        self.lineEdit_component_z.setText(f"{wave_vector[2] : .4f}".replace(" ", ""))

    def attribute_callback(self):
        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == 0:
            self.constant_data_assignment()
        elif tab_index == 1:
            self.tabular_data_assignment()

    def check_inputs(self, line_edit: QLineEdit, label, only_positive: bool = True):

        message = ""
        title = "Invalid value typed"
        input_str = line_edit.text()

        if input_str != "":

            input_str = input_str.replace(",", ".")

            try:
                out = float(input_str)
                
                if out <= 0 and only_positive:
                    message = f"Insert a positive value to the {label}."
                    message += "\n\nNote: zero value is not allowed."

            except Exception as _err:
                message = f"You have typed and invalid value at the {label} input field.\n\n"
                message += str(_err)

        else:
            message = f"Insert some value at the {label} input field."

        if message != "":
            self.hide()
            line_edit.setFocus()
            PrintMessageInput([window_title_1, title, message])
            return None
        else:
            return out

    def check_complex_entries(self, line_edit_real: QLineEdit, line_edit_imag: QLineEdit, label: str):

        real_value = None
        str_real = line_edit_real.text()
        if str_real != "":
            try:
                str_real = str_real.replace(",", ".")
                real_value = float(str_real)

            except Exception:
                self.hide()
                line_edit_real.setFocus()
                title = f"Invalid value detected"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([window_title_1, title, message])
                return True

        imag_value = None
        str_imag = line_edit_imag.text()
        if str_imag != "":
            try:
                str_imag = str_imag.replace(",", ".")
                imag_value = float(str_imag)

            except Exception:
                self.hide()
                line_edit_imag.setFocus()
                title = f"Invalid value detected"
                message = f"Wrong input for imaginary part of {label}."
                PrintMessageInput([window_title_1, title, message])
                return True

        if self.comboBox_wave_direction.currentIndex() == 0:
            if real_value <= 0:
                self.hide()
                line_edit_real.setFocus()
                title = f"Invalid value detected"
                message = "Enter a positive value for the normal "
                message += "incident wave amplitude."
                PrintMessageInput([window_title_1, title, message])
                return None

            # return complex(real_value)

        if real_value is None and imag_value is None:
            values = None
        elif real_value is None:
            values = 1j * imag_value
        elif imag_value is None:
            values = complex(real_value)
        else:
            values = real_value + 1j * imag_value

        return values

    def wave_direction_callback(self):
        index = self.comboBox_wave_direction.currentIndex()
        self.frame_wave_vector.setEnabled(bool(index))

    def get_average_surface_normal(self, surface_id: int):

        normal = 0.
        connectivity_from_surfaces = self.mesh.connectivity_from_surfaces.get(surface_id)
        for connect in connectivity_from_surfaces:
            normal += self.mesh.get_element_face_normal(connect)

        normal /= len(connectivity_from_surfaces)

        return normal
    
    def get_input_wave_vector(self, surface_id: int):

        if self.comboBox_wave_direction.currentIndex() == 0:
            normal_vector = self.get_average_surface_normal(surface_id)
            wave_vector = [float(value) for value in -normal_vector]

        else:
            e_x = self.check_inputs(self.lineEdit_component_x, "e_x", only_positive=False)
            e_y = self.check_inputs(self.lineEdit_component_y, "e_y", only_positive=False)
            e_z = self.check_inputs(self.lineEdit_component_z, "e_z", only_positive=False)

            if (e_x, e_y, e_z).count(None):
                return None
            
            wave_vector = [e_x, e_y, e_z]

        return wave_vector


    def get_incident_wave_inputs(self):
        
        P_inc = self.check_complex_entries(self.lineEdit_incident_pressure_real, self.lineEdit_incident_pressure_imag, "P_inc")

        if self.comboBox_wave_direction.currentIndex():
            wave_direction = "components"
        else:
            wave_direction = "normal"

        if P_inc is None:
            return dict()

        output = {
                  "wave_direction" : wave_direction,
                  "values" : [P_inc],
                  }

        return output
    
    def check_for_inside_surfaces(self, surface_ids: list[int]):
        """
        """
        for surface_id in surface_ids:
            volumes_from_surface = self.mesh.volumes_from_surface.get(surface_id)
            if len(volumes_from_surface) != 1:
                return True

        return False

    def check_wave_incidence(self, surface_ids: list[int], P_inc: complex | np.ndarray):
        
        if isinstance(P_inc, complex):
            P_inc = np.array([P_inc], dtype=complex)

        for surface_id in surface_ids:

            wave_vector = self.get_input_wave_vector(surface_id)
            if wave_vector is None:
                return

            wave_vector = np.array(wave_vector, dtype=float)
            ns_vector = self.get_average_surface_normal(surface_id)
            
            values = P_inc * (ns_vector @ wave_vector)

            for value in np.real(values):
                if np.real(value) < 0:
                    continue
            
                self.hide()
                title = 'Invalid setup detected'
                message = "The plane wave should be incident, i.e., directed inwards of the domain. "
                message += "We recommend to verify the entered values of the incident pressure amplitude "
                message += "and of the wave vector."
                PrintMessageInput([window_title_1, title, message])
                return True

        return False

    def constant_data_assignment(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(
                                                               input_ids, 
                                                               selection = "surfaces",
                                                               single_id = False,
                                                               )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        if self.check_for_inside_surfaces(surface_ids):
            self.hide()
            title = "Invalid surface selected"
            message = "An invalid surface has been detected in the current "
            message += "selection. The incident plane wave excitation can"
            message += "only applied on the outside surfaces."
            PrintMessageInput([window_title_1, title, message])
            return

        incident_wave_inputs = self.get_incident_wave_inputs()
        if not incident_wave_inputs:
            return

        self.remove_conflicting_excitations(surface_ids)

        values = incident_wave_inputs.get("values")
        wave_direction = incident_wave_inputs.get("wave_direction")

        real_values = [value if value is None else np.real(value) for value in values]
        imag_values = [value if value is None else np.imag(value) for value in values]

        data = {
                "wave_direction" : wave_direction,
                "real_values" : real_values,
                "imag_values" : imag_values,
                }

        if self.check_wave_incidence(surface_ids, values[0]):
            return

        for surface_id in surface_ids:

            wave_vector = self.get_input_wave_vector(surface_id)
            if wave_vector is None:
                return

            data["wave_vector"] = wave_vector
            self.properties._set_property("incident_plane_wave", data, surface=surface_id)

        self.actions_to_finalize()  

    def load_table(self, lineEdit : QLineEdit, direct_load=False):

        title = "Error reached while loading 'incident plane wave' table"
        imported_file = None

        try:
            if direct_load:
                imported_table_path = lineEdit.text()
                imported_file = np.loadtxt(imported_table_path, delimiter=",")

            else:
               imported_data = DataImporter.import_single_file("imported_table_folder", ["csv", "dat", "txt"], "Choose a table to import the absorption surface")

               if not imported_data:
                   return
               
               imported_file = imported_data.data
               lineEdit.setText(imported_data.path)


            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The incident plane wave"
                message += " data must have two columns in the form: frequencies real values, and imaginary values."
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
        # imag_values = _imported_values[:, 2]

        data = np.array([_frequencies, real_values], dtype=float).T
        # data = np.array([_frequencies, real_values, imag_values], dtype=float).T

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

    def load_incident_pressure_table(self):
        self.imported_values = self.load_table(self.lineEdit_table_path)

    def tabular_data_assignment(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(
                                                               input_ids, 
                                                               selection = "surfaces",
                                                               single_id = False,
                                                               )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        if self.check_for_inside_surfaces(surface_ids):
            self.hide()
            title = "Invalid surface selected"
            message = "An invalid surface has been detected in the current "
            message += "selection. The incident plane wave excitation can"
            message += "only applied on the outside surfaces."
            PrintMessageInput([window_title_1, title, message])
            return

        if self.comboBox_wave_direction.currentIndex():
            wave_direction = "components"
        else:
            wave_direction = "normal"

        self.remove_conflicting_excitations(surface_ids)

        if self.lineEdit_table_path.text() != "":

            if self.imported_values is None:
                self.imported_values = self.load_table( self.lineEdit_table_path, 
                                                        direct_load = True )

                if isinstance(self.imported_values, np.ndarray):
                    if self.imported_values.shape[1] < 3:
                        return
                else:
                    return
            
            complex_values = self.imported_values[:, 1] + 1j * self.imported_values[:, 2]
            table_path = self.lineEdit_table_path.text()

            if self.check_wave_incidence(surface_ids, complex_values):
                return
            
            for surface_id in surface_ids:

                wave_vector = self.get_input_wave_vector(surface_id)
                if wave_vector is None:
                    return

                table_name = f"incident_pressure_wave_{surface_id}"
                if self.save_table_values(table_name, self.imported_values):
                    self.lineEdit_table_path.setFocus()
                    self.imported_values = None
                    return

                data = {
                        "wave_direction" : wave_direction,
                        "wave_vector" : wave_vector,
                        "table_names": [table_name],
                        "table_paths" : [table_path],
                        "values" : [complex_values],
                        }

                self.properties._set_property("incident_plane_wave", data, surface=surface_id)

            self.actions_to_finalize()

        else:
            title = "Additional inputs required"
            message = "You must inform at least one absorption surface\n"
            message += "table path before confirming the input!"
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

        labels = ["incident_plane_wave"]
        labels = [
                  "acoustic_pressure",
                  "surface_velocity",
                  "incident_plane_wave",
                  "mass_flow_rate",
                  "reciprocating_compressor_excitation",
                  "reciprocating_pump_excitation",
                  "specific_impedance",
                  "absorption_surface",
                  ]

        for surface_id in surface_ids:
            for label in labels:
                table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_id : list):
        table_names = self.properties.get_property_related_table_names("incident_plane_wave", surface_id, "surfaces")
        self.process_table_file_removal(table_names)

    def remove_callback(self):
        
        str_selection_id = self.lineEdit_selection_id.text()
        if str_selection_id == "":
            return

        surface_id = int(str_selection_id)
        self.remove_table_files_from_surfaces(surface_id)

        self.properties._remove_surface_property("incident_plane_wave", surface_id)
        self.actions_to_finalize()

    def reset_callback(self):

        surface_ids = list()
        for (property, *args) in self.properties.surface_properties.keys():
            if property == "incident_plane_wave":
                surface_ids.append(args[0])

        if not surface_ids:
            return

        self.hide()

        title = "Incident pressure wave reset"
        message = "Would you like to remove the all applied incident pressure waves from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        self.remove_table_files_from_surfaces(surface_ids)
        for surface_id in surface_ids:
            self.properties._remove_surface_property("incident_plane_wave", surface_id)

        self.actions_to_finalize()

    def actions_to_finalize(self):
        self.load_model_info()
        self.check_model_frequency_controls()
        self.main_window.update_info_text()
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

        properties = [
                      "acoustic_pressure", 
                      "surface_velocity", 
                      "specific_impedance",
                      "incident_plane_wave",
                      "incident_plane_wavee",
                      "transfer_impedance",
                      "perforated_plate", 
                      "reciprocating_compressor_excitation",
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

    def update_tabs_visibility(self):

        for key in self.properties.surface_properties.keys():
            property, *args = key
            if property == "incident_plane_wave":
                self.tabWidget_main.setTabVisible(2, True)
                return

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_main.setTabVisible(2, False)

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

# fmt: on