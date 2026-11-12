from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QDialog, QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.interface import error_title
from vibra.interface.common.common_interface import update_entities_selection
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.model_inputs.acoustic.definitions.enums import AttributionBodiesType, SetupTabType
from vibra.interface.ui_generated.model.acoustic.dissipation_models.proportional_damping_inputs_ui import ProportionalDampingInputs_UI
from vibra.interface.model_inputs.general.grouping_assistant_inputs import GroupingAssistantInputs


class ProportionalDampingInput(ProportionalDampingInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()
        app().main_window.selection.volume_selection_mode = True

        self._config_window()
        self._configure_validators()
        self._initialize()
        self._create_connections()
        self.load_model_info()

        while self.keep_window_open:
            self.exec()

    @property
    def model(self):
        return app().project.model

    @property
    def mesh(self):
        return app().project.model.mesh

    @property
    def properties(self):
        return app().project.model.properties

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _config_widgets(self):

        self.treeWidget_proportional_damping.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        for i, w in enumerate([70, 180]):
            self.treeWidget_proportional_damping.setColumnWidth(i, w)
            self.treeWidget_proportional_damping.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _initialize(self):
        self.group_assistant = None
        self.keep_window_open = True

    def _configure_validators(self):
        self.lineEdit_speed_of_sound_complex_factor.setValidator(StrictDoubleValidator(0, 1, 8))
        self.lineEdit_fluid_density_complex_factor.setValidator(StrictDoubleValidator(0, 1, 8))

    def _create_connections(self):

        # QComboBox connection
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)

        # QPushButton connection
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_select_group.clicked.connect(self.group_assistant_callback)

        # QTabWidget connection
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)

        # QTreeWidget connection
        self.treeWidget_proportional_damping.itemClicked.connect(self.on_click_item)
        self.treeWidget_proportional_damping.itemDoubleClicked.connect(self.on_doubleclick_item)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

        self.geometry_selection_callback()
        self.attribution_type_callback()

    def attribution_type_callback(self):
        index = self.comboBox_attribution_type.currentIndex()
        all_bodies = index == AttributionBodiesType.ALL_BODIES
        self.lineEdit_selection_id.setDisabled(all_bodies)

        if all_bodies:
            self.lineEdit_selection_id.setText("All bodies")
            return

        self.clear_line_edit_selection_id()

    def geometry_selection_callback(self):
        volumes = app().main_window.selection.geometry_volumes
        if not volumes:
            return

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
            if "volumes" in self.mesh.geometry_information:
                volume_ids = self.mesh.geometry_information["volumes"]

        elif attribute_type == AttributionBodiesType.SELECTED_BODIES:
            input_ids = self.lineEdit_selection_id.text()
            volume_ids, error_data = self.model.check_selected_ids(
                input_ids,
                "volumes",
                domain="acoustic",
            )

            if error_data is not None:
                self.lineEdit_selection_id.setFocus()
                PrintMessageInput(error_data)
                return True

            app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
            update_entities_selection(self.lineEdit_selection_id, "volumes", volume_ids)
            app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

        _eta_speed = self.lineEdit_speed_of_sound_complex_factor.text()
        speed_of_sound_factor = 0 if _eta_speed == "" else float(_eta_speed)

        _eta_density = self.lineEdit_fluid_density_complex_factor.text()
        fluid_density_factor = 0 if _eta_density == "" else float(_eta_density)

        if not any((speed_of_sound_factor, fluid_density_factor)):
            title = "Invalid inputs detected"
            message = "Enter a non-zero positive value to proceed with the proportional damping configuration."
            PrintMessageInput([error_title, title, message])
            return

        data = {
            "speed_of_sound_factor": speed_of_sound_factor,
            "fluid_density_factor": fluid_density_factor,
        }

        for volume_id in volume_ids:
            self.properties._set_property("proportional_damping", data, volume=volume_id)

        self.actions_to_finalize(close_window)

    def remove_callback(self):
        selected_items = self.treeWidget_proportional_damping.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            volume_id = int(item.text(0))
            self.properties._remove_volume_property("proportional_damping", volume_id)

        self.clear_line_edit_selection_id()
        self.treeWidget_proportional_damping.clearSelection()

        app().main_window.selection.clear_selection()
        self.actions_to_finalize()

    def reset_callback(self):

        title = "Proportional damping reset"
        message = "Would you like to remove the proportional damping effects?"

        buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            self.properties._reset_property("proportional_damping")
            self.actions_to_finalize()

    def tab_event_callback(self):
        list_tab = self.tabWidget_main.currentIndex() == SetupTabType.LIST
        self.pushButton_apply.setDisabled(list_tab)
        self.pushButton_apply_and_close.setDisabled(list_tab)
        self.lineEdit_selection_id.setDisabled(list_tab)
        self.comboBox_attribution_type.setDisabled(list_tab)

    def on_click_item(self, item):
        selected_items = self.treeWidget_proportional_damping.selectedItems()
        if not selected_items:
            return

        volume_ids = []
        for item in selected_items:
            volume_ids.append(int(item.text(0)))

        if not volume_ids:
            return

        app().main_window.selection.set_geometry_selection(volumes=volume_ids)

    def on_doubleclick_item(self, item):
        self.on_click_item(item)
          
    def clear_line_edit_selection_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")

    def load_model_info(self):
        self.treeWidget_proportional_damping.clear()

        for (property, volume_id), data in self.properties.volume_properties.items():
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
        for (property, _) in self.properties.volume_properties:
            if property != "proportional_damping":
                continue

            self.tabWidget_main.setTabVisible(SetupTabType.LIST, True)
            return

        self.tabWidget_main.setTabVisible(SetupTabType.LIST, False)
        self.tabWidget_main.setCurrentIndex(SetupTabType.SETUP)

    def group_assistant_callback(self):
        if self.group_assistant is None:
            self.group_assistant = GroupingAssistantInputs(selector_mode=True)
            self.group_assistant.exec()
            self.group_assistant = None
            return

        self.group_assistant.raise_()
        self.group_assistant.activateWindow()

    def actions_to_finalize(self, close_window: bool = False):

        self.load_model_info()
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

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        if isinstance(self.group_assistant, QDialog):
            self.group_assistant.close()

        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        app().main_window.selection.volume_selection_mode = False
        return super().closeEvent(a0)