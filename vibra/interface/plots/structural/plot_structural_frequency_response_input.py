from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QRadioButton
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from vibra import app, UI_DIR

from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

import numpy as np

window_title1 = "Error"
window_title2 = "Warning"

class PlotStructuralFrequencyResponseInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots_/results_/structural_/plot_structural_frequency_response.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()
        self.project = self.main_window.project
        self.model = self.project.model
        self.properties = self.model.properties

        self._config_window()
        self._load_icons()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.writeNodes(self.list_node_IDs)
        self.exec()

    def _config_window(self):
        self.vibra_icon = app().main_window.vibra_icon
        self.setWindowIcon(self.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _initialize(self):
        self.dof_labels = ["Ux", "Uy", "Uz", "Rx", "Ry", "Rz"]

    def _define_qt_variables(self):
        # LineEdit
        self.lineEdit_node_id = self.findChild(QLineEdit, 'lineEdit_node_id')
        # PushButton
        self.pushButton_call_data_exporter = self.findChild(QPushButton, 'pushButton_call_data_exporter')
        self.pushButton_plot_frequency_response = self.findChild(QPushButton, 'pushButton_plot_frequency_response')
        self.pushButton_call_data_exporter.setIcon(self.export_icon)
        # RadioButton
        self.radioButton_ux = self.findChild(QRadioButton, 'radioButton_ux')
        self.radioButton_uy = self.findChild(QRadioButton, 'radioButton_uy')
        self.radioButton_uz = self.findChild(QRadioButton, 'radioButton_uz')
        self.radioButton_rx = self.findChild(QRadioButton, 'radioButton_rx')
        self.radioButton_ry = self.findChild(QRadioButton, 'radioButton_ry')
        self.radioButton_rz = self.findChild(QRadioButton, 'radioButton_rz')

    def _create_connections(self):
        self.pushButton_call_data_exporter.clicked.connect(self.call_data_exporter)
        self.pushButton_plot_frequency_response.clicked.connect(self.call_plotter)
    
    def _load_icons(self):
        self.icon = app().main_window.vibra_icon
        self.setWindowIcon(self.icon)

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_node_id.setText(text)

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

    def check_inputs(self):

        lineEdit_node_id = self.lineEdit_node_id.text()
        stop, self.node_ID = self.before_run.check_input_NodeID(lineEdit_node_id, single_ID=True)
        if stop:
            self.lineEdit_node_id.setFocus()
            return True

        if self.radioButton_ux.isChecked():
            self.local_dof = 0
        elif self.radioButton_uy.isChecked():
            self.local_dof = 1
        elif self.radioButton_uz.isChecked():
            self.local_dof = 2
        elif self.radioButton_rx.isChecked():
            self.local_dof = 3
        elif self.radioButton_ry.isChecked():
            self.local_dof = 4
        else:
            self.local_dof = 5

        self.local_dof_label = self.dof_labels[self.local_dof]

        if self.local_dof in [0, 1, 2]:
            self.unit_label = "m"
        else:
            self.unit_label = "rad"

        return False

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
        self.title = "Structural frequency response - {}".format(self.analysisMethod)
        legend_label = "Response {} at node {}".format(self.local_dof_label, self.node_ID)
        data_information = "Structural nodal response {} at node {}".format(self.local_dof_label, self.node_ID)
        self.model_results = {  "x_data" : self.frequencies,
                                "y_data" : self.get_response(),
                                "x_label" : "Frequency [Hz]",
                                "y_label" : "Nodal response",
                                "title" : self.title,
                                "data_information" : data_information,
                                "legend" : legend_label,
                                "unit" : self.unit_label,
                                "color" : [0,0,1],
                                "linestyle" : "-"  }

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.call_plotter()
        elif event.key() == Qt.Key_Escape:
            self.close()