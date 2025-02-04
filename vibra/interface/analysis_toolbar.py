from PyQt5.QtWidgets import QToolBar, QComboBox, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from vibra.interface.analysis.acoustic_harmonic_analysis_input import AcousticHarmonicAnalysisInput
from vibra.interface.analysis.acoustic_modal_analysis_input import AcousticModalAnalysisInput
from vibra.interface.analysis.structural_harmonic_analysis_input import StructuralHarmonicAnalysisInput
from vibra.interface.analysis.structural_modal_analysis_input import StructuralModalAnalysisInput
from vibra.interface.analysis.analysis_type_input import AnalysisTypeInput

from vibra import ICON_DIR, app


class AnalysisToolbar(QToolBar):
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
    
    def _create_connections(self):
        self.pushButton_run_analysis.clicked.connect(self.run_analysis)
        self.pushButton_configure_analysis.clicked.connect(self.configure_analysis)

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
    
    def _load_analysis_types(self):
        self.combo_box_analysis_type.addItem("Harmonic")
        self.combo_box_analysis_type.addItem("Modal")

        self.combo_box_analysis_domain.addItem("Structural")
        self.combo_box_analysis_domain.addItem("Acoustic")
    
    def run_analysis(self):
        ...

    def configure_analysis(self):
        analysis_type = self.combo_box_analysis_type.currentText()
        physical_domain = self.combo_box_analysis_domain.currentText()

        if analysis_type == "Harmonic":
            if physical_domain == "Structural":
                self.harmonic_structural()
            elif physical_domain == "Acoustic":
                self.harmonic_acoustic()
    
    def harmonic_structural(self):
        select = StructuralHarmonicAnalysisInput()
        if select.index == -1:
            return

        method_id = select.index

        if method_id == 0:
            analysis_id = 0
        else:
            analysis_id = 1
        
        return

        app().project.set_analysis_id(analysis_id)

        app().project.reset_solution()
        if app().main_window.input_ui.analysis_setup():
            self.update_run_analysis_button()
    
    def harmonic_acoustic(self):
        ...

