from PySide6.QtWidgets import QComboBox, QLineEdit, QPushButton, QDialog, QWidget
from PySide6.QtCore import Qt, QEvent, QObject, Signal
from PySide6.QtGui import QCloseEvent

from vibra import app, UI_DIR
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

from molde import load_ui

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class PlotAcousticPressureFrequencyResponseFunctionInput(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/acoustic/plot_acoustic_pressure_frequency_response_function.ui"
        load_ui(ui_path, self, ui_path.parent)

        self.main_window = app().main_window
        self.main_window.show_geometry_render_widget()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        self._load_analysis_data_and_solution()
        self.geometry_selection_callback()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.update_render_according_to_selector()

    def _initialize(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "Pa/Pa"

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_selector_filter : QComboBox

        # QLineEdit
        self.lineEdit_output_selected_id : QLineEdit
        self.lineEdit_input_selected_id : QLineEdit
        self.current_lineEdit = self.lineEdit_output_selected_id

        # QPushButton
        self.pushButton_export_data : QPushButton
        self.pushButton_plot_data : QPushButton
        self.pushButton_flip_selection : QPushButton

    def _create_connections(self):
        #
        self.comboBox_selector_filter.currentIndexChanged.connect(self.update_render_according_to_selector)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_flip_selection.clicked.connect(self.flip_nodes)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.clickable(self.lineEdit_input_selected_id).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_output_selected_id).connect(self.lineEdit_2_clicked)

    def update_render_according_to_selector(self):

        self.geometry_selection_callback()

        if self.comboBox_selector_filter.currentIndex() in [0, 1]:
            self.main_window.show_geometry_render_widget()

        else:
            self.main_window.show_mesh_render_widget()

    def clickable(self, widget):
        class Filter(QObject):
            clicked = Signal()

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
        self.current_lineEdit = self.lineEdit_input_selected_id

    def lineEdit_2_clicked(self):
        self.current_lineEdit = self.lineEdit_output_selected_id

    def _load_analysis_data_and_solution(self):

        self.analysis_method = ""
        analysis_data = self.project.analysis_data

        if "analysis_id" in analysis_data.keys():
            if analysis_data["analysis_id"] == 3:
                self.analysis_method = "Direct method"

        self.frequencies = self.project.acoustic_harmonic_solver.frequencies
        self.solution = self.project.acoustic_harmonic_solver.solution

    def geometry_selection_callback(self):
        
        faces = self.main_window.selected_geometry_surfaces
        lines = self.main_window.selected_geometry_lines
        nodes = self.main_window.selected_mesh_nodes

        index = self.comboBox_selector_filter.currentIndex()
        if faces and index == 0:

            if len(faces) > 1:
                return

            else:
                _faces = [str(i) for i in faces]
                self.current_lineEdit.setText(_faces[0])

        if lines and index == 1:

            if len(lines) > 1:
                return

            else:
                _lines = [str(i) for i in lines]
                self.current_lineEdit.setText(_lines[0])

        if nodes and index == 2:
            
            if len(nodes) > 1:
                return

            else:
                _nodes = [str(i) for i in nodes]
                self.current_lineEdit.setText(_nodes[0])

        elif not any([nodes, lines, nodes]):
            return
            self.current_lineEdit.setText("")

    def flip_nodes(self):
        temp_input = self.lineEdit_input_selected_id.text()
        temp_output = self.lineEdit_output_selected_id.text()
        self.lineEdit_input_selected_id.setText(temp_output)
        self.lineEdit_output_selected_id.setText(temp_input)

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

    def check_inputs(self):

        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            selection = "surfaces"

        elif index == 1:
            selection = "lines"

        else:
            selection = "nodes"
 
        selected_input_id = self.lineEdit_input_selected_id.text()
        self.input_selection_id = self.mesh.check_selected_ids(   
                                                               selected_input_id, 
                                                               selection = selection, 
                                                               single_id = True
                                                               )

        if self.input_selection_id is None:
            self.lineEdit_input_selected_id.setFocus()
            return True

        selected_output_id = self.lineEdit_output_selected_id.text()
        self.output_selection_id = self.mesh.check_selected_ids(  
                                                                selected_output_id, 
                                                                selection = selection, 
                                                                single_id = True
                                                                )

        if self.output_selection_id is None:
            self.lineEdit_output_selected_id.setFocus()
            return True

    def get_response(self):

        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            rows_num = self.project.model.mesh.nodes_from_surfaces[self.output_selection_id]
            rows_den = self.project.model.mesh.nodes_from_surfaces[self.input_selection_id]

        elif index == 1:
            rows_num = self.project.model.mesh.nodes_from_lines[self.output_selection_id]
            rows_den = self.project.model.mesh.nodes_from_lines[self.input_selection_id]

        else:
            rows_num = self.output_selection_id
            rows_den = self.input_selection_id

        if isinstance(rows_num, int) and isinstance(rows_den, int):
            numerator = self.solution[rows_num,:]
            denominator = self.solution[rows_den,:]

        else:
            numerator = np.average(self.solution[rows_num,:], axis=0)
            denominator = np.average(self.solution[rows_den,:], axis=0)

        if complex(0) in denominator:
            denominator += 1e-12

        response = numerator / denominator

        if complex(0) in response:
            response += 1e-12

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
        y_data = self.get_response()
        if y_data is None:
            return

        title = "Acoustic frequency response function - {}".format(self.analysis_method)
        legend_label = "Acoustic FRF between {}s [{}] and [{}]".format(  selection_type, 
                                                                    self.output_selection_id, 
                                                                    self.input_selection_id  )

        key = (selection_type, (self.input_selection_id, self.output_selection_id))

        self.model_results[key] = { 
                                    "x_data" : self.frequencies,
                                    "y_data" : y_data,
                                    "x_label" : "Frequency [Hz]",
                                    "y_label" : "Acoustic pressures ratio",
                                    "title" : title,
                                    "data_type" : "acoustic pressures ratio",
                                    "legend" : legend_label,
                                    "unit" : self.unit_label,
                                    "color" : [0,0,1],
                                    "linestyle" : "-"
                                   }

    def get_color(self, index):
        colors = [  (0,0,1), (0,0,0), (1,0,0),
                    (1,1,0), (1,0,1), (0,1,1),
                    (0.25,0.25,0.25)  ]
        
        if index <= 6:
            return colors[index]
        else:
            return tuple(np.random.randint(0, 255, size=3))

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

        return super().closeEvent(a0)