from PySide6.QtGui import Qt

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.analysis.acoustic_modal_analysis_input import AcousticModalAnalysisInput
from vibra.interface.analysis.structural_modal_analysis_input import StructuralModalAnalysisInput
from vibra.interface.analysis.harmonic_analysis_method_selector_input import StructuralHarmonicAnalysisMethodSelecorInput
from vibra.interface.ui_generated.analysis.general.analysis_type_input_ui import AnalysisTypeInput_UI


class AnalysisTypeInput(AnalysisTypeInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config_window()
        self._initialize()
        self._create_connections()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")
        self.pushButton_harmonic_coupled.setDisabled(True)

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
        self.analysis_setup = {}
        self.analysis_id = AnalysisID.NO_ANALYSIS
        self.analysis_type_label = None
        self.analysis_method_label = None
        self.complete = False
        self.modes = 0
        self.sigma_factor = 1e-4
        self.run_modal = False
        self.keep_window_open = True

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
            analysis_id = AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD
        else:
            analysis_id = AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION

        self.analysis_setup = {"analysis_id": analysis_id}
        self.finalize()

    def harmonic_acoustic(self):
        self.analysis_setup = {"analysis_id": AnalysisID.ACOUSTIC_HARMONIC}
        self.finalize()

    def harmonic_coupled(self):

        self.hide()
        select = StructuralHarmonicAnalysisMethodSelecorInput()
        if select.index == -1:
            return

        if select.index == 0:
            analysis_id = AnalysisID.COUPLED_HARMONIC_DIRECT_METHOD
        else:
            analysis_id = AnalysisID.COUPLED_HARMONIC_MODE_SUPERPOSITION

        self.analysis_setup = {"analysis_id": analysis_id}
        self.finalize()

    def modal_structural(self):

        self.close()
        modal = StructuralModalAnalysisInput()
        if not modal.setup_defined:
            return

        self.analysis_setup = modal.analysis_setup.copy()
        self.run_modal = modal.proceed_solution
        self.finalize()

    def modal_acoustic(self):

        self.close()
        modal = AcousticModalAnalysisInput()
        if not modal.setup_defined:
            return

        self.analysis_setup = modal.analysis_setup.copy()
        self.run_modal = modal.proceed_solution
        self.finalize()

    def finalize(self):

        self.complete = True
        if len(app().project.analysis_setup):
            for key, value in app().project.analysis_setup.items():
                if key in ["f_min", "f_max", "f_step", "frequencies", "global_damping"]:
                    self.analysis_setup[key] = value

        app().project.set_analysis_setup(self.analysis_setup)
        app().project.create_solver()

        if self.analysis_setup["analysis_id"] in [
            AnalysisID.STRUCTURAL_MODAL,
            AnalysisID.ACOUSTIC_MODAL,
        ]:
            app().file.write_analysis_setup_in_file(self.analysis_setup)

        self.close()

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)