import logging
from collections import defaultdict
from pathlib import Path
from time import sleep

import numpy as np
from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QFileDialog, QLineEdit

from vibra import app
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing, HarmonicAnalysisSetup
from vibra.interface import error_title
from vibra.interface.common.common_interface import mesher_interface_callback
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.utils import clear_style_sheet
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.ui_generated.model.acoustic.element_transfer.acoustic_transfer_element_inputs_ui import AcousticTransferElementInputs_UI


class AcousticTransferElementInputs(AcousticTransferElementInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self._config_window()
        self._configure_validators()
        self._reset_variables()
        self._configure_qt_variables()
        self._create_connections()

        self._load_analysis_setup()
        self.geometry_selection_callback()

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

    @property
    def solution(self):
        return app().project.model.solution

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _configure_validators(self):
        validator = StrictDoubleValidator(0, 1e5, 8)
        self.lineEdit_fmin.setValidator(validator)
        self.lineEdit_fmax.setValidator(validator)
        self.lineEdit_fstep.setValidator(validator)

    def _reset_variables(self):
        self.keep_window_open = True
        self.analysis_setup = None
        self.analysis_setup = None
        self.frequencies = None

        self.surface_ids = list()
        self.element_transfer_data = dict()

        self.highlight_style_sheet = """border-color: rgb(32, 207, 255); border-width: 2px;"""

    def _configure_qt_variables(self):
        self.current_line_edit = self.lineEdit_output_selected_id
        self.tabWidget_main.setTabVisible(1, False)

    def _create_connections(self):
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_process_data.clicked.connect(self.process_data_callback)
        self.pushButton_invert_selection.clicked.connect(self.invert_selection_callback)
        self.pushButton_search.clicked.connect(self.search_callback)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.clickable(self.lineEdit_input_selected_id).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_output_selected_id).connect(self.lineEdit_2_clicked)

    def geometry_selection_callback(self):

        selected_faces = app().main_window.selection.geometry_surfaces
        if len(selected_faces) != 1:
            return

        if isinstance(self.current_line_edit, QLineEdit):
            _selected_faces = [str(i) for i in selected_faces]
            self.current_line_edit.setText(_selected_faces[0])

    def invert_selection_callback(self):

        if self.check_typed_ids():
            return

        input_id = self.lineEdit_input_selected_id.text()
        output_id = self.lineEdit_output_selected_id.text()

        self.lineEdit_output_selected_id.setText(input_id)
        self.lineEdit_input_selected_id.setText(output_id)

    def clickable(self, widget):
        class Filter(QObject):
            clicked = Signal()

            def eventFilter(self, obj, event):
                if obj == widget and event.type() == QEvent.MouseButtonRelease and obj.rect().contains(event.pos()):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def lineEdit_1_clicked(self):
        self.current_line_edit = self.lineEdit_input_selected_id
        self.highlight_line_edit()

    def lineEdit_2_clicked(self):
        self.current_line_edit = self.lineEdit_output_selected_id
        self.highlight_line_edit()

    def highlight_line_edit(self):
        line_edits = [self.lineEdit_input_selected_id, self.lineEdit_output_selected_id]
        clear_style_sheet([line_edit for line_edit in line_edits if line_edit is not self.current_line_edit])
        self.current_line_edit.setStyleSheet(self.highlight_style_sheet)

    def _load_analysis_setup(self):
        analysis_setup = self.analysis_setup
        if not isinstance(analysis_setup, HarmonicAnalysisSetup):
            return

        self.lineEdit_fmin.setText(str(analysis_setup.f_min))
        self.lineEdit_fmax.setText(str(analysis_setup.f_max))
        self.lineEdit_fstep.setText(str(analysis_setup.f_step))

    def search_callback(self):

        caption = "Set a file name to export the acoustic element transfer data"

        last_path = app().config.get_last_folder_for(
            "exported_data_folder",
            default=Path().home(),
        )

        _filter = "Spreadsheet (*.xlsx);; Spreadsheet (*.xls)"

        path, check = QFileDialog.getSaveFileName(self, caption, str(last_path), filter=_filter)

        if not check:
            return True

        file_extension = self.get_file_extension_from_string(check)

        if file_extension not in path:
            path += f".{file_extension}"

        self.lineEdit_spreadsheet_path.setText(path)
        app().config.write_last_folder_path_in_file("exported_data_folder", path)

    def get_file_extension_from_string(self, string: str) -> str:
        return string.split(".")[1][:-1]

    def check_typed_ids(self):

        line_edits = [
            self.lineEdit_input_selected_id,
            self.lineEdit_output_selected_id,
        ]

        self.surface_ids.clear()
        for line_edit in line_edits:
            surface_id, error_data = self.mesh.check_selected_ids(
                line_edit.text(),
                selection="surfaces",
                single_id=True,
            )

            if error_data is not None:
                line_edit.setFocus()
                line_edit.selectAll()
                PrintMessageInput(error_data)
                return True

            self.surface_ids.append(surface_id)

    def check_frequency_entries(self):

        line_edits = [
            self.lineEdit_fmin,
            self.lineEdit_fmax,
            self.lineEdit_fstep,
        ]

        freq_data = list()

        for line_edit in line_edits:
            if line_edit.text() == "":
                line_edit.setFocus()
                line_edit.setStyleSheet(self.highlight_style_sheet)
                return True

            clear_style_sheet(line_edit)
            freq_data.append(float(line_edit.text()))

        [f_min, f_max, f_step] = freq_data

        if f_max < f_min + f_step:
            title = "Invalid frequency setup"
            message = "The maximum frequency (fmax) must be greater than \n"
            message += "the sum between minimum frequency (fmin) and \n"
            message += "frequency resolution (df)."
            PrintMessageInput([error_title, title, message])
            return True

        ## Define the analysis frequency setup
        self.analysis_setup = self.model.get_harmonic_analysis_setup(
            analysis_id=AnalysisID.ACOUSTIC_HARMONIC,
            frequency_spacing=FrequencySpacing.EQUALLY_DISTRIBUTED,
            f_min=f_min,
            f_max=f_max,
            f_step=f_step,
        )

        self.frequencies = self.analysis_setup.get_frequencies()

    def process_data_callback(self):
        self.hide()
        self.element_transfer_data.clear()

        if self.lineEdit_spreadsheet_path.text() == "":
            if self.search_callback():
                return

        if self.check_typed_ids():
            return

        if self.check_frequency_entries():
            return True

        app().project.configure_analysis(self.analysis_setup)

        if not app().project.model.is_there_a_valid_mesh():
            if mesher_interface_callback(self, close_after_generate=True):
                return

        # integrate the areas of the selected surfaces
        self.process_areas()

        app().main_window.selection.set_geometry_selection()

        def compute_model_solution():
            for i, surface_id in enumerate(self.surface_ids):
                logging.info(f"Solving model [{5 + 50 * i}/100]...")
                sleep(1)

                # remove all model excitations and acoustic impedances
                self.remove_model_excitations_and_impedances()

                # define the acoustic excitation
                self.set_surface_velocity(surface_id)

                # compute the model solution for the current excitation
                app().project.solve_acoustic_harmonic_analysis()

                # export the obtained data for the current excitation
                self.join_model_data(surface_id)

            logging.info("Exporting the admittance matrix data... [20/100]")
            sleep(0.5)

            logging.info("Exporting the admittance matrix data... [90/100]")
            self.export_data_callback()

            sleep(0.5)
            logging.info("Exporting the admittance matrix data... [100/100]")

        LoadingWindow(compute_model_solution).run()

        # remove all model excitations and acoustic impedances
        self.remove_model_excitations_and_impedances()

        # reset model solution data
        app().main_window.analysis_toolbar.reset_solution(True)

        app().main_window.results_viewer_widget.results_viewer_items.update_items()
        self.print_final_message()

    def remove_model_excitations_and_impedances(self):

        model_excitations = [
            "acoustic_pressure",
            "surface_velocity",
            "reciprocating_compressor_excitation",
            "compressor_excitation_spectrum",
            "compressor_excitation_waveform",
            "incident_plane_wave",
            "mass_source",
        ]

        model_impedances = [
            "specific_impedance",
            "absorption_surface",
        ]

        properties_to_remove = defaultdict(list)
        for property in model_excitations:
            for key in self.properties.surface_properties.keys():
                if key[0] == property:
                    properties_to_remove[key[0]].append(key[1])

        for property in model_impedances:
            for key in self.properties.surface_properties.keys():
                if key[0] == property and key[1] in self.surface_ids:
                    properties_to_remove[key[0]].append(key[1])

        self.remove_table_data(properties_to_remove)

    def remove_table_data(self, properties_to_remove: dict):
        if not properties_to_remove:
            return

        table_names = list()
        for property_label, surface_ids in properties_to_remove.items():
            for table_name in self.properties.get_property_related_table_names(property_label, surface_ids, "surfaces"):
                if table_name in table_names:
                    continue

                table_names.append(table_name)

            for surface_id in surface_ids:
                self.properties._remove_surface_property(property_label, surface_id)

        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)

        if table_names:
            app().project.update_model_properties_file()

    def set_surface_velocity(self, surface_id: int):

        data = {
            "real_values": [1.0],
            "imag_values": [0.0],
            "element_integration": True,
        }

        self.properties._set_property("surface_velocity", data, surface=surface_id)

        app().project.update_model_properties_file()
        # app().main_window.selection.set_geometry_selection(surfaces=[surface_id])

    def process_areas(self):

        def function_callback():
            logging.info("Processing area... [60/100]")
            self.mesh.process_face_elements_connected_to_nodes(self.surface_ids)

        LoadingWindow(function_callback).run()

    def get_response(self, excitation_id: int, surface_id: int):

        surface_nodes = self.mesh.get_nodes_from_surface(surface_id)

        rho, _ = self.model.get_fluid_properties_from_surface(surface_id)
        if rho is None:
            return None

        area, surface_velocity = self.get_area_and_surface_velocity(excitation_id)

        if area is None:
            title = "Surface velocity not detected"
            message = f"The surface velocity associated to the surface #{surface_id} has not been found. "
            message += "It is recommended to check the acoustic model excitations and change the excitation "
            message += "surface ID to proceed with the transfer function data exportation."
            PrintMessageInput([error_title, title, message])
            app().main_window.set_input_widget(self)
            return None

        # Note: the negative signal ensures the assembly consistency of acoustic transfer element
        volume_velocity = -surface_velocity * area

        node_ids = np.sort(surface_nodes)
        pressures = self.solution.acoustic_solution[node_ids, :]
        avg_pressure = np.average(pressures, axis=0)

        return avg_pressure / volume_velocity

    def get_area_and_surface_velocity(self, surface_id: int):
        for key, data in self.properties.surface_properties.items():
            if key[0] != "surface_velocity":
                continue

            if key[1] != surface_id:
                continue

            real_values = np.array(data["real_values"])
            imag_values = np.array(data["imag_values"])
            surface_velocity = real_values + 1j * imag_values

            area = self.mesh.surface_area_from_element_integration[surface_id]

            return area, surface_velocity

        return None, None

    def join_model_data(self, excitation_id: int):

        for k, response_id in enumerate(self.surface_ids):
            data = self.get_response(excitation_id, response_id)
            if data is None:
                self.element_transfer_data.clear()
                return

            if response_id == self.surface_ids[0]:
                resp_id = 1
            else:
                resp_id = 2

            if excitation_id == self.surface_ids[0]:
                excit_id = 1
            else:
                excit_id = 2

            unit_label = "Pa/m³/s"
            data_type = "transfer_function"
            y_label = "Transfer function H(f)"

            data_name = f"transfer_function_h{resp_id}{excit_id}"
            key = (data_name, tuple(self.surface_ids))

            self.element_transfer_data[key] = {
                "x_data": self.frequencies,
                "y_data": data,
                "x_label": "Frequency [Hz]",
                "y_label": y_label,
                "title": "Element transfer data",
                "data_type": data_type,
                "legend": "element transfer data",
                "unit": unit_label,
                "color": (0, 0, 1),
                "linestyle": "-",
            }

    def export_data_in_spreadsheet_format(self, export_path: str):

        from pandas import ExcelWriter
        from polars import DataFrame

        with ExcelWriter(export_path) as writer:
            for key, data in self.element_transfer_data.items():
                if not isinstance(data, dict):
                    continue

                selection_type, selection_id = key
                sheet_name = f"{selection_type}_{selection_id}"

                unit = data["unit"]
                x_data = data["x_data"]
                y_data = data["y_data"]
                x_label = data.get("x_label")
                y_label = data.get("y_label")

                if isinstance(y_data[0], complex):
                    header = [x_label, f"{y_label} - real [{unit}]", f"{y_label} - imaginary [{unit}]", f"Absolute [{unit}]"]
                    data_to_export = np.array([x_data, np.real(y_data), np.imag(y_data), np.abs(y_data)]).T

                else:
                    data_type = data["data_type"]
                    header = [x_label, f"{data_type.capitalize()} [{unit}]"]
                    data_to_export = np.array([x_data, y_data]).T

                df = DataFrame(data_to_export, schema=header)
                df.to_pandas().to_excel(writer, sheet_name=sheet_name, index=False)

    def export_data_callback(self):
        if self.element_transfer_data:
            path = self.lineEdit_spreadsheet_path.text()
            self.export_data_in_spreadsheet_format(path)

    def print_final_message(self):

        window_title = "Vibra"
        title = "Data exporting finished"
        message = "The acoustic transfer element data exportation has been finished."
        PrintMessageInput([window_title, title, message])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.export_data_callback()

        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)
