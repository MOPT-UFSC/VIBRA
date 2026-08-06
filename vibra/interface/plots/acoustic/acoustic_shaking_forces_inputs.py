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
from vibra.interface.ui_generated.plots.acoustic.acoustic_shaking_forces_inputs_ui import AcousticShakingForcesInputs_UI


class SelectionType(IntEnum):
    ALL_SURFACES = 0
    SELECTED_SURFACES = 1


class OutputMode(IntEnum):
    RESULTING_LOADS = 0
    INDIVIDUAL_LOADS = 1


class CutoffFrequency(IntEnum):
    DISABLED = 0
    USER_DEFINED = 1
    AUTOMATIC = 2


class AcousticShakingForcesInputs(AcousticShakingForcesInputs_UI):
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

    def _load_analysis_setup_and_solution(self):
        self.analysis_method = ""
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.analysis_method = "Direct method"

        self.frequencies = app().project.model.frequencies

    def _initialize(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "N"

    def _config_widgets(self):
        #
        unit = units_abreviations.get(self.mesh.length_unit)
        self.label_unit_combo_box.setText(f"[{unit}]")

    def _configure_validator(self):
        self.lineEdit_cutoff_frequency.setValidator(StrictDoubleValidator(0, 1e8, 6))

    def _create_connections(self):

        # QComboBox connections
        self.comboBox_cutoff_frequency.currentIndexChanged.connect(self.compute_pipe_cutoff_frequency_callback)
        self.comboBox_cutoff_frequency_options.currentIndexChanged.connect(self.cutoff_frequency_options_callback)
        self.comboBox_selector_filter.currentIndexChanged.connect(self.selection_mode_callback)

        # QPushButton connections
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        self.update_cutoff_related_widgets_visibility()

    def geometry_selection_callback(self):

        if not app().main_window.action_results_workspace.isChecked():
            return

        surfaces = app().main_window.selection.geometry_surfaces
        if not surfaces:
            return

        self.comboBox_selector_filter.setCurrentIndex(SelectionType.SELECTED_SURFACES)

        text = ", ".join([str(i) for i in surfaces])
        self.lineEdit_selection_id.setText(text)

    def check_inputs(self):

        if self.comboBox_selector_filter.currentIndex() == SelectionType.ALL_SURFACES:
            error_data = None
            self.selected_ids = np.unique(self.mesh.faces_connectivity[:, 1]).astype(int)

        else:
            self.selected_ids, error_data = self.mesh.check_selected_ids(
                self.lineEdit_selection_id.text(),
                selection = "surfaces",
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

    def process_acoustic_loads(self) -> dict:

        load_data = {}
        acoustic_postprocessing = app().project.get_acoustic_postprocessing()
        # all_surfaces = self.comboBox_selector_filter.currentIndex() == SelectionType.ALL_SURFACES

        if self.comboBox_output_mode.currentIndex() == OutputMode.RESULTING_LOADS:
            acoustic_load = acoustic_postprocessing.calculate_loads_caused_by_acoustic_pressure_field(
                self.nodal_solution,
                surface_ids=self.selected_ids,
                )

            if self.comboBox_selector_filter.currentIndex() == SelectionType.ALL_SURFACES:
                load_data["all_surfaces"] = acoustic_load
            else:
                load_data[tuple(self.selected_ids)] = acoustic_load
            
        else:
            for surface_id in self.selected_ids:
                acoustic_load = acoustic_postprocessing.calculate_loads_caused_by_acoustic_pressure_field(
                    self.nodal_solution,
                    surface_ids=[surface_id],
                    )

                load_data[surface_id] = acoustic_load

        return load_data

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

        self.map_curvatures_to_fluid = {}
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
            return
        
        if not self.map_curvatures_to_fluid:
            return
        
        key = float(self.comboBox_cutoff_frequency.currentText())
        data = self.map_curvatures_to_fluid.get(key)
        if data is None:
            return

        d_in, fluid = data
        if not isinstance(fluid, Fluid):
            return

        if d_in == 0:
            return

        # speed of sound in m/s
        Co = fluid.speed_of_sound

        # cut-off frequency of a circular pipe
        d_in = convert_length_unit(d_in, self.mesh.length_unit, "meter")
        f_cut = round(1.8412 * Co / (np.pi * d_in), 4)

        self.lineEdit_cutoff_frequency.setText(str(f_cut))

    def selection_mode_callback(self):

        all_surfaces = self.comboBox_selector_filter.currentIndex() == SelectionType.ALL_SURFACES
        self.comboBox_output_mode.setDisabled(all_surfaces)
        self.lineEdit_selection_id.setDisabled(all_surfaces)

        if all_surfaces:
            self.lineEdit_selection_id.setText("All surfaces")
            self.comboBox_output_mode.setCurrentIndex(OutputMode.RESULTING_LOADS)
            return

        self.lineEdit_selection_id.clear()
        self.geometry_selection_callback()

    def join_model_data(self):

        ind = 0
        self.model_results = {}
        self.title = "Acoustic shaking forces"

        acoustic_loads = self.process_acoustic_loads()

        for i, (surfaces, loads) in enumerate(acoustic_loads.items()):
            for j, load_label in enumerate(["Fx", "Fy", "Fz"]):

                ind += 1
                y_data = loads[j, :]
                key = ("surface", (load_label, surfaces))

                self.model_results[key] = { 
                    "x_data" : self.frequencies,
                    "y_data" : y_data,
                    "x_label" : "Frequency [Hz]",
                    "y_label" : "Acoustic loads",
                    "title" : self.title,
                    "data_type" : "acoustic loads",
                    "legend" : self.get_legend_label(load_label, surfaces),
                    "unit" : self.unit_label,
                    "color" : get_color(3 * i + j),
                    "linestyle" : "-",
                    }

    def get_legend_label(self, load_label: str, surfaces: list[int] | int | str):

        legend_label = ""
        if isinstance(surfaces, str):
            legend_label = f"Acoustic load {load_label} at all surfaces"

        elif isinstance(surfaces, int):
            legend_label = f"Acoustic load {load_label} at surface ({surfaces})"

        else:

            if len(surfaces) == 1:
                legend_label = f"Acoustic load {load_label} at surface ({surfaces[0]})"

            else:
                if len(surfaces) <= 5:
                    text = ", ".join([str(i) for i in surfaces])
                else:
                    text = ", ".join([str(i) for i in surfaces[:5]]) + ", ..."

                legend_label = f"Acoustic load {load_label} at surfaces ({text})"

        return legend_label

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