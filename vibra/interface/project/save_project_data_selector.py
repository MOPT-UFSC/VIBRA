# fmt: off
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app, TEMP_PROJECT_DIR
from vibra.interface.ui_generated.project.save_project_data_selector_ui import SaveProjectDataSelector_UI

import os

window_title_1 = "Error"
window_title_2 = "Warning"


class SaveProjectDataSelector(SaveProjectDataSelector_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._configure_qt_variables()
        self._create_connections()

        self.get_required_memory()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.keep_window_open = True
        self.complete = False

    def _configure_qt_variables(self):
        self.lineEdit_required_memory.setDisabled(True)

    def _create_connections(self):
        #
        self.checkBox_mesh_data.stateChanged.connect(self.remove_solution_data)
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_proceed.clicked.connect(self.proceed_callback)

    def get_required_memory(self):
        if TEMP_PROJECT_DIR.exists():
            size_of_file = get_folder_size(TEMP_PROJECT_DIR) / 1e6
            self.lineEdit_required_memory.setText(f"{size_of_file:.4}")

    def remove_solution_data(self):
        if self.checkBox_mesh_data.isChecked():
            self.checkBox_solution_data.setDisabled(False)
        else:
            self.checkBox_solution_data.setChecked(False)
            self.checkBox_solution_data.setDisabled(True)

    def proceed_callback(self):

        self.ignore_results_data = False
        if not self.checkBox_solution_data.isChecked():
            self.ignore_results_data = True
        
        self.ignore_mesh_data = False
        if not self.checkBox_mesh_data.isChecked():
            self.ignore_mesh_data = True

        self.complete = True
        self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)
    

def get_folder_size(path: Path):
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())

# fmt: on