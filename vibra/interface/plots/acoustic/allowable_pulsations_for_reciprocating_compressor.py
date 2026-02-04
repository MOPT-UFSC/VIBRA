from PySide6.QtWidgets import QDialog, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra.engine import AnalysisID
from vibra import app
from vibra.engine.properties.fluid import Fluid

from vibra.interface.ui_generated.plots.acoustic.allowable_pulsations_for_reciprocating_compressor_inputs_ui import AllowablePulsationsForReciprocatingCompressorInputs_UI
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.model_inputs.general.fluid.simplified_fluid_inputs import SimplifiedFluidInputs

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class AllowablePulsationsForReciprocatingCompressorInputs(AllowablePulsationsForReciprocatingCompressorInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self.mesh = app().new_project.model.mesh
        self.properties = app().new_project.model.properties

        self._reset_variables()
        self._create_connections()

        self._load_analysis_setup_and_solution()
        self.geometry_selection_callback()

    def _load_analysis_setup_and_solution(self):
        self.analysis_method = ""
        if app().new_project.current_analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.analysis_method = "Direct method"

        self.frequencies = app().new_project.model.frequencies
        self.solution = app().new_project.solver.solution

    def _reset_variables(self):

        self.plotter = None
        self.exporter = None
        self.fluid_dialog = None
        self.selected_fluid = None

        self.unit_label = "Pa"
        self.selection_types = ["surfaces", "lines", "points", "nodes"]

    def _create_connections(self):
        #
        self.comboBox_selector_filter.currentIndexChanged.connect(self.selection_filter_callback)
        #
        self.lineEdit_pressure_ratio.textChanged.connect(self.process_unfiltered_criteria)
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

            if self.tabWidget_main.currentIndex() == 1:
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

    def process_unfiltered_criteria(self):

        str_pressure_ratio = self.lineEdit_pressure_ratio.text()
        if str_pressure_ratio == "":
            return

        try:
            pressure_ratio = float(str_pressure_ratio)     
            unfiltered_criteria = min(3*pressure_ratio, 7)

        except:
            self.lineEdit_unfiltered_criteria.setFocus()
            self.lineEdit_unfiltered_criteria.selectAll()
            return

        self.lineEdit_unfiltered_criteria.setText(f"{unfiltered_criteria : .6f}")

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
            rows = app().new_project.model.mesh.get_nodes_from_surface(selected_id)
        elif index == 1:
            rows = app().new_project.model.mesh.get_nodes_from_line(selected_id)
        elif index == 2:
            rows = app().new_project.model.mesh.nodes_from_points.get(selected_id)
        else:
            rows = selected_id

        if isinstance(rows, int):
            response = self.solution[rows,:]
        else:
            response = np.average(self.solution[rows,:], axis=0)

        if complex(0) in response:
            response += 1e-12
        #     response += np.ones(len(response), dtype=float)*(1e-12)

        return response
    
    def get_fluid_property(self, fluid_property: str):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        if isinstance(self.selected_fluid, Fluid):
            if fluid_property == "pressure":
                return self.selected_fluid.pressure / 1e5
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
                message = f"You have typed and invalid value at the {label} input field.\n\n"
                message += str(_err)

        else:
            message = f"Insert some value at the {label} input field."

        if message != "":
            line_edit.setFocus()
            PrintMessageInput([window_title_1, title, message])
            return None
        else:
            return out

    def join_model_data(self):
        
        # absolute average line pressure P_L in bar(a) and speed of sound C_0 in m/s
        P_L = self.get_fluid_property("pressure")
        if P_L is None:
            return True

        # define the frequency vector for filtered pulsation criteria

        df = 0.5
        f_max = self.frequencies[-1]
        freq = np.arange(df, f_max + df, df)

        index = self.comboBox_selector_filter.currentIndex()
        selection_type = self.selection_types[index]

        if self.tabWidget_main.currentIndex() == 0:
            title = "Maximum Allowable Pressure Pulsation at Compressor \nCylinder Flanges"  
        else:
            title = "Allowable Pulsation Levels at and Beyond Line-side \nConnections of Pulsation Suppression Devices"

        self.model_results = dict()
        for i, selected_id in enumerate(self.selected_ids):

            key = ("pressure_ratio", (selected_id))
            legend_label = f"Acoustic pressure at {selection_type} [{selected_id}]"

            acoustic_pressure = self.get_response(index, selected_id)

            # express the absolute pressure in bar units and in peak-to-peak scale
            pulsation_pp = 100 * (2 * acoustic_pressure / 1e5) / P_L

            self.model_results[key] = { 
                                       "x_data" : self.frequencies,
                                       "y_data" : pulsation_pp * (P_L / 100),
                                       "x_label" : "Frequency [Hz]",
                                       "y_label" : "Pressure ratio",
                                       "title" : title,
                                       "data_information" : legend_label,
                                       "legend" : legend_label,
                                       "unit" : "bar (a) (peak-to-peak)",
                                       "color" : self.get_color(i),
                                       "linestyle" : "-" 
                                       }

        factor = 1.0

        if self.tabWidget_main.currentIndex() == 0:

            # inside diameter in millimeters
            pressure_ratio = self.check_inputs(self.lineEdit_pressure_ratio, "Pressure ratio")
            if pressure_ratio is None:
                return True

            # allowable peak-to-peak pulsation levels in bar(a) at cylinder flanges

            pulsation_criteria = min(3*pressure_ratio, 7)
            pulsation_criteria *= np.ones_like(freq, dtype=float)

            key = ("unfiltered_criteria", (None))
            legend_label = "Pulsation criteria"

        else:

            # speed of sound C_0 in m/s
            C_0 = self.get_fluid_property("speed_of_sound")
            if C_0 is None:
                return True

            # inside diameter in millimeters
            inside_diameter = self.check_inputs(self.lineEdit_inside_diameter, "Inside diameter")
            if inside_diameter is None:
                return True

            # allowable peak-to-peak pulsation levels in bar(a) as percentage of the average mean line pressure
            pulsation_criteria = 400 * ((C_0 / (350 * P_L * inside_diameter * freq))**(1/2))

            if self.checkBox_pre_study_analysis.isChecked():
                factor = 0.7

            key = ("filtered_criteria", (None))
            legend_label = "Pulsation criteria"

        self.model_results[key] = { 
                                   "x_data" : freq,
                                   "y_data" : factor * pulsation_criteria * (P_L / 100),
                                   "x_label" : "Frequency [Hz]",
                                   "y_label" : "Acoustic pressure",
                                   "title" : title,
                                   "data_information" : legend_label,
                                   "legend" : legend_label,
                                   "unit" : "bar (a) (peak-to-peak)",
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
        self.fluid_dialog = SimplifiedFluidInputs(update_workspace = False)
        self.fluid_dialog.fluid_widget.pushButton_attribute.setText("Select fluid")
        self.fluid_dialog.pushButton_attribute.clicked.connect(self.get_selected_fluid)
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
