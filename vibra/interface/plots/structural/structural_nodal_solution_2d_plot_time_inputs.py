from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.common.common_interface import update_entities_selection
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.numeric_checks.int_list_validator import IntListValidator
from vibra.interface.numeric_checks.unit_utilities import convert_angle_unit, convert_length_unit
from vibra.interface.plots.general.frequency_response_plotter import DataFormat, FrequencyResponsePlotter
from vibra.interface.ui_generated.plots.structural.structural_nodal_solution_2d_plot_time_inputs_ui import StructuralNodalSolution2dPlotTimeInputs_UI
from vibra.utils.signal_processing import process_ifft_from_one_sided_spectrum_signal


class SelectionType(IntEnum):
    SURFACES = 0
    LINES = 1
    POINTS = 2
    NODES = 3


class StructuralNodalSolution2dPlotTimeInputs(StructuralNodalSolution2dPlotTimeInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self._initialize()
        self._configure_validator()
        self._create_connections()
        self.update_render_according_to_selector()

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
    def frequencies(self):
        return app().project.model.frequencies

    @property
    def nodal_solution(self):
        return app().project.model.solution.structural_solution

    def _initialize(self):
        self.exporter = None
        self.plotter = None
        self.model_results = {}
        self.selection_types = [
            "surfaces",
            "lines",
            "points",
            "nodes",
            ]

    def _configure_validator(self):
        validator = IntListValidator()
        self.lineEdit_selection_id.setValidator(validator)

    def _create_connections(self):

        # QComboBox connection
        self.comboBox_selector_filter.currentIndexChanged.connect(self.update_render_according_to_selector)
        self.comboBox_structural_results.currentIndexChanged.connect(self.update_units_combo_box_items)

        # QPushButton conenctions
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        self.update_combo_box_items_callback()

    def update_combo_box_items_callback(self):

        self.comboBox_structural_results.clear()

        def dof_label(dof_index: str, n_int: int):
            dof_type = "U" if dof_index < 3 else "\u03b8"
            directions = ["x", "y", "z", "x", "y", "z"]
            data_types = ["{}{}", "d{}{}/dt", "d²{}{}/dt²"]
            # data_types = ["{}<sub>{}</sub>", "d{}<sub>{}</sub>/dt", "d²{}<sub>{}</sub>/dt²"]
            return data_types[n_int].format(dof_type, directions[dof_index])

        volume_exists = self.mesh.are_there_volumes_in_geometry()
        n_dofs = 3 if volume_exists else 6

        for j, results_label in enumerate(["Displacement", "Velocity", "Acceleration"]):
            for dof_index in range(n_dofs):
                _dof_label = dof_label(dof_index, j)
                # self.comboBox_structural_results.setItemText(dof_index, f"{_dof_label}")
                self.comboBox_structural_results.addItem(f"{results_label} {_dof_label}")

    def update_units_combo_box_items(self):

        self.comboBox_output_units.clear()
        index = self.get_structure_data_index()

        suffixes = ["", "/s", "/s²"]
        unit_den = suffixes[index]

        if index <= 2:
            for label in ["m", "mm", "um", "in", "ft"]:
                self.comboBox_output_units.addItem(f"{label}{unit_den}")
        else:
            for label in ["rad", "deg"]:
                self.comboBox_output_units.addItem(f"{label}{unit_den}")

        if index == 2:
            self.comboBox_output_units.addItem("g")

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

        if self.comboBox_selector_filter.currentIndex() == SelectionType.NODES:
            app().main_window.show_mesh_render_widget()
        else:
            app().main_window.show_geometry_render_widget()

    def check_selected_ids(self):

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

    def get_response(self, selected_id: int, dof_index: int):

        index = self.comboBox_selector_filter.currentIndex()

        if index == SelectionType.SURFACES:
            nodes = self.mesh.get_nodes_from_surface(selected_id)
        elif index == SelectionType.LINES:
            nodes = self.mesh.get_nodes_from_line(selected_id)
        elif index == SelectionType.POINTS:
            nodes = self.mesh.nodes_from_points.get(selected_id)
        else:
            nodes = selected_id

        # process the acoustic dofs of the selected entities
        gdof = self.model.get_dof_indices_from_nodes(nodes, "structural")
        rows = gdof[:, dof_index]

        if isinstance(rows, int):
            response = self.nodal_solution[rows,:]
        else:
            response = np.average(self.nodal_solution[rows,:], axis=0)

        # differentiate the structural nodal solution (if required)
        n_int = self.get_structure_data_index()
        if n_int:
            response *= (1j * 2 * np.pi * self.frequencies)**n_int

        return response

    def join_model_data(self):

        self.model_results.clear()
        dof_index = self.get_dof_index()
        index = self.comboBox_selector_filter.currentIndex()
        selection_type = self.selection_types[index][:-1]

        self.y_label = self.get_ylabel()
        self.unit = self.comboBox_output_units.currentText()
        self.title = "Structural response (time domain)"

        unit_factor = self.get_unit_factor()

        for i, selected_id in enumerate(self.selected_ids):

            key = (selection_type, (selected_id))
            legend_label = f"Structural response {self.y_label.lower()} at {selection_type} [{selected_id}]"

            Xf = self.get_response(selected_id, dof_index)
            x_data, y_data = process_ifft_from_one_sided_spectrum_signal(
                self.frequencies, 
                Xf,
                dc_included = False,
                )

            self.model_results[key] = {
                "x_data": x_data,
                "y_data": unit_factor * y_data,
                "x_label": "Time [s]",
                "y_label": self.y_label,
                "title": self.title,
                "data_type": self.y_label,
                "legend": legend_label,
                "unit": self.unit,
                "color": get_color(i),
                "linestyle": "-",
            }

    def get_structure_data_index(self) -> int:
        """
        This method returns an integer corresponding to the structural data, where 0 represents 
        displacement, 1 represents velocity, and 2 represents acceleration.
        """
        volume_exists = self.mesh.are_there_volumes_in_geometry()
        n_dofs = 3 if volume_exists else 6
        index = self.comboBox_structural_results.currentIndex()
        return index // n_dofs

    def get_dof_index(self) -> int:
        """
        This method returns an integer corresponding to the structural local dof index.
        """
        volume_exists = self.mesh.are_there_volumes_in_geometry()
        n_dofs = 3 if volume_exists else 6
        index = self.comboBox_structural_results.currentIndex()
        return index % n_dofs

    def get_ylabel(self) -> str:
        dof_index = self.get_dof_index()
        index = self.get_structure_data_index()

        directions = ["x", "y", "z", "x", "y", "z"]
        dof_label = "u" if dof_index < 3 else "\u03b8"
        data_types = ["${}_{}$", "$d{}_{}$/dt", "d²${}_{}$/dt²"]

        text = data_types[index].format(dof_label, directions[dof_index])
        results_label = self.comboBox_structural_results.currentText().split(" ")[0]

        if index and dof_index >= 3:
            return f"Angular {results_label.lower()} {text}"

        return f"{results_label} {text}"

    def get_unit_factor(self):

        index = self.get_structure_data_index()
        unit_label = self.comboBox_output_units.currentText().split("/")[0]

        if index <= 2:
            if unit_label == "g":
                unit_factor = 1 / 9.80665
            else:
                unit_factor = convert_length_unit(1, "m", unit_label)
        else:
            unit_factor = convert_angle_unit(1, "rad", unit_label)

        return unit_factor

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