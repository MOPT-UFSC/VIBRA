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
        self.comboBox_selector_filter : QComboBox
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
        self.comboBox_selector_filter.currentIndexChanged.connect(self.update_render_according_to_selector)
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_export_data.clicked.connect(self.call_data_exporter)
        self.pushButton_invert_selection.clicked.connect(self.invert_selection_callback)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.clickable(self.lineEdit_input_selected_id).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_output_selected_id).connect(self.lineEdit_2_clicked)

    def geometry_selection_callback(self):
        
        faces = self.main_window.selected_geometry_surfaces
        lines = self.main_window.selected_geometry_lines
        nodes = self.main_window.selected_mesh_nodes

        index = self.comboBox_selector_filter.currentIndex()
        if faces and index == 0:

            if len(faces) > 1:
                return

            else:
                _faces = [str(i) for i in faces]
                self.current_lineEdit.setText(_faces[0])

        if nodes and index == 1:
            
            if len(nodes) > 1:
                return

            else:
                _nodes = [str(i) for i in nodes]
                self.current_lineEdit.setText(_nodes[0])

        elif not any([nodes, lines, nodes]):
            return
            self.current_lineEdit.setText("")

    def invert_selection_callback(self):

        if self.check_inputs():
            return

        input_id = self.lineEdit_input_selected_id.text()
        output_id = self.lineEdit_output_selected_id.text()

        self.lineEdit_output_selected_id.setText(input_id)
        self.lineEdit_input_selected_id.setText(output_id)

    def update_render_according_to_selector(self):

        self.geometry_selection_callback()

        if self.comboBox_selector_filter.currentIndex() == 0:

            if not self.main_window.viewer_tabs.isTabEnabled(2):
                self.main_window.viewer_tabs.show_geometry()
                return

            self.main_window.viewer_tabs.setCurrentIndex(1)

        else:

            if self.main_window.viewer_tabs.currentIndex() != 2:
                if not self.main_window.viewer_tabs.isTabEnabled(2):
                    self.main_window.viewer_tabs.show_mesh()
                    return

            self.main_window.viewer_tabs.setCurrentIndex(2)

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

        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            selection = "surfaces"

        else:
            selection = "nodes"
 
        input_selected_id = self.lineEdit_input_selected_id.text()
        stop, self.input_selection_id = self.mesh.check_selected_ids(   input_selected_id, 
                                                                        selection = selection, 
                                                                        single_id = True   )

        if stop:
            self.lineEdit_input_selected_id.setFocus()
            self.lineEdit_input_selected_id.selectAll()
            return True

        output_selected_id = self.lineEdit_output_selected_id.text()
        stop, self.output_selection_id = self.mesh.check_selected_ids(  output_selected_id, 
                                                                        selection = selection, 
                                                                        single_id = True  )

        if stop:
            self.lineEdit_output_selected_id.setFocus()
            self.lineEdit_output_selected_id.selectAll()
            return True

    def call_data_exporter(self):

        if self.check_inputs():
            return

        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def get_response(self, selected_id: int, comp_label: str):

        def function_callback():
            
            selection_type = self.comboBox_selector_filter.currentIndex()

            if selection_type == 0:
                particle_velocity, pressure = self.get_surface_particle_velocity_and_pressures(selected_id, comp_label)

            else:
                particle_velocity, pressure = self.get_nodal_particle_velocity_and_pressure(selected_id, comp_label)

            logging.info("Processing particle velocity..." + ProgressStatus(95, 100))

            return [particle_velocity, pressure]

        function = load_function(function_callback, app().main_window)

        return function()

    def get_surface_particle_velocity_and_pressures(self, surface_id : int, component_label: str):

        element_3d, _ = self.project.acoustic_assembler.get_element()
        element_3d.reorder_connect()

        list_nodes = list()
        for tag, surface_nodes in self.mesh.nodes_from_surfaces.items():
            if self.comboBox_selector_filter.currentIndex() == 0:
                if tag == surface_id:
                    list_nodes.extend(surface_nodes)

        rho = self.model.get_fluid_density_for_particle_velocity_calculation(surface_id, self.frequencies)
        if rho is None:
            return np.zeros_like(self.frequencies, dtype=complex)

        self.particle_velocity = self.project.acoustic_harmonic_solver.get_particle_velocity_from_surface(surface_id, rho)
        particle_velocities = np.array(list(self.particle_velocity[component_label].values()), dtype=complex)

        node_ids = np.sort(list_nodes)
        pressures = self.solution[node_ids, :]

        avg_pressure = np.average(pressures, axis=0)
        avg_particle_velocity = np.average(particle_velocities, axis=0)

        return avg_particle_velocity, avg_pressure

    def get_nodal_particle_velocity_and_pressure(self, node_id : int, component_label: str):

        if self.particle_velocity:
            if component_label in self.particle_velocity.keys():
                if node_id in self.particle_velocity[component_label].keys():
                    particle_velocity = self.particle_velocity[component_label][node_id]
                    pressure = self.solution[node_id, :]
                    return pressure / particle_velocity

        element_3d, _ = self.project.acoustic_assembler.get_element()
        element_3d.reorder_connect()

        list_nodes = list()
        for tag, surface_nodes in self.mesh.nodes_from_surfaces.items():
            if self.comboBox_selector_filter.currentIndex() == 1:
                if node_id in surface_nodes:
                    list_nodes.extend(surface_nodes)
                    surface_id = tag

        rho = self.model.get_fluid_density_for_particle_velocity_calculation(surface_id, self.frequencies)
        if rho is None:
            return np.zeros_like(self.frequencies, dtype=complex)

        self.particle_velocity = self.project.acoustic_harmonic_solver.get_particle_velocity_from_surface(surface_id, rho)

        particle_velocity = self.particle_velocity[component_label][node_id]
        pressure = self.solution[node_id, :]

        return particle_velocity, pressure

    def join_model_data(self):

        self.hide()

        if self.comboBox_selector_filter.currentIndex() == 0:
            selection_type = "face"
        else:
            selection_type = "node"

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

            for j, data_type in enumerate(["velocity", "pressure"]):

                if data_type in "velocity":
                    unit_label = "m/s"
                    data_name = f"{label}_{data_type}_{v_label}_{selection_type}"
                else:
                    unit_label = "Pa"
                    data_name = f"{label}_{data_type}_{selection_type}"

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
            self.call_data_exporter()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        self.keep_window_open = False
        return super().closeEvent(a0)
