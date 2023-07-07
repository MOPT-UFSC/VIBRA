import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QComboBox, QButtonGroup, QRadioButton, QSpacerItem


class ModalAnalisysBar(QWidget):
    def __init__(self):
        super().__init__()

        self.mode_box = QComboBox()
        self.frequency_box = QComboBox()
        self.mode_box.setMinimumWidth(200)
        self.frequency_box.setMinimumWidth(200)

        real_part_button = QRadioButton("Real Part")
        absolute_button = QRadioButton("Absolute")
        button_group = QButtonGroup()
        button_group.addButton(real_part_button)
        button_group.addButton(absolute_button)

        color_scaling_layout = QVBoxLayout()
        color_scaling_layout.addWidget(real_part_button)
        color_scaling_layout.addWidget(absolute_button)

        analisys_info_layout = QGridLayout()
        analisys_info_layout.addWidget(QLabel("Mode"), 0, 0)
        analisys_info_layout.addWidget(self.mode_box, 1, 0)
        analisys_info_layout.addWidget(QLabel("Natural Frequency"), 0, 1)
        analisys_info_layout.addWidget(self.frequency_box, 1, 1)

        layout = QHBoxLayout()
        layout.addLayout(analisys_info_layout)
        layout.addLayout(color_scaling_layout)
        layout.addStretch()
        self.setLayout(layout)
