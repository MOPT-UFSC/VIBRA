from enum import IntEnum

import numpy as np
from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.engine import AnalysisID
from vibra.engine.properties.fluid import Fluid
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.utils import clear_style_sheet

# from vibra.interface.numeric_checks.int_list_validator import IntListValidator
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.ui_generated.plots.acoustic.acoustic_waves_decomposition_inputs_ui import AcousticWavesDecompositionInputs_UI


class CutoffFrequency(IntEnum):
    DISABLED = 0
    USER_DEFINED = 1
    AUTOMATIC = 2


class SelectionType(IntEnum):
    SURFACES = 0
    LINES = 1
    POINTS = 2
    NODES = 3


class AcousticWavesDecompositionInputs(AcousticWavesDecompositionInputs_UI):
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

    def _initialize(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "Pa"

    def _config_widgets(self):
        self.current_lineEdit = self.lineEdit_output_selected_id

    def _configure_validator(self):
        pass

    def _create_connections(self):
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
        line_edits = [self.lineEdit_input_selected_id, self.lineEdit_output_selected_id]
        clear_style_sheet([line_edit for line_edit in line_edits if line_edit is not self.current_lineEdit])
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
        if len(surfaces) != 1:
            return

        _surfaces = [str(i) for i in surfaces]
        self.current_lineEdit.setText(_surfaces[0])

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
 
        selected_input_id = self.lineEdit_input_selected_id.text()
        self.input_selection_id, error_data = self.mesh.check_selected_ids(selected_input_id, selection="surfaces", single_id=True)

        if error_data is not None:
            self.lineEdit_input_selected_id.setFocus()
            PrintMessageInput(error_data)
            return True

        selected_output_id = self.lineEdit_output_selected_id.text()
        self.output_selection_id, error_data = self.mesh.check_selected_ids(selected_output_id, selection="surfaces", single_id=True)

        if error_data is not None:
            self.lineEdit_output_selected_id.setFocus()
            PrintMessageInput(error_data)
            return True

    def get_response(self):

        rows_2 = self.mesh.get_nodes_from_surface(self.output_selection_id)
        rows_1 = self.mesh.get_nodes_from_surface(self.input_selection_id)

        if isinstance(rows_2, int) and isinstance(rows_1, int):
            P_2 = self.nodal_solution[rows_2, :]
            P_1 = self.nodal_solution[rows_1, :]

        else:
            P_2 = np.average(self.nodal_solution[rows_2, :], axis=0)
            P_1 = np.average(self.nodal_solution[rows_1, :], axis=0)

        x_2 = np.average(self.mesh.nodal_coordinates[rows_2, 1])
        x_1 = np.average(self.mesh.nodal_coordinates[rows_1, 1])

        omega = 2 * np.pi * self.model.frequencies
        vol_ids = self.mesh.volumes_from_surface.get(self.input_selection_id)
   
        fluid: Fluid = self.properties._get_property("fluid", volume=vol_ids[0])

        k = omega / fluid.speed_of_sound

        P_pos = (P_1 * np.exp(-1j * k * x_1) - P_2 * np.exp(-1j * k * x_2)) / (np.exp(-2 * 1j * k * x_1) - np.exp(-2 * 1j * k * x_2))
        P_neg = (P_1 * np.exp(1j * k * x_1) - P_2 * np.exp(1j * k * x_2)) / (np.exp(2 * 1j * k * x_1) - np.exp(2 * 1j * k * x_2))

        return P_pos, P_neg

    def join_model_data(self):

        self.model_results = dict()
        P_pos, P_neg = self.get_response()
        if P_pos is None:
            return

        title = "Acoustic pressure waves spectrum"
        legends = ["Positive wave pressure", "Negative wave pressure"]
        selection_ids = (self.input_selection_id, self.output_selection_id)

        colors = ((0,0,0), (1,0,0))

        for i, y_data in enumerate([P_pos, P_neg]):

            key = ("surface", selection_ids[i])

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