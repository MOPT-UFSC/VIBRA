from copy import deepcopy
from enum import IntEnum
from pathlib import Path

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem

# from scipy.io import wavfile
from scipy.signal.windows import hann

from vibra import app
from vibra.interface import error_title
from vibra.interface.common.common_interface import update_analysis_setup_in_file, update_entities_selection
from vibra.interface.data.data_manager import get_spectral_data_from_array
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.utils import clear_style_sheet
from vibra.interface.plots.general.frequency_response_plotter import DataFormat, FrequencyResponsePlotter
from vibra.interface.ui_generated.model.acoustic.excitations.compressor_excitation_waveform_inputs_ui import CompressorExcitationWaveformInputs_UI
from vibra.utils.signal_processing import extend_signal, get_window_and_correction_factor, process_one_sided_spectrum


class TabIndex(IntEnum):
    SETUP = 0
    SIGNALS = 1
    LIST = 2


class CompressorExcitationWaveformInputs(CompressorExcitationWaveformInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

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
        
        self.T_audio = 5
        self.fading_samples = 4096

        self.model_results = dict()

        self.auralize_signal = False
        self.keep_window_open = True

        self.imported_values = None
        self.spectrum_plotter = None
        self.waveform_plotter = None

        self.reset_plotting_attributes()

    def _configure_qt_variables(self):
        #
        self.pushButton_reproduce_audio.setToolTip("Auralize the signal")
        self.pushButton_spectrum_data.setDisabled(True)
        self.pushButton_waveform_data.setDisabled(True)
        #
        for i, w in enumerate([120]):
            self.treeWidget_surface_velocity.setColumnWidth(i, w)
            self.treeWidget_surface_velocity.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_normal_velocity_axis.currentIndexChanged.connect(self.compute_compressor_excitation_spectrum)
        self.comboBox_excitation_mapping.currentIndexChanged.connect(self.compute_compressor_excitation_spectrum)
        self.comboBox_data_source.currentIndexChanged.connect(self.data_source_callback)
        self.comboBox_single_revolution.currentIndexChanged.connect(self.compute_compressor_excitation_spectrum)
        self.comboBox_excitation_type.currentIndexChanged.connect(self.update_data_to_plot_combo_box)
        #
        self.lineEdit_angular_resolution.textEdited.connect(self.compute_compressor_excitation_spectrum)
        self.lineEdit_frequency_resolution_required.textEdited.connect(self.compute_compressor_excitation_spectrum)
        self.lineEdit_maximum_frequency.textEdited.connect(self.compute_compressor_excitation_spectrum)
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_load_table.clicked.connect(self.load_compressor_excitation_data)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_spectrum_data.clicked.connect(self.plot_spectrum_data_callback)
        self.pushButton_waveform_data.clicked.connect(self.plot_waveform_data_callback)
        self.pushButton_reproduce_audio.clicked.connect(self.reproduce_audio_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_surface_velocity.itemClicked.connect(self.on_click_item)
        self.treeWidget_surface_velocity.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.data_source_callback()
        self.geometry_selection_callback()

    def data_source_callback(self):
        self.imported_values = None
        self.comboBox_data_to_plot.clear()

        cfd_source = self.comboBox_data_source.currentText() == "CFD"
        self.comboBox_excitation_mapping.setEnabled(cfd_source)
        self.comboBox_normal_velocity_axis.setVisible(cfd_source)
        self.label_normal_velocity_axis.setVisible(cfd_source)
        self.lineEdit_angular_resolution.setDisabled(cfd_source)
        self.pushButton_spectrum_data.setDisabled(True)
        self.pushButton_waveform_data.setDisabled(True)

        if not cfd_source:           
            self.comboBox_single_revolution.setCurrentText("yes")
            if self.comboBox_data_source.currentText() == "SCORG":
                if self.comboBox_excitation_type.currentText() =="surface velocity -> m/s":
                    self.comboBox_excitation_type.setCurrentText("mass flow rate -> kg/s")
                self.comboBox_compressor_type.setCurrentText("screw")
                self.comboBox_compressor_type.setDisabled(True)
            else:
                self.comboBox_excitation_type.setCurrentText("")
                self.comboBox_compressor_type.setEnabled(True)
            return

        self.comboBox_excitation_type.setCurrentText("surface velocity -> m/s")

    def geometry_selection_callback(self):
        surfaces = app().main_window.selection.geometry_surfaces
        if not surfaces:
            return

        text = ", ".join([str(i) for i in surfaces])
        self.lineEdit_selection_id.setText(text)

        if len(surfaces) == 1:
            surface_id = list(surfaces)[0]
            self.load_property_data(surface_id)

    def load_property_data(self, surface_id: int):
        if self.tabWidget_main.currentIndex() == TabIndex.LIST:
            return

        data = self.properties._get_property("compressor_excitation_waveform", surface=surface_id)
        if not isinstance(data, dict):
            return

        excitation_type = data.get("excitation_type", "mass flow rate")
        excitation_units = data.get("excitation_units", "kg/s")
        excitation_type_label = f"{excitation_type} -> {excitation_units}"

        self.comboBox_data_source.setCurrentText(data.get("data_source", "SCORG"))
        self.comboBox_connection_type.setCurrentText(data.get("connection_type", "discharge"))
        self.comboBox_excitation_type.setCurrentText(excitation_type_label)
        self.comboBox_excitation_mapping.setCurrentText(data.get("excitation_mapping", "surface averaged"))
        self.comboBox_compressor_type.setCurrentText(data.get("compressor_type", "screw"))
        self.comboBox_single_revolution.setCurrentText(data.get("single_revolution", "yes"))

        angular_resolution = data.get("angular_resolution", 1.0)
        self.lineEdit_angular_resolution.setText(f"{angular_resolution}")

        frequency_resolution_req = data.get("frequency_resolution_req", 1.0)
        self.lineEdit_frequency_resolution_required.setText(f"{frequency_resolution_req}")

        if "table_paths" in data.keys():
            table_path = data.get("table_paths")[0]
            self.lineEdit_table_path.setText(table_path)
            self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
            self.lineEdit_frequency_resolution.setText("not calculated")

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
            title = "Invalid input to the analysis setup"
            PrintMessageInput([error_title, title, message])
            line_edit.setStyleSheet("""border-color: rgb(240, 10, 10); border-width: 2px;""")
            return None

        clear_style_sheet(line_edit)

        return value

    def load_compressor_excitation_data(self):
        self.hide()
        self.pushButton_spectrum_data.setDisabled(True)
        self.pushButton_waveform_data.setDisabled(True)

        if self.comboBox_data_source.currentText() == "CFD":
            self.load_cfd_data()
        else:
            self.load_non_cfd_data()

        self.update_data_to_plot_combo_box()

    def load_non_cfd_data(self, direct_load: bool=False):
        self.imported_values = self.load_table(self.lineEdit_table_path, direct_load=direct_load)
        spectrum_data = self.process_signal_spectrum_for_non_cfd_data()
        if spectrum_data is None:
            return
        
        self.pushButton_spectrum_data.setEnabled(True)
        self.pushButton_waveform_data.setEnabled(True)

        df = spectrum_data[0, 0]
        self.lineEdit_frequency_resolution.setText(f"{df}")

    def load_cfd_data(self, table_path: str|None = None):
        if table_path is None:
            table_path = self.load_hdf_file()

        if table_path is None:
            return

        if not Path(table_path).exists():
            return

        self.lineEdit_table_path.setText(table_path)
        self.imported_values = DataImporter.load_cfd_simulation_data_from_hdf_file(table_path)

        angular_resolution = self.imported_values.get("delta_theta")
        if angular_resolution is None:
            return

        self.comboBox_single_revolution.blockSignals(True)
        self.lineEdit_angular_resolution.blockSignals(True)

        self.comboBox_single_revolution.setCurrentText("No")
        self.lineEdit_angular_resolution.setText(f"{angular_resolution}")

        self.comboBox_single_revolution.blockSignals(False)
        self.lineEdit_angular_resolution.blockSignals(False)

        data_label, invert_signal  = self.get_velocity_label_and_signal()
        spectrum_data = self.process_signal_spectrum_for_cfd_data(
            data_label, 
            invert_signal = invert_signal
            )

        if spectrum_data is None:
            return

        self.pushButton_spectrum_data.setEnabled(True)
        self.pushButton_waveform_data.setEnabled(True)
        self.update_velocity_axis_by_coordinates()

        df = spectrum_data[0, 0]
        self.lineEdit_frequency_resolution.setText(f"{df}")

    def update_velocity_axis_by_coordinates(self):
        if self.imported_values is None:
            return
        
        coords = self.imported_values.get("nodal_coordinates")
        if isinstance(coords, np.ndarray):
            min_coords = np.min(coords, axis=0)
            max_coords = np.max(coords, axis=0)
            range_coords = np.abs(max_coords - min_coords)
            indices = np.argsort(range_coords)
            if round(range_coords[indices[0]], 4) == 0:
                axis_labels = ["x-axis (+)", "y-axis (+)", "z-axis (+)"]
                self.comboBox_normal_velocity_axis.setCurrentText(axis_labels[indices[0]])

    def compute_compressor_excitation_spectrum(self):

        self.mass_flow_sdata = None
        self.normal_surface_velocity_sdata = None
        self.pressure_sdata = None
        self.acoustic_impedance_sdata = None

        single_rev = self.comboBox_single_revolution.currentText() == "yes"
        self.lineEdit_angular_resolution.setDisabled(single_rev)

        if self.imported_values is None:
            return True

        if self.comboBox_data_source.currentText() in ["SCORG", "Other"]:
            self.mass_flow_sdata = self.process_signal_spectrum_for_non_cfd_data()
            if self.mass_flow_sdata is None:
                return True

            df = self.mass_flow_sdata[0, 0]
            self.lineEdit_frequency_resolution.setText(f"{df}")

        else:
            data_label, invert_signal  = self.get_velocity_label_and_signal()
            self.normal_surface_velocity_sdata = self.process_signal_spectrum_for_cfd_data(
                data_label, 
                invert_signal = invert_signal
                )

            if self.normal_surface_velocity_sdata is None:
                return True

            df = self.normal_surface_velocity_sdata[0, 0]
            self.lineEdit_frequency_resolution.setText(f"{df}")

    def get_velocity_label_and_signal(self):

        keys_map_cfd = {
            "x" : "velocity_u",
            "y" : "velocity_v",
            "z" : "velocity_w",
            }

        axis_label = self.comboBox_normal_velocity_axis.currentText()
        str_values = axis_label.split("-axis")
        direction = str_values[0]
        signal = str_values[1].replace(" (", "").replace(")", "")
        invert_signal = False if signal == "+" else True

        return keys_map_cfd.get(direction), invert_signal

    def process_signal_spectrum_for_cfd_data(self, data_label: str, invert_signal: bool=False):

        if not isinstance(self.imported_values, dict):
            return None

        time_vector = self.imported_values.get("time_seconds")
        x_data_nodal = self.imported_values.get(data_label)
        if invert_signal:
            x_data_nodal *= -1

        nodal_area = self.imported_values.get("nodal_area")
        weights = nodal_area.reshape(-1, 1) / np.sum(nodal_area)

        if self.comboBox_excitation_mapping.currentText() == "surface averaged":
            x_data = np.sum(x_data_nodal * weights, axis=0)
        else:
            return

        return self.compute_signal_spectrum(time_vector, x_data)

    def process_signal_spectrum_for_non_cfd_data(self):

        if self.imported_values is None:
            return None

        if self.comboBox_single_revolution.currentText() == "yes":
            time_vector = self.imported_values[:, 0]
            mass_flow = self.imported_values[:, 1]
            angular_resoltion = 360 / (time_vector.size - 1)
            self.lineEdit_angular_resolution.setText(f"{angular_resoltion}")

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

    def reset_plotting_attributes(self):

        # reset attributes for waveform plot
        self.time_vector = None
        self.x_data = None

        # reset attributes for spectrum plot
        self.frequencies_vector = None
        self.Xf_data = None

    def compute_signal_spectrum(self, time_vector: np.ndarray, x_data: np.ndarray, export=False, filename=""):

        self.reset_plotting_attributes()

        # the desired frequency resolution
        f_step = self.check_inputs(self.lineEdit_frequency_resolution_required, "Frequency resolution")
        if f_step is None:
            self.lineEdit_frequency_resolution_required.setFocus()
            return None

        f_max = self.check_inputs(self.lineEdit_maximum_frequency, "Maximum frequency")
        if f_max is None:
            self.lineEdit_maximum_frequency.setFocus()
            return None

        # calculat the time step
        dt = time_vector[-1] - time_vector[-2]

        # time to complete one revolution of the male rotor
        T_rev = time_vector[-1] - time_vector[0]

        if self.auralize_signal:
            T_req = self.T_audio
        else:
            # Sampling time to obtain desired frequency resolution
            T_req = 1 / f_step

        # number of repetitions to reach the desired frequency resolution
        N_rep = int(np.ceil(T_req / T_rev))

        # extend the signal by 'N_rep' times to adjust the frequency resolution
        x_data_ext = extend_signal(x_data, N_rep)
        time_ext = np.arange(x_data_ext.size, dtype=float) * dt

        # update attributes for waveform plot
        self.time_vector = time_ext
        self.x_data = x_data_ext
        if self.auralize_signal:
            return None

        # get window type
        window_type = self.comboBox_window_type.currentText()

        # get the correction type
        correction_type = self.comboBox_correction_type.currentText()

        # get window and corerction factor
        window, correction_factor = get_window_and_correction_factor(window_type, correction_type, time_ext.size + 1)

        # windowing the signal
        x_window = x_data_ext * window[:-1]

        # process one-sided spectrum
        freq, Xf = process_one_sided_spectrum(x_window, dt)

        # apply correction factor
        Xf[1:] *= correction_factor
        
        # update attributes for spectrum plot
        self.frequencies_vector = freq
        self.Xf_data = Xf

        # process the frequency resolution
        df = 1 / (x_data_ext.size * dt)

        # output data matrix
        output_data = np.array([freq, np.real(Xf), np.imag(Xf)], dtype=float).T

        # filter the zero-frequency component
        mask_min = freq > 0
        mask_max = freq <= f_max

        if export:
            np.savetxt(filename, np.array([time_ext, x_data_ext]).T, delimiter=",", fmt="%.16e")

        # update the signal processing parameters
        self.update_signal_processing_parameters(
            time_increment = dt,
            revolution_time = T_rev,
            number_of_revolutions = N_rep,
            frequency_resolution = df,
        )

        return output_data[mask_min * mask_max, :]

    def update_signal_processing_parameters(self, **kwargs):
        dt = kwargs.get("time_increment", "--")
        T_rev = kwargs.get("revolution_time", "--")
        N_rev = kwargs.get("number_of_revolutions", "--")
        df = kwargs.get("frequency_resolution", "--")

        self.lineEdit_time_increment.setText(f"{dt}")
        self.lineEdit_revolution_time.setText(f"{T_rev}")
        self.lineEdit_number_of_revolutions.setText(f"{N_rev}")
        self.lineEdit_sampling_time_block.setText(f"{N_rev*T_rev}")
        self.lineEdit_sampling_frequency.setText(f"{1/dt}")
        self.lineEdit_frequency_resolution_plot.setText(f"{df}")

    def tab_event_callback(self):
        tab_list = self.tabWidget_main.currentIndex() == TabIndex.LIST
        self.lineEdit_selection_id.setDisabled(tab_list)
        self.pushButton_apply.setDisabled(tab_list)
        self.pushButton_apply_and_close.setDisabled(tab_list)

        if tab_list:
            self.lineEdit_selection_id.setText("")
            return

        surfaces = app().main_window.selection.geometry_surfaces
        if not surfaces:
            return

        text = ", ".join([str(i) for i in surfaces])
        self.lineEdit_selection_id.setText(text)

    def load_hdf_file(self):

        extensions = ["h5", "hd5", "hdf5"]
        caption = "Choose the HDF file to import the external compressor excitation data"

        imported_path, file_extension = DataImporter.get_file_paths(caption, "imported_table_folder", extensions)
        if not file_extension:
            return

        return imported_path
    
    def load_table(self, line_edit : QLineEdit, direct_load: bool=False):

        imported_values = None
        title = "Error reached while loading 'surface velocity' table"

        try:

            if direct_load:
                imported_table_path = line_edit.text()
                imported_values = DataImporter.read_data_in_file(imported_table_path)[0].data

            else:
                extensions = ["csv", "dat", "txt", "xlsx", "xls"]
                caption = "Choose a table to import the compressor excitation waveform data"
                imported_data = DataImporter.import_single_file("imported_table_folder", extensions, caption)

                if not imported_data:
                    return

                imported_values = imported_data.data
                line_edit.setText(imported_data.path)

            if imported_values.shape[1] < 2:
                message = "The imported table has insufficient number of columns. The mass flow data signal "
                message += "must have two columns in the form: time, and mass flow values."
                PrintMessageInput([error_title, title, message])
                return None

            return imported_values

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            line_edit.setFocus()
            return None

    def save_table_values(self, table_name: str, imported_values: np.ndarray):

        _frequencies = imported_values[:, 0]

        if app().project.model.change_analysis_frequency_setup(list(_frequencies)):
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        update_analysis_setup_in_file(_frequencies)

        real_values = imported_values[:, 1]
        imag_values = imported_values[:, 2]
        data = np.array([_frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def apply_callback(self, close_window: bool = False):
        if self.tabWidget_main.currentIndex() == TabIndex.LIST:
            return

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.model.check_selected_ids(
            input_ids,
            "surfaces",
            domain="acoustic",
        )

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        update_entities_selection(self.lineEdit_selection_id, "surfaces", surface_ids)
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

        self.remove_conflicting_excitations(surface_ids)

        if self.lineEdit_table_path.text() == "":
            title = "Additional inputs required"
            message = "You must select the external compressor excitation "
            message += "table path to proceed with the assignment."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_table_path.setFocus()
            return

        if self.imported_values is None:
            self.imported_values = self.load_table( 
                self.lineEdit_table_path, 
                direct_load = True 
                )

        if self.compute_compressor_excitation_spectrum():
            return

        data_source = self.comboBox_data_source.currentText()
        compressor_type = self.comboBox_compressor_type.currentText()
        (excitation_type, excitation_units) = self.comboBox_excitation_type.currentText().split(" -> ")
        connection_type = self.comboBox_connection_type.currentText()
        excitation_mapping = self.comboBox_excitation_mapping.currentText()
        single_revolution = self.comboBox_single_revolution.currentText()

        angular_resolution = float(self.lineEdit_angular_resolution.text())
        frequency_resolution_req = float(self.lineEdit_frequency_resolution_required.text())

        for surface_id in surface_ids:

            if data_source == "CFD":
                if not isinstance(self.normal_surface_velocity_sdata, np.ndarray):
                    return

                if self.normal_surface_velocity_sdata.shape[1] >= 3:
                    table_name = f"compressor_excitation_waveform_at_surface_{surface_id}"
                    if self.save_table_values(table_name, self.normal_surface_velocity_sdata):
                        self.lineEdit_table_path.setFocus()
                        self.imported_values = None
                        return

                complex_values = get_spectral_data_from_array(self.normal_surface_velocity_sdata)

            else:
                if not isinstance(self.mass_flow_sdata, np.ndarray):
                    return

                if self.mass_flow_sdata.shape[1] >= 3:
                    table_name = f"compressor_excitation_waveform_at_surface_{surface_id}"
                    if self.save_table_values(table_name, self.mass_flow_sdata):
                        self.lineEdit_table_path.setFocus()
                        self.imported_values = None
                        return

                complex_values = get_spectral_data_from_array(self.mass_flow_sdata)

            # table path from imported tabular data
            table_path = self.lineEdit_table_path.text()

            data = {
                "data_source" : data_source,
                "compressor_type" : compressor_type,
                "excitation_type" : excitation_type,
                "excitation_units" : excitation_units,
                "connection_type" : connection_type,
                "excitation_mapping" : excitation_mapping,
                "single_revolution" : single_revolution,
                "angular_resolution" : angular_resolution,
                "frequency_resolution_req" : frequency_resolution_req,
                "table_names" : [table_name],
                "table_paths" : [table_path],
                "values" : [complex_values],
                "element_integration": True,
                }

            self.properties._set_property("compressor_excitation_waveform", data, surface=surface_id)

        self.actions_to_finalize(close_window)

    def remove_conflicting_excitations(self, surface_ids: int | list):

        if isinstance(surface_ids, int):
            surface_ids = [surface_ids]

        labels = [
            "acoustic_pressure",
            "surface_velocity",
            "incident_plane_wave",
            "compressor_excitation_spectrum",
            "compressor_excitation_waveform",
            "reciprocating_compressor_excitation",
            "mass_source",
            ]

        for surface_id in surface_ids:
            for label in labels:
                self.properties._remove_surface_property(label, surface_id)

    def remove_callback(self):

        if self.lineEdit_selection_id.text() == "":
            return

        surface_id = int(self.lineEdit_selection_id.text())

        self.properties._remove_surface_property("compressor_excitation_waveform", surface_id)
        self.actions_to_finalize()

    def reset_callback(self):

        title = "External comrpressor excitation reset"
        message = "Would you like to remove the all external compressor excitations from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            self.properties._reset_property("compressor_excitation_waveform")
            self.actions_to_finalize()

    def actions_to_finalize(self, close_window: bool = False):
        self.load_model_info()
        app().project.update_model_properties_file()
        app().main_window.update_info_text()
        app().main_window.update_symbols()

        if close_window:
            self.close()

    def update_tabs_visibility(self):

        for key in self.properties.surface_properties:
            property, *args = key
            if property != "compressor_excitation_waveform":
                continue

            self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
            return

        self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)

    def on_click_item(self, item):
        if item.text(0) != "":
            self.pushButton_remove.setDisabled(False)
            surface_id = int(item.text(0))
            self.lineEdit_selection_id.setText(item.text(0))
            app().main_window.selection.set_geometry_selection(surfaces=[surface_id])

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def load_model_info(self):
        self.treeWidget_surface_velocity.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property != "compressor_excitation_waveform":
                continue

            data_source = data.get("data_source")
            angular_resolution = data.get("angular_resolution")

            item = QTreeWidgetItem([str(surface_id), data_source, str(angular_resolution)])
            for i in range(3):
                item.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_surface_velocity.addTopLevelItem(item)

        self.update_tabs_visibility()

    def get_unit_label_for_cfd_data(self, data_label: str):
        if "velocity" in data_label:
            return "m/s"
        elif data_label == "pressure":
            return "bar"
        elif data_label == "temperature":
            return "K"
        else:
            return "--"

    def update_data_to_plot_combo_box(self):

        cfd_data_keys = [
            "pressure",
            "temperature",
            "velocity_u",
            "velocity_v",
            "velocity_w",
            ]

        self.comboBox_data_to_plot.clear()

        if self.comboBox_data_source.currentText() == "CFD":
            if isinstance(self.imported_values, dict):
                self.comboBox_data_to_plot.clear()
                self.comboBox_data_to_plot.setEnabled(True)

                for key in self.imported_values.keys():
                    if key in cfd_data_keys:
                        data_unit = self.get_unit_label_for_cfd_data(key)
                        item_text = f"{key} -> {data_unit}"
                        self.comboBox_data_to_plot.addItem(item_text)

        else:
            excitation_type = self.comboBox_excitation_type.currentText()
            self.comboBox_data_to_plot.addItem(excitation_type)
            self.comboBox_data_to_plot.setDisabled(True)

    def process_signals_to_plot(self):
        if self.comboBox_data_source.currentText() == "CFD":
            cfd_data_key = self.comboBox_data_to_plot.currentText().split(" -> ")[0]
            self.process_signal_spectrum_for_cfd_data(cfd_data_key)
        else:
            self.process_signal_spectrum_for_non_cfd_data()

    def join_spectrum_data(self):

        self.model_results.clear()

        excitation_type, unit_label = self.comboBox_data_to_plot.currentText().split(" -> ")
        plot_type = excitation_type.capitalize()

        f_max = self.spinBox_maximum_frequency.value()
        mask = self.frequencies_vector < f_max

        key = ("compressor", "excitation")
        legend_label = "compressor excitation signal"
        title = f"{excitation_type} spectrum".capitalize()

        self.model_results[key] = { 
            "x_data" : self.frequencies_vector[mask],
            "y_data" : self.Xf_data[mask],
            "x_label" : "Frequency [Hz]",
            "y_label" : plot_type,
            "title" : title,
            "data_type" : plot_type.lower(),
            "legend" : legend_label,
            "unit" : unit_label,
            "color" : (0,0,1),
            "linestyle" : "-"  
            }

    def join_waveform_data(self):

        self.model_results.clear()

        excitation_type, unit_label = self.comboBox_data_to_plot.currentText().split(" -> ")
        plot_type = excitation_type.capitalize()

        key = ("compressor", "excitation")
        legend_label = "compressor excitation signal"
        title = f"{excitation_type} waveform".capitalize()

        self.model_results[key] = { 
            "x_data" : self.time_vector,
            "y_data" : self.x_data,
            "x_label" : "Time [s]",
            "y_label" : plot_type,
            "title" : title,
            "data_type" : plot_type.lower(),
            "legend" : legend_label,
            "unit" : unit_label,
            "color" : (0,0,1),
            "linestyle" : "-" ,
            }

    def plot_spectrum_data_callback(self):
        if self.imported_values is None:
            return
        
        if isinstance(self.spectrum_plotter, FrequencyResponsePlotter):
            self.spectrum_plotter.close()

        self.process_signals_to_plot()
        self.join_spectrum_data()

        self.spectrum_plotter = FrequencyResponsePlotter(close_dialogs=True)
        self.spectrum_plotter._set_model_results_data_to_plot(self.model_results)
        
    def plot_waveform_data_callback(self):
        if self.imported_values is None:
            return

        if isinstance(self.waveform_plotter, FrequencyResponsePlotter):
            self.waveform_plotter.close()

        self.process_signals_to_plot()
        self.join_waveform_data()

        self.waveform_plotter = FrequencyResponsePlotter(close_dialogs=True)
        self.waveform_plotter.comboBox_data_format.setCurrentIndex(DataFormat.REAL)
        self.waveform_plotter.data_format_changed_callback()
        self.waveform_plotter._set_model_results_data_to_plot(self.model_results)

    def reproduce_audio_callback(self):
        import sounddevice as sd

        if self.x_data is None:
            return

        if sd._last_callback is not None:
            if sd.get_stream().active:
                sd.stop()
                return

        # frequency sampling for audio
        fs_audio = 44100

        self.auralize_signal = True
        self.process_signals_to_plot()

        time_vector_audio = np.arange(0, self.T_audio, 1/fs_audio)
        audio_signal = np.interp(time_vector_audio, self.time_vector, self.x_data)
        
        # remove dc component
        audio_signal -= np.average(audio_signal)

        # rescale signal to oscillate between -1 and 1
        audio_signal /= np.max(np.abs(audio_signal))

        ## save the signal to a WAV file
        # file_name = "compressor_signal.wav"
        # wavfile.write(file_name, fs_audio, (audio_signal * 32767).astype(np.int16)) # Scale for 16-bit PCM

        # create a hann window for fading purposes
        hann_window = hann(2*self.fading_samples)

        # deepcopy the audio signal
        audio_signal_faded = deepcopy(audio_signal)

        # apply the fade-in to audio signal
        N_ws = self.fading_samples
        audio_signal_faded[:N_ws] = audio_signal_faded[:N_ws] * hann_window[:N_ws]
        
        # apply the fade-out to audio signal
        N_fout = audio_signal_faded.size - N_ws
        audio_signal_faded[N_fout:] = audio_signal_faded[N_fout:] * hann_window[N_ws:]

        # play the signal
        sd.play(audio_signal_faded, fs_audio)

        self.auralize_signal = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            return

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)