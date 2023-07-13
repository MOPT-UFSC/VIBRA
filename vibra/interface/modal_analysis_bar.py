import typing
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class AcousticModalAnalysisBar(QWidget):
    plot_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Avoid using fixed sizes for all widgets!!

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

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(QLabel("Color Scale:"))
        layout.addWidget(self.absolute_button)
        layout.addWidget(self.real_part_button)
        layout.addSpacing(100)
        layout.addWidget(self.show_mesh_button)
        layout.addSpacing(100)
        layout.addWidget(QLabel("Mode Selector:"))
        layout.addWidget(self.frequency_box)
        self.setLayout(layout)

        self.frequency_box.activated.connect(self.plot_changed.emit)
        self.real_part_button.clicked.connect(self.plot_changed.emit)
        self.absolute_button.clicked.connect(self.plot_changed.emit)

    def set_frequencies(self, frequencies):
        self.frequency_box.clear()

        if frequencies is None:
            return

        for i, freq in enumerate(frequencies):
            self.frequency_box.addItem(f" Mode {i + 1}: {round(freq, 6)} Hz")


class StructuralModalAnalysisBar(QWidget):
    plot_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Avoid using fixed sizes for all widgets!!

        self.frequency_box = QComboBox()
        self.response_ux_button = QRadioButton("Real Ux")
        self.response_uy_button = QRadioButton("Real Uy")
        self.response_uz_button = QRadioButton("Real Uz")
        self.absolute_button = QRadioButton("Absolute")
        self.show_mesh_button = QCheckBox("Show mesh")

        button_group = QButtonGroup()
        button_group.addButton(self.response_ux_button)
        button_group.addButton(self.response_uy_button)
        button_group.addButton(self.response_uz_button)
        button_group.addButton(self.absolute_button)
        self.frequency_box.setMinimumWidth(180)
        self.frequency_box.setMaximumWidth(300)
        self.absolute_button.setChecked(True)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(QLabel("Color Scale:"))
        layout.addWidget(self.absolute_button)
        layout.addWidget(self.response_ux_button)
        layout.addWidget(self.response_uy_button)
        layout.addWidget(self.response_uz_button)
        layout.addSpacing(100)
        layout.addWidget(self.show_mesh_button)
        layout.addSpacing(100)
        layout.addWidget(QLabel("Mode Selector:"))
        layout.addWidget(self.frequency_box)
        self.setLayout(layout)

        self.frequency_box.activated.connect(self.plot_changed.emit)
        self.response_ux_button.clicked.connect(self.plot_changed.emit)
        self.response_uy_button.clicked.connect(self.plot_changed.emit)
        self.response_uz_button.clicked.connect(self.plot_changed.emit)
        self.absolute_button.clicked.connect(self.plot_changed.emit)

    def set_frequencies(self, frequencies):
        self.frequency_box.clear()

        if frequencies is None:
            return

        for i, freq in enumerate(frequencies):
            self.frequency_box.addItem(f" Mode {i + 1}: {round(freq, 6)} Hz")