import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDialog, QLineEdit

from vibra import app
from vibra.engine import AnalysisID
from vibra.engine.properties.fluid import Fluid
from vibra.interface import error_title
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.fluid.set_fluid_inputs_simplified import SetFluidInputsSimplified
from vibra.interface.plots.general.frequency_response_plotter import DataFormat, FrequencyResponsePlotter
from vibra.interface.ui_generated.plots.acoustic.allowable_pulsations_2d_for_screw_compressor_inputs_ui import (
    AllowablePulsations2dForScrewCompressorInputs_UI,
)
from vibra.utils.signal_processing import process_ifft_from_one_sided_spectrum_signal


class AllowablePulsations2DPlotForScrewCompressorInputs(AllowablePulsations2dForScrewCompressorInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self._reset_variables()
        self._add_penalization_values_to_combo_box()
        self._create_connections()

        self._load_analysis_setup_and_solution()

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

    def _load_analysis_setup_and_solution(self):
        self.analysis_method = ""
        if self.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.analysis_method = "Direct method"

    def _reset_variables(self):

        self.plotter = None
        self.exporter = None
        self.fluid_dialog = None
        self.selected_fluid = None

        self.model_results = {}

        self.unit_label = "Pa"
        self.selection_types = ["surfaces", "lines", "points", "nodes"]

    def _add_penalization_values_to_combo_box(self):
        self.comboBox_penalization_factor.clear()

        for value in range(0, 100, 5):
            self.comboBox_penalization_factor.addItem(str(value))

        tool_tip = "Use this to reduced the allowable pulsation criteria by (1 - penalization) factor. "
        self.comboBox_penalization_factor.setToolTip(tool_tip)
        self.label_penalization_factor.setToolTip(tool_tip)

    def _create_connections(self):

        # QComboBox connection
        self.comboBox_selector_filter.currentIndexChanged.connect(self.selection_filter_callback)

        # QPushButton connection
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        self.geometry_selection_callback()

    def geometry_selection_callback(self):

        if not app().main_window.action_results_workspace.isChecked():
            return

        surfaces = app().main_window.selection.geometry_surfaces
        lines = app().main_window.selection.geometry_lines
        points = app().main_window.selection.geometry_points
        nodes = app().main_window.selection.mesh_nodes

        index = self.comboBox_selector_filter.currentIndex()
        if surfaces and index == 0:
            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)

        elif lines and index == 1:
            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)

        elif points and index == 2:
            text = ", ".join([str(i) for i in points])
            self.lineEdit_selection_id.setText(text)

        elif nodes and index == 3:
            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)

        else:
            self.lineEdit_selection_id.setText("")

        if surfaces:
            fluid = self.get_fluids_related_to_surfaces_selection(list(surfaces))
            if isinstance(fluid, Fluid):
                self.get_selected_fluid(selected_fluid=fluid)
                return

        if lines:
            fluid = self.get_fluids_related_to_lines_selection(list(lines))
            if isinstance(fluid, Fluid):
                self.get_selected_fluid(selected_fluid=fluid)
                return

        if points:
            fluid = self.get_fluids_related_to_points_selection(list(points))
            if isinstance(fluid, Fluid):
                self.get_selected_fluid(selected_fluid=fluid)
                return

        if nodes:
            fluid = self.get_fluids_related_to_nodes_selection(list(nodes))
            if isinstance(fluid, Fluid):
                self.get_selected_fluid(selected_fluid=fluid)
                return            

    def get_fluids_related_to_surfaces_selection(self, selected_surfaces: list[int]):
        fluids = list()
        for surface_id in selected_surfaces:
            for volume_id in self.mesh.volumes_from_surface.get(surface_id, list()):
                fluid = self.properties._get_property("fluid", volume=volume_id)
                if fluid not in fluids:
                    fluids.append(fluid)

        if len(fluids) == 1:
            return fluids[0]

        return list()

    def get_fluids_related_to_lines_selection(self, selected_lines: list[int]):
        fluids = list()
        for line_id in selected_lines:
            for surface_id in self.mesh.surfaces_from_line.get(line_id, list()):
                for volume_id in self.mesh.volumes_from_surface.get(surface_id, list()):
                    fluid = self.properties._get_property("fluid", volume=volume_id)
                    if fluid not in fluids:
                        fluids.append(fluid)

        if len(fluids) == 1:
            return fluids[0]

        return list()

    def get_fluids_related_to_points_selection(self, selected_points: list[int]):
        fluids = list()
        for point_id in selected_points:
            for line_id in self.mesh.lines_from_point.get(point_id, list()):
                for surface_id in self.mesh.surfaces_from_line.get(line_id, list()):
                    for volume_id in self.mesh.volumes_from_surface.get(surface_id, list()):
                        fluid = self.properties._get_property("fluid", volume=volume_id)
                        if fluid not in fluids:
                            fluids.append(fluid)

        if len(fluids) == 1:
            return fluids[0]

        return list()

    def get_fluids_related_to_nodes_selection(self, selected_nodes: list[int]):
        fluids = list()
        volume_ids = self.mesh.get_volumes_from_selected_nodes(selected_nodes, return_volumes=True)
        for volume_id in volume_ids:
            fluid = self.properties._get_property("fluid", volume=volume_id)
            if fluid not in fluids:
                fluids.append(fluid)

        if len(fluids) == 1:
            return fluids[0]

        return list()

    def selection_filter_callback(self):

        self.geometry_selection_callback()
        if self.comboBox_selector_filter.currentIndex() == 3:
            app().main_window.show_mesh_render_widget()
        else:
            app().main_window.show_geometry_render_widget()

    def check_selected_ids(self):

        index = self.comboBox_selector_filter.currentIndex()
        selection = self.selection_types[index]

        input_ids = self.lineEdit_selection_id.text()
        self.selected_ids, error_data = self.mesh.check_selected_ids(
                                                                     input_ids, 
                                                                     selection = selection, 
                                                                     single_id = False
                                                                     )

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

    def plot_data_callback(self):

        if self.check_selected_ids():
            return

        if self.join_model_data():
            return

        self.plotter = FrequencyResponsePlotter(close_dialogs=True)
        self.plotter.comboBox_data_format.setCurrentIndex(DataFormat.REAL)
        self.plotter.data_format_changed_callback()
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def export_data_callback(self):
        
        if self.check_selected_ids():
            return

        if self.join_model_data():
            return

        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def get_response(self, index, selected_id):

        if index == 0:
            rows = self.mesh.get_nodes_from_surface(selected_id)
        elif index == 1:
            rows = self.mesh.get_nodes_from_line(selected_id)
        elif index == 2:
            rows = self.mesh.nodes_from_points.get(selected_id)
        else:
            rows = selected_id

        if isinstance(rows, int):
            response = self.nodal_solution[rows,:]
        else:
            response = np.average(self.nodal_solution[rows, :], axis=0)

        return response
    
    def get_fluid_property(self, fluid_property: str):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        if isinstance(self.selected_fluid, Fluid):
            if fluid_property == "pressure":
                return self.selected_fluid.pressure / 1e3
            elif fluid_property == "speed_of_sound":
                return self.selected_fluid.speed_of_sound

        return None

    def check_inputs(self, line_edit: QLineEdit, label, only_positive: bool = True):

        message = ""
        title = "Invalid value typed"
        input_str = line_edit.text()

        if input_str != "":

            input_str = input_str.replace(",", ".")

            try:
                out = float(input_str)
                
                if out <= 0 and only_positive:
                    message = f"Insert a positive value to the {label}."
                    message += "\n\nNote: zero value is not allowed."

            except Exception as _err:
                message = f"You have typed an invalid value at the {label} input field.\n\n"
                message += str(_err)

        else:
            message = f"Insert some value at the {label} input field."

        if message != "":
            line_edit.setFocus()
            PrintMessageInput([error_title, title, message])
            return None
        else:
            return out

    def join_model_data(self):
        
        index = self.comboBox_selector_filter.currentIndex()
        selection_type = self.selection_types[index]

        title = "Allowable pulsation levels on the process piping\n "
        title += "side of the inlet and discharge silencers"

        self.model_results.clear()
        for i, selected_id in enumerate(self.selected_ids):

            key = ("pressure", (selected_id))
            legend_label = f"Acoustic pressure at {selection_type} [{selected_id}]"

            acoustic_pressure = self.get_response(index, selected_id)
            time_vector, acoustic_pressure = process_ifft_from_one_sided_spectrum_signal(
                self.model.frequencies, 
                acoustic_pressure, 
                dc_included=False
                )

            self.model_results[key] = { 
                "x_data" : time_vector,
                "y_data" : acoustic_pressure / 1e3,
                "x_label" : "Time [s]",
                "y_label" : "Acoustic pressure",
                "title" : title,
                "data_information" : legend_label,
                "legend" : legend_label,
                "unit" : "kPa (a)",
                "color" : self.get_color(i),
                "linestyle" : "-" 
                }
        
        # create an auxiliar vector of ones values
        aux_ones = np.ones_like(time_vector, dtype=float)

        # absolute average line pressure P_AM in kPa(a)
        P_AM = self.get_fluid_property("pressure")
        if P_AM is None:
            return True

        # allowable pulsation levels as a percentage of absolute mean line pressure in kPa
        allowable_levels_percentual =  min(2, (28.6 / (P_AM**(1/3))))

        # allowable pulsation bounds 0-peak in kPa (a)
        pulsation_criteria_peak = (allowable_levels_percentual / 200) * P_AM * aux_ones

        # penalization factor for pre-study analysis
        penalization_factor = int(self.comboBox_penalization_factor.currentText())
        factor = penalization_factor / 100

        if penalization_factor:
            title += f" (penalized in {penalization_factor}%)"

        key = ("allowable pulsation limits (upper)", (None))
        legend_label_upper = "Allowable pulsation (upper bound)"

        self.model_results[key] = { 
            "x_data" : time_vector,
            "y_data" : factor * pulsation_criteria_peak,
            "x_label" : "Time [s]",
            "y_label" : "Acoustic pressure",
            "title" : title,
            "data_information" : legend_label_upper,
            "legend" : legend_label_upper,
            "unit" : "kPa (a)",
            "color" : [0.7, 0, 0],
            "linestyle" : "-",
            }

        key = ("allowable pulsation limits (lower)", (None))
        legend_label_lower = "Allowable pulsation (lower bound)"

        self.model_results[key] = { 
            "x_data" : time_vector,
            "y_data" : -factor * pulsation_criteria_peak,
            "x_label" : "Time [s]",
            "y_label" : "Acoustic pressure",
            "title" : title,
            "data_information" : legend_label_lower,
            "legend" : legend_label_lower,
            "unit" : "kPa (a)",
            "color" : [1, 0, 0],
            "linestyle" : "-"  
            }

    def get_color(self, index):

        colors = [  
            (0,0,1),
            (0,0,0),
            (0,1,1),
            (1,0,1),
            (1,1,0),
            (0.25,0.25,0.25),
            ]

        if index <= 5:
            return colors[index]
        else:
            return tuple(np.random.randint(0, 255, size=3) / 255)

    def get_fluid_callback(self):
        self.fluid_dialog = SetFluidInputsSimplified(update_workspace = False)
        self.fluid_dialog.fluid_widget.pushButton_apply.setVisible(False)
        self.fluid_dialog.fluid_widget.pushButton_apply_and_close.clicked.connect(self.get_selected_fluid)
        self.fluid_dialog.exec()

    def get_selected_fluid(self, selected_fluid: Fluid|None=None):

        if isinstance(self.fluid_dialog, QDialog):
            selected_fluid = self.fluid_dialog.get_selected_fluid()     
            self.fluid_dialog.close()
            self.fluid_dialog = None

        if isinstance(selected_fluid, Fluid):
            P_AM = selected_fluid.pressure / 1e3
            C_0 = selected_fluid.speed_of_sound

            self.lineEdit_selected_fluid.setText(selected_fluid.name)
            self.lineEdit_average_line_pressure.setText(f"{P_AM : .6f}")
            self.lineEdit_speed_of_sound.setText(f"{C_0 : .6f}")

        self.selected_fluid = selected_fluid

    def showEvent(self, event):
        super().showEvent(event)
        self.selection_filter_callback()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        return super().closeEvent(a0)