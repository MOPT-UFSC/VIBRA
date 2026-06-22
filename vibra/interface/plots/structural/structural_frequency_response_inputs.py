import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.engine.analysis_info import HarmonicAnalysisSetup
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.ui_generated.plots.structural.structural_frequency_response_inputs_ui import StructuralFrequencyResponseInputs_UI


class PlotStructuralFrequencyResponseInputs(StructuralFrequencyResponseInputs_UI):
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
        return app().project.model.solution.nodal_solution

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
        self.dof_labels = ["Ux", "Uy", "Uz", "Rx", "Ry", "Rz"]

        self.selection_types = ["surfaces", "lines", "points", "nodes"]

    def _create_connections(self):
        #
        self.comboBox_structural_results.currentIndexChanged.connect(self.update_combo_box_items_callback)
        self.comboBox_selector_filter.currentIndexChanged.connect(self.selection_type_callback)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.update_dof_combo_box_texts()
        self.update_combo_box_items_callback()

    def update_combo_box_items_callback(self):
        results_label = self.comboBox_structural_results.currentText()
        index = self.comboBox_structural_results.currentIndex()

        def dof_label(dof_index: str, n_int: int):
            dof_type = "U" if dof_index > 3 else "\u03b8"
            directions = ["x", "y", "z", "x", "y", "z"]
            data_types = ["{}{}", "d{}{}/dt", "d²{}{}/dt²"]
            # data_types = ["{}<sub>{}</sub>", "d{}<sub>{}</sub>/dt", "d²{}<sub>{}</sub>/dt²"]
            return data_types[n_int].format(dof_type, directions[dof_index])

        volume_exists = self.mesh.are_there_volumes_in_geometry()
        n_dofs = 3 if volume_exists else 6

        self.comboBox_dof_selector.blockSignals(True)
        # self.comboBox_dof_selector.clear()

        for dof_index in range(n_dofs):
            _dof_label = dof_label(dof_index, index)
            # self.comboBox_dof_selector.setItemText(dof_index, f"{_dof_label}")
            self.comboBox_dof_selector.setItemText(dof_index, f"{results_label} {_dof_label}")

        self.comboBox_dof_selector.blockSignals(False)

    def selection_type_callback(self):
        if self.comboBox_selector_filter.currentIndex() == 3:
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

        else:
            self.lineEdit_selection_id.setText("")

    def update_dof_combo_box_texts(self):

        dof_labels = [
            "Displacement Ux", 
            "Displacement Uy", 
            "Displacement Uz", 
            "Rotation Rx", 
            "Rotation Ry", 
            "Rotation Rz",
            ]

        volume_exists = self.mesh.are_there_volumes_in_geometry()
        if volume_exists:
            active_dof_labels = dof_labels[:3]
        else:
            active_dof_labels = dof_labels

        self.comboBox_dof_selector.clear()
        self.comboBox_dof_selector.addItems(active_dof_labels)

    def _load_analysis_setup_and_solution(self):
        analysis_setup = self.model.analysis_setup

        self.analysis_method = ""
        if isinstance(analysis_setup, HarmonicAnalysisSetup):
            analysis_method = analysis_setup.analysis_method.capitalize().replace("_", " ")
            self.analysis_method = f"{analysis_method} method"

        self.frequencies = self.model.frequencies

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

    def get_response(self, selection_type: str, selected_id: int, dof_index: int):

        surface_ids = list()

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
                dof_per_node = self.model.structural_element_2d.DOF_PER_NODE

            else:
                if self.model.structural_element_3d is None:
                    self.model.set_structural_elements()
                dof_per_node = self.model.structural_element_3d.DOF_PER_NODE

            gdof = dof_per_node * nodes.reshape(-1, 1) + np.arange(dof_per_node, dtype=int)
            rows = gdof[:, dof_index]

        if isinstance(rows, int):
            response = self.nodal_solution[rows,:]
        else:
            response = np.average(self.nodal_solution[rows,:], axis=0)

        n_int = self.comboBox_structural_results.currentIndex()

        if n_int:
            response *= (1j * 2 * np.pi * self.frequencies)**n_int

        return response

    def join_model_data(self):

        dof_index = self.comboBox_dof_selector.currentIndex()
        index = self.comboBox_selector_filter.currentIndex()
        selection_type = self.selection_types[index][:-1]

        self.model_results = dict()
        self.y_label = self.get_ylabel()
        self.unit = self.get_unit()
        self.title = f"Structural frequency response - {self.analysis_method}"

        for i, selected_id in enumerate(self.selected_ids):

            key = (selection_type, (selected_id))
            legend_label = f"Structural response {self.dof_labels[dof_index]} at {selection_type} [{selected_id}]"
            y_data = self.get_response(selection_type, selected_id, dof_index)

            self.model_results[key] = {
                "x_data": self.frequencies,
                "y_data": y_data,
                "x_label": "Frequency [Hz]",
                "y_label": self.y_label,
                "title": self.title,
                "data_type": self.y_label,
                "legend": legend_label,
                "unit": self.unit,
                "color": get_color(i),
                "linestyle": "-",
            }

    def get_ylabel(self) -> str:
        results_label = self.comboBox_structural_results.currentText()
        dof_index = self.comboBox_dof_selector.currentIndex()

        directions = ["x", "y", "z", "x", "y", "z"]
        dof_type = "u" if dof_index < 3 else "\u03b8"
        data_types = ["${}_{}$", "$d{}_{}$/dt:", "d²${}_{}$/dt²:"]

        index = self.comboBox_structural_results.currentIndex()
        dof_label = data_types[index].format(dof_type, directions[dof_index])

        if index and dof_index  >= 3:
            return f"Angular {results_label.lower()} {dof_label}"

        return f"{results_label} {dof_label}"

    def get_unit(self) -> str:
        dof_index = self.comboBox_dof_selector.currentIndex()
        index = self.comboBox_structural_results.currentIndex()

        suffixes = ["", "/s", "/s²"]
        unit_num = "m" if dof_index < 3 else "rad"
        unit_den = suffixes[index]

        return f"{unit_num}{unit_den}"

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
    else:
        return tuple(np.random.randint(0, 255, size=3) / 255)