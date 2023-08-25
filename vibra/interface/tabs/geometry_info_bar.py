import typing

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vibra.utils.interface_functions import get_main_window


class GeometryInfoBar(QWidget):
    def __init__(self):
        super().__init__()

        self.main_window = get_main_window()
        self.project = self.main_window.project
        self.mesh = self.project.model.mesh

        self.number_of_points = None
        self.number_of_curves = None
        self.number_of_surfaces = None
        self.number_of_volumes = None

        self._define_qt_variables()

    def _define_qt_variables(self):
        #
        self.frame_spacer = QFrame()
        #
        self.label_number_of_points = QLabel(f"Number of points: {self.number_of_points}")
        self.label_number_of_curves = QLabel(f"Number of curves: {self.number_of_curves}")
        self.label_number_of_surfaces = QLabel(f"Number of surfaces: {self.number_of_surfaces}")
        self.label_number_of_volumes = QLabel(f"Number of volumes: {self.number_of_volumes}")
        #
        analysis_info_layout = QGridLayout()
        layout = QHBoxLayout()
        #
        self._config_widgets()
        #
        analysis_info_layout.addWidget(self.frame_spacer, 0, 0)
        analysis_info_layout.addWidget(self.label_number_of_points, 0, 1)
        analysis_info_layout.addWidget(self.label_number_of_curves, 0, 2)
        analysis_info_layout.addWidget(self.label_number_of_surfaces, 0, 3)
        analysis_info_layout.addWidget(self.label_number_of_volumes, 0, 4)
        #
        layout.addLayout(analysis_info_layout)
        self.setLayout(layout)
        self.setContentsMargins(2, 0, 2, 0)
        self.setStyleSheet("border: 1px solid")
        layout.setContentsMargins(0, 0, 0, 0)

    def _config_widgets(self):
        height = 28

        self.setMinimumHeight(height + 0)
        self.setMaximumHeight(height + 0)

        self.frame_spacer.setMinimumHeight(height)
        self.frame_spacer.setMaximumHeight(height)

        # self.label_number_of_points.setAlignment(Qt.AlignRight)
        self.label_number_of_points.setMinimumSize(100, height)
        self.label_number_of_points.setMaximumSize(200, height)

        self.label_number_of_curves.setMinimumSize(100, height)
        self.label_number_of_curves.setMaximumSize(200, height)

        self.label_number_of_surfaces.setMinimumSize(100, height)
        self.label_number_of_surfaces.setMaximumSize(200, height)

        self.label_number_of_volumes.setMinimumSize(100, height)
        self.label_number_of_volumes.setMaximumSize(200, height)
