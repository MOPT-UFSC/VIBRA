from vibra.engine import AnalysisID
from vibra.engine import HarmonicAnalysisSetup
from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.ui_generated.model.setup.acoustic.compressor_excitation_spectrum_inputs_ui import CompressorExcitationSpectrumInputs_UI

import numpy as np

error_title = "Error"


class CompressorExcitationSpectrumInputs(CompressorExcitationSpectrumInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.project = app().project
        self.model = app().new_project.model
        self.mesh = app().new_project.model.mesh
        self.properties = app().new_project.model.properties

        self._initialize()
        self._config_window()
        self._config_widgets()
        self._create_connections()

        self.load_model_info()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.complex_values = None
        self.imported_values = None
        self.keep_window_open = True

    def _config_widgets(self):
        #
        for i, w in enumerate([120]):
            self.treeWidget_compressor_excitation_spectrum.setColumnWidth(i, w)
            self.treeWidget_compressor_excitation_spectrum.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_load_table.clicked.connect(self.load_compressor_excitation_spectrum_data)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_compressor_excitation_spectrum.itemClicked.connect(self.on_click_item)
        self.treeWidget_compressor_excitation_spectrum.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

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
        if self.tabWidget_main.currentIndex() != 0:
            return

        data = self.properties._get_property("compressor_excitation_spectrum", surface=surface_id)
        if not isinstance(data, dict):
            return

        excitation_type = data.get("excitation_type", "mass flow rate")
        excitation_units = data.get("excitation_units", "kg/s")
        excitation_type_label = f"{excitation_type} -> {excitation_units}"

        self.comboBox_connection_type.setCurrentText(data.get("connection_type", "discharge"))
        self.comboBox_excitation_type.setCurrentText(excitation_type_label)
        self.comboBox_compressor_type.setCurrentText(data.get("compressor_type", "screw"))

        if "table_paths" in data.keys():
            table_path = data.get("table_paths")[0]
            self.lineEdit_table_path.setText(table_path)
            self.tabWidget_main.setCurrentIndex(0)

    def tab_event_callback(self):
        if self.tabWidget_main.currentIndex() == 1:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_attribute.setDisabled(True)
            return

        self.lineEdit_selection_id.setDisabled(False)
        self.pushButton_attribute.setEnabled(True)

        surfaces = app().main_window.selection.geometry_surfaces
        if not surfaces:
            return

        text = ", ".join([str(i) for i in surfaces])
        self.lineEdit_selection_id.setText(text)

    def on_click_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))
        self.remove_callback()

    def load_model_info(self):
        self.treeWidget_compressor_excitation_spectrum.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "compressor_excitation_spectrum":

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
                self.treeWidget_compressor_excitation_spectrum.addTopLevelItem(new)

        self.update_tabs_visibility()

    def load_table(self, lineEdit : QLineEdit, direct_load=False):

        title = "Error reached while loading compressor excitation data"
        imported_file = None

        try:
            if direct_load:
                imported_table_path = lineEdit.text()
                imported_file = np.loadtxt(imported_table_path, delimiter=",")

            else:
                extensions = ["csv", "dat", "txt", "xlsx", "xls"]
                caption = "Choose a table to import the compressor excitation spectrum data"
                imported_data = DataImporter.import_single_file("imported_table_folder", extensions, caption)

                if not imported_data:
                    return

                imported_file = imported_data.data
                lineEdit.setText(imported_data.path)

            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have three columns in the form: frequencies, real and imaginary values."
                PrintMessageInput([error_title, title, message])
                return None

            return imported_file

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            lineEdit.setFocus()
            return None

    def save_table_values(self, table_name: str, imported_values: np.ndarray):
        
        # filter the zero-frequency component
        mask = imported_values[:, 0] > 0
        imported_values = imported_values[mask, :]

        # define the frequencies vector
        frequencies = imported_values[:, 0]

        if app().new_project.model.change_analysis_frequency_setup(list(frequencies)):
            self.hide()
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        self.update_analysis_setup_in_file(frequencies)

        # real values vector
        real_values = imported_values[:, 1]
        
        # imaginary values vector
        imag_values = imported_values[:, 2]

        # complex values vector
        self.complex_values = real_values + 1j * imag_values

        data = np.array([frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def update_analysis_setup_in_file(self, frequencies: np.ndarray):
        f_min = frequencies[0]
        f_max = frequencies[-1]
        f_step = frequencies[1] - frequencies[0] 

        analysis_setup = app().new_project.model.new_analysis_setup
        if isinstance(analysis_setup, HarmonicAnalysisSetup):
            new_analysis_setup = analysis_setup.replace(
                f_min=f_min,
                f_max=f_max,
                f_step=f_step,
            )
        else:
            new_analysis_setup = HarmonicAnalysisSetup(f_min, f_max, f_step)

        app().new_project.configure_analysis(
            AnalysisID.ACOUSTIC_HARMONIC,
            new_analysis_setup,
        )

    def load_compressor_excitation_spectrum_data(self):
        self.imported_values = self.load_table(self.lineEdit_table_path)

    def attribute_callback(self):

        if self.tabWidget_main.currentIndex() != 0:
            return

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(
            input_ids, 
            selection = "surfaces"
            )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        self.remove_conflicting_excitations(surface_ids)

        if self.lineEdit_table_path.text() == "":
            self.hide()
            title = "Additional inputs required"
            message = "You must inform at least one mass flow rate\n"
            message += "table path before confirming the input!"
            PrintMessageInput([error_title, title, message])
            self.lineEdit_table_path.setFocus()
            return

        compressor_type = self.comboBox_compressor_type.currentText()
        (excitation_type, excitation_units) = self.comboBox_excitation_type.currentText().split(" -> ")
        connection_type = self.comboBox_connection_type.currentText()

        if self.imported_values is None:
            self.imported_values = self.load_table( 
                self.lineEdit_table_path, 
                direct_load = True,
                )

        for surface_id in surface_ids:

            if isinstance(self.imported_values, np.ndarray):
                if self.imported_values.shape[1] >= 3:

                    table_name = f"compressor_excitation_spectrum_at_surface_{surface_id}"
                    if self.save_table_values(table_name, self.imported_values):
                        self.lineEdit_table_path.setFocus()
                        self.complex_values = None
                        self.imported_values = None
                        return

            else:
                return

            table_path = self.lineEdit_table_path.text()

            data = {
                "compressor_type" : compressor_type,
                "excitation_type" : excitation_type,
                "excitation_units" : excitation_units,
                "connection_type" : connection_type,
                "table_paths" : [table_path],
                "table_names" : [table_name],
                "values" : [self.complex_values],
                "nodal_attribution": False,
                "averaged": False,
                }

            self.properties._set_property("compressor_excitation_spectrum", data, surface=surface_id)

        self.actions_to_finalize()

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)

        if table_names:
            app().new_project.update_model_properties_file()

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
                table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_id : list):
        table_names = self.properties.get_property_related_table_names("compressor_excitation_spectrum", surface_id, "surfaces")
        self.process_table_file_removal(table_names)

    def remove_callback(self):

        if self.lineEdit_selection_id.text() != "":

            surface_id = int(self.lineEdit_selection_id.text())
            self.remove_table_files_from_surfaces(surface_id)

            self.properties._remove_surface_property("compressor_excitation_spectrum", surface_id)
            self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Compressor excitation reseting"
        message = "Would you like to remove the all compressor excitations in frequency domain from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            surface_ids = list()
            for (property, *args), data in self.properties.surface_properties.items():
                if property == "compressor_excitation_spectrum":
                    surface_id = args[0]
                    surface_ids.append(surface_id)

            self.remove_table_files_from_surfaces(surface_ids)

            self.properties._reset_property("compressor_excitation_spectrum")
            self.actions_to_finalize()

    def actions_to_finalize(self):
        self.load_model_info()
        self.check_model_frequency_controls()
        app().new_project.update_model_properties_file()
        app().main_window.update_info_text()
        app().main_window.update_symbols()

    def check_model_frequency_controls(self):

        properties = [
            "acoustic_pressure",
            "surface_velocity",
            "specific_impedance",
            "compressor_excitation_spectrum",
            "compressor_excitation_waveform",
            "reciprocating_compressor_excitation",
            ]

        for key, data in self.properties.surface_properties.items():
            property, _ = key
            if property in properties:
                if "table_names" in data.keys():
                    return
        
        # No idea of what it does
        app().new_project.configure_analysis(
            app().new_project.current_analysis_id,
            app().new_project.model.new_analysis_setup,
        )


    def update_tabs_visibility(self):

        for key in self.properties.surface_properties.keys():
            property, *args = key
            if property == "compressor_excitation_spectrum":
                self.tabWidget_main.setTabVisible(1, True)
                return

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_main.setTabVisible(1, False)

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