from PySide6.QtWidgets import QDialog, QLineEdit
from PySide6.QtGui import Qt

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.ui_generated.analysis.structural.harmonic_analysis_setup_input_ui import HarmonicAnalysisSetupInput_UI

error_title = "Error"


class HarmonicAnalysisSetupInput(HarmonicAnalysisSetupInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.project = app().project
        self.model = app().project.model
        self.analysis_setup = app().project.analysis_setup

        self.analysis_id = kwargs.get("analysis_id")
        if self.analysis_id is None:
            self.analysis_id = self.analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

        """
        |--------------------------------------------------------------------|
        |                    Analysis ID codification                        |
        |--------------------------------------------------------------------|
        |    0 - Structural - Harmonic analysis through direct method        |
        |    1 - Structural - Harmonic analysis through mode superposition   |
        |    2 - Structural - Modal analysis                                 |
        |    3 - Acoustic - Harmonic analysis through direct method          |
        |    4 - Acoustic - Modal analysis                                   |
        |    5 - Coupled - Harmonic analysis through direct method           |
        |    6 - Coupled - Harmonic analysis through mode superposition      |
        |--------------------------------------------------------------------|
        """
        app().main_window.close_dialogs()
        app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self._create_connections()

        self.load_analysis_setup()
        self.update_harmonic_analysis_title()
        self.check_mesh_related_issues()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.frequencies = list()
        self.setup_defined = False
        self.solve_analysis = False
        self.keep_window_open = True

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Analysis setup")

    def _create_connections(self):
        #
        self.comboBox_method.currentIndexChanged.connect(self.analysis_method_callback)
        #
        self.pushButton_enter_setup.clicked.connect(self.enter_setup_callback)
        self.pushButton_run_analysis.clicked.connect(self.run_analysis)

    def analysis_method_callback(self):

        direct_method = self.comboBox_method.currentText() == "Direct"
        self.label_modes_to_expand.setVisible(not direct_method)
        self.lineEdit_modes_to_expand.setVisible(not direct_method)

        if direct_method:
            self.lineEdit_modes_to_expand.setText("")
            return

        analysis_setup = app().file.read_analysis_setup_from_file()
        if not isinstance(analysis_setup, dict):
            return

        if self.analysis_id in [AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.COUPLED_HARMONIC]:
            if analysis_setup.get("analysis_method") == "mode_superposition":
                modes_to_expand = analysis_setup.get("modes_number")
                self.lineEdit_modes_to_expand.setText(f"{modes_to_expand}")
        else:
            self.lineEdit_modes_to_expand.setText(f"")

    def _update_fmin(self):
        df = self.lineEdit_fstep.text()
        self.lineEdit_fmin.setText(df)

    def load_analysis_setup(self):

        f_min = self.analysis_setup.get("f_min", 5)
        f_max = self.analysis_setup.get("f_max", 600)
        f_step = self.analysis_setup.get("f_step", 5)
        global_damping = self.analysis_setup.get("global_damping", (0, 0, 0))

        self.load_analysis_type()
        self.load_damping_inputs(self.analysis_id, global_damping)
        self.load_frequency_setup_inputs(f_min, f_max, f_step)

    def load_analysis_type(self):

        self.comboBox_method.blockSignals(True)

        if self.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.comboBox_method.removeItem(1)
            self.tabWidget_main.setTabVisible(1, False)

        elif self.analysis_id in [AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.COUPLED_HARMONIC]:
            mode_sup = self.analysis_setup.get("analysis_method") == "mode_superposition"
            self.comboBox_method.setCurrentIndex(int(mode_sup))

        self.comboBox_method.blockSignals(False)
        self.analysis_method_callback()

    def load_damping_inputs(self, analysis_id: int, global_damping: tuple | list):
        if sum(global_damping) and analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC, 
            AnalysisID.COUPLED_HARMONIC,          
        ]:

            if global_damping[0]:
                self.lineEdit_mass_multiplier.setText(str(global_damping[0]))

            if global_damping[1]:
                self.lineEdit_stiffness_multiplier.setText(str(global_damping[1]))

            if global_damping[2]:
                self.lineEdit_constant_structural_coefficient.setText(str(global_damping[2]))

    def load_frequency_setup_inputs(self, f_min: float, f_max: float, f_step: float):
        self.lineEdit_fmin.setText(f"{f_min : .12f}")
        self.lineEdit_fmax.setText(f"{f_max : .12f}")
        self.lineEdit_fstep.setText(f"{f_step : .12f}")

        key = app().project.model.properties.check_if_there_are_tables_at_the_model()

        self.lineEdit_fmin.setDisabled(key)
        self.lineEdit_fmax.setDisabled(key)
        self.lineEdit_fstep.setDisabled(key)

    def update_harmonic_analysis_title(self):
        if self.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.label_title.setText("Acoustic harmonic analysis setup")
        elif self.analysis_id == AnalysisID.STRUCTURAL_HARMONIC:
            self.label_title.setText("Structural harmonic analysis setup")
        elif self.analysis_id == AnalysisID.COUPLED_HARMONIC:
            self.label_title.setText("Coupled harmonic analysis setup")

    def check_mesh_related_issues(self):

        # disable run_analysis button if there are disconnected nodes or collapsed elements
        mesh = app().project.model.mesh
        disconnected_nodes = bool(mesh.disconnected_nodes)
        collapsed_elements = bool(mesh.collapsed_3d_elements or mesh.collapsed_2d_elements or mesh.collapsed_1d_elements)

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

    def enter_setup_callback(self):
        # analysis_setup = app().file.read_analysis_setup_from_file()
        # if analysis_setup is None:
        #     analysis_setup = dict()

        analysis_id = app().main_window.analysis_toolbar.get_current_analysis_id()
        analysis_method = "direct" if self.comboBox_method.currentIndex() == 0 else "mode_superposition"

        analysis_setup = dict()
        analysis_setup["analysis_id"] = analysis_id
        analysis_setup["analysis_method"] = analysis_method

        if analysis_method == "mode_superposition":
            modes_number = self.check_inputs(
                self.lineEdit_modes_to_expand, 
                "modes to expand",
                int_value = True,
                )

            if modes_number is None:
                self.lineEdit_modes_to_expand.setFocus()
                return True

            analysis_setup["modes_number"] = modes_number

        f_min = f_max = f_step = 0.

        if analysis_id in [AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.ACOUSTIC_HARMONIC, AnalysisID.COUPLED_HARMONIC]:

            zero_allowed = app().main_window.analysis_toolbar.combo_box_physical_domain.currentText() == "Structural"

            f_min = self.check_inputs(
                self.lineEdit_fmin, 
                "minimum frequency (Freq. min)", 
                zero_included = zero_allowed, 
                )

            if f_min is None:
                self.lineEdit_fmin.setFocus()
                return True

            f_max = self.check_inputs(
                self.lineEdit_fmax, 
                "maximum frequency (Freq. max)"
                )

            if f_max is None:
                self.lineEdit_fmax.setFocus()
                return True

            f_step = self.check_inputs(
                self.lineEdit_fstep, 
                "frequency resolution (Freq. step)"
                )

            if f_step is None:
                self.lineEdit_fstep.setFocus()
                return True

            if f_max < f_min + f_step:
                self.hide()
                title = "Invalid frequency setup"
                message = "The maximum frequency (fmax) must be greater than the sum of "
                message += "minimum frequency (fmin) and frequency resolution (df)."
                PrintMessageInput([error_title, title, message])
                return True

            analysis_setup["f_min"] = f_min
            analysis_setup["f_max"] = f_max
            analysis_setup["f_step"] = f_step

        alpha = beta = eta = 0.0

        if analysis_id in [AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.COUPLED_HARMONIC]:

            alpha = self.check_inputs(
                self.lineEdit_mass_multiplier, 
                "mass matrix multiplier (α)", 
                zero_included = True
                )

            if alpha is None:
                self.lineEdit_mass_multiplier.setFocus()
                return True

            beta = self.check_inputs(
                self.lineEdit_stiffness_multiplier, 
                "stiffness matrix multiplier (β)", 
                zero_included = True
                )

            if beta is None:
                self.lineEdit_stiffness_multiplier.setFocus()
                return True

            eta = self.check_inputs(
                self.lineEdit_constant_structural_coefficient, 
                "proportional hysteretic damping (η)", 
                zero_included = True
                )

            if eta is None:
                self.lineEdit_constant_structural_coefficient.setFocus()
                return True

            analysis_setup["global_damping"] = [alpha, beta, eta]

        if app().project.model.properties.check_if_there_are_tables_at_the_model():
            self.frequencies = self.model.frequencies
        else:
            self.model.set_analysis_setup(analysis_setup)

        app().file.write_analysis_setup_in_file(analysis_setup)

        self.project.set_analysis_setup(analysis_setup)
        self.project.create_solver()

        self.setup_defined = True
        app().main_window.analysis_toolbar.check_analysis_setup_callback()
        self.close()

        return False

    def check_inputs(self, lineEdit: QLineEdit, label: str, zero_included: bool = False, int_value: bool = False):
        message = ""
        if lineEdit.text() != "":
            try:
                if int_value:
                    value = int(lineEdit.text())
                else:
                    value = float(lineEdit.text())

                if zero_included:
                    if value < 0:
                        message = f"Enter a positive value in the {label} input field. "
                else:
                    if value <= 0:
                        message = f"Enter a positive value in the {label} input field. "
                        message += "The zero value is not allowed."

            except Exception as _err:
                message = f"The typed value at the {label} input field is invalid.\n\n"
                message += str(_err)

        else:
            if zero_included:
                return float(0)
            else:
                message = f"Enter a positive value in the '{label}' input field."

        if message != "":
            self.hide()
            title = "Invalid input to the analysis setup"
            PrintMessageInput([error_title, title, message])
            return None

        return value

    def run_analysis(self):
        if self.enter_setup_callback():
            return
        self.solve_analysis = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.run_analysis()
        elif event.key() == Qt.Key_Escape:
            self.close()