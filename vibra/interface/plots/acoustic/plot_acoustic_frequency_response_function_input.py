from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton, QDialog
from PyQt5.QtCore import Qt, QEvent, QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.general.print_message_input2 import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

from vibra.utils.interface_functions import get_main_window

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

window_title1 = "Error"
window_title2 = "Warning"

class PlotAcousticFrequencyResponseFunctionInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/acoustic/plot_acoustic_frequency_response_function.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()

        self.project = self.main_window.project
        self.model = self.project.model
        self.properties = self.model.properties

        self._load_icons()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
    
        ConfigWidgetAppearance(self, tool_tip=True)

        self._load_analysis_data_and_solution()
        self.exec()

    def _load_icons(self):
        self.vibra_icon = app().main_window.vibra_icon
        self.setWindowIcon(self.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _reset_variables(self):
        self.unit_label = "Pa/Pa"

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_selector_filter : QComboBox
        # QLineEdit
        self.lineEdit_output_node_id : QLineEdit
        self.lineEdit_input_node_id : QLineEdit
        self.current_lineEdit = self.lineEdit_output_node_id
        # QPushButton
        self.pushButton_call_data_exporter : QPushButton
        self.pushButton_plot_frequency_response : QPushButton
        self.pushButton_flip_selection : QPushButton

    def _create_connections(self):
        #
        self.pushButton_call_data_exporter.clicked.connect(self.call_data_exporter)
        self.pushButton_flip_selection.clicked.connect(self.flip_nodes)
        self.pushButton_plot_frequency_response.clicked.connect(self.call_plotter)
        #
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)
        #
        self.clickable(self.lineEdit_input_node_id).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_output_node_id).connect(self.lineEdit_2_clicked)

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
        self.current_lineEdit = self.lineEdit_input_node_id

    def lineEdit_2_clicked(self):
        self.current_lineEdit = self.lineEdit_output_node_id

    def writeNodes(self, list_node_ids):
        node_id = list_node_ids[0]
        self.current_lineEdit.setText(str(node_id))

    def _load_analysis_data_and_solution(self):

        self.analysis_method = ""
        analysis_data = self.project.analysis_data

        if "analysis_id" in analysis_data.keys():
            if analysis_data["analysis_id"] == 3:
                self.analysis_method = "Direct method"

        if "frequencies" in analysis_data.keys():
            self.frequencies = analysis_data["frequencies"]

        self.solution = self.project.acoustic_harmonic_solver.solution

    def geometry_selection_callback(self, points, lines, faces):
        
        index = self.comboBox_selector_filter.currentIndex()
        if faces and index == 0:
            text = ", ".join([str(i) for i in faces])
            self.current_lineEdit.setText(text)
            self.entity_type = "surface"

        if lines and index == 1:
            text = ", ".join([str(i) for i in lines])
            self.current_lineEdit.setText(text)
            self.entity_type = "line"

        if points and index == 2:
            text = ", ".join([str(i) for i in points])
            self.current_lineEdit.setText(text)
            self.entity_type = "point"

        elif not any([points, lines, faces]):
            self.current_lineEdit.setText("")

    def flip_nodes(self):
        temp_text_input = self.lineEdit_input_node_id.text()
        temp_text_output = self.lineEdit_output_node_id.text()
        self.lineEdit_input_node_id.setText(temp_text_output)
        self.lineEdit_output_node_id.setText(temp_text_input)

    def call_plotter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_data_to_plot(self.model_results)

    def call_data_exporter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def check_inputs(self):

        lineEdit_output_node_id = self.lineEdit_output_node_id.text()
        self.stop, self.output_node_id = self.model.check_input_surface_id(lineEdit_output_node_id, single_ID=True)
        if self.stop:
            self.lineEdit_output_node_id.setFocus()
            return True
        
        lineEdit_input_node_id = self.lineEdit_input_node_id.text()
        self.stop, self.input_node_id = self.model.check_input_surface_id(lineEdit_input_node_id, single_ID=True)
        if self.stop:
            self.lineEdit_input_node_id.setFocus()
            return True

    def get_response(self):

        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            self.selection_type = "surfaces"
            rows_num = self.project.model.mesh.nodes_from_surfaces[self.output_node_id]
            rows_den = self.project.model.mesh.nodes_from_surfaces[self.input_node_id]

        elif index == 1:
            self.selection_type = "lines"
            rows_num = self.project.model.mesh.nodes_from_lines[self.output_node_id]
            rows_den = self.project.model.mesh.nodes_from_lines[self.input_node_id]

        else:
            self.selection_type = ""
            return None

        numerator = np.average(self.solution[rows_num,:], axis=0)
        denominator = np.average(self.solution[rows_den,:], axis=0)

        if complex(0) in denominator:
            denominator += 1e-12

        response = numerator/denominator

        return response

    def join_model_data(self):

        self.model_results = dict()
        y_data = self.get_response()
        if y_data is None:
            return

        self.title = "Acoustic frequency response function - {}".format(self.analysis_method)
        legend_label = "Acoustic FRF between {} {} and {}".format(self.selection_type, 
                                                                  self.output_node_id, 
                                                                  self.input_node_id)

        self.model_results = {  "x_data" : self.frequencies,
                                "y_data" : y_data,
                                "x_label" : "Frequency [Hz]",
                                "y_label" : "Nodal response",
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