
from PySide6.QtWidgets import QDialog, QPushButton, QWidget
from PySide6.QtCore import Qt

from vibra import app, UI_DIR
from molde import load_ui

from pathlib import Path

class ShowPorousMaterialModelEquations(QDialog):
    def __init__(self, file_path: str | Path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / str(file_path)
        load_ui(ui_path, self, ui_path.parent)

        self._config_window()
        self._define_qt_variables()
        self._create_connections()

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Vibra")

    def _define_qt_variables(self):
        self.pushButton_exit: QPushButton

    def _create_connections(self):
        self.pushButton_exit.clicked.connect(self.close)