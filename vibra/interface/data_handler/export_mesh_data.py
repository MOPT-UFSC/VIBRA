from PySide6.QtWidgets import QFileDialog, QPushButton
from PySide6.QtCore import Qt

from vibra import app
from vibra.interface.ui_generated.data_handler.export_mesh_ui import ExportMesh_UI
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.common.common_interface import mesher_interface_callback

import os
from pathlib import Path


class ExportMeshData(ExportMesh_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = self.model.properties

        if self.mesh is None:
            return
        else:
            app().main_window.action_mesh_workspace_callback()

        self._configure_window()
        self._reset_variables()
        self._create_connections()
        self.exec()

    def _configure_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

        self.checkBox_nodal_coordinates.setChecked(True)
        self.checkBox_face_elements_connectivity.setChecked(True)
        self.checkBox_solid_elements_connectivity.setChecked(True)
        self.checkBox_export_vtu_file.setChecked(True)

    def _reset_variables(self):
        self.folder_path = ""
        self.temp_path = os.path.expanduser('~')
    
    def _create_connections(self):
        self.pushButton_export_mesh.clicked.connect(self.export_mesh_data)
        self.pushButton_search_folder.clicked.connect(self.search_folder)

    def search_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(None, 'Choose a folder to export the mesh data', str(self.temp_path))
        self.lineEdit_folder_path.setText(str(self.folder_path))
        if self.folder_path == "":
            return True
        else:
            self.temp_path = self.folder_path
            return False

    def export_mesh_data(self):

        if mesher_interface_callback(self, close_after_generate=True):
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
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.export_mesh_data()
        if event.key() == Qt.Key_Escape:
            self.close()