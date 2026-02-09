from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import Qt

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.ui_generated.analysis.harmonic_analysis_setup_input_ui import HarmonicAnalysisSetupInput_UI
from vibra.interface.analysis.user_defined_solution_steps_by_manual_input import UserDefinedSolutionStepsByManualInput
from vibra.interface.analysis.user_defined_solution_steps_from_tabular_data_input import UserDefinedSolutionStepsFromTabularDataInput
from vibra.interface.analysis.solutions_step_display_input import SolutionStepsDisplayInput

import numpy as np

error_title = "Error"


class HarmonicAnalysisSetupInput(HarmonicAnalysisSetupInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.model = app().project.model
        self.analysis_setup = app().project.analysis_setup

        self.analysis_id = kwargs.get("analysis_id")
        if self.analysis_id is None:
            self.analysis_id = self.analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

        self.ud_interface = None

        app().main_window.close_dialogs()
        app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self._create_connections()

        self.load_analysis_setup()
        self.check_mesh_related_issues()
        self.update_display_table_visibility()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.setup_defined = False
        self.solve_analysis = False
        self.keep_window_open = True
        self.user_defined_solution_steps = list()
        self.table_exists = self.model.properties.check_if_there_are_tables_at_the_model()
        self.tabular_frequency_setup = self.model.get_tabular_frequency_setup()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Analysis setup")

    def _create_connections(self):
        #
        self.comboBox_frequency_spacing.currentIndexChanged.connect(self.frequency_spacing_callback)
        self.comboBox_method.currentIndexChanged.connect(self.analysis_method_callback)
        #
        self.pushButton_enter_setup.clicked.connect(self.enter_setup_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_reset_frequency_settings.clicked.connect(self.reset_frequency_setup_based_on_tabular_data)
        self.pushButton_run_analysis.clicked.connect(self.run_analysis)
        self.pushButton_solution_steps_configurator.clicked.connect(self.solution_steps_setup_callback)
        self.pushButton_show_solution_steps_table.clicked.connect(self.display_solution_steps_callback)
        #
        self.frequency_spacing_callback()

    def update_display_table_visibility(self):
        frequencies_defined = isinstance(self.model.frequencies, list | np.ndarray)
        self.pushButton_show_solution_steps_table.setEnabled(frequencies_defined)

    def solution_steps_setup_callback(self):
        self.hide()

        if self.table_exists:
            self.ud_interface = UserDefinedSolutionStepsFromTabularDataInput()

        else:
            self.ud_interface = UserDefinedSolutionStepsByManualInput()

        if self.ud_interface.setup_defined:
            self.user_defined_solution_steps = self.ud_interface.user_defined_solution_steps

        self.update_display_table_visibility()

    def frequency_spacing_callback(self):
        user_defined = self.comboBox_frequency_spacing.currentText() == "User-defined"
        self.frame_equally_distributed.setVisible(not user_defined)
        self.frame_solution_steps_setup.setVisible(user_defined)

    def update_solution_steps_controls_visibility(self):

        self.label_fstep_unit_combo_box.setVisible(self.table_exists)
        self.label_fstep_combo_box.setVisible(self.table_exists)
        self.comboBox_fstep.setVisible(self.table_exists)

        self.label_fstep_unit_line_edit.setVisible(not self.table_exists)
        self.label_fstep_line_edit.setVisible(not self.table_exists)
        self.lineEdit_fstep.setVisible(not self.table_exists)

        if self.tabular_frequency_setup is None:
            return

        _, f_max, f_step, _ = self.tabular_frequency_setup

        for i in range(5):
            _f_step = f_step*(i + 1)
            if _f_step >= f_max:
                continue

            self.comboBox_fstep.addItem(f"{round(_f_step, 14)}")

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

    def display_solution_steps_callback(self):
        self.hide()
        SolutionStepsDisplayInput()

    def reset_frequency_setup_based_on_tabular_data(self):
        if not self.model.properties.check_if_there_are_tables_at_the_model():
            return
        
        if self.tabular_frequency_setup is None:
            return

        f_min, f_max, f_step, _ = self.tabular_frequency_setup

        if (f_min, f_max, f_step).count(None):
            return
    
        self.load_frequency_setup_inputs(f_min, f_max, f_step)

    def update_reset_settings_button_visibility(self):
        self.pushButton_reset_frequency_settings.setVisible(self.table_exists)
        if not self.table_exists:
            return

        misaligned_fsetup = self.model.has_spectral_content_been_modified()
        self.pushButton_reset_frequency_settings.setEnabled(misaligned_fsetup)

    def load_analysis_setup(self):

        f_min = self.analysis_setup.get("f_min", 5)
        f_max = self.analysis_setup.get("f_max", 600)
        f_step = self.analysis_setup.get("f_step", 5)
        global_damping = self.analysis_setup.get("global_damping", (0., 0., 0.))

        self.load_analysis_type()
        self.load_damping_inputs(self.analysis_id, global_damping)
        self.update_solution_steps_controls_visibility()
        self.load_frequency_setup_inputs(f_min, f_max, f_step)

        if self.analysis_setup.get("frequency_spacing") == "user-defined":
            self.comboBox_frequency_spacing.setCurrentText("User-defined")

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
        self.update_harmonic_analysis_title()

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

        self.lineEdit_fmin.setText("{}".format(round(f_min, 14)))
        self.lineEdit_fmax.setText("{}".format(round(f_max, 14)))
        self.lineEdit_fstep.setText("{}".format(round(f_step, 14)))
        self.comboBox_fstep.setCurrentText(f"{round(f_step, 14)}")

        self.lineEdit_fstep.setDisabled(self.table_exists)
        self.tabWidget_main.setTabVisible(2, self.table_exists)

        self.update_reset_settings_button_visibility()

    def check_tabular_frequencies_compatibility(self, f_min: float, f_max: float):
        if not self.table_exists:
            return False
        
        if self.tabular_frequency_setup is None:
            return False
        
        f_min_tab, f_max_tab, *_ = self.tabular_frequency_setup
    
        if f_min < f_min_tab:
            if not np.isclose(f_min, f_min_tab, 1e-8):
                self.hide()
                title = "Invalid minimum frequency"
                message = "The value entered for the minimum frequency is out of the allowable range."
                PrintMessageInput([error_title, title, message])
                self.lineEdit_fmin.setFocus()
                self.lineEdit_fmin.setStyleSheet("border-color: rgb(255,0,0); border-width: 2px")
                return True
            
        if f_max > f_max_tab:
            if not np.isclose(f_max, f_max_tab, 1e-8):
                self.hide()
                title = "Invalid maximum frequency"
                message = "The value entered for the maximum frequency is out of the allowable range."
                PrintMessageInput([error_title, title, message])
                self.lineEdit_fmax.setFocus()
                self.lineEdit_fmax.setStyleSheet("border-color: rgb(255,0,0); border-width: 2px")
                return True
            
        self.lineEdit_fmin.setStyleSheet("")
        self.lineEdit_fmax.setStyleSheet("")

        return False

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

    def enter_setup_callback(self):

        analysis_id = app().main_window.analysis_toolbar.get_current_analysis_id()
        analysis_method = "direct" if self.comboBox_method.currentIndex() == 0 else "mode_superposition"
        frequency_spacing = self.comboBox_frequency_spacing.currentText().lower()

        if frequency_spacing == "user-defined":
            if not self.user_defined_solution_steps:
                self.hide()
                title = "No solution steps found"
                message = "Enter the solution steps before confirming the analysis "
                message += "setup or trying to solve the harmonic analysis."
                PrintMessageInput([error_title, title, message])
                self.solution_steps_setup_callback()
                return

        analysis_setup = {
            "analysis_id" : analysis_id,
            "analysis_method" : analysis_method,
            "frequency_spacing" : frequency_spacing,
        }

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

        if analysis_id in [AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.ACOUSTIC_HARMONIC, AnalysisID.COUPLED_HARMONIC]:
            if frequency_spacing == "user-defined":
                analysis_setup.update(
                    {
                    "frequencies" : np.array(self.user_defined_solution_steps, dtype=float),
                    "user_defined_solution_steps" : self.user_defined_solution_steps,
                    }
                    )

            user_defined_manually = not self.table_exists and self.user_defined_solution_steps
            if not user_defined_manually:
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

                if self.lineEdit_fstep.isVisible():
                    f_step = self.check_inputs(
                        self.lineEdit_fstep, 
                        "frequency resolution (Freq. step)"
                        )

                    if f_step is None:
                        self.lineEdit_fstep.setFocus()
                        return True

                else:
                    f_step = float(self.comboBox_fstep.currentText())

                condition_1 = f_max < f_min + f_step

                if self.tabular_frequency_setup is None:
                    condition_2 = True
                else:
                    (_, f_max_tab, _, _) = self.tabular_frequency_setup
                    condition_2 = not f_max_tab >= f_max

                if condition_1:
                    if condition_2:
                        self.hide()
                        title = "Invalid frequency setup"
                        message = "The maximum frequency (fmax) must be greater than the sum of "
                        message += "minimum frequency (fmin) and frequency resolution (df)."
                        PrintMessageInput([error_title, title, message])
                        return True
                
                if self.check_tabular_frequencies_compatibility(f_min, f_max):
                    return True
            
                analysis_setup.update(
                    {
                    "f_min" : f_min,
                    "f_max" : f_max,
                    "f_step" : f_step,
                    }
                )

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

        app().file.write_analysis_setup_in_file(analysis_setup)
        app().project.set_analysis_setup(analysis_setup)
        app().project.create_solver()

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
                message = f"The value entered in the {label} input field is invalid.\n\n"
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

    def check_analysis_setup_update(self):

        if self.ud_interface is None:
            return
        
        if not self.ud_interface.setup_defined:
            return

        if self.setup_defined:
            return

        self.hide()

        title = "Analysis setup not updated"
        message = "A set of solution steps has been configured, however, "
        message += "the analysis setup has not been updated. Would you "
        message += "like to update the analysis setup before exit?"

        buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            self.enter_setup_callback()
            return

    def closeEvent(self, a0):

        self.check_analysis_setup_update()
        self.keep_window_open = False

        return super().closeEvent(a0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.run_analysis()
        elif event.key() == Qt.Key_Escape:
            self.close()