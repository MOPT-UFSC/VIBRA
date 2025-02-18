from pathlib import Path

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vibra import ICON_DIR
from vibra.utils.icons import load_icon


class StructuralModalAnalysisBar(QWidget):
    slider_pressed = pyqtSignal()
    slider_released = pyqtSignal()
    value_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Avoid using fixed sizes for all widgets!!

        self.create_sliders()

        self.play_icon = load_icon(ICON_DIR / "play.png", QColor("#0055DD"))
        self.pause_icon = load_icon(ICON_DIR / "pause.png", QColor("#0055DD"))
        self.play_pause_button = QPushButton(self.play_icon, "")
        self.play_pause_button.setShortcut("Space")
        self.play_pause_button.setToolTip("Play animation")
        self.play_pause_button.setMinimumWidth(80)

        self.create_video_icon = load_icon(ICON_DIR / "create_video_icon.png", QColor("#0055DD"))
        self.create_video_button = QPushButton(self.create_video_icon, "")
        self.create_video_button.setToolTip("Create video")
        self.create_video_button.setMinimumWidth(80)

        self.show_mesh_button = QCheckBox("Show mesh")

        self.show_mesh_button.setChecked(True)

        sliders_layout = QGridLayout()
        sliders_layout.addWidget(QLabel("Magnification factor:"), 0, 0)
        sliders_layout.addWidget(self.magnification_factor_slider, 0, 1)
        sliders_layout.addWidget(self.magnification_factor_label, 0, 2)
        sliders_layout.addWidget(QLabel("Phase [deg]:"), 1, 0)
        sliders_layout.addWidget(self.phase_slider, 1, 1)
        sliders_layout.addWidget(self.phase_label, 1, 2)

        config_layout = QHBoxLayout()
        config_layout.addWidget(self.show_mesh_button)
        config_layout.addStretch()
        config_layout.addWidget(self.play_pause_button)
        config_layout.addWidget(self.create_video_button)

        buttons_layout = QVBoxLayout()
        buttons_layout.addLayout(config_layout)

        layout = QHBoxLayout()
        layout.addLayout(sliders_layout)
        # layout.addStretch()
        layout.addLayout(buttons_layout)
        layout.addStretch()
        self.setLayout(layout)

    def use_play_icon(self):
        self.play_pause_button.setIcon(self.play_icon)
        self.play_pause_button.setToolTip("Play animation")

    def use_pause_icon(self):
        self.play_pause_button.setIcon(self.pause_icon)
        self.play_pause_button.setToolTip("Pause animation")

    def create_sliders(self):

        self.magnification_factor_label = QLabel("value")
        self.magnification_factor_label.setFixedWidth(60)
        self.magnification_factor_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.magnification_factor_slider = QSlider(Qt.Orientation.Horizontal)
        self.magnification_factor_slider.setMinimum(0)
        self.magnification_factor_slider.setMaximum(32)
        self.magnification_factor_slider.setValue(16)
        self.magnification_factor_slider.setSingleStep(1)
        self.magnification_factor_slider.setMaximumWidth(200)
        self.magnification_factor_slider.valueChanged.connect(self.value_change_callback)
        self.magnification_factor_slider.sliderPressed.connect(self.slider_pressed.emit)
        self.magnification_factor_slider.sliderReleased.connect(self.slider_released.emit)
        self.magnification_factor_label.setText(f"({self.magnification_factor_slider.value() / 16}x)")

        self.phase_label = QLabel("value")
        self.phase_label.setFixedWidth(60)
        self.phase_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.phase_slider = QSlider(Qt.Orientation.Horizontal)
        self.phase_slider.setMinimum(0)
        self.phase_slider.setMaximum(360)
        self.phase_slider.setValue(0)
        self.phase_slider.setSingleStep(1)
        self.phase_slider.setMaximumWidth(200)
        self.phase_slider.valueChanged.connect(self.value_change_callback)
        self.phase_slider.sliderPressed.connect(self.slider_pressed.emit)
        self.phase_slider.sliderReleased.connect(self.slider_released.emit)
        self.phase_label.setText(f"({self.phase_slider.value()}°)")

    def value_change_callback(self):
        self.magnification_factor_label.setText(f"({self.magnification_factor_slider.value() / 16}x)")
        self.phase_label.setText(f"({self.phase_slider.value()}°)")
        self.value_changed.emit()