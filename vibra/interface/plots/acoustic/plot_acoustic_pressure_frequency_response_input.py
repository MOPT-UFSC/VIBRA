from PySide6.QtWidgets import QComboBox, QWidget, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.ui_generated.plots.acoustic.plot_acoustic_pressure_frequency_response_input_ui import PlotAcousticPressureFrequencyResponseInput_UI
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

import numpy as np

window_title1 = "Error"
window_title2 = "Warning"

class PlotAcousticPressureFrequencyResponseInput(PlotAcousticPressureFrequencyResponseInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = app().main_window
        self.main_window.show_geometry_render_widget()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._reset_variables()
        self._create_connections()

        self._load_analysis_data_and_solution()
        self.geometry_selection_callback()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.update_render_according_to_selector()

    def _load_analysis_data_and_solution(self):
        self.analysis_method = ""
        analysis_data = self.project.analysis_data
        if "analysis_id" in analysis_data.keys():
            if analysis_data["analysis_id"] == 3:
                self.analysis_method = "Direct method"

        self.frequencies = self.project.acoustic_harmonic_solver.frequencies
        self.solution = self.project.acoustic_harmonic_solver.solution

    def _reset_variables(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "Pa"

    def _create_connections(self):
        #
        self.comboBox_selector_filter.currentIndexChanged.connect(self.update_render_according_to_selector)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
    
    def geometry_selection_callback(self):

        faces = self.main_window.selected_geometry_surfaces
        lines = self.main_window.selected_geometry_lines
        nodes = self.main_window.selected_mesh_nodes

        index = self.comboBox_selector_filter.currentIndex()
        if faces and index == 0:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)

        if lines and index == 1:
            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)

        if nodes and index == 2:
            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)

        elif not any([nodes, lines, faces]):
            self.lineEdit_selection_id.setText("")

    def update_render_according_to_selector(self):

        self.geometry_selection_callback()

        if self.comboBox_selector_filter.currentIndex() in [0, 1]:
            self.main_window.show_geometry_render_widget()
        else:
            self.main_window.show_mesh_render_widget()

    def check_inputs(self):

        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            selection = "surfaces"

        elif index == 1:
            selection = "lines"

        else:
            selection = "nodes"

        input_ids = self.lineEdit_selection_id.text()
        self.typed_ids = self.mesh.check_selected_ids(
                                                      input_ids, 
                                                      selection = selection
                                                      )

        if self.typed_ids is None:
            self.lineEdit_selection_id.setFocus()
            return True

    def plot_data_callback(self):

        if self.check_inputs():
            return

        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def export_data_callback(self):
        
        if self.check_inputs():
            return

        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def get_response(self, index, selected_id):

        if index == 0:
            rows = self.project.model.mesh.nodes_from_surfaces[selected_id]

        elif index == 1:
            rows = self.project.model.mesh.nodes_from_lines[selected_id]

        else:
            rows = selected_id

        if isinstance(rows, int):
            response = self.solution[rows,:]
        else:
            response = np.average(self.solution[rows,:], axis=0)

        if complex(0) in response:
            response += 1e-12
        #     response += np.ones(len(response), dtype=float)*(1e-12)

        return response

    def join_model_data(self):

        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            selection_type = "surface"
        elif index == 1:
            selection_type = "line"
        else:
            selection_type = "node"

        self.model_results = dict()
        self.title = f"Acoustic frequency response - {self.analysis_method}"

        for i, selected_id in enumerate(self.typed_ids):

            key = (selection_type, (selected_id))
            legend_label = f"Acoustic pressure at {selection_type} [{selected_id}]"

            y_data = self.get_response(index, selected_id)

            self.model_results[key] = { 
                                        "x_data" : self.frequencies,
                                        "y_data" : y_data,
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : "Acoustic pressure",
                                        "title" : self.title,
                                        "data_type" : "acoustic pressure",
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

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        return super().closeEvent(a0)
