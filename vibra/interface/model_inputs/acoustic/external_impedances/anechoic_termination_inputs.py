# fmt: on

from PySide6.QtWidgets import QTreeWidgetItem, QAbstractItemView
from PySide6.QtCore import Qt, QPoint, QItemSelectionModel
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.ui_generated.model.setup.acoustic.anechoic_termination_inputs_ui import AnechoicTerminationInputs_UI
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.acoustic.definitions.enums import SetupTabType

window_title_1 = "Error"
window_title_2 = "Warning"


class AnechoicTerminationInputs(AnechoicTerminationInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.project = app().project
        self.model = app().new_project.model
        self.mesh = app().new_project.model.mesh
        self.properties = app().new_project.model.properties

        self._initialize()
        self._config_window()
        self._configure_qt_variables()
        self._create_connections()
        self._config_widgets()

        self.load_model_info()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.keep_window_open = True
        self.anechoic_termination = None
        self.tree_item_clicked = False

    def _configure_qt_variables(self):
        self.comboBox_volume_id.setDisabled(True)
        self.lineEdit_selection_id.setDisabled(True)
        self.treeWidget_anechoic_termination.setColumnWidth(1, 20)
        self.treeWidget_anechoic_termination.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_anechoic_termination.itemClicked.connect(self.on_click_item)
        self.treeWidget_anechoic_termination.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

    def _config_widgets(self):
        #
        self.comboBox_volume_id.setDisabled(True)
        #
        self.lineEdit_selection_id.setDisabled(True)
        #
        for i, w in enumerate([120]):
            self.treeWidget_anechoic_termination.setColumnWidth(i, w)
            self.treeWidget_anechoic_termination.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def tab_event_callback(self):
        app().main_window.selection.clear_selection()

        self.clear_line_edit_selection_id()
        self.treeWidget_anechoic_termination.clearSelection()
        self.pushButton_remove.setDisabled(True)

        if self.tabWidget_main.currentIndex() == SetupTabType.LIST:
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_attribute.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)
            self.pushButton_attribute.setEnabled(True)

    def geometry_selection_callback(self):
        if self.tabWidget_main.currentIndex() == SetupTabType.LIST:
            self.verify_if_selected_surfaces_are_in_tree_widget_anechoic_termination()
            return

        faces = app().main_window.selection.geometry_surfaces

        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.update_volumes_from_faces()

    def update_volumes_from_faces(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(
                                                                input_ids, 
                                                                selection = "surfaces"
                                                                )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        list_volumes = list()
        for face_id in surface_ids:            
            for volume_id in self.model.mesh.volumes_from_surface[face_id]:
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
    
    def verify_if_selected_surfaces_are_in_tree_widget_anechoic_termination(self):
        if self.tree_item_clicked:
            return

        selected_surfaces = app().main_window.selection.geometry_surfaces

        if not selected_surfaces:
            return

        self.clear_line_edit_selection_id()
        self.treeWidget_anechoic_termination.clearSelection()
        self.pushButton_remove.setDisabled(True)

        map_id_to_model_index = self.get_tree_widget_anechoic_termination_items_map()
        selected_ids = set(map_id_to_model_index.keys())
        selected_surfaces_in_tree_widget = selected_surfaces.intersection(selected_ids)

        if not selected_surfaces_in_tree_widget:
            return
        
        self.pushButton_remove.setEnabled(True)
        
        model_selector = self.treeWidget_anechoic_termination.selectionModel()

        for surface_id in selected_surfaces_in_tree_widget:
            model_index = map_id_to_model_index[surface_id]

            model_selector.select(model_index, QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)

        self.treeWidget_anechoic_termination.setSelectionMode(QAbstractItemView.SingleSelection)
        self.set_selection_text(selected_surfaces_in_tree_widget)

    def get_tree_widget_anechoic_termination_items_map(self) -> dict:
        map_id_to_model_index = dict()

        index = self.treeWidget_anechoic_termination.indexAt(QPoint(0, 0))
        while index.isValid():
            item = self.treeWidget_anechoic_termination.itemFromIndex(index)
            surface_id = item.text(0)

            map_id_to_model_index[int(surface_id)] = index

            index = self.treeWidget_anechoic_termination.indexBelow(index)
        
        return map_id_to_model_index

    def attribute_callback(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(
                                                                input_ids, 
                                                                selection = "surfaces"
                                                                )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        self.remove_conflicting_excitations(surface_ids)

        for surface_id in surface_ids:

            volume_ids = self.model.mesh.volumes_from_surface[surface_ids[0]]
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
                try:
                    volume_id = int(self.comboBox_volume_id.currentText())
                except Exception:
                    window_title = "Error"
                    title = "Error in the model setup"
                    message = "You cannot set an anechoic termination for a shell element"

                    PrintMessageInput([window_title, title, message])
                    return

            data = {
                    "anechoic_termination" : True,
                    "volume_id" : volume_id,
                    }

            self.properties._set_property("specific_impedance", data, surface=surface_id)

        self.actions_to_finalize()

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().new_project.update_model_properties_file()

    def remove_conflicting_excitations(self, surface_ids: int | list):

        if isinstance(surface_ids, int):
            surface_ids = [surface_ids]

        labels = [
            "absorption_surface",
            "specific_impedance",
            "incident_plane_wave",
            ]

        for surface_id in surface_ids:
            for label in labels:
                table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_id : list):
        table_names = self.properties.get_property_related_table_names("specific_impedance", surface_id, "surfaces")
        self.process_table_file_removal(table_names)

    def remove_callback(self):
        selected_surfaces = self.get_selected_surfaces_from_tree_widget_anechoic_termination()

        if not selected_surfaces:
            return
    
        for surface_id in selected_surfaces:
            self.remove_table_files_from_surfaces(surface_id)
            self.properties._remove_surface_property("specific_impedance", surface_id)

        self.clear_line_edit_selection_id()
        self.pushButton_remove.setDisabled(True)

        app().main_window.selection.clear_selection()
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

            surface_ids = list()
            for (property, *args), data in self.properties.surface_properties.items():
                if property == "specific_impedance":
                    if "anechoic_termination" in data.keys():
                        surface_id = args[0]
                        surface_ids.append(surface_id)

            self.remove_table_files_from_surfaces(surface_ids)

            self.properties._reset_property("specific_impedance")
            self.actions_to_finalize()

    def actions_to_finalize(self):
        self.load_model_info()
        self.check_model_frequency_controls()
        app().main_window.update_info_text()
        app().new_project.update_model_properties_file()
        app().main_window.update_symbols()

    def check_model_frequency_controls(self):

        for key, data in self.properties.surface_properties.items():
            property, _ = key
            if property in ["acoustic_pressure", "surface_velocity", "specific_impedance", "reciprocating_compressor_excitation"]:
                if "table_names" in data.keys():
                    return

        if isinstance(self.project.analysis_setup, dict):
            analysis_setup = self.project.analysis_setup
            self.project.set_analysis_setup(analysis_setup)
            app().file.write_analysis_setup_in_file(analysis_setup)

    def update_tabs_visibility(self):

        for key, data in self.properties.surface_properties.items():
            property, *args = key
            if property == "specific_impedance":
                if "anechoic_termination" in data.keys():
                    self.tabWidget_main.setTabVisible(SetupTabType.LIST, True)
                    return

        self.tabWidget_main.setCurrentIndex(SetupTabType.SETUP)
        self.tabWidget_main.setTabVisible(SetupTabType.LIST, False)

    def on_click_item(self, item):
        self.tree_item_clicked = True

        surface_ids = self.get_selected_surfaces_from_tree_widget_anechoic_termination()

        if not surface_ids:
            return
    
        app().main_window.selection.set_geometry_selection(surfaces=surface_ids)

        self.pushButton_remove.setDisabled(False)
        self.set_selection_text(surface_ids)

        self.tree_item_clicked = False

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def get_selected_surfaces_from_tree_widget_anechoic_termination(self) -> list:
        selected_items = self.treeWidget_anechoic_termination.selectedItems()

        if not selected_items:
            return list()

        return [int(item.text(0)) for item in selected_items]
    
    def set_selection_text(self, selected_surfaces: list | set):
        selected_surfaces = list(selected_surfaces)
        selected_surfaces.sort()

        selected_surfaces = map(str, selected_surfaces)
        selection_text = ", ".join(selected_surfaces)

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)
    
    def clear_line_edit_selection_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")

    def load_model_info(self):
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_main.currentIndex() == SetupTabType.SETUP:
                self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Control:
            self.treeWidget_anechoic_termination.setSelectionMode(QAbstractItemView.MultiSelection)
        elif event.key() == Qt.Key_Shift:
            self.treeWidget_anechoic_termination.setSelectionMode(QAbstractItemView.ContiguousSelection)
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.treeWidget_anechoic_termination.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)
    
# fmt: on