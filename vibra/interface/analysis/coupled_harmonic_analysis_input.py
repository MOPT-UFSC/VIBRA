from pathlib import Path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from vibra import app
from vibra.interface.ui_generated.analysis.coupled.coupled_harmonic_analysis_input_ui import CoupledHarmonicAnalysisInput_UI


class CoupledHarmonicAnalysisInput(CoupledHarmonicAnalysisInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowIcon(app().main_window.vibra_icon)

        self.comboBox.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox.currentIndex()
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
