from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton, QDialog
from PyQt5.QtCore import Qt, QEvent, QObject, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter


window_title1 = "Error"
window_title2 = "Warning"

class PlotTransmissionLossInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/acoustic/plot_transmission_loss.ui"
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

        self._config_widgets()
        self._load_analysis_data()
        self.exec()

    def _load_analysis_data(self):
        self.analysis_method = ""
        analysis_data = self.project.analysis_data
        if "analysis_id" in analysis_data.keys():
            if analysis_data["analysis_id"] == 3:
                self.analysis_method = "Direct method"

    def _load_icons(self):
        self.vibra_icon = app().main_window.vibra_icon
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.vibra_icon)

    def _reset_variables(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "dB"

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_processing_selector : QComboBox
        
        # QLineEdit
        self.lineEdit_output_surface_id : QLineEdit
        self.lineEdit_input_surface_id : QLineEdit
        
        # QPushButton
        self.pushButton_call_data_exporter : QPushButton
        self.pushButton_plot_frequency_response : QPushButton
        self.pushButton_flip_selection : QPushButton

    def _create_connections(self):
        self.pushButton_call_data_exporter.clicked.connect(self.call_data_exporter)
        self.pushButton_flip_selection.clicked.connect(self.flip_nodes)
        self.pushButton_plot_frequency_response.clicked.connect(self.call_plotter)
        #
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)
        #
        self.clickable(self.lineEdit_input_surface_id).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_output_surface_id).connect(self.lineEdit_2_clicked)

    def _config_widgets(self):
        self.current_lineEdit = self.lineEdit_input_surface_id
        self.lineEdit_input_surface_id.setFocus()

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
        self.current_lineEdit = self.lineEdit_input_surface_id

    def lineEdit_2_clicked(self):
        self.current_lineEdit = self.lineEdit_output_surface_id

    def writeNodes(self, list_node_ids):
        node_id = list_node_ids[0]
        self.current_lineEdit.setText(str(node_id))
    
    def geometry_selection_callback(self, points, lines, faces):
        
        index = self.comboBox_processing_selector.currentIndex()
        if faces and index == 0:
            text = ", ".join([str(i) for i in faces])
            self.current_lineEdit.setText(text)
            self.entity_type = "surface"

        elif not any([points, lines, faces]):
            self.current_lineEdit.setText("")

    def flip_nodes(self):
        temp_text_input = self.lineEdit_input_surface_id.text()
        temp_text_output = self.lineEdit_output_surface_id.text()
        self.lineEdit_input_surface_id.setText(temp_text_output)
        self.lineEdit_output_surface_id.setText(temp_text_input)

    def call_plotter(self):

        if self.check_inputs():
            return

        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter.imported_dB_data()
        self.plotter._set_data_to_plot(self.model_results)

    def call_data_exporter(self):

        if self.check_inputs():
            return

        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def check_inputs(self):

        lineEdit_output_surface_id = self.lineEdit_output_surface_id.text()
        self.stop, self.output_surface_id = self.model.check_input_surface_id(lineEdit_output_surface_id, single_ID=True)
        if self.stop:
            self.lineEdit_output_surface_id.setFocus()
            return True
        
        lineEdit_input_surface_id = self.lineEdit_input_surface_id.text()
        self.stop, self.input_surface_id = self.model.check_input_surface_id(lineEdit_input_surface_id, single_ID=True)
        if self.stop:
            self.lineEdit_input_surface_id.setFocus()
            return True

    def join_model_data(self):

        self.model_results = dict()

        if self.comboBox_processing_selector.currentIndex() == 0:
            plot_type = "Transmission loss"
            self.project.model.mesh._process_face_elements_connected_to_nodes()
            self.project.model.mesh._process_nodal_areas()
            x_data, y_data = self.project.acoustic_harmonic_solver.get_transmission_loss(self.input_surface_id, self.output_surface_id)
        else:
            plot_type = "Noise reduction"
            x_data, y_data = self.project.acoustic_harmonic_solver.get_noise_reduction(self.input_surface_id, self.output_surface_id)

        if y_data is None:
            return

        self.title = f"{plot_type} - {self.analysis_method}"

        legend_label = f"{plot_type} between [{self.output_surface_id}] and [{self.input_surface_id}]"
        self.model_results = {  "x_data" : x_data,
                                "y_data" : y_data,
                                "x_label" : "Frequency [Hz]",
                                "y_label" : plot_type,
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

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        # self.keep_window_open = False
        return super().closeEvent(a0)