
from vibra.engine import ModalAnalysisSetup
from PySide6.QtGui import Qt

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface import error_title
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.general.mesher_setup_inputs import MesherSetupInputs
from vibra.interface.ui_generated.analysis.modal_analysis_input_ui import ModalAnalysisInput_UI


class ModalAnalysisInput(ModalAnalysisInput_UI):
    def __init__(self, analysis_id: AnalysisID):
        super().__init__()
        app().main_window.set_input_widget(self)

        self.analysis_id = AnalysisID(analysis_id)

        self._initialize()
        self._config_window()
        self._update_modal_analysis_title()
        self._create_connections()
        self._load_analysis_setup()
        self.check_mesh_related_issues()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.keep_window_open = True
        self.modes_number = None
        self.setup_defined = False
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

        self.lineEdit_number_modes.setText(str(modes_number))
        self.lineEdit_sigma_factor.setText(str(sigma))

    def check_mesh_related_issues(self):

        # disable run_analysis button if there are disconnected nodes or collapsed elements
        mesh = app().project.model.mesh
        disconnected_nodes = bool(mesh.disconnected_nodes_data)
        collapsed_elements = bool(mesh.collapsed_elements_data)

        text = ""
        if collapsed_elements:
            text = "Collapsed elements have been detected during the mesh post-processing. \n"
            text += "The model solution will stay deactivated until the collapsed-related \n"
            text += "issues have been addressed."

        if disconnected_nodes:
            text += "Disconnected nodes have been detected during the mesh post-processing. \n"
            text += "The model solution will stay deactivated until the meshing-related issues \n"
            text += "have been addressed."

        self.pushButton_run_analysis.setToolTip(text)
        self.pushButton_run_analysis.setDisabled(collapsed_elements or disconnected_nodes)

    def check_analysis_inputs(self):

        title = "Invalid input value"

        if self.lineEdit_number_modes.text() == "":
            message = "Invalid a value to the number of modes."
            PrintMessageInput([error_title, title, message])
            return True

        else:

            try:
                self.modes_number = int(self.lineEdit_number_modes.text())
            except Exception:
                message = "Invalid input value for number of modes."
                PrintMessageInput([error_title, title, message])
                return True

            try:
                self.sigma_factor = float(self.lineEdit_sigma_factor.text())
            except Exception:
                message = "Invalid input value for sigma factor."
                PrintMessageInput([error_title, title, message])
                return True

        return False

    def enter_setup_callback(self):

        if self.check_analysis_inputs():
            return True

        self.analysis_setup = ModalAnalysisSetup(
            analysis_id = self.analysis_id,
            modes_number = self.modes_number,
            sigma_factor = self.sigma_factor,
        )

        self.setup_defined = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()
        self.close()

    def run_analysis(self):

        if not app().project.model.generated_mesh:
            self.hide()
            obj = MesherSetupInputs(close_after_generate = True)
            if not obj.complete:
                app().main_window.set_input_widget(self)
                return

            app().main_window.update_plots()

        if self.enter_setup_callback():
            return

        self.proceed_solution = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()
        self.close()

    def button_clicked(self):
        self.check_analysis_inputs()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.run_analysis()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)