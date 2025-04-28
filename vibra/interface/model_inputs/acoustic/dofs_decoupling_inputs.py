# fmt: on

from PySide6.QtWidgets import QComboBox, QDialog, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem 
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app, UI_DIR
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

from molde import load_ui

window_title_1 = "Error"
window_title_2 = "Warning"


class DofsDecouplingInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/acoustic_dofs_decoupling_inputs.ui"
        load_ui(ui_path, self, ui_path.parent)

        self.main_window = app().main_window
        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self.main_window.set_input_widget(self)
        self.main_window.action_model_workspace_callback()

        self._reset()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()

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
        self.pushButton_attribute : QPushButton
        self.pushButton_exit : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton

        # QTabWidget
        self.tabWidget_main : QTabWidget

        # QTreeWidget
        self.treeWidget_dofs_decoupling : QTreeWidget
        self.treeWidget_dofs_decoupling.setColumnWidth(1, 20)
        self.treeWidget_dofs_decoupling.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tabEvent_callback)
        self.treeWidget_dofs_decoupling.itemClicked.connect(self.on_click_item)
        self.treeWidget_dofs_decoupling.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)

    def tabEvent_callback(self):
        if self.tabWidget_main.currentIndex() == 1:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_attribute.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)
            self.pushButton_attribute.setEnabled(True)

    def geometry_selection_callback(self):

        faces = self.main_window.selected_geometry_surfaces

        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.update_volumes_from_faces()  

    def update_volumes_from_faces(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_ids = self.mesh.check_selected_ids(
                                                   input_ids, 
                                                   selection = "surfaces"
                                                   )

        if surface_ids is None:
            return

        volume_ids = list()
        for surface_id in surface_ids:            
            for volume_id in self.model.mesh.volumes_from_surface[surface_id]:
                if volume_id not in volume_ids:
                    volume_ids.append(volume_id)

        for volume_id in volume_ids:
            for surface_id in self.model.mesh.surfaces_from_volume[volume_id]:
                if surface_id in surface_ids:
                    continue

                # surface_velocity = self.model.properties._get_property("surface_velocity", surface=surface_id)
                # if isinstance(surface_velocity, dict):
                #     current_volume = volume_id
                #     break

                # acoustic_pressure = self.model.properties._get_property("acoustic_pressure", surface=surface_id)
                # if isinstance(acoustic_pressure, dict):
                #     current_volume = volume_id
                #     break

        self.comboBox_volume_id.clear()
        for vol_id in volume_ids:
            self.comboBox_volume_id.addItem(str(vol_id))
        
        if len(volume_ids) == 1:
            self.comboBox_volume_id.setDisabled(True)
        else:
            if len(surface_ids) == 1:
                self.comboBox_volume_id.setDisabled(False)
            else:
                self.comboBox_volume_id.clear()
                self.comboBox_volume_id.addItem("multiple")

    def attribute_callback(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        stop, surface_ids = self.mesh.check_input_surface_id(lineEdit_selection_id)
        if stop:
            self.lineEdit_selection_id.setFocus()
            return

        for surface_id in surface_ids:

            volume_ids = self.model.mesh.volumes_from_surface[surface_ids[0]]
            if len(surface_ids) > 1 and len(volume_ids) > 1:
                
                title = "Undefined volume"

                message = "The multiple selection of faces related to more than one volume is not allowed. "
                message += "In this case, it is necessary to select the Face ID and the respective Volume ID "
                message += "to proceed."

                self.hide()
                PrintMessageInput([window_title_2, title, message])
                return

            if self.comboBox_volume_id.currentText() == "multiple":
                volume_id = volume_ids[0]
            else:
                volume_id = int(self.comboBox_volume_id.currentText())

            data = {
                    "volume_id" : volume_id,
                    "nodal_attribution": False
                    }

            self.properties._set_property("acoustic_dofs_decoupling", data, surface=surface_id)

        self.actions_to_finalize()

        print(f"[Set anechoic termination] - defined at surface(s) {surface_ids}")

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().file.write_imported_table_data_in_file()

    def remove_callback(self):

        if self.lineEdit_selection_id.text() != "":

            surface_id = int(self.lineEdit_selection_id.text())
            data = self.properties._get_property("acoustic_dofs_decoupling", surface=surface_id)
            if isinstance(data, dict):
                new_surface_id = data.get("new_surface_id")
                if isinstance(new_surface_id, int):
                    self.properties._remove_surface_property("fluid", new_surface_id)
                    self.properties._remove_surface_property("fluid_id", new_surface_id)

            self.properties._remove_surface_property("acoustic_dofs_decoupling", surface_id)
            self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Anechoic termination resetting"
        message = "Would you like to remove the all applied anechoic termination from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            new_surface_ids = list()
            for (property, *args), data in self.properties.surface_properties.items():
                if property == "acoustic_dofs_decoupling":
                    data: dict
                    new_surface_id = data.get("new_surface_id")
                    if isinstance(new_surface_id, int):
                        new_surface_ids.append(new_surface_id)

            for _new_surface_id in new_surface_ids:
                self.properties._remove_surface_property("fluid", _new_surface_id)
                self.properties._remove_surface_property("fluid_id", _new_surface_id)

            self.properties._reset_property("acoustic_dofs_decoupling")
            self.actions_to_finalize()

    def actions_to_finalize(self):
        self.load_info()
        self.main_window.update_info_text()
        app().file.write_model_properties_in_file()
        app().file.write_imported_table_data_in_file()
        app().main_window.mesh_widget.update_symbols()

    def update_tabs_visibility(self):
        for key in self.properties.surface_properties.keys():
            property, _ = key
            if property == "acoustic_dofs_decoupling":
                self.tabWidget_main.setTabVisible(1, True)
                return

        self.tabWidget_main.setTabVisible(1, False)

    def on_click_item(self, item):
        if item.text(0) != "":
            surface_id = int(item.text(0))
            self.lineEdit_selection_id.setText(item.text(0))
            app().main_window.set_geometry_selection(surfaces=[surface_id])

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def load_info(self):
        self.treeWidget_dofs_decoupling.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "acoustic_dofs_decoupling":

                volume_id = data.get("volume_to_decouple")
                if volume_id is None:
                    continue

                new = QTreeWidgetItem([str(surface_id), str(volume_id)])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_dofs_decoupling.addTopLevelItem(new)

        self.update_tabs_visibility()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_main.currentIndex() == 0:
                self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            return

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)
    
# fmt: on