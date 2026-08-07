
from enum import IntEnum
from numbers import Number

import numpy as np
from PySide6.QtGui import QIntValidator, Qt

from vibra import app
from vibra.engine.analysis_info import (
    AnalysisID,
    FrequencySpacing,
    HarmonicAnalysisSetup,
)
from vibra.engine.analysis_info.analysis_enums import AnalysisMethod
from vibra.interface import error_title
from vibra.interface.analysis.solutions_step_display_input import SolutionStepsDisplayInput
from vibra.interface.analysis.user_defined_solution_steps_by_manual_input import UserDefinedSolutionStepsByManualInput
from vibra.interface.analysis.user_defined_solution_steps_from_tabular_data_input import UserDefinedSolutionStepsFromTabularDataInput
from vibra.interface.common.common_interface import check_mesh_related_issues  #, mesher_interface_callback
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.utils import clear_style_sheet
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.ui_generated.analysis.harmonic_analysis_setup_input_ui import HarmonicAnalysisSetupInput_UI


class TabType(IntEnum):
    FREQUENCY_SETUP = 0
    DAMPING_SETUP = 1


class AnalysisMethodIndex(IntEnum):
    DIRECT = 0
    MODE_SUPERPOSITION = 1


class HarmonicAnalysisSetupInput(HarmonicAnalysisSetupInput_UI):
    def __init__(self, analysis_id: AnalysisID):
        super().__init__()
        app().main_window.set_input_widget(self)

        self.analysis_id = AnalysisID(analysis_id)

        self._initialize()
        self._config_window()
        self._config_widgets()
        self._configure_validators()
        self._create_connections()

        self.load_table_data()
        self.set_default_values()
        self.frequency_spacing_callback()
        self.update_harmonic_analysis_title()

        check_mesh_related_issues(self.pushButton_run_analysis)
        self.update_display_table_visibility()

        while self.keep_window_open:
            self.exec()
    
    @property
    def model(self):
        return app().project.model

    @property
    def analysis_setup(self):
        return app().project.model.analysis_setup

    def _initialize(self):
        self.ud_interface = None
        self.setup_defined = False
        self.solve_analysis = False
        self.keep_window_open = True
        self.keep_window_open_after_enter_setup = False
        self.user_defined_solution_steps = list()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Analysis setup")

    def _config_widgets(self):

        # get the QLineEdit font
        font = self.lineEdit_fmax.font()

        # use same QLineEdit's font in the frequency step QComboBox
        self.comboBox_fstep.setFont(font)
        self.comboBox_fstep.setEditable(True)
        self.comboBox_fstep.lineEdit().setFont(font)
        self.comboBox_fstep.lineEdit().setReadOnly(True)
        self.comboBox_fstep.lineEdit().setAlignment(Qt.AlignCenter)

    def _configure_validators(self):

        # modes to expand validator
        self.lineEdit_modes_to_expand.setValidator(QIntValidator(0, 1e5))

        # frequency inputs validators
        fmin_lowest_value = 0 if AnalysisID.is_structural(self.analysis_id) else 1e-6
        self.lineEdit_fmin.setValidator(StrictDoubleValidator(fmin_lowest_value, 1e8, 8))
        self.lineEdit_fmax.setValidator(StrictDoubleValidator(1e-3, 1e8, 8))
        self.lineEdit_fstep.setValidator(StrictDoubleValidator(1e-8, 1e8, 8))

        # damping inputs validators
        self.lineEdit_mass_multiplier.setValidator(StrictDoubleValidator(0, 1e8, 8))
        self.lineEdit_stiffness_multiplier.setValidator(StrictDoubleValidator(0, 1e8, 8))
        self.lineEdit_constant_structural_coefficient.setValidator(StrictDoubleValidator(0, 1, 8))

    def _create_connections(self):
        #
        self.comboBox_frequency_spacing.currentIndexChanged.connect(self.frequency_spacing_callback)
        self.comboBox_method.currentIndexChanged.connect(self.analysis_method_callback)
        #
        self.pushButton_enter_setup.clicked.connect(self.enter_setup_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_reset_frequency_settings.clicked.connect(self.reset_frequency_setup_based_on_tabular_data)
        self.pushButton_run_analysis.clicked.connect(self.run_analysis)
        self.pushButton_show_solution_steps_table.clicked.connect(self.display_solution_steps_callback)
        self.pushButton_solution_steps_configurator.clicked.connect(self.solution_steps_setup_callback)
        
    def update_display_table_visibility(self):
        frequencies_defined = isinstance(self.model.frequencies, list | np.ndarray)
        self.pushButton_show_solution_steps_table.setEnabled(frequencies_defined)

    def solution_steps_setup_callback(self):
        self.hide()
        if self.table_exists:
            self.ud_interface = UserDefinedSolutionStepsFromTabularDataInput()
        else:
            self.ud_interface = UserDefinedSolutionStepsByManualInput(
                current_solution_steps=self.user_defined_solution_steps,
            )

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
        direct_method = self.comboBox_method.currentIndex() == AnalysisMethodIndex.DIRECT
        self.label_modes_to_expand.setVisible(not direct_method)
        self.lineEdit_modes_to_expand.setVisible(not direct_method)

        if direct_method:
            self.lineEdit_modes_to_expand.clear()
            return

        if AnalysisID(self.analysis_id).is_harmonic_structural():
            if self.analysis_setup.analysis_method == AnalysisMethod.MODE_SUPERPOSITION:
                modes_to_expand = self.analysis_setup.modes_number
                self.lineEdit_modes_to_expand.setText(f"{modes_to_expand}")
        else:
            self.lineEdit_modes_to_expand.clear()

    def display_solution_steps_callback(self):
        
        self.keep_window_open_after_enter_setup = True
        # check analysis setup update before loading the solution steps
        self.check_analysis_setup_update()
        self.keep_window_open_after_enter_setup = False

        self.hide()
        SolutionStepsDisplayInput()

    def check_analysis_setup_update(self):

        if self.ud_interface is None:
            return
        
        if not self.ud_interface.setup_defined:
            if len(self.user_defined_solution_steps) == 0:
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

    def reset_frequency_setup_based_on_tabular_data(self):
        if not self.model.properties.check_if_there_are_tables_at_the_model():
            return
        
        if self.tabular_frequency_setup is None:
            return

        f_min, f_max, f_step, _ = self.tabular_frequency_setup

        if (f_min, f_max, f_step).count(None):
            return
    
        self.load_frequency_setup_inputs(f_min, f_max, f_step)
        self.pushButton_show_solution_steps_table.setDisabled(True)

    def update_reset_settings_button_visibility(self):
        self.pushButton_reset_frequency_settings.setVisible(self.table_exists)
        if not self.table_exists:
            return
        
        misaligned_fsetup = self.model.has_spectral_content_been_modified()
        self.pushButton_reset_frequency_settings.setEnabled(misaligned_fsetup)

    def load_table_data(self):
        self.tabular_frequency_setup = self.model.get_tabular_frequency_setup()
        self.table_exists = self.model.properties.check_if_there_are_tables_at_the_model()

    def set_default_values(self):

        self.load_analysis_type()
        self.load_damping_inputs()
        self.reset_frequency_inputs()

        if not isinstance(self.analysis_setup, HarmonicAnalysisSetup):
            return
    
        frequency_spacing = self.analysis_setup.frequency_spacing

        if frequency_spacing == FrequencySpacing.USER_DEFINED:
            self.comboBox_frequency_spacing.setCurrentText("User-defined")

        elif frequency_spacing == FrequencySpacing.EQUALLY_DISTRIBUTED:
            self.comboBox_frequency_spacing.setCurrentText("Equally distributed")

    def reset_frequency_inputs(self):
        self.update_solution_steps_controls_visibility()

        f_min = 5
        f_max = 600
        f_step = 5

        if isinstance(self.analysis_setup, HarmonicAnalysisSetup):
            if self.analysis_setup.frequency_spacing == FrequencySpacing.EQUALLY_DISTRIBUTED:
                f_min = self.analysis_setup.f_min
                f_max = self.analysis_setup.f_max
                f_step = self.analysis_setup.f_step

        else:
            if self.table_exists:
                self.reset_frequency_setup_based_on_tabular_data()
                return

        self.load_frequency_setup_inputs(f_min, f_max, f_step)

    def load_analysis_type(self):
        self.comboBox_method.blockSignals(True)

        if self.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.comboBox_method.removeItem(AnalysisMethodIndex.MODE_SUPERPOSITION)
            self.tabWidget_main.setTabVisible(TabType.DAMPING_SETUP, False)

        elif AnalysisID(self.analysis_id).is_harmonic_structural():
            if isinstance(self.analysis_setup, HarmonicAnalysisSetup):
                if self.analysis_setup.analysis_method == AnalysisMethod.DIRECT:
                    self.comboBox_method.setCurrentIndex(AnalysisMethodIndex.DIRECT)
                else:
                    self.comboBox_method.setCurrentIndex(AnalysisMethodIndex.MODE_SUPERPOSITION)

        self.comboBox_method.blockSignals(False)
        self.analysis_method_callback()
        self.update_harmonic_analysis_title()

    def load_damping_inputs(self):

        if AnalysisID(self.analysis_id).is_harmonic_structural():

            alpha, beta, eta = self.model.global_damping

            if isinstance(alpha, Number):
                self.lineEdit_mass_multiplier.setText(str(alpha))

            if isinstance(beta, Number):
                self.lineEdit_stiffness_multiplier.setText(str(beta))

            if isinstance(eta, Number):
                self.lineEdit_constant_structural_coefficient.setText(str(eta))

    def load_frequency_setup_inputs(self, f_min: float, f_max: float, f_step: float):
        self.lineEdit_fmin.setText("{}".format(round(f_min, 14)))
        self.lineEdit_fmax.setText("{}".format(round(f_max, 14)))
        self.lineEdit_fstep.setText("{}".format(round(f_step, 14)))
        self.comboBox_fstep.setCurrentText(f"{round(f_step, 14)}")

        self.lineEdit_fstep.setDisabled(self.table_exists)
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

        clear_style_sheet([self.lineEdit_fmin, self.lineEdit_fmax])

        return False

    def update_harmonic_analysis_title(self):
        if self.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.label_title.setText("Acoustic harmonic analysis setup")

        elif self.analysis_id == AnalysisID.STRUCTURAL_HARMONIC:
            self.label_title.setText("Structural harmonic analysis setup")

        elif self.analysis_id == AnalysisID.COUPLED_HARMONIC:
            self.label_title.setText("Coupled harmonic analysis setup")

    def check_frequencies_inputs(self):

        line_edits = [
            self.lineEdit_fmin,
            self.lineEdit_fmax,
            self.lineEdit_fstep,
        ]

        for line_edit in line_edits:
            if line_edit.text() == "":
                line_edit.setFocus()
                return None

        f_min = float(self.lineEdit_fmin.text())
        f_max = float(self.lineEdit_fmax.text())

        if self.lineEdit_fstep.isVisible():
            f_step = float(self.lineEdit_fstep.text())
        else:
            f_step = float(self.comboBox_fstep.currentText())

        condition_A = f_max < f_min + f_step

        if self.tabular_frequency_setup is None:
            condition_B = True
        else:
            (f_min_tab, f_max_tab, _, _) = self.tabular_frequency_setup
            condition_B = not f_max_tab >= f_max

        if condition_A and condition_B:
            self.hide()
            title = "Invalid frequency setup"
            message = "The maximum frequency (fmax) must be greater than the sum of "
            message += "minimum frequency (fmin) and frequency resolution (df)."
            PrintMessageInput([error_title, title, message])
            return None

        if self.check_tabular_frequencies_compatibility(f_min, f_max):
            return None

        _f_min = f_min
        if round(f_min % f_step, 10):
            _f_min = np.floor(f_min / f_step) * f_step
            print(f"The minimum frequency has been changed from {f_min} to {_f_min}")

        _f_max = f_max
        if round(f_max % f_step, 10):
            _f_max = np.ceil(f_max / f_step) * f_step
            print(f"The maximum frequency has been changed from {f_max} to {_f_max}")

        # additional checks to prevent out-of-index access errors
        if isinstance(self.tabular_frequency_setup, tuple):
            if _f_min < f_min_tab:
                _f_min = f_min_tab

            if _f_max > f_max_tab:
                _f_max = f_max_tab

        return {
            "f_min" : _f_min,
            "f_max" : _f_max,
            "f_step" : f_step,
            }
    
    def check_damping_inputs(self):

        line_edits = [
            self.lineEdit_mass_multiplier,
            self.lineEdit_stiffness_multiplier,
            self.lineEdit_constant_structural_coefficient,
        ]

        global_damping = list()
        for line_edit in line_edits:
            if line_edit.text() == "":
                global_damping.append(0.0)
            else:
                global_damping.append(float(line_edit.text()))

        return global_damping

    def enter_setup_callback(self):
        if self.comboBox_method.currentIndex() == AnalysisMethodIndex.DIRECT:
            analysis_method = AnalysisMethod.DIRECT
        else:
            analysis_method = AnalysisMethod.MODE_SUPERPOSITION

        frequency_spacing = self.comboBox_frequency_spacing.currentText().lower()
        analysis_id = app().main_window.analysis_toolbar.get_current_analysis_id()

        if frequency_spacing == FrequencySpacing.USER_DEFINED:
            if len(self.user_defined_solution_steps) == 0:
                if len(self.model.frequencies) == 0:
                    self.hide()
                    title = "No solution steps found"
                    message = "Enter the solution steps before confirming the analysis "
                    message += "setup or trying to solve the harmonic analysis."
                    PrintMessageInput([error_title, title, message])
                    self.solution_steps_setup_callback()
                    return

        analysis_setup_data = {
            "analysis_id" : analysis_id,
            "analysis_method" : analysis_method,
            "frequency_spacing" : frequency_spacing,
        }

        if analysis_method == AnalysisMethod.MODE_SUPERPOSITION:
            if self.lineEdit_modes_to_expand.text() == "":
                self.lineEdit_modes_to_expand.setFocus()
                return True

            analysis_setup_data["modes_number"] = int(self.lineEdit_modes_to_expand.text())

        if AnalysisID.is_harmonic(analysis_id):

            if frequency_spacing == FrequencySpacing.USER_DEFINED:
                if len(self.user_defined_solution_steps) == 0:
                    if isinstance(self.analysis_setup, HarmonicAnalysisSetup):
                        if self.analysis_setup.frequency_spacing == FrequencySpacing.USER_DEFINED:
                            self.user_defined_solution_steps = self.model.frequencies

                analysis_setup_data.update(
                    {"frequencies" : np.array(self.user_defined_solution_steps, dtype=float)}
                    )

            if len(self.user_defined_solution_steps) == 0:
                freq_data = self.check_frequencies_inputs()
                if not isinstance(freq_data, dict):
                    return True

                analysis_setup_data.update(freq_data)

        is_harmonic_structural = AnalysisID(analysis_id).is_harmonic_structural()
        if is_harmonic_structural:
            analysis_setup_data["global_damping"] = self.check_damping_inputs()

        analysis_setup = self.model.get_harmonic_analysis_setup(**analysis_setup_data)

        if is_harmonic_structural:
            # In order to avoid the division-by-zero error, we must filter out the zero frequency from the 
            #  structural harmonic analysis if there is a prescribed velocity or acceleration in the model
            if self.model.properties.is_there_a_prescribed_velocity_or_acceleration_in_the_model():
                analysis_setup = self.model.modify_analysis_setup_to_filter_zero_frequency(analysis_setup)

        app().project.configure_analysis(analysis_setup)

        self.setup_defined = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()

        if app().main_window.action_results_workspace.isChecked():
            app().main_window.action_model_workspace_callback()

        if not self.keep_window_open_after_enter_setup:
            self.close()

        return False

    def run_analysis(self):

        # if not self.model.is_there_a_valid_mesh():
        #     if mesher_interface_callback(self, close_after_generate=True):
        #         return

        if self.enter_setup_callback():
            return

        self.solve_analysis = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()

    def closeEvent(self, a0):
        self.keep_window_open = False
        # check if there is no updated analysis setup
        self.check_analysis_setup_update()
        return super().closeEvent(a0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.run_analysis()
        elif event.key() == Qt.Key_Escape:
            self.close()