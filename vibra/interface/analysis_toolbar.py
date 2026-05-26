import logging

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QComboBox, QLabel, QPushButton, QToolBar, QWidget

from vibra import ICON_DIR, app
from vibra.engine import AnalysisID
from vibra.engine.analysis_info import AnalysisType, PhysicalDomain
from vibra.interface.analysis.harmonic_analysis_setup_input import HarmonicAnalysisSetupInput
from vibra.interface.analysis.modal_analysis_input import ModalAnalysisInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.loading_window import LoadingWindow


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
        self.settings_icon = QIcon(str(ICON_DIR / "settings.png"))
        self.solution_icon = QIcon(str(ICON_DIR / "go_next.png"))
        self.resume_icon = QIcon(str(ICON_DIR / "resume_icon.png"))
        self.reset_icon = QIcon(str(ICON_DIR / "reset_icon.png"))

    def _define_qt_variables(self):

        # QComboBox
        self.combo_box_analysis_type = QComboBox()
        self.combo_box_physical_domain = QComboBox()

        # QLabel
        self.label_analysis_type = QLabel("Analysis type:")
        self.label_analysis_domain = QLabel("Physical domain:")

        # QPushButton
        self.pushButton_run_analysis = QPushButton(self)
        self.pushButton_configure_analysis = QPushButton(self)
        self.pushButton_reset_solution = QPushButton(self)
        self.pushButton_resume_analysis = QPushButton(self)

    def _create_connections(self):
        #
        self.combo_box_physical_domain.currentTextChanged.connect(self.check_analysis_setup_callback)
        self.combo_box_analysis_type.currentTextChanged.connect(self.check_analysis_setup_callback)
        #
        self.pushButton_run_analysis.clicked.connect(self.run_analysis)
        self.pushButton_resume_analysis.clicked.connect(lambda: self.run_analysis(True))
        self.pushButton_configure_analysis.clicked.connect(self.configure_analysis)
        self.pushButton_reset_solution.clicked.connect(self.project_solution_data_reset_callback)
        self.enable_pushbutons.connect(self.check_analysis_setup_callback)
        self.enable_pushbutons.connect(self.set_pushbutton_reset_solution_enabled)

        # app().project.can_resume_solution_changed.connect(self.update_pushbutton_resume_analysis)

    def _configure_appearance(self):
        self.setMinimumHeight(40)
        self.setMovable(True)
        self.setFloatable(True)

        font = QFont()
        font.setPointSize(10)

        widgets_type = [QComboBox, QLabel, QPushButton]
        for widget_type in widgets_type:
            for widget in self.findChildren(widget_type):
                widget.setFont(font)

        self.setStyleSheet(
            """
            QToolBar {
                border-style: solid;
                border-width: 0.5px;
                border-color: #888888;
            }
            """
        )

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
        self.addWidget(self.pushButton_configure_analysis)
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_run_analysis)
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_resume_analysis)
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_reset_solution)
        #
        self.adjustSize()

    def _config_widgets(self):

        # QComboBox
        self.combo_box_analysis_type.setFixedSize(100, 28)
        self.combo_box_physical_domain.setFixedSize(100, 28)

        # QPushButton
        self.pushButton_configure_analysis.setFixedSize(50, 30)
        self.pushButton_configure_analysis.setIcon(self.settings_icon)
        self.pushButton_configure_analysis.setIconSize(QSize(20, 20))
        self.pushButton_configure_analysis.setCursor(Qt.PointingHandCursor)
        self.pushButton_configure_analysis.setToolTip("Configure the analysis")

        self.pushButton_run_analysis.setFixedSize(50, 30)
        self.pushButton_run_analysis.setIcon(self.solution_icon)
        self.pushButton_run_analysis.setIconSize(QSize(20, 20))
        self.pushButton_run_analysis.setCursor(Qt.PointingHandCursor)
        self.pushButton_run_analysis.setToolTip("Run the analysis")

        self.pushButton_resume_analysis.setFixedSize(50, 30)
        self.pushButton_resume_analysis.setIcon(self.resume_icon)
        self.pushButton_resume_analysis.setIconSize(QSize(20, 20))
        self.pushButton_resume_analysis.setCursor(Qt.PointingHandCursor)
        self.pushButton_resume_analysis.setToolTip("Resume the analysis")
        self.pushButton_resume_analysis.setDisabled(True)

        self.pushButton_reset_solution.setFixedSize(50, 30)
        self.pushButton_reset_solution.setIcon(self.reset_icon)
        self.pushButton_reset_solution.setIconSize(QSize(20, 20))
        self.pushButton_reset_solution.setCursor(Qt.PointingHandCursor)
        self.pushButton_reset_solution.setToolTip("Reset Solution")
        self.pushButton_reset_solution.setDisabled(True)

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

    def set_pushbutton_resume_analysis_enabled(self, enable=True):
        self.pushButton_resume_analysis.setEnabled(enable)

    def update_pushbutton_resume_analysis(self):
        can_resume_solution = app().project.can_resume_solution
        self.pushButton_resume_analysis.setEnabled(can_resume_solution)

    def set_pushbutton_reset_solution_enabled(self):
        self.pushButton_reset_solution.setEnabled(True)

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

    def check_analysis_setup_callback(self):
        app().main_window.update_symbols()
        app().main_window.update_info_text()

    def run_analysis(self, is_resume: bool = False):
        if self.model.analysis_setup is None:
            self.configure_analysis()
            if not self.solve_analysis:
                return

        if app().main_window.action_results_workspace.isChecked():
            app().main_window.action_model_workspace_callback()

        app().main_window.action_results_workspace.setDisabled(True)
        app().main_window.results_viewer_widget.clear_treeWidgets_of_frequencies()

        self.update_analysis_combo_boxes()

        if app().project.analysis_id.is_harmonic():
            interrupt_function = self.model.toggle_processing_callback
        else:
            interrupt_function = None

        LoadingWindow(
            app().project.run_analysis,
            interrupt_function,
        ).run()

        self.solve_analysis = False

        if self.model.stop_processing:
            self.model.toggle_processing_callback()
            app().project.project_writer.delete_results_data()
            return

        app().main_window.configure_results_render_widget()
        app().main_window.results_viewer_widget.results_viewer_items.update_items()

        LoadingWindow(self.post_processing_analysis).run()

    def post_processing_analysis(self):
        logging.info("Post-processing results... [10/100]")
        self.set_pushbutton_reset_solution_enabled()

        logging.info("Post-processing results... [65/100]")
        app().main_window.model_setup_widget.model_setup_items.update_items_appearance()

    def project_solution_data_reset_callback(self):

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

        self.reset_solution(True)

    def reset_solution(self, force_delete_harmonic=False):
        app().project.reset_solution()
        self.pushButton_reset_solution.setDisabled(True)
        app().main_window.project_data_modified = True
        app().main_window.action_model_workspace_callback()
        app().main_window.action_export_element_transfer_data.setDisabled(True)

    def configure_analysis(self):

        self.solve_analysis = False

        match self.get_current_analysis_id():
            case AnalysisID.STRUCTURAL_HARMONIC:
                self.harmonic_structural()
            case AnalysisID.ACOUSTIC_HARMONIC:
                self.harmonic_acoustic()
            case AnalysisID.STRUCTURAL_MODAL:
                self.modal_structural()
            case AnalysisID.ACOUSTIC_MODAL:
                self.modal_acoustic()

    # TODO: these functions are almost equal.
    # Maybe they can be unified into a single one.
    def harmonic_structural(self):
        analysis_id = AnalysisID.STRUCTURAL_HARMONIC
        harmonic = HarmonicAnalysisSetupInput(analysis_id)
        self.solve_analysis = harmonic.solve_analysis

        if self.solve_analysis:
            self.run_analysis()
            app().main_window.update_symbols()

    def harmonic_acoustic(self):
        analysis_id = AnalysisID.ACOUSTIC_HARMONIC
        harmonic = HarmonicAnalysisSetupInput(analysis_id)
        self.solve_analysis = harmonic.solve_analysis

        if self.solve_analysis:
            self.run_analysis()

    def modal_structural(self):
        analysis_id = AnalysisID.STRUCTURAL_MODAL
        modal = ModalAnalysisInput(analysis_id)
        self.solve_analysis = modal.proceed_solution

        if modal.setup_defined:
            app().project.configure_analysis(
                analysis_id,
                modal.analysis_setup,
            )

        if self.solve_analysis:
            self.run_analysis()

    def modal_acoustic(self):
        analysis_id = AnalysisID.ACOUSTIC_MODAL
        modal = ModalAnalysisInput(analysis_id)
        self.solve_analysis = modal.proceed_solution

        if modal.setup_defined:
            app().project.configure_analysis(
                analysis_id,
                modal.analysis_setup,
            )

        if self.solve_analysis:
            self.run_analysis()
