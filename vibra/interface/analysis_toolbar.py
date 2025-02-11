from PyQt5.QtWidgets import QToolBar, QComboBox, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal

from vibra.interface.analysis.acoustic_modal_analysis_input import AcousticModalAnalysisInput
from vibra.interface.analysis.harmonic_analysis_method_selector_input import StructuralHarmonicAnalysisMethodSelecorInput
from vibra.interface.analysis.structural_modal_analysis_input import StructuralModalAnalysisInput
from vibra.interface.analysis.analysis_setup_input import AnalysisSetupInput

from vibra import ICON_DIR, app

from typing import Literal

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

    enable_pushbutons = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.main_window = app().main_window

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
        self.reset_icon = QIcon(str(ICON_DIR / "reset_icon.png"))

    def _define_qt_variables(self):

        # QComboBox
        self.combo_box_analysis_type = QComboBox()
        self.combo_box_analysis_domain = QComboBox()

        # QLabel
        self.label_analysis_type = QLabel("Analysis type:")
        self.label_analysis_domain = QLabel("Physical domain:")

        # QPushButton
        self.pushButton_run_analysis = QPushButton(self)
        self.pushButton_configure_analysis = QPushButton(self)
        self.pushButton_reset_solution = QPushButton(self)
    
    def _create_connections(self):
        self.pushButton_run_analysis.clicked.connect(self.run_analysis)
        self.pushButton_configure_analysis.clicked.connect(self.configure_analysis)
        self.pushButton_reset_solution.clicked.connect(self.reset_solution)
        self.enable_pushbutons.connect(self.update_pushbutton_run_analysis)
        self.enable_pushbutons.connect(self.update_pushbutton_reset_solution)
        self.combo_box_analysis_domain.currentTextChanged.connect(lambda: self.update_pushbutton_run_analysis(True))
        self.combo_box_analysis_type.currentTextChanged.connect(lambda: self.update_pushbutton_run_analysis(True))

    def _configure_appearance(self):
        self.setMinimumHeight(40)
        self.setMovable(True)
        self.setFloatable(True)

        font = QFont()
        font.setPointSize(10)

        for widget in self.findChildren((QComboBox, QLabel, QPushButton)):
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
        self.addWidget(self.combo_box_analysis_domain)
        self.addWidget(self.get_spacer())
        #
        self.addSeparator()
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_configure_analysis)
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_run_analysis)
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_reset_solution)
        #
        self.adjustSize()

    def _config_widgets(self):

        # QComboBox
        self.combo_box_analysis_type.setFixedSize(100, 28)
        self.combo_box_analysis_domain.setFixedSize(100, 28)

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

        self.pushButton_reset_solution.setFixedSize(50, 30)
        self.pushButton_reset_solution.setIcon(self.reset_icon)
        self.pushButton_reset_solution.setIconSize(QSize(20, 20))
        self.pushButton_reset_solution.setCursor(Qt.PointingHandCursor)
        self.pushButton_reset_solution.setToolTip("Reset Solution")
        self.pushButton_reset_solution.setDisabled(True)
    
    def _load_analysis_types(self):
        self.combo_box_analysis_type.addItem("Harmonic")
        self.combo_box_analysis_type.addItem("Modal")

        self.combo_box_analysis_domain.addItem("Structural")
        self.combo_box_analysis_domain.addItem("Acoustic")
    
    def update_pushbutton_run_analysis(self, disable=False):
        self.pushButton_run_analysis.setDisabled(disable)
    
    def update_pushbutton_reset_solution(self):
        self.pushButton_reset_solution.setDisabled(False)

    def update_analysis_combo_boxes(self):
        analysis_type, analysis_domain = app().project.last_analysis.split()
        
        if analysis_type == "Harmonic":
            self.combo_box_analysis_type.setCurrentIndex(0)
        else:
            self.combo_box_analysis_type.setCurrentIndex(1)

        if analysis_domain == "Structural":
            self.combo_box_analysis_domain.setCurrentIndex(0)
        else:
            self.combo_box_analysis_domain.setCurrentIndex(1)
    
    def run_analysis(self):
        self.main_window.menu_widget.run_analysis()
        self.update_pushbutton_reset_solution()
    
    def reset_solution(self):
        app().project.reset_solutions()
        app().file.remove_results_data_from_project_file()
        
        self.pushButton_reset_solution.setDisabled(True)
        self.pushButton_run_analysis.setDisabled(True)
        app().main_window.action_model_workspace_callback()
        app().main_window.disable_advanced_acoustic_plots_buttons(True)
        app().project.last_analysis = None

    def configure_analysis(self):
        analysis_type : AnalysisType = self.combo_box_analysis_type.currentText()
        physical_domain : PhysicalDomain = self.combo_box_analysis_domain.currentText()

        self.pushButton_run_analysis.setDisabled(True)

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
        
    def harmonic_structural(self):
        select = StructuralHarmonicAnalysisMethodSelecorInput()
        method_id = select.index

        analysis_type_label = "Structural Harmonic Analysis"

        if method_id == 0:
            analysis_id = 0
            analysis_method_label = "Direct Method"
        else:
            analysis_id = 1
            analysis_method_label = "Mode Superposition Method"
        #
        analysis_data = {
            "analysis_id": analysis_id,
            "analysis_type": analysis_type_label,
            "analysis_method_label": analysis_method_label,
        }
        self.finalize(analysis_data, analysis_id)
        self.run_analysis()
    
    def harmonic_acoustic(self):
        method_id = 0
        analysis_id = 3
        analysis_type_label = "Acoustic Harmonic Analysis"
        analysis_method_label = "Direct Method"
        #
        analysis_data = {
            "analysis_id": analysis_id,
            "analysis_type": analysis_type_label,
            "analysis_method_label": analysis_method_label,
        }
        self.finalize(analysis_data, analysis_id)
        harmonic = AnalysisSetupInput()
        if harmonic.solve_analysis:
            self.run_analysis()
    
    def modal_structural(self):
        modal = StructuralModalAnalysisInput()

        if modal.modes is None:
            return

        if modal.setup_defined:
            self.finalize(modal.analysis_setup, modal.analysis_setup["analysis_id"])
       
        if modal.proceed_solution:
            self.run_analysis()

    def modal_acoustic(self):
        modal = AcousticModalAnalysisInput()

        if modal.modes is None:
            return
        
        if modal.setup_defined:
            self.finalize(modal.analysis_setup, modal.analysis_setup["analysis_id"])
        
        if modal.proceed_solution:
            self.run_analysis()

    def finalize(self, analysis_data: dict, analysis_id: int):
        if app().project.analysis_data is not None:
            for key, value in app().project.analysis_data.items():
                if key in ["f_min", "f_max", "f_step", "frequencies"]:
                    analysis_data[key] = value

        app().project.set_analysis_data(analysis_data)
        app().project.create_solver()

        if analysis_id in [2, 3, 4]:
            app().file.write_analysis_setup_in_file(analysis_data)

