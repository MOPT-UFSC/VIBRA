import logging

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface import error_title
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.plots.general.frequency_response_plotter import (
    FrequencyResponsePlotter,
)
from vibra.interface.ui_generated.plots.acoustic.acoustic_impedance_inputs_ui import (
    AcousticImpedanceInputs_UI,
)


class AcousticImpedanceInputs(AcousticImpedanceInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self._config_window()
        self._reset_variables()
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
    def acoustic_post(self):
        return app().project.get_acoustic_postprocessing()

    def _load_analysis_setup_and_solution(self):
        self.analysis_method = ""
        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.analysis_method = "Direct method"

        self.frequencies = app().project.model.frequencies

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _reset_variables(self):
        self.keep_window_open = True
        self.exporter = None
        self.plotter = None

    def _create_connections(self):
        #
        self.comboBox_selector_filter.currentIndexChanged.connect(self.update_render_according_to_selector)
        self.comboBox_volumes.currentIndexChanged.connect(self.volume_selector_callback)
        self.comboBox_nodal_normals.currentIndexChanged.connect(self.toggle_nodal_normals_symbols_visibility)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.geometry_selection_callback()

    def update_render_according_to_selector(self):
        self.geometry_selection_callback()
        if self.comboBox_selector_filter.currentIndex() == 0:
            app().main_window.show_geometry_render_widget()           
        else:
            app().main_window.show_mesh_render_widget()

    def volume_selector_callback(self):
        if self.comboBox_volumes.currentText() != "":
            volume_id = int(self.comboBox_volumes.currentText())
            app().main_window.selection.set_geometry_selection(volumes=[volume_id])

    def toggle_nodal_normals_symbols_visibility(self):
        show_normals = (self.comboBox_nodal_normals.currentText() == "Show")
        app().main_window.results_widget.visualization_filter.normal_symbols = show_normals
        app().main_window.update_symbols()

    def geometry_selection_callback(self):

        if not app().main_window.action_results_workspace.isChecked():
            return

        volumes = app().main_window.selection.geometry_volumes
        surfaces = app().main_window.selection.geometry_surfaces
        nodes = app().main_window.selection.mesh_nodes

        if volumes:
            if len(volumes) == 1:
                try:
                    self.comboBox_volumes.setCurrentText(f"{list(volumes)[0]}")
                except Exception:
                    pass
            return

        if not (surfaces or nodes):
            return

        index = self.comboBox_selector_filter.currentIndex()
        if surfaces and index == 0:
            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)
            
            self.check_volumes_from_surfaces(surfaces)

        elif nodes and index == 1:
            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)

            self.check_volumes_from_nodes(nodes)

    def check_volumes_from_nodes(self, node_ids: list[int]):

        surfaces_from_nodes = set()
        for node_id in node_ids:
            surface_ids = self.mesh.get_surfaces_from_node(node_id)
            surfaces_from_nodes |= set(surface_ids)

        self.check_volumes_from_surfaces(list(surfaces_from_nodes))

    def check_volumes_from_surfaces(self, surface_ids: list[int]):

        external_surfaces_map = dict()
        internal_surfaces_map = dict()  
        self.comboBox_volumes.blockSignals(True) 

        for surface_id in surface_ids:
            volumes_from_surface = self.mesh.volumes_from_surface.get(surface_id, list())
            if len(volumes_from_surface) == 1:
                external_surfaces_map[surface_id] = volumes_from_surface[0]

            elif len(volumes_from_surface) == 2:
                internal_surfaces_map[surface_id] = volumes_from_surface

        self.comboBox_volumes.clear()
        if external_surfaces_map and internal_surfaces_map:
            self.lineEdit_selection_id.setText("")
            app().main_window.selection.set_geometry_selection()
            app().processEvents()

            title = "Invalid selection"
            message = "The current selection contains internal and external surfaces. "
            message += "The selection of multiple external surfaces is allowed, but"
            message += "only one internal surface can be selected each time."
            PrintMessageInput([error_title, title, message])
            self.comboBox_volumes.blockSignals(False)
            return

        if external_surfaces_map:
            volumes_set = set()
            self.comboBox_volumes.setEnabled(False)
            for volume_id in external_surfaces_map.values():
                volumes_set |= set([volume_id])

            if len(volumes_set) == 1:
                self.comboBox_volumes.addItem(str(volume_id))
            elif len(volumes_set) > 1:
                self.comboBox_volumes.addItem("Multiple")

        if internal_surfaces_map:
            self.comboBox_volumes.setEnabled(True)
            for volume_ids in internal_surfaces_map.values():
                for volume_id in volume_ids:
                    self.comboBox_volumes.addItem(str(volume_id))

        self.comboBox_volumes.blockSignals(False)

    def check_inputs(self):

        input_ids = self.lineEdit_selection_id.text()
        selection_type = self.comboBox_selector_filter.currentText().lower()

        self.selected_ids, error_data = self.mesh.check_selected_ids(
                                                                     input_ids, 
                                                                     selection = selection_type
                                                                     )

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

    def plot_data_callback(self):

        self.mesh.nodal_normals_data.clear()

        if self.check_inputs():
            return

        self.join_model_data()

        show_normals = (self.comboBox_nodal_normals.currentText() == "Show")
        app().main_window.results_widget.visualization_filter.normal_symbols = show_normals
        if show_normals:
            app().main_window.update_symbols()

        self.plotter = FrequencyResponsePlotter(close_dialogs=True)
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def export_data_callback(self):
        
        if self.check_inputs():
            return

        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def get_response(self, selection_type: str, selected_id: int):

        if self.comboBox_volumes.currentText() == "Multiple":
            if selection_type == "surfaces":
                volume_id = self.mesh.volumes_from_surface.get(selected_id)[0]
            else:
                surfaces_from_node = self.mesh.get_surfaces_from_node(selected_id)
                volume_id = self.mesh.volumes_from_surface.get(surfaces_from_node[0])[0]
        else:
            volume_id = int(self.comboBox_volumes.currentText())
       
        def function_callback():

            if selection_type == "surfaces":
                acoustic_impedance = self.acoustic_post.compute_acoustic_impedance(
                    surface_id = selected_id,
                    volume_id = volume_id,
                    )

            else:
                acoustic_impedance = self.acoustic_post.compute_acoustic_impedance(
                    node_id = selected_id,
                    volume_id = volume_id,
                    )

            if self.comboBox_normalized_impedance.currentText() == "Enabled":

                if app().project.assembler.fluid_properties_from_volume:
                    prop_data: dict = app().project.assembler.fluid_properties_from_volume.get(volume_id)
                    rho_f = prop_data.get("rho_f")
                    C_f = prop_data.get("C_f")

                else:
                    rho_f, C_f = self.model.get_fluid_properties_from_volume(volume_id)

                Z0_f = rho_f * C_f
                acoustic_impedance /= Z0_f

            logging.info("Processing particle velocity... [95/100]")

            return acoustic_impedance

        return LoadingWindow(function_callback).run()

    def join_model_data(self):

        selection_type = self.comboBox_selector_filter.currentText().lower()

        self.model_results = dict()

        if self.comboBox_normalized_impedance.currentText() == "Enabled":
            plot_type = "Normalized acoustic impedance"
            unit_label = "--"
        else:
            plot_type = "Specific acoustic impedance"
            unit_label = "Pa/m/s"

        for i, selected_id in enumerate(self.selected_ids):

            key = (selection_type, (selected_id))
            legend_label = f"{plot_type} at {selection_type} [{selected_id}]"

            self.model_results[key] = { 
                                        "x_data" : self.frequencies,
                                        "y_data" : self.get_response(selection_type, selected_id),
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : plot_type,
                                        "title" : plot_type,
                                        "data_type" : plot_type.lower(),
                                        "legend" : legend_label,
                                        "unit" : unit_label,
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

        self.keep_window_open = False
        return super().closeEvent(a0)