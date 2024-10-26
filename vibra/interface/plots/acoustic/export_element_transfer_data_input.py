from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton, QDialog
from PyQt5.QtCore import Qt, QEvent, QObject, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.loading_bar import load_function
from vibra.utils.progress_status import ProgressStatus

import logging
import numpy as np

window_title1 = "Error"
window_title2 = "Warning"

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

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_input_velocity_component: QComboBox
        self.comboBox_output_velocity_component: QComboBox

        # QLineEdit
        self.lineEdit_input_selected_id : QLineEdit
        self.lineEdit_output_selected_id : QLineEdit
        self.current_lineEdit = self.lineEdit_output_selected_id

        # QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_export_data : QPushButton
        self.pushButton_invert_selection: QPushButton

    def _create_connections(self):
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_invert_selection.clicked.connect(self.invert_selection_callback)
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
            clicked = pyqtSignal()

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
        self.exporter._set_data_to_export(self.model_results)
        self.pushButton_cancel.setText("Close")

    def get_response(self, selected_id: int, comp_label: str):

        def function_callback():

            logging.info("Processing area..." + ProgressStatus(25, 100))
            self.mesh._process_face_elements_connected_to_nodes(selected_id)

            particle_velocity, volume_velocity, pressure = self.get_volume_velocity_and_pressures(selected_id, comp_label)
            logging.info("Processing particle velocity..." + ProgressStatus(95, 100))

            return [particle_velocity, volume_velocity, pressure]

        function = load_function(function_callback, app().main_window)

        return function()

    def get_volume_velocity_and_pressures(self, surface_id : int, component_label: str):

        element_3d, _ = self.project.acoustic_assembler.get_element()
        element_3d.reorder_connect()

        list_nodes = list()
        for tag, surface_nodes in self.mesh.nodes_from_surfaces.items():
            if tag == surface_id:
                list_nodes.extend(surface_nodes)

        rho = self.model.get_fluid_density_for_particle_velocity_calculation(surface_id, self.frequencies)
        if rho is None:
            return np.zeros_like(self.frequencies, dtype=complex)

        particle_velocities = self.project.acoustic_harmonic_solver.get_particle_velocity_from_surface(surface_id, rho)
        particle_velocities_comp = np.array(list(particle_velocities[component_label].values()), dtype=complex)

        node_ids = np.sort(list_nodes)
        pressures = self.solution[node_ids, :]

        avg_pressure = np.average(pressures, axis=0)
        avg_particle_velocity = np.average(particle_velocities_comp, axis=0)

        area = self.model.mesh.surface_area_from_element_integration[surface_id]
        volume_velocity = avg_particle_velocity * area

        return avg_particle_velocity, volume_velocity, avg_pressure

    def join_model_data(self):

        self.hide()

        self.model_results = dict()

        labels = ["input", "output"]
        v_labels = ["Vx", "Vy", "Vz", "Vn"]

        for i, selected_id in enumerate([self.input_selection_id, self.output_selection_id]):

            if i == 0:
                v_index = self.comboBox_input_velocity_component.currentIndex()
            else:
                v_index = self.comboBox_output_velocity_component.currentIndex()

            label = labels[i]
            v_label = v_labels[v_index]
            data = self.get_response(selected_id, v_label)

            for j, data_type in enumerate(["pvelocity", "vvelocity", "pressure"]):

                if data_type == "pvelocity":
                    unit_label = "m/s"
                    data_name = f"{label}_{data_type}_{v_label}_face"

                elif data_type == "vvelocity":
                    unit_label = "m³/s"
                    data_name = f"{label}_{data_type}_{v_label}_face"

                else:
                    unit_label = "Pa"
                    data_name = f"{label}_{data_type}_face"     

                key = (data_name, (selected_id))

                self.model_results[key] = { 
                                            "x_data" : self.frequencies,
                                            "y_data" : data[j],
                                            "x_label" : "Frequency [Hz]",
                                            "y_label" : data_type.replace("_", " ").capitalize(),
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
