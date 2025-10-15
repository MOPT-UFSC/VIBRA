from PySide6.QtWidgets import QToolBar, QComboBox, QLabel, QPushButton, QWidget
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, QSize, Signal

from vibra import ICON_DIR, app
from vibra.engine import AnalysisID
from vibra.interface.analysis.acoustic_modal_analysis_input import AcousticModalAnalysisInput
from vibra.interface.analysis.structural_modal_analysis_input import StructuralModalAnalysisInput
from vibra.interface.analysis.harmonic_analysis_setup_input import HarmonicAnalysisSetupInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.loading_window import LoadingWindow

import logging
from typing import Literal
from time import time

AnalysisType = Literal[
    "",
    "Harmonic",
    "Modal"
]

PhysicalDomain = Literal[
    "",
    "Structural",
    "Acoustic"
]


class AnalysisToolbar(QToolBar):

    enable_pushbutons = Signal()

    def __init__(self):
        super().__init__()

        self._load_icons()
        self._define_qt_variables()
        self._configure_layout()
        self._configure_appearance()
        self._config_widgets()
        self._load_analysis_types()
        self._create_connections()

        self.setWindowTitle("Analysis toolbar")

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

        app().project.can_resume_solution_changed.connect(self.update_pushbutton_resume_analysis)

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
                border-width: 1px;
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
        self.pushButton_run_analysis.setDisabled(True)

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

        analysis_type, physical_domain = app().project.get_analysis_type_and_physical_domain()

        if analysis_type == "harmonic":
            self.combo_box_analysis_type.setCurrentIndex(0)
        elif analysis_type == "modal":
            self.combo_box_analysis_type.setCurrentIndex(1)
        elif analysis_type == "static":
            self.combo_box_analysis_type.setCurrentIndex(2)

        if physical_domain == "structural":
            self.combo_box_physical_domain.setCurrentIndex(0)
        elif physical_domain == "acoustic":
            self.combo_box_physical_domain.setCurrentIndex(1)
        elif physical_domain == "coupled":
            self.combo_box_physical_domain.setCurrentIndex(2)

        if block_signals:
            self.combo_box_analysis_type.blockSignals(False)
            self.combo_box_physical_domain.blockSignals(False)

    def set_pushbutton_run_analysis_enabled(self, enable: bool = True):
        self.pushButton_run_analysis.setEnabled(enable)

    def set_pushbutton_resume_analysis_enabled(self, enable=True):
        self.pushButton_resume_analysis.setEnabled(enable)

    def update_pushbutton_resume_analysis(self, can_resume_value: bool):
        self.pushButton_resume_analysis.setEnabled(can_resume_value)

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
        current_analysis_id = self.get_current_analysis_id()
        valid_setup = app().project.is_there_a_valid_analysis_setup(current_analysis_id=current_analysis_id)
        self.set_pushbutton_run_analysis_enabled(valid_setup)

    def run_analysis(self, is_resume: bool = False):

        if app().main_window.action_results_workspace.isChecked():
            app().main_window.action_model_workspace_callback()

        # Do not solve models with collapsed elements!
        mesh = app().project.model.mesh   
        collapsed = (mesh.collapsed_3d_elements or mesh.collapsed_2d_elements or mesh.collapsed_1d_elements)
        if collapsed:
            return

        self.update_analysis_combo_boxes()
        if app().project.run_analysis(is_resume):
            return

        if app().project.model.stop_processing:
            app().project.model.toggle_processing_callback()
            app().file.remove_results_data_from_project_file()
            return

        if is_resume:
            app().project.can_resume_solution = False

        LoadingWindow(self.post_processing_analysis).run()

    def post_processing_analysis(self):
        logging.info("Post-processing results... [10/100]")
        self.set_pushbutton_reset_solution_enabled()

        logging.info("Post-processing results... [65/100]")
        app().main_window.model_setup_widget.model_setup_items.update_items_appearance()

        if not app().file.geometry_data_filepath.exists():
            app().file.write_geometry_data_in_file()

        logging.info("Post-processing results... [85/100]")
        if not app().file.mesh_data_filepath.exists():
            app().file.write_mesh_data_in_file()

        logging.info("Post-processing results... [90/100]")
        app().file.write_model_properties_in_file()

        logging.info("Post-processing results... [95/100]")
        app().file.write_results_data_in_file()

    def project_solution_data_reset_callback(self):

        title = "Removal of project solution data"
        message = "Would you like to delete all solution data from this project? "
        tool_tip = "Be aware, this process cannot be undone."

        buttons_config = {
                          "left_button_label": "Cancel", 
                          "right_button_label": "Delete all",
                          "right_toolTip" : tool_tip
                          }

        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config, window_title="Vibra")
        if read._cancel:
            return

        if not read._continue:
            return

        self.reset_solution(True)

    def reset_solution(self, force_delete_harmonic = False):
        app().project.reset_solutions()
        app().file.remove_results_data_from_project_file()

        if force_delete_harmonic:
            app().file.delete_harmonic_solution()

        self.pushButton_reset_solution.setDisabled(True)
        app().main_window.project_data_modified = True
        app().main_window.action_model_workspace_callback()
        app().main_window.disable_advanced_acoustic_plots_buttons(True)

    def configure_analysis(self):

        analysis_type : AnalysisType = self.combo_box_analysis_type.currentText()
        physical_domain : PhysicalDomain = self.combo_box_physical_domain.currentText()

        if analysis_type == "Harmonic":
            if physical_domain == "Structural":
                self.harmonic_structural()
            elif physical_domain == "Acoustic":
                self.harmonic_acoustic()

        elif analysis_type == "Modal":
            if physical_domain == "Structural":
                self.modal_structural()
            elif physical_domain == "Acoustic":
                self.modal_acoustic()

        # disable run_analysis button if there are collapsed elements
        mesh = app().project.model.mesh   
        collapsed = (mesh.collapsed_3d_elements or mesh.collapsed_2d_elements or mesh.collapsed_1d_elements)
        self.pushButton_run_analysis.setDisabled(bool(collapsed))

    def harmonic_structural(self):

        harmonic = HarmonicAnalysisSetupInput(analysis_id=AnalysisID.STRUCTURAL_HARMONIC)

        if harmonic.setup_defined:
            self.final_actions()

        if harmonic.solve_analysis:
            self.run_analysis()
            app().main_window.update_symbols()

    def harmonic_acoustic(self):

        harmonic = HarmonicAnalysisSetupInput(analysis_id=AnalysisID.ACOUSTIC_HARMONIC)

        if harmonic.setup_defined:
            self.final_actions()

        if harmonic.solve_analysis:
            self.run_analysis()
    
    def modal_structural(self):
        modal = StructuralModalAnalysisInput()

        if modal.modes_number is None:
            return

        if modal.setup_defined:
            self.update_analysis_setup(modal.analysis_setup)
            self.pushButton_run_analysis.setEnabled(True)
            self.final_actions()

        if modal.proceed_solution:
            self.run_analysis()

    def modal_acoustic(self):
        modal = AcousticModalAnalysisInput()

        if modal.modes_number is None:
            return

        if modal.setup_defined:
            self.update_analysis_setup(modal.analysis_setup)
            self.pushButton_run_analysis.setEnabled(True)
            self.final_actions()

        if modal.proceed_solution:
            self.run_analysis()

    def update_analysis_setup(self, analysis_setup: dict):

        keys_to_ignore = list(analysis_setup.keys())
        if isinstance(app().project.analysis_setup, dict):
            for key, value in app().project.analysis_setup.items():
                if key in keys_to_ignore:
                    continue
                analysis_setup[key] = value

        app().project.set_analysis_setup(analysis_setup)

    def final_actions(self):
        self.reset_solution()
        app().project.create_solver()
        app().file.write_analysis_setup_in_file(app().project.analysis_setup)