from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtCore import *
from PySide6.QtGui import *

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.analysis.acoustic_modal_analysis_input import AcousticModalAnalysisInput
from vibra.interface.analysis.structural_modal_analysis_input import StructuralModalAnalysisInput
from vibra.interface.analysis.harmonic_analysis_method_selector_input import StructuralHarmonicAnalysisMethodSelecorInput
from molde import load_ui


class AnalysisTypeInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "analysis/general/analysis_type_input.ui"
        load_ui(ui_path, self, UI_DIR)

        self.main_window = app().main_window

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self)

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
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
        self.analysis_method_label = None
        self.complete = False
        self.modes = 0
        self.sigma_factor = 1e-4
        self.run_modal = False

        self.keep_window_open = True

    def _define_qt_variables(self):

        # QPushButton
        self.pushButton_harmonic_structural : QPushButton
        self.pushButton_harmonic_acoustic : QPushButton
        self.pushButton_harmonic_coupled : QPushButton
        self.pushButton_modal_structural : QPushButton
        self.pushButton_modal_acoustic : QPushButton
        # temporary
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

        self.hide()
        select = StructuralHarmonicAnalysisMethodSelecorInput()
        if select.index == -1:
            return

        if select.index == 0:
            analysis_id = 0
        else:
            analysis_id = 1

        self.analysis_data = {"analysis_id": analysis_id}
        self.finalize()

    def harmonic_acoustic(self):

        self.analysis_data = {"analysis_id": 3}
        self.finalize()

    def harmonic_coupled(self):

        self.hide()
        select = StructuralHarmonicAnalysisMethodSelecorInput()
        if select.index == -1:
            return

        if select.index == 0:
            analysis_id = 5
        else:
            analysis_id = 6

        self.analysis_data = {"analysis_id": analysis_id}
        self.finalize()

    def modal_structural(self):

        self.close()
        modal = StructuralModalAnalysisInput()
        if not modal.setup_defined:
            return

        self.analysis_data = modal.analysis_setup.copy()
        self.run_modal = modal.proceed_solution
        self.finalize()

    def modal_acoustic(self):

        self.close()
        modal = AcousticModalAnalysisInput()
        if not modal.setup_defined:
            return

        self.analysis_data = modal.analysis_setup.copy()
        self.run_modal = modal.proceed_solution
        self.finalize()

    def finalize(self):

        self.complete = True
        if len(app().project.analysis_data):
            for key, value in app().project.analysis_data.items():
                if key in ["f_min", "f_max", "f_step", "frequencies", "global_damping"]:
                    self.analysis_data[key] = value

        app().project.set_analysis_data(self.analysis_data)
        app().project.create_solver()

        if self.analysis_data["analysis_id"] in [2, 4]:
            app().file.write_analysis_setup_in_file(self.analysis_data)

        self.close()

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)