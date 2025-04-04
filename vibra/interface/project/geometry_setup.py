# fmt: off

from PySide6.QtWidgets import QCheckBox, QComboBox, QDialog, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app, UI_DIR, TEMP_PROJECT_FILE

from molde import load_ui

import os

window_title_1 = "Error"
window_title_2 = "Warning"


class GeometrySetup(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "project/geometry/geometry_setup.ui"
        load_ui(ui_path, self, ui_path.parent)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)

        self._initialize()
        self._list_qt_variables()
        self._create_connections()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.keep_window_open = True
        self.complete = False

    def _list_qt_variables(self):
        self.pushButton_exit: QPushButton
        self.pushButton_proceed: QPushButton

    def _create_connections(self):
        self.pushButton_proceed.clicked.connect(self.proceed_callback)
        self.pushButton_exit.clicked.connect(self.close)

    def proceed_callback(self):
        print("pushButton_pressed")
        self.complete = True
        self.close()

    def closeEvent(self, arg__1):
        self.keep_window_open = False
        return super().closeEvent(arg__1)
