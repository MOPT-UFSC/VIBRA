
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QRadioButton,
    QSlider,
    QWidget,
)
from PySide6.QtGui import QIcon

from vibra import app
from vibra.engine import AnalysisID


class AcousticModalAnalysisBar(QWidget):
    slider_pressed = Signal()
    slider_released = Signal()
    value_changed = Signal()

    def __init__(self):
        super().__init__()
        # Avoid using fixed sizes for all widgets!!

        self.create_sliders()

        self.play_icon = QIcon(":/icons/play.png")
        self.pause_icon = QIcon(":/icons/pause.png")
        self.play_pause_button = QPushButton(self.play_icon, "")
        self.play_pause_button.setToolTip("Play animation")
        self.play_pause_button.setShortcut("Space")
        self.play_pause_button.setMinimumWidth(80)

        self.create_video_icon = QIcon(":/icons/create_video_icon.png")
        self.create_video_button = QPushButton(self.create_video_icon, "")
        self.create_video_button.setToolTip("Create video")
        self.create_video_button.setMinimumWidth(80)

        self.frequency_box = QComboBox()
        self.absolute_button = QRadioButton("Absolute")
        self.real_part_button = QRadioButton("Real part")
        self.show_mesh_button = QCheckBox("Show mesh")

        button_group = QButtonGroup()
        button_group.addButton(self.real_part_button)
        button_group.addButton(self.absolute_button)
        self.frequency_box.setMinimumWidth(180)
        self.frequency_box.setMaximumWidth(300)
        self.real_part_button.setChecked(True)
        self.show_mesh_button.setChecked(True)

        hspacing = 20

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Phase [deg]:"))
        layout.addWidget(self.phase_slider)
        layout.addWidget(self.phase_label)
        layout.addSpacing(hspacing)

        layout.addWidget(QLabel("Color Scale:"))
        layout.addWidget(self.absolute_button)
        layout.addWidget(self.real_part_button)
        layout.addSpacing(hspacing)

        layout.addWidget(self.show_mesh_button)
        layout.addSpacing(hspacing)

        layout.addWidget(self.play_pause_button)
        layout.addWidget(self.create_video_button)
        layout.addStretch()

        self.selector_label = QLabel("List of results:")

        layout.addWidget(self.selector_label)
        layout.addWidget(self.frequency_box)
        self.setLayout(layout)

        self.frequency_box.activated.connect(self.value_changed.emit)
        self.real_part_button.clicked.connect(self.value_changed.emit)
        self.absolute_button.clicked.connect(self.value_changed.emit)

    def use_play_icon(self):
        self.play_pause_button.setIcon(self.play_icon)
        self.play_pause_button.setToolTip("Play animation")

    def use_pause_icon(self):
        self.play_pause_button.setIcon(self.pause_icon)
        self.play_pause_button.setToolTip("Pause animation")

    def set_frequencies(self, frequencies):
        self.frequency_box.clear()

        if frequencies is None:
            return

        if app().project.model.analysis_id == AnalysisID.ACOUSTIC_MODAL:
            prefix = "Mode"
        else:
            prefix = "Frequency"

        for i, freq in enumerate(frequencies):
            self.frequency_box.addItem(f" {prefix} {i + 1}: {round(freq, 6)} Hz")

    def create_sliders(self):
        self.phase_label = QLabel("value")
        self.phase_label.setMaximumWidth(60)
        self.phase_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.phase_slider = QSlider(Qt.Orientation.Horizontal)
        self.phase_slider.setMinimum(0)
        self.phase_slider.setMaximum(360)
        self.phase_slider.setValue(0)
        self.phase_slider.setSingleStep(1)
        self.phase_slider.setMaximumWidth(200)

        self.phase_slider.sliderPressed.connect(self.slider_pressed.emit)
        self.phase_slider.sliderReleased.connect(self.slider_released.emit)
        self.phase_slider.valueChanged.connect(self.value_change_callback)
        self.phase_label.setText(f"({self.phase_slider.value()}°)")

    def value_change_callback(self):
        self.phase_label.setText(f"({self.phase_slider.value()}°)")
        self.value_changed.emit()