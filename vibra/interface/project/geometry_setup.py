# fmt: off

from PySide6.QtCore import Qt

from vibra import app
from vibra.interface.ui_generated.project.geometry.geometry_setup_ui import GeometrySetup_UI

window_title_1 = "Error"
window_title_2 = "Warning"


class GeometrySetup(GeometrySetup_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self._create_connections()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.keep_window_open = True
        self.complete = False

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _create_connections(self):
        self.pushButton_proceed.clicked.connect(self.proceed_callback)
        self.pushButton_exit.clicked.connect(self.close)

    def get_geometry_quality_factor(self):
        quality_factors = [1.0, 0.5, 3.0]
        index = self.comboBox_geometry_quality.currentIndex()
        return quality_factors[index]

    def proceed_callback(self):

        length_unit = self.comboBox_length_units.currentText()
        app().project.model.set_length_unit(length_unit)

        quality_factor = self.get_geometry_quality_factor()
        app().project.model.set_geometry_quality_factor(quality_factor)

        self.complete = True
        self.close()

    def closeEvent(self, arg__1):
        self.keep_window_open = False
        return super().closeEvent(arg__1)
