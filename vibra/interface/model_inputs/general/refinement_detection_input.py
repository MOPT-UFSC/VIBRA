from time import perf_counter

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from vibra import app
from vibra.interface.numeric_checks.unit_utilities import convert_length_unit, units_abreviations


class RefinementDetectionInput(QDialog):
    LINE_MODES = {
        "loose": 0.5,
        "medium": 0.75,
        "strict": 1.0,
    }

    FACE_MODES = {
        "strict": 1.2,
        "medium": 1.35,
        "loose": 1.5,
    }

    ADJACENT_MODES = {
        "loose": 2.0,
        "medium": 10.0,
        "strict": 50.0,
    }

    def __init__(self, mesher_inputs):
        super().__init__()

        self.mesher_inputs = mesher_inputs
        self.mesh = mesher_inputs.model.mesh

        if self.mesh is None:
            from vibra.engine.mesher.mesh import Mesh

            self.mesh = Mesh(length_unit="millimeter")

        self.minimum_element_size = mesher_inputs.doubleSpinBox_minimum_element_size.value()

        self.line_mode = "medium"
        self.face_mode = "strict"
        self.line_result = None
        self.face_result = None
        self.detection_result = None
        self.estimated_elements = 0.0

        self._config_window()
        self._create_widgets()
        self._create_connections()
        self._config_widgets()

    def _config_window(self):
        self.setWindowTitle("Refinement detection")
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.NonModal)
        self.setMinimumSize(760, 640)
        self.resize(820, 700)

    def _create_widgets(self):
        main_layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget(self)
        main_layout.addWidget(self.tab_widget)

        self._create_lines_page()
        self._create_faces_page()
        self._create_small_areas_page()
        self._create_points_page()

    def _create_lines_page(self):
        self.lines_page = QWidget(self)
        layout = QVBoxLayout(self.lines_page)

        title = QLabel("<b>Step 1: detect short lines</b>")
        message = QLabel(
            "Select how restrictive the line detection should be. "
            "Only the lines below the chosen threshold will be highlighted in red."
        )
        message.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(message)

        target_row = QHBoxLayout()
        target_row.addWidget(QLabel("Detection target:"))

        self.comboBox_detection_target = QComboBox()
        self.comboBox_detection_target.addItem("Lines only")
        self.comboBox_detection_target.addItem("Faces")
        target_row.addWidget(self.comboBox_detection_target)
        target_row.addStretch()
        layout.addLayout(target_row)

        self.checkBox_refine_adjacent_lines = QCheckBox("Refine lines adjacent to the detected lines")
        self.checkBox_refine_adjacent_lines.setChecked(True)
        layout.addWidget(self.checkBox_refine_adjacent_lines)

        mode_row = QHBoxLayout()
        self.label_line_mode = QLabel("Line threshold:")
        mode_row.addWidget(self.label_line_mode)

        self.line_mode_group = QButtonGroup(self)
        self.line_mode_buttons = {}
        line_mode_labels = {
            "loose": "Loose (<= 50%)",
            "medium": "Medium (<= 75%)",
            "strict": "Strict (<= 100%)",
            "custom": "Custom",
        }

        for mode, label in line_mode_labels.items():
            button = QPushButton(label)
            button.setCheckable(True)
            button.setMinimumHeight(30)
            button.setProperty("mode", mode)
            self.line_mode_group.addButton(button)
            self.line_mode_buttons[mode] = button
            mode_row.addWidget(button)

        mode_row.addStretch()
        layout.addLayout(mode_row)

        custom_line_row = QHBoxLayout()
        custom_line_row.addWidget(QLabel("Custom value:"))

        self.doubleSpinBox_custom_line_threshold = QDoubleSpinBox()
        self.doubleSpinBox_custom_line_threshold.setMinimum(1.0)
        self.doubleSpinBox_custom_line_threshold.setMaximum(500.0)
        self.doubleSpinBox_custom_line_threshold.setSingleStep(1.0)
        self.doubleSpinBox_custom_line_threshold.setDecimals(1)
        self.doubleSpinBox_custom_line_threshold.setValue(80.0)
        self.doubleSpinBox_custom_line_threshold.setSuffix(" %")
        custom_line_row.addWidget(self.doubleSpinBox_custom_line_threshold)

        self.doubleSpinBox_custom_adjacent_factor = QDoubleSpinBox()
        self.doubleSpinBox_custom_adjacent_factor.setMinimum(0.1)
        self.doubleSpinBox_custom_adjacent_factor.setMaximum(500.0)
        self.doubleSpinBox_custom_adjacent_factor.setSingleStep(1.0)
        self.doubleSpinBox_custom_adjacent_factor.setDecimals(1)
        self.doubleSpinBox_custom_adjacent_factor.setValue(20.0)
        self.doubleSpinBox_custom_adjacent_factor.setSuffix(" x")
        custom_line_row.addWidget(self.doubleSpinBox_custom_adjacent_factor)

        custom_line_row.addStretch()
        layout.addLayout(custom_line_row)

        self.label_line_threshold = QLabel("")
        layout.addWidget(self.label_line_threshold)

        self.pushButton_detect_lines = QPushButton("Detect lines")
        self.pushButton_detect_lines.setMinimumHeight(34)
        layout.addWidget(self.pushButton_detect_lines)

        self.label_lines_count = QLabel("No lines detected.")
        self.label_lines_count.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.label_lines_count)

        self.list_lines = QListWidget()
        self.list_lines.setMinimumHeight(240)
        layout.addWidget(self.list_lines)

        line_size_row = QHBoxLayout()
        line_size_row.addWidget(QLabel("Max sizes:"))

        self.spinBox_line_size_bins = QSpinBox()
        self.spinBox_line_size_bins.setMinimum(1)
        self.spinBox_line_size_bins.setMaximum(12)
        self.spinBox_line_size_bins.setValue(5)
        line_size_row.addWidget(self.spinBox_line_size_bins)

        line_size_row.addSpacing(16)
        line_size_row.addWidget(QLabel("Size ratio:"))

        self.doubleSpinBox_line_size_ratio = QDoubleSpinBox()
        self.doubleSpinBox_line_size_ratio.setMinimum(1.05)
        self.doubleSpinBox_line_size_ratio.setMaximum(4.0)
        self.doubleSpinBox_line_size_ratio.setSingleStep(0.05)
        self.doubleSpinBox_line_size_ratio.setDecimals(2)
        self.doubleSpinBox_line_size_ratio.setValue(1.5)
        line_size_row.addWidget(self.doubleSpinBox_line_size_ratio)

        line_size_row.addSpacing(16)
        line_size_row.addWidget(QLabel("Line size factor:"))

        self.doubleSpinBox_line_size_factor = QDoubleSpinBox()
        self.doubleSpinBox_line_size_factor.setMinimum(0.01)
        self.doubleSpinBox_line_size_factor.setMaximum(10.0)
        self.doubleSpinBox_line_size_factor.setSingleStep(0.01)
        self.doubleSpinBox_line_size_factor.setDecimals(2)
        self.doubleSpinBox_line_size_factor.setValue(0.33)
        line_size_row.addWidget(self.doubleSpinBox_line_size_factor)

        line_size_row.addStretch()
        layout.addLayout(line_size_row)

        line_band_row = QHBoxLayout()
        line_band_row.addWidget(QLabel("Transition band:"))

        self.doubleSpinBox_line_transition_band = QDoubleSpinBox()
        self.doubleSpinBox_line_transition_band.setMinimum(0.1)
        self.doubleSpinBox_line_transition_band.setMaximum(50.0)
        self.doubleSpinBox_line_transition_band.setSingleStep(0.5)
        self.doubleSpinBox_line_transition_band.setDecimals(2)
        self.doubleSpinBox_line_transition_band.setValue(20.0)
        line_band_row.addWidget(self.doubleSpinBox_line_transition_band)
        line_band_row.addStretch()
        layout.addLayout(line_band_row)

        self.pushButton_send_lines = QPushButton("Send lines to refinement")
        self.pushButton_send_lines.setMinimumHeight(34)
        layout.addWidget(self.pushButton_send_lines)

        self.label_line_send_status = QLabel("")
        layout.addWidget(self.label_line_send_status)

        buttons_row = QHBoxLayout()
        self.pushButton_cancel_lines = QPushButton("Cancel")
        self.pushButton_next = QPushButton("Faces tab")
        self.pushButton_next.setMinimumHeight(32)
        buttons_row.addStretch()
        buttons_row.addWidget(self.pushButton_cancel_lines)
        buttons_row.addWidget(self.pushButton_next)
        layout.addLayout(buttons_row)

        self.tab_widget.addTab(self.lines_page, "Lines size control setup")

    def _create_faces_page(self):
        self.faces_page = QWidget(self)
        layout = QVBoxLayout(self.faces_page)

        title = QLabel("<b>Step 2: select related faces</b>")
        message = QLabel(
            "Choose the area margin used to select the faces related to the detected lines. "
            "The selected faces will be shown in the list below."
        )
        message.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(message)

        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel("Face area margin:"))

        self.face_mode_group = QButtonGroup(self)
        face_mode_labels = {
            "strict": "Strict (+20%)",
            "medium": "Medium (+35%)",
            "loose": "Loose (+50%)",
            "custom": "Custom",
        }

        for mode, label in face_mode_labels.items():
            button = QPushButton(label)
            button.setCheckable(True)
            button.setMinimumHeight(30)
            button.setProperty("mode", mode)
            self.face_mode_group.addButton(button)
            mode_row.addWidget(button)

        mode_row.addStretch()
        layout.addLayout(mode_row)

        custom_face_row = QHBoxLayout()
        custom_face_row.addWidget(QLabel("Custom face area margin:"))

        self.doubleSpinBox_custom_face_margin = QDoubleSpinBox()
        self.doubleSpinBox_custom_face_margin.setMinimum(0.0)
        self.doubleSpinBox_custom_face_margin.setMaximum(500.0)
        self.doubleSpinBox_custom_face_margin.setSingleStep(1.0)
        self.doubleSpinBox_custom_face_margin.setDecimals(1)
        self.doubleSpinBox_custom_face_margin.setValue(30.0)
        self.doubleSpinBox_custom_face_margin.setSuffix(" %")
        custom_face_row.addWidget(self.doubleSpinBox_custom_face_margin)

        custom_face_row.addStretch()
        layout.addLayout(custom_face_row)

        grouping_row = QHBoxLayout()
        grouping_row.addWidget(QLabel("Max element sizes:"))

        self.spinBox_max_size_bins = QSpinBox()
        self.spinBox_max_size_bins.setMinimum(1)
        self.spinBox_max_size_bins.setMaximum(12)
        self.spinBox_max_size_bins.setValue(5)
        grouping_row.addWidget(self.spinBox_max_size_bins)

        grouping_row.addSpacing(20)
        grouping_row.addWidget(QLabel("Size ratio:"))

        self.doubleSpinBox_size_ratio = QDoubleSpinBox()
        self.doubleSpinBox_size_ratio.setMinimum(1.05)
        self.doubleSpinBox_size_ratio.setMaximum(4.0)
        self.doubleSpinBox_size_ratio.setSingleStep(0.05)
        self.doubleSpinBox_size_ratio.setDecimals(2)
        self.doubleSpinBox_size_ratio.setValue(1.5)
        grouping_row.addWidget(self.doubleSpinBox_size_ratio)

        grouping_row.addStretch()
        layout.addLayout(grouping_row)

        multiplier_row = QHBoxLayout()
        multiplier_row.addWidget(QLabel("Element size multiplier:"))

        self.doubleSpinBox_size_multiplier = QDoubleSpinBox()
        self.doubleSpinBox_size_multiplier.setMinimum(0.1)
        self.doubleSpinBox_size_multiplier.setMaximum(10.0)
        self.doubleSpinBox_size_multiplier.setSingleStep(0.1)
        self.doubleSpinBox_size_multiplier.setDecimals(2)
        self.doubleSpinBox_size_multiplier.setValue(2.0)
        multiplier_row.addWidget(self.doubleSpinBox_size_multiplier)

        multiplier_row.addWidget(QLabel("(element size = grouped line size x multiplier)"))
        multiplier_row.addStretch()
        layout.addLayout(multiplier_row)

        band_row = QHBoxLayout()
        band_row.addWidget(QLabel("Transition band:"))

        self.doubleSpinBox_transition_band = QDoubleSpinBox()
        self.doubleSpinBox_transition_band.setMinimum(0.1)
        self.doubleSpinBox_transition_band.setMaximum(50.0)
        self.doubleSpinBox_transition_band.setSingleStep(0.5)
        self.doubleSpinBox_transition_band.setDecimals(2)
        self.doubleSpinBox_transition_band.setValue(20.0)
        band_row.addWidget(self.doubleSpinBox_transition_band)

        band_row.addWidget(QLabel("(line mode: band x line size | whole faces: band x minimum element size)"))
        band_row.addStretch()
        layout.addLayout(band_row)

        self.checkBox_refine_whole_faces = QCheckBox("Refine whole faces instead of only the bands around lines")
        self.checkBox_refine_whole_faces.setChecked(False)
        layout.addWidget(self.checkBox_refine_whole_faces)

        self.pushButton_select_faces = QPushButton("Select related faces")
        self.pushButton_select_faces.setMinimumHeight(34)
        layout.addWidget(self.pushButton_select_faces)

        self.label_faces_count = QLabel("No faces selected.")
        self.label_faces_count.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.label_faces_count)

        self.list_faces = QTreeWidget()
        self.list_faces.setHeaderLabels(["Size group / face", "Area"])
        self.list_faces.setMinimumHeight(320)
        layout.addWidget(self.list_faces)

        self.label_refinement_size = QLabel("")
        layout.addWidget(self.label_refinement_size)

        self.label_cost_estimate = QLabel("")
        layout.addWidget(self.label_cost_estimate)

        buttons_row = QHBoxLayout()
        self.pushButton_back = QPushButton("Back")
        self.pushButton_cancel_faces = QPushButton("Cancel")
        self.pushButton_send_to_refinement = QPushButton("Send to refinement")
        self.pushButton_send_to_refinement.setMinimumHeight(32)
        buttons_row.addWidget(self.pushButton_back)
        buttons_row.addStretch()
        buttons_row.addWidget(self.pushButton_cancel_faces)
        buttons_row.addWidget(self.pushButton_send_to_refinement)
        layout.addLayout(buttons_row)

        self.tab_widget.addTab(self.faces_page, "Faces size control setup")

    def _create_small_areas_page(self):
        self.small_areas_page = QWidget(self)
        layout = QVBoxLayout(self.small_areas_page)

        title = QLabel("<b>Small areas based size control setup</b>")
        message = QLabel(
            "Detect faces whose area is small compared with the area of one element "
            "at the minimum element size. Only the detected faces are refined."
        )
        message.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(message)

        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel("Element size factor:"))

        self.small_area_mode_group = QButtonGroup(self)
        self.small_area_mode_buttons = {}
        self.small_area_mode = "medium"
        labels = {
            "strict": "Strict (0.25x size)",
            "medium": "Medium (0.5x)",
            "loose": "Loose (1x)",
            "custom": "Custom",
        }

        for mode, label in labels.items():
            button = QPushButton(label)
            button.setCheckable(True)
            button.setMinimumHeight(30)
            button.setProperty("mode", mode)
            self.small_area_mode_group.addButton(button)
            self.small_area_mode_buttons[mode] = button
            mode_row.addWidget(button)

        mode_row.addStretch()
        layout.addLayout(mode_row)

        custom_row = QHBoxLayout()
        custom_row.addWidget(QLabel("Area threshold:"))
        self.doubleSpinBox_small_area_custom_factor = QDoubleSpinBox()
        self.doubleSpinBox_small_area_custom_factor.setMinimum(0.01)
        self.doubleSpinBox_small_area_custom_factor.setMaximum(1000.0)
        self.doubleSpinBox_small_area_custom_factor.setSingleStep(0.5)
        self.doubleSpinBox_small_area_custom_factor.setDecimals(2)
        self.doubleSpinBox_small_area_custom_factor.setValue(2.0)
        self.doubleSpinBox_small_area_custom_factor.setSuffix(" x element area")
        custom_row.addWidget(self.doubleSpinBox_small_area_custom_factor)

        custom_row.addSpacing(20)
        custom_row.addWidget(QLabel("Custom size factor:"))
        self.doubleSpinBox_small_area_size_factor = QDoubleSpinBox()
        self.doubleSpinBox_small_area_size_factor.setMinimum(0.01)
        self.doubleSpinBox_small_area_size_factor.setMaximum(10.0)
        self.doubleSpinBox_small_area_size_factor.setSingleStep(0.01)
        self.doubleSpinBox_small_area_size_factor.setDecimals(2)
        self.doubleSpinBox_small_area_size_factor.setValue(0.5)
        custom_row.addWidget(self.doubleSpinBox_small_area_size_factor)

        custom_row.addSpacing(20)
        custom_row.addWidget(QLabel("Transition band:"))
        self.doubleSpinBox_small_area_transition_band = QDoubleSpinBox()
        self.doubleSpinBox_small_area_transition_band.setMinimum(0.1)
        self.doubleSpinBox_small_area_transition_band.setMaximum(50.0)
        self.doubleSpinBox_small_area_transition_band.setSingleStep(0.5)
        self.doubleSpinBox_small_area_transition_band.setDecimals(2)
        self.doubleSpinBox_small_area_transition_band.setValue(20.0)
        custom_row.addWidget(self.doubleSpinBox_small_area_transition_band)
        custom_row.addStretch()
        layout.addLayout(custom_row)

        bins_row = QHBoxLayout()
        bins_row.addWidget(QLabel("Max sizes:"))

        self.spinBox_small_area_size_bins = QSpinBox()
        self.spinBox_small_area_size_bins.setMinimum(1)
        self.spinBox_small_area_size_bins.setMaximum(12)
        self.spinBox_small_area_size_bins.setValue(5)
        bins_row.addWidget(self.spinBox_small_area_size_bins)

        bins_row.addSpacing(16)
        bins_row.addWidget(QLabel("Size ratio:"))

        self.doubleSpinBox_small_area_size_ratio = QDoubleSpinBox()
        self.doubleSpinBox_small_area_size_ratio.setMinimum(1.05)
        self.doubleSpinBox_small_area_size_ratio.setMaximum(4.0)
        self.doubleSpinBox_small_area_size_ratio.setSingleStep(0.05)
        self.doubleSpinBox_small_area_size_ratio.setDecimals(2)
        self.doubleSpinBox_small_area_size_ratio.setValue(1.5)
        bins_row.addWidget(self.doubleSpinBox_small_area_size_ratio)

        bins_row.addStretch()
        layout.addLayout(bins_row)

        self.label_small_area_threshold = QLabel("")
        layout.addWidget(self.label_small_area_threshold)

        self.pushButton_detect_small_areas = QPushButton("Detect small areas")
        self.pushButton_detect_small_areas.setMinimumHeight(34)
        layout.addWidget(self.pushButton_detect_small_areas)

        self.label_small_areas_count = QLabel("No small areas detected.")
        self.label_small_areas_count.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.label_small_areas_count)

        self.list_small_areas = QListWidget()
        self.list_small_areas.setMinimumHeight(320)
        layout.addWidget(self.list_small_areas)

        self.pushButton_send_small_areas = QPushButton("Send small areas to refinement")
        self.pushButton_send_small_areas.setMinimumHeight(34)
        self.pushButton_send_small_areas.setDisabled(True)
        layout.addWidget(self.pushButton_send_small_areas)

        self.tab_widget.addTab(self.small_areas_page, "Small areas based size control setup")

    def _create_points_page(self):
        self.points_page = QWidget(self)
        layout = QVBoxLayout(self.points_page)

        title = QLabel("<b>Points distance based size control setup</b>")
        message = QLabel(
            "Detect pairs of points closer than the minimum element size and refine "
            "around those points. The element size is based on the point distance."
        )
        message.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(message)

        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel("Point size factor:"))

        self.point_mode_group = QButtonGroup(self)
        self.point_mode_buttons = {}
        self.point_mode = "medium"
        labels = {
            "strict": "Strict (0.25x distance)",
            "medium": "Medium (0.50x)",
            "loose": "Loose (0.75x)",
            "custom": "Custom",
        }

        for mode, label in labels.items():
            button = QPushButton(label)
            button.setCheckable(True)
            button.setMinimumHeight(30)
            button.setProperty("mode", mode)
            self.point_mode_group.addButton(button)
            self.point_mode_buttons[mode] = button
            mode_row.addWidget(button)

        mode_row.addStretch()
        layout.addLayout(mode_row)

        custom_row = QHBoxLayout()
        custom_row.addWidget(QLabel("Custom factor:"))
        self.doubleSpinBox_point_custom_factor = QDoubleSpinBox()
        self.doubleSpinBox_point_custom_factor.setMinimum(1.0)
        self.doubleSpinBox_point_custom_factor.setMaximum(100.0)
        self.doubleSpinBox_point_custom_factor.setSingleStep(1.0)
        self.doubleSpinBox_point_custom_factor.setDecimals(1)
        self.doubleSpinBox_point_custom_factor.setValue(50.0)
        self.doubleSpinBox_point_custom_factor.setSuffix(" % of distance")
        custom_row.addWidget(self.doubleSpinBox_point_custom_factor)

        custom_row.addSpacing(20)
        custom_row.addWidget(QLabel("Transition band:"))
        self.doubleSpinBox_point_transition_band = QDoubleSpinBox()
        self.doubleSpinBox_point_transition_band.setMinimum(0.1)
        self.doubleSpinBox_point_transition_band.setMaximum(50.0)
        self.doubleSpinBox_point_transition_band.setSingleStep(0.5)
        self.doubleSpinBox_point_transition_band.setDecimals(2)
        self.doubleSpinBox_point_transition_band.setValue(20.0)
        custom_row.addWidget(self.doubleSpinBox_point_transition_band)
        custom_row.addStretch()
        layout.addLayout(custom_row)

        self.label_points_threshold = QLabel("")
        layout.addWidget(self.label_points_threshold)

        self.pushButton_detect_points = QPushButton("Detect close point pairs")
        self.pushButton_detect_points.setMinimumHeight(34)
        layout.addWidget(self.pushButton_detect_points)

        self.label_points_count = QLabel("No close point pairs detected.")
        self.label_points_count.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.label_points_count)

        self.list_points = QListWidget()
        self.list_points.setMinimumHeight(320)
        layout.addWidget(self.list_points)

        self.pushButton_send_points = QPushButton("Send points to refinement")
        self.pushButton_send_points.setMinimumHeight(34)
        self.pushButton_send_points.setDisabled(True)
        layout.addWidget(self.pushButton_send_points)

        self.tab_widget.addTab(self.points_page, "Points distance based size control setup")

    def _create_connections(self):
        self.line_mode_group.buttonClicked.connect(self._line_mode_changed)
        self.face_mode_group.buttonClicked.connect(self._face_mode_changed)

        self.pushButton_detect_lines.clicked.connect(self._detect_lines)
        self.pushButton_next.clicked.connect(self._show_faces_page)
        self.pushButton_select_faces.clicked.connect(self._select_faces)
        self.pushButton_back.clicked.connect(self._show_lines_page)
        self.pushButton_send_to_refinement.clicked.connect(self._send_to_refinement)

        self.spinBox_max_size_bins.valueChanged.connect(self._size_grouping_changed)
        self.doubleSpinBox_size_ratio.valueChanged.connect(self._size_grouping_changed)
        self.doubleSpinBox_size_multiplier.valueChanged.connect(self._size_grouping_changed)
        self.doubleSpinBox_transition_band.valueChanged.connect(self._size_grouping_changed)
        self.checkBox_refine_whole_faces.toggled.connect(self._refine_mode_changed)
        self.comboBox_detection_target.currentIndexChanged.connect(self._target_changed)
        self.checkBox_refine_adjacent_lines.toggled.connect(self._adjacent_lines_changed)
        self.doubleSpinBox_custom_line_threshold.valueChanged.connect(self._custom_line_value_changed)
        self.doubleSpinBox_custom_adjacent_factor.valueChanged.connect(self._custom_line_value_changed)
        self.doubleSpinBox_custom_face_margin.valueChanged.connect(self._custom_face_value_changed)

        self.pushButton_send_lines.clicked.connect(self._send_lines_to_refinement)
        self.small_area_mode_group.buttonClicked.connect(self._small_area_mode_changed)
        self.doubleSpinBox_small_area_custom_factor.valueChanged.connect(self._update_small_area_threshold)
        self.pushButton_detect_small_areas.clicked.connect(self._detect_small_areas)
        self.pushButton_send_small_areas.clicked.connect(self._send_small_areas_to_refinement)
        self.point_mode_group.buttonClicked.connect(self._point_mode_changed)
        self.doubleSpinBox_point_custom_factor.valueChanged.connect(self._update_points_threshold)
        self.pushButton_detect_points.clicked.connect(self._detect_close_points)
        self.pushButton_send_points.clicked.connect(self._send_points_to_refinement)

        self.pushButton_cancel_lines.clicked.connect(self.reject)
        self.pushButton_cancel_faces.clicked.connect(self.reject)

    def _config_widgets(self):
        for button in self.line_mode_group.buttons():
            if button.property("mode") == self.line_mode:
                button.setChecked(True)

        for button in self.face_mode_group.buttons():
            if button.property("mode") == self.face_mode:
                button.setChecked(True)

        for button in self.small_area_mode_group.buttons():
            if button.property("mode") == self.small_area_mode:
                button.setChecked(True)

        for button in self.point_mode_group.buttons():
            if button.property("mode") == self.point_mode:
                button.setChecked(True)

        self.pushButton_next.setDisabled(True)
        self.pushButton_send_to_refinement.setDisabled(True)
        self.tab_widget.setCurrentWidget(self.lines_page)
        self._update_line_mode_labels()
        self._update_line_threshold_label()
        self._update_custom_controls()
        self._update_small_area_threshold()
        self._update_points_threshold()

    @property
    def length_unit_label(self) -> str:
        return units_abreviations.get(self.mesh.length_unit, self.mesh.length_unit)

    def _log_time(self, label: str, start_time: float):
        print(f"[RefinementDetection] {label}: {perf_counter() - start_time:.3f}s", flush=True)

    def _is_lines_only_target(self) -> bool:
        return self.comboBox_detection_target.currentText() == "Lines only"

    def _get_line_length_factor(self) -> float:
        if self.line_mode == "custom":
            return self.doubleSpinBox_custom_line_threshold.value() / 100.0
        return self.LINE_MODES[self.line_mode]

    def _get_adjacent_factor(self) -> float:
        if self.line_mode == "custom":
            return self.doubleSpinBox_custom_adjacent_factor.value()
        return self.ADJACENT_MODES[self.line_mode]

    def _get_face_area_factor(self) -> float:
        if self.face_mode == "custom":
            return 1.0 + self.doubleSpinBox_custom_face_margin.value() / 100.0
        return self.FACE_MODES[self.face_mode]

    def _update_custom_controls(self):
        lines_only = self._is_lines_only_target()

        self.doubleSpinBox_custom_line_threshold.setVisible(not lines_only)
        self.doubleSpinBox_custom_adjacent_factor.setVisible(lines_only)
        self.doubleSpinBox_custom_line_threshold.setEnabled(self.line_mode == "custom")
        self.doubleSpinBox_custom_adjacent_factor.setEnabled(self.line_mode == "custom")
        self.doubleSpinBox_custom_face_margin.setEnabled(self.face_mode == "custom")

    def _update_line_mode_labels(self):
        lines_only = self._is_lines_only_target()
        self.checkBox_refine_adjacent_lines.setEnabled(lines_only)
        self.checkBox_refine_whole_faces.setEnabled(not lines_only)

        if lines_only:
            self.checkBox_refine_whole_faces.setChecked(False)
            self.label_line_mode.setText("Adjacent line factor:")
            labels = {
                "loose": "Loose (2x)",
                "medium": "Medium (10x)",
                "strict": "Strict (50x)",
                "custom": "Custom",
            }
        else:
            self.label_line_mode.setText("Line threshold:")
            labels = {
                "loose": "Loose (<= 50%)",
                "medium": "Medium (<= 75%)",
                "strict": "Strict (<= 100%)",
                "custom": "Custom",
            }

        for mode, button in self.line_mode_buttons.items():
            button.setText(labels[mode])

        self._update_custom_controls()

    def _update_line_threshold_label(self):
        unit_label = self.length_unit_label
        self.label_line_threshold.setText("")

        if self._is_lines_only_target():
            adjacent_factor = self._get_adjacent_factor()
            text = (
                f"Lines up to {self.minimum_element_size:.6g} {unit_label} are detected"
            )
            if self.checkBox_refine_adjacent_lines.isChecked():
                text += f" | adjacent lines up to {adjacent_factor:g}x the smallest"
            self.label_line_threshold.setText(text)
            return

        factor = self._get_line_length_factor()
        threshold = factor * self.minimum_element_size
        text = (
            f"Minimum element size: {self.minimum_element_size:.6g} {unit_label} | "
            f"line threshold: {threshold:.6g} {unit_label}"
        )
        self.label_line_threshold.setText(text)

    def _reset_detection_results(self):
        self.line_result = None
        self.face_result = None

        self.list_lines.clear()
        self.list_faces.clear()
        self.label_lines_count.setText("No lines detected.")
        self.label_faces_count.setText("No faces selected.")
        self.label_refinement_size.setText("")
        self.label_cost_estimate.setText("")
        self.estimated_elements = 0.0
        self.pushButton_next.setDisabled(True)
        self.pushButton_send_to_refinement.setDisabled(True)

        app().main_window.clear_refinement_detection_lines()
        app().main_window.entity_visibility.unhide_all()

    def _line_mode_changed(self, button: QPushButton):
        self.line_mode = button.property("mode")
        self._update_line_threshold_label()
        self._update_custom_controls()
        self._reset_detection_results()

    def _target_changed(self):
        self._update_line_mode_labels()
        self._update_line_threshold_label()
        self._reset_detection_results()

    def _adjacent_lines_changed(self):
        self._update_line_threshold_label()
        self._reset_detection_results()

    def _custom_line_value_changed(self):
        self._update_line_threshold_label()
        if self.line_mode == "custom":
            self._reset_detection_results()

    def _custom_face_value_changed(self):
        if self.face_mode == "custom" and self.line_result is not None:
            self._select_faces()

    def _face_mode_changed(self, button: QPushButton):
        self.face_mode = button.property("mode")
        self._update_custom_controls()
        if self.line_result is not None:
            self._select_faces()

    def _size_grouping_changed(self):
        if self.line_result is not None:
            self._select_faces()

    def _refine_mode_changed(self):
        self.doubleSpinBox_transition_band.setEnabled(True)
        self._size_grouping_changed()

    def _run_detection(self) -> dict:
        if self._is_lines_only_target():
            length_factor = 1.0
            adjacent_factor = (
                self._get_adjacent_factor()
                if self.checkBox_refine_adjacent_lines.isChecked()
                else None
            )
        else:
            length_factor = self._get_line_length_factor()
            adjacent_factor = None

        return self.mesh.detect_refinement_need(
            self.minimum_element_size,
            length_factor=length_factor,
            area_factor=self._get_face_area_factor(),
            adjacent_factor=adjacent_factor,
        )

    def _detect_lines(self):
        t_start = perf_counter()
        print("[RefinementDetection] line detection started...", flush=True)

        t_detect = perf_counter()
        result = self._run_detection()
        self._log_time("detect_refinement_need (lines)", t_detect)

        self.line_result = result
        self.face_result = None

        t_populate = perf_counter()
        self._populate_lines(result)
        self._log_time("populate line list", t_populate)

        self.list_faces.clear()
        self.label_faces_count.setText("No faces selected.")
        self.label_refinement_size.setText("")
        self.label_cost_estimate.setText("")
        self.estimated_elements = 0.0
        self.pushButton_send_to_refinement.setDisabled(True)

        line_ids = result["line_ids"]

        t_render = perf_counter()
        if line_ids:
            app().main_window.set_refinement_detection_lines(line_ids)
            app().main_window.selection.set_geometry_selection(lines=line_ids)
        else:
            app().main_window.clear_refinement_detection_lines()
            app().main_window.selection.set_geometry_selection(lines=[])
        self._log_time("highlight detected lines", t_render)

        t_unhide = perf_counter()
        app().main_window.entity_visibility.unhide_all()
        self._log_time("unhide all entities", t_unhide)

        self.pushButton_next.setDisabled(not line_ids)
        self._log_time("line detection total", t_start)

    def _populate_lines(self, result: dict):
        groups = sorted(result["groups"], key=lambda group: group["line_length"])
        unit_label = self.length_unit_label

        self.list_lines.setUpdatesEnabled(False)
        self.list_lines.clear()
        for group in groups:
            length = convert_length_unit(group["line_length"], "meter", self.mesh.length_unit)
            self.list_lines.addItem(f"Line {group['line_id']}: {length:.6g} {unit_label}")
        self.list_lines.setUpdatesEnabled(True)

        self.label_lines_count.setText(f"{len(groups)} line(s) detected.")

    def _show_faces_page(self):
        if self.line_result is None or not self.line_result["line_ids"]:
            return

        self.tab_widget.setCurrentWidget(self.faces_page)
        self._select_faces()

    def _show_lines_page(self):
        self.tab_widget.setCurrentWidget(self.lines_page)
        app().main_window.entity_visibility.unhide_all()

        if self.line_result is not None:
            app().main_window.selection.set_geometry_selection(lines=self.line_result["line_ids"])

    def _select_faces(self):
        if self.line_result is None:
            return

        t_start = perf_counter()
        print("[RefinementDetection] face selection started...", flush=True)

        t_detect = perf_counter()
        result = self._run_detection()
        self._log_time("detect_refinement_need (faces)", t_detect)

        t_group = perf_counter()
        bins = self.mesh.group_refinement_sizes(
            result["groups"],
            max_bins=self.spinBox_max_size_bins.value(),
            merge_ratio=self.doubleSpinBox_size_ratio.value(),
            representative="median",
            size_multiplier=self.doubleSpinBox_size_multiplier.value(),
        )
        self._log_time("group_refinement_sizes", t_group)

        line_ids = sorted({line_id for bin_data in bins for line_id in bin_data["line_ids"]})
        surface_ids = sorted({
            surface_id
            for bin_data in bins
            for surface_id in bin_data["surface_ids"]
        })

        result["line_ids"] = line_ids
        result["surface_ids"] = surface_ids
        result["bins"] = bins
        self.face_result = result

        t_populate = perf_counter()
        self._populate_faces(result)
        self._log_time("populate face tree", t_populate)

        t_render = perf_counter()
        app().main_window.set_refinement_detection_lines(line_ids)
        app().main_window.selection.set_geometry_selection(lines=line_ids, surfaces=surface_ids)
        self._log_time("highlight detected lines and faces", t_render)

        t_ghost = perf_counter()
        if surface_ids:
            self.mesher_inputs.ghost_surfaces_except(surface_ids)
        else:
            app().main_window.entity_visibility.unhide_all()
        self._log_time("ghost remaining surfaces", t_ghost)

        self.pushButton_send_to_refinement.setDisabled(not surface_ids)
        self._log_time("face selection total", t_start)

    def _populate_faces(self, result: dict):
        bins = result["bins"]
        surface_areas = result["surface_areas"]
        length_factor = convert_length_unit(1.0, "meter", self.mesh.length_unit)
        area_factor = length_factor**2
        unit_label = self.length_unit_label

        self.list_faces.setUpdatesEnabled(False)
        self.list_faces.clear()

        total_faces = sum(len(bin_data["surface_ids"]) for bin_data in bins)
        added_faces = 0
        last_progress = perf_counter()

        for bin_data in bins:
            size = convert_length_unit(bin_data["element_size"], "meter", self.mesh.length_unit)
            count = len(bin_data["surface_ids"])
            bin_item = QTreeWidgetItem([f"Size {size:.6g} {unit_label} ({count} face(s))", ""])
            self.list_faces.addTopLevelItem(bin_item)

            for surface_id in sorted(bin_data["surface_ids"], key=lambda _id: surface_areas.get(_id, 0)):
                area = surface_areas[surface_id] * area_factor
                face_item = QTreeWidgetItem([f"Face {surface_id}", f"{area:.6g} {unit_label}²"])
                bin_item.addChild(face_item)
                added_faces += 1

                if perf_counter() - last_progress >= 1.0:
                    print(
                        f"[RefinementDetection] face tree progress: {added_faces}/{total_faces} faces...",
                        flush=True,
                    )
                    last_progress = perf_counter()

            bin_item.setExpanded(True)

        self.list_faces.setUpdatesEnabled(True)

        self.label_faces_count.setText(
            f"{len(result['surface_ids'])} face(s) selected in {len(bins)} size group(s)."
        )

        sizes = [
            convert_length_unit(bin_data["element_size"], "meter", self.mesh.length_unit)
            for bin_data in bins
        ]
        sizes_text = ", ".join(f"{size:.6g} {unit_label}" for size in sizes)
        self.label_refinement_size.setText(f"Element sizes: {sizes_text}" if sizes_text else "")

        estimated_elements = self._estimate_elements(
            bins,
            surface_areas,
            refine_whole_faces=self.checkBox_refine_whole_faces.isChecked(),
            transition_band=self.doubleSpinBox_transition_band.value(),
        )
        self.estimated_elements = estimated_elements
        self.label_cost_estimate.setStyleSheet("font-weight: bold;")

        if estimated_elements >= 3_000_000:
            self.label_cost_estimate.setStyleSheet("font-weight: bold; color: red;")
            estimate_text = f"Estimated elements: ~{estimated_elements:,.0f} (very high, OOM risk)"
        elif estimated_elements > 2_000_000:
            self.label_cost_estimate.setStyleSheet("font-weight: bold; color: #d97706;")
            estimate_text = f"Estimated elements: ~{estimated_elements:,.0f} (high, check before generating)"
        else:
            estimate_text = f"Estimated elements: ~{estimated_elements:,.0f}"

        mode = "whole faces" if self.checkBox_refine_whole_faces.isChecked() else "line bands"
        self.label_cost_estimate.setText(f"{estimate_text} [{mode}]")

    def _estimate_elements(
        self,
        bins: list[dict],
        surface_areas: dict[int, float],
        refine_whole_faces: bool,
        transition_band: float,
    ) -> float:
        from math import pi

        triangle_area_factor = 0.433
        tetra_volume_factor = 0.1
        estimated_elements = 0.0

        for bin_data in bins:
            size = bin_data["element_size"]
            if size <= 0:
                continue

            band_reference = self.minimum_element_size if self.minimum_element_size > 0 else size
            band_distance = transition_band * band_reference
            line_length_sum = bin_data.get("line_length_sum", 0.0)

            if refine_whole_faces:
                area = sum(surface_areas.get(surface_id, 0.0) for surface_id in bin_data["surface_ids"])
                surface_elements = area / (triangle_area_factor * size**2)
                transition_volume = area * band_distance
                volume_elements = transition_volume / (tetra_volume_factor * size**3)
                bin_estimate = surface_elements + volume_elements
            else:
                band_distance = transition_band * size
                surface_band_area = 2 * band_distance * line_length_sum
                surface_elements = surface_band_area / (triangle_area_factor * size**2)
                band_volume = pi * band_distance**2 * line_length_sum
                volume_elements = band_volume / (tetra_volume_factor * size**3)
                bin_estimate = surface_elements + volume_elements

            estimated_elements += bin_estimate
            print(
                f"[RefinementDetection] bin {size:.6g} m: {len(bin_data['surface_ids'])} faces, "
                f"estimated elements ~{bin_estimate:,.0f}",
                flush=True,
            )

        print(f"[RefinementDetection] estimated total elements: ~{estimated_elements:,.0f}", flush=True)
        return estimated_elements

    def _send_to_refinement(self):
        if self.face_result is None or not self.face_result["surface_ids"]:
            return

        if self.estimated_elements > 5_000_000:
            from PySide6.QtWidgets import QMessageBox

            message = (
                f"The estimated number of surface elements is ~{self.estimated_elements:,.0f}.\n\n"
                "This can exhaust the available memory and make the mesh generation process be killed.\n"
                "Do you want to continue anyway?"
            )
            buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            answer = QMessageBox.warning(self, "High mesh refinement cost", message, buttons, QMessageBox.StandardButton.No)
            if answer != QMessageBox.StandardButton.Yes:
                return

        print("[RefinementDetection] sending result to refinement...", flush=True)
        refine_whole_faces = self.checkBox_refine_whole_faces.isChecked() and not self._is_lines_only_target()
        self.detection_result = {
            "line_ids": self.face_result["line_ids"],
            "surface_ids": self.face_result["surface_ids"],
            "bins": self.face_result["bins"],
            "transition_band": self.doubleSpinBox_transition_band.value(),
            "refine_whole_faces": refine_whole_faces,
            "refinement_length": min(
                (bin_data["element_size"] for bin_data in self.face_result["bins"]),
                default=None,
            ),
        }
        self.accept()

    def _send_lines_to_refinement(self):
        if self.line_result is None or not self.line_result["groups"]:
            return

        bins = self.mesh.group_refinement_sizes(
            self.line_result["groups"],
            max_bins=self.spinBox_line_size_bins.value(),
            merge_ratio=self.doubleSpinBox_line_size_ratio.value(),
            representative="median",
            size_multiplier=self.doubleSpinBox_line_size_factor.value(),
        )

        line_ids = sorted({line_id for bin_data in bins for line_id in bin_data["line_ids"]})
        surface_ids = sorted({surface_id for bin_data in bins for surface_id in bin_data["surface_ids"]})

        result = {
            "line_ids": line_ids,
            "surface_ids": surface_ids,
            "bins": bins,
            "transition_band": self.doubleSpinBox_line_transition_band.value(),
            "refine_whole_faces": False,
            "refinement_length": min((bin_data["element_size"] for bin_data in bins), default=None),
        }
        self.mesher_inputs._apply_refinement_detection_result(result)
        self.label_line_send_status.setText(f"Sent {len(line_ids)} line(s) in {len(bins)} size group(s).")

    def _small_area_mode_changed(self, button: QPushButton):
        self.small_area_mode = button.property("mode")
        self.doubleSpinBox_small_area_size_factor.setEnabled(self.small_area_mode == "custom")

    def _get_small_area_size_factor(self) -> float:
        factors = {"strict": 0.25, "medium": 0.5, "loose": 1.0}
        if self.small_area_mode == "custom":
            return self.doubleSpinBox_small_area_size_factor.value()
        return factors[self.small_area_mode]

    def _get_element_area(self) -> float:
        minimum_size = convert_length_unit(self.minimum_element_size, self.mesh.length_unit, "meter")
        return minimum_size**2

    def _update_small_area_threshold(self):
        self.doubleSpinBox_small_area_size_factor.setEnabled(self.small_area_mode == "custom")
        threshold = self.doubleSpinBox_small_area_custom_factor.value() * self._get_element_area()
        length_factor = convert_length_unit(1.0, "meter", self.mesh.length_unit)
        threshold_display = threshold * length_factor**2
        unit_label = self.length_unit_label
        self.label_small_area_threshold.setText(
            f"Faces with area <= {threshold_display:.6g} {unit_label}² are selected."
        )
        self.small_area_result = []
        self.list_small_areas.clear()
        self.label_small_areas_count.setText("No small areas detected.")
        self.pushButton_send_small_areas.setDisabled(True)

    def _detect_small_areas(self):
        threshold = self.doubleSpinBox_small_area_custom_factor.value() * self._get_element_area()
        selected = [
            (surface_id, area)
            for surface_id, area in self.mesh.area_from_surfaces.items()
            if 0 < area <= threshold
        ]
        selected.sort(key=lambda item: item[1])

        self.small_area_result = selected
        self.list_small_areas.clear()

        length_factor = convert_length_unit(1.0, "meter", self.mesh.length_unit)
        area_factor = length_factor**2
        unit_label = self.length_unit_label
        for surface_id, area in selected:
            self.list_small_areas.addItem(f"Face {surface_id}: {area * area_factor:.6g} {unit_label}²")

        self.label_small_areas_count.setText(f"{len(selected)} small face(s) detected.")
        self.pushButton_send_small_areas.setDisabled(not selected)

        if selected:
            surface_ids = [surface_id for surface_id, _ in selected]
            app().main_window.selection.set_geometry_selection(surfaces=surface_ids)

    def _send_small_areas_to_refinement(self):
        if not getattr(self, "small_area_result", None):
            return

        groups = []
        for index, (surface_id, area) in enumerate(self.small_area_result):
            groups.append({
                "line_id": index,
                "line_length": area**0.5,
                "smallest_surface_id": surface_id,
                "surface_ids": [surface_id],
            })

        bins = self.mesh.group_refinement_sizes(
            groups,
            max_bins=self.spinBox_small_area_size_bins.value(),
            merge_ratio=self.doubleSpinBox_small_area_size_ratio.value(),
            representative="median",
            size_multiplier=self._get_small_area_size_factor(),
        )

        surface_ids = sorted({surface_id for bin_data in bins for surface_id in bin_data["surface_ids"]})
        if not surface_ids:
            return

        transition_band = self.doubleSpinBox_small_area_transition_band.value()
        result = {
            "line_ids": [],
            "surface_ids": surface_ids,
            "bins": bins,
            "transition_band": transition_band,
            "refine_whole_faces": True,
            "refinement_length": min((bin_data["element_size"] for bin_data in bins), default=None),
        }
        self.mesher_inputs._apply_refinement_detection_result(result)
        self.label_small_areas_count.setText(
            f"Sent {len(surface_ids)} face(s) in {len(bins)} size group(s) to refinement."
        )

    def _point_mode_changed(self, button: QPushButton):
        self.point_mode = button.property("mode")
        self._update_points_threshold()

    def _get_point_factor(self) -> float:
        factors = {"strict": 0.25, "medium": 0.5, "loose": 0.75}
        if self.point_mode == "custom":
            return self.doubleSpinBox_point_custom_factor.value() / 100.0
        return factors[self.point_mode]

    def _update_points_threshold(self):
        self.doubleSpinBox_point_custom_factor.setEnabled(self.point_mode == "custom")
        unit_label = self.length_unit_label
        self.label_points_threshold.setText(
            f"Point pairs closer than {self.minimum_element_size:.6g} {unit_label} are selected; "
            f"element size = {self._get_point_factor():.3g}x distance."
        )
        self.point_target_sizes = {}
        self.list_points.clear()
        self.label_points_count.setText("No close point pairs detected.")
        self.pushButton_send_points.setDisabled(True)

    def _point_coordinates(self):
        import numpy as np

        node_index = {
            int(node_id): index
            for index, node_id in enumerate(self.mesh.nodal_coordinates[:, 0])
        }
        point_ids = sorted(self.mesh.nodes_from_points)
        coordinates = np.array([
            self.mesh.nodal_coordinates[node_index[self.mesh.nodes_from_points[point_id]], 1:]
            for point_id in point_ids
        ])
        return point_ids, coordinates

    def _detect_close_points(self):
        import numpy as np
        from scipy.spatial import cKDTree

        point_ids, coordinates = self._point_coordinates()
        if len(point_ids) < 2:
            self.label_points_count.setText("Not enough points to analyze.")
            return

        maximum_distance = convert_length_unit(self.minimum_element_size, self.mesh.length_unit, "meter")
        tree = cKDTree(coordinates)
        pairs = tree.query_pairs(maximum_distance, output_type="ndarray")

        factor = self._get_point_factor()
        pair_results = []
        point_sizes = {}

        for index_1, index_2 in pairs:
            distance = float(np.linalg.norm(coordinates[index_1] - coordinates[index_2]))
            if distance <= 0:
                continue

            point_1 = point_ids[int(index_1)]
            point_2 = point_ids[int(index_2)]
            target_size = distance * factor
            pair_results.append((point_1, point_2, distance, target_size))

            for point_id in (point_1, point_2):
                current = point_sizes.get(point_id)
                if current is None or target_size < current:
                    point_sizes[point_id] = target_size

        pair_results.sort(key=lambda item: item[2])
        self.point_pair_results = pair_results
        self.point_target_sizes = point_sizes
        self.list_points.clear()

        unit_label = self.length_unit_label
        for point_1, point_2, distance, target_size in pair_results:
            distance_display = convert_length_unit(distance, "meter", self.mesh.length_unit)
            size_display = convert_length_unit(target_size, "meter", self.mesh.length_unit)
            self.list_points.addItem(
                f"Points {point_1} <-> {point_2}: distance {distance_display:.6g} {unit_label}, "
                f"element size {size_display:.6g} {unit_label}"
            )

        self.label_points_count.setText(
            f"{len(pair_results)} close pair(s), {len(point_sizes)} point(s) selected."
        )
        self.pushButton_send_points.setDisabled(not point_sizes)

    def _send_points_to_refinement(self):
        if not getattr(self, "point_target_sizes", None):
            return

        from statistics import median

        point_ids = sorted(self.point_target_sizes)
        element_size = median(self.point_target_sizes.values())
        size_model = convert_length_unit(element_size, "meter", self.mesh.length_unit)
        transition_band = self.doubleSpinBox_point_transition_band.value()

        self.mesher_inputs._add_local_mesh_size_control("points", size_model, point_ids, transition_band)
        app().main_window.selection.set_geometry_selection(points=point_ids)
        app().main_window.entity_visibility.unhide_all()
        self.label_points_count.setText(f"Sent {len(point_ids)} point(s) to refinement.")

    def done(self, result):
        app().main_window.clear_refinement_detection_lines()
        app().main_window.set_input_widget(self.mesher_inputs)

        if self.detection_result is None:
            app().main_window.entity_visibility.unhide_all()

        super().done(result)
