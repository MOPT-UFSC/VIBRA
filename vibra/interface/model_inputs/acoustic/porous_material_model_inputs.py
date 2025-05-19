# fmt: off
from PySide6.QtWidgets import QComboBox, QDialog, QDoubleSpinBox, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.ui_generated.model.setup.acoustic.porous_material_model_inputs_ui import PorousMaterialModelInputs_UI

from vibra.interface.model_inputs.acoustic.fluid.simplified_fluid_inputs import SimplifiedFluidInputs
from vibra.interface.model_inputs.acoustic.show_porous_material_model_equations import ShowPorousMaterialModelEquations
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

from vibra.engine.properties.fluid import Fluid
from vibra.engine.dissipation_models.porous_materials_models import PorousMaterialModels

import warnings
import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class PorousMaterialModelInputs(PorousMaterialModelInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.action_model_workspace_callback()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._create_connections()

        self.load_info()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Porous material model")

    def _initialize(self):
        self.selected_fluid = None
        self.auxiliar_dialog = None
        self.update_tabs = True
        self.keep_window_open = True
        self.material_model_data = dict()

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.update_attribution_type)
        self.comboBox_plot_type.currentIndexChanged.connect(self.plot_type_callback)
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.attribute_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        self.pushButton_DB_equations.clicked.connect(self.show_equations_for_DBM_callback)
        self.pushButton_DBM_equations.clicked.connect(self.show_equations_for_DBM_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tabEvent_porous_material_model)
        #
        self.treeWidget_porous_material_model.itemClicked.connect(self.on_click_item)
        self.treeWidget_porous_material_model.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.update_attribution_type()
        self.update_plot_buttons_access()

    def actions_to_finalize(self):
        app().main_window.update_symbols()
    
    def geometry_selection_callback(self):

        volumes = self.main_window.selected_geometry_volumes

        if volumes:

            if self.comboBox_attribution_type.currentIndex() == 0:
                self.comboBox_attribution_type.setCurrentIndex(1)
                # return

            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selection_id.setText(text)

            if len(volumes) == 1 and self.update_tabs:
                volume_id = list(volumes)[0]
                pm_data = self.properties._get_property("porous_material_model", volume=volume_id)
                if pm_data is None:
                    return

                self.load_porous_material_model_inputs(pm_data)

    def load_porous_material_model_inputs(self, pm_data: dict):

        pm_model = pm_data.get("model")

        if pm_model == "Delany-Bazley":

            self.tabWidget_main.setCurrentIndex(0)
            self.doubleSpinBox_C1_DB.setValue(pm_data["C1"])
            self.doubleSpinBox_C2_DB.setValue(pm_data["C2"])
            self.doubleSpinBox_C3_DB.setValue(pm_data["C3"])
            self.doubleSpinBox_C4_DB.setValue(pm_data["C4"])
            self.doubleSpinBox_C5_DB.setValue(pm_data["C5"])
            self.doubleSpinBox_C6_DB.setValue(pm_data["C6"])
            self.doubleSpinBox_C7_DB.setValue(pm_data["C7"])
            self.doubleSpinBox_C8_DB.setValue(pm_data["C8"])
            self.doubleSpinBox_flow_resistivity_DB.setValue(pm_data["flow_resistivity"])       

        elif pm_model == "Delany-Bazley-Miki":

            self.tabWidget_main.setCurrentIndex(1)
            self.doubleSpinBox_C1_DBM.setValue(pm_data["C1"])
            self.doubleSpinBox_C2_DBM.setValue(pm_data["C2"])
            self.doubleSpinBox_C3_DBM.setValue(pm_data["C3"])
            self.doubleSpinBox_C4_DBM.setValue(pm_data["C4"])
            self.doubleSpinBox_C5_DBM.setValue(pm_data["C5"])
            self.doubleSpinBox_C6_DBM.setValue(pm_data["C6"])
            self.doubleSpinBox_C7_DBM.setValue(pm_data["C7"])
            self.doubleSpinBox_C8_DBM.setValue(pm_data["C8"])
            self.doubleSpinBox_flow_resistivity_DB.setValue(pm_data["flow_resistivity"])

        elif pm_model in ["Jhonson-Champoux-Allard", ""]:

            self.tabWidget_main.setCurrentIndex(2)
            self.doubleSpinBox_porosity_JCA.setValue(pm_data["porosity"])
            self.doubleSpinBox_tortuosity_JCA.setValue(pm_data["tortuosity"])
            self.lineEdit_thermal_characteristic_length_JCA.setText(pm_data["thermal_characteristic_length"])
            self.lineEdit_viscous_characteristic_length_JCA.setText(pm_data["viscous_characteristic_length"])
            self.doubleSpinBox_flow_resistivity_JCA.setValue(pm_data["flow_resistivity"])

        elif pm_model == "Jhonson-Champoux-Allard-Lafarge":

            self.tabWidget_main.setCurrentIndex(3)
            self.doubleSpinBox_porosity_JCAL.setValue(pm_data["porosity"])
            self.doubleSpinBox_tortuosity_JCAL.setValue(pm_data["tortuosity"])
            self.lineEdit_thermal_characteristic_length_JCAL.setText(pm_data["thermal_characteristic_length"])
            self.lineEdit_viscous_characteristic_length_JCAL.setText(pm_data["viscous_characteristic_length"])
            self.doubleSpinBox_flow_resistivity_JCAL.setValue(pm_data["flow_resistivity"])

    def show_equations_for_DBM_callback(self):
        self.auxiliar_dialog = ShowPorousMaterialModelEquations()

    def update_plot_buttons_access(self):
        state = self.selected_fluid is None
        self.comboBox_plot_type.setDisabled(state)
        self.pushButton_plot_data.setDisabled(state)
        self.plot_type_callback()

    def plot_type_callback(self):
        if self.comboBox_plot_type.currentIndex() < 2:
            self.doubleSpinBox_porous_material_depth.setDisabled(True)
        else:
            self.doubleSpinBox_porous_material_depth.setDisabled(False)

    def remove_callback(self):
        if self.lineEdit_selection_id.text() != "":
            volume_id = int(self.lineEdit_selection_id.text())
            self.properties._remove_volume_property("porous_material_model", volume_id)
            app().file.write_model_properties_in_file()
            self.load_info()
            self.actions_to_finalize()

    def reset_callback(self):

        volume_ids = list()
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "porous_material_model":
                volume_ids.append(volume_id)

        if volume_ids:

            self.hide()

            title = "Porous material model resetting"
            message = "Would you like to remove the porous material effects from the model?"

            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:

                for volume_id in volume_ids:
                    self.properties._remove_volume_property("porous_material_model", volume_id)

                app().file.write_model_properties_in_file()
                self.actions_to_finalize()
                self.close()

    def tabEvent_porous_material_model(self):

        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == 4:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.comboBox_attribution_type.setDisabled(True)

        else:

            self.comboBox_attribution_type.setDisabled(False)
            if self.comboBox_attribution_type.currentIndex() == 0:
                return

            self.lineEdit_selection_id.setDisabled(False)

    def on_click_item(self, item):

        try:
            str_id = item.text(0)
            volume_id = int(str_id)
            self.lineEdit_selection_id.setText(str_id)
            self.update_tabs = False
            app().main_window.set_geometry_selection(volumes=[volume_id])
            self.update_tabs = True

        except:
            self.lineEdit_selection_id.setText("")

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def update_attribution_type(self):
        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selection_id.setText("All bodies")
            self.lineEdit_selection_id.setEnabled(False)
        elif index == 1:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setEnabled(True)
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

    # def check_selected_bodies(self):
    #     str_selection_ids = self.lineEdit_selection_id.text()
    #     volume_ids = self.mesh.check_selected_ids(str_selection_ids, selection="volumes")
    #     if volume_ids is None:
    #         self.lineEdit_selection_id.setFocus()
    #         return True

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

    def attribute_callback(self):

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

        attribute_type = self.comboBox_attribution_type.currentIndex()
        if attribute_type in [0, 1]:
            
            volume_ids = list()
            if attribute_type == 0:
                if "volumes" in self.mesh.geometry_information.keys():
                    volume_ids = self.mesh.geometry_information["volumes"]

            elif attribute_type == 1:

                input_ids = self.lineEdit_selection_id.text()
                volume_ids, error_data = self.mesh.check_selected_ids(
                                                                      input_ids, 
                                                                      selection = "volumes", 
                                                                      single_id = False,
                                                                      )

                if error_data is not None:
                    self.hide()
                    self.lineEdit_selection_id.setFocus()
                    PrintMessageInput(error_data)
                    return True

            for volume_id in volume_ids:
                self.properties._set_property("porous_material_model", model_data, volume=volume_id)

            app().file.write_model_properties_in_file()
            self.actions_to_finalize()

            print(f"The porous material model '{model_data['model']}' has been attributed to the volumes {volume_ids}")
            self.load_info()

    def check_inputs(self, lineEdit, label, only_positive=False, zero_included=True, _float=True):

        self.stop = False
        message = ""

        title = "Invalid input at dissipation model"
        input_str = lineEdit.text()

        if input_str != "":

            input_str = input_str.replace(",", ".")

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

    # Plot viscous-thermal effective properties

    def get_fluid_callback(self):
        self.hide()
        self.fluid_dialog = SimplifiedFluidInputs()
        self.fluid_dialog.fluid_widget.pushButton_attribute.setText("Select fluid")
        self.fluid_dialog.pushButton_attribute.clicked.connect(self.get_selected_fluid)
        self.fluid_dialog.exec()
        self.main_window.set_input_widget(self)

    def get_selected_fluid(self):
        self.selected_fluid = self.fluid_dialog.get_selected_fluid()
        if isinstance(self.selected_fluid, Fluid):
            self.fluid_dialog.close()
            self.update_plot_buttons_access()
            self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
            self.lineEdit_fluid_density.setText(f"{self.selected_fluid.fluid_density}")
            self.lineEdit_speed_of_sound.setText(f"{self.selected_fluid.speed_of_sound}")

    def get_effective_properties(self, fluid: Fluid):

        warnings.filterwarnings('ignore')

        frequencies = None
        analysis_setup = app().project.analysis_setup
        if isinstance(analysis_setup, dict):
            frequencies = analysis_setup.get("frequencies", None)

        if frequencies is None:
            df = 5
            f_min = 5
            f_max = 1400
            frequencies = np.arange(f_min, f_max+df, df)

        if frequencies[0] == 0:
            freq = frequencies[1:]
        else:
            freq = frequencies

        omega = 2 * np.pi * freq

        model = PorousMaterialModels(self.model)

        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == 0:
            pm_data = self.get_Delany_Bazley_model_inputs()
            rho_eff, C_eff = model.get_Delany_Bazley_Miki_effective_properties(omega, fluid, pm_data)

        elif tab_index == 1:
            pm_data = self.get_Delany_Bazley_Miki_model_inputs()
            rho_eff, C_eff = model.get_Delany_Bazley_Miki_effective_properties(omega, fluid, pm_data)

        elif tab_index == 2:
            pm_data = self.get_Jhonson_Champoux_Allard_model_inputs()
            rho_eff, C_eff = model.get_JCA_effective_properties(omega, fluid, pm_data)

        elif tab_index == 3:
            pm_data = self.get_Jhonson_Champoux_Allard_Lafarge_model_inputs()
            rho_eff, C_eff = model.get_JCAL_effective_properties(omega, fluid, pm_data)

        k_cr = omega / C_eff

        return freq, rho_eff, C_eff, k_cr

    def get_porous_material_model(self):
        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == 0:
            return "Delany-Bazley"
        elif tab_index == 1:
            return "Delany-Bazley-Miki"
        elif tab_index == 2:
            return "Jhonson-Champoux-Allard"
        elif tab_index == 3:
            return "Jhonson-Champoux-Allard-Lafarge"

    def plot_data_callback(self):
        plot_key = self.comboBox_plot_type.currentIndex()
        if plot_key == 0:
            self.plot_effective_fluid_density()
        elif plot_key == 1:
            self.plot_effective_speed_of_sound()
        elif plot_key == 2:
            self.plot_surface_impedance()
        else:
            self.plot_absorption_coefficient()

    def plot_effective_fluid_density(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        freq, rho_eff, _, _ = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        pm_model = self.get_porous_material_model()
        self.plot_data(freq, rho_eff, "effective fluid density", pm_model)

    def plot_effective_speed_of_sound(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        freq, _, C_eff, _ = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        pm_model = self.get_porous_material_model()
        self.plot_data(freq, C_eff, "effective speed of sound", pm_model)

    def plot_surface_impedance(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        h = self.doubleSpinBox_porous_material_depth.value()
        Z_0 = self.selected_fluid.speed_of_sound * self.selected_fluid.fluid_density

        freq, rho_eff, C_eff, k_cr = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        Z_pm = rho_eff * C_eff
        Z_s = Z_pm * (1 / np.tanh(k_cr * h))
        Z_norm = Z_s / Z_0

        pm_model = self.get_porous_material_model()
        self.plot_data(freq, Z_norm, "normalized surface impedance", pm_model)

    def plot_absorption_coefficient(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        h = self.doubleSpinBox_porous_material_depth.value()
        Z_0 = self.selected_fluid.speed_of_sound * self.selected_fluid.fluid_density

        freq, rho_eff, C_eff, k_cr = self.get_effective_properties(self.selected_fluid)

        Z_pm = rho_eff * C_eff
        Z_s = Z_pm * (1 / np.tanh(k_cr * h))

        R_r = (Z_s - Z_0) / (Z_s + Z_0)
        alpha_n = 1 - np.abs(R_r)**2

        if freq is None:
            return

        pm_model = self.get_porous_material_model()
        self.plot_data(freq, alpha_n, "absorption coefficient", pm_model)

    def join_model_data(self, x_data, y_data, label: str, pm_label: str):

        self.hide()
        self.data_to_plot = dict()

        if label == "effective fluid density":
            unit_label = "kg/m³"
            y_label = "Effective fluid density"

        elif label == "effective speed of sound":
            unit_label = "m/s"
            y_label = "Effective speed of sound"

        elif label == "normalized surface impedance":
            unit_label = "--"
            y_label = "Normalized surface impedance"

        else:
            unit_label = "--"
            y_label = "Absorption coeffient"

        legend_label = label
        title = f"{pm_label} Porous Material Curve"

        key = (label.replace(" ", "_"), None)

        self.data_to_plot[key] = { 
                                    "x_data" : x_data,
                                    "y_data" : y_data,
                                    "x_label" : "Frequency [Hz]",
                                    "y_label" : y_label,
                                    "title" : title,
                                    "data_type" : "porous material data",
                                    "legend" : legend_label,
                                    "unit" : unit_label,
                                    "color" : [0,0,1],
                                    "linestyle" : "-"
                                   }

    def plot_data(self, x_data, y_data, label, pm_label):
        self.join_model_data(x_data, y_data, label, pm_label)
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.data_to_plot)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        self.keep_window_open = False
        warnings.filterwarnings('default')

        if isinstance(self.auxiliar_dialog, QDialog):
            self.auxiliar_dialog.close()

        return super().closeEvent(a0)

# fmt: on