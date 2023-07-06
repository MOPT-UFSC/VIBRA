import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QGridLayout, QHBoxLayout, QWidget, QComboBox, QButtonGroup, QRadioButton


class ModalAnalisysBar(QWidget):
    def __init__(self):
        super().__init__()

        self.mode_box = QComboBox()
        self.frequency_box = QComboBox()

        real_part_button = QRadioButton("Real Part")
        absolute_button = QRadioButton("Absolute")
        color_scaling_layout = QButtonGroup()
        color_scaling_layout.addButton(real_part_button)
        color_scaling_layout.addButton(absolute_button)

        # color_scaling_layout = QGridLayout()
        # color_scaling_layout.addWidget(QLabel("Color Scaling Setup"), 0, 0)
        # color_scaling_layout.addWidget(QLabel("Real Part"), 1, 0)
        # color_scaling_layout.addWidget(QLabel("Absolute"), 1, 1)

        analisys_info_layout = QGridLayout()
        analisys_info_layout.addWidget(QLabel("Mode"), 0, 0)
        analisys_info_layout.addWidget(self.mode_box, 1, 0)
        analisys_info_layout.addWidget(QLabel("Natural Frequency"), 0, 1)
        analisys_info_layout.addWidget(self.frequency_box, 1, 1)

        layout = QHBoxLayout()
        layout.addWidget(real_part_button)
        layout.addWidget(absolute_button)
        layout.addLayout(analisys_info_layout)
        self.setLayout(layout)
