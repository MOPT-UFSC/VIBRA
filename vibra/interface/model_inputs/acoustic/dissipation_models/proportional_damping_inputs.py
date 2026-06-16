from PySide6.QtCore import QItemSelectionModel, QPoint, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.interface import error_title
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.acoustic.definitions.enums import AttributionBodiesType, SetupTabType
from vibra.interface.ui_generated.model.acoustic.dissipation_models.proportional_damping_inputs_ui import ProportionalDampingInputs_UI


class ProportionalDampingInput(ProportionalDampingInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()
        app().main_window.selection.volume_selection_mode = True

        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._create_connections()
        self.load_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.keep_window_open = True
        self.tree_item_clicked = False

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_proportional_damping.itemClicked.connect(self.on_click_item)
        self.treeWidget_proportional_damping.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.geometry_selection_callback()
        self.attribution_type_callback()

    def attribution_type_callback(self):

        index = self.comboBox_attribution_type.currentIndex()
        if index == AttributionBodiesType.ALL_BODIES:
            self.lineEdit_selection_id.setText("All bodies")
        elif index == AttributionBodiesType.SELECTED_BODIES:
            self.clear_line_edit_selection_id()

        self.lineEdit_selection_id.setEnabled(bool(index))

    def geometry_selection_callback(self):
        if self.tabWidget_main.currentIndex() == SetupTabType.LIST:
            self.verify_if_selected_volumes_are_in_tree_widget_proportional_damping()
            return

        volumes = app().main_window.selection.geometry_volumes

        if volumes:
            volume_ids = [int(vol_id) for vol_id in volumes]

            if self.comboBox_attribution_type.currentIndex() == AttributionBodiesType.ALL_BODIES:
                self.comboBox_attribution_type.setCurrentIndex(AttributionBodiesType.SELECTED_BODIES)

            text = ", ".join([str(i) for i in volume_ids])
            self.lineEdit_selection_id.setText(text)

            if len(volume_ids) == 1:
                p_data = self.properties._get_property("proportional_damping", volume=volume_ids[0])
                if p_data is None:
                    return
                
                self.load_dissipation_model_data(p_data)

    def load_dissipation_model_data(self, data: dict):

        self.lineEdit_speed_of_sound_complex_factor.clear()
        self.lineEdit_fluid_density_complex_factor.clear()

        if not isinstance(data, dict):
            return

        speed_factor = data.get("speed_of_sound_factor", 0.)
        self.lineEdit_speed_of_sound_complex_factor.setText(f"{speed_factor : .4f}")

        density_factor = data.get("density_factor", 0.)
        self.lineEdit_fluid_density_complex_factor.setText(f"{density_factor : .4f}")
        self.actions_to_finalize()
    
    def verify_if_selected_volumes_are_in_tree_widget_proportional_damping(self):
        if self.tree_item_clicked:
            return

        selected_volumes = app().main_window.selection.geometry_volumes

        if not selected_volumes:
            return

        self.clear_line_edit_selection_id()
        self.treeWidget_proportional_damping.clearSelection()
        self.pushButton_remove.setDisabled(True)

        map_id_to_model_index = self.get_tree_widget_proportional_damping_items_map()
        selected_ids = set(map_id_to_model_index.keys())
        selected_volumes_in_tree_widget = selected_volumes.intersection(selected_ids)

        if not selected_volumes_in_tree_widget:
            return
        
        self.pushButton_remove.setEnabled(True)
        
        model_selector = self.treeWidget_proportional_damping.selectionModel()

        for volume_id in selected_volumes_in_tree_widget:
            model_index = map_id_to_model_index[volume_id]

            model_selector.select(model_index, QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)

        self.treeWidget_proportional_damping.setSelectionMode(QAbstractItemView.SingleSelection)
        self.set_selection_text(selected_volumes_in_tree_widget)

    def get_tree_widget_proportional_damping_items_map(self) -> dict:
        map_id_to_model_index = dict()

        index = self.treeWidget_proportional_damping.indexAt(QPoint(0, 0))
        while index.isValid():
            item = self.treeWidget_proportional_damping.itemFromIndex(index)
            volume_id = int(item.text(0))

            map_id_to_model_index[volume_id] = index

            index = self.treeWidget_proportional_damping.indexBelow(index)
        
        return map_id_to_model_index

    def check_inputs(self, lineEdit: QLineEdit, label: str, only_positive=False, zero_included=True, _float=True):

        message = ""
        title = "Invalid input at dissipation model"

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
                message = "Dear user, you have typed an invalid value at the \n"
                message += f"{label} input field.\n\n"
                message += str(_err)

        else:
            if zero_included:
                return float(0)
            else:
                message = f"Insert some value at the {label} input field."

        if message != "":
            PrintMessageInput([error_title, title, message])
            return None

        return out

    def apply_callback(self, close_window: bool = False):

        attribute_type = self.comboBox_attribution_type.currentIndex()
            
        volume_ids = list()
        if attribute_type == AttributionBodiesType.ALL_BODIES:
            if "volumes" in self.mesh.geometry_information.keys():
                volume_ids = self.mesh.geometry_information["volumes"]

        elif attribute_type == AttributionBodiesType.SELECTED_BODIES:
            input_ids = self.lineEdit_selection_id.text()
            volume_ids, error_data = self.mesh.check_selected_ids(input_ids, selection="volumes", single_id=False)

            if error_data is not None:
                self.hide()
                self.lineEdit_selection_id.setFocus()
                PrintMessageInput(error_data)
                return

        lineEdit = self.lineEdit_speed_of_sound_complex_factor
        speed_of_sound_factor = self.check_inputs(lineEdit, "Speed of sound complex factor", only_positive=True)
        if speed_of_sound_factor is None:
            lineEdit.setFocus()
            return True

        lineEdit = self.lineEdit_fluid_density_complex_factor
        fluid_density_factor = self.check_inputs(lineEdit, "Fluid density complex factor", only_positive=True)
        if fluid_density_factor is None:
            lineEdit.setFocus()
            return True

        data = {
            "speed_of_sound_factor": speed_of_sound_factor,
            "fluid_density_factor": fluid_density_factor,
        }

        for volume_id in volume_ids:
            self.properties._set_property("proportional_damping", data, volume=volume_id)

        self.actions_to_finalize(close_window)

    def remove_callback(self):
        selected_volumes = self.get_selected_volumes_from_tree_widget_proportional_damping()

        if not selected_volumes:
            return

        for volume_id in selected_volumes:
            self.properties._remove_volume_property("proportional_damping", volume_id)

        self.clear_line_edit_selection_id()
        self.treeWidget_proportional_damping.clearSelection()
        self.pushButton_remove.setDisabled(True)

        app().main_window.selection.clear_selection()
        self.actions_to_finalize()

    def reset_callback(self):

        volume_ids = list()
        for (property, volume_id) in self.properties.volume_properties.keys():
            if property != "proportional_damping":
                continue
            volume_ids.append(volume_id)

        if volume_ids:

            self.hide()

            title = "Proportional damping reset"
            message = "Would you like to remove the proportional damping effects?"

            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:
                for volume_id in volume_ids:
                    self.properties._remove_volume_property("proportional_damping", volume_id)

                self.actions_to_finalize()

    def tab_event_callback(self):
        app().main_window.selection.clear_selection()

        list_tab = self.tabWidget_main.currentIndex() == SetupTabType.LIST
        self.pushButton_apply.setDisabled(list_tab)
        self.pushButton_apply_and_close.setDisabled(list_tab)
        self.lineEdit_selection_id.setDisabled(list_tab)
        self.comboBox_attribution_type.setDisabled(list_tab)

        self.clear_line_edit_selection_id()

        if list_tab:
            self.pushButton_remove.setDisabled(True)
            self.treeWidget_proportional_damping.clearSelection()

    def on_click_item(self, item):
        self.tree_item_clicked = True

        volume_ids = self.get_selected_volumes_from_tree_widget_proportional_damping()

        if not volume_ids:
            return

        app().main_window.selection.set_geometry_selection(volumes=volume_ids)

        self.pushButton_remove.setEnabled(True)
        self.set_selection_text(volume_ids)

        self.tree_item_clicked = False

    def on_doubleclick_item(self, item):
        self.on_click_item(item)
    
    def get_selected_volumes_from_tree_widget_proportional_damping(self) -> list:
        selected_items = self.treeWidget_proportional_damping.selectedItems()

        if not selected_items:
            return list()
        
        return [int(item.text(0)) for item in selected_items]
    
    def set_selection_text(self, selected_volumes: list | set):
        selected_volumes = list(selected_volumes)
        selected_volumes.sort()

        selected_volumes = map(str, selected_volumes)
        selection_text = ", ".join(selected_volumes)

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)
    
    def clear_line_edit_selection_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")

    def load_info(self):
        self.treeWidget_proportional_damping.clear()
        self.treeWidget_proportional_damping.setColumnWidth(0, 80)
        self.treeWidget_proportional_damping.setColumnWidth(1, 160)

        for key, data in self.properties.volume_properties.items():

            property, volume_id = key
            if property != "proportional_damping":
                continue

            data: dict
            speed_factor = data.get("speed_of_sound_factor")
            density_factor = data.get("fluid_density_factor")

            item = QTreeWidgetItem([str(volume_id), f"{speed_factor}", f"{density_factor}"])
            for i in range(3):
                item.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_proportional_damping.addTopLevelItem(item)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        for (property, _) in self.properties.volume_properties.keys():
            if property != "proportional_damping":
                continue

            self.tabWidget_main.setTabVisible(SetupTabType.LIST, True)
            return

        self.tabWidget_main.setTabVisible(SetupTabType.LIST, False)
        self.tabWidget_main.setCurrentIndex(SetupTabType.SETUP)

    def actions_to_finalize(self, close_window: bool = False):
        self.load_info()
        app().main_window.update_info_text()
        app().project.update_model_properties_file()
        app().main_window.update_symbols()

        if close_window:
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Control:
            self.treeWidget_proportional_damping.setSelectionMode(QAbstractItemView.MultiSelection)
        elif event.key() == Qt.Key_Shift:
            self.treeWidget_proportional_damping.setSelectionMode(QAbstractItemView.ContiguousSelection)
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.treeWidget_proportional_damping.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        app().main_window.selection.volume_selection_mode = False
        return super().closeEvent(a0)