# fmt: off
from PySide6.QtWidgets import QDialog, QTableWidgetItem, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.formatters.icons import change_icon_color_for_widgets
from vibra.interface.ui_generated.model.setup.acoustic.porous_material_model_inputs_ui import PorousMaterialModelInputs_UI

from vibra.interface.model_inputs.acoustic.fluid.simplified_fluid_inputs import SimplifiedFluidInputs
from vibra.interface.model_inputs.acoustic.show_porous_material_model_equations import ShowPorousMaterialModelEquations
from vibra.interface.model_inputs.acoustic.delany_bazley_data import DelanyBazleyData
from vibra.interface.model_inputs.acoustic.jca_data import JCAData
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

from vibra.engine.properties.fluid import Fluid
from vibra.engine.dissipation_models.porous_materials_models import PorousMaterialModels

import warnings
import numpy as np
from collections import defaultdict
from enum import IntEnum
from typing import Dict, List

window_title_1 = "Error"
window_title_2 = "Warning"


class PMModels(IntEnum):
    DELANY_BAZLEY = 0
    DELANY_BAZLEY_MIKI = 1
    JCA = 2
    JCAL = 3


class PorousMaterialModelInputs(PorousMaterialModelInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.action_model_workspace_callback()

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._configure_widgets()
        self._create_connections()
        self._paint_icons()
        self.load_info()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _configure_widgets(self):
        for i, width in enumerate([120, 160]):
            self.treeWidget_porous_material_model.setColumnWidth(i, width)

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
        self.tabWidget_main.currentChanged.connect(self.tab_event_porous_material_model)
        #
        self.tableWidget_delany.cellChanged.connect(lambda row, column: self.cell_changed_callback(row, column, model="delany"))
        self.tableWidget_jca.cellChanged.connect(lambda row, column: self.cell_changed_callback(row, column, model="jca"))
        #
        self.treeWidget_porous_material_model.itemClicked.connect(self.on_click_item)
        self.treeWidget_porous_material_model.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        app().main_window.theme_changed.connect(self._paint_icons)
        #
        self.update_attribution_type()
        self.update_plot_buttons_access()
    
    def _paint_icons(self):
        icon_color = None
        theme = app().config.user_preferences.interface_theme
        from vibra import LIGHT_ICON_COLOR, DARK_ICON_COLOR
        if theme == "dark":
            icon_color = DARK_ICON_COLOR.to_qt()
        else:
            icon_color = LIGHT_ICON_COLOR.to_qt()

        widgets = [self.pushButton_DB_equations, self.pushButton_DBM_equations]
        change_icon_color_for_widgets(widgets, icon_color)

    def actions_to_finalize(self):
        app().main_window.update_symbols()
    
    def geometry_selection_callback(self):

        volumes = app().main_window.selected_geometry_volumes

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
            self.lineEdit_thermal_characteristic_length_JCA.setText(str(pm_data["thermal_characteristic_length"]))
            self.lineEdit_viscous_characteristic_length_JCA.setText(str(pm_data["viscous_characteristic_length"]))
            self.doubleSpinBox_flow_resistivity_JCA.setValue(pm_data["flow_resistivity"])

        elif pm_model == "Jhonson-Champoux-Allard-Lafarge":

            self.tabWidget_main.setCurrentIndex(3)
            self.doubleSpinBox_porosity_JCAL.setValue(pm_data["porosity"])
            self.doubleSpinBox_tortuosity_JCAL.setValue(pm_data["tortuosity"])
            self.lineEdit_thermal_characteristic_length_JCAL.setText(str(pm_data["thermal_characteristic_length"]))
            self.lineEdit_viscous_characteristic_length_JCAL.setText(str(pm_data["viscous_characteristic_length"]))
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
        selected_items = self.treeWidget_porous_material_model.selectedItems()

        if not selected_items:
            return
        
        selected_item = selected_items[0]

        volume_id = int(selected_item.text(0))

        self.properties._remove_volume_property("porous_material_model", volume_id)
        app().file.write_model_properties_in_file()

        self.load_info()
        self.actions_to_finalize()

        if len(self.map_model_id_to_model) > 0:
            self.tabWidget_main.setCurrentIndex(5)

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

    def tab_event_porous_material_model(self):

        pm_tab = self.tabWidget_main.currentIndex() <= 3

        self.frame_plot_setup.setVisible(pm_tab)
        self.frame_plot_buttons.setVisible(pm_tab)

        if pm_tab:
            self.comboBox_attribution_type.setDisabled(False)
            if self.comboBox_attribution_type.currentIndex() == 0:
                return

            self.lineEdit_selection_id.setDisabled(False)

        else:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.comboBox_attribution_type.setDisabled(True)

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

    def cell_changed_callback(self, row, column, model):        
        item = None
        model_id = None
        parameter_position = row - 2

        if model == "delany":
            item = self.tableWidget_delany.item(row, column)
            model_id = int(self.tableWidget_delany.item(0, column).text())
        else:
            item = self.tableWidget_jca.item(row, column)
            model_id = int(self.tableWidget_jca.item(0, column).text())

        new_parameter_value = None
        value_error = False
        
        try:
            new_parameter_value = float(item.text())
        except:
            value_error = True
        
        parameters_position = self.map_model_id_to_model[model_id].get_parameters_position()
        model = self.map_model_id_to_model[model_id]

        if value_error:
            new_parameter_value = getattr(model, parameters_position[parameter_position])
            item.setText(str(new_parameter_value))
        else:
            setattr(model, parameters_position[parameter_position], new_parameter_value)

            volumes = self.map_model_id_to_volumes[model_id]

            for volume in volumes:
                self.properties._set_property("porous_material_model", model.get_data(), volume=volume)
            
            app().file.write_model_properties_in_file()
                                                  
    def update_attribution_type(self):
        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selection_id.setText("All bodies")
            self.lineEdit_selection_id.setEnabled(False)
        elif index == 1:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setEnabled(True)
        # self.comboBox_attribution_type.setCurrentIndex(index)

    def map_existing_porous_materials(self):
        self.map_model_id_to_volumes: Dict[int, List[str]] = defaultdict(list)
        self.map_model_id_to_model: Dict[int, DelanyBazleyData|JCAData] = dict()

        models = list()
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key

            if property != "porous_material_model":
                continue
        
                
            try:
                model = None
                if data["model"] in ["Delany-Bazley", "Delany-Bazley-Miki"]:
                    model = DelanyBazleyData.set_data(data)
                else:
                    model = JCAData.set_data(data)
                
                if model not in models:
                    models.append(model)

                model_id = models.index(model) + 1
                self.map_model_id_to_model[model_id] = model

                if volume_id not in self.map_model_id_to_volumes[model_id]:
                    self.map_model_id_to_volumes[model_id].append(volume_id)

            except:
                    title = "Porous Material Model Error"
                    message = "An error occurred while trying to load the porous material model data "
                    message += "from the project file. The porous material model will be deleted."
                    PrintMessageInput([window_title_1, title, message])

                    self.properties._reset_property("porous_material_model")
                    app().main_window.update_symbols()

                    return

    def load_info(self):
        self.map_existing_porous_materials()

        self.treeWidget_porous_material_model.clear()
        self.update_treeWidget_porous_materials()
        self.configure_tables_and_tabs_widgets()

        delany_counter = 0
        jca_counter = 0

        there_is_delany_model = False
        there_is_jca_model = False

        for _, (model_id, model_data) in enumerate(self.map_model_id_to_model.items()):
            model = model_data.model
            model_data_dict = model_data.get_data()

            model_id_item = QTableWidgetItem(str(model_id))
            model_item = QTableWidgetItem(self.addapt_model_name(model))
            model_id_item.setFlags(Qt.ItemIsSelectable)
            model_item.setFlags(Qt.ItemIsSelectable)
            model_item.setToolTip(model)
        
            if model in ["Delany-Bazley", "Delany-Bazley-Miki"]:
                there_is_delany_model = True

                self.tableWidget_delany.setItem(0, delany_counter, model_id_item)
                self.tableWidget_delany.setItem(1, delany_counter, model_item)

                for k, model_input in enumerate(model_data_dict.values()):

                    if isinstance(model_input, str):
                        continue

                    self.tableWidget_delany.setItem(2+k, delany_counter, QTableWidgetItem(str(model_input)))

                delany_counter += 1

            else:
                there_is_jca_model = True

                self.tableWidget_jca.setItem(0, jca_counter, model_id_item)
                self.tableWidget_jca.setItem(1, jca_counter, model_item)

                for k, model_input in enumerate(model_data_dict.values()):

                    if isinstance(model_input, str):
                        continue

                    self.tableWidget_jca.setItem(2+k, jca_counter, QTableWidgetItem(str(model_input)))

                jca_counter += 1

        if there_is_jca_model:
            self.tabWidget_models.setTabVisible(1, True)
        
        if there_is_delany_model:
            self.tabWidget_models.setTabVisible(0, True)
            self.tabWidget_models.setCurrentIndex(0)

        if there_is_jca_model or there_is_delany_model:
            self.tabWidget_main.setTabVisible(4, True)
            self.tabWidget_main.setTabVisible(5, True)
            self.tabWidget_main.setCurrentIndex(4)
        
        self.update_tableWidget_delany_items()
        self.update_tableWidget_jca_items()
    
    def update_treeWidget_porous_materials(self):
        for model_id, volume_ids in self.map_model_id_to_volumes.items():
            model_data = self.map_model_id_to_model[model_id]

            for volume_id in volume_ids:
                new = QTreeWidgetItem([str(volume_id), self.addapt_model_name(model_data.model), str(model_id)])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_porous_material_model.addTopLevelItem(new)
        
    def configure_tables_and_tabs_widgets(self):
        delany_count = 0
        jca_count = 0

        for model in self.map_model_id_to_model.values():
            if isinstance(model, DelanyBazleyData):
                delany_count += 1
            else:
                jca_count += 1

        self.tableWidget_delany.clearContents()
        self.tableWidget_delany.blockSignals(True)
        self.tableWidget_delany.setRowCount(11)
        self.tableWidget_delany.setColumnCount(delany_count)

        self.tableWidget_jca.clearContents()
        self.tableWidget_jca.blockSignals(True)
        self.tableWidget_jca.setRowCount(7)
        self.tableWidget_jca.setColumnCount(jca_count)

        self.tabWidget_models.setTabVisible(0, False)
        self.tabWidget_models.setTabVisible(1, False)

        self.tabWidget_main.setTabVisible(4, False)
        self.tabWidget_main.setTabVisible(5, False)
    
    def update_tableWidget_delany_items(self):
        for i in range(self.tableWidget_delany.rowCount()):
            for j in range(self.tableWidget_delany.columnCount()):
                item = self.tableWidget_delany.item(i, j)

                if item is None:
                    item = QTableWidgetItem()
                    self.tableWidget_delany.setItem(i, j, item)
                    item.setFlags(Qt.ItemIsSelectable)

                item.setTextAlignment(Qt.AlignCenter)
        
        self.tableWidget_delany.blockSignals(False)
    
    def update_tableWidget_jca_items(self):
        for i in range(self.tableWidget_jca.rowCount()):
            for j in range(self.tableWidget_jca.columnCount()):
                item = self.tableWidget_jca.item(i, j)

                if item is None:
                    item = QTableWidgetItem()
                    self.tableWidget_jca.setItem(i, j, item)
                    item.setFlags(Qt.ItemIsSelectable)

                item.setTextAlignment(Qt.AlignCenter)

        self.tableWidget_jca.blockSignals(False)
    
    def addapt_model_name(self, model:str) -> str:
        if model == "Delany-Bazley":
            return "DB"
        elif model == "Delany-Bazley-Miki":
            return "DBM"
        elif model == "Jhonson-Champoux-Allard":
            return "JCA"
        
        return "JCAL"

    def get_Delany_Bazley_model_data(self) -> DelanyBazleyData:
        return DelanyBazleyData(self.doubleSpinBox_C1_DB.value(), 
                                self.doubleSpinBox_C2_DB.value(), self.doubleSpinBox_C3_DB.value(), 
                                self.doubleSpinBox_C4_DB.value(), self.doubleSpinBox_C5_DB.value(), 
                                self.doubleSpinBox_C6_DB.value(), self.doubleSpinBox_C7_DB.value(), 
                                self.doubleSpinBox_C8_DB.value(), self.doubleSpinBox_flow_resistivity_DB.value(), 
                                "Delany-Bazley",)

    def get_Delany_Bazley_Miki_model_data(self) -> DelanyBazleyData:
        return DelanyBazleyData(self.doubleSpinBox_C1_DBM.value(), 
                                self.doubleSpinBox_C2_DBM.value(), self.doubleSpinBox_C3_DBM.value(), 
                                self.doubleSpinBox_C4_DBM.value(), self.doubleSpinBox_C5_DBM.value(), 
                                self.doubleSpinBox_C6_DBM.value(), self.doubleSpinBox_C7_DBM.value(), 
                                self.doubleSpinBox_C8_DBM.value(), self.doubleSpinBox_flow_resistivity_DBM.value(),
                                "Delany-Bazley-Miki")

    def get_Jhonson_Champoux_Allard_model_data(self) -> JCAData:

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

        return JCAData(self.doubleSpinBox_porosity_JCA.value(),
                      self.doubleSpinBox_tortuosity_JCA.value(), vcl,
                      tcl, self.doubleSpinBox_flow_resistivity_JCA.value(),
                      "Jhonson-Champoux-Allard")

    def get_Jhonson_Champoux_Allard_Lafarge_model_data(self) -> JCAData:

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

        return JCAData(self.doubleSpinBox_porosity_JCAL.value(),
                      self.doubleSpinBox_tortuosity_JCAL.value(), vcl,
                      tcl, self.doubleSpinBox_flow_resistivity_JCAL.value(),
                      "Jhonson-Champoux-Allard-Lafarge")

    def attribute_callback(self):

        index = self.tabWidget_main.currentIndex()
        if index == PMModels.DELANY_BAZLEY:
            model_data = self.get_Delany_Bazley_model_data()
        elif index == PMModels.DELANY_BAZLEY_MIKI:
            model_data = self.get_Delany_Bazley_Miki_model_data()
        elif index == PMModels.JCA:
            model_data = self.get_Jhonson_Champoux_Allard_model_data()
        elif index == PMModels.JCAL:
            model_data = self.get_Jhonson_Champoux_Allard_Lafarge_model_data()
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
                self.properties._set_property("porous_material_model", model_data.get_data(), volume=volume_id)

            app().file.write_model_properties_in_file()
            self.actions_to_finalize()
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
        app().main_window.set_input_widget(self)

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

        if tab_index == PMModels.DELANY_BAZLEY:
            pm_data = self.get_Delany_Bazley_model_data()
            rho_eff, C_eff = model.get_Delany_Bazley_Miki_effective_properties(omega, fluid, pm_data.get_data())

        elif tab_index == PMModels.DELANY_BAZLEY_MIKI:
            pm_data = self.get_Delany_Bazley_Miki_model_data()
            rho_eff, C_eff = model.get_Delany_Bazley_Miki_effective_properties(omega, fluid, pm_data.get_data())

        elif tab_index == PMModels.JCA:
            pm_data = self.get_Jhonson_Champoux_Allard_model_data()
            rho_eff, C_eff = model.get_JCA_effective_properties(omega, fluid, pm_data.get_data())

        elif tab_index == PMModels.JCAL:
            pm_data = self.get_Jhonson_Champoux_Allard_Lafarge_model_data()
            rho_eff, C_eff = model.get_JCAL_effective_properties(omega, fluid, pm_data.get_data())

        else:
            return None, None

        k_cr = omega / C_eff

        return freq, rho_eff, C_eff, k_cr

    def get_porous_material_model(self):
        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == PMModels.DELANY_BAZLEY:
            return "Delany-Bazley"
        elif tab_index == PMModels.DELANY_BAZLEY_MIKI:
            return "Delany-Bazley-Miki"
        elif tab_index == PMModels.JCA:
            return "Jhonson-Champoux-Allard"
        elif tab_index == PMModels.JCAL:
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