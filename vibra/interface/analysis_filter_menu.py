from PyQt5.QtWidgets import*
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from vibra.utils.interface_functions import get_main_window


class AnalysisFilter(QWidget):
    def __init__(self):
        super().__init__()

        self.main_window = get_main_window()

        self.frame = QFrame()
        self.frame_main = QFrame()
        self.frame_buttons = QFrame()

        self.line = QFrame()
        self.line.setLineWidth(2)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.label_main = QLabel("Analysis type selector", self)
        self.label_main.setMinimumSize(QSize(270, 30))
        self.label_main.setMaximumSize(QSize(270, 30))
        self.label_main.setStyleSheet("font: 50 bold 11pt")
        self.label_main.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        grid_main = QGridLayout()
        grid_main.addWidget(self.label_main, 0, 0)
        grid_main.addWidget(self.line, 1, 0)
        grid_main.setContentsMargins(0, 0, 0, 0)
        self.frame_main.setLayout(grid_main)

        self.radio_button_acoustic = QRadioButton("Acoustic", self)
        self.radio_button_structural = QRadioButton("Structural", self)
        self.radio_button_coupled = QRadioButton("Coupled", self)
        #
        self.radio_button_acoustic.setStyleSheet("font: 10pt")
        self.radio_button_structural.setStyleSheet("font: 10pt")
        self.radio_button_coupled.setStyleSheet("font: 10pt")
        self.radio_button_acoustic.setChecked(True)
        #
        self.radio_button_acoustic.setFixedHeight(30)
        self.radio_button_structural.setFixedHeight(30)
        self.radio_button_coupled.setFixedHeight(30)
        #
        self.radio_button_acoustic.clicked.connect(self.main_window.menu_widget.filter_analysis_type)
        self.radio_button_structural.clicked.connect(self.main_window.menu_widget.filter_analysis_type)
        self.radio_button_coupled.clicked.connect(self.main_window.menu_widget.filter_analysis_type)
        #

        group = QButtonGroup()
        group.addButton(self.radio_button_acoustic)
        group.addButton(self.radio_button_structural)
        group.addButton(self.radio_button_coupled)
        
        grid_buttons = QHBoxLayout()
        grid_buttons.addWidget(self.radio_button_acoustic)
        grid_buttons.addWidget(self.radio_button_structural)
        grid_buttons.addWidget(self.radio_button_coupled)
        grid_buttons.setContentsMargins(2, 0, 2, 0)
        self.frame_buttons.setLayout(grid_buttons)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.frame_main, 0, 0)
        grid_layout.addWidget(self.line, 1, 0)
        grid_layout.addWidget(self.frame_buttons, 2, 0)
        #
        self.frame.setLayout(grid_layout)
        self.frame.setContentsMargins(0, 0, 0, 0)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setVerticalSpacing(2)

        grid_layout2 = QGridLayout()
        grid_layout2.addWidget(self.frame, 0, 0)
        grid_layout2.setVerticalSpacing(2)
        self.setLayout(grid_layout2)
        grid_layout2.setContentsMargins(4, 2, 4, 2)
        
        self.setMinimumSize(QSize(280, 80))
        self.setMaximumSize(QSize(280, 80))