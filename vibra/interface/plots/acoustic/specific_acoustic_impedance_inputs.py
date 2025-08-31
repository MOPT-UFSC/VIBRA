from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra.engine import AnalysisID
from vibra import app
from vibra.interface.ui_generated.plots.acoustic.specific_acoustic_impedance_inputs_ui import SpecificAcousticImpedanceInputs_UI
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.general.print_message_input import PrintMessageInput

import logging
import numpy as np

window_title1 = "Error"
window_title2 = "Warning"


class SpecificAcousticImpedanceInputs(SpecificAcousticImpedanceInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh

        self._config_window()
        self._reset_variables()
        self._create_connections()

        self._load_analysis_setup_and_solution()
        self.geometry_selection_callback()

    def _load_analysis_setup_and_solution(self):
        self.analysis_method = ""
        analysis_setup = self.project.analysis_setup
        if "analysis_id" in analysis_setup.keys():
            if analysis_setup["analysis_id"] == AnalysisID.ACOUSTIC_HARMONIC:
                self.analysis_method = "Direct method"

        self.frequencies = app().project.model.frequencies
        self.solution = self.project.acoustic_harmonic_solver.solution

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _reset_variables(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "Pa/m/s"
        self.keep_window_open = True
        self.particle_velocity = dict()

    def _create_connections(self):
        #
        self.comboBox_selector_filter.currentIndexChanged.connect(self.update_render_according_to_selector)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
    
    def geometry_selection_callback(self):

        faces = app().main_window.selected_geometry_surfaces
        nodes = app().main_window.selected_mesh_nodes

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
            app().main_window.show_mesh_render_widget()
        else:
            app().main_window.show_geometry_render_widget()

    def check_inputs(self):

        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            selection = "surfaces"

        else:
            selection = "nodes"

        input_ids = self.lineEdit_selection_id.text()
        self.selected_ids, error_data = self.mesh.check_selected_ids(
                                                                     input_ids, 
                                                                     selection = selection, 
                                                                     single_id = False
                                                                     )

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

    def plot_data_callback(self):

        if self.check_inputs():
            return

        self.join_model_data()
        self.plotter = FrequencyResponsePlotter(close_dialogs=True)
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def export_data_callback(self):
        
        if self.check_inputs():
            return

        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def get_response(self, selected_id):

        def function_callback():
            
            selection_type = self.comboBox_selector_filter.currentIndex()
            

            if selection_type == 0:
                acoustic_impedance = self.get_surface_specific_acoustic_impedance(selected_id)

            else:
                acoustic_impedance = self.get_nodal_specific_acoustic_impedance(selected_id)

            logging.info("Processing particle velocity... [95/100]")

            return acoustic_impedance

        return LoadingWindow(function_callback).run()

    def get_surface_specific_acoustic_impedance(self, surface_id : int):

        component_label = "Vn"

        rho, _ = self.model.get_fluid_properties_from_surface(surface_id, self.frequencies)
        if rho is None:
            return np.zeros_like(self.frequencies, dtype=complex)

        self.particle_velocity = self.project.acoustic_harmonic_solver.get_particle_velocity_from_surface(surface_id, rho)
        particle_velocities = np.array(list(self.particle_velocity[component_label].values()), dtype=complex)

        nodes = self.mesh.get_nodes_from_surface(surface_id)
        pressures = self.solution[np.sort(nodes), :]

        specific_impedance = pressures / particle_velocities

        return np.average(specific_impedance, axis=0)

    def get_nodal_specific_acoustic_impedance(self, node_id : int):

        component_label = "Vn"

        if self.particle_velocity:
            if component_label in self.particle_velocity.keys():
                if node_id in self.particle_velocity[component_label].keys():
                    particle_velocity = self.particle_velocity[component_label][node_id]
                    pressure = self.solution[node_id, :]
                    return pressure / particle_velocity

        mask = np.sum(np.isin(self.mesh.faces_connectivity[:, 4:], node_id), axis=1) == 1
        surface_ids = [int(surf_id) for surf_id in np.unique(self.mesh.faces_connectivity[:, 1][mask])]
        surface_id = surface_ids[0]

        rho, _ = self.model.get_fluid_properties_from_surface(surface_id, self.frequencies)
        if rho is None:
            return np.zeros_like(self.frequencies, dtype=complex)

        self.particle_velocity = self.project.acoustic_harmonic_solver.get_particle_velocity_from_surface(surface_id, rho)

        particle_velocity = self.particle_velocity[component_label][node_id]
        pressure = self.solution[node_id, :]

        return pressure / particle_velocity

    def join_model_data(self):

        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            selection_type = "surface"
        else:
            selection_type = "node"

        self.model_results = dict()
        title = "Specific acoustic impedance"

        for i, selected_id in enumerate(self.selected_ids):

            key = (selection_type, (selected_id))
            legend_label = f"Specific acoustic impedance at {selection_type} [{selected_id}]"

            self.model_results[key] = { 
                                        "x_data" : self.frequencies,
                                        "y_data" : self.get_response(selected_id),
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : "Specific acoustic impedance",
                                        "title" : title,
                                        "data_type" : "specific acoustic impedance",
                                        "legend" : legend_label,
                                        "unit" : self.unit_label,
                                        "color" : self.get_color(i),
                                        "linestyle" : "-"  
                                      }

    def get_color(self, index):

        colors = [  
                  (0,0,1), 
                  (0,0,0), 
                  (1,0,0),
                  (0,1,1), 
                  (1,0,1), 
                  (1,1,0),
                  (0.25,0.25,0.25)
                  ]

        if index <= 6:
            return colors[index]
        else:
            return tuple(np.random.randint(0, 255, size=3) / 255)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        self.keep_window_open = False
        return super().closeEvent(a0)