from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QTreeWidgetItem
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

from vibra import app
from vibra.interface.ui_generated.model.setup.fluid.set_fluid_composition_input_ui import SetFluidCompositionInput_UI
from vibra.interface.model_inputs.acoustic.fluid.refprop_interface import RefpropInterface
from vibra.interface.model_inputs.acoustic.fluid.load_fluid_composition_inputs import LoadFluidCompositionInputs
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.utils.utils import *

import os
from enum import IntEnum

error_title = "Error"
warning_title = "Warning"


class TemperatureUnit(IntEnum):
    KELVIN = 0
    CELSIUS = 1
    FARENHEIT = 2


class SetFluidCompositionInputs(SetFluidCompositionInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.selected_fluid_to_edit = kwargs.get("selected_fluid_to_edit", None)
        self.state_properties = kwargs.get("state_properties", dict())

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self._config_window()
        self._initialize()
        self._create_connections()
        self._config_widgets()

        if self.state_properties:
            self.check_state_properties(self.state_properties)

        self.update_remainig_composition()
        if self.initialize_refprop_interface():
            return

        if self.selected_fluid_to_edit:
            self.update_selected_fluid()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Vibra")

    def _initialize(self):

        self.fluid_to_row = dict()
        self.fluid_to_composition = dict()
        self.remaining_molar_fraction = 1

        self.selected_row = None
        self.complete = False
        self.keep_window_open = True

        self.selected_fluid = ""
        self.composition_file_path = ""

        # self.unit_temperature = "K"
        # self.unit_pressure = "Pa"

    def initialize_refprop_interface(self):
        self.refprop_interface = RefpropInterface()
        if self.refprop_interface.initialize_REFPROP():
            return True

        self.refprop = self.refprop_interface.refprop
        self.load_default_gases_info(self.refprop_interface.refprop_fluids)

        version = self.refprop_interface.get_REFPROP_version()
        self.setWindowTitle(f"Vibra (REFPROP v{version})")

    def _create_connections(self):
        #
        self.pushButton_add_gas.clicked.connect(self.add_selected_fluid_button_callback)
        self.pushButton_confirm.clicked.connect(self.get_fluid_properties)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_load_composition.clicked.connect(self.load_fluid_composition_callback)
        self.pushButton_remove_gas.clicked.connect(self.remove_selected_gas)
        self.pushButton_reset_fluid.clicked.connect(self.reset_fluid)
        #
        self.tableWidget_new_fluid.cellClicked.connect(self.cell_clicked_on_composition_table)
        self.tableWidget_new_fluid.itemChanged.connect(self.item_changed_callback)
        #
        self.treeWidget_refprop_fluids.itemClicked.connect(self.on_click_item_refprop_fluids)
        self.treeWidget_refprop_fluids.itemDoubleClicked.connect(self.on_double_click_item_refprop_fluids)

    def _config_widgets(self):

        self.label_discharge.setVisible(False)
        self.label_suction.setVisible(False)
        self.label_spacing.setVisible(False)
        #
        self.lineEdit_composition.setFixedHeight(28)
        self.lineEdit_pressure_disch.setVisible(False)
        self.lineEdit_temperature_disch.setVisible(False)

    def check_state_properties(self, state_properties: dict):

        self.comboBox_temperature_units.setDisabled(True)
        self.comboBox_pressure_units.setDisabled(True)
        self.comboBox_temperature_units.setCurrentIndex(0)

        self.reciprocating_machine = state_properties.get("source", None)
        self.check_ideal_gas = state_properties.get("check_ideal_gas", True)

        if self.reciprocating_machine is None:

            pressure = state_properties.get("pressure", None)
            temperature = state_properties.get("temperature", None)

            if isinstance(temperature, (int | float)):
                self.lineEdit_temperature.setText(str(round(temperature, 4)))

            if isinstance(pressure, (int | float)):
                self.lineEdit_pressure.setText(f"{pressure : .8e}")

        else:

            self.label_discharge.setVisible(True)
            self.label_suction.setVisible(True)
            self.label_spacing.setVisible(True)

            self.lineEdit_temperature.setDisabled(True)
            self.lineEdit_pressure.setDisabled(True)

            self.lineEdit_pressure_disch.setVisible(True)
            self.lineEdit_pressure_disch.setDisabled(True)

            self.lineEdit_temperature_disch.setVisible(True)
            self.lineEdit_temperature_disch.setDisabled(True)

            self.connection_type = state_properties['connection_type']
            self.T_suction = state_properties[f'temperature_at_suction']
            self.P_suction = state_properties[f'suction_pressure']

            if self.connection_type == "suction":
                self.lineEdit_pressure_disch.setVisible(False)
                self.lineEdit_temperature_disch.setVisible(False)
                self.label_discharge.setVisible(False)

            if 'suction_pressure' in state_properties.keys():
                self.lineEdit_temperature.setText(f"{self.T_suction : .4f}")
                self.lineEdit_pressure.setText(f"{self.P_suction : .8e}")

            if 'pressure_ratio' in state_properties.keys():
                self.p_ratio =  state_properties['pressure_ratio']
                self.P_discharge = self.p_ratio * self.P_suction

            elif 'discharge_pressure' in state_properties.keys():
                self.P_discharge = state_properties['discharge_pressure']

            self.lineEdit_pressure_disch.setText(f"{self.P_discharge : .8e}")

            if 'temperature_at_discharge' in state_properties.keys():
                self.T_discharge = state_properties[f'temperature_at_discharge']
                self.lineEdit_temperature_disch.setText(f"{self.T_discharge : .4f}")

            else:

                tool_tip = "The temperature at discharge will be "
                tool_tip += "calculated after the fluid definition."

                self.lineEdit_temperature_disch.setText("---")
                self.lineEdit_temperature_disch.setToolTip(tool_tip)

    def update_selected_fluid(self):

        [fluid_name, temperature, pressure, key_mixture, molar_fractions] = self.selected_fluid_to_edit

        fluid_file_names = key_mixture.split(";")
        self.lineEdit_fluid_name.setText(fluid_name)
        self.lineEdit_pressure.setText(str(pressure))
        self.lineEdit_temperature.setText(str(temperature))
        #
        self.comboBox_temperature_units.setCurrentIndex(0)

        for index, fluid_file_name in enumerate(fluid_file_names):
            final_name = self.refprop_interface.fluid_file_to_final_name[fluid_file_name]
            str_molar_fraction = str(round(molar_fractions[index]*100, 6))
            self.fluid_to_composition[final_name] = [str_molar_fraction, 
                                                        molar_fractions[index], 
                                                        fluid_file_name]

        self.load_fluid_composition_info()
        self.update_remainig_composition()

    def add_selected_fluid_button_callback(self):
        self.add_selected_fluid_to_composition_table(self.selected_fluid)

    def add_selected_fluid(self, fluid_name: str, molar_fraction: float):

        fluid_file_name, _, _ = self.refprop_fluids[fluid_name]

        if isinstance(molar_fraction, float):
            self.fluid_to_composition[fluid_name] = [  
                                                    str(molar_fraction), 
                                                    molar_fraction / 100, 
                                                    fluid_file_name
                                                    ]

            if molar_fraction == 0:
                if fluid_name in self.fluid_to_composition.keys():
                    self.fluid_to_composition.pop(fluid_name)

        elif molar_fraction == "":
            self.fluid_to_composition[fluid_name] = list()

        self.update_remainig_composition()

    def update_remainig_composition(self):

        self.remaining_molar_fraction = 1
        for composition_data in self.fluid_to_composition.values():
            if len(composition_data) == 3:
                composition_value = composition_data[1]
                self.remaining_molar_fraction -= composition_value

        _remain = round(100 * self.remaining_molar_fraction, 6)
        if _remain == 0:
            _remain = 0.00

        self.remaining_composition_highlight(_remain)
        if not self.state_properties:
            return
        
        if self.state_properties.get("connection_type", "") == "suction":
            return

        if round(abs(self.remaining_molar_fraction), 6) == 0:
            self.compute_reciprocating_compressor_state_properties()

    def remaining_composition_highlight(self, value: float):
        if value >= 0:
            style_sheet =   """  QLabel{border-radius: 4px; border-color: rgb(100, 100, 100); 
                                        border-style: solid; border-width: 1px; color: rgb(100, 100, 100); 
                                        background-color: rgb(255, 255, 255)}
                            """

        else:
            style_sheet =   """  QLabel{border-radius: 4px; border-color: rgb(250, 10, 10); 
                                        border-style: solid; border-width: 2px; color: rgb(250, 10, 10); 
                                        background-color: rgb(255, 255, 255)}
                            """

        self.label_remaining_composition.setStyleSheet(style_sheet)
        self.label_remaining_composition.setText(str(value))

    def compute_reciprocating_compressor_state_properties(self):

        composition_data = self.get_fluid_composition_data()
        if composition_data is None:
            return
        else:
            fluids_string, molar_fractions = composition_data

        fluid_property, errors = self.refprop_interface.get_specific_fluid_property( 
                                                                                    fluids_string = fluids_string,
                                                                                    molar_fractions = molar_fractions,
                                                                                    property_key = self.refprop_interface.isentropic_label,
                                                                                    temperature_K = self.T_suction,
                                                                                    pressure_Pa = self.P_suction,
                                                                                    )

        if errors:
            return

        k_isen = fluid_property 
        T_disch = (self.T_suction) * (self.p_ratio**((k_isen - 1) / k_isen))
        self.T_discharge = T_disch
        self.lineEdit_temperature_disch.setText(f"{T_disch : .4f}")

    def remove_selected_gas(self):

        if isinstance(self.selected_row, int):

            item = self.tableWidget_new_fluid.item(self.selected_row, 0)

            if item is None:
                return

            selected_fluid = item.text()
            self.tableWidget_new_fluid.removeRow(self.selected_row)

            if selected_fluid in self.fluid_to_composition.keys():
                self.fluid_to_composition.pop(selected_fluid)
                self.update_remainig_composition()

    def reset_fluid(self):

        self.hide()

        title = f"Fluid composition reset"
        message = "Would you like to reset the current fluid composition?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        self.fluid_to_composition.clear()
        self.load_fluid_composition_info()
        self.update_remainig_composition()

    def load_default_gases_info(self, refprop_fluids: dict):

        self.config_table_data()
        self.refprop_fluids = refprop_fluids
        self.treeWidget_refprop_fluids.clear()
        self.treeWidget_refprop_fluids.headerItem().setText(0, "Default fluid library")

        for fluid in self.refprop_fluids.keys():
            new = QTreeWidgetItem([fluid])
            new.setTextAlignment(0, Qt.AlignCenter)
            self.treeWidget_refprop_fluids.addTopLevelItem(new)

    def config_table_data(self):

        header = ['Fluid name', 'Molar fraction [%]']
        
        self.tableWidget_new_fluid.setColumnCount(len(header))
        self.tableWidget_new_fluid.setHorizontalHeaderLabels(header)
        self.tableWidget_new_fluid.setSelectionBehavior(QAbstractItemView.SelectionBehavior(1))
        self.tableWidget_new_fluid.resizeColumnsToContents()

        self.tableWidget_new_fluid.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(0))
        self.tableWidget_new_fluid.horizontalHeader().setStretchLastSection(True)

        for j, width in enumerate([220, 120]):
            self.tableWidget_new_fluid.horizontalHeader().resizeSection(j, width)
            self.tableWidget_new_fluid.horizontalHeaderItem(j).setTextAlignment(Qt.AlignCenter)

    def load_fluid_composition_info(self):

        self.tableWidget_new_fluid.blockSignals(True)
        self.tableWidget_new_fluid.clearContents()
        self.tableWidget_new_fluid.setRowCount(len(self.fluid_to_composition))
        self.tableWidget_new_fluid.setColumnCount(2)

        for row, (fluid, composition_data) in enumerate(self.fluid_to_composition.items()):

            self.tableWidget_new_fluid.setItem(row, 0, QTableWidgetItem(fluid))
            self.tableWidget_new_fluid.item(row, 0).setTextAlignment(Qt.AlignCenter)

            if len(composition_data) == 3:
                molar_fraction = round(100*composition_data[1], 7)
                self.add_molar_fraction_to_cell(row, molar_fraction = str(molar_fraction))

        self.label_selected_fluid.setText("")
        self.lineEdit_composition.setText("")
        self.tableWidget_new_fluid.blockSignals(False)

    def check_composition_input(self, fluid_name, composition):

        if isinstance(composition, float):

            fluid_file_name, _, _ = self.refprop_fluids[fluid_name]
            self.fluid_to_composition[fluid_name] = [  str(composition), 
                                                        composition / 100, 
                                                        fluid_file_name  ]

            if composition == 0:
                if fluid_name in self.fluid_to_composition.keys():
                    self.fluid_to_composition.pop(fluid_name)

            return False

    def on_click_item_refprop_fluids(self, item):
        self.selected_item = item
        self.selected_fluid = item.text(0)
        self.label_selected_fluid.setText(self.selected_fluid)

    def on_double_click_item_refprop_fluids(self, item):
        self.on_click_item_refprop_fluids(item)
        self.add_selected_fluid_to_composition_table(item.text(0))

    def add_selected_fluid_to_composition_table(self, selected_fluid):

        self.tableWidget_new_fluid.blockSignals(True)

        if selected_fluid == "":
            self.tableWidget_new_fluid.blockSignals(False)
            return

        if selected_fluid in self.fluid_to_composition.keys():
            self.tableWidget_new_fluid.blockSignals(False)
            return
        else:
            rows = self.tableWidget_new_fluid.rowCount()
            self.fluid_to_row[selected_fluid] = rows
            self.fluid_to_composition[selected_fluid] = list()

        self.tableWidget_new_fluid.setColumnCount(2)
        self.tableWidget_new_fluid.insertRow(rows)

        self.tableWidget_new_fluid.setItem(rows, 0, QTableWidgetItem(selected_fluid))
        self.tableWidget_new_fluid.item(rows, 0).setTextAlignment(Qt.AlignCenter)

        if self.add_molar_fraction_to_cell(rows):
            self.tableWidget_new_fluid.blockSignals(False)
            return

        molar_fraction = self.tableWidget_new_fluid.item(rows, 1).text()
        self.add_selected_fluid(self.selected_fluid, float(molar_fraction))

        self.tableWidget_new_fluid.blockSignals(False)

    def add_molar_fraction_to_cell(self, row, molar_fraction=None):

        if molar_fraction is None:
            if self.lineEdit_composition.text() == "":
                self.tableWidget_new_fluid.setItem(row, 1, QTableWidgetItem())
                self.tableWidget_new_fluid.item(row, 1).setTextAlignment(Qt.AlignCenter)
                return True

        try:

            if molar_fraction is None:
                molar_fraction = self.lineEdit_composition.text()

            molar_fraction = molar_fraction.replace(",", ".")
            self.tableWidget_new_fluid.setItem(row, 1, QTableWidgetItem(molar_fraction))
            self.tableWidget_new_fluid.item(row, 1).setTextAlignment(Qt.AlignCenter)
            self.lineEdit_composition.setText("")

        except:
            self.lineEdit_composition.setText("")
            self.lineEdit_composition.setFocus()
            return True

    def check_remaining_molar_fraction(self):

        message = ""
        if round(self.remaining_molar_fraction, 6):
            self.hide()
            remaining_molar_fraction = round(100*self.remaining_molar_fraction, 6)
            title = "Fluid composition not invalid"
            message += "The sum of all molar fractions must be equals to the unity. It is recommended "
            message += "to adjust the fluid composition until this requirement is met.\n\n"
            message += f"Remaining molar fraction: {remaining_molar_fraction} %"
            PrintMessageInput([error_title, title, message])
            return True
        
        return False
        
    def check_fluid_name(self):

        if self.lineEdit_fluid_name.text() == "":
            self.hide()
            title = "Additional input required"
            message = "Define a fluid name at specific input field to proceed."
            self.lineEdit_fluid_name.setFocus()
            PrintMessageInput([error_title, title, message])
            return True
        
        return False

    def get_fluid_composition_data(self):
        fluids_string = ""
        molar_fractions = list()
        for composition_data in self.fluid_to_composition.values():
            if len(composition_data) != 3:
                continue

            _, _fraction, file_name = composition_data
            fluids_string += file_name + ";"
            molar_fractions.append(_fraction)

        if fluids_string == "":
            return None

        fluids_string = fluids_string[:-1]

        return (fluids_string, molar_fractions)

    def process_fluid_properties_for_general_purposes(self, **kwargs):

        fluids_string = kwargs.get("fluids_string", "")
        molar_fractions = kwargs.get("molar_fractions", list())
        temperature_K = kwargs.get("temperature_K")
        pressure_Pa = kwargs.get("pressure_Pa")

        for key_prop, prop_label in self.refprop_interface.map_properties.items():
            if key_prop in ["PRANDTL", "TD", "KV"]:
                continue 

            fluid_property, errors = self.refprop_interface.get_specific_fluid_property(
                                                                                        fluids_string = fluids_string,
                                                                                        molar_fractions = molar_fractions,
                                                                                        property_key = key_prop,
                                                                                        temperature_K = temperature_K,
                                                                                        pressure_Pa = pressure_Pa,
                                                                                        )

            if errors:
                self.errors[prop_label] = errors

            self.fluid_properties[prop_label] = fluid_property

    def process_fluid_properties_for_reciprocating_compressors(self, **kwargs):

        fluids_string = kwargs.get("fluids_string", "")
        molar_fractions = kwargs.get("molar_fractions", list())
        temperature_K = kwargs.get("temperature_K")
        pressure_Pa = kwargs.get("pressure_Pa")

        for key_prop, prop_label in self.refprop_interface.map_properties.items():
            if key_prop in ["PRANDTL", "TD", "KV"]:
                continue

            fluid_property, errors = self.refprop_interface.get_specific_fluid_property(
                                                                                        fluids_string = fluids_string,
                                                                                        molar_fractions = molar_fractions,
                                                                                        property_key = key_prop,
                                                                                        temperature_K = temperature_K,
                                                                                        pressure_Pa = pressure_Pa,
                                                                                        )

            if errors:
                self.errors[prop_label] = errors

            self.fluid_properties[prop_label] = fluid_property
            if key_prop != "M":
                if key_prop == self.refprop_interface.isentropic_label:
                    self.k = fluid_property 

        self.T_discharge = (self.T_suction)*(self.p_ratio**((self.k-1)/self.k))
        self.lineEdit_temperature_disch.setText(str(round(self.T_discharge, 4)))

        temperature_K = self.T_discharge
        pressure_Pa = self.P_discharge

        if self.connection_type == "discharge":
            count = 0
            criteria = 100
            cache_temperatures = [temperature_K]
            while criteria > 0.001 and count <= 100:

                for key_prop, prop_label in self.refprop_interface.map_properties.items():
                    if key_prop in ["PRANDTL", "TD", "KV"]:
                        continue    

                    fluid_property, errors = self.refprop_interface.get_specific_fluid_property(
                                                                                                fluids_string = fluids_string,
                                                                                                molar_fractions = molar_fractions,
                                                                                                property_key = key_prop,
                                                                                                temperature_K = temperature_K,
                                                                                                pressure_Pa = pressure_Pa,
                                                                                                )

                    if errors:
                        self.errors[prop_label] = errors

                    self.fluid_properties[prop_label] = fluid_property  
                    if key_prop == self.refprop_interface.isentropic_label:
                        k_iter = fluid_property

                count += 1
                temperature_K_iter = self.T_suction*(self.p_ratio**((k_iter-1)/k_iter))
                cache_temperatures.append(temperature_K_iter)
                criteria = abs(cache_temperatures[-1]-cache_temperatures[-2])/((cache_temperatures[-1]+cache_temperatures[-2])/2)
                temperature_K = temperature_K_iter
                self.fluid_properties["temperature"] = temperature_K
                # print(count, k_iter, cache_temperatures[-1], cache_temperatures[-2], criteria)
            
            self.fluid_properties["pressure"] = pressure_Pa

    def get_fluid_properties(self):

        if self.check_fluid_name():
            return

        if self.check_remaining_molar_fraction():
            return

        composition_data = self.get_fluid_composition_data()
        if composition_data is None:
            return
        else:
            fluids_string, molar_fractions = composition_data

        values = self.get_temperature_and_pressure_SI_units()
        if values is None:
            return

        self.errors = dict()
        self.fluid_setup = list()
        self.fluid_properties = dict()

        [temperature_K, pressure_Pa] = values
        self.fluid_properties["temperature"] = temperature_K
        self.fluid_properties["pressure"] = pressure_Pa
        self.fluid_properties["name"] = self.lineEdit_fluid_name.text()

        if self.state_properties:
            self.process_fluid_properties_for_reciprocating_compressors(
                                                                        fluids_string = fluids_string,
                                                                        molar_fractions = molar_fractions,
                                                                        temperature_K = temperature_K,
                                                                        pressure_Pa = pressure_Pa,
                                                                        )

        else:
            self.process_fluid_properties_for_general_purposes(
                                                                fluids_string = fluids_string,
                                                                molar_fractions = molar_fractions,
                                                                temperature_K = temperature_K,
                                                                pressure_Pa = pressure_Pa,
                                                                )

        self.fluid_setup = [fluids_string, molar_fractions]

        self.process_errors()
        # if self.process_errors():
        #     return

        self.complete = True
        self.close()
        # self.actions_to_finalize()

        state_properties = self.refprop_interface.get_state_properties(
                                                                        temperatures_K = [386.8270, 313.15],
                                                                        pressures_Pa = [6011.48e3, 5883.01e3],
                                                                        distribution_type = "linear",
                                                                        N_fluids = 11,
                                                                        )

        self.fluid_properties_for_all_states, errors = self.refprop_interface.compute_fluid_properties_for_multiple_state_properties(
                                                                                                                                    fluid_name = self.lineEdit_fluid_name.text(),
                                                                                                                                    fluids_string = fluids_string,
                                                                                                                                    molar_fractions = molar_fractions,
                                                                                                                                    state_properties = state_properties,
                                                                                                                                    )                 

        # from pprint import pprint
        # pprint(fluid_properties_for_all_states)

    def get_temperature_and_pressure_SI_units(self):
        
        # if self.reciprocating_machine == "reciprocating_pump":
        #     if self.state_properties["connection_type"] == "suction":
        #         temperature_K = self.state_properties["temperature_at_suction"]
        #         pressure_Pa = self.state_properties["suction_pressure"]

        #     else:
        #         temperature_K = self.state_properties["temperature_at_discharge"]
        #         pressure_Pa = self.state_properties["discharge_pressure"]

        #     return [temperature_K, pressure_Pa]

        str_temperature = self.lineEdit_temperature.text()
        str_pressure = self.lineEdit_pressure.text()

        input_temperature = self.check_input_value(str_temperature, "'temperature'")
        if input_temperature is None:
            return None

        temperature_unit = self.comboBox_temperature_units.currentText()
        if "C" in temperature_unit:
            print("passou Celsius")
            temperature_K = input_temperature + 273.15
        elif "F" in temperature_unit:
            print("passou Farenheit")
            temperature_K = (input_temperature - 32) * (5 / 9) + 273.15
        else:
            print("passou Kelvin")
            temperature_K = input_temperature

        if temperature_K < 0:
            title = "Invalid entry to the temperature"
            message = "The typed value at temperature input field reaches a negative value in Kelvin scale."
            message += "It is necessary to enter a value that maintains the physicall coherence and consistence "
            message += "to proceed with the fluid setup."
            PrintMessageInput([error_title, title, message])
            return None

        input_pressure = self.check_input_value(str_pressure, "'pressure'")
        if input_pressure is None:
            return None

        pressure_unit = self.comboBox_pressure_units.currentText()
        if "kPa" in pressure_unit:
            pressure_Pa = 1e3 * input_pressure
        elif "atm" in pressure_unit:
            pressure_Pa = 101325 * input_pressure
        elif "bar" in pressure_unit:
            pressure_Pa = 1e5 * input_pressure
        elif "kgf/cm²" in pressure_unit:
            pressure_Pa = 9.80665e4 * input_pressure
        elif "psi" in pressure_unit:
            pressure_Pa = 6.89475729e3 * input_pressure
        elif "ksi" in pressure_unit:
            pressure_Pa = 6.89475729e6 * input_pressure
        else:
            pressure_Pa = input_pressure

        if "(g)" in pressure_unit:
            pressure_Pa += 101325

        if pressure_Pa < 0:
            title = "Invalid entry to the pressure"
            message = "The typed value at pressure input field reaches a negative value in Pascal scale. "
            message += "It is necessary to enter a value that maintains the physicall coherence and consistence "
            message += "to proceed with the fluid setup."
            PrintMessageInput([error_title, title, message])
            return None

        return [round(temperature_K, 8), round(pressure_Pa, 8)]

    def process_errors(self):
        if not self.errors:
            return
    
        title = "Error while processing fluid properties"
        message = "The following errors were found in while processing the fluid properties.\n\n"
    
        for key, _error in self.errors.items():
            message += f"{str(key)}: {str(_error)}\n\n"
    
        message += "It is recommended to check the fluid composition and state properties to proceed."
        PrintMessageInput([error_title, title, message])
        return True

    def actions_to_finalize(self):
        if not self.state_properties:
            return

        if self.state_properties["connection type"] == 1:
            title = "Fluid properties convergence"
            message = "The following fluid properties were obtained after completing the iterative updating process:"
            message += f"\n\nTemperature (discharge) = {round(self.fluid_properties['temperature'], 4)} [K]"
            message += f"\nIsentropic exponent = {round(self.fluid_properties['isentropic_exponent'], 6)} [-]"
            message += "\n\nReference fluid properties:"
            message += f"\n\nTemperature (suction) = {self.state_properties['temperature (suction)']} [K]"
            message += f"\nPressure (suction) = {self.state_properties['pressure (suction)']} [Pa]"
            message += f"\nPressure (discharge) = {round(self.state_properties['pressure (discharge)'], 4)} [Pa]"
            message += f"\nMolar mass = {round(self.fluid_properties['molar_mass'],6)} [kg/mol]"   
            PrintMessageInput([warning_title, title, message])

    def check_input_value(self, str_value: str, label: str):
        value = None
        if str_value != "":
            try:
                str_value = str_value.replace(",", ".")
                value = float(str_value)

            except Exception as error_log:
                title = f"Invalid entry to the {label}"
                message = f"Dear user, you have typed an invalid value at the {label} input field."
                message += "You should to inform a valid float number to proceed.\n\n"
                message += f"Details: {str(error_log)}"
                PrintMessageInput([error_title, title, message])
                return None

        else:
            title = "Empty field detected"
            message = f"The {label} input field is empty. Please, inform a valid float number to proceed."
            PrintMessageInput([error_title, title, message])
            return None       

        return value

    def cell_clicked_on_composition_table(self, row, col):
        self.selected_row = row

    def item_changed_callback(self, item):

        self.tableWidget_new_fluid.blockSignals(True)

        if item.column() == 0:
            row = item.row()
            selected_fluid = item.text()

            if selected_fluid in self.refprop_fluids.keys():
                if selected_fluid in self.fluid_to_composition.keys():
                    self.tableWidget_new_fluid.removeRow(row)
                    self.tableWidget_new_fluid.blockSignals(False)
                    return

                fluid_to_row = self.fluid_to_row.copy()
                for key, value in fluid_to_row.items():
                    if row == value:
                        if key != selected_fluid:

                            self.fluid_to_row.pop(key)
                            if key in self.fluid_to_composition.keys():
                                self.fluid_to_composition.pop(key)
                            
                            self.tableWidget_new_fluid.removeRow(row)
                            self.update_remainig_composition()
                            self.tableWidget_new_fluid.blockSignals(False)
                            return

            else:

                if self.selected_fluid in self.refprop_fluids.keys():
                    if self.selected_fluid in self.fluid_to_composition.keys():
                        self.fluid_to_composition.pop(self.selected_fluid)
                        self.update_remainig_composition()

                self.tableWidget_new_fluid.removeRow(row)
                self.tableWidget_new_fluid.blockSignals(False)
                return

            self.fluid_to_row[selected_fluid] = row
            if self.add_molar_fraction_to_cell(row):
                self.tableWidget_new_fluid.blockSignals(False)
                return

            molar_fraction = self.tableWidget_new_fluid.item(item.row(), 1).text()
            if molar_fraction != "":
                molar_fraction = float(molar_fraction)

            self.add_selected_fluid(selected_fluid, molar_fraction)

        else:

            if self.item_is_invalid_number(item):
                self.tableWidget_new_fluid.blockSignals(False)
                return
 
            self.go_to_next_cell(item)
            selected_fluid = self.tableWidget_new_fluid.item(item.row(), 0).text()
            molar_fraction = self.tableWidget_new_fluid.item(item.row(), 1).text()

            if molar_fraction != "":
                molar_fraction = float(molar_fraction)
            self.add_selected_fluid(selected_fluid, molar_fraction)

        self.tableWidget_new_fluid.blockSignals(False)

    def go_to_next_cell(self, item):
        
        row = item.row()
        column = item.column()
        if column == 0:
            return

        if row <= self.tableWidget_new_fluid.rowCount() - 1:
            next_item = self.tableWidget_new_fluid.item(row + 1, column)
            if next_item is None:
                return
            
            if next_item.text() == "":
                self.tableWidget_new_fluid.setCurrentItem(next_item)
                self.tableWidget_new_fluid.editItem(next_item)

    def item_is_invalid_number(self, item):

        if item is None:
            return True
        
        if item.text() == "":
            return False

        if item.column() == 0:
            return True
        
        str_value = item.text().replace(",", ".")
        item.setText(str_value)

        try:
            value = float(str_value)

        except Exception as error_log:
            window_title = "Error"
            title = "Invalid real number"
            message = "The value typed for molar composition must be a non-zero positive number.\n\n"
            message += f"Details: {error_log}"
            PrintMessageInput([window_title, title, message])
            item.setText("")
            return True
        
        message = ""

        if value > 100 or value < 0:
            message = "Dear user, you have typed an invalid entry at the fluid Composition input. "
            message += "The value should be a positive value less or equals to 100."

        if message != "":
            self.hide()
            window_title = "Error"
            title = "Invalid molar fraction"
            PrintMessageInput([window_title, title, message])
            item.setText("")
            return True
        
        return False

    def load_fluid_composition_callback(self):

        self.hide()
        self.label_selected_fluid.setText("")

        self.fluid_data = dict()
        self.fluid_to_composition = dict()

        read = LoadFluidCompositionInputs(file_path = self.composition_file_path)

        if read.complete:

            self.composition_file_path = read.file_path
            composition_data = read.fluid_composition_data

            comp = 0
            for (i, label, refprop_fluid_name, molar_fraction) in composition_data:

                self.fluid_data[i] = [label, refprop_fluid_name, molar_fraction]

                if not refprop_fluid_name in self.refprop_fluids.keys():
                    pass

                if refprop_fluid_name in self.refprop_fluids.keys():
                    if molar_fraction:

                        [fluid_file, _, _] = self.refprop_fluids[refprop_fluid_name]
                        self.fluid_to_composition[refprop_fluid_name] = [str(molar_fraction), molar_fraction, fluid_file]
                        comp += molar_fraction

            self.load_fluid_composition_info()
            self.update_remainig_composition()

        app().main_window.set_input_widget(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.get_fluid_properties()
        if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.remove_selected_gas()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.keep_window_open = False