from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QMenu

from vibra.interface.loading_bar import load_function
from vibra.interface.model_inputs.mesh.mesher_inputs import MesherInputs
from vibra.interface.model_inputs.structural.material_inputs import (
    MaterialInput,
)
from vibra.utils.icons import load_icon
from vibra.utils.interface_functions import get_main_window


class MesherMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = get_main_window()
        self.setTitle("Model setup")
        self.setObjectName("model_setup_menu")
        self.create_and_connect_actions()
        self.create_layout()

    def create_and_connect_actions(self):
        color = QColor("#0055DD")
        #
        self.new_project_icon = load_icon(Path("data/icons/new_file.png"), color)
        #
        self.set_fluid_action = QAction(self.new_project_icon, "Set fluid", self)
        self.set_material_action = QAction(self.new_project_icon, "Set material", self)
        self.mesher_setup_action = QAction(self.new_project_icon, "Mesher setup", self)
        self.generate_mesh_action = QAction(self.new_project_icon, "Generate mesh", self)
        self.generate_mesh_action.setObjectName("generate_mesh_action")
        #
        self.set_fluid_action.triggered.connect(self.call_fluid_configurator)
        self.set_material_action.triggered.connect(self.call_material_configurator)
        self.mesher_setup_action.triggered.connect(self.call_mesher_inputs)
        self.generate_mesh_action.triggered.connect(self.call_generate_mesh)
        self.generate_mesh_action.setDisabled(True)

    def create_layout(self):
        self.clear()
        self.addAction(self.set_fluid_action)
        self.addAction(self.set_material_action)
        self.addAction(self.mesher_setup_action)
        self.addAction(self.generate_mesh_action)

    def call_fluid_configurator(self):
        pass

    def call_material_configurator(self):
        MaterialInput()
        pass

    def call_mesher_inputs(self):
        mesher = MesherInputs()
        if mesher.complete:
            self.parent().project.set_mesh_setup(mesher.mesh_setup)
            self.generate_mesh_action.setDisabled(False)
            self.main_window.menu_widget.item_child_generate_mesh.setDisabled(False)

    def call_generate_mesh(self):
        generate_mesh = load_function(self.main_window.project.generate_mesh, self.main_window)
        generate_mesh()
        self.main_window.viewer_tabs.show_mesh()
        self.main_window.viewer_tabs.update_plots()
