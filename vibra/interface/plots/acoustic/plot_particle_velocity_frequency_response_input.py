from PySide6.QtWidgets import QComboBox, QDialog, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import Qt
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

window_title1 = "Error"
window_title2 = "Warning"

class PlotParticleVelocityFrequencyResponseInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/acoustic/plot_particle_velocity_frequency_response_input.ui"
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
        self.plotter = None
        self.unit_label = "m/s"
        self.keep_window_open = True
        self.particle_velocity = dict()

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_selector_filter: QComboBox
        self.comboBox_component_selector: QComboBox

        # QLineEdit
        self.lineEdit_selection_id: QLineEdit

        # QPushButton
        self.pushButton_export_data: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_plot_data: QPushButton

    def _create_connections(self):
        #
        self.comboBox_selector_filter.currentIndexChanged.connect(self.update_render_according_to_selector)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
    
    def geometry_selection_callback(self):

        faces = self.main_window.selected_geometry_surfaces
        nodes = self.main_window.selected_mesh_nodes

        index = self.comboBox_selector_filter.currentIndex()
        if faces and index == 0:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)

        elif nodes and index == 1:
            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)

        else:
            self.lineEdit_selection_id.setText("")

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

    def check_inputs(self):

        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            selection = "surfaces"

        else:
            selection = "nodes"

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        stop, self.typed_ids = self.mesh.check_selected_ids(lineEdit_selection_id, 
                                                            selection = selection)

        if stop:
            self.lineEdit_selection_id.setFocus()
            return True

    def plot_data_callback(self):

        if self.check_inputs():
            return

        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.model_results)

        self.pushButton_cancel.setText("Exit")

    def export_data_callback(self):
        
        if self.check_inputs():
            return

        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def get_component_label(self):
        index = self.comboBox_component_selector.currentIndex()
        if index == 0:
            return "Vx"
        elif index == 1:
            return "Vy"
        elif index == 2:
            return "Vz"
        else:
            return "Vn"

    def get_response(self, selected_id):

        def function_callback():
            
            selection_type = self.comboBox_selector_filter.currentIndex()
            logging.info("Processing particle velocity..." + ProgressStatus(15, 100))

            if selection_type == 0:
                particle_velocity = self.get_surface_particle_velocity(selected_id)

            else:
                particle_velocity = self.get_nodal_particle_velocity(selected_id)

            logging.info("Processing particle velocity..." + ProgressStatus(95, 100))

            return particle_velocity

        get_particle_velocity = load_function(function_callback, self.main_window)

        return get_particle_velocity()

    def get_surface_particle_velocity(self, surface_id : int):

        component_label = self.get_component_label()

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
            input_velocities = np.array(list(self.particle_velocity[component_label].values()), dtype=complex)

            return np.average(input_velocities, axis=0)            

    def get_nodal_particle_velocity(self, node_id : int):

        component_label = self.get_component_label()

        if self.particle_velocity:
            if component_label in self.particle_velocity.keys():
                if node_id in self.particle_velocity[component_label].keys():
                    return self.particle_velocity[component_label][node_id]

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

        return self.particle_velocity[component_label][node_id]

    def join_model_data(self):

        self.hide()
        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            selection_type = "surface"
        else:
            selection_type = "node"

        component_label = self.get_component_label()

        self.model_results = dict()
        self.title = f"Particle velocity frequency response - {self.analysis_method}"

        for i, selected_id in enumerate(self.typed_ids):

            key = (selection_type, (selected_id))
            legend_label = f"Particle velocity at {selection_type} [{selected_id}]"

            self.model_results[key] = { 
                                        "x_data" : self.frequencies,
                                        "y_data" : self.get_response(selected_id),
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : f"Particle velocity {component_label}",
                                        "title" : self.title,
                                        "data_type" : "particle velocity",
                                        "legend" : legend_label,
                                        "unit" : self.unit_label,
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
            self.plot_data_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        self.keep_window_open = False
        return super().closeEvent(a0)
