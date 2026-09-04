from enum import IntEnum

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
from vibra.interface.numeric_checks.unit_utilities import convert_pressure_unit
from vibra.interface.plots.general.frequency_response_plotter import DataFormat, FrequencyResponsePlotter
from vibra.interface.ui_generated.plots.acoustic.allowable_pulsations_for_reciprocating_compressor_inputs_ui import (
    AllowablePulsationsForReciprocatingCompressorInputs_UI,
)
from vibra.utils.signal_processing import process_ifft_from_one_sided_spectrum_signal


class SelectionType(IntEnum):
    SURFACES = 0
    LINES = 1
    POINTS = 2
    NODES = 3


class PulsationCriteria(IntEnum):
    UNFILTERED = 0
    FILTERED = 1


class AllowablePulsationsForReciprocatingCompressorInputs(AllowablePulsationsForReciprocatingCompressorInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self._reset_variables()
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
        return app().project.model.solution.acoustic_solution

    def _load_analysis_setup_and_solution(self):
        self.analysis_method = ""
        if self.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.analysis_method = "Direct method"

        self.frequencies = self.model.frequencies

    def _reset_variables(self):

        self.plotter = None
        self.exporter = None
        self.fluid_dialog = None
        self.selected_fluid = None

        self.model_results = dict()

        self.unit_label = "Pa"
        self.selection_types = ["surfaces", "lines", "points", "nodes"]

    def _create_connections(self):
        #
        self.comboBox_selector_filter.currentIndexChanged.connect(self.selection_filter_callback)
        #
        self.lineEdit_pressure_ratio.textChanged.connect(self.process_unfiltered_criterion)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        self.pushButton_get_internal_diameter_from_selection.clicked.connect(self.get_internal_diameter_from_selection)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
    
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

        if len(surfaces) == 1:
            surface_id = list(surfaces)[0]

            volumes_from_surface = self.mesh.volumes_from_surface.get(surface_id)
            if len(volumes_from_surface) == 1:
                selected_fluid = self.properties._get_property("fluid", volume=volumes_from_surface[0])
                self.get_selected_fluid(selected_fluid=selected_fluid)

            elif len(volumes_from_surface) == 2:
                fluid_A = self.properties._get_property("fluid", volume=volumes_from_surface[0])
                fluid_B = self.properties._get_property("fluid", volume=volumes_from_surface[1])
                if fluid_A == fluid_B:
                    self.get_selected_fluid(selected_fluid=fluid_A)

            if self.tabWidget_main.currentIndex() == PulsationCriteria.FILTERED:
                return

            data = self.properties._get_property("reciprocating_compressor_excitation", surface=surface_id)
            if data is None:
                return

            if isinstance(data, dict):
                parameters = data.get("parameters")
                if parameters is None:
                    return

            if isinstance(parameters, dict):
                pressure_ratio = parameters.get("pressure_ratio")
                self.lineEdit_pressure_ratio.setText(f"{pressure_ratio : .6f}")

    def process_unfiltered_criterion(self):

        str_pressure_ratio = self.lineEdit_pressure_ratio.text()
        if str_pressure_ratio == "":
            return

        try:
            pressure_ratio = float(str_pressure_ratio)     
            unfiltered_criterion = min(3*pressure_ratio, 7)

        except Exception:
            self.lineEdit_unfiltered_criterion.setFocus()
            self.lineEdit_unfiltered_criterion.selectAll()
            return

        self.lineEdit_unfiltered_criterion.setText(f"{unfiltered_criterion : .6f}")

    def selection_filter_callback(self):

        self.geometry_selection_callback()
        if self.comboBox_selector_filter.currentIndex() == SelectionType.NODES:
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

        if self.tabWidget_main.currentIndex() == PulsationCriteria.UNFILTERED:
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

    def get_response(self, index: int, selected_id: int | list[int]):

        if index == SelectionType.SURFACES:
            nodes = self.mesh.get_nodes_from_surface(selected_id)
        elif index == SelectionType.LINES:
            nodes = self.mesh.get_nodes_from_line(selected_id)
        elif index == SelectionType.POINTS:
            nodes = self.mesh.nodes_from_points.get(selected_id)
        else:
            nodes = selected_id

        # map structural dofs
        _nodes = self.model.fluid_node_mapping[nodes]
        dof_per_node = self.model.acoustic_element_3d.dof_per_node

        gdof = dof_per_node * _nodes.reshape(-1, 1) + np.arange(dof_per_node, dtype=int)
        rows = gdof[:, 0]

        if isinstance(rows, int):
            response = self.nodal_solution[rows,:]
        else:
            response = np.average(self.nodal_solution[rows,:], axis=0)

        if complex(0) in response:
            response += 1e-12
        #     response += np.ones(len(response), dtype=float)*(1e-12)

        return response
    
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

        self.model_results.clear()

        index = self.comboBox_selector_filter.currentIndex()
        selection_type = self.selection_types[index]

        if self.tabWidget_main.currentIndex() == PulsationCriteria.UNFILTERED:
            title = "Maximum Allowable Pressure Pulsation at Compressor \nCylinder Flanges"  
        else:
            title = "Allowable Pulsation Levels at and Beyond Line-side \nConnections of Pulsation Suppression Devices"

        filtered_criterion = self.tabWidget_main.currentIndex() == PulsationCriteria.FILTERED

        if not isinstance(self.selected_fluid, Fluid):
            self.get_fluid_callback()
            return True

        # absolute average line fluid pressure in bar (a)
        P_L = convert_pressure_unit(self.selected_fluid.pressure, "Pa (a)", "bar (a)")

        # speed of sound C_0 in m/s
        C_0 = self.selected_fluid.speed_of_sound

        if filtered_criterion:

            for i, selected_id in enumerate(self.selected_ids):

                key = ("acoustic_pressure", (selected_id))
                legend_label = f"Acoustic pressure at {selection_type} [{selected_id}]"

                acoustic_pressure_pp = 2 * self.get_response(index, selected_id)

                # express the absolute pressure in bar units and in peak-to-peak scale
                acoustic_pressure_pp_conv = convert_pressure_unit(acoustic_pressure_pp, "Pa (a)", "bar (a)")

                self.model_results[key] = {
                    "x_data": self.frequencies,
                    "y_data": acoustic_pressure_pp_conv,
                    "x_label": "Frequency [Hz]",
                    "y_label": "Pressure ratio",
                    "title": title,
                    "data_information": legend_label,
                    "legend": legend_label,
                    "unit": "bar (a) (peak-to-peak)",
                    "color": get_color(i),
                    "linestyle": "-",
                }

            # inside diameter in millimeters
            inside_diameter = self.check_inputs(self.lineEdit_inside_diameter, "Inside diameter")
            if inside_diameter is None:
                return True

            # define the frequency vector for filtered pulsation criteria
            df = 0.5
            f_max = self.frequencies[-1]
            freq = np.arange(df, f_max + df, df)

            # allowable peak-to-peak pulsation levels in bar(a) as percentage of the average mean line pressure
            P_1 = 400 * ((C_0 / (350 * P_L * inside_diameter * freq))**(1/2))

            factor = 0.7 if self.checkBox_prestudy_analysis.isChecked() else 1.0

            key = ("filtered_criterion", (None))
            legend_label = "Pulsation criteria"

            self.model_results[key] = {
                "x_data": freq,
                "y_data": factor * P_1 * (P_L / 100),
                "x_label": "Frequency [Hz]",
                "y_label": "Acoustic pressure",
                "title": title,
                "data_information": legend_label,
                "legend": legend_label,
                "unit": "bar (a) (peak-to-peak)",
                "color": [1, 0, 0],
                "linestyle": "-",
            }

        else:

            if len(self.selected_ids) != 1:
                title = "Invalid selection"
                message = "Select the surface where the compressor excitation has been "
                message += "applied to process the pulsation criterion properly. "
                message += "This pulsation criterion should be evaluated in surfaces near "
                message += "the compressor cylinder flange."
                PrintMessageInput([error_title, title, message])
                return True

            selected_id = self.selected_ids[0]
            acoustic_pressure = self.get_response(index, selected_id)

            time_vector, acoustic_pressure = process_ifft_from_one_sided_spectrum_signal(
                self.model.frequencies, 
                acoustic_pressure, 
                dc_included=False
                )
            
            y_axis_label = "bar (a)"
            acoustic_pressure_conv = convert_pressure_unit(acoustic_pressure, "Pa (a)", "bar (a)")

            key = ("pressure", (selected_id))
            legend_label = f"Acoustic pressure at {selection_type} [{selected_id}]"

            self.model_results[key] = { 
                "x_data" : time_vector,
                "y_data" : acoustic_pressure_conv,
                "x_label" : "Time [s]",
                "y_label" : "Acoustic pressure",
                "title" : title,
                "data_information" : legend_label,
                "legend" : legend_label,
                "unit" : y_axis_label,
                "color" : [0, 0, 1],
                "linestyle" : "-" 
                }

            # inside diameter in millimeters
            pressure_ratio = self.check_inputs(self.lineEdit_pressure_ratio, "Pressure ratio")
            if pressure_ratio is None:
                return True

            # allowable peak-to-peak pulsation levels in bar(a) at cylinder flanges
            P_cf = min(3 * pressure_ratio, 7) / 100

            key = ("allowable pulsation limits (upper)", (None))
            legend_label_upper = "Allowable pulsation (upper bound)"
            
            if not isinstance(self.selected_fluid, Fluid):
                return True

            # mean line fluid pressure in Pa (a)
            P_L = convert_pressure_unit(self.selected_fluid.pressure, "Pa (a)", "bar (a)")

            # pulsation recommended limits in bar (a)
            pulsation_criterion_peak = P_cf * (P_L / 2)

            self.model_results[key] = { 
                "x_data" : time_vector,
                "y_data" : pulsation_criterion_peak,
                "x_label" : "Time [s]",
                "y_label" : "Acoustic pressure",
                "title" : title,
                "data_information" : legend_label_upper,
                "legend" : legend_label_upper,
                "unit" : y_axis_label,
                "color" : [0.7, 0, 0],
                "linestyle" : "-",
                }

            key = ("allowable pulsation limits (lower)", (None))
            legend_label_lower = "Allowable pulsation (lower bound)"

            self.model_results[key] = { 
                "x_data" : time_vector,
                "y_data" : -pulsation_criterion_peak,
                "x_label" : "Time [s]",
                "y_label" : "Acoustic pressure",
                "title" : title,
                "data_information" : legend_label_lower,
                "legend" : legend_label_lower,
                "unit" : y_axis_label,
                "color" : [1, 0, 0],
                "linestyle" : "-"  
                }

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
            P_L = selected_fluid.pressure / 1e5
            C_0 = selected_fluid.speed_of_sound

            self.lineEdit_selected_fluid.setText(selected_fluid.name)
            self.lineEdit_average_line_pressure.setText(f"{P_L : .6f}")
            self.lineEdit_speed_of_sound.setText(f"{C_0 : .6f}")

        self.selected_fluid = selected_fluid

    def get_internal_diameter_from_selection(self):

        if self.lineEdit_selection_id.text() == "":
            return

        if self.check_selected_ids():
            return

        area = self.mesh.area_from_surfaces.get(self.selected_ids[0])
        diameter = np.sqrt(4 * area / np.pi) * 1000

        self.lineEdit_inside_diameter.setText(f"{diameter : .4f}")

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

def get_color(index: int):

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
