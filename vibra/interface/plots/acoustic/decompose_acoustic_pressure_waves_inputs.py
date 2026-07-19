from enum import IntEnum

import numpy as np
from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.engine import AnalysisID
from vibra.engine.properties.fluid import Fluid
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.numeric_checks.unit_utilities import convert_length_unit, units_abreviations
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.ui_generated.plots.acoustic.acoustic_pressure_frequency_response_function_inputs_ui import (
    AcousticPressureFrequencyResponseFunctionInputs_UI,
)


class CutoffFrequency(IntEnum):
    DISABLED = 0
    USER_DEFINED = 1
    AUTOMATIC = 2


class DecomposeAcousticPressureWavesInputs(AcousticPressureFrequencyResponseFunctionInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self._initialize()
        self._config_widgets()
        self._configure_validator()
        self._create_connections()

        self._load_analysis_setup_and_solution()
        self.geometry_selection_callback()
    
    @property
    def model(self):
        return app().project.model

    @property
    def mesh(self):
        return app().project.model.mesh

    @property
    def properties(self):
        return app().project.model.properties

    @property
    def nodal_solution(self):
        return app().project.model.solution.nodal_solution

    def showEvent(self, event):
        super().showEvent(event)
        self.update_render_according_to_selector()

    def _initialize(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "Pa"
        self.selection_types = ["surfaces", "lines", "points", "nodes"]

    def _config_widgets(self):
        self.current_lineEdit = self.lineEdit_output_selected_id
        #
        unit = units_abreviations.get(self.mesh.length_unit)
        self.label_unit_combo_box.setText(f"[{unit}]")

    def _configure_validator(self):
        self.lineEdit_cutoff_frequency.setValidator(StrictDoubleValidator(0, 1e8, 6))

    def _create_connections(self):
        #
        self.comboBox_selector_filter.currentIndexChanged.connect(self.update_render_according_to_selector)
        self.comboBox_cutoff_frequency.currentIndexChanged.connect(self.compute_pipe_cutoff_frequency_callback)
        self.comboBox_cutoff_frequency_options.currentIndexChanged.connect(self.cutoff_frequency_options_callback)
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
        self.update_cutoff_related_widgets_visibility()

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
        if self.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.analysis_method = "Direct method"

        self.frequencies = self.model.frequencies

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

        f_cut = None
        if self.comboBox_cutoff_frequency_options.currentIndex() != CutoffFrequency.DISABLED:
            f_cut = float(self.lineEdit_cutoff_frequency.text()) 

        self.plotter.set_cutoff_frequency(f_cut)
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
            selection=selection,
            single_id=True,
        )

        if error_data is not None:
            self.lineEdit_input_selected_id.setFocus()
            PrintMessageInput(error_data)
            return True

        selected_output_id = self.lineEdit_output_selected_id.text()
        self.output_selection_id, error_data = self.mesh.check_selected_ids(
            selected_output_id,
            selection=selection,
            single_id=True,
        )

        if error_data is not None:
            self.lineEdit_output_selected_id.setFocus()
            PrintMessageInput(error_data)
            return True

        if self.comboBox_cutoff_frequency_options.currentIndex() != CutoffFrequency.DISABLED:
            line_edit = self.lineEdit_cutoff_frequency
            if line_edit.text() == "":
                line_edit.setFocus()
                return True

    def get_response(self):

        index = self.comboBox_selector_filter.currentIndex()

        if index == 0:
            rows_2 = self.mesh.get_nodes_from_surface(self.output_selection_id)
            rows_1 = self.mesh.get_nodes_from_surface(self.input_selection_id)
        elif index == 1:
            rows_2 = self.mesh.get_nodes_from_line(self.output_selection_id)
            rows_1 = self.mesh.get_nodes_from_line(self.input_selection_id)
        elif index == 2:
            rows_2 = self.mesh.nodes_from_points.get(self.output_selection_id)
            rows_1 = self.mesh.nodes_from_points.get(self.input_selection_id)
        else:
            rows_2 = self.output_selection_id
            rows_1 = self.input_selection_id

        if isinstance(rows_2, int) and isinstance(rows_1, int):
            P_2 = self.nodal_solution[rows_2, :]
            P_1 = self.nodal_solution[rows_1, :]

        else:
            P_2 = np.average(self.nodal_solution[rows_2, :], axis=0)
            P_1 = np.average(self.nodal_solution[rows_1, :], axis=0)

        x_2 = np.average(self.mesh.nodal_coordinates[rows_2, 1])
        x_1 = np.average(self.mesh.nodal_coordinates[rows_1, 1])
        # delta = x_2 - x_1

        omega = 2 * np.pi * self.model.frequencies
        vol_ids = self.mesh.volumes_from_surface.get(self.input_selection_id)
   
        fluid: Fluid = self.properties._get_property("fluid", volume=vol_ids[0])

        k = omega / fluid.speed_of_sound

        # P_pos = (P_2 - P_1 * np.exp(1j * k * delta)) / (np.exp(-1j * k * x_2) - np.exp(-1j * k * (x_1 - delta)))
        # P_neg = (P_1 * np.exp(-1j * k * delta) - P_2) / (np.exp(1j * k * (x_1 - delta)) - np.exp(1j * k * x_2))

        P_pos = (P_1 * np.exp(-1j * k * x_1) - P_2 * np.exp(-1j * k * x_2)) / (np.exp(-2 * 1j * k * x_1) - np.exp(-2 * 1j * k * x_2))
        P_neg = (P_1 * np.exp(1j * k * x_1) - P_2 * np.exp(1j * k * x_2)) / (np.exp(2 * 1j * k * x_1) - np.exp(2 * 1j * k * x_2))

        return P_pos, P_neg

    def update_cutoff_related_widgets_visibility(self):
        index = self.comboBox_cutoff_frequency_options.currentIndex()
        user_defined = index == CutoffFrequency.USER_DEFINED
        self.lineEdit_cutoff_frequency.setEnabled(user_defined)

        automatic = index == CutoffFrequency.AUTOMATIC
        self.comboBox_cutoff_frequency.setVisible(automatic)
        self.label_fc_combo_box.setVisible(automatic)
        self.label_unit_combo_box.setVisible(automatic)

    def cutoff_frequency_options_callback(self):
        index = self.comboBox_cutoff_frequency_options.currentIndex()
        self.update_cutoff_related_widgets_visibility()

        if index == CutoffFrequency.DISABLED:
            self.lineEdit_cutoff_frequency.clear()

        elif index == CutoffFrequency.AUTOMATIC:
            self.map_cylindrical_surfaces_to_fluids()
            self.compute_pipe_cutoff_frequency_callback()

    def map_cylindrical_surfaces_to_fluids(self):

        self.map_curvatures_to_fluid = dict()
        self.comboBox_cutoff_frequency.clear()
        self.comboBox_cutoff_frequency.blockSignals(True)

        for surface_id, diameter in self.mesh.cylindrical_surfaces_data.items():

            d_in = convert_length_unit(diameter, "meter", self.mesh.length_unit)
            dr_in = round(d_in, 4)

            fluid = self.properties._get_property("fluid", surface=surface_id)
            if isinstance(fluid, Fluid):
                if (dr_in, fluid) not in self.map_curvatures_to_fluid.values():
                    self.map_curvatures_to_fluid[dr_in] = (dr_in, fluid)

            elif isinstance(fluid, list) and len(fluid) == 2:
                for _fluid in fluid:
                    if not isinstance(_fluid, Fluid):
                        continue

                    if (dr_in, _fluid) not in self.map_curvatures_to_fluid.values():
                        self.map_curvatures_to_fluid[dr_in] = (dr_in, _fluid)

        for (_d_in, fluid) in self.map_curvatures_to_fluid.values():
            self.comboBox_cutoff_frequency.addItem(str(_d_in))

        max_din = max(self.map_curvatures_to_fluid.keys())
        self.comboBox_cutoff_frequency.setCurrentText(str(max_din))
        self.comboBox_cutoff_frequency.blockSignals(False)

    def compute_pipe_cutoff_frequency_callback(self):
        if self.comboBox_cutoff_frequency.currentText() == "":
            return None
        
        if not self.map_curvatures_to_fluid:
            return None
        
        key = float(self.comboBox_cutoff_frequency.currentText())
        data = self.map_curvatures_to_fluid.get(key)
        if data is None:
            return None

        d_in, fluid = data
        if not isinstance(fluid, Fluid):
            return None

        if d_in == 0:
            return None

        # speed of sound in m/s
        Co = fluid.speed_of_sound

        # cut-off frequency of a circular pipe
        d_in = convert_length_unit(d_in, self.mesh.length_unit, "meter")
        f_cut = round(1.8412 * Co / (np.pi * d_in), 4)

        self.lineEdit_cutoff_frequency.setText(str(f_cut))

    def join_model_data(self):

        current_text = self.comboBox_selector_filter.currentText()
        selection_type = current_text.lower()[:-1]

        self.model_results = dict()
        P_pos, P_neg = self.get_response()
        if P_pos is None:
            return

        title = "Acoustic pressure waves spectrum"
        # legend_label = "Acoustic FRF between {}s [{}] and [{}]".format(selection_type, self.output_selection_id, self.input_selection_id)

        legends = ["Positive wave pressure", "Negative wave pressure"]
        selection_ids = (self.input_selection_id, self.output_selection_id)

        colors = ((0,0,0), (1,0,0))

        for i, y_data in enumerate([P_pos, P_neg]):

            key = (selection_type, selection_ids[i])

            self.model_results[key] = {
                "x_data": self.frequencies,
                "y_data": y_data,
                "x_label": "Frequency [Hz]",
                "y_label": "Acoustic pressures wave",
                "title": title,
                "data_type": "acoustic pressures waves",
                "legend": legends[i],
                "unit": self.unit_label,
                "color": colors[i],
                "linestyle": "-",
            }

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