from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QIcon
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QVBoxLayout

from vibra import app, ICON_DIR
from vibra.engine.mesher.element_type import (
    ElementType,
    TETRAHEDRON_4,
    TETRAHEDRON_10,
    HEXAHEDRON_8,
    HEXAHEDRON_20,
)

from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.ui_generated.model.general.advanced_element_options_input_ui import AdvancedElementOptionsInput_UI

import logging
import matplotlib.colors as mcolors
import numpy as np

from collections import defaultdict
from copy import deepcopy
from enum import IntEnum, StrEnum
from gmsh import isInitialized as is_gmsh_initialized


class TabIndex(IntEnum):
    HEX8 = 0
    HEX20 = 1
    TET4 = 2
    TET10 = 3


class ElementType(StrEnum):
    HEXAHEDRAL = "hexahedral"
    TETRAHEDRAL = "tetrahedral"


class ShapeFunction(StrEnum):
    LINEAR = "linear"
    QUADRATIC = "quadratic"


error_title = "Error"
warning_title = "Warning"


class AdvancedElementOptionsInputs(AdvancedElementOptionsInput_UI):
    def __init__(self, **kwargs):
        super().__init__()

        app().main_window.set_input_widget(self)
        self.model = app().project.model

        self._initialize()
        self._config_window()
        self._config_widgets()
        self._create_connections()
        self.update_tab_visibility()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.complete = False
        self.keep_window_open = True

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _config_widgets(self):
        # Hex8 - additional options
        self.label_option_2.setVisible(False)
        self.label_option_3.setVisible(False)
        self.comboBox_option_2.setVisible(False)
        self.comboBox_option_3.setVisible(False)

    def _create_connections(self):
        self.pushButton_confirm.clicked.connect(self.set_element_options_callback)
        self.pushButton_exit.clicked.connect(self.close)

    def load_advanced_options(self):

        advanced_element_options = self.model.properties._get_property("advanced_element_options")
        if not isinstance(advanced_element_options, dict):
            return

        if self.tabWidget_main.currentIndex() == TabIndex.HEX8:
            hex8_options = advanced_element_options.get("hex8", dict)
            if not isinstance(hex8_options, dict):
                return

            extra_shape_function = hex8_options.get("extra_shape_functions")
            self.comboBox_extra_shape_functions.setCurrentText("enabled" if extra_shape_function else "disabled")

    def update_tab_visibility(self):

        mesh_setup = app().project.model.mesh_setup
        if not isinstance(mesh_setup, dict):
            return
    
        ElementType = mesh_setup.get("ElementType")

        for i in range(4):
            self.tabWidget_main.setTabVisible(i, False)

        if ElementType == TETRAHEDRON_4:
            self.tabWidget_main.setTabVisible(TabIndex.TET4, True)

        elif ElementType == TETRAHEDRON_10:
            self.tabWidget_main.setTabVisible(TabIndex.TET10, True)

        elif ElementType == HEXAHEDRON_8:
            self.tabWidget_main.setTabVisible(TabIndex.HEX8, True)

        elif ElementType == HEXAHEDRON_20:
            self.tabWidget_main.setTabVisible(TabIndex.HEX20, True)

        else:
            NotImplementedError("Invalid ElementType")
            return
        
        self.load_advanced_options()

    def set_element_options_callback(self):
        advanced_options = dict()
        if self.tabWidget_main.currentIndex() == TabIndex.HEX8:
            advanced_options["hex8"] = {
                "extra_shape_functions" : self.comboBox_extra_shape_functions.currentText() == "enabled"
                }

        if not advanced_options:
            return

        self.model.properties._set_property("advanced_element_options", advanced_options)
        app().file.write_model_properties_in_file()

        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.close()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)