from PyQt5.QtWidgets import QComboBox, QDialog, QLineEdit, QPushButton, QRadioButton
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance

import numpy as np

window_title1 = "Error"
window_title2 = "Warning"

class PlotStructuralFrequencyResponseInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/structural/plot_structural_frequency_response.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        app().main_window.action_model_workspace_callback()

        self.model = app().project.model
        self.mesh = app().project.model.mesh

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

        self._load_analysis_data_and_solution()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.keep_window_open = True
        self.plotter = None
        self.exporter = None
        self.dof_labels = ["Ux", "Uy", "Uz", "Rx", "Ry", "Rz"]

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_selector_filter : QComboBox
        self.comboBox_dof_selector : QComboBox

        # QLineEdit
        self.lineEdit_selection_id : QLineEdit

        # QPushButton
        self.pushButton_export_data : QPushButton
        self.pushButton_exit: QPushButton
        self.pushButton_plot_data : QPushButton

    def _create_connections(self):
        #
        self.comboBox_selector_filter.currentIndexChanged.connect(self.selection_type_callback)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
    
    def selection_type_callback(self):
        if self.comboBox_selector_filter.currentIndex() == 3:
            app().main_window.viewer_tabs.show_mesh()
        else:
            app().main_window.viewer_tabs.show_geometry()

    def geometry_selection_callback(self):

        faces = app().main_window.selected_geometry_surfaces
        lines = app().main_window.selected_geometry_lines
        points = app().main_window.selected_geometry_points
        nodes = app().main_window.selected_mesh_nodes

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

    def _load_analysis_data_and_solution(self):

        self.analysis_method = ""
        analysis_data = app().project.analysis_data

        if "analysis_id" in analysis_data.keys():
            if analysis_data["analysis_id"] == 0:
                self.analysis_method = "Direct method"

            elif analysis_data["analysis_id"] == 1:
                self.analysis_method = "Mode Superposition method"

        self.frequencies = app().project.structural_harmonic_solver.frequencies
        self.solution_full = app().project.structural_harmonic_solver.solution_full

    def check_inputs(self):

        entities = ["surfaces", "lines", "points", "nodes"]
        selection = entities[self.comboBox_selector_filter.currentIndex()]

        input_ids = self.lineEdit_selection_id.text()
        self.typed_ids = self.mesh.check_selected_ids(  
                                                      input_ids, 
                                                      selection = selection
                                                      )

        if self.typed_ids is None:
            self.lineEdit_selection_id.setFocus()
            return True

        self.local_dof = self.comboBox_dof_selector.currentIndex()
        self.local_dof_label = self.dof_labels[self.local_dof]

        if self.local_dof in [0, 1, 2]:
            self.unit_label = "m"
            self.y_label = "Displacement"

        else:
            self.unit_label = "rad"
            self.y_label = "Rotation"

        return False

    def plot_data_callback(self):

        if self.check_inputs():
            return

        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def export_data_callback(self):
        
        if self.check_inputs():
            return

        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def get_response(self, selection_type: str, selected_id: int, dof_index: int):

        surface_ids = list()
        element_3d, element_2d = app().project.structural_harmonic_solver.assembler.get_element()

        if selection_type == "surface":
            surface_ids.append(selected_id)
            nodes = self.mesh.nodes_from_surfaces[selected_id]

        elif selection_type == "line":           
            surface_ids = self.mesh.surface_from_line[selected_id]
            nodes = self.mesh.nodes_from_lines[selected_id]

        elif selection_type == "point":
            node_id = selected_id - 1
            for surf_id, surf_nodes in self.mesh.nodes_from_surfaces.items():
                if node_id in surf_nodes:
                    if surf_id not in surface_ids:
                        surface_ids.append(surf_id)

            nodes = np.array([node_id], dtype=int)

        else:
            for surf_id, surf_nodes in self.mesh.nodes_from_surfaces.items():
                if selected_id in surf_nodes:
                    if surf_id not in surface_ids:
                        surface_ids.append(surf_id)

            nodes = np.array([selected_id], dtype=int)

        for surf_id in surface_ids:

            surf_data = self.model.properties._get_property("surface_thickness", surface=surf_id)
            if isinstance(surf_data, dict):
                dofs_per_node = element_2d.DOFS_PER_NODE
            else:
                dofs_per_node = element_3d.DOFS_PER_NODE

            gdofs = dofs_per_node * nodes.reshape(-1, 1) + np.arange(dofs_per_node, dtype=int)
            rows = gdofs[:, dof_index]

        if isinstance(rows, int):
            response = self.solution_full[rows,:]
        else:
            response = np.average(self.solution_full[rows,:], axis=0)

        # if complex(0) in response:
        #     response += 1e-12

        return response

    def join_model_data(self):

        self.hide()

        if self.comboBox_selector_filter.currentIndex() == 0:
            selection_type = "surface"
        elif self.comboBox_selector_filter.currentIndex() == 1:
            selection_type = "line"
        elif self.comboBox_selector_filter.currentIndex() == 2:
            selection_type = "point"
        else:
            selection_type = "node"

        self.model_results = dict()
        self.title = f"Structural frequency response - {self.analysis_method}"

        for i, selected_id in enumerate(self.typed_ids):

            key = (selection_type, (selected_id))
            legend_label = f"Structural response {self.local_dof_label} at {selection_type} [{selected_id}]"
            y_data = self.get_response(selection_type, selected_id, self.local_dof)

            self.model_results[key] = { 
                                        "x_data" : self.frequencies,
                                        "y_data" : y_data,
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : self.y_label,
                                        "title" : self.title,
                                        "data_type" : self.y_label,
                                        "legend" : legend_label,
                                        "unit" : self.unit_label,
                                        "color" : get_color(i),
                                        "linestyle" : "-"  
                                      }

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        self.keep_window_open = False
        return super().closeEvent(a0)
    
def get_color(index):

    colors = [  (0,0,1), 
                (0,0,0), 
                (1,0,0),
                (0,1,1), 
                (1,0,1), 
                (1,1,0),
                (0.25,0.25,0.25)  ]

    if index <= 6:
        return colors[index]
    else:
        return tuple(np.random.randint(0, 255, size=3) / 255)