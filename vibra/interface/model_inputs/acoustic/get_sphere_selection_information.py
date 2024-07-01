
# fmt: off
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton

from vibra import app, UI_DIR
from vibra.interface.general.print_message_input import PrintMessageInput

import numpy as np
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"

class GetSphereSelectionInformation(QDialog):
    def __init__(self, selection_id, selection_radius, averaged, filter_type, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/get_sphere_selection_information.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.main_window.viewer_tabs.show_mesh()
        self.main_window.set_input_widget(self)

        self.project = self.main_window.project
        self.model = self.main_window.project.model
        self.properties = self.model.properties

        self.selection_id = selection_id
        self.selection_radius = selection_radius
        self.averaged = averaged
        self.filter_type = filter_type

        self._config_window()
        self._define_qt_variables()
        self._config_widgets()
        self.get_selection_info()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.main_window.vibra_icon)
        self.setWindowTitle("Get sphere selection information")

    def _define_qt_variables(self):

        # QLineEdit
        self.lineEdit_coordinate_x : QLineEdit
        self.lineEdit_coordinate_y : QLineEdit
        self.lineEdit_coordinate_z : QLineEdit
        self.lineEdit_number_of_elements : QLineEdit
        self.lineEdit_number_of_nodes : QLineEdit
        self.lineEdit_selection_radius : QLineEdit

    def _config_widgets(self):
        self.lineEdit_number_of_elements.setDisabled(True)
        self.lineEdit_number_of_nodes.setDisabled(True)
        self.lineEdit_selection_radius.setDisabled(True)
        self.lineEdit_selection_radius.setText(str(round(self.selection_radius, 6)))

    def get_selection_info(self):

        list_elements, list_nodes = self.model.get_elements_and_nodes_from_sphere(  self.selection_id, 
                                                                                    self.selection_radius, 
                                                                                    averaged = self.averaged,
                                                                                    filter_type = self.filter_type)

        list_center_coords = self.model.get_average_nodal_coordinates(  self.selection_id,
                                                                        averaged=self.averaged  )

        if len(list_center_coords) == 0:
            self.lineEdit_coordinate_x.setText("")
            self.lineEdit_coordinate_y.setText("")
            self.lineEdit_coordinate_z.setText("")

        elif len(list_center_coords) == 1:
            _round_center_coords = [round(value, 4) for value in list_center_coords[0]]
            self.lineEdit_coordinate_x.setText(str(_round_center_coords[0]))
            self.lineEdit_coordinate_y.setText(str(_round_center_coords[1]))
            self.lineEdit_coordinate_z.setText(str(_round_center_coords[2]))

        else:
            self.lineEdit_coordinate_x.setText("Multiple centers")
            self.lineEdit_coordinate_y.setText("Multiple centers")
            self.lineEdit_coordinate_z.setText("Multiple centers")

        self.lineEdit_number_of_elements.setText(str(len(list_elements)))
        self.lineEdit_number_of_nodes.setText(str(len(list_nodes)))

        self.highlight_mesh_elements(list_elements)

    def highlight_mesh_elements(self, elements):
        mesh_widget = self.main_window.viewer_tabs.mesh_widget
        mesh_widget.select_multiple_volumes(elements)