from PyQt5.QtWidgets import QComboBox, QDialog, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

import numpy as np

window_title1 = "Error"
window_title2 = "Warning"

class PlotAcousticFrequencyResponseInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/acoustic/plot_acoustic_frequency_response_input.ui"
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

        while self.keep_window_open:
            self.exec()

    def _load_analysis_data_and_solution(self):
        self.analysis_method = ""
        analysis_data = self.project.analysis_data
        if "analysis_id" in analysis_data.keys():
            if analysis_data["analysis_id"] == 3:
                self.analysis_method = "Direct method"
        if "frequencies" in analysis_data.keys():
            self.frequencies = analysis_data["frequencies"]
        self.solution = self.project.acoustic_harmonic_solver.solution

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _reset_variables(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "Pa"
        self.keep_window_open = True

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_selector_filter : QComboBox
        
        # QLineEdit
        self.lineEdit_selection_id : QLineEdit

        # QPushButton
        self.pushButton_call_data_exporter : QPushButton
        self.pushButton_plot_frequency_response : QPushButton

    def _create_connections(self):
        self.pushButton_call_data_exporter.clicked.connect(self.call_data_exporter)
        self.pushButton_plot_frequency_response.clicked.connect(self.call_plotter)
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)
    
    def geometry_selection_callback(self, points, lines, faces):
        
        index = self.comboBox_selector_filter.currentIndex()
        if faces and index == 0:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.entity_type = "surface"

        if lines and index == 1:
            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)
            self.entity_type = "line"

        if points and index == 2:
            text = ", ".join([str(i) for i in points])
            self.lineEdit_selection_id.setText(text)
            self.entity_type = "point"

        elif not any([points, lines, faces]):
            self.lineEdit_selection_id.setText("")

    def check_inputs(self):

        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            selection = "surfaces"

        elif index == 1:
            selection = "lines"

        else:
            selection = "nodes"

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        stop, self.typed_ids = self.mesh.check_selected_ids(lineEdit_selection_id, 
                                                            selection = selection)

        if stop:
            self.lineEdit_selection_id.setFocus()
            return True

    def call_plotter(self):

        if self.check_inputs():
            return

        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def call_data_exporter(self):
        
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

        response = np.average(self.solution[rows,:], axis=0)

        # if complex(0) in response:
        #     response += 1e-12
            # response += np.ones(len(response), dtype=float)*(1e-12)

        return response

    def join_model_data(self):

        self.hide()
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

            print(i, self.get_color(i))
            self.model_results[key] = { 
                                        "x_data" : self.frequencies,
                                        "y_data" : self.get_response(index, selected_id),
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
            self.call_plotter()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        self.keep_window_open = False
        return super().closeEvent(a0)
