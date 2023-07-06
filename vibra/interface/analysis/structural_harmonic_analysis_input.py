from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

from pathlib import Path

class StructuralHarmonicAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(Path('data/ui_files/analysis/structural/structural_harmonic_analysis_input.ui'), self)

        icon_path = str(Path('data/icons/logo_vibra.png'))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)

        self.index = -1
        self.comboBox = self.findChild(QComboBox, 'comboBox')
        self.pushButton_2 = self.findChild(QPushButton, 'pushButton_2')
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