# fmt: on

from PySide6.QtWidgets import QComboBox, QDialog, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem 
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app, UI_DIR
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow

from molde import load_ui
from copy import deepcopy

window_title_1 = "Error"
window_title_2 = "Warning"


class DegreesOfFreedomDecouplingInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/acoustic_dofs_decoupling_inputs.ui"
        load_ui(ui_path, self, ui_path.parent)

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        app().main_window.set_input_widget(self)
        app().main_window.action_model_workspace_callback()

        self._initialize()
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

    def _initialize(self):
        self.setup_complete = False
        self.keep_window_open = True
        self.cache_surface_properties = deepcopy(self.properties.surface_properties)

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
        self.treeWidget_dofs_decoupling.setColumnWidth(1, 40)
        self.treeWidget_dofs_decoupling.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_dofs_decoupling.itemClicked.connect(self.on_click_item)
        self.treeWidget_dofs_decoupling.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)

    def tab_event_callback(self):
        if self.tabWidget_main.currentIndex() == 1:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_attribute.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)
            self.pushButton_attribute.setEnabled(True)

    def geometry_selection_callback(self):

        faces = app().main_window.selected_geometry_surfaces

        if len(faces) == 1:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.update_volumes_from_faces()  

    def update_volumes_from_faces(self):

        self.comboBox_volume_id.setDisabled(True)
        input_ids = self.lineEdit_selection_id.text()
        surface_ids = self.mesh.check_selected_ids(
                                                   input_ids, 
                                                   selection = "surfaces"
                                                   )

        if surface_ids is None:
            return

        self.comboBox_volume_id.clear()
        volumes_from_surface = self.model.mesh.volumes_from_surface[surface_ids[0]]

        if len(volumes_from_surface) != 2:
            return

        self.comboBox_volume_id.setEnabled(True)
        for volume_id in volumes_from_surface:
            self.comboBox_volume_id.addItem(str(volume_id))

        for volume_id in volumes_from_surface:

            for surface_id in self.model.mesh.surfaces_from_volume[volume_id]:
                if surface_id in surface_ids:
                    continue

                for property in ["surface_velocity", "acoustic_pressure", "reciprocating_compressor"]:
                    data = self.model.properties._get_property(property, surface=surface_id)
                    if isinstance(data, dict):
                        self.select_the_volume_to_preserve(volumes_from_surface, volume_id)
                        return

    def select_the_volume_to_preserve(self, volume_ids: list[int], volume_to_preserve: int):

        if len(volume_ids) == 2:
            for volume_id in volume_ids:
                if volume_id != volume_to_preserve:
                    self.comboBox_volume_id.setCurrentText(str(volume_id))
                    return

    def attribute_callback(self):

        str_selection_ids = self.lineEdit_selection_id.text()
        surface_ids = self.mesh.check_selected_ids(str_selection_ids, selection="surfaces")
        if surface_ids is None:
            self.lineEdit_selection_id.setFocus()
            return
        
        surface_id = surface_ids[0]

        if len(surface_ids) != 1:
            return

        message = ""
        volumes_from_surface = self.model.mesh.volumes_from_surface.get(surface_id)

        if volumes_from_surface is None:
            message = "The selected surface is not connected to any volume. "
            message += "You must select an internal surface connected "
            message += "with two volumes to proceed with dofs decoupling."

        elif len(volumes_from_surface) == 1:
            message = "The selected surface is connected to one volume, this means that an external " 
            message += "surface has been selected. You must select an internal surface connected "
            message += "with two volumes to proceed with dofs decoupling."

        if message != "":
            self.hide()
            title = "Invalid surface selected"
            PrintMessageInput([window_title_2, title, message])
            return

        data = {"volume_to_decouple" : int(self.comboBox_volume_id.currentText())}
        self.properties._set_property("acoustic_dofs_decoupling", data, surface=surface_id)

        self.setup_complete = True
        self.actions_to_finalize()

    def remove_all_surface_properties_from_surface(self, new_surface_ids: list[int]):
        if not new_surface_ids:
            return

        surface_properties = deepcopy(self.properties.surface_properties)
        for new_surface_id in new_surface_ids:
            for (property, surf_id) in surface_properties.keys():
                if surf_id == new_surface_id:
                    self.properties._remove_surface_property(property, new_surface_id)

    def remove_all_line_properties_boundind_surface(self, new_surface_ids: list[int]):
        if not new_surface_ids:
            return

        line_properties = deepcopy(self.properties.line_properties)
        for new_surface_id in new_surface_ids:
            lines_from_surface = self.mesh.lines_from_surface.get(new_surface_id)
            if lines_from_surface is None:
                continue

            for line_from_surface in lines_from_surface:
                for (property, line_id) in line_properties.keys():
                    if line_from_surface == line_id:
                        self.properties._remove_line_property(property, line_id)

    def remove_callback(self):

        if self.lineEdit_selection_id.text() != "":

            surface_id = int(self.lineEdit_selection_id.text())
            data = self.properties._get_property("acoustic_dofs_decoupling", surface=surface_id)
            if isinstance(data, dict):
                new_surface_id = data.get("new_surface_id")
                if isinstance(new_surface_id, int):   
                    self.remove_all_surface_properties_from_surface([new_surface_id])
                    self.remove_all_line_properties_boundind_surface([new_surface_id]) 

            self.properties._remove_surface_property("acoustic_dofs_decoupling", surface_id)

            app().project.model.generated_mesh = False
            app().file.remove_mesh_data_from_project_file
            app().file.remove_mesh_data_from_project_file()
            app().file.remove_results_data_from_project_file()
            self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Acoustic dofs decoupling resetting"
        message = "Would you like to revert the acoustic degrees of freedom decoupling from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            new_surface_ids = list()
            for (property, _), data in self.properties.surface_properties.items():
                if property == "acoustic_dofs_decoupling":
                    data: dict
                    new_surface_id = data.get("new_surface_id")
                    if isinstance(new_surface_id, int):
                        new_surface_ids.append(new_surface_id)

            self.remove_all_surface_properties_from_surface([new_surface_id])
            self.remove_all_line_properties_boundind_surface([new_surface_id]) 
            self.properties._reset_property("acoustic_dofs_decoupling")

            app().project.model.generated_mesh = False
            app().file.remove_mesh_data_from_project_file()
            app().file.remove_results_data_from_project_file()
            self.actions_to_finalize()

    def actions_to_finalize(self):
        self.load_info()
        app().file.write_model_properties_in_file()
        app().file.write_imported_table_data_in_file()
        app().main_window.update_info_text()
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
                data: dict

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

    def is_the_surface_property_present_in_the_model(self, property_to_check: str):

        for (property, _) in app().project.model.properties.surface_properties.keys():
            if property == property_to_check:
                return True

        return False

    def process_degress_of_freedom_decoupling(self):

        if not self.setup_complete:
            return False
        
        if not self.properties.is_the_surface_property_present_in_the_model("acoustic_dofs_decoupling"):
            return False

        if not app().project.model.generated_mesh:
            self.hide()
            app().main_window.input_ui.mesh_setup()
            app().main_window.set_input_widget(self)
            if not app().project.model.generated_mesh:
                return True
            else:
                return False

        if self.mesh.cache_nodal_coordinates is None:
            self.mesh.cache_mesh_information()

        def process_decoupling():
            self.model.process_degrees_of_freedom_decoupling()
            app().file.write_mesh_data_in_file()
            app().file.write_geometry_data_in_file()
            app().main_window.update_mesh_information()
            app().main_window.update_geometry_information()
            app().main_window.update_plots()

        LoadingWindow(process_decoupling).run()
        return False

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        if self.process_degress_of_freedom_decoupling():
            return

        self.keep_window_open = False
        return super().closeEvent(a0)

# fmt: on