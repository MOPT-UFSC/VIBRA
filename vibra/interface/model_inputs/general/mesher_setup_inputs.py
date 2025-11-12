from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QIcon
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QVBoxLayout

from vibra import app, ICON_DIR
from vibra.engine.mesher import gmsh_constants
from vibra.engine.mesher.element_type import (
    ElementType,
    TETRAHEDRON_4,
    TETRAHEDRON_10,
    HEXAHEDRON_8,
    HEXAHEDRON_20,
)

from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.ui_generated.mesh.mesher_setup_inputs_ui import MesherSetupInputs_UI
from vibra.interface.ui_generated.plots.general.mesh_quality_histogram_plot_ui import MeshQualityHistogramPlot_UI

import logging
import matplotlib.colors as mcolors
import numpy as np

from collections import defaultdict
from copy import deepcopy
from enum import IntEnum
from gmsh import isInitialized as is_gmsh_initialized

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


gmsh_algorithms_2d = [
    gmsh_constants.MESH_ADAPT_2D,
    gmsh_constants.AUTOMATIC_2D,
    gmsh_constants.INITIAL_MESH_ONLY_2D,
    gmsh_constants.DELAUNAY_2D,
    gmsh_constants.FRONTAL_DELAUNAY_2D,
    gmsh_constants.QUASI_STRUCTURED_QUADS_2D,
]

gmsh_algorithms_3d = [
    gmsh_constants.DELAUNAY_3D,
    gmsh_constants.FRONTAL_3D,
    gmsh_constants.HXT_3D,
]

map_algorithms_2d = dict(zip(gmsh_algorithms_2d, [0, 1, 2, 3, 4, 5]))
map_algorithms_3d = dict(zip(gmsh_algorithms_3d, [0, 1, 2]))


class GMSHAlgorithms_3D(IntEnum):
    DELAUNAY_3D = 0
    FRONTAL_3D = 1
    HXT_3D = 2


error_title = "Error"
warning_title = "Warning"


class MesherSetupInputs(MesherSetupInputs_UI):
    def __init__(self, **kwargs):
        super().__init__()

        self.close_after_generate = kwargs.get("close_after_generate", False)

        app().main_window.set_input_widget(self)
        self.mesh = app().project.model.mesh

        self._config_window()
        self._initialize()
        self._create_connections()
        self._config_widgets()
        self.update_combo_boxes_according_to_geometry_info()
        self.update_advanced_gmsh_controls()
        self._load_current_mesh_setup()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.complete = False

        self.keep_window_open = True
        self.bad_elements_showed = False
        self.synchronize_sizes = False

        self.mesh_quality_data = None
        self.mesh_setup = dict()
        self.mesh_refinement_data = defaultdict(list)
        self.cache_mesh_refinement_data = defaultdict(list)

        self.mesh_quality_parameters = {
            0: "gamma",
            1: "volume",
            2: "minSJ",
            3: "aspectRatio",
        }

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _config_widgets(self):
        #
        self.comboBox_2d_algorithm.setDisabled(True)
        self.comboBox_2d_algorithm.setDisabled(True)
        self.comboBox_recombination_algorithm.setDisabled(True)
        self.comboBox_subdivision_algorithm.setDisabled(True)
        self.comboBox_second_order_incomplete.setDisabled(True)
        self.comboBox_recombine_all.setDisabled(True)
        #
        self.pushButton_show_bad_elements.setDisabled(True)
        self.pushButton_generate_mesh.setAutoDefault(False)
        #
        self.lineEdit_selected_ids.setDisabled(True)
        #
        widths = [160, 160]
        for i, width in enumerate(widths):
            self.tableWidget_refining_mesh_data.setColumnWidth(i, width)
            self.tableWidget_refining_mesh_data.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)
        #
        self.tableWidget_refining_mesh_data.setSelectionBehavior(QAbstractItemView.SelectionBehavior(1))
        self.tableWidget_refining_mesh_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(0))
        self.tableWidget_refining_mesh_data.horizontalHeader().setStretchLastSection(True)

    def _create_connections(self):
        #
        self.comboBox_shape_function.currentIndexChanged.connect(self.update_advanced_gmsh_controls)
        self.comboBox_element_type.currentIndexChanged.connect(self.update_advanced_gmsh_controls)
        self.comboBox_mesh_quality_metrics.currentIndexChanged.connect(self.mesh_quality_metrics_callback)
        #
        self.doubleSpinBox_maximum_element_size.valueChanged.connect(self.maximum_element_size_changed_callback)
        self.doubleSpinBox_minimum_element_size.valueChanged.connect(self.minimum_element_size_changed_callback)
        #
        self.pushButton_add.clicked.connect(self.add_button_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_delete.clicked.connect(self.remove_callback)
        self.pushButton_generate_mesh.clicked.connect(self.generate_mesh_callback)
        self.pushButton_show_bad_elements.clicked.connect(self.show_bad_elements)
        self.pushButton_plot_histogram.clicked.connect(self.plot_mesh_parameter_histogram)
        self.pushButton_syncrhonize.clicked.connect(self.synchronize_button_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.tableWidget_refining_mesh_data.itemClicked.connect(self.item_clicked_callback)
        self.tableWidget_mesh_quality.itemClicked.connect(self.mesh_quality_item_clicked)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.mesh_quality_metrics_callback()

    def mesh_quality_metrics_callback(self):

        if self.comboBox_mesh_quality_metrics.currentText() == "Disabled":
            if self.tabWidget_main.currentIndex() == 2:
                self.tabWidget_main.setCurrentIndex(0)
            self.tabWidget_main.setTabVisible(2, False)
            return

        if self.is_mesh_quality_computed():
            self.config_control_quality_table()
            return

        def mesh_quality_callback():
            self.hide()
            self.mesh.compute_mesh_quality_parameters()
            app().file.write_mesh_quality_data_in_file()
            self.config_control_quality_table()

        if is_gmsh_initialized():
            LoadingWindow(mesh_quality_callback).run()

    def maximum_element_size_changed_callback(self):
        if self.synchronize_sizes:
            value = self.doubleSpinBox_maximum_element_size.value()
            self.doubleSpinBox_minimum_element_size.setValue(value)

    def minimum_element_size_changed_callback(self):
        if self.synchronize_sizes:
            value = self.doubleSpinBox_minimum_element_size.value()
            self.doubleSpinBox_maximum_element_size.setValue(value)

    def synchronize_button_callback(self):
        self.synchronize_sizes = not self.synchronize_sizes
        if self.synchronize_sizes:
            icon = QIcon(str(ICON_DIR / "sync_disabled.png"))
            tool_tip = "Desynchronize the minimum and maximum sizes"
        else:
            icon = QIcon(str(ICON_DIR / "sync_enabled.png"))
            tool_tip = "Synchronize the minimum and maximum sizes"

        self.pushButton_syncrhonize.setIcon(icon)
        self.pushButton_syncrhonize.setToolTip(tool_tip)
        self.maximum_element_size_changed_callback()

    def geometry_selection_callback(self):
        faces = app().main_window.selected_geometry_surfaces
        volumes = app().main_window.selected_geometry_volumes

        if volumes:
            selection = volumes
            self.label_selected_ids.setText("Selected volume IDs:")
        elif faces:
            selection = faces
            self.label_selected_ids.setText("Selected surface IDs:")
        else:
            self.lineEdit_selected_ids.setText("")
            return

        if selection:
            text = ", ".join([str(i) for i in selection])
            self.lineEdit_selected_ids.setText(text)

    def tab_event_callback(self):
        mesh_quality_tab = self.tabWidget_main.currentIndex() == 2
        self.pushButton_generate_mesh.setDisabled(mesh_quality_tab)

    def item_clicked_callback(self, item):
        row = item.row()
        selection_type = self.tableWidget_refining_mesh_data.item(row, 1).text()
        str_selected_ids = self.tableWidget_refining_mesh_data.item(row, 2).text()
        selected_ids = [int(_id) for _id in str_selected_ids.split(",")]

        if selected_ids:
            if selection_type == "volumes":
                app().main_window.set_geometry_selection(volumes=selected_ids)
            else:
                app().main_window.set_geometry_selection(surfaces=selected_ids)

    def get_selected_ids(self):
        selected_ids = list()
        if self.lineEdit_selected_ids.text() == "":
            return selected_ids

        try:
            str_selected_ids = self.lineEdit_selected_ids.text()
            selected_ids = [int(_id) for _id in str_selected_ids.split(",")]
        except Exception:
            pass

        return selected_ids

    def add_button_callback(self):
        if self.lineEdit_selected_ids.text() == "":
            return

        if app().main_window.selected_geometry_volumes:
            selected_type = "volumes"
        else:
            selected_type = "surfaces"

        selected_ids = self.get_selected_ids()
        ref_size = self.doubleSpinBox_refined_element_size.value()

        if selected_ids:
            for selected_id in selected_ids:
                if (
                    selected_id
                    not in self.mesh_refinement_data[(selected_type, ref_size)]
                ):
                    self.mesh_refinement_data[(selected_type, ref_size)].append(
                        selected_id
                    )

            for key, _selected_ids in self.mesh_refinement_data.copy().items():
                if key[0] == selected_type and key[1] != ref_size:
                    for selected_id in selected_ids:
                        if selected_id in _selected_ids:
                            _selected_ids.remove(selected_id)
                            if _selected_ids:
                                self.mesh_refinement_data[key] = _selected_ids
                            else:
                                self.mesh_refinement_data.pop(key)

            self.update_refining_table_data()

        self.lineEdit_selected_ids.setText("")

    def remove_callback(self):
        current_row = self.tableWidget_refining_mesh_data.currentRow()
        if current_row == -1:
            return

        try:
            if isinstance(current_row, int):
                ref_size = float(
                    self.tableWidget_refining_mesh_data.item(current_row, 0).text()
                )
                selection_type = self.tableWidget_refining_mesh_data.item(
                    current_row, 1
                ).text()
                self.tableWidget_refining_mesh_data.removeRow(current_row)

                if (selection_type, ref_size) in self.mesh_refinement_data.keys():
                    self.mesh_refinement_data.pop((selection_type, ref_size))
                    self.update_refining_table_data()

            app().main_window.set_geometry_selection()

        except Exception:
            return

    def _load_initial_element_size(self):
        element_size = app().project.model.initial_element_size
        if element_size is not None:
            self.doubleSpinBox_maximum_element_size.setValue(element_size)
            self.doubleSpinBox_minimum_element_size.setValue(int(0.9 * element_size))

    def _load_current_mesh_setup(self):
        mesh_setup = app().project.model.mesh_setup

        if mesh_setup is None:
            self._load_initial_element_size()
            return

        if isinstance(mesh_setup, dict):
            try:

                geometry_tolerance = mesh_setup["geometry_tolerance"]
                minimum_element_size = mesh_setup["minimum_element_size"]
                maximum_element_size = mesh_setup["maximum_element_size"]
                size_factor = mesh_setup["size_factor"]
                mesh_refinement_parameters = mesh_setup["mesh_refinement_parameters"]
                mesh_connection = mesh_setup.get("mesh_connection", True)

                gmsh_algorithm_3d = mesh_setup.get("algorithm_3d")
                if gmsh_algorithm_3d is not None:
                    self.comboBox_3d_algorithm.setCurrentIndex(map_algorithms_3d[gmsh_algorithm_3d])

                self.update_element_type(mesh_setup["ElementType"])

                self.doubleSpinBox_maximum_element_size.setValue(maximum_element_size)
                self.doubleSpinBox_minimum_element_size.setValue(minimum_element_size)
                self.doubleSpinBox_size_factor.setValue(size_factor)
                self.lineEdit_geometry_tolerance.setText(str(geometry_tolerance))

                self.comboBox_volumes_interface_behavior.setCurrentIndex(int(mesh_connection))
                
                for selection_type, e_size, selected_ids in mesh_refinement_parameters:
                    self.mesh_refinement_data[(selection_type, e_size)].extend(selected_ids)

                self.cache_refinement_data()
                self.update_refining_table_data()
                self.config_control_quality_table()

            except Exception as error_log:
                self.hide()
                title = "Error while loading mesh setup"
                message = str(error_log)
                PrintMessageInput([error_title, title, message])

    def cache_refinement_data(self):
        self.cache_mesh_refinement_data = deepcopy(self.mesh_refinement_data)

    def update_refining_table_data(self):
        self.tableWidget_refining_mesh_data.clearContents()

        try:
            row = 0
            for (
                _selection_type,
                _e_size,
            ), _selected_ids in self.mesh_refinement_data.items():
                str_selected_ids = ", ".join([str(i) for i in _selected_ids])

                self.tableWidget_refining_mesh_data.setRowCount(row + 1)
                self.tableWidget_refining_mesh_data.setItem(
                    row, 0, QTableWidgetItem(str(_e_size))
                )
                self.tableWidget_refining_mesh_data.setItem(
                    row, 1, QTableWidgetItem(_selection_type)
                )
                self.tableWidget_refining_mesh_data.setItem(
                    row, 2, QTableWidgetItem(str_selected_ids)
                )

                for j in range(3):
                    self.tableWidget_refining_mesh_data.item(row, j).setTextAlignment(
                        Qt.AlignCenter
                    )

                row += 1

        except Exception as error_log:
            self.hide()
            title = "Error while table data"
            message = str(error_log)
            PrintMessageInput([error_title, title, message])

    def update_element_type(self, ElementType: ElementType):

        if ElementType == TETRAHEDRON_4:
            self.comboBox_element_type.setCurrentText("Tetrahedral")
            self.comboBox_shape_function.setCurrentText("Linear")

        elif ElementType == TETRAHEDRON_10:
            self.comboBox_element_type.setCurrentText("Tetrahedral")
            self.comboBox_shape_function.setCurrentText("Quadratic")

        elif ElementType == HEXAHEDRON_8:
            self.comboBox_element_type.setCurrentText("Hexahedral")
            self.comboBox_shape_function.setCurrentText("Linear")

        elif ElementType == HEXAHEDRON_20:
            self.comboBox_element_type.setCurrentText("Hexahedral")
            self.comboBox_shape_function.setCurrentText("Quadratic")

        else:
            NotImplementedError()

    def generate_mesh_callback(self):
        if self.check_mesh_inputs():
            return

        if self.bad_elements_showed:
            app().main_window.distinguish_mesh_solids([])

        app().main_window.clear_selection()
        self.hide()

        def generate_function():
            logging.info("Processing mesh... [20/100]")
            app().project.reset_solutions()

            logging.info("Processing mesh... [30/100]")
            app().project.set_mesh_setup(self.mesh_setup)

            mesh_setup = deepcopy(self.mesh_setup)
            mesh_setup.pop("ElementType")
            app().file.write_mesh_setup_in_file(mesh_setup)

            logging.info("Processing mesh... [40/100]")
            app().project.generate_mesh()

        LoadingWindow(generate_function).run()

        if self.mesh.error_data:
            title = self.mesh.error_data.get("title")
            message = self.mesh.error_data.get("message")
            PrintMessageInput([error_title, title, message])
            return

        disconnected_nodes = bool(self.mesh.disconnected_nodes_data)
        collapsed_elements = bool(self.mesh.collapsed_3d_elements or self.mesh.collapsed_2d_elements or self.mesh.collapsed_1d_elements)

        run_analysis_button = app().main_window.analysis_toolbar.pushButton_run_analysis
        run_analysis_button.setDisabled(collapsed_elements or disconnected_nodes)

        if app().project.model.analysis_setup is None:
            run_analysis_button.setDisabled(True)

        self.check_post_process_mesh_criteria()
        self.process_degress_of_freedom_if_necessary()

        app().file.write_mesh_data_in_file()
        app().file.write_geometry_data_in_file()

        self.mesh_quality_data = None
        if self.comboBox_mesh_quality_metrics.currentText() == "Enabled":
            app().file.write_mesh_quality_data_in_file()
            self.config_control_quality_table()
            self.tabWidget_main.setTabVisible(2, True)
        else:
            app().file.remove_mesh_quality_data_from_project_file()

        self.cache_refinement_data()
        app().main_window.update_mesh_information()
        app().main_window.update_geometry_information()

        LoadingWindow(self.actions_to_finalize).run()
        self.complete = True

        disconnected_nodes = self.mesh.get_list_of_disconnected_nodes()
        if disconnected_nodes:
            app().main_window.set_mesh_selection(nodes=disconnected_nodes)

    def check_post_process_mesh_criteria(self):

        disconnected_nodes = self.mesh.disconnected_nodes_data
        if disconnected_nodes:

            message = ""
            title = "The generated mesh contains disconnected nodes"

            if disconnected_nodes.get("elements_3D"):
                message = "Disconnected nodes from 3d elements: " + ", ".join(str(int(node_id)) for node_id in disconnected_nodes.get("elements_3D")) + "."

            if disconnected_nodes.get("elements_2D"):
                message = "Disconnected nodes from 2d elements: " + ", ".join(str(int(node_id)) for node_id in disconnected_nodes.get("elements_2D")) + "."

            if disconnected_nodes.get("elements_1D"):
                message = "Disconnected nodes from 1d elements: " + ", ".join(str(int(node_id)) for node_id in disconnected_nodes.get("elements_1D")) + "."

            PrintMessageInput([error_title, title, message])

        collapsed_elements = self.mesh.collapsed_3d_elements or self.mesh.collapsed_2d_elements or self.mesh.collapsed_1d_elements
        if collapsed_elements:

            message = ""
            title = "The generated mesh contains collapsed elements"

            if self.mesh.collapsed_3d_elements:
                message += "Collapsed 3d elements: " + ", ".join(str(elem_id) for elem_id in self.mesh.collapsed_3d_elements) + ".\n\n"

            if self.mesh.collapsed_2d_elements:
                message += "Collapsed 2d elements: " + ", ".join(str(elem_id) for elem_id in self.mesh.collapsed_2d_elements) + ".\n\n"

            if self.mesh.collapsed_1d_elements:
                message += "Collapsed 1d elements: " + ", ".join(str(elem_id) for elem_id in self.mesh.collapsed_1d_elements) + "."

            PrintMessageInput([error_title, title, message])

    def process_degress_of_freedom_if_necessary(self):
        if not app().project.model.properties.is_the_surface_property_present_in_the_model(
            "degrees_of_freedom_decoupling"
        ):
            return

        def process_decoupling():
            app().project.model.mesh.cache_mesh_information()
            app().project.model.process_degrees_of_freedom_decoupling()

        LoadingWindow(process_decoupling).run()

    def actions_to_finalize(self):
        if self.close_after_generate:
            self.close()

        logging.info("Updating render... [95/100]")
        app().main_window.action_mesh_workspace_callback()
        app().main_window.update_plots()

        app().project.reset_solutions()
        app().file.remove_results_data_from_project_file()
        app().main_window.analysis_toolbar.pushButton_reset_solution.setDisabled(True)
        app().main_window.disable_advanced_acoustic_plots_buttons(True)

        app().main_window.update_symbols()

    def get_mesh_refinement_data(self):
        refine_data = list()
        for (
            selection_type,
            ref_size,
        ), selected_ids in self.mesh_refinement_data.items():
            refine_data.append((selection_type, ref_size, selected_ids))

        return refine_data

    def check_mesh_inputs(self):

        maximum_element_size = self.doubleSpinBox_maximum_element_size.value()
        minimum_element_size = self.doubleSpinBox_minimum_element_size.value()
        size_factor = self.doubleSpinBox_size_factor.value()

        lineEdit = self.lineEdit_geometry_tolerance
        geometry_tolerance = self.check_inputs(lineEdit, "Geometry tolerance")
        if self.stop:
            lineEdit.setFocus()
            return True

        solid_element = self.get_element_type()
        if solid_element is None:
            return True

        alg3d_index = self.comboBox_3d_algorithm.currentIndex()
        if alg3d_index == GMSHAlgorithms_3D.DELAUNAY_3D:
            solid_element.algorithm_3d = gmsh_constants.DELAUNAY_3D
        elif alg3d_index == GMSHAlgorithms_3D.FRONTAL_3D:
            solid_element.algorithm_3d = gmsh_constants.FRONTAL_3D
        elif alg3d_index == GMSHAlgorithms_3D.HXT_3D:
            solid_element.algorithm_3d = gmsh_constants.HXT_3D
        else:
            return

        merge_nodes = self.comboBox_volumes_interface_behavior.currentText() == "Merge nodes"
        mesh_quality_metrics = self.comboBox_mesh_quality_metrics.currentText() == "Enabled"

        self.mesh_setup = {
            "ElementType" : solid_element,
            "element_type" : self.comboBox_element_type.currentText().lower(),
            "shape_function" : self.comboBox_shape_function.currentText().lower(),
            "minimum_element_size" : minimum_element_size,
            "maximum_element_size" : maximum_element_size,
            "size_factor" : size_factor,
            "geometry_tolerance" : geometry_tolerance,
            "algorithm_3d" : solid_element.algorithm_3d,
            "mesh_refinement_parameters" : self.get_mesh_refinement_data(),
            "mesh_connection" : merge_nodes,
            "mesh_quality_metrics"  : mesh_quality_metrics,
        }

    def get_element_type(self) -> ElementType:
        element_type = self.comboBox_element_type.currentText().lower()
        shape_function = self.comboBox_shape_function.currentText().lower()

        if element_type == "tetrahedral" and shape_function == "linear":
            return TETRAHEDRON_4
        elif element_type == "tetrahedral" and shape_function == "quadratic":
            return TETRAHEDRON_10
        elif element_type == "hexahedral" and shape_function == "linear":
            return HEXAHEDRON_8
        elif element_type == "hexahedral" and shape_function == "quadratic":
            return HEXAHEDRON_20
        else:
            return None
            # raise NotImplementedError(f"Element type not defined!")

    def update_combo_boxes_according_to_geometry_info(self):
        volume_exists = self.mesh.are_there_volumes_in_geometry()
        if not volume_exists:
            self.comboBox_element_type.removeItem(1)
            self.comboBox_shape_function.removeItem(1)

    def update_advanced_gmsh_controls(self):
        element_type = self.get_element_type()
        if element_type not in [None, TETRAHEDRON_4, TETRAHEDRON_10]:
            self.comboBox_mesh_quality_metrics.setCurrentText("Disabled")
            self.comboBox_mesh_quality_metrics.setDisabled(True)
            if element_type is None:
                return

        else:
            self.comboBox_mesh_quality_metrics.setEnabled(True)

        self.comboBox_2d_algorithm.setCurrentIndex(map_algorithms_2d[element_type.algorithm_2d])
        self.comboBox_3d_algorithm.setCurrentIndex(map_algorithms_3d[element_type.algorithm_3d])

        self.comboBox_recombination_algorithm.setCurrentIndex(element_type.recombination_algorithm)
        self.comboBox_subdivision_algorithm.setCurrentIndex(element_type.subdivision_algorithm)
        self.comboBox_recombine_all.setCurrentIndex(int(element_type.recombine_all))
        self.comboBox_second_order_incomplete.setCurrentIndex(int(element_type.second_order_incomplete))

    def check_inputs(
        self, lineEdit, label, only_positive=True, zero_included=False, _float=True
    ):
        self.stop = False
        message = ""
        title = "Invalid input at mesh setup"

        if lineEdit.text() != "":
            try:
                if _float:
                    out = float(lineEdit.text())
                else:
                    out = int(lineEdit.text())

                if only_positive:
                    if zero_included:
                        if out < 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is allowed."
                    elif out <= 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is not allowed."

            except Exception as _err:
                message = "Dear user, you have typed and invalid value at the \n"
                message += f"{label} input field.\n\n"
                message += str(_err)

        else:
            if zero_included:
                return float(0)
            else:
                message = f"Insert some value at the {label} input field."

        if message != "":
            PrintMessageInput([error_title, title, message])
            self.stop = True
            return None

        return out

    def is_mesh_quality_computed(self):
        if self.mesh_quality_data is None:
            self.mesh_quality_data = app().file.read_mesh_quality_data_from_file()
            if self.mesh_quality_data is None:
                return False

        if isinstance(self.mesh_quality_data, dict):
            return bool(sum([len(qdata) for qdata in self.mesh_quality_data.values()])) 

        return False

    def config_control_quality_table(self):

        volume_exists = self.mesh.are_there_volumes_in_geometry()
        self.tabWidget_main.setTabVisible(2, volume_exists)                
        if not volume_exists:
            return

        if self.get_element_type() not in [TETRAHEDRON_4, TETRAHEDRON_10]:
            self.tabWidget_main.setTabVisible(2, False)
            self.comboBox_mesh_quality_metrics.setCurrentText("Disabled")
            self.comboBox_mesh_quality_metrics.setDisabled(True)
            return

        else:
            self.comboBox_mesh_quality_metrics.setEnabled(True)

        if not self.is_mesh_quality_computed():
            return
        
        self.comboBox_mesh_quality_metrics.setCurrentText("Enabled")
        self.pushButton_plot_histogram.setDisabled(True)        
        quality_bins = self.mesh.quality_bins

        param_map = {
            0: (
                "gamma",
                "Gamma",
                lambda v: "green"
                if v > quality_bins["gamma"][0]
                else "yellow"
                if v > quality_bins["gamma"][1]
                else "red",
            ),
            1: (
                "volume",
                "Volume (mm³)",
                lambda v: "green"
                if v > quality_bins["volume"][0]
                else "yellow"
                if v > quality_bins["volume"][1]
                else "red",
            ),
            2: (
                "minSJ",
                "Scaled Jacobian",
                lambda v: "green"
                if v > quality_bins["minSJ"][0]
                else "yellow"
                if v > quality_bins["minSJ"][1]
                else "red",
            ),
            3: (
                "aspectRatio",
                "Aspect Ratio",
                lambda v: "green"
                if v < quality_bins["aspectRatio"][0]
                else "yellow"
                if v < quality_bins["aspectRatio"][1]
                else "red",
            ),
        }

        self.tableWidget_mesh_quality.clearContents()
        self.tableWidget_mesh_quality.setRowCount(len(param_map))
        self.tableWidget_mesh_quality.horizontalHeader().resizeSection(0, 110)
        self.tableWidget_mesh_quality.horizontalHeader().resizeSection(2, 80)

        # This should be done in the done in the ui file
        # but it kept going like this so I'm leaving it here.

        gamma_tool_tip  = "The Gamma quality metric is the ratio between the radius of the inscribed sphere and\n"
        gamma_tool_tip += "the radius of the circumscribed sphere of an element. It ranges from 0 to 1, \n"
        gamma_tool_tip += "where values closer to 1 indicate more regular, well-shaped elements.\n"

        volume_tool_tip  = "The Volume metric is simply the calculated volume of the elements. \n"
        volume_tool_tip += "Very small volumes possibly indicate collapsed elements, wich are a problem.\n"
        
        scaled_jacobian_tool_tip  = "Scaled Jacobian is the ratio between the minimum and maximum "
        scaled_jacobian_tool_tip += "Jacobian determinant inside the element.\nValues close to 1 "
        scaled_jacobian_tool_tip += "indicate good shape; values ≤ 0 mean inverted or invalid elements."

        aspect_ratio_tool_tip  = "The Aspect Ratio measures how stretched a tetrahedral element is, "
        aspect_ratio_tool_tip += "defined as the ratio between the longest edge \nand the shortest edge. "
        aspect_ratio_tool_tip += "Values close to 1 indicate well-shaped elements; higher values mean the "
        aspect_ratio_tool_tip += "element is elongated or distorted.\n"

        tool_tips = [
                    gamma_tool_tip, 
                    volume_tool_tip, 
                    scaled_jacobian_tool_tip, 
                    aspect_ratio_tool_tip,
                    ]

        bad_elements = self.mesh_quality_data.get("bad_elements")
        mesh_quality_statistics = self.mesh_quality_data.get("statistics")

        for i, (key, (gmsh_label, label, color_fn)) in enumerate(param_map.items()):
            metric_label_item = QTableWidgetItem(label)
            metric_label_item.setToolTip(tool_tips[i])
            metric_label_item.setTextAlignment(Qt.AlignCenter)

            metric_statistics = mesh_quality_statistics.get(gmsh_label)
            if not metric_statistics:
                continue

            self.tableWidget_mesh_quality.setItem(i, 0, metric_label_item)

            worst_value_item = QTableWidgetItem(str(round(metric_statistics[0], 3)))
            avg_item = QTableWidgetItem(str(round(metric_statistics[1], 3)))
            stdev_item = QTableWidgetItem(str(round(metric_statistics[2], 3)))

            if bad_elements:
                bad_elements_count = QTableWidgetItem(str(len(bad_elements.get(gmsh_label))))
            else:
                bad_elements_count = QTableWidgetItem("")

            worst_value_color = color_fn(metric_statistics[0])
            worst_value_item.setForeground(QBrush(QColor(worst_value_color)))

            avg_color = color_fn(metric_statistics[1])
            avg_item.setForeground(QBrush(QColor(avg_color)))

            for j, _item in enumerate([worst_value_item, avg_item, stdev_item, bad_elements_count]):
                _item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_mesh_quality.setItem(i, j+1, _item)

        self.tableWidget_mesh_quality.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_mesh_quality.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        if any(bad_elements.values()):
            self.tabWidget_main.tabBar().setTabTextColor(2, QColor("orange"))

        if self.tableWidget_mesh_quality.rowCount() > 0:
            self.tableWidget_mesh_quality.setCurrentCell(0, 0)

    def mesh_quality_item_clicked(self, item):
        if not self.is_mesh_quality_computed():
            self.pushButton_show_bad_elements.setEnabled(False)
            return

        bad_elements_data = self.mesh_quality_data.get("bad_elements")
        selected_parameter = self.mesh_quality_parameters.get(item.row())
        bad_elements = bad_elements_data[selected_parameter]

        self.pushButton_show_bad_elements.setEnabled(bool(bad_elements))
        self.pushButton_plot_histogram.setEnabled(True)

    def plot_mesh_parameter_histogram(self):
        if not self.is_mesh_quality_computed():
            return

        current_index = self.tableWidget_mesh_quality.currentIndex().row()
        selected_parameter = self.mesh_quality_parameters.get(current_index)

        histograms_data = self.mesh_quality_data.get("histograms_data")
        hist, bin_edges, percentile_5, percentile_95 = histograms_data[selected_parameter]

        bin_edges = np.array(bin_edges)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_min = self.mesh.quality_bins[selected_parameter][1]
        bin_max = self.mesh.quality_bins[selected_parameter][0]
        bin_med = (bin_min + bin_max) / 2

        if selected_parameter == "aspectRatio":
            cmap = mcolors.LinearSegmentedColormap.from_list(
                "qualidade", [(0, "green"), (bin_med / bin_max, "gold"), (1, "red")]
            )
        else:
            cmap = mcolors.LinearSegmentedColormap.from_list(
                "qualidade", [(0, "red"), (bin_med, "gold"), (1, "green")]
            )
        norm = mcolors.Normalize(vmin=min(bin_centers), vmax=max(bin_centers))
        colors = cmap(norm(bin_centers))

        fig = Figure(figsize=(10, 5))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        for i in range(len(hist)):
            ax.bar(
                bin_edges[i],
                hist[i],
                width=bin_edges[i + 1] - bin_edges[i],
                align="edge",
                color=colors[i],
                edgecolor="black",
                alpha=0.9,
            )

        ax.axvline(
            percentile_5,
            color="grey",
            linestyle="--",
            linewidth=2,
            label="5% percentile",
        )
        ax.axvline(
            percentile_95,
            color="black",
            linestyle="--",
            linewidth=2,
            label="95% percentile",
        )

        ax.legend()

        title = {
            "gamma": "Gamma",
            "volume": "Volume",
            "minSJ": "Scaled Jacobian",
            "aspectRatio": "Aspect Ratio",
        }

        ax.set_title(f"{title[selected_parameter]} histogram")
        ax.set_xlabel("Parameter value")
        ax.set_ylabel("Number of elements")
        ax.grid(True, linestyle=":", alpha=0.5)
        fig.tight_layout()

        # Insere no layout
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        plot_ui = MeshQualityHistogramPlot_UI()
        plot_ui.widget_plot.setLayout(layout)

        canvas.draw()
        plot_ui.setWindowTitle("Mesh quality histogram plotter")
        plot_ui.setWindowFlag(Qt.WindowStaysOnTopHint)
        plot_ui.setWindowIcon(app().main_window.vibra_icon)
        plot_ui.exec_()

    def show_bad_elements(self):

        if not self.is_mesh_quality_computed():
            return

        current_index = self.tableWidget_mesh_quality.currentIndex().row()
        selected_parameter = self.mesh_quality_parameters.get(current_index)

        bad_elements_data = self.mesh_quality_data.get("bad_elements", dict())
        if not bad_elements_data:
            return
    
        mesh_bad_elements = bad_elements_data[selected_parameter]
        if not mesh_bad_elements:
            return

        app().main_window.distinguish_mesh_solids(mesh_bad_elements)
        self.bad_elements_showed = True

    def check_unprocessed_mesh_refining(self):

        if self.cache_mesh_refinement_data == self.mesh_refinement_data:
            return

        self.hide()

        title = "Unprocessed mesh refinement"    
        message = "The mesh refinement configuration has been modified, but the mesh itself "
        message += "has not been processed. Would you like to generate the new mesh?"

        buttons_config = {
                        "left_button_label": "No", 
                        "right_button_label": "Generate",
                        }

        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config, window_title="Vibra")
        if read._cancel:
            return True

        if not read._continue:
            return True

        self.generate_mesh_callback()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.generate_mesh_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0):
        self.keep_window_open = False
        self.check_unprocessed_mesh_refining()

        if self.bad_elements_showed:
            app().main_window.distinguish_mesh_solids([])

        return super().closeEvent(a0)