from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QWidget,
)

from vibra import app


class AnalysisFilter(QWidget):
    def __init__(self):
        super().__init__()

        self.initialize()

        grid_main = QHBoxLayout()
        grid_main.addWidget(self.spacing_frame_left)
        grid_main.addWidget(self.label_main)
        grid_main.addWidget(self.comboBox_analysis_selector)
        grid_main.addWidget(self.spacing_frame_right)
        grid_main.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(grid_main)
        self.setMinimumWidth(300)
        self.setMaximumWidth(360)
        self.setFixedHeight(70)

    def initialize(self):
        """
        """
        # self.frame = QFrame()
        # self.frame.setLineWidth(1)
        # self.frame.setFrameShape(QFrame.Box)
        #
        self.spacing_frame_left = QFrame()
        # self.spacing_frame_left.setLineWidth(1)
        # self.spacing_frame_left.setFrameShape(QFrame.Box)
        self.spacing_frame_right = QFrame()
        # self.spacing_frame_right.setLineWidth(1)
        # self.spacing_frame_right.setFrameShape(QFrame.Box)

        self.label_main = QLabel("Analysis type:", self)
        self.label_main.setMinimumSize(QSize(40, 30))
        self.label_main.setMaximumSize(QSize(150, 30))
        self.label_main.setStyleSheet("font: 11pt")
        self.label_main.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # self.label_main.setFrameShape(QFrame.Box)

        self.comboBox_analysis_selector = QComboBox(self)
        labels = [" Acoustic", " Structural", " Coupled"]
        for label in labels:
            self.comboBox_analysis_selector.addItem(label)

        self.comboBox_analysis_selector.setFixedHeight(30)
        self.comboBox_analysis_selector.setFixedWidth(110)
        self.comboBox_analysis_selector.setStyleSheet("""   QComboBox{border-radius: 4px; border-style: ridge; border-width: 2px; font: 10pt "MS Shell Dlg 2"}
                                                            QComboBox:hover{border-radius: 4px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; background-color: rgba(174, 213, 255, 100); font: 10pt "MS Shell Dlg 2"}
                                                            QComboBox:disabled{border-radius: 4px; border-style: ridge; border-width: 2px; font: 10pt "MS Shell Dlg 2"}   """)
        #
        self.comboBox_analysis_selector.currentIndexChanged.connect(app().main_window.menu_widget.filter_analysis_type)