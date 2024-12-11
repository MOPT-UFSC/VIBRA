import typing

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vibra import app
from vibra.utils.interface_functions import get_main_window


class GeometryInfoBar(QWidget):
    def __init__(self):
        super().__init__()

        self.project = app().project
        self.mesh = self.project.model.mesh

        self.number_of_points = ""
        self.number_of_curves = ""
        self.number_of_surfaces = ""
        self.number_of_volumes = ""

        self._define_qt_variables()

    def _define_qt_variables(self):
        #
        self.frame_spacer = QFrame()
        #
        self.label_number_of_points = QLabel(f"Points: \t")
        self.label_number_of_curves = QLabel(f"Curves: \t")
        self.label_number_of_surfaces = QLabel(f"Surfaces: \t")
        self.label_number_of_volumes = QLabel(f"Volumes: \t")
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
        # self.setStyleSheet("border: 1px solid")
        layout.setContentsMargins(0, 0, 0, 0)

    def _config_widgets(self):
        height = 28

        self.setMinimumHeight(height + 0)
        self.setMaximumHeight(height + 0)

        self.frame_spacer.setMinimumHeight(height)
        self.frame_spacer.setMaximumHeight(height)

        # self.label_number_of_points.setAlignment(Qt.AlignRight)
        self.label_number_of_points.setMinimumSize(80, height)
        self.label_number_of_points.setMaximumSize(160, height)

        self.label_number_of_curves.setMinimumSize(80, height)
        self.label_number_of_curves.setMaximumSize(160, height)

        self.label_number_of_surfaces.setMinimumSize(80, height)
        self.label_number_of_surfaces.setMaximumSize(160, height)

        self.label_number_of_volumes.setMinimumSize(80, height)
        self.label_number_of_volumes.setMaximumSize(160, height)

    def update_geometry_information(self):
        points, curves, surfaces, volumes = app().project.model.mesh.get_geometry_info()
        self.label_number_of_points.setText(f"Points: {points}")
        self.label_number_of_curves.setText(f"Curves: {curves}")
        self.label_number_of_surfaces.setText(f"Surfaces: {surfaces}")
        self.label_number_of_volumes.setText(f"Volumes: {volumes}")
