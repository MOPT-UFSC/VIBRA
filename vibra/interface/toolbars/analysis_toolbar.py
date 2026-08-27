import logging

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import QComboBox, QLabel, QPushButton, QToolBar, QWidget

from vibra import app
from vibra.engine import AnalysisID
from vibra.engine.analysis_info import AnalysisType, PhysicalDomain
from vibra.engine.checkers.analysis_checker import AnalysisChecker
from vibra.interface.analysis.harmonic_analysis_setup_input import HarmonicAnalysisSetupInput
from vibra.interface.analysis.modal_analysis_input import ModalAnalysisInput
from vibra.interface.formatters.icons import Icon
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.loading_window import LoadingWindow
from vibra.utils.RamMonitor import RamMonitor
from vibra.utils.subprocess.subprocess_handler import SubProcessHandler, SubProcessStatus


class AnalysisToolbar(QToolBar):
    enable_pushbutons = Signal()

    def __init__(self):
        super().__init__()

        self.solve_analysis = False

        self._load_icons()
        self._define_qt_variables()
        self._configure_layout()
        self._configure_appearance()
        self._config_widgets()
        self._load_analysis_types()
        self._create_connections()

        self.setWindowTitle("Analysis toolbar")

    @property
    def model(self):
        return app().project.model

    @property
    def mesh(self):
        return app().project.model.mesh

    def _load_icons(self):
        self.configure_analysis_icon = Icon(":/icons/settings.png")
        self.reset_solution_icon = Icon(":/icons/reset_icon.png")
        self.resume_solution_icon = Icon(":/icons/resume_icon.png")
        self.run_analysis_icon = Icon(":/icons/go_next.png")

    def _define_qt_variables(self):

        # QComboBox
        self.combo_box_analysis_type = QComboBox()
        self.combo_box_physical_domain = QComboBox()

        # QLabel
        self.label_analysis_type = QLabel("Analysis type:")
        self.label_analysis_domain = QLabel("Physical domain:")

        # QPushButton
        self.run_analysis_action = QAction(self.run_analysis_icon, "Run Analysis", self)
        self.configure_analysis_action = QAction(self.configure_analysis_icon, "Analysis Setup", self)
        self.reset_solution_action = QAction(self.reset_solution_icon, "Reset Solution", self)
        self.resume_solution_action = QAction(self.resume_solution_icon, "Resume Solution", self)

    def _create_connections(self):
        #
        self.combo_box_physical_domain.currentTextChanged.connect(self.check_analysis_setup_callback)
        self.combo_box_analysis_type.currentTextChanged.connect(self.analysis_type_callback)
        #
        self.run_analysis_action.triggered.connect(self.run_analysis_callback)
        self.resume_solution_action.triggered.connect(lambda: self.run_analysis_callback(True))
        self.configure_analysis_action.triggered.connect(self.configure_analysis_callback)
        self.reset_solution_action.triggered.connect(self.reset_solution_callback)
        #
        self.enable_pushbutons.connect(self.check_analysis_setup_callback)
        self.enable_pushbutons.connect(self.update_reset_solution_button_accessibility)

    def _configure_appearance(self):
        self.setMinimumHeight(40)
        self.setMovable(True)
        self.setFloatable(True)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        font = QFont()
        font.setPointSize(10)

        widgets_type = [QComboBox, QLabel, QPushButton]
        for widget_type in widgets_type:
            for widget in self.findChildren(widget_type):
                widget.setFont(font)

    def get_spacer(self):
        spacer = QWidget()
        spacer.setFixedWidth(8)
        return spacer

    def _configure_layout(self):
        #
        self.addSeparator()
        self.addWidget(self.label_analysis_type)
        self.addWidget(self.combo_box_analysis_type)
        self.addWidget(self.get_spacer())
        #
        self.addWidget(self.label_analysis_domain)
        self.addWidget(self.combo_box_physical_domain)
        self.addWidget(self.get_spacer())
        #
        self.addSeparator()
        self.addWidget(self.get_spacer())
        self.addAction(self.configure_analysis_action)
        self.addWidget(self.get_spacer())
        self.addAction(self.run_analysis_action)
        self.addWidget(self.get_spacer())
        self.addAction(self.reset_solution_action)
        self.addWidget(self.get_spacer())
        self.addAction(self.resume_solution_action)
        #
        self.adjustSize()

    def _config_widgets(self):

        # QComboBox
        self.combo_box_analysis_type.setFixedSize(100, 28)
        self.combo_box_physical_domain.setFixedSize(100, 28)

        # QAction
        self.configure_analysis_action.setToolTip("Configure the analysis settings")
        self.resume_solution_action.setToolTip("Resume the analysis")
        self.run_analysis_action.setToolTip("Run the analysis")
        self.reset_solution_action.setToolTip("Reset Solution")
        #
        self.reset_solution_action.setDisabled(True)
        self.resume_solution_action.setVisible(False)

    def _load_analysis_types(self):

        for analysis_type in ["Harmonic", "Modal"]:
            self.combo_box_analysis_type.addItem(analysis_type)

        for physical_domain in ["Structural", "Acoustic"]:
            self.combo_box_physical_domain.addItem(physical_domain)

        # default setup
        self.combo_box_analysis_type.setCurrentText("Harmonic")
        self.combo_box_physical_domain.setCurrentText("Acoustic")

    def update_analysis_combo_boxes(self, block_signals: bool = False):

        if block_signals:
            self.combo_box_analysis_type.blockSignals(block_signals)
            self.combo_box_physical_domain.blockSignals(block_signals)

        analysis_type = app().project.get_analysis_type()
        physical_domain = app().project.get_physical_domain()

        match analysis_type:
            case AnalysisType.HARMONIC:
                self.combo_box_analysis_type.setCurrentIndex(0)
            case AnalysisType.MODAL:
                self.combo_box_analysis_type.setCurrentIndex(1)
            case AnalysisType.STATIC:
                self.combo_box_analysis_type.setCurrentIndex(2)

        match physical_domain:
            case PhysicalDomain.STRUCTURAL:
                self.combo_box_physical_domain.setCurrentIndex(0)
            case PhysicalDomain.ACOUSTIC:
                self.combo_box_physical_domain.setCurrentIndex(1)
            case PhysicalDomain.COUPLED:
                self.combo_box_physical_domain.setCurrentIndex(2)

        if block_signals:
            self.combo_box_analysis_type.blockSignals(False)
            self.combo_box_physical_domain.blockSignals(False)

    def update_resume_soluton_button_visibility(self):
        can_resume_solution = app().project.model.can_resume_solution
        self.resume_solution_action.setVisible(can_resume_solution)

    def update_reset_solution_button_accessibility(self):
        solution_exists = self.model.solution is not None
        self.reset_solution_action.setEnabled(solution_exists)
        self.update_resume_soluton_button_visibility()

    def get_current_analysis_id(self):
        analysis_type = self.combo_box_analysis_type.currentText()
        physical_domain = self.combo_box_physical_domain.currentText()

        if analysis_type == "Harmonic":
            if physical_domain == "Structural":
                return AnalysisID.STRUCTURAL_HARMONIC
            else:
                return AnalysisID.ACOUSTIC_HARMONIC

        elif analysis_type == "Modal":
            if physical_domain == "Structural":
                return AnalysisID.STRUCTURAL_MODAL
            else:
                return AnalysisID.ACOUSTIC_MODAL

        return AnalysisID.NO_ANALYSIS

    def is_analysis_setup_valid(self):
        current_analysis_id = self.get_current_analysis_id()
        return self.model.is_there_a_valid_analysis_setup(current_analysis_id=current_analysis_id)

    def analysis_type_callback(self):
        analysis_id = self.model.analysis_id
        new_analysis_id = self.get_current_analysis_id()
        self.run_analysis_action.setEnabled(analysis_id == new_analysis_id)
        self.combo_box_physical_domain.blockSignals(False)
        self.check_analysis_setup_callback()

    def check_analysis_setup_callback(self):
        app().main_window.update_symbols()
        app().main_window.update_info_text()
        valid_analysis_setup = self.is_analysis_setup_valid()
        self.run_analysis_action.setEnabled(valid_analysis_setup)
        # self.domain_changed.emit()

    def run_analysis_callback(self, is_resume: bool = False):
        app().project.mark_solution_as_outdated(reset=True)
        if app().config.user_preferences.run_analysis_in_subprocess:
            self.run_analysis_in_subprocess(is_resume)
        else:
            self.run_analysis_in_current_process(is_resume)

    def run_analysis_in_current_process(self, is_resume: bool = False):
        if self.model.analysis_setup is None:
            self.configure_analysis_callback()
            if not self.solve_analysis:
                return

        if app().main_window.action_results_workspace.isChecked():
            app().main_window.action_model_workspace_callback()

        app().main_window.action_results_workspace.setDisabled(True)
        app().main_window.results_viewer_widget.clear_treeWidgets_of_frequencies()

        self.update_analysis_combo_boxes()

        if app().project.model.analysis_id.is_harmonic():
            interrupt_function = self.model.toggle_processing_callback
        else:
            interrupt_function = None

        LoadingWindow(app().project.run_analysis, interrupt_function).run(is_resume)

        self.solve_analysis = False

        if self.model.stop_processing:
            self.model.toggle_processing_callback()
            app().project.project_writer.delete_results_data()
            return

        app().main_window.configure_results_render_widget()
        app().main_window.results_viewer_widget.results_viewer_items.update_items()

        LoadingWindow(self.post_processing_analysis).run()

    @RamMonitor()
    def run_analysis_in_subprocess(self, is_resume: bool = True) -> bool:
        if app().main_window.action_results_workspace.isChecked():
            app().main_window.action_model_workspace_callback()

        app().main_window.action_results_workspace.setDisabled(True)
        app().main_window.results_viewer_widget.clear_treeWidgets_of_frequencies()

        checker = AnalysisChecker(self.model)
        checker.check_analysis_requirements()

        app().project.write_to_working_dir()

        flag = "--continue-analysis" if is_resume else "--run-analysis"
        command = f"{SubProcessHandler.get_executable()} {flag} {str(app().project.working_directory)}"
        subprocess_status = SubProcessHandler(command).run()

        if subprocess_status != SubProcessStatus.SUCCESS:
            app().project.reset_solution()
            return False

        app().project.reload_solution_from_working_dir()

        app().main_window.configure_results_render_widget()
        app().main_window.results_viewer_widget.results_viewer_items.update_items()

        LoadingWindow(self.post_processing_analysis).run()
        return True

    def post_processing_analysis(self):
        logging.info("Post-processing results... [10/100]")
        self.update_reset_solution_button_accessibility()

        logging.info("Post-processing results... [65/100]")
        app().main_window.model_setup_widget.model_setup_items.update_items_appearance()

    def reset_solution_callback(self):

        title = "Removal of project solution data"
        message = "Would you like to delete all solution data from this project? "
        tool_tip = "Be aware, this process cannot be undone."

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Delete all",
            "right_toolTip": tool_tip,
        }

        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config, window_title="Vibra")
        if read._cancel:
            return

        if not read._continue:
            return

        self.reset_solution()

    def reset_solution(self):
        app().project.reset_solution()
        app().project.mark_project_as_modified()
        self.update_reset_solution_button_accessibility()
        app().main_window.action_model_workspace_callback()
        app().main_window.action_export_element_transfer_data.setDisabled(True)

    def configure_analysis_callback(self):

        self.solve_analysis = False

        match self.get_current_analysis_id():
            case AnalysisID.STRUCTURAL_HARMONIC:
                self.harmonic_analysis_setup_callback(AnalysisID.STRUCTURAL_HARMONIC)
            case AnalysisID.ACOUSTIC_HARMONIC:
                self.harmonic_analysis_setup_callback(AnalysisID.ACOUSTIC_HARMONIC)
            case AnalysisID.STRUCTURAL_MODAL:
                self.modal_analysis_setup_callback(AnalysisID.STRUCTURAL_MODAL)
            case AnalysisID.ACOUSTIC_MODAL:
                self.modal_analysis_setup_callback(AnalysisID.ACOUSTIC_MODAL)

    def harmonic_analysis_setup_callback(self, analysis_id: AnalysisID):
        harmonic = HarmonicAnalysisSetupInput(analysis_id)
        self.solve_analysis = harmonic.solve_analysis

        if self.solve_analysis:
            self.run_analysis_callback()
            app().main_window.update_symbols()

    def modal_analysis_setup_callback(self, analysis_id: AnalysisID):
        modal = ModalAnalysisInput(analysis_id)
        self.solve_analysis = modal.proceed_solution

        if self.solve_analysis:
            self.run_analysis_callback()
