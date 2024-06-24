from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter


def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

window_title1 = "Error"
window_title2 = "Warning"

class PlotAcousticFrequencyResponseInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/acoustic/plot_acoustic_frequency_response_input.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.project = self.main_window.project
        self.model = self.project.model
        self.properties = self.model.properties

        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()

        self._load_icons()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

        self._load_analysis_data_and_solution()
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

    def _load_icons(self):
        self.icon_path = str(Path("data/icons/logo_vibra.png"))
        self.export_icon = QIcon(get_icons_path('save.png'))
        self.icon = QIcon(self.icon_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _reset_variables(self):
        self.unit_label = "Pa"

    def _define_qt_variables(self):
        self.comboBox_selector_filter = self.findChild(QComboBox, 'comboBox_selector_filter')
        self.lineEdit_selection_id = self.findChild(QLineEdit, 'lineEdit_selection_id')
        self.pushButton_call_data_exporter = self.findChild(QPushButton, 'pushButton_call_data_exporter')
        self.pushButton_plot_frequency_response = self.findChild(QPushButton, 'pushButton_plot_frequency_response')
        self.pushButton_call_data_exporter.setIcon(self.export_icon)

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

    def call_plotter(self):
        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.typed_ids = self.model.check_input_surface_id(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return
        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_data_to_plot(self.model_results)

    def call_data_exporter(self):
        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.typed_ids = self.model.check_input_surface_id(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return
        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def get_response(self):

        selected_id = self.typed_ids[0]
        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            rows = self.project.model.mesh.nodes_from_surfaces[selected_id]
        elif index == 1:
            rows = self.project.model.mesh.nodes_from_lines[selected_id]
        else:
            rows = [3670]
            # return

        # print(len(rows))
        response = np.average(self.solution[rows,:], axis=0)

        # if complex(0) in response:
        #     response += 1e-12
            # response += np.ones(len(response), dtype=float)*(1e-12)

        return response

    def join_model_data(self):
        self.model_results = dict()
        self.title = "Acoustic frequency response - {}".format(self.analysis_method)
        legend_label = "Acoustic pressure at {} [{}]".format(self.entity_type, self.typed_ids[0])
        self.model_results = {  "x_data" : self.frequencies,
                                "y_data" : self.get_response(),
                                "x_label" : "Frequency [Hz]",
                                "y_label" : "Acoustic pressure",
                                "title" : self.title,
                                "data_information" : legend_label,
                                "legend" : legend_label,
                                "unit" : self.unit_label,
                                "color" : [0,0,1],
                                "linestyle" : "-"  }

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.call_plotter()
        elif event.key() == Qt.Key_Escape:
            self.close()