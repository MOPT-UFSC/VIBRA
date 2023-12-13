import numpy as np
from pathlib import Path

# fmt: off
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget

from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.interface_functions import get_main_window

window_title_1 = "ERROR"
window_title_2 = "WARNING"

class GetSphereSelectionInformation(QDialog):
    def __init__(self, selection_id, selection_radius, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path("data/ui_files/model/acoustic/get_sphere_selection_information.ui"), self)

        icon_path = str(Path("data/icons/logo_vibra.png"))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Get sphere selection information")

        self.main_window = get_main_window()
        # self.main_window.set_input_widget(self)
        self.project = self.main_window.project
        self.model = self.main_window.project.model
        self.properties = self.model.properties

        self.selection_id = selection_id
        self.selection_radius = selection_radius
        self.lineEdit_selection_radius.setText(str(self.selection_radius))

        self._define_qt_variables()
        self._create_connections()
        self.get_selection_info()
        self.exec()

    def _define_qt_variables(self):
        # QLineEdit objects
        self.lineEdit_center_coordinates = self.findChild(QLineEdit, 'lineEdit_center_coordinates')
        self.lineEdit_number_of_elements = self.findChild(QLineEdit, 'lineEdit_number_of_elements')
        self.lineEdit_number_of_nodes = self.findChild(QLineEdit, 'lineEdit_number_of_nodes')
        self.lineEdit_selection_radius = self.findChild(QLineEdit, 'lineEdit_selection_radius')
        self.lineEdit_number_of_elements.setDisabled(True)
        self.lineEdit_number_of_nodes.setDisabled(True)
        self.lineEdit_selection_radius.setDisabled(True)
        # QPushButton objects
        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
    
    def _create_connections(self):
        self.pushButton_close.clicked.connect(self.close)

    def get_selection_info(self):
        list_elements, list_nodes = self.model.get_elements_and_nodes_from_sphere(self.selection_id, self.selection_radius)
        center_coords = self.model.get_average_nodal_coordinates(self.selection_id)
        if None in center_coords:
            self.lineEdit_center_coordinates.setText("")
        else:
            _round_center_coords = [round(value,4) for value in center_coords]
            self.lineEdit_center_coordinates.setText(str(_round_center_coords))

        self.lineEdit_number_of_elements.setText(str(len(list_elements)))
        self.lineEdit_number_of_nodes.setText(str(len(list_nodes)))
        self.highlight_mesh_elements(list_elements)

    def highlight_mesh_elements(self, elements):
        mesh_widget = self.main_window.viewer_tabs.mesh_widget
        # _elements = list(np.random.randint(0, 1000, 800))
        mesh_widget.select_multiple_volumes(elements)