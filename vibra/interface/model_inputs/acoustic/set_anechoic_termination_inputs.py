import configparser
import os
from pathlib import Path

import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from vibra import UI_DIR
from vibra.interface.general.call_double_confirmation_input import CallDoubleConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.interface_functions import get_main_window

window_title_1 = "ERROR"
window_title_2 = "WARNING"


class SetAnechoicTerminationInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/acoustic/set_anechoic_termination_input.ui"
        uic.loadUi(ui_path, self)

        icon_path = str(Path("data/icons/logo_vibra.png"))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set anechoic termination")

        self.main_window = get_main_window()
        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()
        self.project = self.main_window.project
        self.model = self.project.model
        self.properties = self.model.properties

        self._reset()
        self._define_qt_variables()
        self._create_connections()
        self.load_info()
        self.exec()

    def _reset(self):
        self.typed_ids = []
        self.remove_anechoic_termination = False
        self.anechoic_termination = None
        self.userPath = os.path.expanduser("~")
        self.new_load_path_table = ""
        self.project_path = self.project.file.project_path
        self.acoustic_bc_filename = self.project.file.acoustic_model_setup_filename
        self.acoustic_bc_info_path = os.path.join(self.project_path, self.acoustic_bc_filename)
        self.acoustic_folder_path = self.project.file.acoustic_imported_data_folder_path
        self.anechoic_termination_tables_folder_path = os.path.join(self.acoustic_folder_path, "anechoic_termination_files")

    def _define_qt_variables(self):
        
        # QComboBox
        self.comboBox_volume_id : QComboBox
        
        # QLineEdit
        self.lineEdit_selection_id : QLineEdit
        
        # QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_remove_bc_confirm : QPushButton
        self.pushButton_reset : QPushButton

        # QTabWidget
        self.tabWidget_anechoic_termination : QTabWidget
        
        # QTreeWidget
        self.treeWidget_anechoic_termination = self.findChild(QTreeWidget, "treeWidget_anechoic_termination")
        self.treeWidget_anechoic_termination.setColumnWidth(1, 20)
        self.treeWidget_anechoic_termination.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.pushButton_confirm.clicked.connect(self.confirm_button_pressed)
        self.pushButton_remove_bc_confirm.clicked.connect(self.remove_bc_from_selection)
        self.pushButton_reset.clicked.connect(self.check_reset)
        #
        self.tabWidget_anechoic_termination.currentChanged.connect(self.tabEvent_callback)
        self.treeWidget_anechoic_termination.itemClicked.connect(self.on_click_item)
        self.treeWidget_anechoic_termination.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)

    def tabEvent_callback(self):
        current_tab = self.tabWidget_anechoic_termination.currentIndex()
        if current_tab == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)

    def on_click_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))
        self.remove_bc_from_selection()

    def load_info(self):
        self.treeWidget_anechoic_termination.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "specific_impedance":
                if "anechoic_termination" in data.keys():
                    volume_id = data["volume_id"]
                    new = QTreeWidgetItem([str(surface_id), str(volume_id)])
                    new.setTextAlignment(0, Qt.AlignCenter)
                    new.setTextAlignment(1, Qt.AlignCenter)
                    self.treeWidget_anechoic_termination.addTopLevelItem(new)
        self.update_tabs_visibility()

    def geometry_selection_callback(self, points, lines, faces):
        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.update_volumes_from_faces()

        elif not any([points, lines, faces]):
            self.lineEdit_selection_id.setText("")       

    def update_volumes_from_faces(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.typed_ids = self.model.check_input_surface_id(lineEdit_selection_id)

        list_volumes = list()
        for face_id in self.typed_ids:            
            for volume_id in self.model.mesh.volume_from_surface[face_id]:
                if volume_id not in list_volumes:
                    list_volumes.append(volume_id)

        self.comboBox_volume_id.clear()
        for vol_id in list_volumes:
            self.comboBox_volume_id.addItem(str(vol_id))
        
        if len(list_volumes) == 1:
            self.comboBox_volume_id.setDisabled(True)
        else:
            if len(self.typed_ids) == 1:
                self.comboBox_volume_id.setDisabled(False)
            else:
                self.comboBox_volume_id.clear()
                self.comboBox_volume_id.addItem("multiple")

    def confirm_button_pressed(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.typed_ids = self.model.check_input_surface_id(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return

        for face_id in self.typed_ids:
            volume_ids = self.model.mesh.volume_from_surface[self.typed_ids[0]]
            if len(volume_ids) > 1:
                title = "Undefined volume"
                message = f"The selected face ID [{face_id}] is associated to the volumes {volume_ids}. "
                message += "The multiple selection of faces related to more than one volume is not allowed. "
                message += "In this case, it is necessary to select the Face ID and the respective Volume ID "
                message += "to proceed."
                PrintMessageInput([window_title_2, title, message])
                return 

        volume_id = int(self.comboBox_volume_id.currentText())

        data = {"anechoic_termination" : True,
                "volume_id" : volume_id,
                "nodal_attribution": False}

        for face_id in self.typed_ids:
            self.project.set_specific_impedance(data, face_id)

        self.properties.export_model_properties()

        print(f"[Set anechoic termination] - defined at surface(s) {self.typed_ids}")
        self.close()

    def lineEdit_reset(self, lineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def get_list_table_names_from_selected_surfaces(self, list_ids):
        list_table_names = []
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "specific_impedance":
                if surface_id in list_ids:
                    if "table_name" in data.keys():
                        list_table_names.append(data["table_name"])
        return list_table_names

    def remove_bc_from_selection(self):
        if self.lineEdit_selection_id.text() != "":
            surface_properties = self.properties.surface_properties.copy()
            picked_id = int(self.lineEdit_selection_id.text())
            for key, data in surface_properties.items():
                property, surface_id = key
                if property == "specific_impedance" and picked_id == surface_id:
                    if "anechoic_termination" in data.keys():
                        self.properties._remove_surface_property("specific_impedance", picked_id)
                        self.load_info()
                        self.lineEdit_selection_id.setText("")
                        return

    def check_reset(self):
        surface_ids = []
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "specific_impedance":
                if "anechoic_termination" in data.keys():
                    surface_ids.append(surface_id)

        if len(surface_ids) > 0:
            
            title = f"Resetting of all applied specific impedances"
            message = "Would you like to remove the all anechoic terminations from the model?"

            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

            if read._doNotRun:
                return

            if read._continue:
                for face_id in surface_ids:
                    self.properties._remove_surface_property("specific_impedance", face_id)

                self.properties.export_model_properties()
                self.close()

    def update(self):
        return

    def write_ids(self, list_ids):

        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)

        current_tab = self.tabWidget_anechoic_termination.currentIndex()
        if current_tab != 2:
            self.lineEdit_selection_id.setText(text[:-2])

    def update_tabs_visibility(self):
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "specific_impedance":
                if "anechoic_termination" in data.keys():
                    self.tabWidget_anechoic_termination.setTabVisible(1, True)
                    return

        self.tabWidget_anechoic_termination.setTabVisible(1, False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_anechoic_termination.currentIndex() == 0:
                self.confirm_button_pressed()
            if self.tabWidget_anechoic_termination.currentIndex() == 1:
                self.check_table_values()
        elif event.key() == Qt.Key_Delete:
            if self.tabWidget_anechoic_termination.currentIndex() == 2:
                self.remove_bc_from_selection()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            return
