from PySide6.QtWidgets import QFileDialog, QLineEdit
from PySide6.QtCore import Qt, QEvent, QObject, Signal
from PySide6.QtGui import QCloseEvent, QColor

from vibra.engine import AnalysisID
from vibra import app
from vibra.interface.formatters.icons import change_icon_color_for_widgets
from vibra.interface.ui_generated.model.setup.acoustic.acoustic_transfer_element_inputs_ui import AcousticTransferElementInputs_UI
from vibra.interface.mesh.set_mesh_setup_inputs import MeshSetupInputs
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow

import logging
import numpy as np

from collections import defaultdict
from pathlib import Path
from time import sleep

window_title_1 = "Error"
window_title_2 = "Warning"


class AcousticTransferElementInputs(AcousticTransferElementInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.action_model_workspace_callback()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._reset_variables()
        self._configure_qt_variables()
        self._create_connections()

        self._paint_icons()
        self._load_analysis_setup()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Acoustic transfer element data")

    def _reset_variables(self):
        self.keep_window_open = True
        self.element_transfer_data = dict()

    def _configure_qt_variables(self):
        self.current_lineEdit = self.lineEdit_output_selected_id
        self.tabWidget_main.setTabVisible(1, False)

    def _create_connections(self):
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_process_data.clicked.connect(self.process_data_callback)
        self.pushButton_invert_selection.clicked.connect(self.invert_selection_callback)
        self.pushButton_search.clicked.connect(self.search_callback)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        app().main_window.theme_changed.connect(self._paint_icons)
        #
        self.clickable(self.lineEdit_input_selected_id).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_output_selected_id).connect(self.lineEdit_2_clicked)

    def geometry_selection_callback(self):

        selected_faces = app().main_window.selected_geometry_surfaces

        if len(selected_faces) == 1:
            if isinstance(self.current_lineEdit, QLineEdit):
                _selected_faces = [str(i) for i in selected_faces]
                self.current_lineEdit.setText(_selected_faces[0])

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
        self.current_lineEdit = self.lineEdit_input_selected_id

    def lineEdit_2_clicked(self):
        self.current_lineEdit = self.lineEdit_output_selected_id

    def _load_analysis_setup(self):

        data = self.project.analysis_setup
        if isinstance(data, dict):

            if "f_min" in data.keys():
                self.f_min = data["f_min"]
                self.lineEdit_fmin.setText(str(self.f_min))

            if "f_max" in data.keys():
                self.f_max = data["f_max"]
                self.lineEdit_fmax.setText(str(self.f_max))

            if "f_step" in data.keys():
                self.f_step = data["f_step"]
                self.lineEdit_fstep.setText(str(self.f_step))

    def search_callback(self):

        caption = "Set a file name to export the acoustic element transfer data"

        last_path = app().config.get_last_folder_for("exported_data_folder")
        if last_path is None:
            last_path = str(Path().home())

        _filter = "Spreadsheet (*.xlsx);; Spreadsheet (*.xls)"

        path, check = QFileDialog.getSaveFileName( 
                                                  self, 
                                                  caption, 
                                                  last_path, 
                                                  filter = _filter
                                                  )

        if not check:
            return True

        self.lineEdit_spreadsheet_path.setText(path)
        app().config.write_last_folder_path_in_file("exported_data_folder", path)

    def check_typed_ids(self):

        input_selected_id = self.lineEdit_input_selected_id.text()
        self.input_selection_id, error_data = self.mesh.check_selected_ids(
                                                                            input_selected_id, 
                                                                            selection = "surfaces",
                                                                            single_id = True,
                                                                            )

        if error_data is not None:
            self.hide()
            self.lineEdit_input_selected_id.setFocus()
            self.lineEdit_input_selected_id.selectAll()
            PrintMessageInput(error_data)
            return

        output_selected_id = self.lineEdit_output_selected_id.text()
        self.output_selection_id, error_data = self.mesh.check_selected_ids(  
                                                                            output_selected_id, 
                                                                            selection = "surfaces", 
                                                                            single_id = True  
                                                                            )

        if error_data is not None:
            self.hide()
            self.lineEdit_input_selected_id.setFocus()
            self.lineEdit_input_selected_id.selectAll()
            PrintMessageInput(error_data)
            return

    def check_frequency_entries(self):

        str_fmin = self.lineEdit_fmin.text()
        stop, input_fmin = self.check_inputs(str_fmin, "'minimum frequency'")
        if stop:
            self.lineEdit_fmin.setFocus()
            self.lineEdit_fmin.selectAll()
            return True

        str_fmax = self.lineEdit_fmax.text()
        stop, input_fmax = self.check_inputs(str_fmax, "'maximum frequency'")
        if stop:
            self.lineEdit_fmax.setFocus()
            self.lineEdit_fmax.selectAll()
            return True

        str_fstep = self.lineEdit_fstep.text()
        stop, input_fstep = self.check_inputs(str_fstep, "'frequency resolution (df)'")
        if stop:
            self.lineEdit_fstep.setFocus()
            self.lineEdit_fstep.selectAll()
            return True

        if input_fmax < input_fmin + input_fstep:
            title = "Invalid frequency setup"
            message = "The maximum frequency (fmax) must be greater than \n"
            message += "the sum between minimum frequency (fmin) and \n"
            message += "frequency resolution (df)."
            PrintMessageInput([window_title_1, title, message])
            return True

        self.frequencies = np.arange(input_fmin, input_fmax + input_fstep, input_fstep)

        self.analysis_setup["f_min"] = input_fmin
        self.analysis_setup["f_max"] = input_fmax
        self.analysis_setup["f_step"] = input_fstep
        self.analysis_setup["frequencies"] = self.frequencies

    def check_inputs(self, input_value: str, label: str):

        message = ""
        title = "Invalid input to the analysis setup"
        if input_value != "":
            try:

                _value = input_value.replace(",", ".")
                value = float(_value)

                if value <= 0:
                    message = f"Insert a positive value to the {label}."
                    message += "\n\nNote: zero value is not allowed."

            except Exception as _err:
                message = "Dear user, you have typed and invalid value at the \n"
                message += f"{label} input field.\n\n"
                message += str(_err)

        else:
            message = f"Insert some value at the {label} input field."

        if message != "":
            PrintMessageInput([window_title_1, title, message])
            return True, None

        else:
            return False, value

    def configure_analysis(self):

        self.analysis_setup = {"analysis_id": AnalysisID.ACOUSTIC_HARMONIC}

        if self.check_frequency_entries():
            return True

        app().project.set_analysis_setup(self.analysis_setup)
        app().project.create_solver()
        app().project.file.write_analysis_setup_in_file(self.analysis_setup)

    def process_data_callback(self):
        """
        """
        self.hide()
        self.element_transfer_data.clear()

        if self.lineEdit_spreadsheet_path.text() == "":
            if self.search_callback():
                return

        if self.check_typed_ids():
            return
        else:
            self.process_areas()

        if self.configure_analysis():
            return   

        if not app().project.model.generated_mesh:
            obj = MeshSetupInputs()
            if obj.complete:
                app().main_window.update_plots()
            else:
                return
        
        app().main_window.set_geometry_selection()

        def callback():
            for i, surface_id in enumerate([self.input_selection_id, self.output_selection_id]):

                logging.info(f"Solving model [{5+50*i}/100]...")
                sleep(1)

                self.remove_model_excitations()
                self.set_surface_velocity(surface_id)
                self.project.solve_acoustic_harmonic_analysis()
                self.join_model_data(surface_id)

            logging.info("Exporting the admittance matrix data... [20/100]")
            sleep(0.5)

            logging.info("Exporting the admittance matrix data... [90/100]")
            self.export_data_callback()

            sleep(0.5)
            logging.info("Exporting the admittance matrix data... [100/100]")

        LoadingWindow(callback).run()

        app().main_window.menu_widget.update_items()
        self.print_final_message()

    def remove_model_excitations(self):

        properties_to_remove = defaultdict(list)
        for property in ["acoustic_pressure", "surface_velocity", "compressor_excitation", "specific_impedance"]:
            for key in self.properties.surface_properties.keys():
                if key[0] == property:
                    properties_to_remove[key[0]].append(key[1])
                elif key[0] == property and key[1] in [self.input_selection_id, self.output_selection_id]:
                    properties_to_remove[key[0]].append(key[1])

        for _prop, _surface_ids in properties_to_remove.items():
            for _id in _surface_ids:             
                self.properties._remove_surface_property(_prop, _id)

    def set_surface_velocity(self, surface_id: int):

        data = {
                "real_values": [1.0],
                "imag_values": [0.0],
                }

        self.properties._set_property("surface_velocity", data, surface=surface_id)

        app().project.file.write_model_properties_in_file()
        # app().main_window.set_geometry_selection(surfaces=[surface_id])

    def process_areas(self):

        def function_callback():
            surface_ids = [self.input_selection_id, self.output_selection_id]
            logging.info("Processing area... [60/100]")
            self.mesh._process_face_elements_connected_to_nodes(surface_ids)

        LoadingWindow(function_callback).run()

    def get_response(self, excitation_id: int, surface_id: int):

        element_3d, _ = self.project.acoustic_assembler.get_element()
        element_3d.reorder_connect()

        surface_nodes = self.mesh.nodes_from_surfaces[surface_id]

        rho, _ = self.model.get_fluid_properties_from_surface(surface_id, self.frequencies)
        if rho is None:
            return None
        
        area, surface_velocity = self.get_area_and_surface_velocity(excitation_id)

        if area is None:
            self.hide()
            title = "Surface velocity not detected"
            message = f"The surface velocity associated to the surface #{surface_id} has not been found. "
            message += "It is recommended to check the acoustic model excitations and change the excitation "
            message += "surface ID to proceed with the transfer function data exportation."
            PrintMessageInput([window_title_1, title, message])
            app().main_window.set_input_widget(self)
            return None

        # Note: the negative signal ensures the assembly consistency of acoustic transfer element
        volume_velocity = -surface_velocity * area

        node_ids = np.sort(surface_nodes)
        pressures = self.solution[node_ids, :]
        avg_pressure = np.average(pressures, axis=0)

        return avg_pressure / volume_velocity

    def get_area_and_surface_velocity(self, surface_id: int):
        for key, data in self.properties.surface_properties.items():
            if key[0] == "surface_velocity" and key[1] == surface_id:
                real_values = np.array(data["real_values"])
                imag_values = np.array(data["imag_values"])
                surface_velocity = real_values + 1j * imag_values
                area = self.model.mesh.surface_area_from_element_integration[surface_id]
                return area, surface_velocity
        return None, None

    def join_model_data(self, excitation_id: int):

        self.solution = self.project.acoustic_harmonic_solver.solution

        for k, response_id in enumerate([self.input_selection_id, self.output_selection_id]):
            
            data = self.get_response(excitation_id, response_id)
            if data is None:
                self.element_transfer_data.clear()
                return
            
            if response_id == self.input_selection_id:
                resp_id = 1
            else:
                resp_id = 2

            if excitation_id == self.input_selection_id:
                excit_id = 1
            else:
                excit_id = 2

            unit_label = "Pa/m³/s"
            data_type = "transfer_function"
            y_label = "Transfer function H(f)"

            data_name = f"transfer_function_h{resp_id}{excit_id}"
            key = (data_name, (self.input_selection_id, self.output_selection_id))

            self.element_transfer_data[key] = { 
                                        "x_data" : self.frequencies,
                                        "y_data" : data,
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : y_label,
                                        "title" : "Element transfer data",
                                        "data_type" : data_type,
                                        "legend" : "element transfer data",
                                        "unit" : unit_label,
                                        "color" :(0,0,1),
                                        "linestyle" : "-"
                                        }

    def export_data_in_spreadsheet_format(self, export_path: str):

        from pandas import ExcelWriter, DataFrame

        with ExcelWriter(export_path) as writer:

            for key, data in self.element_transfer_data.items():

                selection_type, selection_id = key
                sheet_name = f"{selection_type}_{selection_id}"

                x_data = data["x_data"]
                y_data = data["y_data"]
                unit = data["unit"]

                if isinstance(y_data[0], complex):
                    header = ["Frequency[Hz]", f"Real part [{unit}]", f"Imaginary part [{unit}]", f"Absolute [{unit}]"]
                    data_to_export = np.array([x_data, np.real(y_data), np.imag(y_data), np.abs(y_data)]).T 
                else:
                    data_type = data["data_type"]
                    header = ["Frequency[Hz]", f"{data_type.capitalize()} [{unit}]"]
                    data_to_export = np.array([x_data, y_data]).T

                df = DataFrame(data_to_export, columns=header)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def export_data_callback(self):
        if self.element_transfer_data:
            path = self.lineEdit_spreadsheet_path.text()
            self.export_data_in_spreadsheet_format(path)
        
    def _paint_icons(self):
        icon_color = None
        theme = app().config.user_preferences.interface_theme
        
        if theme == "dark":
            icon_color = QColor("#5f9af4")
        else:
            icon_color = QColor("#1a73e8")

        widgets = [self.pushButton_invert_selection, self.pushButton_search]
        change_icon_color_for_widgets(widgets, icon_color)

    def print_final_message(self):

        window_title = "Vibra"
        title = "Data exporting finished"
        message = "The acoustic transfer element data exportation has been finished."
        PrintMessageInput([window_title, title, message])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.export_data_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)