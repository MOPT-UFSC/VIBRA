# fmt: on

from PySide6.QtWidgets import QComboBox, QDialog, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem 
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6 import uic

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"


class SetAnechoicTerminationInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/set_anechoic_termination_input.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.project = app().main_window.project
        self.model = app().main_window.project.model
        self.mesh = app().main_window.project.model.mesh
        self.properties = app().main_window.project.model.properties

        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()

        self._reset()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

        self.load_info()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Vibra")

    def _reset(self):
        self.keep_window_open = True
        self.anechoic_termination = None

    def _define_qt_variables(self):
        
        # QComboBox
        self.comboBox_volume_id : QComboBox
        self.comboBox_volume_id.setDisabled(True)

        # QLineEdit
        self.lineEdit_selection_id : QLineEdit
        self.lineEdit_selection_id.setDisabled(True)

        # QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_remove_bc_confirm : QPushButton
        self.pushButton_reset : QPushButton

        # QTabWidget
        self.tabWidget_anechoic_termination : QTabWidget
        
        # QTreeWidget
        self.treeWidget_anechoic_termination : QTreeWidget
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
        self.main_window.selection_changed.connect(self.geometry_selection_callback)

    def tabEvent_callback(self):
        current_tab = self.tabWidget_anechoic_termination.currentIndex()
        if current_tab == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)

    def on_click_item(self, item):
        if item.text(0) != "":
            surface_id = int(item.text(0))
            self.lineEdit_selection_id.setText(item.text(0))
            app().main_window.set_geometry_selection(surfaces=[surface_id])

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

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

    def geometry_selection_callback(self):

        faces = self.main_window.selected_geometry_surfaces

        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.update_volumes_from_faces()  

    def update_volumes_from_faces(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        stop, surface_ids = self.mesh.check_selected_ids(lineEdit_selection_id, selection="surfaces")
        if stop:
            return

        list_volumes = list()
        for face_id in surface_ids:            
            for volume_id in self.model.mesh.volume_from_surface[face_id]:
                if volume_id not in list_volumes:
                    list_volumes.append(volume_id)

        self.comboBox_volume_id.clear()
        for vol_id in list_volumes:
            self.comboBox_volume_id.addItem(str(vol_id))
        
        if len(list_volumes) == 1:
            self.comboBox_volume_id.setDisabled(True)
        else:
            if len(surface_ids) == 1:
                self.comboBox_volume_id.setDisabled(False)
            else:
                self.comboBox_volume_id.clear()
                self.comboBox_volume_id.addItem("multiple")

    def confirm_button_pressed(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        stop, surface_ids = self.mesh.check_input_surface_id(lineEdit_selection_id)
        if stop:
            self.lineEdit_selection_id.setFocus()
            return

        for face_id in surface_ids:

            volume_ids = self.model.mesh.volume_from_surface[surface_ids[0]]
            if len(surface_ids) > 1 and len(volume_ids) > 1:
                
                self.hide()
                title = "Undefined volume"
                
                # message = f"The selected face ID [{face_id}] is associated to the volumes {volume_ids}. "
                message = "The multiple selection of faces related to more than one volume is not allowed. "
                message += "In this case, it is necessary to select the Face ID and the respective Volume ID "
                message += "to proceed."
                PrintMessageInput([window_title_2, title, message])

                return

            if self.comboBox_volume_id.currentText() == "multiple":
                volume_id = volume_ids[0]
            else:
                volume_id = int(self.comboBox_volume_id.currentText())

            data = {
                    "anechoic_termination" : True,
                    "volume_id" : volume_id,
                    "nodal_attribution": False
                    }

            self.project.set_specific_impedance(data, face_id)

        self.main_window.viewer_tabs.update_info_text()
        app().main_window.file.write_model_properties_in_file()

        print(f"[Set anechoic termination] - defined at surface(s) {surface_ids}")
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

            self.hide()
            
            title = "Resetting of all applied specific impedances"
            message = "Would you like to remove the all applied anechoic terminations from the model?"

            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:
                for face_id in surface_ids:
                    self.properties._remove_surface_property("specific_impedance", face_id)

                app().main_window.file.write_model_properties_in_file()
                self.close()

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

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)
    
# fmt: on