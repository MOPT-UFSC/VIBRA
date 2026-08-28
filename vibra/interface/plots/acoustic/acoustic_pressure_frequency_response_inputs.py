from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.engine import AnalysisID
from vibra.engine.properties.fluid import Fluid
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.numeric_checks.unit_utilities import convert_length_unit, units_abreviations
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.ui_generated.plots.acoustic.acoustic_pressure_frequency_response_inputs_ui import AcousticPressureFrequencyResponseInputs_UI


class SelectionType(IntEnum):
    SURFACES = 0
    LINES = 1
    POINTS = 2
    NODES = 3


class CutoffFrequency(IntEnum):
    DISABLED = 0
    USER_DEFINED = 1
    AUTOMATIC = 2


class AcousticPressureFrequencyResponseInputs(AcousticPressureFrequencyResponseInputs_UI):
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

    def _load_analysis_setup_and_solution(self):
        self.analysis_method = ""
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.analysis_method = "Direct method"

        self.frequencies = app().project.model.frequencies

    def _initialize(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "Pa"
        self.selection_types = ["surfaces", "lines", "points", "nodes"]

    def _config_widgets(self):
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
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.update_cutoff_related_widgets_visibility()

    def geometry_selection_callback(self):

        if not app().main_window.action_results_workspace.isChecked():
            return

        surfaces = app().main_window.selection.geometry_surfaces
        lines = app().main_window.selection.geometry_lines
        points = app().main_window.selection.geometry_points
        nodes = app().main_window.selection.mesh_nodes

        index = self.comboBox_selector_filter.currentIndex()
        if surfaces and index == SelectionType.SURFACES:
            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)

        elif lines and index == SelectionType.LINES:
            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)

        elif points and index == SelectionType.POINTS:
            text = ", ".join([str(i) for i in points])
            self.lineEdit_selection_id.setText(text)

        elif nodes and index == SelectionType.NODES:
            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)

        elif not any([nodes, points, lines, surfaces]):
            self.lineEdit_selection_id.setText("")

    def update_render_according_to_selector(self):

        self.geometry_selection_callback()

        if self.comboBox_selector_filter.currentIndex() == 3:
            app().main_window.show_mesh_render_widget()
        else:
            app().main_window.show_geometry_render_widget()

    def check_inputs(self):

        index = self.comboBox_selector_filter.currentIndex()
        selection = self.selection_types[index]

        input_ids = self.lineEdit_selection_id.text()
        self.selected_ids, error_data = self.mesh.check_selected_ids(
            input_ids,
            selection = selection,
            single_id = False,
            )

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        if self.comboBox_cutoff_frequency_options.currentIndex() != CutoffFrequency.DISABLED:
            line_edit = self.lineEdit_cutoff_frequency
            if line_edit.text() == "":
                line_edit.setFocus()
                return True

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

    def get_response(self, selected_id: int):

        index = self.comboBox_selector_filter.currentIndex()

        if index == SelectionType.SURFACES:
            nodes = self.mesh.get_nodes_from_surface(selected_id)
        elif index == SelectionType.LINES:
            nodes = self.mesh.get_nodes_from_line(selected_id)
        elif index == SelectionType.POINTS:
            nodes = self.mesh.nodes_from_points.get(selected_id)
        elif index == SelectionType.NODES:
            nodes = selected_id
        else:
            return None

        indices = self.model.fluid_node_mapping[nodes]

        if isinstance(indices, int):
            response = self.nodal_solution[indices, :]
        else:
            response = np.average(self.nodal_solution[indices, :], axis=0)

        if complex(0) in response:
            response += 1e-12
        #     response += np.ones(len(response), dtype=float)*(1e-12)

        return response

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

        index = self.comboBox_selector_filter.currentIndex()
        selection_type = self.selection_types[index][:-1]

        self.model_results = dict()
        self.title = "Acoustic frequency response"

        for i, selected_id in enumerate(self.selected_ids):

            key = (selection_type, (selected_id))
            legend_label = f"Acoustic pressure at {selection_type} [{selected_id}]"

            y_data = self.get_response(selected_id)
            if y_data is None:
                continue

            self.model_results[key] = { 
                "x_data" : self.frequencies,
                "y_data" : y_data,
                "x_label" : "Frequency [Hz]",
                "y_label" : "Acoustic pressure",
                "title" : self.title,
                "data_type" : "acoustic pressure",
                "legend" : legend_label,
                "unit" : self.unit_label,
                "color" : get_color(i),
                "linestyle" : "-",
                }

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        return super().closeEvent(a0)

def get_color(index: int):

    colors = [
        (0, 0, 1),
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
        (0.25, 0.25, 0.25),
    ]

    if index <= 6:
        return colors[index]
    else:
        return tuple(np.random.randint(0, 255, size=3) / 255)