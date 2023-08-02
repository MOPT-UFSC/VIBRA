import typing
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from pathlib import Path
from vibra.utils.icons import load_icon


class AcousticModalAnalysisBar(QWidget):
    slider_pressed = pyqtSignal()
    slider_released = pyqtSignal()
    value_changed = pyqtSignal()


    # value_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Avoid using fixed sizes for all widgets!!

        self.create_sliders()

        self.play_icon = load_icon(Path("data/icons/play.png"), QColor("#0055DD"))
        self.pause_icon = load_icon(Path("data/icons/pause.png"), QColor("#0055DD"))
        self.play_pause_button = QPushButton(self.play_icon, "")
        self.play_pause_button.setShortcut("Space")
        self.play_pause_button.setMinimumWidth(80)

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
        layout.addStretch()
        
        layout.addWidget(QLabel("Mode Selector:"))
        layout.addWidget(self.frequency_box)
        self.setLayout(layout)

        self.frequency_box.activated.connect(self.value_changed.emit)
        self.real_part_button.clicked.connect(self.value_changed.emit)
        self.absolute_button.clicked.connect(self.value_changed.emit)

    def use_play_icon(self):
        self.play_pause_button.setIcon(self.play_icon)

    def use_pause_icon(self):
        self.play_pause_button.setIcon(self.pause_icon)

    def set_frequencies(self, frequencies):
        self.frequency_box.clear()

        if frequencies is None:
            return

        for i, freq in enumerate(frequencies):
            self.frequency_box.addItem(f" Mode {i + 1}: {round(freq, 6)} Hz")

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


class StructuralModalAnalysisBar(QWidget):
    slider_pressed = pyqtSignal()
    slider_released = pyqtSignal()
    value_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Avoid using fixed sizes for all widgets!!

        self.create_sliders()

        self.play_icon = load_icon(Path("data/icons/play.png"), QColor("#0055DD"))
        self.pause_icon = load_icon(Path("data/icons/pause.png"), QColor("#0055DD"))
        self.play_pause_button = QPushButton(self.play_icon, "")
        self.play_pause_button.setShortcut("Space")
        self.play_pause_button.setMinimumWidth(80)

        self.frequency_box = QComboBox()
        self.response_ux_button = QRadioButton("Real Ux")
        self.response_uy_button = QRadioButton("Real Uy")
        self.response_uz_button = QRadioButton("Real Uz")
        self.sum_button = QRadioButton("Sum")
        self.show_mesh_button = QCheckBox("Show mesh")
        self.update_coloring = QCheckBox("Update coloring")
        self.sum_button.setChecked(True)
        self.show_mesh_button.setChecked(True)
        self.update_coloring.setChecked(True)
        self.update_coloring.stateChanged.connect(self.value_changed)

        button_group = QButtonGroup()
        button_group.addButton(self.response_ux_button)
        button_group.addButton(self.response_uy_button)
        button_group.addButton(self.response_uz_button)
        button_group.addButton(self.sum_button)
        self.frequency_box.setMinimumWidth(180)
        self.frequency_box.setMaximumWidth(300)


        sliders_layout = QGridLayout()
        sliders_layout.addWidget(QLabel("Magnification factor:"), 0, 0)
        sliders_layout.addWidget(self.magnification_factor_slider, 0, 1)
        sliders_layout.addWidget(self.magnification_factor_label, 0, 2)
        sliders_layout.addWidget(QLabel("Phase [deg]:"), 1, 0)
        sliders_layout.addWidget(self.phase_slider, 1, 1)
        sliders_layout.addWidget(self.phase_label, 1, 2)

        plot_layout = QHBoxLayout()
        # plot_layout.addWidget(QLabel("Data to plot:"))
        plot_layout.addWidget(self.sum_button)
        plot_layout.addWidget(self.response_ux_button)
        plot_layout.addWidget(self.response_uy_button)
        plot_layout.addWidget(self.response_uz_button)
        plot_layout.setSpacing(20)

        config_layout = QHBoxLayout()
        config_layout.addWidget(self.show_mesh_button)
        config_layout.addWidget(self.update_coloring)
        config_layout.addStretch()
        config_layout.addWidget(self.play_pause_button)

        buttons_layout = QVBoxLayout()
        buttons_layout.addLayout(plot_layout)
        buttons_layout.addLayout(config_layout)


        layout = QHBoxLayout()
        layout.addLayout(sliders_layout)
        # layout.addStretch()
        layout.addLayout(buttons_layout)
        layout.addStretch()
        layout.addWidget(QLabel("Mode Selector:"))
        layout.addWidget(self.frequency_box)
        self.setLayout(layout)

        self.frequency_box.activated.connect(self.value_changed.emit)
        self.response_ux_button.clicked.connect(self.value_changed.emit)
        self.response_uy_button.clicked.connect(self.value_changed.emit)
        self.response_uz_button.clicked.connect(self.value_changed.emit)
        self.sum_button.clicked.connect(self.value_changed.emit)

    def set_frequencies(self, frequencies):
        self.frequency_box.clear()

        if frequencies is None:
            return

        for i, freq in enumerate(frequencies):
            self.frequency_box.addItem(f" Mode {i + 1}: {round(freq, 6)} Hz")

    def use_play_icon(self):
        self.play_pause_button.setIcon(self.play_icon)

    def use_pause_icon(self):
        self.play_pause_button.setIcon(self.pause_icon)

    def create_sliders(self):
        #
        self.magnification_factor_label = QLabel("value")
        self.magnification_factor_label.setFixedWidth(60)
        self.magnification_factor_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.magnification_factor_slider = QSlider(Qt.Orientation.Horizontal)
        self.magnification_factor_slider.setMinimum(0)
        self.magnification_factor_slider.setMaximum(4)
        self.magnification_factor_slider.setValue(2)
        self.magnification_factor_slider.setSingleStep(1)
        self.magnification_factor_slider.setMaximumWidth(200)
        self.magnification_factor_slider.valueChanged.connect(self.value_change_callback)
        self.magnification_factor_slider.sliderPressed.connect(self.slider_pressed.emit)
        self.magnification_factor_slider.sliderReleased.connect(self.slider_released.emit)
        self.magnification_factor_label.setText(f"({self.magnification_factor_slider.value()}x)")
        #
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
        #

    def value_change_callback(self):
        self.magnification_factor_label.setText(f"({self.magnification_factor_slider.value()}x)")
        self.phase_label.setText(f"({self.phase_slider.value()}°)")
        self.value_changed.emit()