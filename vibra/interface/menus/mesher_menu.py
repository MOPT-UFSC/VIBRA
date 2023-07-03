from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QMenu

from vibra.interface.loading_bar import load_function
from vibra.utils.icons import load_icon
from interface.model.mesh.mesher_inputs import MesherInputs


class MesherMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Mesher")
        self.create_and_connect_actions()
        self.create_layout()


    def create_and_connect_actions(self):
        color = QColor("#0055DD")
        #
        self.new_project_icon = load_icon(Path("data/icons/new_file.png"), color)
        #
        self.mesher_setup_action = QAction(self.new_project_icon, "Mesher setup", self)
        self.generate_mesh_action = QAction(self.new_project_icon, "Generate mesh", self)
        self.mesher_setup_action.triggered.connect(self.call_mesher_inputs)
        self.generate_mesh_action.triggered.connect(self.call_generate_mesh)


    def create_layout(self):
        self.clear()
        self.addAction(self.mesher_setup_action)
        self.addAction(self.generate_mesh_action)


    def call_mesher_inputs(self):
        MesherInputs(self.parent())


    def call_generate_mesh(self):
        pass