from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton, QDialog
from PyQt5.QtCore import Qt, QEvent, QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

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

class PlotTransmissionLossInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/ui_files/plots/acoustic/plot_transmission_loss.ui'), self)

        self.main_window = get_main_window()
        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()
        self.project = self.main_window.project
        self.model = self.project.model
        self.properties = self.model.properties

        self._load_icons()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
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
        self.pushButton_call_data_exporter.setIcon(self.export_icon)

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

    def get_TL_NR(self):

        rows_output = self.project.model.mesh.nodes_from_surfaces[self.output_surface_id]
        P_out = np.average(self.solution[rows_output,:], axis=0)

        volume_out = self.project.model.mesh.volume_from_surface[self.output_surface_id][0]
        volume_in = self.project.model.mesh.volume_from_surface[self.input_surface_id][0]

        fluid_out, _ = self.project.model.get_fluid(volume=volume_out)
        fluid_in, _ = self.project.model.get_fluid(volume=volume_in)

        rho_out = fluid_out.fluid_density
        c0_out = fluid_out.speed_of_sound

        rho_in = fluid_in.fluid_density
        c0_in = fluid_in.speed_of_sound

        A_in = self.project.model.surfaces_areas[self.input_surface_id]
        A_out = self.project.model.surfaces_areas[self.output_surface_id]

        # the zero_shift constant is summed to avoid zero values either in P_input2 or P_output2 variables
        zero_shift = 1e-12

        if self.comboBox_processing_selector.currentIndex() == 0:

            # Transmission loss
            surf_velocity = self.project.model.properties.get_surface_velocity(self.input_surface_id)
            if surf_velocity is None:
                return None

            real_values = np.array(surf_velocity["real_values"])
            imag_values = np.array(surf_velocity["imag_values"])
            V_n = real_values + 1j * imag_values
            
            P_in = V_n*rho_in*c0_in / 2
            Prms_in2 = (P_in/np.sqrt(2))**2

            Prms_out2 = np.real(P_out*np.conjugate(P_out)) / 2 + zero_shift

            W_in = 10*np.log10(Prms_in2*A_in/(rho_in*c0_in))
            W_out = 10*np.log10(Prms_out2*A_out/(rho_out*c0_out))
            TL = W_in - W_out

            # TL = 20*np.log10(P_in/P_out) + 20*np.log10(A_in/A_out)

            return TL[1:]

        else:

            # Noise reduction
            rows_input = self.project.model.mesh.nodes_from_surfaces[self.input_surface_id]
            P_in = np.average(self.solution[rows_input,:], axis=0)

            Prms_out2 = np.real(P_out*np.conjugate(P_out)) / 2 + zero_shift
            Prms_in2 = np.real(P_in*np.conjugate(P_in)) / 2 + zero_shift
            NR = 10*np.log10(Prms_in2/Prms_out2)

            return NR[1:]

    def join_model_data(self):

        self.model_results = dict()
        y_data = self.get_TL_NR()
        if y_data is None:
            return

        if self.comboBox_processing_selector.currentIndex() == 0:
            plot_type = "Transmission loss"
        else:
            plot_type = "Noise reduction"

        self.title = f"{plot_type} - {self.analysis_method}"

        legend_label = f"{plot_type} between [{self.output_surface_id}] and [{self.input_surface_id}]"
        self.model_results = {  "x_data" : self.frequencies[1:],
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