# fmt: off

from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.ui_generated.model.setup.acoustic.proportional_damping_inputs_ui import ProportionalDampingInputs_UI
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class ProportionalDampingInput(ProportionalDampingInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._create_connections()
        self.load_info()

        self.geometry_selection_callback()
        self.attribution_type_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.keep_window_open = True

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_confirm.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tabEvent_dissipation_model)
        #
        self.treeWidget_proportional_damping.itemClicked.connect(self.on_click_item)
        self.treeWidget_proportional_damping.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)

    def attribution_type_callback(self):

        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selection_id.setText("All bodies")
        elif index == 1:
            self.lineEdit_selection_id.setText("")

        self.lineEdit_selection_id.setEnabled(bool(index))

    def geometry_selection_callback(self):

        volumes = app().main_window.selected_geometry_volumes

        if volumes:

            volume_ids = [int(vol_id) for vol_id in volumes]

            if self.comboBox_attribution_type.currentIndex() == 0:
                self.comboBox_attribution_type.setCurrentIndex(1)

            text = ", ".join([str(i) for i in volume_ids])
            self.lineEdit_selection_id.setText(text)

            if len(volume_ids) == 1:
                p_data = self.properties._get_property("proportional_damping", volume=volume_ids[0])
                if p_data is None:
                    return
                
                self.load_dissipation_model_data(p_data)

    def load_dissipation_model_data(self, data: dict):

        self.lineEdit_speed_of_sound_complex_factor.setText("")
        self.lineEdit_fluid_density_complex_factor.setText("")

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
                message = "Dear user, you have typed and invalid value at the \n"
                message += f"{label} input field.\n\n"
                message += str(_err)

        else:
            if zero_included:
                return float(0)
            else:
                message = f"Insert some value at the {label} input field."

        if message != "":
            PrintMessageInput([window_title_1, title, message])
            return None

        return out

    def attribute_callback(self):

        attribute_type = self.comboBox_attribution_type.currentIndex()
            
        volume_ids = list()
        if attribute_type == 0:
            if "volumes" in self.mesh.geometry_information.keys():
                volume_ids = self.mesh.geometry_information["volumes"]

        elif attribute_type == 1:
            input_ids = self.lineEdit_selection_id.text()
            volume_ids, error_data = self.mesh.check_selected_ids(
                                                                    input_ids, 
                                                                    selection = "volumes", 
                                                                    single_id = False
                                                                    )

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
                "speed_of_sound_factor" : speed_of_sound_factor,
                "fluid_density_factor" : fluid_density_factor,
                }

        for volume_id in volume_ids:
            self.properties._set_property("proportional_damping", data, volume=volume_id)

        self.actions_to_finalize()

    def remove_callback(self):

        if self.lineEdit_selection_id.text() == "":
            return

        volume_id = int(self.lineEdit_selection_id.text())
        self.properties._remove_volume_property("proportional_damping", volume_id)
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

    def tabEvent_dissipation_model(self):
        tab_index = self.tabWidget_main.currentIndex()
        self.comboBox_attribution_type.setDisabled(bool(tab_index))
        if tab_index == 1:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)

    def on_click_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))
        # self.remove_bc_from_selection()

    def update_tabs_visibility(self):

        volume_with_dissipation_model = list()
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "proportional_damping":
                volume_with_dissipation_model.append(volume_id)

        if volume_with_dissipation_model:
            self.tabWidget_main.setTabVisible(1, True)
        else:
            self.tabWidget_main.setTabVisible(1, False)

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

    def actions_to_finalize(self):
        self.load_info()
        app().main_window.update_info_text()
        app().file.write_model_properties_in_file()
        app().main_window.update_symbols()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
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