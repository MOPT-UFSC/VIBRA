from PySide6.QtWidgets import QDialog, QHeaderView, QTableWidgetItem
from PySide6.QtCore import Qt

from vibra import app
from vibra.interface.ui_generated.model.setup.fluid.fluid_widget_ui import FluidWidget_UI
from vibra.interface.formatters.icons import *

from vibra.interface.general.pick_color_input import PickColorInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.model_inputs.acoustic.fluid.set_fluid_composition_inputs import SetFluidCompositionInputs

from vibra.engine.properties.fluid import Fluid
from vibra.libraries.default_libraries import default_fluid_library

from vibra.utils.utils import *
from molde import Color
from copy import deepcopy
from itertools import count

window_title_1 = "Error"
window_title_2 = "Warning"

COLOR_ROW = 11

def get_color_rgb(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class FluidWidget(FluidWidget_UI):
    def __init__(self, *argas, **kwargs):
        super().__init__()

        self.dialog = kwargs.get("dialog", None)
        self.state_properties = kwargs.get("state_properties", dict())

        self.project = app().project
        self.model = app().project.model
        self.properties = app().project.model.properties

        self._initialize()
        self._configure_qt_variables()
        self._create_connections()
        self._config_widgets()
        self._paint_icons()
        self.load_data_from_fluids_library()

    def _initialize(self):

        self.row = None
        self.col = None
        self.refprop = None
        self.selected_column = None

        self.fluids_from_library = dict()
        self.fluid_data_refprop = dict()
        self.fluid_name_to_refprop_data = dict()

        self.fluid_data_keys = [
                                "name",
                                "identifier",
                                "temperature",
                                "pressure",
                                "fluid_density",
                                "speed_of_sound",
                                "isentropic_exponent",
                                "thermal_conductivity",
                                "specific_heat_Cp",
                                "dynamic_viscosity",
                                "molar_mass",
                                "color"
                                ]

    def _configure_qt_variables(self):
        self.tableWidget_fluid_data.setStyleSheet("")

    def _create_connections(self):
        #
        self.pushButton_add_column.clicked.connect(self.add_column)
        self.pushButton_duplicate.clicked.connect(self.duplicate_selected_fluid)
        self.pushButton_refprop.clicked.connect(self.call_refprop_interface)
        self.pushButton_remove_column.clicked.connect(self.remove_selected_column)
        # self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)
        #
        self.tableWidget_fluid_data.cellClicked.connect(self.cell_clicked_callback)
        self.tableWidget_fluid_data.itemChanged.connect(self.item_changed_callback)
        self.tableWidget_fluid_data.cellDoubleClicked.connect(self.cell_double_clicked_callback)

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _config_widgets(self):
        self.tableWidget_fluid_data.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))
    
    def _update_size_policy(self):
        if len(self.fluids_from_library) > 6:
            self.tableWidget_fluid_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        else:
            self.tableWidget_fluid_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _paint_icons(self):
        icon_color = None
        theme = app().config.user_preferences.interface_theme
        from vibra import LIGHT_ICON_COLOR, DARK_ICON_COLOR
        if theme == "dark":
            icon_color = DARK_ICON_COLOR.to_qt()
        else:
            icon_color = LIGHT_ICON_COLOR.to_qt()

        widgets = [self.pushButton_duplicate]
        change_icon_color_for_widgets(widgets, icon_color)

    def _add_icon_and_title(self):
        self._config_window()

    def load_data_from_fluids_library(self):

        config = app().file.read_fluid_library_from_file()
        if config is None:
            self.reset_library_to_default()
            return

        self.fluids_from_library.clear()
        self.fluid_name_to_refprop_data.clear()

        if not list(config.sections()):
            self.update_table()
            return

        for tag in config.sections():

            section = config[tag]
            keys = config[tag].keys()

            name = section.get('name')
            identifier =  int(section.get('identifier'))
            fluid_density =  float(section.get('fluid_density'))
            speed_of_sound =  float(section.get('speed_of_sound'))
            color =  get_color_rgb(section.get('color'))

            if 'isentropic_exponent' in keys:
                isentropic_exponent = float(section.get('isentropic_exponent'))
            else:
                isentropic_exponent = ""

            if 'thermal_conductivity' in keys:
                thermal_conductivity = float(section.get('thermal_conductivity'))
            else:
                thermal_conductivity = ""

            if 'specific_heat_Cp' in keys:
                specific_heat_Cp = float(section.get('specific_heat_Cp'))
            else:
                specific_heat_Cp = ""

            if 'dynamic_viscosity' in keys:
                dynamic_viscosity = float(section.get('dynamic_viscosity'))
            else:
                dynamic_viscosity = ""
            
            if 'temperature' in keys:
                temperature = float(section.get('temperature'))
            else:
                temperature = None

            if 'pressure' in keys:
                pressure = float(section.get('pressure'))
            else:
                pressure = None

            if 'key_mixture' in keys:
                key_mixture = section.get('key_mixture')
            else:
                key_mixture = None

            if 'molar_fractions' in keys:
                str_molar_fractions = section.get('molar_fractions')
                molar_fractions = get_list_of_values_from_string(str_molar_fractions, int_values=False)
            else:
                molar_fractions = None

            if 'molar_mass' in keys:
                if section.get('molar_mass') == "None":
                    molar_mass = None
                else:
                    molar_mass = float(section.get('molar_mass'))
            else:
                molar_mass = None

            fluid = Fluid(  name = name,
                            fluid_density = fluid_density,
                            speed_of_sound = speed_of_sound,
                            color =  color,
                            identifier = identifier,
                            isentropic_exponent = isentropic_exponent,
                            thermal_conductivity = thermal_conductivity,
                            specific_heat_Cp = specific_heat_Cp,
                            dynamic_viscosity = dynamic_viscosity,
                            temperature = temperature,
                            pressure = pressure,
                            molar_mass = molar_mass  )

            self.fluids_from_library[identifier] = fluid

            aux = [
                   name,
                   temperature, 
                   pressure, 
                   key_mixture, 
                   molar_fractions
                   ]

            if aux.count(None) == 0:
                self.fluid_name_to_refprop_data[name] = aux

        self.update_table()

    def update_table(self):

        self.tableWidget_fluid_data.clearContents()
        self.tableWidget_fluid_data.blockSignals(True)
        self.tableWidget_fluid_data.setRowCount(COLOR_ROW + 1)
        self.tableWidget_fluid_data.setColumnCount(len(self.fluids_from_library))

        for j, fluid in enumerate(self.fluids_from_library.values()):
            if isinstance(fluid, Fluid):

                self.tableWidget_fluid_data.setItem( 0, j, QTableWidgetItem(str(fluid.name)))
                self.tableWidget_fluid_data.setItem( 1, j, QTableWidgetItem(str(fluid.identifier)))
                self.tableWidget_fluid_data.setItem( 2, j, QTableWidgetItem(str(fluid.temperature)))
                self.tableWidget_fluid_data.setItem( 3, j, QTableWidgetItem(str(fluid.pressure)))
                self.tableWidget_fluid_data.setItem( 4, j, QTableWidgetItem(str(fluid.fluid_density)))
                self.tableWidget_fluid_data.setItem( 5, j, QTableWidgetItem(str(fluid.speed_of_sound)))
                self.tableWidget_fluid_data.setItem( 6, j, QTableWidgetItem(str(fluid.isentropic_exponent)))
                self.tableWidget_fluid_data.setItem( 7, j, QTableWidgetItem(f"{fluid.thermal_conductivity : .4e}"))
                self.tableWidget_fluid_data.setItem( 8, j, QTableWidgetItem(str(fluid.specific_heat_Cp)))
                self.tableWidget_fluid_data.setItem( 9, j, QTableWidgetItem(f"{fluid.dynamic_viscosity : .4e}"))
                self.tableWidget_fluid_data.setItem(10, j, QTableWidgetItem(str(fluid.molar_mass)))

                item = QTableWidgetItem()
                item.setBackground(Color(*fluid.color).to_qt())
                item.setForeground(Color(*fluid.color).to_qt())
                self.tableWidget_fluid_data.setItem(COLOR_ROW, j, item)

                if fluid.name in self.fluid_name_to_refprop_data.keys():
                    for i in range(11):
                        self.tableWidget_fluid_data.item(i, j).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        for i in range(self.tableWidget_fluid_data.rowCount()):
            for j in range(self.tableWidget_fluid_data.columnCount()):
                self.tableWidget_fluid_data.item(i, j).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_fluid_data.blockSignals(False)
        self._update_size_policy()

    def get_selected_column(self) -> int:
        selected_items = self.tableWidget_fluid_data.selectedIndexes()
        if not selected_items:
            return -1
        return selected_items[-1].column()

    def get_selected_fluid(self) -> Fluid | None:

        selected_column = self.get_selected_column()
        if selected_column < 0:
            return

        if selected_column >= len(self.fluids_from_library):
            return

        item = self.tableWidget_fluid_data.item(1, selected_column)
        identifier = int(item.text())

        return self.fluids_from_library.get(identifier)

    def add_column(self):
    
        self.tableWidget_fluid_data.blockSignals(True)

        table_size = self.tableWidget_fluid_data.columnCount()
        if table_size > len(self.fluids_from_library):
            # it means that if you already have a new row
            # to insert data you don't need another one
            self.tableWidget_fluid_data.blockSignals(False)
            return 

        last_col = self.tableWidget_fluid_data.columnCount()
        self.tableWidget_fluid_data.insertColumn(last_col)

        for i in range(self.tableWidget_fluid_data.rowCount()):
            item = QTableWidgetItem()
            item.setSizeHint(QSize(80, 30))
            self.tableWidget_fluid_data.setItem(i, last_col, item)
            self.tableWidget_fluid_data.item(i, last_col).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_fluid_data.selectColumn(last_col)
        first_item = self.tableWidget_fluid_data.item(0, last_col)
        if self.refprop is None:
            self.tableWidget_fluid_data.editItem(first_item)

        self.tableWidget_fluid_data.blockSignals(False)

    def remove_selected_column(self):

        selected_column = self.get_selected_column()
        if selected_column < 0:
            return

        if selected_column >= len(self.fluids_from_library):
            # if it is the last item and a not an already configured
            # fluid, just remove the last line
            current_size = self.tableWidget_fluid_data.columnCount()
            self.tableWidget_fluid_data.setColumnCount(current_size - 1)

            self._update_size_policy()
            self.tableWidget_fluid_data.horizontalScrollBar().setSliderPosition(0)
            return

        item = self.tableWidget_fluid_data.item(1, selected_column)
        identifier = int(item.text())
        fluid = self.fluids_from_library.get(identifier)

        self.remove_fluid_from_file(fluid)
        self._update_size_policy()

        self.tableWidget_fluid_data.horizontalScrollBar().setSliderPosition(0)

    def duplicate_selected_fluid(self):

        selected_column = self.get_selected_column()
        if selected_column < 0:
            return
        
        self.refprop = None
        item = self.tableWidget_fluid_data.item(1, selected_column)
        if item.text() == "":
            return

        identifier = int(item.text())
        fluid = self.fluids_from_library.get(identifier)
        if not isinstance(fluid, Fluid):
            return

        dfluid = deepcopy(fluid)
        new_identifier = self.new_identifier()

        dfluid.identifier = new_identifier
        dfluid.name = self.get_suffix_for_duplicated_fluid(dfluid.name)
        self.fluids_from_library[new_identifier] = dfluid

        self.update_table()
        last_col = self.tableWidget_fluid_data.columnCount()

        self.add_fluid_to_file(last_col-1, fluid=dfluid.__dict__)

        app().processEvents()
        self.set_scroll_bar_to_maximum()

    def get_suffix_for_duplicated_fluid(self, fluid_name: str):

        already_used_names = set()
        for fluid in self.fluids_from_library.values():
            fluid: Fluid
            if fluid_name in fluid.name:
                already_used_names.add(fluid.name)

        for i in count(1):
            new_name = f"{fluid_name} ({i})"
            if new_name not in already_used_names:
                return new_name

    def set_scroll_bar_to_maximum(self):
        scroll_bar = self.tableWidget_fluid_data.horizontalScrollBar()
        scroll_bar.setSliderPosition(scroll_bar.minimum())
        app().processEvents()
        scroll_bar.setSliderPosition(scroll_bar.maximum())

        
    def item_changed_callback(self, item):

        self.tableWidget_fluid_data.blockSignals(True)

        if item.row() == 0:
            if self.column_has_invalid_name(item.column()):
                self.tableWidget_fluid_data.blockSignals(False)
                return

        elif item.row() == 1:
            if self.column_has_invalid_identifier(item.column()):
                self.tableWidget_fluid_data.blockSignals(False)
                return

        else:
            if self.item_is_invalid_number(item):
                self.tableWidget_fluid_data.blockSignals(False)
                return

        self.go_to_next_cell(item)
        if self.column_has_empty_items(item.column()):
            self.tableWidget_fluid_data.blockSignals(False)
            return

        self.add_fluid_to_file(item.column())
        self.load_data_from_fluids_library()

        self.tableWidget_fluid_data.blockSignals(False)
        self.tableWidget_fluid_data.horizontalScrollBar().setSliderPosition(0)
    
    def go_to_next_cell(self, item):

        row = item.row()
        column = item.column()

        if row < COLOR_ROW - 1:
            next_item = self.tableWidget_fluid_data.item(row + 1, column)
            if next_item.text() == "":
                self.tableWidget_fluid_data.setCurrentItem(next_item)
                self.tableWidget_fluid_data.editItem(next_item)

        elif row == COLOR_ROW - 1:
            self.pick_color(row + 1, column)

    def column_has_invalid_name(self, column):

        item = self.tableWidget_fluid_data.item(0, column)
        if item is None:
            return True

        column_name = item.text()

        if not column_name:
            return True

        for fluid in self.fluids_from_library.values():
            if fluid.name == column_name:
                return True

        return False 

    def column_has_invalid_identifier(self, column):

        item = self.tableWidget_fluid_data.item(1, column)

        already_used_ids = set()
        for fluid in self.fluids_from_library.values():
            already_used_ids.add(fluid.identifier)
        
        if item.text() == "":
            return True
        
        try:
            if int(item.text()) in already_used_ids:
                item.setText("")
                return True
        except:
            item.setText("")
            return True

    def column_has_empty_items(self, column):
        for row in range(COLOR_ROW + 1):

            item = self.tableWidget_fluid_data.item(row, column)
            if item is None:
                return True
            
            if row == COLOR_ROW:
                color = item.background().color().getRgb()
                if list(color) == 0:
                    return True

            elif item.text() == "":
                return True

        return False

    def item_is_invalid_number(self, item):

        if item is None:
            return True

        row = item.row()
        if row == COLOR_ROW:
            return
        
        prop_labels = {
                        2 : "temperature", 
                        3 : "pressure",
                        4 : "fluid_density",
                        5 : "speed_of_sound",
                        6 : "isentropic_exponent",
                        7 : "thermal_conductivity",
                        8 : "specific_heat_Cp",
                        9 : "dynamic_viscosity",
                       10 : "molar_mass"
                    }

        if row not in prop_labels.keys():
            return True
        
        if item.text() == "":
            return True

        try:

            str_value = item.text().replace(",", ".")
            item.setText(str_value)
            value = float(str_value)

        except Exception as error_log:
            title = "Invalid real number"
            message = f"The value typed for '{prop_labels[row]}' "
            message += "must be a non-zero positive number.\n\n"
            message += f"Details: {error_log}"
            PrintMessageInput([window_title_1, title, message])
            item.setText("")
            return True

        if value < 0:
            title = "Negative value not allowed"
            message = f"The value typed for '{prop_labels[row]}' must be a non-zero positive number."
            PrintMessageInput([window_title_1, title, message])
            item.setText("")
            return True

        return False

    def add_fluid_to_file(self, column: int, fluid: None | dict = None):
        try:

            fluid_data = dict()
            for i, key in enumerate(self.fluid_data_keys):
                item = self.tableWidget_fluid_data.item(i, column)

                if key == "color":
                    color = item.background().color().getRgb()
                    fluid_data[key] = list(color[:3])

                else:
                    if fluid is None:
                        fluid_data[key] = item.text()
                    else:
                        fluid_data[key] = str(fluid.get(key))

            identifier = fluid_data["identifier"]

            if self.refprop is not None:
                [key_mixture, molar_fractions] = self.fluid_setup
                fluid_data['key_mixture'] = key_mixture
                fluid_data['molar_fractions'] = molar_fractions
                fluid_data['molar_mass'] = round(self.fluid_data_refprop['molar_mass'], 6)

            config = app().file.read_fluid_library_from_file()
            config[identifier] = fluid_data

            app().file.write_fluid_library_in_file(config)

        except Exception as error_log:
            title = "Error while writing fluid data in file"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return True

    def remove_fluid_from_file(self, fluid: Fluid):

        config = app().file.read_fluid_library_from_file()

        identifier = str(fluid.identifier)
        if not identifier in config.sections():
            return

        config.remove_section(identifier)
        app().file.write_fluid_library_in_file(config)

        self.reset_fluids_from_bodies_and_surfaces([fluid.identifier])
        self.load_data_from_fluids_library()

    def cell_clicked_callback(self, row, col):
        if row == COLOR_ROW:
            self.pick_color(row, col)

    def cell_double_clicked_callback(self, row, col):

        self.tableWidget_fluid_data.blockSignals(True)
        fluid_name = self.tableWidget_fluid_data.item(0, col).text()

        if fluid_name in self.fluid_name_to_refprop_data.keys():

            if isinstance(self.dialog, QDialog):
                self.dialog.hide()

            selected_fluid = self.fluid_name_to_refprop_data.get(fluid_name)
            self.refprop = SetFluidCompositionInputs(
                                                     selected_fluid_to_edit = selected_fluid, 
                                                     state_properties = self.state_properties
                                                     )

            if not self.refprop.complete:
                self.refprop = None
                app().main_window.set_input_widget(self)
                self.tableWidget_fluid_data.blockSignals(False)
                return

            self.selected_column = col
            self.after_getting_fluid_properties_from_refprop()
            self.selected_column = None

        self.tableWidget_fluid_data.selectColumn(col)
        self.tableWidget_fluid_data.blockSignals(False)

    def new_identifier(self):

        already_used_ids = set()
        for fluid in self.fluids_from_library.values():
            fluid: Fluid
            already_used_ids.add(fluid.identifier)

        for i in count(1):
            if i not in already_used_ids:
                return i

    def pick_color(self, row, col):

        read = PickColorInput()
        if not read.complete:
            return True

        picked_color = read.color
        item = QTableWidgetItem()
        item.setBackground(Color(*picked_color).to_qt())
        item.setForeground(Color(*picked_color).to_qt())
        self.tableWidget_fluid_data.setItem(row, col, item)
        self.tableWidget_fluid_data.item(row, 0).setSelected(True)

    def get_confirmation_to_proceed(self):

        title = "Resetting the fluids library"
        message = "Would you like to reset the fluid library to default?"

        buttons_config = {  "left_button_label" : "No", 
                            "right_button_label" : "Yes",
                            "left_button_size" : 80,
                            "right_button_size" : 80}

        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return False

        if read._continue:
            return True
        
    def reset_library_callback(self):
        if self.get_confirmation_to_proceed():
            self.reset_library_to_default()
            return True
        return False

    def reset_library_to_default(self):

        config_cache = app().file.read_fluid_library_from_file()

        sections_cache = list()
        if config_cache is not None:
            sections_cache = config_cache.sections()

        default_fluid_library()

        config = app().file.read_fluid_library_from_file()

        fluid_identifiers = list()
        for section_cache in sections_cache:
            if section_cache not in config.sections():
                identifier = config_cache[section_cache]["identifier"]
                fluid_identifiers.append(int(identifier))

        self.reset_fluids_from_bodies_and_surfaces(fluid_identifiers)
        self.load_data_from_fluids_library()

    def reset_fluids_from_bodies_and_surfaces(self, fluid_identifiers : list):

        surfaces_to_remove_fluid = list()
        volumes_to_remove_fluid = list()

        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "fluid":
                if isinstance(data, Fluid):
                    if data.identifier in fluid_identifiers:
                        volumes_to_remove_fluid.append(volume_id)
                        surface_ids = self.model.mesh.surfaces_from_volume[volume_id]
                        for surface_id in surface_ids:
                            surfaces_to_remove_fluid.append(surface_id)

        for vol_id in volumes_to_remove_fluid:
            self.model.properties._remove_volume_property("fluid", volume_id=vol_id)

        for surf_id in surfaces_to_remove_fluid:
            self.model.properties._remove_surface_property("fluid", surface_id=surf_id)

        app().file.write_model_properties_in_file()

        if isinstance(self.dialog, QDialog):
            self.dialog.load_model_info()

    def call_refprop_interface(self):

        if isinstance(self.dialog, QDialog):
            self.dialog.hide()

        self.refprop = SetFluidCompositionInputs(state_properties = self.state_properties)
        if not self.refprop.complete:
            self.refprop = None
            app().main_window.set_input_widget(self)
            return True

        self.after_getting_fluid_properties_from_refprop()

    def after_getting_fluid_properties_from_refprop(self):

        if self.refprop.complete:

            self.fluid_setup = self.refprop.fluid_setup
            self.fluid_data_refprop = self.refprop.fluid_properties

            if self.selected_column is None:
                self.add_column()
                self.tableWidget_fluid_data.blockSignals(True)
                selected_column = self.tableWidget_fluid_data.columnCount() - 1
            else:
                selected_column = self.selected_column

            for row, key in enumerate(self.fluid_data_keys):

                if key == "identifier":
                    if isinstance(self.selected_column, int):
                        item = self.tableWidget_fluid_data.item(1, self.selected_column)
                        _data = str(item.text())
                    else:
                        _data = str(self.new_identifier())

                elif key == "color":
                    if self.selected_column is None:
                        self.pick_color(row, selected_column)
                    continue

                else:

                    data = self.fluid_data_refprop[key]
                    if isinstance(data, float):

                        if key in ["pressure", "thermal_conductivity", "dynamic_viscosity"]:
                            _data = f"{data : .6e}"
                        else:
                            _data = f"{data : .6f}"

                    elif isinstance(data, str):
                        _data = data

                self.tableWidget_fluid_data.item(row, selected_column).setText(_data)

            self.add_fluid_to_file(selected_column)
            self.tableWidget_fluid_data.blockSignals(False)
            self.load_data_from_fluids_library()

        self.refprop = None

    def load_compressor_info(self):

        if self.state_properties:

            if isinstance(self.dialog, QDialog):
                return

                volume_id = self.state_properties['volume_id']
                self.dialog.comboBox_attribution_type.setCurrentIndex(1)
                self.dialog.write_ids(volume_id)
                self.dialog.lineEdit_selection_id.setDisabled(True)
                if self.fluid_data_refprop:
                    fluid_name = self.fluid_data_refprop["name"]
                    self.dialog.lineEdit_fluid_name.setText(fluid_name)

                connection_type_comp = self.state_properties['connection type']
                connection_label = "discharge" if connection_type_comp else "suction"
                
                self.dialog.setWindowTitle(f"Set a fluid thermodynamic state at the compressor {connection_label}")

    def update_compressor_fluid_temperature_and_pressure(self):
        return

        temperature_lineEdits = [self.lineEdit_temperature, self.lineEdit_temperature_rp]
        pressure_lineEdits = [self.lineEdit_pressure, self.lineEdit_pressure_rp]

        for temperature_lineEdit in temperature_lineEdits:
            temperature_lineEdit.setText(str(round(self.temperature_comp,4)))
            temperature_lineEdit.setDisabled(True)

        for pressure_lineEdit in pressure_lineEdits:
            pressure_lineEdit.setText(str(round(self.pressure_comp,4)))
            pressure_lineEdit.setDisabled(True)

    def update_compressor_info(self):
        if self.state_properties:
            if self.refprop is not None:
                if self.refprop.complete:
                    self.state_properties["temperature (discharge)"] = round(self.fluid_data_refprop["temperature"], 4)
                    self.state_properties["molar_mass"] = self.fluid_data_refprop["molar_mass"]

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if isinstance(self.dialog, QDialog):
                self.dialog.attribute_callback()

        elif event.key() == Qt.Key_Delete:
            self.remove_selected_column()

        elif event.key() == Qt.Key_Escape:
            if isinstance(self.dialog, QDialog):
                self.dialog.close()
            else:
                self.close()