from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QWidget

from vibra import app


class MeshInfoBar(QWidget):
    def __init__(self):
        super().__init__()

        self.project = app().project
        self.mesh = self.project.model.mesh

        if self.mesh is None:
            return

        self.number_of_nodes = len(self.mesh.nodal_coordinates)
        self.number_of_elements = len(self.mesh.solids_connectivity)

        self._define_qt_variables()

    def _define_qt_variables(self):
        #
        self.frame_spacer = QFrame()
        #
        self.label_number_of_nodes = QLabel(f"Number of nodes: {self.number_of_nodes}")
        self.label_number_of_elements = QLabel(f"Number of elements: {self.number_of_elements}")
        #
        analysis_info_layout = QGridLayout()
        layout = QHBoxLayout()
        #
        self._config_widgets()
        #
        analysis_info_layout.addWidget(self.frame_spacer, 0, 0)
        analysis_info_layout.addWidget(self.label_number_of_nodes, 0, 1)
        analysis_info_layout.addWidget(self.label_number_of_elements, 0, 2)
        #
        layout.addLayout(analysis_info_layout)
        self.setLayout(layout)
        self.setContentsMargins(2, 0, 2, 0)
        self.setStyleSheet("border: 1px solid")
        layout.setContentsMargins(0, 0, 0, 0)
        analysis_info_layout.setContentsMargins(0, 0, 0, 0)

    def _config_widgets(self):
        height = 28

        self.frame_spacer.setMinimumHeight(height)
        self.frame_spacer.setMaximumHeight(height)

        # self.label_number_of_nodes.setAlignment(Qt.AlignRight)
        self.label_number_of_nodes.setMinimumSize(100, height)
        self.label_number_of_nodes.setMaximumSize(200, height)

        # self.label_number_of_elements.setAlignment(Qt.AlignRight)
        self.label_number_of_elements.setMinimumSize(100, height)
        self.label_number_of_elements.setMaximumSize(200, height)
