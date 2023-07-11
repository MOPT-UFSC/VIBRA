import typing
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ModalanalysisBar(QWidget):
    def __init__(self):
        super().__init__()

        self._define_qt_variables()      


    def _define_qt_variables(self):
        #
        self.show_mesh_button = QCheckBox("Show mesh")
        self.mode_box = QComboBox()
        self.frequency_box = QComboBox()
        #
        self.frame_spacer = QFrame()
        #
        self.label_mode_selector = QLabel("Mode selector:")
        self.label_color_scale = QLabel("Color scale:")
        #
        analysis_info_layout = QGridLayout()
        layout = QHBoxLayout()
        #
        self.absolute_button = QRadioButton("Absolute")
        self.real_part_button = QRadioButton("Real part")
        #
        self._config_widgets() 
        #
        analysis_info_layout.addWidget(self.frame_spacer, 0, 0)
        analysis_info_layout.addWidget(self.label_color_scale, 0, 1)
        analysis_info_layout.addWidget(self.real_part_button, 0, 2)
        analysis_info_layout.addWidget(self.absolute_button, 0, 3)
        analysis_info_layout.addWidget(self.show_mesh_button, 0, 4)
        analysis_info_layout.addWidget(self.label_mode_selector, 0, 5)
        analysis_info_layout.addWidget(self.frequency_box, 0, 6)
        #
        layout.addLayout(analysis_info_layout)
        self.setLayout(layout)
        self.setContentsMargins(2, 0, 2, 0)
        self.setStyleSheet("border: 1px solid")
        layout.setContentsMargins(0, 0, 0, 0)
        analysis_info_layout.setContentsMargins(0, 0, 0, 0)


    def _config_widgets(self):

        height = 28

        self.frame_spacer.setMinimumHeight(height)
        self.frame_spacer.setMaximumHeight(height)
        
        self.real_part_button.setMinimumSize(90, height)
        self.real_part_button.setMaximumSize(90, height)
        self.absolute_button.setMinimumSize(90, height)
        self.absolute_button.setMaximumSize(90, height)
        self.real_part_button.setChecked(True)

        self.show_mesh_button.setMinimumSize(100, height)
        self.show_mesh_button.setMaximumSize(100, height)
        
        # self.label_color_scale.setAlignment(Qt.AlignRight)
        self.label_color_scale.setMinimumSize(70, height)
        self.label_color_scale.setMaximumSize(70, height)

        # self.label_mode_selector.setAlignment(Qt.AlignRight)
        self.label_mode_selector.setMinimumSize(100, height)
        self.label_mode_selector.setMaximumSize(100, height)
        
        self.mode_box.setMinimumSize(160, height)
        self.mode_box.setMaximumSize(160, height)
        self.frequency_box.setMinimumSize(180, height)
        self.frequency_box.setMaximumSize(180, height)