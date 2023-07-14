from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

from pathlib import Path

from vibra.interface.analysis.structural_harmonic_analysis_input import StructuralHarmonicAnalysisInput
from vibra.interface.analysis.acoustic_harmonic_analysis_input import AcousticHarmonicAnalysisInput
from vibra.interface.analysis.coupled_harmonic_analysis_input import CoupledHarmonicAnalysisInput
from vibra.interface.analysis.structural_modal_analysis_input import StructuralModalAnalysisInput
from vibra.interface.analysis.acoustic_modal_analysis_input import AcousticModalAnalysisInput

from vibra.utils.interface_functions import get_main_window

class AnalysisTypeInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/ui_files/analysis/analysis_type_input.ui'), self)
        self.main_window = get_main_window()

        icon_path = str(Path('data/icons/logo_vibra.png'))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.exec()


    def _reset_variables(self):
        #
        # Analysis ID 0 ==> Structural Harmonic Analysis - Direct Method
        # Analysis ID 1 ==> Structural Harmonic Analysis - Mode Superposition Method
        # Analysis ID 2 ==> Structural Modal Analysis 
        # Analysis ID 3 ==> Acoustic Harmonic Analysis - Direct Method
        # Analysis ID 4 ==> Acoustic Modal Analysis
        # Analysis ID 5 ==> Coupled Harmonic Analysis - Direct Method
        # Analysis ID 6 ==> Coupled Harmonic Analysis - Mode Superposition Method
        #
        self.analysis_data = {}
        self.analysis_id = None
        self.analysis_type_label = None
        self.method_id = None
        self.analysis_method_label = None
        self.complete = False
        self.modes = 0
        self.sigma_factor = 1e-4


    def _define_qt_variables(self):
        self.pushButton_harmonic_structural = self.findChild(QPushButton, 'pushButton_harmonic_structural')
        self.pushButton_harmonic_acoustic = self.findChild(QPushButton, 'pushButton_harmonic_acoustic')
        self.pushButton_harmonic_coupled = self.findChild(QPushButton, 'pushButton_harmonic_coupled')
        self.pushButton_modal_structural = self.findChild(QPushButton, 'pushButton_modal_structural')
        self.pushButton_modal_acoustic = self.findChild(QPushButton, 'pushButton_modal_acoustic')
        self.pushButton_harmonic_structural.setDisabled(True)
        self.pushButton_harmonic_acoustic.setDisabled(True)
        self.pushButton_harmonic_coupled.setDisabled(True)


    def _create_connections(self):
        self.pushButton_harmonic_structural.clicked.connect(self.harmonic_structural)
        self.pushButton_harmonic_acoustic.clicked.connect(self.harmonic_acoustic)
        self.pushButton_harmonic_coupled.clicked.connect(self.harmonic_coupled)
        self.pushButton_modal_structural.clicked.connect(self.modal_structural)
        self.pushButton_modal_acoustic.clicked.connect(self.modal_acoustic)


    def keyPressEvent(self, event):
        # if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
        #     self.check()
        if event.key() == Qt.Key_Escape:
            self.close()


    def harmonic_structural(self):
        select = StructuralHarmonicAnalysisInput()
        self.method_id = select.index
        self.analysis_type_label = "Structural Harmonic Analysis"
        if self.method_id == 0:
            self.analysis_id = 0
            self.analysis_method_label = "Direct Method"
        else:
            self.analysis_id = 1
            self.analysis_method_label = "Mode Superposition Method"
        #
        self.analysis_data = {  "analysis_id"           : self.analysis_id,
                                "analysis_type"         : self.analysis_type_label,
                                "analysis_method_label" : self.analysis_method_label,
                             }
        self.finalize()


    def harmonic_acoustic(self):
        select = AcousticHarmonicAnalysisInput()
        self.method_id = select.index
        self.method_id = 0
        self.analysis_type_label = "Acoustic Harmonic Analysis"
        if self.method_id == 0:
            self.analysis_id = 3
            self.analysis_method_label = "Direct Method"
        else:
            return
        #
        self.analysis_data = {  "analysis_id"           : self.analysis_id,
                                "analysis_type"         : self.analysis_type_label,
                                "analysis_method_label" : self.analysis_method_label,
                             }
        self.finalize()


    def harmonic_coupled(self):
        select = CoupledHarmonicAnalysisInput()
        self.method_id = select.index
        self.analysis_type_label = "Coupled Harmonic Analysis"
        if self.method_id == 0:
            self.analysis_id = 5
            self.analysis_method_label = "Direct Method"
        else:
            self.analysis_id = 6
            self.analysis_method_label = "Mode Superposition Method"
        #
        self.analysis_data = {  "analysis_id"           : self.analysis_id,
                                "analysis_type"         : self.analysis_type_label,
                                "analysis_method_label" : self.analysis_method_label,
                             }
        self.finalize()


    def modal_structural(self):
        modal = StructuralModalAnalysisInput()
        if modal.modes is None:
            return
        self.modes = modal.modes
        self.sigma_factor = modal.sigma_factor
        self.analysis_id = 2
        self.analysis_type_label = "Structural Modal Analysis"
        self.complete = modal.complete
        if modal.complete:
            self.analysis_data = {  "analysis_id"   : self.analysis_id,
                                    "analysis_type" : self.analysis_type_label,
                                    "modes"         : self.modes,
                                    "sigma_factor"  : self.sigma_factor  }
            self.finalize()


    def modal_acoustic(self):
        modal = AcousticModalAnalysisInput()
        if modal.modes is None:
            return
        self.modes = modal.modes
        self.sigma_factor = modal.sigma_factor
        self.analysis_id = 4
        self.analysis_type_label = "Acoustic Modal Analysis"
        self.complete = modal.complete
        if modal.complete:
            self.analysis_data = {  "analysis_id"   : self.analysis_id,
                                    "analysis_type" : self.analysis_type_label,
                                    "modes"         : self.modes,
                                    "sigma_factor"  : self.sigma_factor  }
            self.finalize()


    def finalize(self):
        self.complete = True
        self.main_window.project.set_analysis_data(self.analysis_data)
        self.close()
