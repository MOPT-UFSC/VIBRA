from PySide6.QtWidgets import QDialog, QComboBox, QLabel, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from vibra import  app
from vibra.interface.ui_generated.analysis.general.harmonic_analysis_method_ui import HarmonicAnalysisMethod_UI


class StructuralHarmonicAnalysisMethodSelecorInput(HarmonicAnalysisMethod_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        app().main_window.close_dialogs()
        app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self._create_connections()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")
        self.label_method.setText("Harmonic Analysis - Structural")

    def _initialize(self):
        self.index = -1
    
    def _create_connections(self):
        self.pushButton_cancel.clicked.connect(self.close_window)
        self.pushButton_proceed.clicked.connect(self.analysis_setup_callback)

    def analysis_setup_callback(self):
        self.go_to_analysis_setup()

    def go_to_analysis_setup(self):
        self.index = self.comboBox_method.currentIndex()
        self.close()

    def close_window(self):
        self.index = -1
        self.close()        

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.go_to_analysis_setup()
        elif event.key() == Qt.Key_Escape:
            self.close_window()