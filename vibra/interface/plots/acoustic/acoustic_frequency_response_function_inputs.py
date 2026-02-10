from PySide6.QtCore import Qt, QEvent, QObject, Signal
from PySide6.QtGui import QCloseEvent

from vibra.engine import AnalysisID
from vibra import app
from vibra.interface.ui_generated.plots.acoustic.acoustic_pressure_frequency_response_function_inputs_ui import AcousticPressureFrequencyResponseFunctionInputs_UI
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class AcousticPressureFrequencyResponseFunctionInputs(AcousticPressureFrequencyResponseFunctionInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._configure_qt_variables()
        self._create_connections()

        self._load_analysis_setup_and_solution()
        self.geometry_selection_callback()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.update_render_according_to_selector()

    def _initialize(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "Pa/Pa"
        self.selection_types = ["surfaces", "lines", "points", "nodes"]

    def _configure_qt_variables(self):
        self.current_lineEdit = self.lineEdit_output_selected_id

    def _create_connections(self):
        #
        self.comboBox_selector_filter.currentIndexChanged.connect(self.update_render_according_to_selector)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_flip_selection.clicked.connect(self.flip_nodes)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.clickable(self.lineEdit_input_selected_id).connect(self.lineEdit_input_clicked)
        self.clickable(self.lineEdit_output_selected_id).connect(self.lineEdit_output_clicked)
        #
        self.lineEdit_output_clicked()

    def update_render_according_to_selector(self):

        self.geometry_selection_callback()

        if self.comboBox_selector_filter.currentIndex() == 3:
            app().main_window.show_mesh_render_widget()
        else:
            app().main_window.show_geometry_render_widget()

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

    def lineEdit_input_clicked(self):
        self.current_lineEdit = self.lineEdit_input_selected_id
        self.highlight_selected_line_edit()

    def lineEdit_output_clicked(self):
        self.current_lineEdit = self.lineEdit_output_selected_id
        self.highlight_selected_line_edit()

    def highlight_selected_line_edit(self):

        if self.current_lineEdit == self.lineEdit_input_selected_id:
            self.lineEdit_output_selected_id.setStyleSheet("")
        else:
            self.lineEdit_input_selected_id.setStyleSheet("")

        self.current_lineEdit.setStyleSheet("""border-color: rgb(32, 207, 255); border-width: 2px;""")

    def alternate_selected_line_edit(self):
        if self.current_lineEdit == self.lineEdit_input_selected_id:
            self.lineEdit_output_clicked()
            self.lineEdit_output_selected_id.setFocus()
        else:
            self.lineEdit_input_clicked()
            self.lineEdit_input_selected_id.setFocus()

    def _load_analysis_setup_and_solution(self):

        self.analysis_method = ""
        analysis_setup = self.project.analysis_setup

        if "analysis_id" in analysis_setup.keys():
            if analysis_setup["analysis_id"] == AnalysisID.ACOUSTIC_HARMONIC:
                self.analysis_method = "Direct method"

        self.frequencies = app().project.model.frequencies
        self.solution = self.project.acoustic_harmonic_solver.solution

    def geometry_selection_callback(self):

        if not app().main_window.action_results_workspace.isChecked():
            return

        surfaces = app().main_window.selection.geometry_surfaces
        lines = app().main_window.selection.geometry_lines
        points = app().main_window.selection.geometry_points
        nodes = app().main_window.selection.mesh_nodes

        index = self.comboBox_selector_filter.currentIndex()
        if surfaces and index == 0:

            if len(surfaces) > 1:
                return

            else:
                _surfaces = [str(i) for i in surfaces]
                self.current_lineEdit.setText(_surfaces[0])

        elif lines and index == 1:

            if len(lines) > 1:
                return

            else:
                _lines = [str(i) for i in lines]
                self.current_lineEdit.setText(_lines[0])

        elif points and index == 2:

            if len(points) > 1:
                return

            else:
                _points = [str(i) for i in points]
                self.current_lineEdit.setText(_points[0])

        elif nodes and index == 3:
            
            if len(nodes) > 1:
                return

            else:
                _nodes = [str(i) for i in nodes]
                self.current_lineEdit.setText(_nodes[0])

        elif not any([nodes, lines, points, nodes]):
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
        self.plotter = FrequencyResponsePlotter(close_dialogs=True)
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def export_data_callback(self):

        if self.check_inputs():
            return

        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def check_inputs(self):

        index = self.comboBox_selector_filter.currentIndex()
        selection = self.selection_types[index]
 
        selected_input_id = self.lineEdit_input_selected_id.text()
        self.input_selection_id, error_data = self.mesh.check_selected_ids(   
                                                                           selected_input_id, 
                                                                           selection = selection, 
                                                                           single_id = True
                                                                           )

        if error_data is not None:
            self.lineEdit_input_selected_id.setFocus()
            PrintMessageInput(error_data)
            return True

        selected_output_id = self.lineEdit_output_selected_id.text()
        self.output_selection_id, error_data = self.mesh.check_selected_ids(  
                                                                            selected_output_id, 
                                                                            selection = selection, 
                                                                            single_id = True
                                                                            )

        if error_data is not None:
            self.lineEdit_output_selected_id.setFocus()
            PrintMessageInput(error_data)
            return True

    def get_response(self):

        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            rows_num = self.project.model.mesh.get_nodes_from_surface(self.output_selection_id)
            rows_den = self.project.model.mesh.get_nodes_from_surface(self.input_selection_id)
        elif index == 1:
            rows_num = self.project.model.mesh.get_nodes_from_line(self.output_selection_id)
            rows_den = self.project.model.mesh.get_nodes_from_line(self.input_selection_id)
        elif index == 2:
            rows_num = self.project.model.mesh.nodes_from_points.get(self.output_selection_id)
            rows_den = self.project.model.mesh.nodes_from_points.get(self.input_selection_id)
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

        current_text = self.comboBox_selector_filter.currentText()
        selection_type = current_text.lower()[:-1]

        self.model_results = dict()
        y_data = self.get_response()
        if y_data is None:
            return

        title = "Acoustic frequency response function"
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

    def get_color(self, index: int):

        colors = [  
                  (0, 0, 1), 
                  (0, 0, 0), 
                  (1, 0, 0),
                  (1, 1, 0), 
                  (1, 0, 1), 
                  (0, 1, 1),
                  (0.25, 0.25, 0.25)
                  ]

        if index <= 6:
            return colors[index]
        else:
            return tuple(np.random.randint(0, 255, size=3))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()
        elif event.key() == Qt.Key_Down or event.key() == Qt.Key_Up:
            self.alternate_selected_line_edit()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        return super().closeEvent(a0)