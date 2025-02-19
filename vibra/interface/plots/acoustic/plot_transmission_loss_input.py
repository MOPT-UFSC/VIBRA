from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton, QWidget
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

import os
import logging
import numpy as np

from time import time
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"

class PlotTransmissionLossInput(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/acoustic/plot_transmission_loss.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.main_window.show_geometry_render_widget()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

        self._config_widgets()
        self._load_analysis_data()

        if self.load_input_surface_id():
            return

        self.geometry_selection_callback()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.main_window.show_geometry_render_widget()

    def _load_analysis_data(self):
        self.analysis_method = ""
        analysis_data = self.project.analysis_data
        if "analysis_id" in analysis_data.keys():
            if analysis_data["analysis_id"] == 3:
                self.analysis_method = "Direct method"

    def _initialize(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "dB"

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_processing_selector: QComboBox

        # QLineEdit
        self.lineEdit_output_surface_id: QLineEdit
        self.lineEdit_input_surface_id: QLineEdit

        # QPushButton
        self.pushButton_export_data: QPushButton
        self.pushButton_plot_data: QPushButton
        self.pushButton_flip_selection: QPushButton

    def _create_connections(self):
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_flip_selection.clicked.connect(self.invert_selection)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.clickable(self.lineEdit_input_surface_id).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_output_surface_id).connect(self.lineEdit_2_clicked)

    def _config_widgets(self):
        self.current_lineEdit = self.lineEdit_output_surface_id
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
    
    def geometry_selection_callback(self):

        faces = self.main_window.selected_geometry_surfaces

        if faces:

            if len(faces) > 1:
                return

            else:
                _faces = [str(i) for i in faces]
                self.current_lineEdit.setText(_faces[0])

        else:
            return

    def load_input_surface_id(self):

        surface_ids = list()
        for (property, id) in self.properties.surface_properties.keys():
            if property == "surface_velocity":
                if id not in surface_ids:
                    surface_ids.append(id)

        if len(surface_ids) == 1:
            self.lineEdit_input_surface_id.setText(str(surface_ids[0]))
            self.lineEdit_output_surface_id.setFocus()
        else:
            self.close()
            title = "Surface velocity not detected"
            message = "The surface velocity excitation was not detected in the model settings, therefore, "
            message += "the transmission loss calculation has been aborted. To calculate the transmission loss properly, "
            message += " it is recommended that the surface velocity be applied at the input face also "
            message += "the specific impedances be applied in both input and output faces."
            PrintMessageInput([window_title_1, title, message])
            return True

    def invert_selection(self):
        temp_text_input = self.lineEdit_input_surface_id.text()
        temp_text_output = self.lineEdit_output_surface_id.text()
        self.lineEdit_input_surface_id.setText(temp_text_output)
        self.lineEdit_output_surface_id.setText(temp_text_input)

    def plot_data_callback(self):

        self.mesh.nodal_normals_data.clear()

        if self.check_inputs():
            return

        if self.join_model_data():
            return

        self.plotter = FrequencyResponsePlotter()
        self.plotter.imported_dB_data()
        self.plotter._set_model_results_data_to_plot(self.model_results)
        app().main_window.mesh_widget.update_symbols()

    def export_data_callback(self):

        if self.check_inputs():
            return

        if self.join_model_data():
            return

        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def check_inputs(self):

        input_surface_id = self.lineEdit_input_surface_id.text()
        self.input_surface_id = self.mesh.check_selected_ids(   
                                                             input_surface_id, 
                                                             selection = "surfaces", 
                                                             single_id = True
                                                             )

        if self.input_surface_id is None:
            self.lineEdit_output_surface_id.setFocus()
            return True

        output_surface_id = self.lineEdit_output_surface_id.text()
        self.output_surface_id = self.mesh.check_selected_ids(  
                                                              output_surface_id, 
                                                              selection = "surfaces", 
                                                              single_id = True
                                                              )

        if self.output_surface_id is None:
            self.lineEdit_output_surface_id.setFocus()
            return True

    def join_model_data(self):

        self.model_results = dict()

        if self.comboBox_processing_selector.currentIndex() == 0:
            plot_type = "Transmission loss"

            def transmission_loss_callback():

                surface_ids = [self.input_surface_id, self.output_surface_id]

                logging.info("Processing the transmission loss..." + ProgressStatus(10, 100))
                self.mesh._process_face_elements_connected_to_nodes(surface_ids)

                logging.info("Processing the transmission loss..." + ProgressStatus(20, 100))
                self.mesh._process_nodal_areas()

                x_data, y_data = self.project.acoustic_harmonic_solver.get_transmission_loss(
                                                                                            self.input_surface_id, 
                                                                                            self.output_surface_id
                                                                                            )

                return x_data, y_data

            tl_callback = load_function(transmission_loss_callback, self.main_window)
            x_data, y_data = tl_callback()

        else:
            plot_type = "Noise reduction"
            x_data, y_data = self.project.acoustic_harmonic_solver.get_noise_reduction( self.input_surface_id, 
                                                                                        self.output_surface_id )

        if y_data is None:
            title = "Invalid input surface id"
            message = "An invalid surface id has been selected at Input ID field. "
            message += "Check if the Input ID has a surface velocity excitation to proceed."
            PrintMessageInput([window_title_1, title, message])
            return True

        self.title = f"{plot_type} - {self.analysis_method}"
        legend_label = f"{plot_type} between surfaces [{self.input_surface_id}] and [{self.output_surface_id}]"

        key = ("surface", (self.input_surface_id, self.output_surface_id))

        self.model_results[key] = { 
                                    "x_data" : x_data,
                                    "y_data" : y_data,
                                    "x_label" : "Frequency [Hz]",
                                    "y_label" : plot_type,
                                    "title" : self.title,
                                    "data_type" : plot_type.lower(),
                                    "legend" : legend_label,
                                    "unit" : self.unit_label,
                                    "color" : [0,0,1],
                                    "linestyle" : "-"  
                                    }

    def plot_nodal_normals(self, normals_data: dict):
        
        app().main_window.mesh_widget.update_symbols()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        # self.keep_window_open = False
        return super().closeEvent(a0)