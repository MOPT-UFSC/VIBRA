from PySide6.QtWidgets import QFileDialog, QLineEdit, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.data_filter.change_frequency_data_handler import ChangeFrequencyDataRangeInput
from vibra.interface.ui_generated.model.setup.acoustic.external_compressor_excitation_inputs_ui import ExternalCompressorExcitationInputs_UI

from utils.data_loaders import load_simulation_data_from_hdf_file
from utils.signal_processing import extend_signal, process_one_sided_spectrum

import os
import platform
import numpy as np

from numbers import Number
from pathlib import Path

error_title = "Error"


class ExternalCompressorExcitationInputs(ExternalCompressorExcitationInputs_UI):
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
        self._configure_qt_variables()
        self._create_connections()

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
        self.keep_window_open = True

    def _configure_qt_variables(self):
        #
        for i, w in enumerate([120]):
            self.treeWidget_surface_velocity.setColumnWidth(i, w)
            self.treeWidget_surface_velocity.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_normal_velocity_axis.currentIndexChanged.connect(self.compute_compressor_excitation_spectrum)
        self.comboBox_output_data.currentIndexChanged.connect(self.compute_compressor_excitation_spectrum)
        self.comboBox_source_data.currentIndexChanged.connect(self.source_data_callback)
        self.comboBox_single_revolution.currentIndexChanged.connect(self.compute_compressor_excitation_spectrum)
        #
        self.lineEdit_angular_resolution.textEdited.connect(self.compute_compressor_excitation_spectrum)
        self.lineEdit_frequency_resolution_required.textEdited.connect(self.compute_compressor_excitation_spectrum)
        self.lineEdit_maximum_frequency.textEdited.connect(self.compute_compressor_excitation_spectrum)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_load_table.clicked.connect(self.load_external_compressor_excitation_data)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_surface_velocity.itemClicked.connect(self.on_click_item)
        self.treeWidget_surface_velocity.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.geometry_selection_callback()

    def source_data_callback(self):
        source_data = self.comboBox_source_data.currentText()
        if source_data == "SCORG":
            self.lineEdit_angular_resolution.setEnabled(True)
        else:
            self.comboBox_single_revolution.setCurrentText("Angular resolution")
            self.lineEdit_angular_resolution.setEnabled(False)

    def geometry_selection_callback(self):

        faces = app().main_window.selected_geometry_surfaces

        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)

            if len(faces) == 1:
                surface_id = list(faces)[0]
                self.load_property_data(surface_id)

    def check_inputs(self, line_edit: QLineEdit, label: str):

        message = ""
        str_value = line_edit.text()
        
        if str_value in ["", "0", "0.", "0,"]:
            return None

        try:
            value = float(str_value.replace(",", "."))
            if value < 0:
                value = abs(value)
                line_edit.setText(f"{value}")

        except Exception as error_log:
            message = f"The typed value at the {label} input field is invalid.\n\n"
            message += str(error_log)

        if message != "":
            self.hide()
            title = "Invalid input to the analysis setup"
            PrintMessageInput([error_title, title, message])
            line_edit.setStyleSheet("""border-color: rgb(240, 10, 10); border-width: 2px;""")
            return None

        line_edit.setStyleSheet("")

        return value

    def load_external_compressor_excitation_data(self):
        self.hide()
        if self.comboBox_source_data.currentText() == "SCORG":
            self.load_scorg_data()
        else:
            self.load_cfd_data()

    def load_scorg_data(self):
        self.imported_values = self.load_table(self.lineEdit_table_path)
        mass_flow_spectrum = self.process_mass_flow_spectrum()
        if mass_flow_spectrum is None:
            return

        df = mass_flow_spectrum[0, 0]
        self.lineEdit_frequency_resolution.setText(f"{df}")

        freq = mass_flow_spectrum[:, 0]
        Xf = mass_flow_spectrum[:, 1] + 1j * mass_flow_spectrum[:, 2]

        plot(freq, Xf, "Frequency [Hz]", "Mass flow [kg/s]", "", absolute=True)

    def load_cfd_data(self):
        table_path = self.load_hdf_file()
        if table_path is None:
            return

        if Path(table_path).exists():
            self.lineEdit_table_path.setText(table_path)
            self.imported_values = load_simulation_data_from_hdf_file(table_path)

            angular_resolution = self.imported_values.get("delta_theta")
            if angular_resolution is None:
                return

            self.comboBox_single_revolution.blockSignals(True)
            self.lineEdit_angular_resolution.blockSignals(True)

            self.comboBox_single_revolution.setCurrentText("No")
            self.lineEdit_angular_resolution.setText(f"{angular_resolution}")

            self.comboBox_single_revolution.blockSignals(False)
            self.lineEdit_angular_resolution.blockSignals(False)

            surface_velocity_spectrum_data = self.process_normal_surface_velocity_spectrum()
            if surface_velocity_spectrum_data is None:
                return

            df = surface_velocity_spectrum_data[0, 0]
            self.lineEdit_frequency_resolution.setText(f"{df}")

            freq = surface_velocity_spectrum_data[:, 0]
            Xf = surface_velocity_spectrum_data[:, 1] + 1j * surface_velocity_spectrum_data[:, 2]

            plot(freq, Xf, "Frequency [Hz]", "Surface velocity [m/s]", "", absolute=True)

    def compute_compressor_excitation_spectrum(self):

        self.mass_flow_sdata = None
        self.normal_surface_velocity_sdata = None
        self.pressure_sdata = None
        self.acoustic_impedance_sdata = None

        if self.imported_values is None:
            return True

        if self.comboBox_source_data.currentText() == "SCORG":
            self.mass_flow_sdata= self.process_mass_flow_spectrum()
            if self.mass_flow_sdata is None:
                return True

            df = self.mass_flow_sdata[0, 0]
            self.lineEdit_frequency_resolution.setText(f"{df}")

        else:
            self.normal_surface_velocity_sdata = self.process_normal_surface_velocity_spectrum()
            if self.normal_surface_velocity_sdata is None:
                return True

            df = self.normal_surface_velocity_sdata[0, 0]
            self.lineEdit_frequency_resolution.setText(f"{df}")

    def get_normal_velocity_axis_data(self):
        axis_label = self.comboBox_normal_velocity_axis.currentText()
        str_values = axis_label.split("-axis")
        direction = str_values[0]
        signal = str_values[1].replace(" (", "").replace(")", "")
        factor = 1 if signal == "+" else -1
        return direction, factor

    def process_normal_surface_velocity_spectrum(self):

        if not isinstance(self.imported_values, dict):
            return None

        keys_map_cfd = {
            "x" : "velocity_u",
            "y" : "velocity_v",
            "z" : "velocity_w",
        }

        direction, sign_factor = self.get_normal_velocity_axis_data()
        velocity_key = keys_map_cfd.get(direction)

        time_vector = self.imported_values.get("time_seconds")
        normal_velocity_nodes = sign_factor * self.imported_values.get(velocity_key)

        nodal_area = self.imported_values.get("nodal_area")
        weights = nodal_area.reshape(-1, 1) / np.sum(nodal_area)

        if self.comboBox_output_data.currentText() == "Surface averaged":
            normal_velocity = np.sum(normal_velocity_nodes * weights, axis=0)
        else:
            return

        surface_velocity_spectrum_data = self.compute_signal_spectrum(time_vector, normal_velocity, export=True, filename="normal_surface_velocity_avg.dat", y_label="Normal surface velocity [m/s]")

        return surface_velocity_spectrum_data

    def process_pressure_spectrum(self):

        if not isinstance(self.imported_values, dict):
            return None

        time_vector = self.imported_values.get("time_seconds")
        pressure_nodes = self.imported_values.get("pressure") * 1e5

        nodal_area = self.imported_values.get("nodal_area")
        weights = nodal_area.reshape(-1, 1) / np.sum(nodal_area)

        if self.comboBox_output_data.currentText() == "Surface averaged":
            pressure = np.sum(pressure_nodes * weights, axis=0)
        else:
            return

        pressure_spectrum_data = self.compute_signal_spectrum(time_vector, pressure)

        freq = pressure_spectrum_data[:, 0]
        Xf = pressure_spectrum_data[:, 1] + 1j * pressure_spectrum_data[:, 2]

        plot(time_vector, pressure, "Time [s]", "Pressure [Pa]", "", absolute=False)
        plot(freq, Xf, "Frequency [Hz]", "Pressure [Pa]", "", absolute=True)

        return pressure_spectrum_data

    def process_mass_flow_spectrum(self):

        if self.imported_values is None:
            return None

        if self.comboBox_single_revolution.currentText() == "Yes":
            time_vector = self.imported_values[:, 0]
            mass_flow = self.imported_values[:, 1]

        else:
            angular_resoltion = self.check_inputs(self.lineEdit_angular_resolution, "Angular resolution")
            if angular_resoltion is None:
                self.lineEdit_angular_resolution.setFocus()
                return None

            n_steps = int(360 / angular_resoltion)
            start = n_steps + 1

            time_vector = self.imported_values[:, 0][-start:]
            mass_flow = self.imported_values[:, 1][-start:]

        return self.compute_signal_spectrum(time_vector, mass_flow)

    def compute_signal_spectrum(self, time_vector: np.ndarray, x_data: np.ndarray, export=False, filename="", y_label=""):

        # the desired frequency resolution
        f_step = self.check_inputs(self.lineEdit_frequency_resolution_required, "Frequency resolution")
        if f_step is None:
            self.lineEdit_frequency_resolution_required.setFocus()
            return None

        f_max = self.check_inputs(self.lineEdit_maximum_frequency, "Maximum frequency")
        if f_max is None:
            self.lineEdit_maximum_frequency.setFocus()
            return None

        # Sampling time to obtain desired frequency resolution
        T_req = 1 / f_step

        # calculat the time step
        dt = time_vector[-1] - time_vector[-2]

        # time to complete one revolution of the male rotor
        T_cycle = time_vector[-1] - time_vector[0]

        # number of repetitions to reach the desired frequency resolution
        N_rep = int(np.ceil(T_req / T_cycle))

        # extend the signal by 'N_rep' times to adjust the frequency resolution
        x_data_ext = extend_signal(x_data, N_rep)
        time_ext = np.arange(x_data_ext.size, dtype=float) * dt

        # process one-sided spectrum
        freq, Xf = process_one_sided_spectrum(x_data_ext, dt)

        # output data matrix
        output_data = np.array([freq, np.real(Xf), np.imag(Xf)], dtype=float).T

        mask_min = 0 < freq
        mask_max = freq <= f_max

        if export:
            np.savetxt(filename, np.array([time_ext, x_data_ext]).T, delimiter=",", fmt="%.16e")
            plot(time_ext, x_data_ext, "Time [s]", y_label, "", absolute=False)

        return output_data[mask_min * mask_max, :]

    def load_property_data(self, surface_id: int):

        if self.tabWidget_main.currentIndex() == 1:
            return

        data = self.properties._get_property("external_compressor_excitation", surface=surface_id)

        if isinstance(data, dict):

            source_data = data.get("source_data", "SCORG")
            angular_resolution = data.get("angular_resolution", 1.0)

            if source_data == "SCORG":
                self.comboBox_source_data.setCurrentText("SCORG")
            else:
                self.comboBox_source_data.setCurrentText("CFD")

            if isinstance(angular_resolution, Number):
                self.comboBox_single_revolution.setCurrentText("Angular resolution")
                self.lineEdit_angular_resolution.setText(f"{angular_resolution}")
            else:
                self.comboBox_single_revolution.setCurrentText("Yes")

            if "table_paths" in data.keys():
                self.tabWidget_main.setCurrentIndex(0)
                self.lineEdit_table_path.setText(data["table_paths"][0])

    def tab_event_callback(self):
        if self.tabWidget_main.currentIndex() == 1:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_attribute.setDisabled(True)
            self.pushButton_remove.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)
            self.pushButton_attribute.setEnabled(True)

    def load_hdf_file(self):

        extensions = ["h5", "hdf5"]
        caption = "Choose the HDF file to import the external compressor excitation data"

        imported_path, file_extension = DataImporter.get_file_paths(caption, "imported_table_folder", extensions)
        if not file_extension:
            return

        return imported_path
    
    def load_table(self, line_edit : QLineEdit, direct_load: bool=False):

        imported_file = None
        title = "Error reached while loading 'surface velocity' table"

        try:

            if direct_load:
                imported_table_path = line_edit.text()
                imported_file = DataImporter.read_data_in_file(imported_table_path).data

            else:
                extensions = ["csv", "dat", "txt", "xlsx", "xls"]
                caption = "Choose a table to import the surface velocity"
                imported_data = DataImporter.import_single_file("imported_table_folder", extensions, caption)

                if not imported_data:
                    return

                imported_file = imported_data.data
                line_edit.setText(imported_data.path)

            if imported_file.shape[1] < 2:
                self.hide()
                message = "The imported table has insufficient number of columns. The mass flow data signal "
                message += "must have two columns in the form: time, and mass flow values."
                PrintMessageInput([error_title, title, message])
                return None

            return imported_file

        except Exception as log_error:
            self.hide()
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            line_edit.setFocus()
            return None

    def save_table_values(self, table_name: str, imported_values: np.ndarray):

        _frequencies = imported_values[:, 0]

        if app().project.model.change_analysis_frequency_setup(list(_frequencies)):
            self.hide()
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        self.update_analysis_setup_in_file(_frequencies)

        real_values = imported_values[:, 1]
        imag_values = imported_values[:, 2]

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

    def attribute_callback(self):

        if self.tabWidget_main.currentIndex():
            return

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

        self.remove_conflicting_excitations(surface_ids)

        if self.lineEdit_table_path.text() == "":
            title = "Additional inputs required"
            message = "You must select the external compressor excitation "
            message += "table path to proceed with the assignment."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_table_path.setFocus()
            return

        source_data = self.comboBox_source_data.currentText()
        if self.imported_values is None:
            self.imported_values = self.load_table( 
                self.lineEdit_table_path, 
                direct_load = True 
                )

        if self.compute_compressor_excitation_spectrum():
            return

        excitation_type = "surface_velocity" if source_data == "CFD" else "mass_flow_rate"

        if self.comboBox_single_revolution.currentText()  == "Yes":
            angular_resolution = None
        else:
            angular_resolution = float(self.lineEdit_angular_resolution.text())

        for surface_id in surface_ids:

            if source_data == "SCORG":
                if not isinstance(self.mass_flow_sdata, np.ndarray):
                    return

                if self.mass_flow_sdata.shape[1] >= 3:
                    table_name = f"external_compressor_excitation_at_surface_{surface_id}"
                    if self.save_table_values(table_name, self.mass_flow_sdata):
                        self.lineEdit_table_path.setFocus()
                        self.imported_values = None
                        return

                complex_values = self.mass_flow_sdata[:, 1] + 1j * self.mass_flow_sdata[:, 2]

            else:
                if not isinstance(self.normal_surface_velocity_sdata, np.ndarray):
                    return

                if self.normal_surface_velocity_sdata.shape[1] >= 3:
                    table_name = f"external_compressor_excitation_at_surface_{surface_id}"
                    if self.save_table_values(table_name, self.normal_surface_velocity_sdata):
                        self.lineEdit_table_path.setFocus()
                        self.imported_values = None
                        return

                complex_values = self.normal_surface_velocity_sdata[:, 1] + 1j * self.normal_surface_velocity_sdata[:, 2]

            table_path = self.lineEdit_table_path.text()

            data = {
                    "excitation_type" : excitation_type,
                    "table_names" : [table_name],
                    "table_paths" : [table_path],
                    "values" : [complex_values],                   
                    "averaged" : False,
                    "nodal_attribution" : False,
                    "source_data" : source_data,
                    "angular_resolution" : angular_resolution,
                    }

            self.properties._set_property("external_compressor_excitation", data, surface=surface_id)

        self.actions_to_finalize()

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().file.write_imported_table_data_in_file()

    def remove_conflicting_excitations(self, surface_ids: int | list):

        if isinstance(surface_ids, int):
            surface_ids = [surface_ids]

        labels = [
                  "acoustic_pressure",
                  "surface_velocity",
                  "incident_plane_wave",
                  "mass_flow_rate",
                  "external_compressor_excitation",
                  "reciprocating_compressor_excitation",
                  ]

        for surface_id in surface_ids:
            for label in labels:
                table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_id : int | list):
        table_names = self.properties.get_property_related_table_names("external_compressor_excitation", surface_id, "surfaces")
        self.process_table_file_removal(table_names)

    def remove_callback(self):

        if self.lineEdit_selection_id.text() == "":
            return

        surface_id = int(self.lineEdit_selection_id.text())
        self.remove_table_files_from_surfaces(surface_id)

        self.properties._remove_surface_property("external_compressor_excitation", surface_id)
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "External comrpressor excitation resetting"
        message = "Would you like to remove the all external compressor excitations from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            surface_ids = list()
            for (property, *args) in self.properties.surface_properties.keys():
                if property == "external_compressor_excitation":
                    surface_id = args[0]
                    surface_ids.append(surface_id)

            self.remove_table_files_from_surfaces(surface_ids)

            self.properties._reset_property("external_compressor_excitation")
            self.actions_to_finalize()

    def actions_to_finalize(self):
        self.load_model_info()
        self.check_model_frequency_controls()
        app().file.write_model_properties_in_file()
        app().file.write_imported_table_data_in_file()
        app().main_window.update_info_text()
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
            if property in [
                "acoustic_pressure",
                "surface_velocity",
                "incident_plane_wave",
                "specific_impedance",
                "external_compressor_excitation",
                "reciprocating_compressor_excitation",
                ]:
                if "table_names" in data.keys():
                    return

        if isinstance(self.project.analysis_setup, dict):
            analysis_setup = self.project.analysis_setup
            self.project.set_analysis_setup(analysis_setup)
            app().file.write_analysis_setup_in_file(analysis_setup)

    def update_tabs_visibility(self):

        for key in self.properties.surface_properties.keys():
            property, *args = key
            if property == "external_compressor_excitation":
                self.tabWidget_main.setTabVisible(1, True)
                return

        self.tabWidget_main.setCurrentIndex(0)    
        self.tabWidget_main.setTabVisible(1, False)

    def on_click_item(self, item):
        if item.text(0) != "":
            self.pushButton_remove.setDisabled(False)
            surface_id = int(item.text(0))
            self.lineEdit_selection_id.setText(item.text(0))
            app().main_window.set_geometry_selection(surfaces=[surface_id])

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def load_model_info(self):
        self.treeWidget_surface_velocity.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property != "external_compressor_excitation":
                continue

            source_data = data.get("source_data")
            angular_resolution = data.get("angular_resolution")
            if angular_resolution is None:
                angular_resolution = "complete revolution"

            item = QTreeWidgetItem([str(surface_id), source_data, str(angular_resolution)])
            for i in range(3):
                item.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_surface_velocity.addTopLevelItem(item)

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
        app().main_window.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)
    

def plot(x, y, x_label, y_label, title, label="", absolute=False):

    import matplotlib.pyplot as plt

    plt.ion()

    fig = plt.figure(figsize=[8, 6])
    ax_ = fig.add_subplot(1,1,1)

    if absolute:
        y = np.abs(y)

    ax_.plot(x, y, color=[0,0,1], linewidth = 1, label = label)

    ax_.set_xlabel(x_label, fontsize = 11, fontweight = 'bold')
    ax_.set_ylabel(y_label, fontsize = 11, fontweight = 'bold')
    ax_.set_title(title, fontsize = 12, fontweight = 'bold')

    plt.grid()
    plt.show()