from enum import IntEnum
from time import perf_counter

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.engine.analysis_info import HarmonicAnalysisSetup
from vibra.interface.common.common_interface import update_entities_selection
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.numeric_checks.unit_utilities import convert_stress_unit
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.ui_generated.plots.structural.structural_stresses_frequency_response_inputs_ui import (
    StructuralStressesFrequencyResponseInputs_UI,
)


class SelectionType(IntEnum):
    SURFACES = 0
    LINES = 1
    POINTS = 2
    NODES = 3


class StructuralStressesFrequencyResponseInputs(StructuralStressesFrequencyResponseInputs_UI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self._config_window()
        self._initialize()
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
        return app().project.model.solution.structural_solution

    @property
    def nodal_averaged_stresses(self):
        t0 = perf_counter()
        nodal_averaged_stresses = self.structural_post.recover_nodal_averaged_structural_stresses()
        dt = perf_counter() - t0
        print(f"Time to compute all nodal stresses: {dt} s")
        return nodal_averaged_stresses

    @property
    def structural_post(self):
        return app().project.get_structural_postprocessing()

    @property
    def is_stress_data_cached(self):
        cache_info = self.structural_post.recover_nodal_averaged_structural_stresses.cache_info()
        return cache_info.currsize != 0

    def _initialize(self):
        self.selected_frequency_index = None

    def set_frames_disabled(self, disabled: bool):
        self.frame_selection_controls.setDisabled(disabled)
        self.frame_plot.setDisabled(disabled)
        self.pushButton_process_nodal_stresses.setEnabled(disabled)

    def showEvent(self, event):
        super().showEvent(event)
        self.selection_type_callback()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)

    def _initialize(self):
        self.plotter = None
        self.exporter = None
        self.model_results = {}
        self.selection_types = ["surfaces", "lines", "points", "nodes"]

        # update the widgets accessibility
        if self.is_stress_data_cached:
            self.process_stress_field()
        else:
            self.set_frames_disabled(True)

    def _create_connections(self):

        # QComboBox connection
        self.comboBox_selector_filter.currentIndexChanged.connect(self.selection_type_callback)
        self.comboBox_stress_units.currentIndexChanged.connect(self.process_units_data)

        # QPushButton connection
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        self.pushButton_process_nodal_stresses.clicked.connect(self.process_stress_field)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

    def selection_type_callback(self):
        if self.comboBox_selector_filter.currentIndex() == SelectionType.NODES:
            app().main_window.show_mesh_render_widget()
        else:
            app().main_window.show_geometry_render_widget()

    def geometry_selection_callback(self):

        faces = app().main_window.selection.geometry_surfaces
        lines = app().main_window.selection.geometry_lines
        points = app().main_window.selection.geometry_points
        nodes = app().main_window.selection.mesh_nodes

        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_selector_filter.setCurrentIndex(0)

        elif lines:
            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_selector_filter.setCurrentIndex(1)

        elif points:
            text = ", ".join([str(i) for i in points])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_selector_filter.setCurrentIndex(2)

        elif nodes:
            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_selector_filter.setCurrentIndex(3)

    def _load_analysis_setup_and_solution(self):
        analysis_setup = self.model.analysis_setup

        self.analysis_method = ""
        if isinstance(analysis_setup, HarmonicAnalysisSetup):
            analysis_method = analysis_setup.analysis_method.capitalize().replace("_", " ")
            self.analysis_method = f"{analysis_method} method"

        self.frequencies = self.model.frequencies

    def process_stress_field(self):

        # recover the averaged structural stresses
        if not self.is_stress_data_cached:
            def recover_stresses():
                t0 = perf_counter()
                self.structural_post.recover_nodal_averaged_structural_stresses()
                dt = perf_counter() - t0
                print(f"Time to compute all nodal stresses: {dt} s")

            LoadingWindow(recover_stresses).run()

        self.set_frames_disabled(False)

    def check_inputs(self):

        index = self.comboBox_selector_filter.currentIndex()
        selection = self.selection_types[index]

        input_ids = self.lineEdit_selection_id.text()
        self.selected_ids, error_data = self.model.check_selected_ids(  
            input_ids,
            selection,
            domain="structural",
        )

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        update_entities_selection(self.lineEdit_selection_id, selection, self.selected_ids)
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

        return False

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

    def get_response(self, selection_type: str, selected_id: int, stress_type_index: int):

        surface_ids = []

        if selection_type == "surface":
            surface_ids = [selected_id]
            nodes = self.mesh.get_nodes_from_surface(selected_id)

        elif selection_type == "line":           
            surface_ids = self.mesh.surfaces_from_line[selected_id]
            nodes = self.mesh.get_nodes_from_line(selected_id)

        elif selection_type == "point":
            node_id = selected_id - 1
            nodes = np.array([node_id], dtype=int)

        else:
            nodes = np.array([selected_id], dtype=int)
        
        if selection_type in ["point", "node"]:   
            mask = np.sum(np.isin(self.mesh.faces_connectivity[:, 4:], nodes), axis=1) == 1
            surface_ids = [int(surf_id) for surf_id in np.unique(self.mesh.faces_connectivity[:, 1][mask])]

        for surf_id in surface_ids:

            surf_data = self.properties._get_property("surface_thickness", surface=surf_id)
            if isinstance(surf_data, dict):
                if self.model.structural_element_2d is None:
                    self.model.set_structural_elements()

            else:
                if self.model.structural_element_3d is None:
                    self.model.set_structural_elements()

        # process the structural dofs of the selected entities
        _node_ids = self.model.get_mapped_nodes(nodes, "structural")

        if isinstance(_node_ids, int):
            response = self.nodal_averaged_stresses[_node_ids, stress_type_index, :]
        else:
            response = np.average(self.nodal_averaged_stresses[_node_ids, stress_type_index, :], axis=0)

        return response

    def join_model_data(self):

        self.model_results.clear()
        stress_index = self.comboBox_structural_stresses.currentIndex()

        index = self.comboBox_selector_filter.currentIndex()
        selection_type = self.selection_types[index][:-1]

        self.process_units_data()

        self.y_label = self.get_ylabel()
        self.title = f"Structural frequency response - {self.analysis_method}"

        for i, selected_id in enumerate(self.selected_ids):

            key = (selection_type, (selected_id))
            legend_label = f"{self.y_label} at {selection_type} [{selected_id}]"
            y_data = self.get_response(selection_type, selected_id, stress_index)

            self.model_results[key] = {
                "x_data": self.frequencies,
                "y_data": self.unit_factor * y_data,
                "x_label": "Frequency [Hz]",
                "y_label": self.y_label,
                "title": self.title,
                "data_type": self.y_label,
                "legend": legend_label,
                "unit": self.stress_units,
                "color": get_color(i),
                "linestyle": "-",
            }

    def process_units_data(self) -> str:
        self.stress_units = self.comboBox_stress_units.currentText()
        self.unit_factor = convert_stress_unit(1, "Pa", self.stress_units)

    def get_ylabel(self) -> str:

        # stress index
        index = self.comboBox_structural_stresses.currentIndex()

        # stress subscript
        subscript = ["x", "y", "z", "xy", "xz", "yz"]

        # stress Greek letter
        stress_letter = "\u03c3" if index < 3 else "\u03c4"

        # stress label
        stress_label = f"${stress_letter}" + r"_{" + subscript[index] + r"}$"

        if index >= 3:
            return f"Shear stress {stress_label}"

        return f"Normal stress {stress_label}"

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
        (1,0,0),
        (0,1,1), 
        (1,0,1), 
        (1,1,0),
        (0.25,0.25,0.25),
        ]

    if index <= 6:
        return colors[index]

    return tuple(np.random.randint(0, 255, size=3) / 255)
