import logging
from time import time

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.plots.general.frequency_response_plotter import DataFormat, FrequencyResponsePlotter
from vibra.interface.ui_generated.plots.acoustic.acoustic_pressure_waveform_2d_plot_inputs_ui import AcousticPressureWaveform2dPlotInputs_UI
from vibra.utils.signal_processing import process_ifft_from_one_sided_spectrum_signal, process_multiple_iffts_from_one_sided_spectrum_signals


class AcousticPressureWaveform2DPlotInputs(AcousticPressureWaveform2dPlotInputs_UI):
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
        return app().project.model.solution.nodal_solution

    def showEvent(self, event):
        super().showEvent(event)
        self.update_render_according_to_selector()

    def _load_analysis_setup_and_solution(self):
        self.analysis_method = ""
        if self.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.analysis_method = "Direct method"

        self.frequencies = self.model.frequencies

    def _reset_variables(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "Pa"
        self.selection_types = ["surfaces", "lines", "points", "nodes"]

    def _create_connections(self):
        #
        self.comboBox_selector_filter.currentIndexChanged.connect(self.update_render_according_to_selector)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
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

        elif not any([nodes, points, lines, surfaces]):
            self.lineEdit_selection_id.setText("")

    def update_render_according_to_selector(self):

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

        self.join_model_data()
        self.plotter = FrequencyResponsePlotter(close_dialogs=True)
        self.plotter.comboBox_data_format.setCurrentIndex(DataFormat.REAL)
        self.plotter.data_format_changed_callback()
        self.plotter.frame_hlines_main.setDisabled(True)
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def export_data_callback(self):
        
        if self.check_selected_ids():
            return

        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def get_response(self, selected_id: int):

        index = self.comboBox_selector_filter.currentIndex()

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
            response = np.average(self.nodal_solution[rows,:], axis=0)

        if complex(0) in response:
            response += 1e-12
        #     response += np.ones(len(response), dtype=float)*(1e-12)

        return response

    def compute_multiple_ifft(self):

        logging.info("Computing multiple iffts... [10/100]")
        solution = self.nodal_solution[:, :]

        t0 = time()
        logging.info("Computing multiple iffts... [25/100]")
        _time_vector, acoustic_pressure_waveform_vectors = process_multiple_iffts_from_one_sided_spectrum_signals(                
            self.frequencies, 
            solution,
            dc_included = False,
            )

        dt = time() - t0
        print(f"Elapsed time to process ifft: {dt : .6f} s")
        ##

    def join_model_data(self):

        current_text = self.comboBox_selector_filter.currentText()
        selection_type = current_text.lower()[:-1]

        self.model_results = dict()
        self.title = "Acoustic pressure waveform"

        ## TODO: only for tests
        # LoadingWindow(self.compute_multiple_ifft).run()

        for i, selected_id in enumerate(self.selected_ids):

            key = (selection_type, (selected_id))
            legend_label = f"Acoustic pressure at {selection_type} [{selected_id}]"

            Xf = self.get_response(selected_id)
            time_vector, acoustic_pressure = process_ifft_from_one_sided_spectrum_signal(
                self.frequencies, 
                Xf,
                dc_included = False,
                )

            self.model_results[key] = { 
                "x_data" : time_vector,
                "y_data" : acoustic_pressure,
                "x_label" : "Time [s]",
                "y_label" : "Acoustic pressure",
                "title" : self.title,
                "data_type" : "acoustic pressure",
                "legend" : legend_label,
                "unit" : self.unit_label,
                "color" : self.get_color(i),
                "linestyle" : "-"  
            }

    def get_color(self, index):

        colors = [  
                  (0,0,1), 
                  (0,0,0), 
                  (1,0,0),
                  (0,1,1), 
                  (1,0,1), 
                  (1,1,0),
                  (0.25,0.25,0.25)
                  ]

        if index <= 6:
            return colors[index]
        else:
            return tuple(np.random.randint(0, 255, size=3) / 255)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        return super().closeEvent(a0)
