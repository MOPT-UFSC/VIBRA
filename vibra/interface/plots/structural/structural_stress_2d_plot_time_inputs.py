from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.common.common_interface import update_entities_selection
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.numeric_checks.int_list_validator import IntListValidator
from vibra.interface.numeric_checks.unit_utilities import convert_stress_unit
from vibra.interface.plots.general.frequency_response_plotter import DataFormat, FrequencyResponsePlotter
from vibra.interface.ui_generated.plots.structural.structural_stress_2d_plot_time_inputs_ui import StructuralStress2dPlotTimeInputs_UI
from vibra.interface.viewer_3d.plot_setup import StressType
from vibra.utils.signal_processing import process_ifft_from_one_sided_spectrum_signal, process_multiple_iffts_from_one_sided_spectrum_signals


class SelectionType(IntEnum):
    SURFACES = 0
    LINES = 1
    POINTS = 2
    NODES = 3


class StructuralStress2dPlotTimeInputs(StructuralStress2dPlotTimeInputs_UI):
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
    def nodal_averaged_stresses_frequency(self):
        if not isinstance(self.structural_post.nodal_averaged_stresses_frequency, np.ndarray):
            self.structural_post.compute_structural_stresses_frequency()
        return self.structural_post.nodal_averaged_stresses_frequency

    @property
    def nodal_averaged_stresses_time(self):
        if not isinstance(self.structural_post.nodal_averaged_stresses_time, np.ndarray):
            self.structural_post.compute_structural_stresses_time()

        return self.structural_post.nodal_averaged_stresses_time

    @property
    def structural_post(self):
        return app().project.get_structural_postprocessing()

    @property
    def is_stress_data_cached(self):
        cache_info = self.structural_post.recover_nodal_averaged_structural_stresses.cache_info()
        return cache_info.currsize != 0

    def set_frames_disabled(self, disabled: bool):
        self.frame_selection_controls.setDisabled(disabled)
        self.frame_plot.setDisabled(disabled)
        self.pushButton_process_nodal_stresses.setEnabled(disabled)

    def _initialize(self):
        self.validation_mode = True 
        self.exporter = None
        self.plotter = None
        self.model_results = {}
        self.selection_types = ["surfaces", "lines", "points", "nodes"]

        # update the widgets accessibility
        if self.is_stress_data_cached:
            self.process_stress_field()
        else:
            self.set_frames_disabled(True)

    def _configure_validator(self):
        validator = IntListValidator()
        self.lineEdit_selection_id.setValidator(validator)

    def _create_connections(self):

        # QComboBox connection
        self.comboBox_selector_filter.currentIndexChanged.connect(self.update_render_according_to_selector)

        # QPushButton connection
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        self.pushButton_process_nodal_stresses.clicked.connect(self.process_stress_field)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

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

    def update_render_according_to_selector(self):

        self.geometry_selection_callback()

        if self.comboBox_selector_filter.currentIndex() == SelectionType.NODES:
            app().main_window.show_mesh_render_widget()
        else:
            app().main_window.show_geometry_render_widget()

    def process_stress_field(self):

        # recover the averaged structural stresses
        if not self.is_stress_data_cached:
            def recover_stresses():
                self.structural_post.compute_structural_stresses_frequency()
                self.structural_post.compute_structural_stresses_time()

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
        self.plotter.comboBox_data_format.setCurrentIndex(DataFormat.REAL)
        self.plotter.data_format_changed_callback()
        self.plotter.frame_hlines_main.setDisabled(True)
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

        stress_vector_ifft = None

        if StressType(stress_type_index).is_normal_or_shear_stress():
            if isinstance(_node_ids, int):
                stress_freq = self.nodal_averaged_stresses_frequency[_node_ids, stress_type_index, :]
                if self.validation_mode:
                    stress_vector_ifft = self.structural_post.nodal_averaged_stresses_time[_node_ids, stress_type_index, :]
            else:
                stress_freq = np.average(self.nodal_averaged_stresses_frequency[_node_ids, stress_type_index, :], axis=0)
                if self.validation_mode:
                    stress_vector_ifft = np.average(self.structural_post.nodal_averaged_stresses_time[_node_ids, stress_type_index, :], axis=0)

            time_vector, stress_vector = process_ifft_from_one_sided_spectrum_signal(
            self.model.frequencies, 
            stress_freq,
            dc_included = False,
            )

        else:
            if isinstance(_node_ids, int):
                stresses_freq = self.nodal_averaged_stresses_frequency[_node_ids, :, :]
                if self.validation_mode:
                    stresses_ifft = self.structural_post.nodal_averaged_stresses_time[_node_ids, :, :]
            else:
                stresses_freq = np.average(self.nodal_averaged_stresses_frequency[_node_ids, :, :], axis=0)
                if self.validation_mode:
                    stresses_ifft = np.average(self.structural_post.nodal_averaged_stresses_time[_node_ids, :, :], axis=0)

            time_vector, stresses_time = process_multiple_iffts_from_one_sided_spectrum_signals(
            self.model.frequencies, 
            stresses_freq,
            dc_included = False,
            )

            stress_vector = self.structural_post.compute_advanced_structural_stresses(stresses_time.T, stress_type_index)
            if self.validation_mode:
                stress_vector_ifft = self.structural_post.compute_advanced_structural_stresses(stresses_ifft.T, stress_type_index)

        return time_vector, stress_vector, stress_vector_ifft

    def join_model_data(self):

        stress_index = self.comboBox_plotting_results.currentIndex()
        index = self.comboBox_selector_filter.currentIndex()
        selection_type = self.selection_types[index][:-1]

        self.title = "Structural stress (time domain)"
        self.y_label = self.get_ylabel()

        stress_units = self.comboBox_stress_units.currentText()
        unit_factor = convert_stress_unit(1, "Pa", stress_units)

        self.model_results.clear()

        for i, selected_id in enumerate(self.selected_ids):

            key = (selection_type, (selected_id))
            legend_label = f"Structural {self.y_label.lower()} at {selection_type} [{selected_id}]"

            time_vector, stress_vector, stress_vector_ifft = self.get_response(selection_type, selected_id, stress_index)

            self.model_results[key] = {
                "x_data": time_vector,
                "y_data": unit_factor * stress_vector,
                "x_label": "Time [s]",
                "y_label": self.y_label,
                "title": self.title,
                "data_type": self.y_label,
                "legend": legend_label,
                "unit": stress_units,
                "color": get_color(i),
                "linestyle": "-",
            }

            if not self.validation_mode:
                continue

            _key = (f"{selection_type}_xt", (selected_id))

            self.model_results[_key] = {
                "x_data": time_vector,
                "y_data": unit_factor * stress_vector_ifft,
                "x_label": "Time [s]",
                "y_label": self.y_label,
                "title": self.title,
                "data_type": self.y_label,
                "legend": legend_label,
                "unit": stress_units,
                "color": get_color(i+20),
                "linestyle": "-",
            }

    def get_ylabel(self) -> str:

        # stress index
        stress_index = self.comboBox_plotting_results.currentIndex()

        if StressType(stress_index).is_normal_or_shear_stress():

            # stress subscript
            subscript = ["x", "y", "z", "xy", "xz", "yz"]

            # stress Greek letter
            stress_letter = "\u03c3" if stress_index < 3 else "\u03c4"

            # stress label
            stress_label = f"${stress_letter}" + r"_{" + subscript[stress_index] + r"}$"

            if stress_index >= 3:
                return f"Shear stress {stress_label}"

            return f"Normal stress {stress_label}"

        else:

            match stress_index:
                case StressType.VON_MISES_STRESS:
                    return "Von Mises stress"

                case StressType.TRESCA_STRESS:
                    return "Tresca stress"

                case StressType.MAXIMUM_PRINCIPAL_STRESS_1:
                    return "Max. principal stress 1"

                case StressType.MAXIMUM_PRINCIPAL_STRESS_2:
                    return "Max. principal stress 2"

                case StressType.MAXIMUM_PRINCIPAL_STRESS_3:
                    return "Max. principal stress 3"

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
