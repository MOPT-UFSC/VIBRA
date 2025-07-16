import logging
from collections import defaultdict

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem

from vibra import app
from vibra.engine.mesher import gmsh_constants
from vibra.engine.mesher.element_type import (
    HEXAHEDRON_8,
    HEXAHEDRON_20,
    TETRAHEDRON_4,
    TETRAHEDRON_10,
    ElementType,
)
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.ui_generated.mesh.mesher_setup_ui import MesherSetup_UI

window_title_1 = "Error"
window_title_2 = "Warning"


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


class MeshSetupInputs(MesherSetup_UI):
    def __init__(self, **kwargs):
        super().__init__()

        self.close_after_generate = kwargs.get("close_after_generate", False)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self._config_window()
        self._initialize()
        self._create_connections()
        self._config_widgets()
        self.update_gmsh_controls()
        self._load_current_mesh_setup()
        self.config_control_quality_table()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.complete = False
        self.keep_window_open = True
        self.mesh_refinement_data = defaultdict(list)

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.main_window.vibra_icon)
        self.setWindowTitle("Mesher setup")

    def _config_widgets(self):
        self.lineEdit_selected_ids.setDisabled(True)
        self.comboBox_2d_algorithm.setDisabled(True)
        self.comboBox_2d_algorithm.setDisabled(True)
        self.comboBox_recombination_algorithm.setDisabled(True)
        self.comboBox_subdivision_algorithm.setDisabled(True)
        self.comboBox_second_order_incomplete.setDisabled(True)
        self.comboBox_recombine_all.setDisabled(True)

        widths = [160, 160]
        for i, width in enumerate(widths):
            self.tableWidget_refining_mesh_data.setColumnWidth(i, width)
            self.tableWidget_refining_mesh_data.horizontalHeaderItem(
                i
            ).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_refining_mesh_data.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior(1)
        )
        self.tableWidget_refining_mesh_data.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode(0)
        )
        self.tableWidget_refining_mesh_data.horizontalHeader().setStretchLastSection(
            True
        )

    def _create_connections(self):
        #
        self.comboBox_shape_function.currentIndexChanged.connect(
            self.update_gmsh_controls
        )
        self.comboBox_element_type.currentIndexChanged.connect(
            self.update_gmsh_controls
        )
        #
        self.pushButton_add.clicked.connect(self.add_button_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_delete.clicked.connect(self.remove_callback)
        self.pushButton_generate_mesh.clicked.connect(self.generate_mesh_callback)
        self.pushButton_show_bad_elements.clicked.connect(self.show_bad_elements)
        self.pushButton_plot_histogram.clicked.connect(
            self.plot_mesh_parameter_histogram
        )
        #
        self.tableWidget_refining_mesh_data.itemClicked.connect(
            self.item_clicked_callback
        )
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)

    def geometry_selection_callback(self):
        faces = self.main_window.selected_geometry_surfaces
        volumes = self.main_window.selected_geometry_volumes

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
        if self.lineEdit_selected_ids.text() == "":
            return list()

        selected_ids = list()

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

            self.update_table_data()

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
                    self.update_table_data()

            app().main_window.set_geometry_selection()

        except Exception:
            return

    def _load_initial_element_size(self):
        element_size = app().project.model.initial_element_size
        if element_size is not None:
            self.doubleSpinBox_maximum_element_size.setValue(element_size)

    def _load_current_mesh_setup(self):
        mesh_setup = app().project.model.mesh_setup

        if mesh_setup is None:
            self._load_initial_element_size()
            return

        if isinstance(mesh_setup, dict):
            try:
                element_type = mesh_setup["element_type"]
                geometry_tolerance = mesh_setup["geometry_tolerance"]
                minimum_element_size = mesh_setup["minimum_element_size"]
                maximum_element_size = mesh_setup["maximum_element_size"]
                size_factor = minimum_element_size / maximum_element_size
                mesh_refinement_parameters = mesh_setup["mesh_refinement_parameters"]
                mesh_connection = mesh_setup["mesh_connection"]

                gmsh_algorithm_3d = mesh_setup.get("algorithm_3d")
                if gmsh_algorithm_3d is not None:
                    self.comboBox_3d_algorithm.setCurrentIndex(
                        map_algorithms_3d[gmsh_algorithm_3d]
                    )

                self.update_element_type(element_type)

                self.doubleSpinBox_maximum_element_size.setValue(maximum_element_size)
                self.doubleSpinBox_minimum_element_size_factor.setValue(size_factor)
                self.lineEdit_geometry_tolerance.setText(str(geometry_tolerance))
                self.checkBox_mesh_connection.setChecked(mesh_connection)

                for selection_type, e_size, selected_ids in mesh_refinement_parameters:
                    self.mesh_refinement_data[(selection_type, e_size)].extend(
                        selected_ids
                    )

                self.update_table_data()

            except Exception as error_log:
                self.hide()
                title = "Error while loading mesh setup"
                message = str(error_log)
                PrintMessageInput([window_title_1, title, message])

    def update_table_data(self):
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
            PrintMessageInput([window_title_1, title, message])

    def update_element_type(self, element_type):
        if element_type == TETRAHEDRON_4:
            self.comboBox_element_type.setCurrentIndex(0)
            self.comboBox_shape_function.setCurrentIndex(0)

        elif element_type == TETRAHEDRON_10:
            self.comboBox_element_type.setCurrentIndex(0)
            self.comboBox_shape_function.setCurrentIndex(1)

        elif element_type == HEXAHEDRON_8:
            self.comboBox_element_type.setCurrentIndex(1)
            self.comboBox_shape_function.setCurrentIndex(0)

        elif element_type == HEXAHEDRON_20:
            self.comboBox_element_type.setCurrentIndex(1)
            self.comboBox_shape_function.setCurrentIndex(1)

        else:
            NotImplementedError()

    def generate_mesh_callback(self):
        if self.check_mesh_inputs():
            return

        self.main_window.clear_selection()

        self.hide()

        def generate_function():
            logging.info("Processing mesh... [20/100]")
            app().project.reset_solutions()

            logging.info("Processing mesh... [30/100]")
            app().project.set_mesh_setup(self.mesh_setup)
            app().file.write_mesh_setup_in_file(self.file_mesh_setup)

            logging.info("Processing mesh... [40/100]")
            app().project.generate_mesh()

        LoadingWindow(generate_function).run()

        self.process_degress_of_freedom_if_necessary()

        app().file.write_mesh_data_in_file()
        app().file.write_geometry_data_in_file()
        app().main_window.update_mesh_information()
        app().main_window.update_geometry_information()

        self.config_control_quality_table()

        LoadingWindow(self.actions_to_finalize).run()
        self.complete = True

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
        # self.worst_value = app().project.model.mesh.mesh_quality_worst_value

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
        min_factor = self.doubleSpinBox_minimum_element_size_factor.value()

        lineEdit = self.lineEdit_geometry_tolerance
        geometry_tolerance = self.check_inputs(lineEdit, "Geometry tolerance")
        if self.stop:
            lineEdit.setFocus()
            return True

        solid_element = self.get_element_type()
        if solid_element is None:
            return True

        alg3d_index = self.comboBox_3d_algorithm.currentIndex()
        solid_element.algorithm_3d = gmsh_algorithms_3d[alg3d_index]

        connected_mesh = self.checkBox_mesh_connection.isChecked()
        self.mesh_setup = {
            "element_type": solid_element,
            "geometry_tolerance": geometry_tolerance,
            "size_factor": 0,
            "minimum_element_size": min_factor * maximum_element_size,
            "maximum_element_size": maximum_element_size,
            "mesh_refinement_parameters": self.get_mesh_refinement_data(),
            "mesh_connection": connected_mesh,
        }

        self.file_mesh_setup = {
            "element_type": self.comboBox_element_type.currentText().lower(),
            "shape_function": self.comboBox_shape_function.currentText().lower(),
            "geometry_tolerance": geometry_tolerance,
            "size_factor": 0,
            "minimum_element_size": min_factor * maximum_element_size,
            "maximum_element_size": maximum_element_size,
            "algorithm_3d": solid_element.algorithm_3d,
            "mesh_refinement_parameters": self.get_mesh_refinement_data(),
            "mesh_connection": connected_mesh,
        }

    def get_element_type(self) -> ElementType:
        _element_type = self.comboBox_element_type.currentText().lower()
        _shape_function = self.comboBox_shape_function.currentText().lower()

        if _element_type == "tetrahedral" and _shape_function == "linear":
            return TETRAHEDRON_4
        elif _element_type == "tetrahedral" and _shape_function == "quadratic":
            return TETRAHEDRON_10
        elif _element_type == "hexahedral" and _shape_function == "linear":
            return HEXAHEDRON_8
        elif _element_type == "hexahedral" and _shape_function == "quadratic":
            return HEXAHEDRON_20
        else:
            return None
            # raise NotImplementedError(f"Element type not defined!")

    def config_control_quality_table(self):
        mesh_statistics = app().project.model.mesh.mesh_quality_statistics

        if not mesh_statistics.all():
            return

        worst_values = mesh_statistics[:, 0]
        avgs = mesh_statistics[:, 1]
        stdevs = mesh_statistics[:, 2]

        self.quality_bins = {
            "gamma": (0.7, 0.2),
            "volume": (1e-5, 0),
            "minSJ": (0.3, 0.1),
            "aspectRatio": (4, 1.5),
        }
        param_map = {
            0: (
                "Gamma",
                lambda v: "green"
                if v > self.quality_bins["gamma"][0]
                else "yellow"
                if v > self.quality_bins["gamma"][1]
                else "red",
            ),
            1: (
                "Volume",
                lambda v: "green"
                if v > self.quality_bins["volume"][0]
                else "yellow"
                if v > self.quality_bins["volume"][1]
                else "red",
            ),
            2: (
                "Scaled Jacobian",
                lambda v: "green"
                if v > self.quality_bins["minSJ"][0]
                else "yellow"
                if v > self.quality_bins["minSJ"][1]
                else "red",
            ),
            3: (
                "Aspect Ratio",
                lambda v: "green"
                if v < self.quality_bins["aspectRatio"][0]
                else "yellow"
                if v < self.quality_bins["aspectRatio"][1]
                else "red",
            ),
        }
        self.tableWidget_mesh_quality.setRowCount(len(param_map))
        self.tableWidget_mesh_quality.horizontalHeader().resizeSection(0, 150)

        for i, (key, (label, color_fn)) in enumerate(param_map.items()):
            self.tableWidget_mesh_quality.setItem(i, 0, QTableWidgetItem(label))

            worst_value_item = QTableWidgetItem(str(round(worst_values[key], 3)))
            avg_item = QTableWidgetItem(str(round(avgs[key], 3)))
            stdev_item = QTableWidgetItem(str(round(stdevs[key], 3)))

            worst_value_color = color_fn(worst_values[key])
            worst_value_item.setForeground(QBrush(QColor(worst_value_color)))

            avg_color = color_fn(avgs[key])
            avg_item.setForeground(QBrush(QColor(avg_color)))

            self.tableWidget_mesh_quality.setItem(i, 1, worst_value_item)
            self.tableWidget_mesh_quality.setItem(i, 2, avg_item)
            self.tableWidget_mesh_quality.setItem(i, 3, stdev_item)

        if self.tableWidget_mesh_quality.rowCount() > 0:
            self.tableWidget_mesh_quality.setCurrentCell(0, 0)

    def plot_mesh_parameter_histogram(self):
        parameter_idx = self.tableWidget_mesh_quality.currentIndex().row()
        parameter = {
            0: "gamma",
            1: "volume",
            2: "minSJ",
            3: "aspectRatio",
        }
        mesh_quality_vals = app().project.model.mesh.mesh_quality[parameter_idx, :][
            "val"
        ]

        bins = np.linspace(min(mesh_quality_vals), max(mesh_quality_vals), 30)
        hist, bin_edges = np.histogram(mesh_quality_vals, bins=bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_min = self.quality_bins[parameter[parameter_idx]][1]
        bin_max = self.quality_bins[parameter[parameter_idx]][0]
        bin_med = (bin_min + bin_max) / 2

        if parameter[parameter_idx] == "aspectRatio":
            cmap = mcolors.LinearSegmentedColormap.from_list(
                "qualidade", [(0, "green"), (bin_med, "gold"), (1, "red")]
            )

        else:
            cmap = mcolors.LinearSegmentedColormap.from_list(
                "qualidade", [(0, "red"), (bin_med, "gold"), (1, "green")]
            )
            norm = mcolors.Normalize(vmin=min(bin_centers), vmax=max(bin_centers))
            colors = cmap(norm(bin_centers))

        plt.figure(figsize=(10, 5))
        for i in range(len(hist)):
            plt.bar(
                bin_edges[i],
                hist[i],
                width=bin_edges[i + 1] - bin_edges[i],
                align="edge",
                color=colors[i],
                edgecolor="black",
                alpha=0.9,
            )

        percentile_5 = np.percentile(mesh_quality_vals, 5)
        percentile_95 = np.percentile(mesh_quality_vals, 95)
        plt.axvline(
            percentile_5,
            color="grey",
            linestyle="--",
            linewidth=2,
            label="5% percentile",
        )
        plt.axvline(
            percentile_95,
            color="black",
            linestyle="--",
            linewidth=2,
            label="95% percentile",
        )
        plt.legend()

        title = {
            "gamma": "Gamma",
            "volume": "Volume",
            "minSJ": "Scaled Jacobian",
            "aspectRatio": "Aspect Ratio",
        }

        plt.title(f"{title[parameter[parameter_idx]]} histogram")
        plt.xlabel("Parameter value")
        plt.ylabel("Number of elements")
        plt.tight_layout()
        plt.grid(True, linestyle=":", alpha=0.5)
        plt.show()

    def show_bad_elements(self):
        parameter_idx = self.tableWidget_mesh_quality.currentIndex().row()
        parameter = {
            0: "gamma",
            1: "volume",
            2: "minSJ",
            3: "aspectRatio",
        }
        mesh_quality = app().project.model.mesh.mesh_quality[parameter_idx]
        bad_elements = []

        for element, quality in mesh_quality:
            if parameter[parameter_idx] == "aspectRatio":
                if quality > self.quality_bins[parameter[parameter_idx]][0]:
                    bad_elements.append(element)
            elif quality < self.quality_bins[parameter[parameter_idx]][1]:
                bad_elements.append(element)

        if not bad_elements:
            PrintMessageInput(
                [
                    "Warning",
                    "No elements to plot",
                    "There are no elements that compromise the mesh according to this parameter.",
                ]
            )

        app().main_window.distinguish_mesh_solids(bad_elements)

    def update_gmsh_controls(self):
        element_type = self.get_element_type()
        if element_type is None:
            return

        self.comboBox_2d_algorithm.setCurrentIndex(
            map_algorithms_2d[element_type.algorithm_2d]
        )
        self.comboBox_3d_algorithm.setCurrentIndex(
            map_algorithms_3d[element_type.algorithm_3d]
        )

        self.comboBox_recombination_algorithm.setCurrentIndex(
            element_type.recombination_algorithm
        )
        self.comboBox_subdivision_algorithm.setCurrentIndex(
            element_type.subdivision_algorithm
        )
        self.comboBox_recombine_all.setCurrentIndex(int(element_type.recombine_all))
        self.comboBox_second_order_incomplete.setCurrentIndex(
            int(element_type.second_order_incomplete)
        )

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
                    else:
                        if out <= 0:
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
            PrintMessageInput([window_title_1, title, message])
            self.stop = True
            return None
        return out

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.generate_mesh_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0):
        app().main_window.distinguish_mesh_solids([])
        self.keep_window_open = False
        return super().closeEvent(a0)


# fmt: on
