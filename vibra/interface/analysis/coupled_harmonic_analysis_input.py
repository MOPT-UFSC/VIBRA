from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vibra import UI_DIR

class CoupledHarmonicAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "analysis/coupled/coupled_harmonic_analysis_input.ui"
        uic.loadUi(ui_path, self)

        icon_path = str(Path("data/icons/logo_vibra.png"))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)

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
            self.index = -1
            self.close()

    def selectionChange(self, index):
        self.index = self.comboBox.currentIndex()

    def check(self):
        self.close()

    def button_clicked(self):
        self.check()
