from PySide6.QtWidgets import QDialog, QHeaderView, QTableWidgetItem
from PySide6.QtCore import Qt, QSize

from molde import Color

from vibra import app
from vibra.interface.ui_generated.model.setup.fluid.fluid_widget_ui import FluidWidget_UI
from vibra.interface.formatters.icons import change_icon_color_for_widgets

from vibra.interface.general.pick_color_input import PickColorInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.model_inputs.acoustic.fluid.set_fluid_composition_inputs import SetFluidCompositionInputs

from vibra.engine.properties.fluid import Fluid
from vibra.libraries.default_libraries import default_fluid_library

from copy import deepcopy
from itertools import count

error_title = "Error"
warning_title = "Warning"

COLOR_ROW = 11


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

        self.refprop_fluids_data = dict()
        self.fluids_from_library = dict()
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

        self.fluids_from_library.clear()
        self.fluid_name_to_refprop_data.clear()

        fluids_from_library = app().load_project.load_fluid_library()
        if fluids_from_library is None:
            self.reset_library_to_default()
            return

        elif isinstance(fluids_from_library, dict):
            if not fluids_from_library:
                self.reset_library_to_default()
                return

        self.fluids_from_library = fluids_from_library

        for fluid in fluids_from_library.values():
            if not isinstance(fluid, Fluid):
                continue

            refprop_parameters = [
                                  fluid.name,
                                  fluid.temperature, 
                                  fluid.pressure, 
                                  fluid.key_mixture, 
                                  fluid.molar_fractions
                                  ]

            if refprop_parameters.count(None) == 0:
                self.fluid_name_to_refprop_data[fluid.name] = refprop_parameters

        self.update_table_of_fluids()

    def update_table_of_fluids(self):

        self.tableWidget_fluid_data.clearContents()
        self.tableWidget_fluid_data.blockSignals(True)
        self.tableWidget_fluid_data.setRowCount(COLOR_ROW + 1)
        self.tableWidget_fluid_data.setColumnCount(len(self.fluids_from_library))

        for j, fluid in enumerate(self.fluids_from_library.values()):
            if isinstance(fluid, Fluid):

                self.tableWidget_fluid_data.setItem( 0, j, QTableWidgetItem(str(fluid.name)))
                self.tableWidget_fluid_data.setItem( 1, j, QTableWidgetItem(f"{fluid.identifier}"))
                self.tableWidget_fluid_data.setItem( 2, j, QTableWidgetItem(f"{round(fluid.temperature, 6)}"))
                self.tableWidget_fluid_data.setItem( 3, j, QTableWidgetItem(f"{fluid.pressure : .6e}"))
                self.tableWidget_fluid_data.setItem( 4, j, QTableWidgetItem(f"{fluid.fluid_density : .6f}"))
                self.tableWidget_fluid_data.setItem( 5, j, QTableWidgetItem(f"{fluid.speed_of_sound : .6f}"))
                self.tableWidget_fluid_data.setItem( 6, j, QTableWidgetItem(f"{fluid.isentropic_exponent : .6f}"))
                self.tableWidget_fluid_data.setItem( 7, j, QTableWidgetItem(f"{fluid.thermal_conductivity : .6e}"))
                self.tableWidget_fluid_data.setItem( 8, j, QTableWidgetItem(f"{fluid.specific_heat_Cp : .6e}"))
                self.tableWidget_fluid_data.setItem( 9, j, QTableWidgetItem(f"{fluid.dynamic_viscosity : .6e}"))
                self.tableWidget_fluid_data.setItem(10, j, QTableWidgetItem(f"{fluid.molar_mass : .3f}"))

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

    def add_column(self, single_add: bool = True):
    
        self.tableWidget_fluid_data.blockSignals(True)

        table_size = self.tableWidget_fluid_data.columnCount()
        if table_size > len(self.fluids_from_library) and single_add:
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
        dfluid.identifier = self.new_identifier()
        dfluid.name = self.get_suffix_for_duplicated_fluid(dfluid.name)

        fluid_data = dfluid.__dict__

        # fluid_data = {
        #             "name" : dfluid.name,
        #             "identifier" : dfluid.identifier,
        #             "temperature" : dfluid.temperature,
        #             "pressure" : dfluid.pressure,
        #             "fluid_density" : dfluid.fluid_density,
        #             "speed_of_sound" : dfluid.speed_of_sound,
        #             "isentropic_exponent" : dfluid.isentropic_exponent,
        #             "thermal_conductivity" : dfluid.thermal_conductivity,
        #             "specific_heat_Cp" : dfluid.specific_heat_Cp,
        #             "dynamic_viscosity" : dfluid.dynamic_viscosity,
        #             "molar_mass" : dfluid.molar_mass,
        #             "color" : dfluid.color,
        #             }

        if self.add_fluid_data_in_file([fluid_data]):
            return

        self.load_data_from_fluids_library()

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

        fluid_data = self.get_fluid_data_for_selected_column(item.column())
        if self.add_fluid_data_in_file([fluid_data]):
            return

        self.load_data_from_fluids_library()

        self.tableWidget_fluid_data.blockSignals(False)
    
    def go_to_next_cell(self, item):

        row = item.row()
        column = item.column()

        if row < COLOR_ROW - 1:
            next_item = self.tableWidget_fluid_data.item(row + 1, column)
            if next_item.text() == "":
                self.tableWidget_fluid_data.setCurrentItem(next_item)
                self.tableWidget_fluid_data.editItem(next_item)

        elif row == COLOR_ROW - 1:
            self.pick_color_for_item(row + 1, column)

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
            PrintMessageInput([error_title, title, message])
            item.setText("")
            return True

        if value < 0:
            title = "Negative value not allowed"
            message = f"The value typed for '{prop_labels[row]}' must be a non-zero positive number."
            PrintMessageInput([error_title, title, message])
            item.setText("")
            return True

        return False

    def add_fluid_data_in_file(self, fluids_data: list, from_refprop: bool=False):

        # read fluid library data from file
        fluid_library_data = app().file.read_fluid_library_from_file()

        # get list of new fluid identifiers
        identifiers = self.get_new_identifiers(len(fluids_data))

        for j, fluid_data in enumerate(fluids_data):
            filt_fluid_data = dict()

            # check all inputs before proceeding
            for key in self.fluid_data_keys:
                value = fluid_data.get(key)
                if value is None:
                    if key == "identifier" and from_refprop:
                        filt_fluid_data["identifier"] = identifiers[j]
                        continue
                    elif key == "color":
                        filt_fluid_data[key] = self.pick_color()
                        continue
                    return True

                filt_fluid_data[key] = value

            # additionally, check all refprop inputs before proceeding    
            if from_refprop:
                for key in ["key_mixture", "molar_fractions"]:
                    value = fluid_data.get(key)
                    if value is None:
                        return True
                    filt_fluid_data[key] = value

            # fluid identifier
            identifier = filt_fluid_data.get("identifier")
        
            # add the new fluid data
            fluid_library_data[identifier] = filt_fluid_data

        # save the modified fluid data in file
        app().file.write_fluid_library_in_file(fluid_library_data)

    def get_fluid_data_for_selected_column(self, column: int):
        try:

            fluid_data = dict()
            for i, key in enumerate(self.fluid_data_keys):
                item = self.tableWidget_fluid_data.item(i, column)
                if key == "name":
                    fluid_data[key] = item.text()

                elif key == "color":
                    color = item.background().color().getRgb()
                    fluid_data[key] = list(color[:3])

                elif key == "identifier":
                    identifier = int(item.text())
                    fluid_data[key] = identifier

                else:
                    fluid_data[key] = float(item.text())

            if self.refprop is not None:
                fluid_data['key_mixture'] = self.refprop_fluids_data.get("key_mixture")
                fluid_data['molar_fractions'] = self.refprop_fluids_data.get("molar_fractions")
                fluid_data['molar_mass'] = round(self.refprop_fluids_data.get("molar_mass"), 6)

            return fluid_data
                    
        except Exception as error_log:
            title = "Error while writing fluid data in file"
            message = str(error_log)
            PrintMessageInput([error_title, title, message])
            return None

    def remove_fluid_from_file(self, fluid: Fluid):

        # read fluid library data from file
        fluid_library_data = app().file.read_fluid_library_from_file()

        str_fluid_id = str(fluid.identifier)
        if not str_fluid_id in fluid_library_data.keys():
            return

        # remove the selected fluid
        fluid_library_data.pop(str_fluid_id)

        # save the modified fluid data in file
        app().file.write_fluid_library_in_file(fluid_library_data)

        self.reset_fluids_from_bodies_and_surfaces([fluid.identifier])
        self.load_data_from_fluids_library()

    def cell_clicked_callback(self, row, col):
        if row == COLOR_ROW:
            self.pick_color_for_item(row, col)

    def cell_double_clicked_callback(self, row, col):
        
        try:
            identifier = int(self.tableWidget_fluid_data.item(1, col).text())
        except:
            return

        selected_fluid = self.fluids_from_library.get(identifier)
        if not isinstance(selected_fluid, Fluid):
            return

        self.tableWidget_fluid_data.blockSignals(True)
        fluid_name = self.tableWidget_fluid_data.item(0, col).text()

        if fluid_name in self.fluid_name_to_refprop_data.keys():
            if self.call_refprop_interface(selected_fluid = selected_fluid):
                self.tableWidget_fluid_data.blockSignals(False)
                return

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

    def get_new_identifiers(self, N: int):

        new_identifiers = list()
        already_used_ids = list(self.fluids_from_library.keys())
        for n in range(N):
            for i in count(1):
                if i not in already_used_ids:
                    already_used_ids.append(i)
                    new_identifiers.append(i)
                    break

        return new_identifiers

    def pick_color(self):

        if isinstance(self.dialog, QDialog):
            self.dialog.hide()

        pick = PickColorInput()
        if not pick.complete:
            return list()

        return pick.color

    def pick_color_for_item(self, row, col):

        picked_color = self.pick_color()
        if not picked_color:
            return True

        self.set_color_to_item(row, col, picked_color)
        self.tableWidget_fluid_data.item(row, 0).setSelected(True)

    def set_color_to_item(self, row: int, col: int, rgb_color: list):
        item = QTableWidgetItem()
        item.setBackground(Color(*rgb_color).to_qt())
        item.setForeground(Color(*rgb_color).to_qt())
        self.tableWidget_fluid_data.setItem(row, col, item)

    def get_confirmation_to_proceed(self):

        title = "Fluids library reset"
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

        # read fluid library data from file
        fluid_library_data = app().file.read_fluid_library_from_file()

        # get the fluid identifiers to be removed from properties
        fluid_identifiers = list()
        if isinstance(fluid_library_data, dict):
            fluid_identifiers = [int(fluid_id) for fluid_id in fluid_library_data.keys()]
       
        # reset the fluid library to default state
        default_fluid_library()

        if fluid_identifiers:
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

    def call_refprop_interface(self, selected_fluid: Fluid | None = None):

        if isinstance(self.dialog, QDialog):
            self.dialog.hide()

        self.refprop = SetFluidCompositionInputs(
                                                fluid_to_edit = selected_fluid,
                                                state_properties = self.state_properties,
                                                )

        if not self.refprop.complete:
            self.refprop = None
            app().main_window.set_input_widget(self)
            return True

        self.after_getting_fluid_properties_from_refprop()
        self.refprop = None

    def after_getting_fluid_properties_from_refprop(self):

        if not self.refprop.complete:
            return

        refprop_fluids_data = deepcopy(self.refprop.refprop_fluids_data)
        fluid_properties = refprop_fluids_data.get("properties")

        if refprop_fluids_data.get("thermodynamic_states") == "multiple_states":
            fluids_data = list(fluid_properties.values())
        else:
            fluids_data = [fluid_properties]
        
        if self.add_fluid_data_in_file(fluids_data, from_refprop=True):
            return

        self.load_data_from_fluids_library()

        app().processEvents()
        self.set_scroll_bar_to_maximum()

        self.tableWidget_fluid_data.blockSignals(False)

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