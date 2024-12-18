from PySide6.QtWidgets import QComboBox, QDialog, QFileDialog, QLineEdit, QPushButton
from PySide6.QtCore import Qt, QEvent, QObject, Signal
from PySide6.QtGui import QCloseEvent
from PySide6 import uic

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.loading_bar import load_function
from vibra.utils.progress_status import ProgressStatus

import logging
import numpy as np
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"

class ExportElementTransferDataInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "data_handler/export_element_transfer_data.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()

        self.project = app().main_window.project
        self.model = app().main_window.project.model
        self.mesh = app().main_window.project.model.mesh
        self.properties = app().main_window.project.model.properties

        self._config_window()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

        self._load_analysis_data_and_solution()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _load_analysis_data_and_solution(self):
        self.analysis_method = ""
        analysis_data = self.project.analysis_data
        if "analysis_id" in analysis_data.keys():
            if analysis_data["analysis_id"] == 3:
                self.analysis_method = "Direct method"

        self.frequencies = self.project.acoustic_harmonic_solver.frequencies
        self.solution = self.project.acoustic_harmonic_solver.solution

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _reset_variables(self):
        self.exporter = None
        self.keep_window_open = True
        self.particle_velocity = dict()
        self.element_transfer_data = dict()

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_excitation_surface: QComboBox

        # QLineEdit
        self.lineEdit_input_selected_id: QLineEdit
        self.lineEdit_output_selected_id: QLineEdit
        self.lineEdit_spreadsheet_path: QLineEdit
        self.current_lineEdit = self.lineEdit_output_selected_id

        # QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_export_data: QPushButton
        self.pushButton_invert_selection: QPushButton
        self.pushButton_search: QPushButton

    def _create_connections(self):
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_invert_selection.clicked.connect(self.invert_selection_callback)
        self.pushButton_search.clicked.connect(self.search_callback)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.clickable(self.lineEdit_input_selected_id).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_output_selected_id).connect(self.lineEdit_2_clicked)

    def geometry_selection_callback(self):

        selected_faces = self.main_window.selected_geometry_surfaces

        if selected_faces:

            if len(selected_faces) > 1:
                return

            else:
                _selected_faces = [str(i) for i in selected_faces]
                self.current_lineEdit.setText(_selected_faces[0])

    def invert_selection_callback(self):

        if self.check_inputs():
            return

        input_id = self.lineEdit_input_selected_id.text()
        output_id = self.lineEdit_output_selected_id.text()

        self.lineEdit_output_selected_id.setText(input_id)
        self.lineEdit_input_selected_id.setText(output_id)

    def update_render_according_to_selector(self):

        self.geometry_selection_callback()

        if not self.main_window.viewer_tabs.isTabEnabled(2):
            self.main_window.viewer_tabs.show_geometry()
            return

        self.main_window.viewer_tabs.setCurrentIndex(1)

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

    def search_callback(self):

        last_path = app().config.get_last_folder_for("imported table folder")
        if last_path is None:
            last_path = str(Path().home())

        caption = f"Choose a file to import element transfer data"
        path, check = QFileDialog.getOpenFileName(
                                                  self,
                                                  caption, 
                                                  last_path, 
                                                  'Table File (*.xls; *.xlsx;)'
                                                  )

        if not check:
            return True

        self.lineEdit_spreadsheet_path.setText(path)
        app().config.write_last_folder_path_in_file("imported table folder", path)

    def check_inputs(self):
 
        input_selected_id = self.lineEdit_input_selected_id.text()
        stop, self.input_selection_id = self.mesh.check_selected_ids(   input_selected_id, 
                                                                        selection = "surfaces", 
                                                                        single_id = True   )

        if stop:
            self.lineEdit_input_selected_id.setFocus()
            self.lineEdit_input_selected_id.selectAll()
            return True

        output_selected_id = self.lineEdit_output_selected_id.text()
        stop, self.output_selection_id = self.mesh.check_selected_ids(  output_selected_id, 
                                                                        selection = "surfaces", 
                                                                        single_id = True  )

        if stop:
            self.lineEdit_output_selected_id.setFocus()
            self.lineEdit_output_selected_id.selectAll()
            return True

    def export_data_callback(self):

        if self.check_inputs():
            return

        self.join_model_data()
        self.exporter = ExportModelResults()
        if self.model_results:
            existing_path = self.lineEdit_spreadsheet_path.text()
            self.exporter._set_data_to_export(self.model_results, existing_path=existing_path)
            self.pushButton_cancel.setText("Close")

    def process_areas(self):

        def function_callback():
            surface_ids = [self.input_selection_id, self.output_selection_id]
            logging.info("Processing area..." + ProgressStatus(60, 100))
            self.mesh._process_face_elements_connected_to_nodes(surface_ids)

        process_area = load_function(function_callback, app().main_window)
        process_area()

    def get_response(self, surface_id: int):

        element_3d, _ = self.project.acoustic_assembler.get_element()
        element_3d.reorder_connect()

        surface_nodes = self.mesh.nodes_from_surfaces[surface_id]

        rho = self.model.get_fluid_density_for_particle_velocity_calculation(surface_id, self.frequencies)
        if rho is None:
            return None

        if self.comboBox_excitation_surface.currentIndex() == 0:
            excitation_id = self.input_selection_id
        else:
            excitation_id = self.output_selection_id
        
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

    def join_model_data(self):

        self.hide()

        self.model_results = dict()
        self.process_areas()

        for i, selected_id in enumerate([self.input_selection_id, self.output_selection_id]):

            data = self.get_response(selected_id)
            if data is None:
                self.model_results.clear()
                return

            unit_label = "Pa/m³/s"
            if self.comboBox_excitation_surface.currentIndex() == 0:
                output_id = 1
            else:
                output_id = 2

            data_type = "transfer_function"
            y_label = "Transfer function H(f)"

            data_name = f"transfer_function_H{i+1}{output_id}"
            key = (data_name, (self.input_selection_id, self.output_selection_id))

            self.model_results[key] = { 
                                        "x_data" : self.frequencies,
                                        "y_data" : data,
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : y_label,
                                        "title" : "Element transfer data",
                                        "data_type" : data_type,
                                        "legend" : "element transfer data",
                                        "unit" : unit_label,
                                        "color" : self.get_color(i),
                                        "linestyle" : "-"
                                        }

    def get_color(self, index):

        colors = [  (0,0,1), (0,0,0), (1,0,0),
                    (0,1,1), (1,0,1), (1,1,0),
                    (0.25,0.25,0.25)  ]
        
        if index <= 6:
            return colors[index]
        else:
            return tuple(np.random.randint(0, 255, size=3) / 255)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.export_data_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        self.keep_window_open = False
        return super().closeEvent(a0)
