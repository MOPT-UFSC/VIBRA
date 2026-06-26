from copy import deepcopy
from enum import IntEnum
from itertools import count
from typing import Optional

from molde import Color
from molde.colors import color_names
from numpy.random import randint
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QAbstractItemDelegate, QAbstractItemView, QDialog, QHeaderView, QTableWidgetItem

from vibra import app
from vibra.interface.numeric_checks.unit_utilities import convert_pressure_unit, convert_temperature_unit
from vibra.engine.properties import FluidLibrary
from vibra.engine.properties.fluid import Fluid
from vibra.errors import InvalidFluidError
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.pick_color_input import PickColorInput
from vibra.interface.model_inputs.fluid.set_fluid_composition_inputs import SetFluidCompositionInputs
from vibra.interface.ui_generated.model.fluid.fluid_widget_ui import FluidWidget_UI
from vibra.utils.interface_utils import block_signals, qt_run_delayed



class RowsEnum(IntEnum):
    NAME = 0
    IDENTIFIER = 1
    TEMPERATURE = 2
    PRESSURE = 3
    FLUID_DENSITY = 4
    SPEED_OF_SOUND = 5
    ISENTROPIC_EXPONENT = 6
    THERMAL_CONDUCTIVITY = 7
    SPECIFIC_HEAT_CP = 8
    DYNAMIC_VISCOSITY = 9
    MOLAR_MASS = 10
    COLOR = 11


class FluidWidget(FluidWidget_UI):
    modified = Signal()

    def __init__(self, *argas, **kwargs):
        super().__init__()

        app().main_window.action_model_workspace_callback()

        self.dialog = kwargs.get("dialog", None)
        self.state_properties = kwargs.get("state_properties", dict())

        self._initialize()
        self._config_widgets()
        self._create_connections()
        self.reload_table_of_fluids()

    @ property
    def properties(self):
        return app().project.model.properties

    def _initialize(self):
        self.refprop = None
        self.refprop_fluids = dict()

    def _config_widgets(self):
        self.tableWidget_fluid_data.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_fluid_data.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectColumns)
        self.tableWidget_fluid_data.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def _create_connections(self):
        #
        self.pushButton_add_column.clicked.connect(self.add_buffer_column)
        self.pushButton_duplicate.clicked.connect(self.duplicate_selected_fluid)
        self.pushButton_remove_column.clicked.connect(self.remove_selected_fluid)
        self.pushButton_refprop.clicked.connect(self.refprop_interface_callback)
        #
        self.tableWidget_fluid_data.cellClicked.connect(self.cell_clicked_callback)
        self.tableWidget_fluid_data.cellDoubleClicked.connect(self.cell_double_clicked_callback)
        self.tableWidget_fluid_data.itemChanged.connect(self.item_changed_callback)
        self.tableWidget_fluid_data.itemDelegate().closeEditor.connect(self.cell_editor_closed_callback)

    def reload_table_of_fluids(self):
        number_of_rows = len(RowsEnum)
        number_of_cols = len(self.properties.fluid_library)
        self.refprop_fluids.clear()

        with block_signals(self.tableWidget_fluid_data):
            self.tableWidget_fluid_data.clearContents()
            self.tableWidget_fluid_data.setRowCount(number_of_rows)
            self.tableWidget_fluid_data.setColumnCount(number_of_cols)

            for j, fluid in enumerate(self.properties.fluid_library.values()):
                self._set_column_values(j, fluid)

                refprop_parameters = [
                    fluid.name,
                    fluid.temperature,
                    fluid.pressure,
                    fluid.key_mixture,
                    fluid.molar_fractions,
                    ]

                if refprop_parameters.count(None):
                    continue

                self.refprop_fluids[fluid.identifier] = refprop_parameters

                for i in range(len(RowsEnum)):
                    self.tableWidget_fluid_data.item(i, j).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            self._update_size_policy()

    def add_buffer_column(self):
        if self._has_buffer_column():
            self.scroll_to_end()
            return

        with block_signals(self.tableWidget_fluid_data):
            column_index = self._add_empty_column()
            self.scroll_to_end()

            color = Color.from_hsv(randint(0, 360), 100, 70)
            color_item = self.tableWidget_fluid_data.item(RowsEnum.COLOR, column_index)
            name_item = self.tableWidget_fluid_data.item(RowsEnum.NAME, column_index)
            identifier_item = self.tableWidget_fluid_data.item(RowsEnum.IDENTIFIER, column_index)

            if color_item is not None:
                color_item.setBackground(color.to_qt())

            if name_item is not None:
                name_item.setText("New fluid")
                self.tableWidget_fluid_data.setCurrentItem(name_item)
                self.tableWidget_fluid_data.editItem(name_item)

            if identifier_item is not None:
                new_id = self.properties.fluid_library.get_new_id()
                identifier_item.setText(str(new_id))

            if self.refprop is None:
                self.load_state_properties_in_SI_units(column_index)
                self.tableWidget_fluid_data.editItem(name_item)

            self._update_size_policy()

        self.modified.emit()

    def duplicate_selected_fluid(self):
        fluid = self.get_selected_fluid()
        if fluid is None:
            return

        new_fluid = deepcopy(fluid)
        new_fluid.identifier = self.new_identifier()
        new_fluid.name = self.properties.fluid_library.get_duplicated_name(fluid.name)

        if self.add_fluid_data_in_file([new_fluid.__dict__]):
            return

        self.reload_table_of_fluids()
        self.scroll_to_end()
        self.modified.emit()

    def remove_selected_fluid(self):
        selected_column = self._get_selected_column()
        if selected_column < 0:
            return

        fluid = self.properties.fluid_library.get_from_ordered_index(selected_column)
        if isinstance(fluid, Fluid):
            self.properties.remove_fluid(fluid)
            self.update_properties_after_fluid_removal([fluid.identifier])

        with block_signals(self.tableWidget_fluid_data):
            self.tableWidget_fluid_data.removeColumn(selected_column)

        self._update_size_policy()
        app().main_window.selection.clear_selection()
        self.modified.emit()

    def reset_library_callback(self):
        """
        Resets the library to default and removes all fluid assignments.
        """
        if not self._get_reset_library_confirmation():
            return

        fluids_to_remove = list(self.properties.fluid_library.values())
        for fluid in fluids_to_remove:
            self.properties.remove_fluid(fluid)

        self.update_properties_after_fluid_removal(fluids_to_remove)

        self.properties.fluid_library = FluidLibrary.default()
        self.reload_table_of_fluids()

        app().main_window.selection.clear_selection()
        self.modified.emit()

    def cell_clicked_callback(self, row, col):
        if row == RowsEnum.COLOR:
            self._pick_color(row, col)

    def cell_double_clicked_callback(self, row: int, col: int):

        try:
            id_item = self.tableWidget_fluid_data.item(RowsEnum.IDENTIFIER, col)
            identifier = int(id_item.text())
        except Exception:
            return

        selected_fluid = self.properties.fluid_library.get(identifier)
        if not isinstance(selected_fluid, Fluid):
            return

        if identifier not in self.refprop_fluids.keys():
            return

        if self.refprop_interface_callback(selected_fluid = selected_fluid):
            return

        # update the fluid property after editing the fluid data
        self.fluid_property_update(selected_fluid.identifier)

    def item_changed_callback(self, item: QTableWidgetItem):
        with block_signals(self.tableWidget_fluid_data):
            ...  # more validation stuff

            if self._column_has_empty_items(item.column()):
                return

            try:
                self._update_library_with_column(item.column())
                app().project.update_model_properties_file()

            except Exception as e:
                msg = f"Column {item.column()} contains unnexpected errors."
                item.setText("")
                raise InvalidFluidError(msg) from e

        self.modified.emit()
        app().main_window.update_info_text()

    def cell_editor_closed_callback(self, _widget, _hint: QAbstractItemDelegate.EndEditHint):
        n_columns = self.tableWidget_fluid_data.columnCount()
        row = self.tableWidget_fluid_data.currentRow()
        col = self.tableWidget_fluid_data.currentColumn()

        # The tabs are updated by default in a left-right, up-down order.
        # This code counteracts this default behavior, so we can customize it next.
        # If a better way to cancel the default behavior is found please replace it.
        match _hint:
            case QAbstractItemDelegate.EndEditHint.EditNextItem:
                col = (col - 1) % n_columns
                row = (row - 1) if (col == (n_columns - 1)) else row
            case QAbstractItemDelegate.EndEditHint.EditPreviousItem:
                col = (col + 1) % n_columns
                row = (row + 1) if (col == 0) else row

        # Go to next or previous cell according to the keyboard input
        with block_signals(self.tableWidget_fluid_data.itemDelegate()):
            match _hint:
                case QAbstractItemDelegate.EndEditHint.EditNextItem | QAbstractItemDelegate.EndEditHint.SubmitModelCache:
                    self.edit_cell(row + 1, col)
                case QAbstractItemDelegate.EndEditHint.EditPreviousItem:
                    self.edit_cell(row - 1, col)

    @qt_run_delayed
    def edit_cell(self, row: int, col: int):
        if not (0 <= row < len(RowsEnum)):
            return

        item = self.tableWidget_fluid_data.item(row, col)
        if item is None:
            return

        if row == RowsEnum.COLOR:
            self._pick_color(row, col)
        else:
            self.tableWidget_fluid_data.setCurrentItem(item)
            self.tableWidget_fluid_data.editItem(item)

    def scroll_to_start(self):
        scroll_bar = self.tableWidget_fluid_data.horizontalScrollBar()
        scroll_bar.setSliderPosition(scroll_bar.minimum())

    def scroll_to_end(self):
        scroll_bar = self.tableWidget_fluid_data.horizontalScrollBar()
        scroll_bar.setSliderPosition(scroll_bar.minimum())
        app().processEvents()
        scroll_bar.setSliderPosition(scroll_bar.maximum())

    def get_selected_fluid(self) -> Optional[Fluid]:
        selected_column = self._get_selected_column()
        if selected_column < 0:
            return

        return self.properties.fluid_library.get_from_ordered_index(selected_column)

    def _hide_parent_dialog(self):
        window = self.nativeParentWidget()
        if isinstance(window, QDialog):
            window.hide()

    def _get_reset_library_confirmation(self):
        title = "Fluids library reset"
        message = "Would you like to reset the fluid library to default?"
        buttons_config = {
            "left_button_label": "No",
            "right_button_label": "Yes",
            "left_button_size": 80,
            "right_button_size": 80,
        }

        read = GetUserConfirmationInput(
            title,
            message,
            buttons_config=buttons_config,
        )

        if read._cancel:
            return False

        if read._continue:
            return True

    def _update_library_with_column(self, col: int):
        fluid_library = self.properties.fluid_library
        fluid = fluid_library.get_from_ordered_index(col)
        if fluid is None:
            # Create a temporary fluid to be updated
            fluid = Fluid()
            fluid_library.add(fluid)

        def to_num(val: str) -> int | float:
            val = val.strip()
            return int(val) if val.isdigit() else float(val)

        for row in RowsEnum:
            item = self.tableWidget_fluid_data.item(row, col)
            if item is None:
                continue

            text = item.text()
            match row:
                case RowsEnum.NAME:
                    fluid.name = text
                case RowsEnum.IDENTIFIER:
                    item.setText(str(fluid.identifier))
                case RowsEnum.COLOR:
                    fluid.color = Color(item.background().color()).to_rgb()
                case RowsEnum.TEMPERATURE:
                    fluid.temperature = to_num(text)
                case RowsEnum.PRESSURE:
                    fluid.pressure = to_num(text)
                case RowsEnum.FLUID_DENSITY:
                    fluid.fluid_density = to_num(text)
                case RowsEnum.SPEED_OF_SOUND:
                    fluid.speed_of_sound = to_num(text)
                case RowsEnum.ISENTROPIC_EXPONENT:
                    fluid.isentropic_exponent = to_num(text)
                case RowsEnum.THERMAL_CONDUCTIVITY:
                    fluid.thermal_conductivity = to_num(text)
                case RowsEnum.SPECIFIC_HEAT_CP:
                    fluid.specific_heat_Cp = to_num(text)
                case RowsEnum.DYNAMIC_VISCOSITY:
                    fluid.dynamic_viscosity = to_num(text)
                case RowsEnum.MOLAR_MASS:
                    fluid.molar_mass = to_num(text)
        
        self._set_column_values(col, fluid)

    def _column_has_empty_items(self, col: int):
        for row in RowsEnum:
            if row == RowsEnum.COLOR:
                continue

            item = self.tableWidget_fluid_data.item(row, col)
            if item is None:
                return True

            if item.text().strip() == "":
                return True

        return False

    def _pick_color(self, row: int, col: int):

        window = self.nativeParentWidget()
        if isinstance(window, QDialog):
            window.hide()

        item = self.tableWidget_fluid_data.item(row, col)

        if item is None:
            read = PickColorInput()
        else:
            color = Color(item.background().color())
            read = PickColorInput(initial_color=color)

        if not read.complete:
            return True

        picked_color = read.color
        item = QTableWidgetItem()
        item.setBackground(Color(*picked_color).to_qt())
        item.setForeground(Color(*picked_color).to_qt())
        self.tableWidget_fluid_data.setItem(row, col, item)
        self.tableWidget_fluid_data.clearSelection()

    def _get_selected_column(self) -> int:
        selected_items = self.tableWidget_fluid_data.selectedIndexes()
        if not selected_items:
            return -1
        return selected_items[-1].column()

    def _has_buffer_column(self):
        return self.tableWidget_fluid_data.columnCount() > len(self.properties.fluid_library)

    def _add_empty_column(self):
        column_index = len(self.properties.fluid_library)
        self.tableWidget_fluid_data.setColumnCount(column_index + 1)

        for i in range(self.tableWidget_fluid_data.rowCount()):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(color_names.GRAY_5.to_qt())
            self.tableWidget_fluid_data.setItem(i, column_index, item)

        return column_index

    def _set_column_values(
        self,
        column: int,
        fluid: Fluid,
    ):
        attributes = [
            fluid.name,
            fluid.identifier,
            round(fluid.temperature, 6),
            f"{fluid.pressure:.6e}",
            f"{fluid.fluid_density:.6f}",
            f"{fluid.speed_of_sound:.6f}",
            f"{fluid.isentropic_exponent:.6f}",
            f"{fluid.thermal_conductivity:.6e}",
            f"{fluid.specific_heat_Cp:.6e}",
            f"{fluid.dynamic_viscosity:.6e}",
            f"{fluid.molar_mass:.3f}",
            Color(*fluid.color),
        ]

        for i, value in enumerate(attributes):
            item = QTableWidgetItem()
            self.tableWidget_fluid_data.setItem(i, column, item)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setSizeHint(QSize(80, 30))

            if isinstance(value, Color):
                item.setBackground(value.to_qt())
                item.setForeground(value.to_qt())
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            else:
                item.setText(str(value))

    def _update_size_policy(self):
        if len(self.properties.fluid_library) > 6:
            self.tableWidget_fluid_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        else:
            self.tableWidget_fluid_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)





    ##TODO: the lines above have been added recently, Please, review them.

    def fluid_property_update(self, fluid_id: int):

        was_updated = False
        fluid_to_update = self.properties.fluid_library.get(fluid_id)
    
        for (prop, vol_id), data in deepcopy(self.properties.volume_properties).items():
            if prop != "fluid":
                continue

            if not isinstance(data, Fluid):
                continue

            if not data.identifier == fluid_to_update.identifier:
                continue
    
            was_updated = True
            self.properties._set_property("fluid", fluid_to_update, volume=vol_id)

            for surf_id in app().project.model.mesh.surfaces_from_volume.get(vol_id):
                self.properties._set_property("fluid", fluid_to_update, surface=surf_id)

        if was_updated:
            app().project.update_model_properties_file()

    def update_properties_after_fluid_removal(self, fluid_identifiers : list):

        surfaces_to_remove_fluid = list()
        volumes_to_remove_fluid = list()

        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property != "fluid":
                continue
        
            if not isinstance(data, Fluid):
                continue
    
            if data.identifier not in fluid_identifiers:
                continue

            volumes_to_remove_fluid.append(volume_id)
            surface_ids = app().project.model.mesh.surfaces_from_volume[volume_id]
            for surface_id in surface_ids:
                surfaces_to_remove_fluid.append(surface_id)

        for vol_id in volumes_to_remove_fluid:
            self.properties._remove_volume_property("fluid", volume_id=vol_id)

        for surf_id in surfaces_to_remove_fluid:
            self.properties._remove_surface_property("fluid", surface_id=surf_id)

        app().project.update_model_properties_file()

    def refprop_interface_callback(self, selected_fluid: Fluid | None = None):

        self._hide_parent_dialog()

        self.refprop = SetFluidCompositionInputs(
            fluid_to_edit = selected_fluid,
            state_properties = self.state_properties,
            )

        if not self.refprop.complete:
            self.refprop = None
            app().main_window.set_input_widget(self)
            return True

        self.postproc_refprop_fluid_properties()
        self.refprop = None

    def postproc_refprop_fluid_properties(self):

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

        self.scroll_to_end()
        self.reload_table_of_fluids()

        if not self.state_properties:
            return

        self.load_state_properties_info()

        window = self.nativeParentWidget()
        if isinstance(window, QDialog):
            last_col = self.tableWidget_fluid_data.columnCount()
            self.tableWidget_fluid_data.selectColumn(last_col - 1)

    def new_identifier(self):

        already_used_ids = set()
        for fluid in self.properties.fluid_library.values():
            fluid: Fluid
            already_used_ids.add(fluid.identifier)

        for i in count(1):
            if i not in already_used_ids:
                return i

    def pick_color(self):

        self._hide_parent_dialog()

        pick = PickColorInput()
        if not pick.complete:
            return list()

        return pick.color

    def add_fluid_data_in_file(self, fluids_data: list, from_refprop: bool=False):

        fluid_data_keys = [
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
            "color",
            ]

        # read fluid library data from file
        fluid_library = self.properties.fluid_library

        # get list of new fluid identifiers
        identifiers = self.get_new_identifiers(len(fluids_data))

        for j, fluid_data in enumerate(fluids_data):

            filtered_fluid_data = dict()

            # check all inputs before proceeding
            for key in fluid_data_keys:
                value = fluid_data.get(key)

                if value is None:
                    if key == "identifier" and from_refprop:
                        filtered_fluid_data["identifier"] = identifiers[j]
                        continue

                    elif key == "color":
                        picked_color = self.pick_color()
                        if picked_color:
                            filtered_fluid_data[key] = picked_color
                        continue

                    return True

                filtered_fluid_data[key] = value

            # additionally, check all refprop inputs before proceeding    
            if from_refprop:
                for key in ["key_mixture", "molar_fractions"]:
                    value = fluid_data.get(key)
                    if value is None:
                        return True
                    filtered_fluid_data[key] = value

            # fluid identifier
            identifier = filtered_fluid_data.get("identifier")
        
            # add the new fluid data
            fluid_library[identifier] = Fluid(**filtered_fluid_data)

        # save the modified fluid data in file
        app().project.update_model_properties_file()

    def get_new_identifiers(self, N: int):

        new_identifiers = list()
        already_used_ids = list(self.properties.fluid_library.keys())
        for n in range(N):
            for i in count(1):
                if i not in already_used_ids:
                    already_used_ids.append(i)
                    new_identifiers.append(i)
                    break

        return new_identifiers

    def load_state_properties_info(self):

        if not isinstance(self.state_properties, dict):
            return

        if not self.state_properties:
            return

        source = self.state_properties.get("source", None)
        if source is None:
            return

        window = self.nativeParentWidget()
        if not isinstance(window, QDialog):
            return

        surface_id = self.state_properties.get("surface_id", None)
        if not isinstance(surface_id, int):
            return

        app().main_window.selection.set_geometry_selection(surfaces=[surface_id])

        connection_type = self.state_properties.get('connection_type')
        if source == "reciprocating_pump":
            title = f"Set a fluid for the reciprocating pump ({connection_type})"

        elif source == "reciprocating_compressor":
            title = f"Set a fluid for the reciprocating compressor ({connection_type})"

        window.setWindowTitle(title)

    def load_state_properties_in_SI_units(self, column_index: int):
        """
        This method returns the state properties in SI unit system.
        """
        if not isinstance(self.state_properties, dict):
            return

        if not self.state_properties:
            return

        if self.state_properties.get('source') is None:
            return

        connection_type = self.state_properties.get("connection_type")
        if connection_type == "discharge":
            pressure = self.state_properties.get("discharge_pressure")
            temperature = self.state_properties.get("discharge_temperature")

        else:
            pressure = self.state_properties.get("suction_pressure")
            temperature = self.state_properties.get("suction_temperature")

        pressure_unit = self.state_properties.get("pressure_unit")
        temperature_unit = self.state_properties.get("temperature_unit")

        pressure_Pa = convert_pressure_unit(pressure, pressure_unit, "Pa")
        temperature_K = convert_temperature_unit(temperature, temperature_unit, "K")

        self.tableWidget_fluid_data.item(3, column_index).setText(f"{pressure_Pa : .8e}")
        self.tableWidget_fluid_data.item(2, column_index).setText(f"{temperature_K : .8f}")

        isentropic_exponent = self.state_properties.get("isentropic_exponent")
        if isinstance(isentropic_exponent, float):
            self.tableWidget_fluid_data.item(6, column_index).setText(f"{isentropic_exponent}")

        molar_mass = self.state_properties.get("molar_mass")
        if isinstance(molar_mass, float):
            self.tableWidget_fluid_data.item(11, column_index).setText(f"{molar_mass}")

    def keyPressEvent(self, event):
        window = self.nativeParentWidget()
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if isinstance(window, QDialog):
                window.attribute_callback()

        elif event.key() == Qt.Key_Delete:
            self.remove_selected_fluid()

        elif event.key() == Qt.Key_Escape:
            if isinstance(window, QDialog):
                window.close()
            else:
                self.close()