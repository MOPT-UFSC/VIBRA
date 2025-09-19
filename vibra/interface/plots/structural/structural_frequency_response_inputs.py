from PySide6.QtCore import Qt

from vibra.engine import AnalysisID
from vibra import app
from vibra.interface.ui_generated.plots.structural.structural_frequency_response_inputs_ui import StructuralFrequencyResponseInputs_UI
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

import numpy as np

window_title1 = "Error"
window_title2 = "Warning"

class PlotStructuralFrequencyResponseInputs(StructuralFrequencyResponseInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self.model = app().project.model
        self.mesh = app().project.model.mesh

        self._config_window()
        self._initialize()
        self._create_connections()

        self._load_analysis_setup_and_solution()
        self.geometry_selection_callback()
    
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

    def _create_connections(self):
        #
        self.comboBox_selector_filter.currentIndexChanged.connect(self.selection_type_callback)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        self.update_dof_combo_box_texts()

    def selection_type_callback(self):
        if self.comboBox_selector_filter.currentIndex() == 3:
            app().main_window.show_mesh_render_widget()
        else:
            app().main_window.show_geometry_render_widget()

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

        self.analysis_method = ""
        analysis_setup = app().project.analysis_setup

        if "analysis_id" in analysis_setup.keys():
            if analysis_setup["analysis_id"] == AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD:
                self.analysis_method = "Direct method"

            elif analysis_setup["analysis_id"] == AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION:
                self.analysis_method = "Mode Superposition method"

        self.frequencies = app().project.model.frequencies
        self.solution = app().project.structural_harmonic_solver.solution

    def check_inputs(self):

        entities = ["surfaces", "lines", "points", "nodes"]
        selection = entities[self.comboBox_selector_filter.currentIndex()]

        input_ids = self.lineEdit_selection_id.text()
        self.selected_ids, error_data = self.mesh.check_selected_ids(  
                                                                     input_ids, 
                                                                     selection = selection
                                                                     )

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
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

            surf_data = self.model.properties._get_property("surface_thickness", surface=surf_id)
            if isinstance(surf_data, dict):
                if self.model.structural_element_2d is None:
                    self.model.set_structural_elements()
                dofs_per_node = self.model.structural_element_2d.DOF_PER_NODE

            else:
                if self.model.structural_element_3d is None:
                    self.model.set_structural_elements()
                dofs_per_node = self.model.structural_element_3d.DOF_PER_NODE

            gdofs = dofs_per_node * nodes.reshape(-1, 1) + np.arange(dofs_per_node, dtype=int)
            rows = gdofs[:, dof_index]

        if isinstance(rows, int):
            response = self.solution[rows,:]
        else:
            response = np.average(self.solution[rows,:], axis=0)

        # if complex(0) in response:
        #     response += 1e-12

        return response

    def join_model_data(self):

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

        for i, selected_id in enumerate(self.selected_ids):

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