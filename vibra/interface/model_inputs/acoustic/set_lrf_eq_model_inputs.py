import numpy as np
from pathlib import Path

# fmt: off
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget

from vibra import UI_DIR
from vibra.interface.model_inputs.acoustic.get_sphere_selection_information import GetSphereSelectionInformation
from vibra.interface.mesh.mesher_inputs import MesherInputs
#
from vibra.interface.general.call_double_confirmation_input import CallDoubleConfirmationInput
from vibra.interface.general.print_message_input2 import PrintMessageInput
# from vibra.interface.exception_message import ErrorMessage
# from vibra.errors import IncompleteMeshSetup, IncompleteSetupError

from vibra.interface.loading_bar import load_function
from vibra.utils.interface_functions import get_main_window

window_title_1 = "Error"
window_title_2 = "Warning"


class LowReducedFrequencyEquivalentModelInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/acoustic/lrf_eq_model_inputs.ui"
        uic.loadUi(ui_path, self)

        icon_path = str(Path("data/icons/logo_vibra.png"))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set the low reduced frequency eq. model")

        self.main_window = get_main_window()
        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()
        
        self.project = self.main_window.project
        self.model = self.main_window.project.model
        self.properties = self.model.properties

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.load_lrf_data()
        self.exec()

    def _reset_variables(self):
        self.typed_ids = []
        # self.model = ""
        self.mesher = None
        self.speed_of_sound_factor = 0
        self.fluid_density_factor = 0

    def _define_qt_variables(self):
        # QComboBox objects
        self.comboBox_selection_by = self.findChild(QComboBox, 'comboBox_selection_by')
        self.comboBox_filter = self.findChild(QComboBox, 'comboBox_filter')
        # QFrame objects
        self.frame_selection_by_surface = self.findChild(QFrame, 'frame_selection_by_surface')
        self.frame_center_coordinates = self.findChild(QFrame, "frame_center_coordinates")
        self.frame_filter_options = self.findChild(QFrame, 'frame_filter_options')
        # QLineEdit objects
        self.lineEdit_center_coordinates = self.findChild(QLineEdit, 'lineEdit_center_coordinates')
        self.lineEdit_selection_id = self.findChild(QLineEdit, "lineEdit_selection_id")
        self.lineEdit_diameter = self.findChild(QLineEdit, "lineEdit_diameter")
        self.lineEdit_selection_radius = self.findChild(QLineEdit, "lineEdit_selection_radius")
        self.lineEdit_selection_radius.setDisabled(True)
        # QPushButton objects
        self.pushButton_confirm = self.findChild(QPushButton, "pushButton_confirm")
        self.pushButton_get_lrf_info = self.findChild(QPushButton, "pushButton_get_lrf_info")
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
        self.comboBox_selection_by.currentIndexChanged.connect(self.update_selection_type_controls)
        #
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)
        #
        self.lineEdit_selection_radius.editingFinished.connect(self.call_sphere_plotter)
        #
        self.pushButton_confirm.clicked.connect(self.set_lrf_eq_model_data)
        self.pushButton_get_lrf_info.clicked.connect(self.get_lrf_info)
        self.pushButton_selection_info.clicked.connect(self.get_selection_information)
        self.pushButton_remove.clicked.connect(self.remove_lrf_eq_model_inputs)
        self.pushButton_reset.clicked.connect(self.reset_lrf_eq_model_inputs)
        #
        self.treeWidget_lrf_model_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_lrf_model_info.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.update_selection_type_controls()

    def update_selection_type_controls(self):
        index = self.comboBox_selection_by.currentIndex()
        if index == 0:
            self.frame_center_coordinates.setVisible(False)
            self.frame_selection_by_surface.setVisible(False)
            self.frame_filter_options.setVisible(False)
        else:
            self.frame_center_coordinates.setVisible(True)
            self.frame_selection_by_surface.setVisible(True)
            self.frame_filter_options.setVisible(True)
            self.call_sphere_plotter()

    def geometry_selection_callback(self, points, lines, faces, volumes):
        self.lineEdit_selection_radius.setDisabled(True)
        self.pushButton_selection_info.setDisabled(True)
        selection_index = self.comboBox_selection_by.currentIndex()
        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.lineEdit_selection_radius.setDisabled(False)
            self.pushButton_selection_info.setDisabled(False)
            if selection_index == 0:
                self.comboBox_selection_by.setCurrentIndex(1)
            self.call_sphere_plotter()
        elif volumes:
            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_selection_by.setCurrentIndex(0)
            self.hide_sphere()
        elif not any([points, lines, faces]):
            self.lineEdit_selection_id.setText("")
            self.lineEdit_center_coordinates.setText("")
            self.hide_sphere()

    def get_center_coordinates(self):

        selection_id = self.lineEdit_selection_id.text()
        selection_index = self.comboBox_selection_by.currentIndex()
        if selection_id == "" or selection_index == 0:
            self.lineEdit_center_coordinates.setText("")
            return []

        index = self.comboBox_selection_by.currentIndex()
        if index == 1:
            averaged_selection = False
        elif index == 2:
            averaged_selection = True

        center_coords = self.model.get_average_nodal_coordinates(selection_id, averaged=averaged_selection)
        if averaged_selection:
            try:
                _round_center_coords = [round(value,4) for value in center_coords[0]]
                self.lineEdit_center_coordinates.setText(str(_round_center_coords))
            except:
                self.lineEdit_center_coordinates.setText("")
                return []
        else:
            self.lineEdit_center_coordinates.setText("Multiple centers")
        return center_coords

    def check_selection_radius(self):
        self.selection_radius = None
        lineEdit = self.lineEdit_selection_radius
        self.selection_radius = self.check_inputs(lineEdit, "Selection radius")
        if self.stop:
            lineEdit.setFocus()
            return True

    def call_sphere_plotter(self):
        if self.comboBox_selection_by.currentIndex() > 0:
            if self.check_selection_radius():
                return
            center_coords = self.get_center_coordinates()
            if len(center_coords):
                all_radius = [self.selection_radius for i in center_coords]
                geometry_widget = self.main_window.viewer_tabs.geometry_widget
                geometry_widget.set_selection_spheres(center_coords, all_radius)

                mesh_widget = self.main_window.viewer_tabs.mesh_widget
                mesh_widget.set_selection_spheres(center_coords, all_radius)

    def hide_sphere(self):
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.clear_selection_spheres()
        mesh_widget = self.main_window.viewer_tabs.mesh_widget
        mesh_widget.clear_selection_spheres()

    def get_selection_information(self):
        selection_id = self.lineEdit_selection_id.text()
        index = self.comboBox_selection_by.currentIndex()
        if selection_id != "":
            if index > 0:

                if self.check_selection_radius():
                    return
                
                if index == 1:
                    averaged_selection = False
                elif index == 2:
                    averaged_selection = True

                if self.generate_mesh():
                    return
                
                filter_type = self.comboBox_filter.currentIndex()
                GetSphereSelectionInformation(  selection_id,
                                                self.selection_radius,
                                                averaged_selection,
                                                filter_type  )
                self.main_window.viewer_tabs.show_geometry()

    def generate_mesh(self):
        if not self.main_window.project.model.generated_mesh:
            self.mesher = MesherInputs(close_after_generate=True)
            if not self.mesher.complete:
                self.mesher = None
                return True

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
        if self.comboBox_selection_by.currentIndex() == 0:
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
        
        index = self.comboBox_selection_by.currentIndex()
        if index == 0:

            data = {"diameter" : self.diameter}
            for _id in self.volume_ids:
                self.project.set_lrf_eq_model_data(data, volume=_id)

        else:

            if index == 1:
                averaged_selection = False
            elif index == 2:
                averaged_selection = True

            group_id = self.get_lrf_group_index()
            filter_type = self.comboBox_filter.currentIndex()

            data = {"surface_ids" : np.array(self.surface_ids),
                    "selection_radius" : self.selection_radius,
                    "averaged" : averaged_selection,
                    "filter_type" : filter_type,
                    "diameter" : self.diameter}

            for _id in self.surface_ids:
                self.project.set_lrf_eq_model_data(data, group=group_id)
        
        self.load_lrf_data()
        # self.close()

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
        title = "Invalid input at LRF eq. model"
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
            PrintMessageInput([window_title, title, message])
            self.stop = True
            return None
        return out

    def on_click_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))
        self.remove_lrf_eq_from_selection()

    def get_lrf_info(self):
        if self.lineEdit_selection_id.text() != "":

            picked_id = self.lineEdit_selection_id.text()
            
            def get_info(data):
                GetSphereSelectionInformation(  data["surface_ids"],
                                                data["selection_radius"],
                                                data["averaged"],
                                                data["filter_type"]  )
                self.main_window.viewer_tabs.show_geometry()

            group_properties = self.properties.group_properties.copy()
            for key, data in group_properties.items():
                property, group_id = key
                if property == "lrf_eq_model" and int(picked_id) == group_id:
                    # self.pushButton_get_lrf_info.setDisabled(False)
                    return get_info(data)

            # volume_properties = self.properties.volume_properties.copy()
            # for key, data in volume_properties.items():
            #     property, volume_id = key
            #     if property == "lrf_eq_model" and int(picked_id) == volume_id:
            #         return get_info()
            
    def remove_lrf_eq_from_selection(self):

        if self.lineEdit_selection_id.text() != "":

            picked_id = int(self.lineEdit_selection_id.text())
            group_properties = self.properties.group_properties.copy()
            volume_properties = self.properties.volume_properties.copy()
            
            for key in group_properties.keys():
                property, group_id = key
                if property == "lrf_eq_model" and picked_id == group_id:
                    self.properties._remove_group_property("lrf_eq_model", picked_id)
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
            title = f"Resetting LRF eq. model"
            message = "Do you really want to remove all LRF equivalent model inputs defined to the acoustic model?"
            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

            if read._doNotRun:
                return

            if read._continue:

                if len(group_ids) + len(volume_ids) > 0:
                    self.properties._reset_property("lrf_eq_model")

                self.properties.export_model_properties()

                title = "Model resetting complete"
                message = "All LRF equivalent model effects active on "
                message += "the acoustic model have been removed."
                PrintMessageInput([window_title_2, title, message], auto_close=True)

                self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.set_lrf_eq_model_data()
        elif event.key() == Qt.Key_Delete:
            self.remove_lrf_eq_from_selection()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.hide_sphere()
        try:
            geometry_widget = self.main_window.viewer_tabs.geometry_widget
            geometry_widget.selection_changed.disconnect(self.geometry_selection_callback)
        except TypeError:
            pass  # ignore if there is nothing to disconect

# fmt: on