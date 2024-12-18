from PySide6.QtWidgets import QComboBox, QDialog, QLineEdit, QPushButton, QRadioButton
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt
from PySide6 import uic

from vibra import app, UI_DIR
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance

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

        self.project = app().main_window.project
        self.model = app().main_window.project.model
        self.mesh = app().main_window.project.model.mesh
        self.properties = app().main_window.project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)

    def _initialize(self):
        self.keep_window_open = True
        self.plotter = None
        self.exporter = None
        self.dof_labels = ["Ux", "Uy", "Uz", "Rx", "Ry", "Rz"]

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_selector_filter : QComboBox

        # QLineEdit
        self.lineEdit_selection_id : QLineEdit

        # QPushButton
        self.pushButton_export_data : QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_plot_data : QPushButton

        # RadioButton
        self.radioButton_ux : QRadioButton
        self.radioButton_uy : QRadioButton
        self.radioButton_uz : QRadioButton
        self.radioButton_rx : QRadioButton
        self.radioButton_ry : QRadioButton
        self.radioButton_rz : QRadioButton

    def _create_connections(self):
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_cancel.clicked.connect(self.close)
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