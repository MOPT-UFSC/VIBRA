from PySide6.QtWidgets import QToolBar, QComboBox, QLabel, QPushButton, QWidget
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, QSize, Signal


from vibra import ICON_DIR, app
from vibra.engine import AnalysisID
from vibra.interface.mesh.set_mesh_setup_inputs import MeshSetupInputs
from vibra.interface.message.loading_window import LoadingWindow
from vibra.interface.message.loading_window_2 import LoadTask
from vibra.interface.analysis.acoustic_modal_analysis_input import AcousticModalAnalysisInput
from vibra.interface.analysis.harmonic_analysis_method_selector_input import StructuralHarmonicAnalysisMethodSelecorInput
from vibra.interface.analysis.structural_modal_analysis_input import StructuralModalAnalysisInput
from vibra.interface.analysis.structural_harmonic_analysis_direct_method_input import StructuralHarmonicAnalysisDirectMethodInput
from vibra.interface.analysis.acoustic_harmonic_analysis_direct_method_input import AcousticHarmonicAnalysisDirectMethodInput
from vibra.interface.message.exception_message import ExceptionMessage
from vibra.errors import ModelException

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

    enable_pushbutons = Signal()

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
        self.combo_box_physical_domain = QComboBox()

        # QLabel
        self.label_analysis_type = QLabel("Analysis type:")
        self.label_analysis_domain = QLabel("Physical domain:")

        # QPushButton
        self.pushButton_run_analysis = QPushButton(self)
        self.pushButton_configure_analysis = QPushButton(self)
        self.pushButton_reset_solution = QPushButton(self)

    def _create_connections(self):
        #
        # self.combo_box_physical_domain.currentIndexChanged.connect(self._update_state)
        # self.combo_box_analysis_type.currentIndexChanged.connect(self._update_state)
        self.combo_box_physical_domain.currentTextChanged.connect(self.check_analysis_setup_callback)
        self.combo_box_analysis_type.currentTextChanged.connect(self.check_analysis_setup_callback)
        #
        self.pushButton_run_analysis.clicked.connect(self.run_analysis)
        self.pushButton_configure_analysis.clicked.connect(self.configure_analysis)
        self.pushButton_reset_solution.clicked.connect(self.reset_solution)
        self.enable_pushbutons.connect(self.check_analysis_setup_callback)
        self.enable_pushbutons.connect(self.set_pushbutton_reset_solution_enabled)
    
    # def _update_state(self):
    #     app().main_window.update_symbols()

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

    def update_analysis_combo_boxes(self):

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

    def set_pushbutton_run_analysis_enabled(self, enable=True):
        self.pushButton_run_analysis.setEnabled(enable)

    def set_pushbutton_reset_solution_enabled(self):
        self.pushButton_reset_solution.setEnabled(True)

    def check_analysis_setup_callback(self):
        # I am guessing this commented function is useless
        # if no one complained yet feel free to remove completely
        # app().main_window.update_symbols()
        valid_setup = app().project.is_there_a_valid_analysis_setup()
        self.pushButton_run_analysis.setEnabled(valid_setup)
    
    def new_project_callback(self):
        self.setDisabled(False)
        self.set_pushbutton_run_analysis_enabled(False)
        self.update_analysis_combo_boxes()

    def run_analysis(self):
        self.update_analysis_combo_boxes()

        if not app().project.model.generated_mesh:
            obj = MeshSetupInputs(close_after_generate=True)
            if obj.complete:
                app().main_window.update_plots()
            else:
                return
        
        try:
            LoadTask(app().project.run_analysis).run()
        
        except ModelException as exception:
            app().main_window.action_model_workspace_callback()
            app().main_window.set_geometry_selection(
                points = exception.points,
                surfaces = exception.surfaces,
                volumes = exception.volumes,
            )
            ExceptionMessage(exception).exec()
        
        else:
            analysis = app().project.analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)
            app().main_window.disable_advanced_acoustic_plots_buttons(AnalysisID.is_modal(analysis))
            app().main_window.results_viewer_widget.results_viewer_items.update_items()
            app().main_window.configure_results_render_widget()

        self.set_pushbutton_reset_solution_enabled()

        # This is needed specially when the geometry
        # and mesh changes because of the analysis
        app().main_window.update_plots(reset_camera=False)

        if not app().project.file.read_geometry_data_from_file():
            app().project.file.write_geometry_data_in_file()

        if not app().project.file.read_mesh_data_from_file():
            app().project.file.write_mesh_data_in_file()

        app().project.file.write_model_properties_in_file()
        app().project.file.write_results_data_in_file()

    def reset_solution(self):
        app().project.reset_solutions()
        app().project.file.remove_results_data_from_project_file()
        app().main_window.action_model_workspace_callback()
        app().main_window.disable_advanced_acoustic_plots_buttons(True)
        self.pushButton_reset_solution.setDisabled(True)

    def configure_analysis(self):
        # aqui
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
        
    def harmonic_structural(self):

        select = StructuralHarmonicAnalysisMethodSelecorInput()
        if select.index == -1:
            return
 
        analysis_setup = {"analysis_id": select.index}
        self.update_analysis_setup(analysis_setup)
        harmonic = StructuralHarmonicAnalysisDirectMethodInput()

        if harmonic.setup_defined:
            self.final_actions()

        if harmonic.solve_analysis:
            self.run_analysis()
            app().main_window.update_symbols()

    def harmonic_acoustic(self):
        analysis_setup = {"analysis_id": AnalysisID.ACOUSTIC_HARMONIC}
        self.update_analysis_setup(analysis_setup)
        harmonic = AcousticHarmonicAnalysisDirectMethodInput()

        if harmonic.setup_defined:
            self.final_actions()

        if harmonic.solve_analysis:
            self.run_analysis()
    
    def modal_structural(self):
        modal = StructuralModalAnalysisInput()

        if modal.modes is None:
            return

        if modal.setup_defined:
            self.update_analysis_setup(modal.analysis_setup)
            self.final_actions()

        if modal.proceed_solution:
            self.run_analysis()

    def modal_acoustic(self):
        modal = AcousticModalAnalysisInput()

        if modal.modes is None:
            return

        if modal.setup_defined:
            self.update_analysis_setup(modal.analysis_setup)
            self.final_actions()

        if modal.proceed_solution:
            self.run_analysis()

    def update_analysis_setup(self, analysis_setup: dict):
        if app().project.analysis_setup is not None:
            for key, value in app().project.analysis_setup.items():
                if key in ["f_min", "f_max", "f_step", "frequencies", "global_damping"]:
                    analysis_setup[key] = value

        app().project.set_analysis_setup(analysis_setup)

    def final_actions(self):
        self.reset_solution()
        app().project.create_solver()
        app().project.file.write_analysis_setup_in_file(app().project.analysis_setup)