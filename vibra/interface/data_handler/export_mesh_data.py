from PyQt5.QtWidgets import QCheckBox, QDialog, QFileDialog, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from vibra.interface.mesh.mesher_inputs import MesherInputs
from vibra.interface.general.print_message_input2 import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

from vibra.utils.interface_functions import get_main_window

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

class ExportMeshData(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/ui_files/data_handler/export_mesh.ui'), self)

        self.main_window = get_main_window()
        self.main_window.set_input_widget(self)
        
        self.project = self.main_window.project
        self.model = self.project.model
        self.mesh = self.project.model.mesh
        self.properties = self.model.properties

        if self.mesh is None:
            return
        else:
            self.main_window.viewer_tabs.show_mesh()

        self._load_icons()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.exec()

    def _load_icons(self):
        self.export_icon = QIcon(get_icons_path('save.png'))
        self.vibra_icon = QIcon(get_icons_path('logo_vibra.png'))
        self.search_icon = QIcon(get_icons_path('import.png'))
        self.clean_icon = QIcon(get_icons_path('broom.png'))
        self.setWindowIcon(self.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Export mesh data")

    def _reset_variables(self):
        self.folder_path = ""
        self.temp_path = os.path.expanduser('~')

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_nodal_coordinates = self.findChild(QCheckBox, 'checkBox_nodal_coordinates')
        self.checkBox_solid_elements_connectivity = self.findChild(QCheckBox, 'checkBox_solid_elements_connectivity')
        self.checkBox_face_elements_connectivity = self.findChild(QCheckBox, 'checkBox_face_elements_connectivity')
        self.checkBox_export_vtu_file = self.findChild(QCheckBox, 'checkBox_export_vtu_file')
        self.checkBox_nodal_coordinates.setChecked(True)
        self.checkBox_face_elements_connectivity.setChecked(True)
        self.checkBox_solid_elements_connectivity.setChecked(True)
        self.checkBox_export_vtu_file.setChecked(True)
        # QLineEdit
        self.lineEdit_folder_path = self.findChild(QLineEdit, 'lineEdit_folder_path')
        # QPushButton
        self.pushButton_export_mesh = self.findChild(QPushButton, 'pushButton_export_mesh')
        self.pushButton_search_folder = self.findChild(QPushButton, 'pushButton_search_folder')
        self.pushButton_export_mesh.setIcon(self.export_icon)
        self.pushButton_search_folder.setIcon(self.search_icon)
    
    def _create_connections(self):
        self.pushButton_export_mesh.clicked.connect(self.export_mesh_data)
        self.pushButton_search_folder.clicked.connect(self.search_folder)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.export_mesh_data()
        if event.key() == Qt.Key_Escape:
            self.close()

    def search_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(None, 'Choose a folder to export the mesh data', self.temp_path)
        self.lineEdit_folder_path.setText(str(self.folder_path))
        if self.folder_path == "":
            return True
        else:
            self.temp_path = self.folder_path
            return False

    def export_mesh_data(self):

        if self.generate_mesh():
            return

        if not os.path.exists(self.folder_path):
            if self.search_folder():
                return

        if self.checkBox_nodal_coordinates.isChecked():
            _path = Path(f"{self.folder_path}/nodal_coordinates.dat")
            self.mesh.export_nodal_coordinates(_path)

        if self.checkBox_face_elements_connectivity.isChecked():
            _path = Path(f"{self.folder_path}/face_elements_connectivity.dat")
            self.mesh.export_face_elements_connectivity(_path)
        
        if self.checkBox_solid_elements_connectivity.isChecked():
            _path = Path(f"{self.folder_path}/solid_elements_connectivity.dat")
            self.mesh.export_solid_elements_connectivity(_path)

        if self.checkBox_export_vtu_file.isChecked():
            _path = Path(f"{self.folder_path}/mesh_data.vtu")
            self.mesh.export_vtu_file(_path)

        if self.check_data_to_export():
            self.close()
            title = "Exporting mesh data"
            message = "The selected mesh data has been exported."
            window_title = "Information"
            PrintMessageInput([window_title, title, message], auto_close=True)
        else:
            return

    def generate_mesh(self):
        if not self.main_window.project.model.generated_mesh:
            self.mesher = MesherInputs(close_after_generate=True)
            if not self.mesher.complete:
                self.mesher = None
                return True
            
    def check_data_to_export(self):
        if self.checkBox_nodal_coordinates.isChecked():
            return True
        elif self.checkBox_face_elements_connectivity.isChecked():
            return True
        elif self.checkBox_solid_elements_connectivity.isChecked():
            return True
        elif self.checkBox_export_vtu_file.isChecked():
            return True
        else:
            title = "Empty mesh data selection"
            message = "Select a mesh data to proceed with the data exportation."
            window_title = "Warning"
            PrintMessageInput([window_title, title, message], auto_close=False)
            return False