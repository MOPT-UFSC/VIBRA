from pathlib import Path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from vibra import app, UI_DIR
from molde import load_ui


class StructuralHarmonicAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "analysis/structural/structural_harmonic_analysis_input.ui"
        load_ui(ui_path, self, ui_path.parent)

        self.setWindowIcon(app().main_window.vibra_icon)

        self.index = -1
        self.comboBox = self.findChild(QComboBox, "comboBox")
        self.pushButton_2 = self.findChild(QPushButton, "pushButton_2")
        self.pushButton_2.clicked.connect(self.button_clicked)

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.index = -1
            self.close()

    def check(self):
        self.index = self.comboBox.currentIndex()
        self.close()

    def button_clicked(self):
        self.check()
