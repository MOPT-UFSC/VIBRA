from PyQt5.QtWidgets import QComboBox, QDialog, QDoubleSpinBox, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

from pathlib import Path
import numpy as np

# fmt: off

window_title_1 = "Error"
window_title_2 = "Warning"

class SetPorousMaterialModel(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/set_porous_material_model.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.project = app().main_window.project
        self.model = self.project.model
        self.properties = self.model.properties

        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

        self.load_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set porous material model")

    def _initialize(self):
        self.keep_window_open = True
        self.material_model_data = dict()

    def _load_icons(self):
        self.icon = app().main_window.vibra_icon

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type : QComboBox

        # QDoubleSpinBox

        self.doubleSpinBox_C1_DB : QDoubleSpinBox
        self.doubleSpinBox_C2_DB : QDoubleSpinBox
        self.doubleSpinBox_C3_DB : QDoubleSpinBox
        self.doubleSpinBox_C4_DB : QDoubleSpinBox
        self.doubleSpinBox_C5_DB : QDoubleSpinBox
        self.doubleSpinBox_C6_DB : QDoubleSpinBox
        self.doubleSpinBox_C7_DB : QDoubleSpinBox
        self.doubleSpinBox_C8_DB : QDoubleSpinBox
        self.doubleSpinBox_flow_resistivity_DB : QDoubleSpinBox

        self.doubleSpinBox_C1_DBM : QDoubleSpinBox
        self.doubleSpinBox_C2_DBM : QDoubleSpinBox
        self.doubleSpinBox_C3_DBM : QDoubleSpinBox
        self.doubleSpinBox_C4_DBM : QDoubleSpinBox
        self.doubleSpinBox_C5_DBM : QDoubleSpinBox
        self.doubleSpinBox_C6_DBM : QDoubleSpinBox
        self.doubleSpinBox_C7_DBM : QDoubleSpinBox
        self.doubleSpinBox_C8_DBM : QDoubleSpinBox
        self.doubleSpinBox_flow_resistivity_DBM : QDoubleSpinBox

        self.doubleSpinBox_porosity_JCA : QDoubleSpinBox
        self.doubleSpinBox_tortuosity_JCA : QDoubleSpinBox
        self.doubleSpinBox_flow_resistivity_JCA : QDoubleSpinBox

        self.doubleSpinBox_porosity_JCAL : QDoubleSpinBox
        self.doubleSpinBox_tortuosity_JCAL : QDoubleSpinBox
        self.doubleSpinBox_flow_resistivity_JCAL : QDoubleSpinBox

        # QLineEdit
        self.lineEdit_selected_id : QLineEdit
        self.lineEdit_thermal_characteristic_length_JCA : QLineEdit
        self.lineEdit_viscous_characteristic_length_JCA : QLineEdit
        self.lineEdit_thermal_characteristic_length_JCAL : QLineEdit
        self.lineEdit_viscous_characteristic_length_JCAL : QLineEdit

        # QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton

        # QTabWidget
        self.tabWidget_main : QTabWidget

        # QTreeWidget
        self.treeWidget_porous_material_model : QTreeWidget

    def _create_connections(self):

        self.comboBox_attribution_type.currentIndexChanged.connect(self.update_attribution_type)
        self.pushButton_remove.clicked.connect(self.remove_porous_material_model)
        self.pushButton_reset.clicked.connect(self.reset_porous_material_model)
        #
        self.tabWidget_main.currentChanged.connect(self.tabEvent_porous_material_model)
        #
        self.treeWidget_porous_material_model.itemClicked.connect(self.on_click_item)
        self.treeWidget_porous_material_model.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.pushButton_confirm.clicked.connect(self.attribute_porous_material_to_selected_bodies)
        #
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)
        #
        self.update_attribution_type()

    def remove_porous_material_model(self):
        if self.lineEdit_selected_id.text() != "":
            volume_id = int(self.lineEdit_selected_id.text())
            self.properties._remove_volume_property("porous_material_model", volume_id)
            app().main_window.file.write_model_properties_in_file()
            self.load_info()

    def reset_porous_material_model(self):

        volume_ids = list()
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "porous_material_model":
                volume_ids.append(volume_id)

        if volume_ids:

            self.hide()

            title = f"Porous material model resetting"
            message = "Would you like to remove the porous material model effects?"

            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:

                for volume_id in volume_ids:
                    self.properties._remove_volume_property("porous_material_model", volume_id)

                app().main_window.file.write_model_properties_in_file()
                self.close()

    def tabEvent_porous_material_model(self):

        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == 4:
            self.lineEdit_selected_id.setText("")
            self.lineEdit_selected_id.setDisabled(True)
            self.comboBox_attribution_type.setDisabled(True)

        else:

            self.comboBox_attribution_type.setDisabled(False)
            if self.comboBox_attribution_type.currentIndex() == 0:
                return

            self.lineEdit_selected_id.setDisabled(False)

    def on_click_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        # self.remove_bc_from_selection()

    def update_attribution_type(self):
        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selected_id.setText("All bodies")
            self.lineEdit_selected_id.setEnabled(False)
        elif index == 1:
            self.lineEdit_selected_id.setText("")
            self.lineEdit_selected_id.setEnabled(True)
        # self.comboBox_attribution_type.setCurrentIndex(index)

    def update_tabs_visibility(self):

        volume_with_porous_material_model = list()
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "porous_material_model":
                volume_with_porous_material_model.append(volume_id)

        if volume_with_porous_material_model:
            self.tabWidget_main.setTabVisible(4, True)
        else:
            self.tabWidget_main.setTabVisible(4, False)

    def load_info(self):

        self.treeWidget_porous_material_model.clear()
        self.treeWidget_porous_material_model.setColumnWidth(0, 80)
        self.treeWidget_porous_material_model.setColumnWidth(1, 160)

        for key, data in self.properties.volume_properties.items():

            property, volume_id = key

            if property == "porous_material_model":

                model = data["model"]

                model_inputs = list()
                for key, value in data.items():
                    if key != "model":
                        model_inputs.append(value)

                new = QTreeWidgetItem([str(volume_id), model, str(model_inputs)])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_porous_material_model.addTopLevelItem(new)

        self.update_tabs_visibility()

    def geometry_selection_callback(self, points, lines, faces, volumes):
        """ """
        if volumes:

            if self.comboBox_attribution_type.currentIndex() == 0:
                self.comboBox_attribution_type.setCurrentIndex(1)
                # return

            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selected_id.setText(text)

        elif not any([points, lines, faces]):
            return

    def check_input_volume_id(self, lineEdit, single_ID=False):
        try:

            title = "Invalid entry to the Surface ID"
            message = ""
            tokens = lineEdit.strip().split(",")
            self.volume_ids = self.project.model.mesh.nodes_from_volumes.keys()

            try:
                tokens.remove("")
            except:
                pass

            _size = len(self.volume_ids)
            list_ids = list(map(int, tokens))

            if len(list_ids) == 0:
                message = "An empty input field for the Surface ID has been detected. Please, enter a valid Surface ID to proceed."

            elif len(list_ids) >= 1:
                if single_ID and len(list_ids) > 1:
                    message = "Multiple Selected IDs"
                else:
                    try:
                        for _id in list_ids:
                            if _id not in self.volume_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                                message += f"The input value(s) must be integer(s) number(s) N such that 1 <= N <= {_size}."
                                break
                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                        message += f"The input value(s) must be integer(s) number(s) N such that 1 <= N <= {_size}."
                        message += f"\n\n{str(error_log)}"

        except Exception as log_error:
            message = "Wrong input for the Selected ID's. "
            message += f"\n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([window_title_1, title, message])
            return True, []

        if single_ID:
            return False, list_ids[0]
        else:
            return False, list_ids

    def check_selected_bodies(self):
        lineEdit = self.lineEdit_selected_id.text()
        self.stop, self.volume_ids = self.check_input_volume_id(lineEdit)
        if self.stop:
            self.lineEdit_selected_id.setFocus()
            return True

    def get_Delany_Bazley_model_inputs(self):
        material_model_data = {
                                "model" : "Delany-Bazley",
                                "C1" : self.doubleSpinBox_C1_DB.value(),
                                "C2" : self.doubleSpinBox_C2_DB.value(),
                                "C3" : self.doubleSpinBox_C3_DB.value(),
                                "C4" : self.doubleSpinBox_C4_DB.value(),
                                "C5" : self.doubleSpinBox_C5_DB.value(),
                                "C6" : self.doubleSpinBox_C6_DB.value(),
                                "C7" : self.doubleSpinBox_C7_DB.value(),
                                "C8" : self.doubleSpinBox_C8_DB.value(),
                                "flow_resistivity" : self.doubleSpinBox_flow_resistivity_DB.value()
                               }
        return material_model_data

    def get_Delany_Bazley_Miki_model_inputs(self):
        material_model_data = {
                                "model" : "Delany-Bazley-Miki",
                                "C1" : self.doubleSpinBox_C1_DBM.value(),
                                "C2" : self.doubleSpinBox_C2_DBM.value(),
                                "C3" : self.doubleSpinBox_C3_DBM.value(),
                                "C4" : self.doubleSpinBox_C4_DBM.value(),
                                "C5" : self.doubleSpinBox_C5_DBM.value(),
                                "C6" : self.doubleSpinBox_C6_DBM.value(),
                                "C7" : self.doubleSpinBox_C7_DBM.value(),
                                "C8" : self.doubleSpinBox_C8_DBM.value(),
                                "flow_resistivity" : self.doubleSpinBox_flow_resistivity_DBM.value()
                               }
        return material_model_data

    def get_Jhonson_Champoux_Allard_model_inputs(self):

        lineEdit = self.lineEdit_viscous_characteristic_length_JCA
        vcl = self.check_inputs(lineEdit, "Viscous characteristic length", only_positive=True)
        if self.stop:
            lineEdit.setFocus()
            return dict()

        lineEdit = self.lineEdit_thermal_characteristic_length_JCA
        tcl = self.check_inputs(lineEdit, "Thermal characteristic length", only_positive=True)
        if self.stop:
            lineEdit.setFocus()
            return dict()

        material_model_data = {
                                "model" : "Jhonson-Champoux-Allard",
                                "porosity" : self.doubleSpinBox_porosity_JCA.value(),
                                "tortuosity" : self.doubleSpinBox_tortuosity_JCA.value(),
                                "thermal_characteristic_length" : tcl,
                                "viscous_characteristic_length" : vcl,
                                "flow_resistivity" : self.doubleSpinBox_flow_resistivity_JCA.value()
                               }

        return material_model_data

    def get_Jhonson_Champoux_Allard_Lafarge_model_inputs(self):

        lineEdit = self.lineEdit_viscous_characteristic_length_JCAL
        vcl = self.check_inputs(lineEdit, "Viscous characteristic length", only_positive=True)
        if self.stop:
            lineEdit.setFocus()
            return dict()

        lineEdit = self.lineEdit_thermal_characteristic_length_JCAL
        tcl = self.check_inputs(lineEdit, "Thermal characteristic length", only_positive=True)
        if self.stop:
            lineEdit.setFocus()
            return dict()

        material_model_data = {
                                "model" : "Jhonson-Champoux-Allard-Lafarge",
                                "porosity" : self.doubleSpinBox_porosity_JCAL.value(),
                                "tortuosity" : self.doubleSpinBox_tortuosity_JCAL.value(),
                                "thermal_characteristic_length" : tcl,
                                "viscous_characteristic_length" : vcl,
                                "flow_resistivity" : self.doubleSpinBox_flow_resistivity_JCAL.value()
                               }

        return material_model_data

    def attribute_porous_material_to_selected_bodies(self):

        index = self.tabWidget_main.currentIndex()
        if index == 0:
            model_data = self.get_Delany_Bazley_model_inputs()
        elif index == 1:
            model_data = self.get_Delany_Bazley_Miki_model_inputs()
        elif index == 2:
            model_data = self.get_Jhonson_Champoux_Allard_model_inputs()
        elif index == 3:
            model_data = self.get_Jhonson_Champoux_Allard_Lafarge_model_inputs()
        else:
            return
        
        if model_data:

            if self.comboBox_attribution_type.currentIndex():
                if self.check_selected_bodies():
                    return
                volume_ids = self.volume_ids

            else:
                volume_ids = list(self.project.model.mesh.nodes_from_volumes.keys())

            for volume_id in volume_ids:
                # surfaces_from_volume = self.project.model.mesh.surfaces_from_volumes[volume_id]
                self.project.set_porous_material_model(model_data, volume=volume_id)
            
            app().main_window.file.write_model_properties_in_file()

            print(f"The porous material model '{model_data['model']}' has been attributed to the volumes {volume_ids}")
            self.close()

    def check_inputs(self, lineEdit, label, only_positive=False, zero_included=True, _float=True):

        self.stop = False
        message = ""

        title = "Invalid input at dissipation model"
        input_str = lineEdit.text()

        if input_str != "":

            input_str.replace(",", ".")

            try:
                if _float:
                    out = float(input_str)
                else:
                    out = int(input_str)

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
            self.stop = True
            return None
        return out

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_porous_material_to_selected_bodies()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)
    
# fmt: on