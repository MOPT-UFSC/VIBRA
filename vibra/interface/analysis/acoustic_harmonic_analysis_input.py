from pathlib import Path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from vibra import app, UI_DIR
from molde import load_ui


class AcousticHarmonicAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "analysis/acoustic/acoustic_harmonic_analysis_input.ui"
        load_ui(ui_path, self, ui_path.parent)

        self.setWindowIcon(app().main_window.vibra_icon)

        self.index = 0

        self.comboBox = self.findChild(QComboBox, "comboBox")
        self.comboBox.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox.currentIndex()

        self.pushButton_2 = self.findChild(QPushButton, "pushButton_2")
        self.pushButton_2.clicked.connect(self.button_clicked)

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def selectionChange(self, index):
        self.index = self.comboBox.currentIndex()

    def check(self):
        self.close()

    def button_clicked(self):
        self.check()
