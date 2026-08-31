import logging
from copy import deepcopy
from enum import IntEnum

import matplotlib.colors as mcolors
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from molde.colors import Color, color_names
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QKeyEvent
from PySide6.QtWidgets import QDoubleSpinBox, QTableWidgetItem, QVBoxLayout

from vibra import app
from vibra.engine.mesher import gmsh_constants
from vibra.engine.mesher.element_setup import (
    GMSH_HEX8,
    GMSH_HEX20,
    GMSH_TET4,
    GMSH_TET10,
    ElementSetup,
    MeshAlgorithms2D,
    MeshAlgorithms3D,
    SubdivisionAlgorithms,
)
from vibra.engine.mesher.mesh_setup import LocalMeshSizeControlSetup, MeshSetup
from vibra.errors import InvalidMeshSetupError
from vibra.interface import error_title
from vibra.interface.formatters.icons import Icon
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.ui_generated.model.general.mesher_setup_inputs_ui import MesherSetupInputs_UI
from vibra.interface.ui_generated.plots.general.mesh_quality_histogram_plot_ui import MeshQualityHistogramPlot_UI
from vibra.utils.interface_utils import block_signals
from vibra.utils.subprocess.subprocess_handler import SubProcessHandler, SubProcessStatus


class GMSHAlgorithms_3D(IntEnum):
    DELAUNAY_3D = 0
    FRONTAL_3D = 1
    HXT_3D = 2


class GMSHAlgorithms_2D(IntEnum):
    MESH_ADAPT_2D = 0
    AUTOMATIC_2D = 1
    INITIAL_MESH_ONLY_2D = 2
    DELAUNAY_2D = 3
    FRONTAL_DELAUNAY_2D = 4
    QUASI_STRUCTURED_QUADS_2D = 5


class QualityTableRows(IntEnum):
    GAMMA = 0
    VOLUME = 1
    MIN_SJ = 2
    ASPECT_RATIO = 3


class QualityTableColumns(IntEnum):
    WORST_VALUE = 0
    AVERAGE = 1
    STANDARD_DEVIATION = 2
    BAD_ELEMENTS = 3


class LocalMeshSizeControlTableColumns(IntEnum):
    ELEMENT_SIZE = 0
    SELECTION_TYPE = 1
    SELECTION_IDS = 2


class MeshSetupTabs(IntEnum):
    GLOBAL_SETTINGS = 0
    LOCAL_MESH_SIZE_CONTROL = 1
    ADVANCED_CONTROLS = 2
    INTERFACE_DISCONNECTION = 3
    MESH_QUALITY = 4


class MesherSetupInputs(MesherSetupInputs_UI):
    def __init__(
        self,
        close_after_generate: bool = False,
        start_on_disconnection_tab: bool = False,
        force_merge_nodes: bool = False,
        **kwargs,
    ):
        super().__init__()

        self.close_after_generate = close_after_generate
        self.start_on_disconnection_tab = start_on_disconnection_tab
        self.force_merge_nodes = force_merge_nodes

        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._create_connections()
        self._config_widgets()
        self._load_current_mesh_setup()
        self.update_combo_boxes_according_to_geometry_info()

        if self.force_merge_nodes:
            self.comboBox_volumes_interface_behavior.setCurrentIndex(1)
        if self.start_on_disconnection_tab:
            self.tabWidget_main.setCurrentIndex(MeshSetupTabs.INTERFACE_DISCONNECTION)

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.complete = False

        self.keep_window_open = True
        self.bad_elements_showed = False
        self.synchronize_sizes = False
        self.tmp_local_mesh_size_control_parameters: list[LocalMeshSizeControlSetup] = []
        self.tmp_disconnected_surfaces: set[int] = set()
        self.last_synced_ids: set[int] = set()
        self.last_synced_disconnected_surfaces: set[int] = set()

        self.gmsh_labels = {
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

    def _create_connections(self):
        #
        self.comboBox_element_geometry.currentIndexChanged.connect(self.element_topology_changed_callback)
        self.comboBox_element_order.currentIndexChanged.connect(self.element_topology_changed_callback)
        #
        self.comboBox_volumes_interface_behavior.currentIndexChanged.connect(self.volumes_interface_behavior_changed_callback)
        #
        self.doubleSpinBox_maximum_element_size.valueChanged.connect(self.maximum_element_size_changed_callback)
        #
        self.pushButton_add.clicked.connect(self.add_button_callback)
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_delete.clicked.connect(self.remove_callback)
        self.pushButton_plot_histogram.clicked.connect(self.plot_mesh_parameter_histogram)
        self.pushButton_show_bad_elements.clicked.connect(self.plot_bad_elements)
        self.pushButton_syncrhonize.clicked.connect(self.synchronize_button_callback)
        self.pushButton_add_disconnected_surface.clicked.connect(self.add_disconnected_surface_callback)
        self.pushButton_delete_disconnected_surface.clicked.connect(self.delete_disconnected_surface_callback)
        # #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        # #
        self.tableWidget_local_mesh_size_control_data.itemClicked.connect(self.local_mesh_size_control_item_clicked_callback)
        self.tableWidget_mesh_quality.itemClicked.connect(self.mesh_quality_item_clicked_callback)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

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
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply_and_close.setAutoDefault(False)
        #
        self.pushButton_plot_histogram.setDisabled(True)
        #
        self.doubleSpinBox_maximum_element_size.setKeyboardTracking(False)
        self.doubleSpinBox_minimum_element_size.setKeyboardTracking(False)

        minimum_spinbox = self.doubleSpinBox_minimum_element_size
        maximum_spinbox = self.doubleSpinBox_maximum_element_size

        def step_by(spinbox, steps):
            if steps > 0:
                value = spinbox.value()
                step = spinbox.singleStep()
                maximum = maximum_spinbox.value()
                if value >= maximum:
                    return
                if value + step * steps > maximum:
                    with block_signals(spinbox):
                        spinbox.setValue(maximum)
                    return
            QDoubleSpinBox.stepBy(spinbox, steps)

        minimum_spinbox.stepBy = step_by.__get__(minimum_spinbox)

    def _load_current_mesh_setup(self):
        mesh_setup = app().project.model.mesh_setup
        if mesh_setup is None:
            self._load_initial_element_size()
            self._show_quality_table(False)
            return

        self.tmp_local_mesh_size_control_parameters = deepcopy(mesh_setup.local_mesh_size_control_parameters)
        self.update_interface_controls(mesh_setup.element_setup)

        self.doubleSpinBox_maximum_element_size.setValue(mesh_setup.maximum_element_size)
        self.doubleSpinBox_minimum_element_size.setValue(mesh_setup.minimum_element_size)
        self.doubleSpinBox_size_factor.setValue(mesh_setup.size_factor)
        self.lineEdit_geometry_tolerance.setText(str(mesh_setup.geometry_tolerance))
        self.comboBox_volumes_interface_behavior.setCurrentIndex(int(mesh_setup.merge_connected_volumes))
        self.comboBox_mesh_quality_metrics.setCurrentIndex(int(mesh_setup.compute_quality_metrics))

        self.tmp_disconnected_surfaces = set(mesh_setup.disconnected_surfaces)
        self.update_disconnected_surfaces_table()
        self.volumes_interface_behavior_changed_callback()

        self.update_local_mesh_size_control_table()
        self.update_mesh_quality_table()

    def _load_initial_element_size(self):
        element_size = app().project.model.initial_element_size
        if element_size is not None:
            self.doubleSpinBox_maximum_element_size.setValue(element_size)
            self.doubleSpinBox_minimum_element_size.setValue(int(0.9 * element_size))

    def maximum_element_size_changed_callback(self):
        if self.synchronize_sizes:
            with block_signals(self.doubleSpinBox_minimum_element_size):
                self.doubleSpinBox_minimum_element_size.setValue(self.doubleSpinBox_maximum_element_size.value())

        self.update_local_mesh_size_control_table()

    def synchronize_button_callback(self):
        self.synchronize_sizes = not self.synchronize_sizes
        if self.synchronize_sizes:
            icon = Icon(":/icons/sync_disabled.png")
            tool_tip = "Desynchronize the minimum and maximum sizes"
        else:
            icon = Icon(":/icons/sync_enabled.png")
            tool_tip = "Synchronize the minimum and maximum sizes"

        self.doubleSpinBox_minimum_element_size.setDisabled(self.synchronize_sizes)
        self.pushButton_syncrhonize.setIcon(icon)
        self.pushButton_syncrhonize.setToolTip(tool_tip)
        self.maximum_element_size_changed_callback()

    def geometry_selection_callback(self):
        volumes = app().main_window.selection.geometry_volumes
        surfaces = app().main_window.selection.geometry_surfaces

        if volumes:
            self.comboBox_local_mesh_size_control_entity_type.setCurrentText("Volumes")
            selection = set(volumes)
        elif surfaces:
            self.comboBox_local_mesh_size_control_entity_type.setCurrentText("Surfaces")
            selection = set(surfaces)
        else:
            self.lineEdit_selected_ids.setText("")
            self.last_synced_ids = set()
            return

        if self.tabWidget_main.currentIndex() == MeshSetupTabs.INTERFACE_DISCONNECTION:
            self.lineEdit_disconnected_surface_id.setText(
                ", ".join(str(i) for i in sorted(selection))
            )
            self.last_synced_disconnected_surfaces = set(selection)
            return

        current_ids = set(self.get_selected_ids())
        manually_edited = current_ids != self.last_synced_ids

        if manually_edited:
            merged_ids = selection | current_ids
            self.last_synced_ids = set(merged_ids)
        else:
            merged_ids = selection
            self.last_synced_ids = set(selection)

        text = ", ".join(str(i) for i in sorted(merged_ids))
        self.lineEdit_selected_ids.setText(text)

    def get_selected_entity_type(self) -> str:
        volumes_selection = self.comboBox_local_mesh_size_control_entity_type.currentText() == "Volumes"
        return "volumes" if volumes_selection else "surfaces"

    def tab_event_callback(self):
        mesh_quality_tab = self.tabWidget_main.currentIndex() == MeshSetupTabs.MESH_QUALITY
        self.pushButton_apply.setDisabled(mesh_quality_tab)
        self.pushButton_apply_and_close.setDisabled(mesh_quality_tab)

        if self.tabWidget_main.currentIndex() == MeshSetupTabs.INTERFACE_DISCONNECTION:
            self._sync_disconnected_surface_line_edit()

    def _sync_disconnected_surface_line_edit(self):
        current_ids = self.get_disconnected_surface_selected_ids()
        manually_edited = current_ids != self.last_synced_disconnected_surfaces
        if manually_edited:
            merged_ids = current_ids | self.tmp_disconnected_surfaces
            self.tmp_disconnected_surfaces = set(merged_ids)
        self.lineEdit_disconnected_surface_id.setText(
            ", ".join(str(i) for i in sorted(self.tmp_disconnected_surfaces))
        )
        self.last_synced_disconnected_surfaces = set(self.tmp_disconnected_surfaces)
        self.update_disconnected_surfaces_table()

    def get_disconnected_surface_selected_ids(self) -> set[int]:
        text = self.lineEdit_disconnected_surface_id.text().strip()
        if text == "":
            return set()
        try:
            return {int(_id) for _id in text.split(",") if _id.strip() != ""}
        except ValueError:
            return self.last_synced_disconnected_surfaces

    def volumes_interface_behavior_changed_callback(self):
        merge_nodes = self.comboBox_volumes_interface_behavior.currentText() == "Merge nodes"
        self.tabWidget_main.setTabEnabled(MeshSetupTabs.INTERFACE_DISCONNECTION, merge_nodes)
        if not merge_nodes:
            self.tmp_disconnected_surfaces = set()
            self.last_synced_disconnected_surfaces = set()
            self.lineEdit_disconnected_surface_id.setText("")
            self.update_disconnected_surfaces_table()

    def add_disconnected_surface_callback(self):
        selected_ids = self.get_disconnected_surface_selected_ids()
        if not selected_ids:
            return

        surface_to_volume = self._get_surface_to_volume_mapping()
        invalid_ids = {
            _id
            for _id in selected_ids
            if len(surface_to_volume.get(_id, [])) < 2
        }
        if invalid_ids:
            message = (
                "The following surface(s) are not shared by at least two volumes, "
                "so they cannot be disconnected: "
                + ", ".join(str(_id) for _id in sorted(invalid_ids))
                + "."
            )
            self.hide()
            PrintMessageInput(["Warning", "Invalid disconnected surfaces", message])
            self.show()
            self.tmp_disconnected_surfaces |= set(selected_ids) - invalid_ids
        else:
            self.tmp_disconnected_surfaces |= set(selected_ids)

        self.lineEdit_disconnected_surface_id.setText("")
        self.last_synced_disconnected_surfaces = set(self.tmp_disconnected_surfaces)
        self.update_disconnected_surfaces_table()

    def delete_disconnected_surface_callback(self):
        selected_rows = {
            item.row() for item in self.tableWidget_disconnected_surfaces_data.selectedItems()
        }
        if not selected_rows:
            return

        surfaces_to_delete = set()
        for row in selected_rows:
            str_surface_id = self.tableWidget_disconnected_surfaces_data.item(row, 0).text()
            if str_surface_id != "":
                surfaces_to_delete.add(int(str_surface_id))

        self.tmp_disconnected_surfaces -= surfaces_to_delete
        self.lineEdit_disconnected_surface_id.setText("")
        self.last_synced_disconnected_surfaces = set(self.tmp_disconnected_surfaces)
        self.update_disconnected_surfaces_table()

    def _get_surface_to_volume_mapping(self) -> dict[int, list[int]]:
        surface_to_volume = {}
        mesh = app().project.model.mesh
        volumes_from_surface = getattr(mesh, "volumes_from_surface", None) if mesh is not None else None
        if volumes_from_surface is not None:
            surfaces_mapping = getattr(mesh, "surfaces_mapping", None) or {}
            for surface_id, volumes in volumes_from_surface.items():
                if isinstance(volumes, list):
                    adjacent_volumes = list(volumes)
                else:
                    adjacent_volumes = list(volumes.keys())

                twin_surface_id = surfaces_mapping.get(surface_id)
                if twin_surface_id is not None:
                    twin_volumes = volumes_from_surface.get(twin_surface_id)
                    if isinstance(twin_volumes, list):
                        twin_volume_ids = list(twin_volumes)
                    elif twin_volumes is not None:
                        twin_volume_ids = list(twin_volumes.keys())
                    else:
                        twin_volume_ids = []
                    adjacent_volumes.extend(v for v in twin_volume_ids if v not in adjacent_volumes)

                surface_to_volume[surface_id] = adjacent_volumes
        return surface_to_volume

    def update_disconnected_surfaces_table(self):
        surface_to_volume = self._get_surface_to_volume_mapping()
        self.tableWidget_disconnected_surfaces_data.setRowCount(len(self.tmp_disconnected_surfaces))
        self.tableWidget_disconnected_surfaces_data.setColumnHidden(2, True)

        for row, surface_id in enumerate(sorted(self.tmp_disconnected_surfaces)):
            adjacent_volumes = surface_to_volume.get(surface_id, [])

            item_surface_id = QTableWidgetItem(str(surface_id))
            item_adjacent_volumes = QTableWidgetItem(", ".join(str(v) for v in adjacent_volumes))
            for item in (item_surface_id, item_adjacent_volumes):
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.tableWidget_disconnected_surfaces_data.setItem(row, 0, item_surface_id)
            self.tableWidget_disconnected_surfaces_data.setItem(row, 1, item_adjacent_volumes)

    def local_mesh_size_control_item_clicked_callback(self, item: QTableWidgetItem):
        row = item.row()
        if not isinstance(row, int):
            return

        str_element_size = self.tableWidget_local_mesh_size_control_data.item(row, LocalMeshSizeControlTableColumns.ELEMENT_SIZE).text()
        selection_type = self.tableWidget_local_mesh_size_control_data.item(row, LocalMeshSizeControlTableColumns.SELECTION_TYPE).text()
        str_selected_ids = self.tableWidget_local_mesh_size_control_data.item(row, LocalMeshSizeControlTableColumns.SELECTION_IDS).text()

        if str_element_size != "":
            element_size = float(str_element_size)
            self.doubleSpinBox_local_mesh_size_control_element_size.setValue(element_size)

        selected_ids = [int(_id) for _id in str_selected_ids.split(",")]
        if not selected_ids:
            return

        if selection_type == "volumes":
            self.comboBox_local_mesh_size_control_entity_type.setCurrentText("Volumes")
            app().main_window.selection.set_geometry_selection(volumes=selected_ids)
        else:
            self.comboBox_local_mesh_size_control_entity_type.setCurrentText("Surfaces")
            app().main_window.selection.set_geometry_selection(surfaces=selected_ids)

    def get_selected_ids(self):
        if self.lineEdit_selected_ids.text() == "":
            return []

        try:
            str_selected_ids = self.lineEdit_selected_ids.text()
            selected_ids = [int(_id) for _id in str_selected_ids.split(",")]
        except Exception:
            return []

        return selected_ids

    def add_button_callback(self):
        if self.lineEdit_selected_ids.text() == "":
            return

        selected_type = self.get_selected_entity_type()
        selected_ids = self.get_selected_ids()

        if not selected_ids:
            return

        mesh = app().project.model.mesh
        if mesh is None:
            return

        _, error_data = mesh.check_selected_ids(selected_ids, selection=selected_type)
        if error_data is not None:
            PrintMessageInput(error_data)
            self.show()
            return

        controlled_size = self.doubleSpinBox_local_mesh_size_control_element_size.value()
        self.lineEdit_selected_ids.setText("")
        self.last_synced_ids = set()

        setup = LocalMeshSizeControlSetup(
            selected_type,
            controlled_size,
            selected_ids,
        )

        new_size_controls = []
        for control in self.tmp_local_mesh_size_control_parameters:
            control.remove_ids(selected_ids, selected_type)

            if not control.is_empty():
                new_size_controls.append(control)

        self.tmp_local_mesh_size_control_parameters = new_size_controls

        self.tmp_local_mesh_size_control_parameters.append(setup)
        self.update_local_mesh_size_control_table()

    def remove_callback(self):
        current_row = self.tableWidget_local_mesh_size_control_data.currentRow()
        self.tmp_local_mesh_size_control_parameters.pop(current_row)
        self.update_local_mesh_size_control_table()

    def update_interface_controls(self, element_setup: ElementSetup):

        match element_setup.element_order:
            case 1:
                self.comboBox_element_order.setCurrentText("Linear")
            case 2:
                self.comboBox_element_order.setCurrentText("Quadratic")
            case _:
                raise NotImplementedError("Invalid element order")

        match element_setup.subdivision_algorithm:
            case SubdivisionAlgorithms.NO_SUBDIVISION:
                self.comboBox_element_geometry.setCurrentText("Tetrahedral")
            case SubdivisionAlgorithms.ALL_HEXAHEDRA_SUBDIVISION:
                self.comboBox_element_geometry.setCurrentText("Hexahedral")

        match element_setup.algorithm_2d:
            case MeshAlgorithms2D.MESH_ADAPT_2D:
                self.comboBox_2d_algorithm.setCurrentIndex(GMSHAlgorithms_2D.MESH_ADAPT_2D)
            case MeshAlgorithms2D.AUTOMATIC_2D:
                self.comboBox_2d_algorithm.setCurrentIndex(GMSHAlgorithms_2D.AUTOMATIC_2D)
            case MeshAlgorithms2D.INITIAL_MESH_ONLY_2D:
                self.comboBox_2d_algorithm.setCurrentIndex(GMSHAlgorithms_2D.INITIAL_MESH_ONLY_2D)
            case MeshAlgorithms2D.DELAUNAY_2D:
                self.comboBox_2d_algorithm.setCurrentIndex(GMSHAlgorithms_2D.DELAUNAY_2D)
            case MeshAlgorithms2D.QUASI_STRUCTURED_QUADS_2D:
                self.comboBox_2d_algorithm.setCurrentIndex(GMSHAlgorithms_2D.QUASI_STRUCTURED_QUADS_2D)

        match element_setup.algorithm_3d:
            case MeshAlgorithms3D.DELAUNAY_3D:
                self.comboBox_3d_algorithm.setCurrentIndex(GMSHAlgorithms_3D.DELAUNAY_3D)
            case MeshAlgorithms3D.FRONTAL_3D:
                self.comboBox_3d_algorithm.setCurrentIndex(GMSHAlgorithms_3D.FRONTAL_3D)
            case MeshAlgorithms3D.HXT_3D:
                self.comboBox_3d_algorithm.setCurrentIndex(GMSHAlgorithms_3D.HXT_3D)

        self.update_mesh_quality_metric_buttons_accessibility()

    def _generate_in_subprocess(self) -> bool:
        mesh_setup = self._get_mesh_setup()
        app().project.configure_mesh(mesh_setup)
        app().project.write_to_working_dir()

        command = SubProcessHandler.get_executable() + ["--generate-mesh", str(app().project.working_directory)]
        status = SubProcessHandler(command).run()
        if status != SubProcessStatus.SUCCESS:
            return False

        def load_mesh_from_working_dir():
            logging.info("Loading generated mesh... [10/100]")
            app().project.model.mesh = app().project.project_reader.read_mesh()

            logging.info("Reading model properties... [65/100]")
            app().project.model.properties = app().project.project_reader.read_model_properties()

            logging.info("Updating project state... [85/100]")
            app().project.reset_solution()
            app().project.mark_project_as_modified()

        LoadingWindow(load_mesh_from_working_dir).run()

        return True

    def apply_callback(self, close_window: bool = False):
        def generate_mesh() -> bool:
            self.hide()

            if app().config.user_preferences.generate_mesh_in_subprocess:
                if not self._generate_in_subprocess():
                    return False
            else:

                def generate():
                    mesh_setup = self._get_mesh_setup()
                    app().project.generate_mesh(mesh_setup)

                LoadingWindow(generate).run()

            LoadingWindow(self.actions_to_finalize).run()

            self.update_local_mesh_size_control_table()
            self.update_mesh_quality_table()

            return True

        try:
            self.complete = generate_mesh()
        except InvalidMeshSetupError as e:
            PrintMessageInput([error_title, "Invalid mesh setup", str(e)])
            self.show()
            return

        if close_window:
            self.close()

    def update_local_mesh_size_control_table(self):
        size_control_parameters = self.tmp_local_mesh_size_control_parameters
        number_of_rows = len(size_control_parameters)
        self.tableWidget_local_mesh_size_control_data.setRowCount(number_of_rows)

        for row, setup in enumerate(size_control_parameters):
            ids = ", ".join(str(i) for i in setup.entity_ids)

            self.tableWidget_local_mesh_size_control_data.setItem(
                row,
                LocalMeshSizeControlTableColumns.ELEMENT_SIZE,
                self._item(setup.element_size),
            )
            self.tableWidget_local_mesh_size_control_data.setItem(
                row,
                LocalMeshSizeControlTableColumns.SELECTION_TYPE,
                self._item(setup.entity_type),
            )
            self.tableWidget_local_mesh_size_control_data.setItem(
                row,
                LocalMeshSizeControlTableColumns.SELECTION_IDS,
                self._item(ids),
            )

    def update_mesh_quality_table(self):
        mesh = app().project.model.mesh

        if mesh.mesh_quality_data:
            self._show_quality_table(True)
        else:
            self._show_quality_table(False)
            return

        mesh_statistics = mesh.mesh_quality_data.get("statistics")
        if mesh_statistics is None:
            self._show_quality_table(False)
            return

        has_bad_elements = False
        for row in QualityTableRows:
            gmsh_label = self.gmsh_labels.get(row)
            smaller_is_better = row is QualityTableRows.ASPECT_RATIO

            statistics = mesh_statistics.get(gmsh_label)
            if not any(statistics):
                self._show_quality_table(False)
                return

            bad_elements = mesh.mesh_quality_data.get("bad_elements", {})
            for metric in bad_elements.values():
                broken = metric.size != 0
                has_bad_elements = has_bad_elements or broken

            worst, mean, std = statistics
            high, low = mesh.quality_bins[gmsh_label]

            for col in QualityTableColumns:
                match col:
                    case QualityTableColumns.WORST_VALUE:
                        color = self._color_fn(worst, low, high, smaller_is_better)
                        item = self._item(f"{worst:.3f}", color)

                    case QualityTableColumns.AVERAGE:
                        color = self._color_fn(mean, low, high, smaller_is_better)
                        item = self._item(f"{mean:.3f}", color)

                    case QualityTableColumns.STANDARD_DEVIATION:
                        item = self._item(f"{std:.3f}")

                    case QualityTableColumns.BAD_ELEMENTS:
                        n_bad_elements = len(bad_elements.get(gmsh_label, []))
                        item = self._item(n_bad_elements)

                    case _:
                        raise ValueError("Invalid column index")

                self.tableWidget_mesh_quality.setItem(row, col, item)

        if has_bad_elements:
            self.tabWidget_main.tabBar().setTabTextColor(MeshSetupTabs.MESH_QUALITY, color_names.RED.to_qt())
        else:
            self.tabWidget_main.tabBar().setTabTextColor(MeshSetupTabs.MESH_QUALITY, QColor())

    def _show_quality_table(self, show=True):
        self.tabWidget_main.setTabVisible(MeshSetupTabs.MESH_QUALITY, show)

    def _item(self, value: str, color: Color | None = None):
        item = QTableWidgetItem()
        item.setText(str(value))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        if color is not None:
            item.setForeground(color.to_qt())
        return item

    def _color_fn(
        self,
        value: float,
        min_value: float,
        max_value: float,
        smaller_is_better: bool = False,
    ) -> Color:
        if smaller_is_better:
            if value < min_value:
                return color_names.GREEN
            elif min_value < value < max_value:
                return color_names.YELLOW
            else:
                return color_names.RED
        else:
            if value < min_value:
                return color_names.RED
            elif min_value < value < max_value:
                return color_names.YELLOW
            else:
                return color_names.GREEN

    def _get_mesh_setup(self) -> MeshSetup:
        element_geometry = self.comboBox_element_geometry.currentText().lower()  # not great
        assert element_geometry in ("tetrahedral", "hexahedral")

        element_order = self.comboBox_element_order.currentText().lower()  # not great
        assert element_order in ("linear", "quadratic")

        try:
            geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
        except Exception as e:
            raise ValueError("Geometry tolerance must be a real positive number") from e

        if geometry_tolerance <= 0:
            raise ValueError("Geometry tolerance must be a real positive number")

        merge_connected_volumes = self.comboBox_volumes_interface_behavior.currentText() == "Merge nodes"
        compute_quality_metrics = self.comboBox_mesh_quality_metrics.currentText() == "Enabled"

        disconnected_surfaces = []
        if merge_connected_volumes:
            disconnected_surfaces = sorted(self.tmp_disconnected_surfaces)

        return MeshSetup(
            minimum_element_size=self.doubleSpinBox_minimum_element_size.value(),
            maximum_element_size=self.doubleSpinBox_maximum_element_size.value(),
            geometry_tolerance=geometry_tolerance,
            size_factor=self.doubleSpinBox_size_factor.value(),
            element_geometry=element_geometry,
            element_order=element_order,
            merge_connected_volumes=merge_connected_volumes,
            disconnected_surfaces=disconnected_surfaces,
            compute_quality_metrics=compute_quality_metrics,
            custom_element_setup=self._get_custom_element_setup(),
            local_mesh_size_control_parameters=self._get_local_mesh_size_control_parameters(),
        )

    def _get_custom_element_setup(self) -> ElementSetup:
        element_geometry = self.comboBox_element_geometry.currentText().lower()  # not great
        assert element_geometry in ("tetrahedral", "hexahedral")

        element_order = self.comboBox_element_order.currentText().lower()  # not great
        assert element_order in ("linear", "quadratic")

        custom_element_setup = None
        match element_geometry, element_order:
            case "tetrahedral", "linear":
                custom_element_setup = GMSH_TET4.copy()
            case "tetrahedral", "quadratic":
                custom_element_setup = GMSH_TET10.copy()
            case "hexahedral", "linear":
                custom_element_setup = GMSH_HEX8.copy()
            case "hexahedral", "quadratic":
                custom_element_setup = GMSH_HEX20.copy()

        assert custom_element_setup is not None
        match self.comboBox_3d_algorithm.currentIndex():
            case GMSHAlgorithms_3D.DELAUNAY_3D:
                custom_element_setup.algorithm_3d = gmsh_constants.DELAUNAY_3D
            case GMSHAlgorithms_3D.FRONTAL_3D:
                custom_element_setup.algorithm_3d = gmsh_constants.FRONTAL_3D
            case GMSHAlgorithms_3D.HXT_3D:
                custom_element_setup.algorithm_3d = gmsh_constants.HXT_3D

        return custom_element_setup

    def _get_local_mesh_size_control_parameters(self) -> list[LocalMeshSizeControlSetup]:
        return deepcopy(self.tmp_local_mesh_size_control_parameters)

    def actions_to_finalize(self):
        if self.close_after_generate:
            self.close()

        ## Temporarily highlights nodes from non-mapped 2D elements after mesh processing

        # mesh = app().project.model.mesh
        # rows = np.isin(np.unique(mesh.faces_connectivity[:, 0].flatten()), list(mesh.face_to_solid_element.keys()), invert=True)
        # elements_2d = mesh.faces_connectivity[rows, 0]
        # if elements_2d.size:
        #     mesh.collapsed_elements_data["collapsed_2d_elements"] = [int(element_id) for element_id in elements_2d]
        #     mesh.nodes_from_collapsed_elements = mesh.get_list_of_nodes_from_collapsed_elements()
        #     # app().main_window.selection.set_mesh_selection(faces=elements_2d)
        #     print(f"Difference (???): {len(mesh.faces_connectivity) - len(mesh.face_to_solid_element)} elements")

        # ##

        logging.info("Updating render... [95/100]")
        app().main_window.action_mesh_workspace_callback()
        app().main_window.update_plots()
        app().main_window.analysis_toolbar.reset_solution_action.setDisabled(True)
        app().main_window.analysis_toolbar.check_analysis_setup_callback()
        app().main_window.action_export_element_transfer_data.setDisabled(True)

    def get_element_setup(self) -> ElementSetup | None:
        element_geometry = self.comboBox_element_geometry.currentText().lower()
        element_order = self.comboBox_element_order.currentText().lower()

        if element_geometry == "tetrahedral" and element_order == "linear":
            return GMSH_TET4
        elif element_geometry == "tetrahedral" and element_order == "quadratic":
            return GMSH_TET10
        elif element_geometry == "hexahedral" and element_order == "linear":
            return GMSH_HEX8
        elif element_geometry == "hexahedral" and element_order == "quadratic":
            return GMSH_HEX20
        else:
            return None
            # raise NotImplementedError(f"Element type not defined!")

    def update_combo_boxes_according_to_geometry_info(self):
        mesh = app().project.model.mesh
        if mesh is None:
            return

        if not mesh.are_there_volumes_in_geometry():
            self.comboBox_element_geometry.removeItem(1)
            self.comboBox_element_order.removeItem(1)

    def element_topology_changed_callback(self):
        element_setup = self.get_element_setup()
        self.update_interface_controls(element_setup)

    def update_mesh_quality_metric_buttons_accessibility(self):
        volume_exists = app().project.model.mesh.are_there_volumes_in_geometry()
        is_tetrahedral = self.comboBox_element_geometry.currentText() == "Tetrahedral"
        enable_mesh_metrics = volume_exists and is_tetrahedral
        self.comboBox_mesh_quality_metrics.setEnabled(enable_mesh_metrics)

        if not is_tetrahedral:
            self.comboBox_mesh_quality_metrics.setCurrentText("Disabled")

    def mesh_quality_item_clicked_callback(self, item):
        self.pushButton_show_bad_elements.setEnabled(False)

        mesh = app().project.model.mesh
        if mesh is None:
            return

        if not mesh.mesh_quality_data:
            return

        bad_elements_data = mesh.mesh_quality_data.get("bad_elements")
        if not bad_elements_data:
            return

        gmsh_label = self.gmsh_labels.get(item.row())
        if not gmsh_label:
            return

        bad_elements = bad_elements_data.get(gmsh_label)
        self.pushButton_show_bad_elements.setEnabled(bad_elements.size > 0)
        self.pushButton_plot_histogram.setEnabled(True)

    def plot_mesh_parameter_histogram(self):
        mesh = app().project.model.mesh
        if mesh is None:
            return

        if not mesh.mesh_quality_data:
            return

        current_index = self.tableWidget_mesh_quality.currentIndex().row()
        gmsh_label = self.gmsh_labels.get(current_index)

        histograms_data = mesh.mesh_quality_data.get("histograms_data")
        hist, bin_edges, percentile_5, percentile_95 = histograms_data[gmsh_label]

        bin_edges = np.array(bin_edges)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_min = mesh.quality_bins[gmsh_label][1]
        bin_max = mesh.quality_bins[gmsh_label][0]
        bin_med = (bin_min + bin_max) / 2

        if gmsh_label == "aspectRatio":
            cmap = mcolors.LinearSegmentedColormap.from_list(
                "qualidade",
                [(0, "green"), (bin_med / bin_max, "gold"), (1, "red")],
            )
        else:
            cmap = mcolors.LinearSegmentedColormap.from_list(
                "qualidade",
                [(0, "red"), (bin_med, "gold"), (1, "green")],
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

        ax.set_title(f"{title[gmsh_label]} histogram")
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

    def plot_bad_elements(self):
        mesh = app().project.model.mesh
        if mesh is None:
            return

        if not mesh.mesh_quality_data:
            return

        current_index = self.tableWidget_mesh_quality.currentIndex().row()
        gmsh_label = self.gmsh_labels.get(current_index)
        if gmsh_label is None:
            return

        bad_elements_data = mesh.mesh_quality_data.get("bad_elements", {})
        if not bad_elements_data:
            return

        mesh_bad_elements = bad_elements_data[gmsh_label]
        if mesh_bad_elements is None:
            return

        app().main_window.distinguish_mesh_solids(mesh_bad_elements)
        self.bad_elements_showed = True

    def check_unprocessed_local_mesh_size_control(self):
        mesh_setup = app().project.model.mesh_setup
        if mesh_setup is None:
            return

        if mesh_setup.local_mesh_size_control_parameters == self.tmp_local_mesh_size_control_parameters:
            return

        title = "Unprocessed local mesh size control"
        message = "The local mesh size control configuration has been modified, but the mesh itself "
        message += "has not been processed. Would you like to generate the new mesh?"

        buttons_config = {
            "left_button_label": "No",
            "right_button_label": "Generate",
        }

        read = GetUserConfirmationInput(
            title,
            message,
            buttons_config=buttons_config,
            window_title="Vibra",
        )

        if read._cancel:
            return True

        if not read._continue:
            return True

        self.apply_callback()

    def keyPressEvent(self, event: QKeyEvent):
        match event.key():
            case Qt.Key.Key_Enter | Qt.Key.Key_Return:
                self.apply_callback()
            case Qt.Key_Delete:
                self.remove_callback()
            case Qt.Key_Escape:
                self.close()

    def closeEvent(self, a0):
        self.keep_window_open = False
        self.check_unprocessed_local_mesh_size_control()

        if self.bad_elements_showed:
            app().main_window.distinguish_mesh_solids([])

        return super().closeEvent(a0)
