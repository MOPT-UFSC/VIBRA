
from PySide6.QtGui import QIntValidator, Qt

from vibra import app
from vibra.engine import AnalysisID, ModalAnalysisSetup
from vibra.interface.common.common_interface import check_mesh_related_issues#, mesher_interface_callback
from vibra.interface.ui_generated.analysis.modal_analysis_input_ui import (
    ModalAnalysisInput_UI,
)
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator


class ModalAnalysisInput(ModalAnalysisInput_UI):
    def __init__(self, analysis_id: AnalysisID):
        super().__init__()
        app().main_window.set_input_widget(self)

        self.analysis_id = AnalysisID(analysis_id)

        self._initialize()
        self._config_window()
        self._configure_validators()
        self._update_modal_analysis_title()
        self._create_connections()
        self._load_analysis_setup()
        check_mesh_related_issues(self.pushButton_run_analysis)

        while self.keep_window_open:
            self.exec()

    def _configure_validators(self):
        self.lineEdit_modes_number.setValidator(QIntValidator(0, 1e5))
        self.lineEdit_sigma_factor.setValidator(StrictDoubleValidator(0, 1e2, 6))

    def _initialize(self):
        self.keep_window_open = True
        self.proceed_solution = False

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _update_modal_analysis_title(self):
        if self.analysis_id == AnalysisID.ACOUSTIC_MODAL:
            self.label_title.setText("Acoustic modal analysis setup")

        elif self.analysis_id == AnalysisID.STRUCTURAL_MODAL:
            self.label_title.setText("Structural modal analysis setup")

    def _create_connections(self):
        self.pushButton_run_analysis.clicked.connect(self.run_analysis)
        self.pushButton_enter_setup.clicked.connect(self.enter_setup_callback)

    def _load_analysis_setup(self):
        analysis_setup = app().project.model.analysis_setup

        if isinstance(analysis_setup, ModalAnalysisSetup) and self.analysis_id.is_modal():
            modes_number = analysis_setup.modes_number
            sigma = analysis_setup.sigma_factor
        else:
            modes_number = 40
            sigma = 0.01

        self.lineEdit_modes_number.setText(str(modes_number))
        self.lineEdit_sigma_factor.setText(str(sigma))

    def enter_setup_callback(self):

        line_edits = [
            self.lineEdit_modes_number,
            self.lineEdit_sigma_factor,
        ]

        for line_edit in line_edits:
            if line_edit.text() == "":
                line_edit.setFocus()
                return True

        analysis_setup = ModalAnalysisSetup(
            analysis_id = self.analysis_id,
            modes_number = int(self.lineEdit_modes_number.text()),
            sigma_factor = float(self.lineEdit_sigma_factor.text()),
        )

        app().project.configure_analysis(analysis_setup)
        app().main_window.analysis_toolbar.enable_pushbutons.emit()

        if app().main_window.action_results_workspace.isChecked():
            app().main_window.action_model_workspace_callback()

        self.close()

    def run_analysis(self):

        # if not app().project.model.is_there_a_valid_mesh():
        #     if mesher_interface_callback(self, close_after_generate=True):
        #         return

        if self.enter_setup_callback():
            return

        self.proceed_solution = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.run_analysis()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)