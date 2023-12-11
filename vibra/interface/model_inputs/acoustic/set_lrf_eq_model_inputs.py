import os
import configparser
import numpy as np
from pathlib import Path

# fmt: off
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from vibra.interface.general.call_double_confirmation_input import CallDoubleConfirmationInput

from vibra.interface.model_inputs.acoustic.get_sphere_selection_information import GetSphereSelectionInformation
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.interface_functions import get_main_window

window_title_1 = "ERROR"
window_title_2 = "WARNING"


class LowReducedFrequencyEquivalentModelInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path("data/ui_files/model/acoustic/lrf_eq_model_inputs.ui"), self)

        icon_path = str(Path("data/icons/logo_vibra.png"))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set the low reduced frequency eq. model")

        self.main_window = get_main_window()
        self.main_window.set_input_widget(self)
        self.project = self.main_window.project
        self.model = self.main_window.project.model
        self.properties = self.model.properties
        
        self.main_window.viewer_tabs.show_geometry()

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.load_lrf_data()
        self.exec()

    def _reset_variables(self):
        self.typed_ids = []
        # self.model = ""
        self.speed_of_sound_factor = 0
        self.fluid_density_factor = 0

    def _define_qt_variables(self):
        # QComboBox objects
        self.comboBox_selection_type = self.findChild(QComboBox, 'comboBox_selection_type')
        # QFrame objects
        self.frame_selection_by_surface = self.findChild(QFrame, 'frame_selection_by_surface')
        self.frame_center_coordinates = self.findChild(QFrame, "frame_center_coordinates")
        # QLineEdit objects
        self.lineEdit_center_coordinates = self.findChild(QLineEdit, 'lineEdit_center_coordinates')
        self.lineEdit_selection_id = self.findChild(QLineEdit, "lineEdit_selection_id")
        self.lineEdit_diameter = self.findChild(QLineEdit, "lineEdit_diameter")
        self.lineEdit_selection_radius = self.findChild(QLineEdit, "lineEdit_selection_radius")
        self.lineEdit_selection_radius.setDisabled(True)
        # QPushButton objects
        self.pushButton_confirm = self.findChild(QPushButton, "pushButton_confirm")
        self.pushButton_selection_info = self.findChild(QPushButton, "pushButton_selection_info")
        self.pushButton_remove = self.findChild(QPushButton, "pushButton_remove")
        self.pushButton_reset = self.findChild(QPushButton, "pushButton_reset")
        # QTabWidget objects
        self.tabWidget_lrf_model = self.findChild(QTabWidget, "tabWidget_lrf_model")
        self.tab_setup = self.tabWidget_lrf_model.findChild(QWidget, "tab_setup")
        self.current_tab = self.tabWidget_lrf_model.currentIndex()
        # QTreeWidget objects
        self.treeWidget_lrf_model_info = self.findChild(QTreeWidget, "treeWidget_lrf_model_info")

    def _create_connections(self):
        #
        self.comboBox_selection_type.currentIndexChanged.connect(self.update_controls_visibility)
        #
        self.pushButton_confirm.clicked.connect(self.set_lrf_eq_model_data)
        self.pushButton_selection_info.clicked.connect(self.get_selection_information)
        self.pushButton_remove.clicked.connect(self.remove_lrf_eq_model_inputs)
        self.pushButton_reset.clicked.connect(self.reset_lrf_eq_model_inputs)
        #
        self.treeWidget_lrf_model_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_lrf_model_info.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)
        self.update_controls_visibility()

    def update_controls_visibility(self):
        index = self.comboBox_selection_type.currentIndex()
        if index == 0:
            self.frame_center_coordinates.setVisible(False)
            self.frame_selection_by_surface.setVisible(False)
        else:
            self.frame_center_coordinates.setVisible(True)
            self.frame_selection_by_surface.setVisible(True)

    def geometry_selection_callback(self, points, lines, faces, volumes):
        self.lineEdit_selection_radius.setDisabled(True)
        self.pushButton_selection_info.setDisabled(True)
        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_selection_type.setCurrentIndex(1)
            self.lineEdit_selection_radius.setDisabled(False)
            self.pushButton_selection_info.setDisabled(False)
            # self.get_center_coordinates()
            self.call_sphere_plotter()
        elif volumes:
            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_selection_type.setCurrentIndex(0)
            self.hide_sphere()
        elif not any([points, lines, faces]):
            self.lineEdit_selection_id.setText("")
            self.lineEdit_center_coordinates.setText("")
            self.hide_sphere()

    def get_center_coordinates(self):
        selection_id = self.lineEdit_selection_id.text()
        if selection_id == "":
            self.lineEdit_center_coordinates.setText("")
            return []
        center_coords = self.model.get_average_nodal_coordinates(selection_id)
        if None in center_coords:
            self.lineEdit_center_coordinates.setText("")
            return []
        _round_center_coords = [round(value,4) for value in center_coords]
        self.lineEdit_center_coordinates.setText(str(_round_center_coords))
        return center_coords

    def call_sphere_plotter(self):
        if self.comboBox_selection_type.currentIndex() == 1:
            if self.check_selection_radius():
                return
            center_coords = self.get_center_coordinates()
            if len(center_coords):
                geometry_widget = self.main_window.viewer_tabs.geometry_widget
                geometry_widget.set_selection_sphere(center_coords, self.selection_radius)    

    def hide_sphere(self):
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.set_selection_sphere((0,0,0), 0)

    def get_selection_information(self):
        selection_id = self.lineEdit_selection_id.text()
        if selection_id != "":
            if self.comboBox_selection_type.currentIndex() == 1:
                if self.check_selection_radius():
                    return
                GetSphereSelectionInformation(selection_id, self.selection_radius)

    def remove_lrf_eq_model_inputs(self):
        self.remove_lrf_eq_from_selection()

    def reset_lrf_eq_model_inputs(self):
        self.check_reset()

    def load_lrf_data(self):
        self.treeWidget_lrf_model_info.clear()
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "lrf_eq_model":
                diameter = data["diameter"]
                new = QTreeWidgetItem([str(volume_id), "volume", str(diameter)])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_lrf_model_info.addTopLevelItem(new)
        for key, data in self.properties.group_properties.items():
            property, group_id = key
            if property == "lrf_eq_model":
                diameter = data["diameter"]
                new = QTreeWidgetItem([str(group_id), "group", str(diameter)])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_lrf_model_info.addTopLevelItem(new)
        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        group_ids = []
        for key in self.properties.group_properties.keys():
            property, group_id = key
            if property == "lrf_eq_model":
                group_ids.append(group_id)

        volume_ids = []
        for key in self.properties.volume_properties.keys():
            property, volume_id = key
            if property == "lrf_eq_model":
                volume_ids.append(volume_id)

        if len(group_ids) + len(volume_ids):
            self.tabWidget_lrf_model.setTabVisible(1, True)
        else:
            self.tabWidget_lrf_model.setTabVisible(1, False)
    
    def highlight_mesh_elements(self, elements):
        mesh_widget = self.main_window.viewer_tabs.mesh_widget
        mesh_widget.select_multiple_volumes(elements)

    def check_lrf_eq_model_entries(self):
        
        selection_id = self.lineEdit_selection_id.text()
        if self.comboBox_selection_type.currentIndex() == 0:
            self.stop, self.volume_ids = self.model.check_input_volume_id(selection_id)
        else:
            self.stop, self.surface_ids = self.model.check_input_surface_id(selection_id)
            lineEdit = self.lineEdit_selection_radius
            self.selection_radius = self.check_inputs(lineEdit, "Selection radius")
            if self.stop:
                lineEdit.setFocus()
                return True

        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return True

        lineEdit = self.lineEdit_diameter
        self.diameter = self.check_inputs(lineEdit, "Diameter")
        if self.stop:
            lineEdit.setFocus()
            return True

    def set_lrf_eq_model_data(self):
        
        if self.check_lrf_eq_model_entries():
            return
        
        index = self.comboBox_selection_type.currentIndex()
        if index == 0:

            data = {"diameter" : self.diameter}
            for _id in self.volume_ids:
                self.project.set_lrf_eq_model_data(data, volume=_id)

        else:

            group_id = self.get_lrf_group_index()
            print(f"group_id: {group_id}")
            data = {"surface_ids" : np.array(self.surface_ids),
                    "diameter" : self.diameter,
                    "selection_radius" : self.selection_radius}

            for _id in self.surface_ids:
                self.project.set_lrf_eq_model_data(data, group=group_id)

        self.close()

    def get_lrf_group_index(self):
        keys = []
        for key in self.properties.group_properties.keys():
            property, group_id = key
            if property == "lrf_eq_model":
                if group_id not in keys:
                    keys.append(group_id)
        index = 1
        while index in keys:
            index += 1
        return index

    def check_inputs(self, lineEdit, label, only_positive=True, zero_included=False, _float=True):
        self.stop = False
        message = ""
        title = "Invalid input to the analysis setup"
        window_title = "ERROR"
        if lineEdit.text() != "":
            try:
                if _float:
                    out = float(lineEdit.text())
                else:
                    out = int(lineEdit.text())

                if only_positive:
                    if zero_included:
                        if out < 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is allowed."
                    else:
                        if out <= 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is not allowed."

            except Exception as _err:
                message = "Dear user, you have typed and invalid value at the \n"
                message += f"{label} input field.\n\n"
                message += str(_err)

        else:
            if zero_included:
                return float(0)
            else:
                message = f"Insert some value at the {label} input field."

        if message != "":
            PrintMessageInput([title, message, window_title])
            self.stop = True
            return None
        return out

    def on_click_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))
        self.remove_lrf_eq_from_selection()

    def remove_lrf_eq_from_selection(self):

        if self.lineEdit_selection_id.text() != "":

            picked_id = int(self.lineEdit_selection_id.text())
            surface_properties = self.properties.surface_properties.copy()
            volume_properties = self.properties.volume_properties.copy()
            
            for key in surface_properties.keys():
                property, surface_id = key
                if property == "lrf_eq_model" and picked_id == surface_id:
                    self.properties._remove_surface_property("lrf_eq_model", picked_id)
                    self.load_lrf_data()
                    self.lineEdit_selection_id.setText("")
                    return
                
            for key in volume_properties.keys():
                property, volume_id = key
                if property == "lrf_eq_model" and picked_id == volume_id:
                    self.properties._remove_volume_property("lrf_eq_model", picked_id)
                    self.load_lrf_data()
                    self.lineEdit_selection_id.setText("")
                    return

    def check_reset(self):

        surface_ids = []
        for key in self.properties.surface_properties.keys():
            property, surface_id = key
            if property == "lrf_eq_model":
                surface_ids.append(surface_id)

        volume_ids = []
        for key in self.properties.volume_properties.keys():
            property, volume_id = key
            if property == "lrf_eq_model":
                volume_ids.append(volume_id)

        if len(surface_ids) + len(volume_ids):
            title = f"Resetting LRF eq. model"
            message = "Do you really want to remove the LRF eq. defined to the model?\n\n"
            message += "\n\nPress the Continue button to proceed with the resetting or press Cancel or "
            message += "Close buttons to abort the current operation."
            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

            if read._doNotRun:
                return

            if read._continue:

                if len(surface_ids) + len(volume_ids) > 0:
                    self.properties._reset_property("lrf_eq_model")

                self.properties.export_model_properties()

                title = "surface velocity resetting process complete"
                message = "All surface velocity applied to the acoustic "
                message += "model have been removed from the model."
                PrintMessageInput([title, message, window_title_2])

                self.close()
    
    def closeEvent(self, event):
        self.hide_sphere()
        try:
            geometry_widget = self.main_window.viewer_tabs.geometry_widget
            geometry_widget.selection_changed.disconnect(self.geometry_selection_callback)
        except TypeError:
            pass  # ignore if there is nothing to disconect

# fmt: on