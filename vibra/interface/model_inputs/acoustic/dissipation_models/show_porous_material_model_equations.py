from PySide6.QtCore import Qt

from vibra import app
from vibra.interface.ui_generated.model.acoustic.dissipation_models.equations_for_DBM_porous_material_models_ui import EquationsForDbmPorousMaterialModels_UI


class ShowPorousMaterialModelEquations(EquationsForDbmPorousMaterialModels_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config_window()
        self._create_connections()

        self.exec()

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Vibra")

    def _create_connections(self):
        self.pushButton_exit.clicked.connect(self.close)