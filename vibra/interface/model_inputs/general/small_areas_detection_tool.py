from PySide6.QtCore import QLocale, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidgetItem,
)

from vibra import app
from vibra.interface.numeric_checks.unit_utilities import convert_length_unit, units_abreviations
from vibra.interface.ui_generated.model.general.small_areas_detection_tool_ui import (
    SmallAreasDetectionTool_UI,
)


class SmallAreasDetectionTool(SmallAreasDetectionTool_UI):
    ELEMENT_SIZE_FACTORS = (
        ("Strict (0.25x)", 0.25),
        ("Medium (0.5x)", 0.5),
        ("Loose (1.0x)", 1.0),
    )
    DEFAULT_ELEMENT_SIZE_FACTOR = 0.5
    MAX_SIZE_GROUPS = 10
    DEFAULT_SIZE_GROUPS = 5
    DEFAULT_THRESHOLD_FACTOR = 2.0

    def __init__(self, mesher_inputs):
        super().__init__()

        app().main_window.set_input_widget(self)

        self.mesher_inputs = mesher_inputs
        self.detection_result = None

        self._initialize()
        self._config_window()
        self._config_widgets()
        self._create_connections()

        while self.keep_window_open:
            self.exec()

    @property
    def length_unit_label(self) -> str:
        if self.mesh is None:
            return ""

        return units_abreviations.get(self.mesh.length_unit, self.mesh.length_unit)

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Small areas detection")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _initialize(self):
        self.keep_window_open = True
        self.mesh = self.mesher_inputs.model.mesh

    def _config_widgets(self):
        self._config_threshold_spinbox()
        self._config_element_size_factor_combobox()
        self._config_size_groups_combobox()
        self._config_table()

        self._clear_results()
        self._update_faces_area_label()

    def _config_threshold_spinbox(self):
        spinbox = self.doubleSpinBox_area_detection_threshold
        spinbox.setLocale(QLocale("pt_BR"))
        spinbox.setDecimals(2)
        spinbox.setMinimum(0.25)
        spinbox.setMaximum(1000.0)
        spinbox.setSingleStep(0.25)
        spinbox.setValue(self.DEFAULT_THRESHOLD_FACTOR)
        spinbox.setKeyboardTracking(False)

    def _config_element_size_factor_combobox(self):
        combobox = self.comboBox_element_size_factor
        combobox.clear()

        for label, factor in self.ELEMENT_SIZE_FACTORS:
            combobox.addItem(label, factor)

        default_index = 0
        for index, (_, factor) in enumerate(self.ELEMENT_SIZE_FACTORS):
            if factor == self.DEFAULT_ELEMENT_SIZE_FACTOR:
                default_index = index
                break

        combobox.setCurrentIndex(default_index)

    def _config_size_groups_combobox(self):
        combobox = self.comboBox_size_groups_quantity
        combobox.clear()

        for quantity in range(1, self.MAX_SIZE_GROUPS + 1):
            combobox.addItem(str(quantity), quantity)

        combobox.setCurrentIndex(self.DEFAULT_SIZE_GROUPS - 1)

    def _config_table(self):
        table = self.tableWidget
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.verticalHeader().setVisible(False)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(False)

    def _create_connections(self):
        self.doubleSpinBox_area_detection_threshold.valueChanged.connect(self._threshold_changed)
        self.pushButton_detect_small_areas.clicked.connect(self._detect_small_areas)
        self.tableWidget.itemClicked.connect(self._table_item_clicked)
        self.pushButton_send_to_local_size_control.clicked.connect(self._send_to_local_size_control)
        self.pushButton_cancel.clicked.connect(self.close)

        minimum_size_spinbox = self.mesher_inputs.doubleSpinBox_minimum_element_size
        minimum_size_spinbox.valueChanged.connect(self._threshold_changed)

    def _get_reference_element_size(self) -> float:
        return self.mesher_inputs.doubleSpinBox_minimum_element_size.value()

    def _get_element_size_factor(self) -> float:
        return float(self.comboBox_element_size_factor.currentData())

    def _get_size_groups_quantity(self) -> int:
        return int(self.comboBox_size_groups_quantity.currentData())

    def _set_send_buttons_enabled(self, enabled: bool):
        self.pushButton_send_to_local_size_control.setEnabled(enabled)

    def _threshold_changed(self, *args):
        self._update_faces_area_label()
        self._clear_results()

    def _update_faces_area_label(self):
        element_size = self._get_reference_element_size()
        threshold = self.doubleSpinBox_area_detection_threshold.value() * element_size**2
        self.label_faces_area.setText(
            f"Faces with area ≤ {threshold:.6g} {self.length_unit_label}² are selected"
        )

    def _clear_results(self):
        self.detection_result = None
        self.tableWidget.setRowCount(0)
        self.label_faces_detected.setText("0 small face(s) detected")
        self._set_send_buttons_enabled(False)

    def _detect_small_areas(self):
        if self.mesh is None:
            return

        self.detection_result = self.mesh.detect_small_areas(
            self._get_reference_element_size(),
            area_factor=self.doubleSpinBox_area_detection_threshold.value(),
        )

        surface_ids = self.detection_result["surface_ids"]
        surface_areas = self.detection_result["surface_areas"]

        grouped_surfaces = self._group_surfaces_by_area(surface_areas)
        self._populate_table(grouped_surfaces)

        self.label_faces_detected.setText(
            f"{len(surface_ids)} small face(s) detected "
            f"in {len(grouped_surfaces)} area group(s)"
        )
        self._set_send_buttons_enabled(bool(surface_ids))

        if surface_ids:
            app().main_window.selection.set_geometry_selection(surfaces=surface_ids)

    def _group_surfaces_by_area(self, surface_areas: dict[int, float]) -> list[tuple[str, list[int]]]:
        length_factor = convert_length_unit(1.0, "meter", self.mesh.length_unit)
        area_factor = length_factor**2

        groups = {}
        for surface_id, area in surface_areas.items():
            area_text = f"{area * area_factor:.6g}"
            groups.setdefault(area_text, []).append(surface_id)

        grouped_surfaces = []
        for area_text, surface_ids in sorted(groups.items(), key=lambda item: float(item[0])):
            grouped_surfaces.append((area_text, sorted(surface_ids)))

        return grouped_surfaces

    def _populate_table(self, grouped_surfaces: list[tuple[str, list[int]]]):
        table = self.tableWidget
        table.setUpdatesEnabled(False)
        table.setRowCount(len(grouped_surfaces))

        for row, (area_text, surface_ids) in enumerate(grouped_surfaces):
            tags = []
            for surface_id in surface_ids:
                tags.append(str(surface_id))

            area_label = f"{area_text} {self.length_unit_label}²"
            table.setItem(row, 0, QTableWidgetItem(", ".join(tags)))
            table.setItem(row, 1, QTableWidgetItem(area_label))

        table.setUpdatesEnabled(True)

    def _table_item_clicked(self, item: QTableWidgetItem):
        surface_item = self.tableWidget.item(item.row(), 0)
        if surface_item is None:
            return

        surface_ids = []
        for tag in surface_item.text().split(","):
            tag = tag.strip()
            if tag:
                surface_ids.append(int(tag))

        if surface_ids:
            app().main_window.selection.set_geometry_selection(surfaces=surface_ids)

    def _get_detected_surface_ids(self) -> list[int]:
        if self.detection_result is None:
            return []

        return self.detection_result["surface_ids"]

    def _build_size_groups(self) -> list[dict]:
        return self.mesh.group_small_areas(
            self._get_detected_surface_ids(),
            max_groups=self._get_size_groups_quantity(),
            representative="median",
            size_multiplier=self._get_element_size_factor(),
        )

    def _send_to_local_size_control(self):
        bins = self._build_size_groups()
        if not bins:
            return

        surface_id_set = set()
        for bin_data in bins:
            for surface_id in bin_data["surface_ids"]:
                surface_id_set.add(surface_id)

        surface_ids = sorted(surface_id_set)

        result = {
            "surface_ids": surface_ids,
            "bins": bins,
        }
        self.mesher_inputs._apply_small_area_refinement_result(result)
        self.label_faces_detected.setText(
            f"Sent {len(surface_ids)} face(s) in {len(bins)} size group(s)."
        )

    def closeEvent(self, event):
        self.keep_window_open = False
        super().closeEvent(event)
