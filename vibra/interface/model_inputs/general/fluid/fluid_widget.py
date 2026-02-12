from copy import deepcopy
from enum import IntEnum
from itertools import count
from typing import Optional

from molde import Color
from molde.colors import color_names
from numpy.random import randint
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QAbstractItemDelegate, QAbstractItemView, QDialog, QHeaderView, QTableWidgetItem

from vibra import app
from vibra.engine.properties.fluid import Fluid
from vibra.errors import InvalidFluidError
from vibra.interface.formatters.icons import change_icon_color_for_widgets
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.pick_color_input import PickColorInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.general.fluid.set_fluid_composition_inputs import SetFluidCompositionInputs
from vibra.interface.ui_generated.model.setup.fluid.fluid_widget_ui import FluidWidget_UI
from vibra.libraries.default_libraries import default_fluid_library
from vibra.utils.interface_utils import block_signals, qt_run_delayed

error_title = "Error"
warning_title = "Warning"

COLOR_ROW = 11


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
    def __init__(self, *argas, **kwargs):
        super().__init__()

        app().main_window.action_model_workspace_callback()

        # self.dialog = kwargs.get("dialog", None)
        # self.state_properties = kwargs.get("state_properties", dict())

        # self.model = app().new_project.model
        # self.properties = app().new_project.model.properties

        # self._initialize()
        # self._configure_qt_variables()
        self._create_connections()
        self._config_widgets()
        # self._paint_icons()
        # self.load_data_from_fluids_library()

        self.reload_table_of_fluids()

    def _create_connections(self):
        #
        self.pushButton_add_column.clicked.connect(self.add_buffer_column)
        self.pushButton_duplicate.clicked.connect(self.duplicate_selected_fluid)
        self.pushButton_remove_column.clicked.connect(self.remove_selected_fluid)
        # self.pushButton_refprop.clicked.connect(self.call_refprop_interface)
        #
        self.tableWidget_fluid_data.cellClicked.connect(self.cell_clicked_callback)
        self.tableWidget_fluid_data.itemChanged.connect(self.item_changed_callback)
        # self.tableWidget_fluid_data.cellDoubleClicked.connect(self.cell_double_clicked_callback)
        self.tableWidget_fluid_data.itemDelegate().closeEditor.connect(self.cell_editor_closed_callback)

    def _config_widgets(self):
        self.tableWidget_fluid_data.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_fluid_data.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectColumns)
        self.tableWidget_fluid_data.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def reload_table_of_fluids(self):
        properties = app().new_project.model.properties
        number_of_rows = len(RowsEnum)
        number_of_cols = len(properties.fluid_library)

        with block_signals(self.tableWidget_fluid_data):
            self.tableWidget_fluid_data.clearContents()
            self.tableWidget_fluid_data.setRowCount(number_of_rows)
            self.tableWidget_fluid_data.setColumnCount(number_of_cols)

            for i, fluid in enumerate(properties.fluid_library.values()):
                self._set_column_values(i, fluid)

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

            if color_item is not None:
                color_item.setBackground(color.to_qt())

            if name_item is not None:
                name_item.setText("New fluid")
                self.tableWidget_fluid_data.setCurrentItem(name_item)
                self.tableWidget_fluid_data.editItem(name_item)

    def duplicate_selected_fluid(self):
        fluid = self.get_selected_fluid()
        if fluid is None:
            return

        properties = app().new_project.model.properties
        new_fluid = fluid.copy()
        new_fluid.name = properties.fluid_library.get_dupplicated_name(fluid.name)
        properties.fluid_library.add(new_fluid)

        self.reload_table_of_fluids()
        self.scroll_to_end()

    def remove_selected_fluid(self):
        selected_column = self._get_selected_column()
        if selected_column < 0:
            return

        properties = app().new_project.model.properties
        fluid = properties.fluid_library.get_from_ordered_index(selected_column)
        if fluid is not None:
            properties.remove_fluid(fluid)

        with block_signals(self.tableWidget_fluid_data):
            self.tableWidget_fluid_data.removeColumn(selected_column)

        app().main_window.selection.clear_selection()

    def cell_clicked_callback(self, row, col):
        if row == RowsEnum.COLOR:
            self._pick_color(row, col)

    def item_changed_callback(self, item: QTableWidgetItem):
        with block_signals(self.tableWidget_fluid_data):
            ...  # more validation stuff

            if self._column_has_empty_items(item.column()):
                return

            try:
                self._update_library_with_column(item.column())
            except Exception as e:
                msg = f"Column {item.column()} contains unnexpected errors."
                item.setText("")
                raise InvalidFluidError(msg) from e

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

        properties = app().new_project.model.properties
        return properties.fluid_library.get_from_ordered_index(selected_column)

    def _update_library_with_column(self, col: int):
        fluid_library = app().new_project.model.properties.fluid_library
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

    def _get_selected_column(self) -> int:
        selected_items = self.tableWidget_fluid_data.selectedIndexes()
        if not selected_items:
            return -1
        return selected_items[-1].column()

    def _has_buffer_column(self):
        properties = app().new_project.model.properties
        return self.tableWidget_fluid_data.columnCount() > len(properties.fluid_library)

    def _add_empty_column(self):
        properties = app().new_project.model.properties
        column_index = len(properties.fluid_library)
        self.tableWidget_fluid_data.setColumnCount(column_index + 1)

        for i in range(self.tableWidget_fluid_data.rowCount()):
            item = QTableWidgetItem()
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
        properties = app().new_project.model.properties

        if len(properties.fluid_library) > 6:
            self.tableWidget_fluid_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        else:
            self.tableWidget_fluid_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # def _initialize(self):

    #     self.row = None
    #     self.col = None
    #     self.refprop = None

    #     self.refprop_fluids_data = dict()
    #     self.fluids_from_library = dict()
    #     self.fluid_name_to_refprop_data = dict()

    #     self.fluid_data_keys = [
    #                             "name",
    #                             "identifier",
    #                             "temperature",
    #                             "pressure",
    #                             "fluid_density",
    #                             "speed_of_sound",
    #                             "isentropic_exponent",
    #                             "thermal_conductivity",
    #                             "specific_heat_Cp",
    #                             "dynamic_viscosity",
    #                             "molar_mass",
    #                             "color"
    #                             ]

    # def _configure_qt_variables(self):
    #     self.tableWidget_fluid_data.setStyleSheet("")

    # def _config_window(self):
    #     self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
    #     self.setWindowModality(Qt.ApplicationModal)
    #     self.setWindowIcon(app().main_window.vibra_icon)
    #     self.setWindowTitle("Vibra")

    # def _config_widgets(self):
    #     self.tableWidget_fluid_data.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))

    # def _paint_icons(self):
    #     icon_color = None
    #     theme = app().config.user_preferences.interface_theme
    #     from vibra import DARK_ICON_COLOR, LIGHT_ICON_COLOR
    #     if theme == "dark":
    #         icon_color = DARK_ICON_COLOR.to_qt()
    #     else:
    #         icon_color = LIGHT_ICON_COLOR.to_qt()

    #     widgets = [self.pushButton_duplicate]
    #     change_icon_color_for_widgets(widgets, icon_color)

    # def _add_icon_and_title(self):
    #     self._config_window()

    # def load_data_from_fluids_library(self):

    #     self.fluids_from_library.clear()
    #     self.fluid_name_to_refprop_data.clear()

    #     fluids_from_library = app().load_project.load_fluid_library()
    #     if fluids_from_library is None:
    #         self.reset_library_to_default()
    #         return

    #     elif isinstance(fluids_from_library, dict):
    #         if not fluids_from_library:
    #             self.reset_library_to_default()
    #             return

    #     self.fluids_from_library = fluids_from_library

    #     for fluid in fluids_from_library.values():
    #         if not isinstance(fluid, Fluid):
    #             continue

    #         refprop_parameters = [
    #                               fluid.name,
    #                               fluid.temperature,
    #                               fluid.pressure,
    #                               fluid.key_mixture,
    #                               fluid.molar_fractions
    #                               ]

    #         if refprop_parameters.count(None) == 0:
    #             self.fluid_name_to_refprop_data[fluid.name] = refprop_parameters

    #     self.update_table_of_fluids()

    # def update_table_of_fluids(self):

    #     self.tableWidget_fluid_data.clearContents()
    #     self.tableWidget_fluid_data.blockSignals(True)
    #     self.tableWidget_fluid_data.setRowCount(COLOR_ROW + 1)
    #     self.tableWidget_fluid_data.setColumnCount(len(self.fluids_from_library))

    #     for j, fluid in enumerate(self.fluids_from_library.values()):
    #         if isinstance(fluid, Fluid):

    #             self.tableWidget_fluid_data.setItem( 0, j, QTableWidgetItem(str(fluid.name)))
    #             self.tableWidget_fluid_data.setItem( 1, j, QTableWidgetItem(f"{fluid.identifier}"))
    #             self.tableWidget_fluid_data.setItem( 2, j, QTableWidgetItem(f"{round(fluid.temperature, 6)}"))
    #             self.tableWidget_fluid_data.setItem( 3, j, QTableWidgetItem(f"{fluid.pressure : .6e}"))
    #             self.tableWidget_fluid_data.setItem( 4, j, QTableWidgetItem(f"{fluid.fluid_density : .6f}"))
    #             self.tableWidget_fluid_data.setItem( 5, j, QTableWidgetItem(f"{fluid.speed_of_sound : .6f}"))
    #             self.tableWidget_fluid_data.setItem( 6, j, QTableWidgetItem(f"{fluid.isentropic_exponent : .6f}"))
    #             self.tableWidget_fluid_data.setItem( 7, j, QTableWidgetItem(f"{fluid.thermal_conductivity : .6e}"))
    #             self.tableWidget_fluid_data.setItem( 8, j, QTableWidgetItem(f"{fluid.specific_heat_Cp : .6e}"))
    #             self.tableWidget_fluid_data.setItem( 9, j, QTableWidgetItem(f"{fluid.dynamic_viscosity : .6e}"))
    #             self.tableWidget_fluid_data.setItem(10, j, QTableWidgetItem(f"{fluid.molar_mass : .3f}"))

    #             item = QTableWidgetItem()
    #             item.setBackground(Color(*fluid.color).to_qt())
    #             item.setForeground(Color(*fluid.color).to_qt())
    #             self.tableWidget_fluid_data.setItem(COLOR_ROW, j, item)

    #             if fluid.name in self.fluid_name_to_refprop_data.keys():
    #                 for i in range(11):
    #                     self.tableWidget_fluid_data.item(i, j).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    #     for i in range(self.tableWidget_fluid_data.rowCount()):
    #         for j in range(self.tableWidget_fluid_data.columnCount()):
    #             self.tableWidget_fluid_data.item(i, j).setTextAlignment(Qt.AlignCenter)

    #     self.tableWidget_fluid_data.blockSignals(False)
    #     self._update_size_policy()

    # def get_selected_column(self) -> int:
    #     selected_items = self.tableWidget_fluid_data.selectedIndexes()
    #     if not selected_items:
    #         return -1
    #     return selected_items[-1].column()

    # def get_selected_fluid(self) -> Fluid | None:

    #     selected_column = self.get_selected_column()
    #     if selected_column < 0:
    #         return

    #     if selected_column >= len(self.fluids_from_library):
    #         return

    #     item = self.tableWidget_fluid_data.item(1, selected_column)
    #     identifier = int(item.text())

    #     return self.fluids_from_library.get(identifier)

    # def add_column(self, single_add: bool = True):

    #     self.tableWidget_fluid_data.blockSignals(True)

    #     table_size = self.tableWidget_fluid_data.columnCount()
    #     if table_size > len(self.fluids_from_library) and single_add:
    #         # it means that if you already have a new row
    #         # to insert data you don't need another one
    #         self.tableWidget_fluid_data.blockSignals(False)
    #         return

    #     last_col = self.tableWidget_fluid_data.columnCount()
    #     self.tableWidget_fluid_data.insertColumn(last_col)

    #     for i in range(self.tableWidget_fluid_data.rowCount()):
    #         item = QTableWidgetItem()
    #         item.setSizeHint(QSize(80, 30))
    #         self.tableWidget_fluid_data.setItem(i, last_col, item)
    #         self.tableWidget_fluid_data.item(i, last_col).setTextAlignment(Qt.AlignCenter)

    #     self.tableWidget_fluid_data.selectColumn(last_col)
    #     first_item = self.tableWidget_fluid_data.item(0, last_col)
    #     if self.refprop is None:
    #         self.tableWidget_fluid_data.editItem(first_item)

    #     self.tableWidget_fluid_data.blockSignals(False)

    # def remove_selected_column(self):

    #     selected_column = self.get_selected_column()
    #     if selected_column < 0:
    #         return

    #     if selected_column >= len(self.fluids_from_library):
    #         # if it is the last item and a not an already configured
    #         # fluid, just remove the last line
    #         current_size = self.tableWidget_fluid_data.columnCount()
    #         self.tableWidget_fluid_data.setColumnCount(current_size - 1)

    #         self._update_size_policy()
    #         self.tableWidget_fluid_data.horizontalScrollBar().setSliderPosition(0)
    #         return

    #     item = self.tableWidget_fluid_data.item(1, selected_column)
    #     identifier = int(item.text())
    #     fluid = self.fluids_from_library.get(identifier)

    #     self.remove_fluid_from_file(fluid)
    #     self._update_size_policy()

    #     self.tableWidget_fluid_data.horizontalScrollBar().setSliderPosition(0)

    # def duplicate_selected_fluid(self):

    #     selected_column = self.get_selected_column()
    #     if selected_column < 0:
    #         return

    #     self.refprop = None
    #     item = self.tableWidget_fluid_data.item(1, selected_column)
    #     if item.text() == "":
    #         return

    #     identifier = int(item.text())
    #     fluid = self.fluids_from_library.get(identifier)
    #     if not isinstance(fluid, Fluid):
    #         return

    #     dfluid = deepcopy(fluid)
    #     dfluid.identifier = self.new_identifier()
    #     dfluid.name = self.get_suffix_for_duplicated_fluid(dfluid.name)

    #     fluid_data = dfluid.__dict__

    #     # fluid_data = {
    #     #             "name" : dfluid.name,
    #     #             "identifier" : dfluid.identifier,
    #     #             "temperature" : dfluid.temperature,
    #     #             "pressure" : dfluid.pressure,
    #     #             "fluid_density" : dfluid.fluid_density,
    #     #             "speed_of_sound" : dfluid.speed_of_sound,
    #     #             "isentropic_exponent" : dfluid.isentropic_exponent,
    #     #             "thermal_conductivity" : dfluid.thermal_conductivity,
    #     #             "specific_heat_Cp" : dfluid.specific_heat_Cp,
    #     #             "dynamic_viscosity" : dfluid.dynamic_viscosity,
    #     #             "molar_mass" : dfluid.molar_mass,
    #     #             "color" : dfluid.color,
    #     #             }

    #     if self.add_fluid_data_in_file([fluid_data]):
    #         return

    #     self.load_data_from_fluids_library()

    #     app().processEvents()
    #     self.set_scroll_bar_to_maximum()

    # def get_suffix_for_duplicated_fluid(self, fluid_name: str):

    #     already_used_names = set()
    #     for fluid in self.fluids_from_library.values():
    #         fluid: Fluid
    #         if fluid_name in fluid.name:
    #             already_used_names.add(fluid.name)

    #     for i in count(1):
    #         new_name = f"{fluid_name} ({i})"
    #         if new_name not in already_used_names:
    #             return new_name

    # def set_scroll_bar_to_maximum(self):
    #     scroll_bar = self.tableWidget_fluid_data.horizontalScrollBar()
    #     scroll_bar.setSliderPosition(scroll_bar.minimum())
    #     app().processEvents()
    #     scroll_bar.setSliderPosition(scroll_bar.maximum())

    # def item_changed_callback(self, item):

    #     self.tableWidget_fluid_data.blockSignals(True)

    #     if item.row() == 0:
    #         if self.column_has_invalid_name(item.column()):
    #             self.tableWidget_fluid_data.blockSignals(False)
    #             return

    #     elif item.row() == 1:
    #         if self.column_has_invalid_identifier(item.column()):
    #             self.tableWidget_fluid_data.blockSignals(False)
    #             return

    #     else:
    #         if self.item_is_invalid_number(item):
    #             self.tableWidget_fluid_data.blockSignals(False)
    #             return

    #     self.go_to_next_cell(item)
    #     if self.column_has_empty_items(item.column()):
    #         self.tableWidget_fluid_data.blockSignals(False)
    #         return

    #     fluid_data = self.get_fluid_data_for_selected_column(item.column())
    #     if self.add_fluid_data_in_file([fluid_data]):
    #         return

    #     self.load_data_from_fluids_library()

    #     self.tableWidget_fluid_data.blockSignals(False)

    # def go_to_next_cell(self, item):

    #     row = item.row()
    #     column = item.column()

    #     if row < COLOR_ROW - 1:
    #         next_item = self.tableWidget_fluid_data.item(row + 1, column)
    #         if next_item.text() == "":
    #             self.tableWidget_fluid_data.setCurrentItem(next_item)
    #             self.tableWidget_fluid_data.editItem(next_item)

    #     elif row == COLOR_ROW - 1:
    #         self.pick_color_for_item(row + 1, column)

    # def column_has_invalid_name(self, column):

    #     item = self.tableWidget_fluid_data.item(0, column)
    #     if item is None:
    #         return True

    #     column_name = item.text()

    #     if not column_name:
    #         return True

    #     for fluid in self.fluids_from_library.values():
    #         if fluid.name == column_name:
    #             return True

    #     return False

    # def column_has_invalid_identifier(self, column):

    #     item = self.tableWidget_fluid_data.item(1, column)

    #     already_used_ids = set()
    #     for fluid in self.fluids_from_library.values():
    #         already_used_ids.add(fluid.identifier)

    #     if item.text() == "":
    #         return True

    #     try:
    #         if int(item.text()) in already_used_ids:
    #             item.setText("")
    #             return True
    #     except:
    #         item.setText("")
    #         return True

    # def column_has_empty_items(self, column):
    #     for row in range(COLOR_ROW + 1):

    #         item = self.tableWidget_fluid_data.item(row, column)
    #         if item is None:
    #             return True

    #         if row == COLOR_ROW:
    #             color = item.background().color().getRgb()
    #             if list(color) == 0:
    #                 return True

    #         elif item.text() == "":
    #             return True

    #     return False

    # def item_is_invalid_number(self, item):

    #     if item is None:
    #         return True

    #     row = item.row()
    #     if row == COLOR_ROW:
    #         return

    #     prop_labels = {
    #                     2 : "temperature",
    #                     3 : "pressure",
    #                     4 : "fluid_density",
    #                     5 : "speed_of_sound",
    #                     6 : "isentropic_exponent",
    #                     7 : "thermal_conductivity",
    #                     8 : "specific_heat_Cp",
    #                     9 : "dynamic_viscosity",
    #                    10 : "molar_mass"
    #                 }

    #     if row not in prop_labels.keys():
    #         return True

    #     if item.text() == "":
    #         return True

    #     try:

    #         str_value = item.text().replace(",", ".")
    #         item.setText(str_value)
    #         value = float(str_value)

    #     except Exception as error_log:
    #         title = "Invalid real number"
    #         message = f"The value typed for '{prop_labels[row]}' "
    #         message += "must be a non-zero positive number.\n\n"
    #         message += f"Details: {error_log}"
    #         PrintMessageInput([error_title, title, message])
    #         item.setText("")
    #         return True

    #     if value < 0:
    #         title = "Negative value not allowed"
    #         message = f"The value typed for '{prop_labels[row]}' must be a non-zero positive number."
    #         PrintMessageInput([error_title, title, message])
    #         item.setText("")
    #         return True

    #     return False

    # def add_fluid_data_in_file(self, fluids_data: list, from_refprop: bool=False):

    #     # read fluid library data from file
    #     fluid_library_data = app().file.read_fluid_library_from_file()

    #     # get list of new fluid identifiers
    #     identifiers = self.get_new_identifiers(len(fluids_data))

    #     for j, fluid_data in enumerate(fluids_data):
    #         filt_fluid_data = dict()

    #         # check all inputs before proceeding
    #         for key in self.fluid_data_keys:
    #             value = fluid_data.get(key)
    #             if value is None:
    #                 if key == "identifier" and from_refprop:
    #                     filt_fluid_data["identifier"] = identifiers[j]
    #                     continue
    #                 elif key == "color":
    #                     filt_fluid_data[key] = self.pick_color()
    #                     continue
    #                 return True

    #             filt_fluid_data[key] = value

    #         # additionally, check all refprop inputs before proceeding
    #         if from_refprop:
    #             for key in ["key_mixture", "molar_fractions"]:
    #                 value = fluid_data.get(key)
    #                 if value is None:
    #                     return True
    #                 filt_fluid_data[key] = value

    #         # fluid identifier
    #         identifier = filt_fluid_data.get("identifier")

    #         # add the new fluid data
    #         fluid_library_data[identifier] = filt_fluid_data

    #     # save the modified fluid data in file
    #     app().file.write_fluid_library_in_file(fluid_library_data)

    # def get_fluid_data_for_selected_column(self, column: int):
    #     try:

    #         fluid_data = dict()
    #         for i, key in enumerate(self.fluid_data_keys):
    #             item = self.tableWidget_fluid_data.item(i, column)
    #             if key == "name":
    #                 fluid_data[key] = item.text()

    #             elif key == "color":
    #                 color = item.background().color().getRgb()
    #                 fluid_data[key] = list(color[:3])

    #             elif key == "identifier":
    #                 identifier = int(item.text())
    #                 fluid_data[key] = identifier

    #             else:
    #                 fluid_data[key] = float(item.text())

    #         if self.refprop is not None:
    #             fluid_data['key_mixture'] = self.refprop_fluids_data.get("key_mixture")
    #             fluid_data['molar_fractions'] = self.refprop_fluids_data.get("molar_fractions")
    #             fluid_data['molar_mass'] = round(self.refprop_fluids_data.get("molar_mass"), 6)

    #         return fluid_data

    #     except Exception as error_log:
    #         title = "Error while writing fluid data in file"
    #         message = str(error_log)
    #         PrintMessageInput([error_title, title, message])
    #         return None

    # def remove_fluid_from_file(self, fluid: Fluid):

    #     # read fluid library data from file
    #     fluid_library_data = app().file.read_fluid_library_from_file()

    #     str_fluid_id = str(fluid.identifier)
    #     if not str_fluid_id in fluid_library_data.keys():
    #         return

    #     # remove the selected fluid
    #     fluid_library_data.pop(str_fluid_id)

    #     # save the modified fluid data in file
    #     app().file.write_fluid_library_in_file(fluid_library_data)

    #     self.reset_fluids_from_bodies_and_surfaces([fluid.identifier])
    #     self.load_data_from_fluids_library()

    # def cell_clicked_callback(self, row, col):
    #     if row == COLOR_ROW:
    #         self.pick_color_for_item(row, col)

    # def cell_double_clicked_callback(self, row, col):

    #     try:
    #         identifier = int(self.tableWidget_fluid_data.item(1, col).text())
    #     except:
    #         return

    #     selected_fluid = self.fluids_from_library.get(identifier)
    #     if not isinstance(selected_fluid, Fluid):
    #         return

    #     self.tableWidget_fluid_data.blockSignals(True)
    #     fluid_name = self.tableWidget_fluid_data.item(0, col).text()

    #     if fluid_name in self.fluid_name_to_refprop_data.keys():
    #         if self.call_refprop_interface(selected_fluid = selected_fluid):
    #             self.tableWidget_fluid_data.blockSignals(False)
    #             return

    #     self.tableWidget_fluid_data.selectColumn(col)
    #     self.tableWidget_fluid_data.blockSignals(False)

    # def new_identifier(self):

    #     already_used_ids = set()
    #     for fluid in self.fluids_from_library.values():
    #         fluid: Fluid
    #         already_used_ids.add(fluid.identifier)

    #     for i in count(1):
    #         if i not in already_used_ids:
    #             return i

    # def get_new_identifiers(self, N: int):

    #     new_identifiers = list()
    #     already_used_ids = list(self.fluids_from_library.keys())
    #     for n in range(N):
    #         for i in count(1):
    #             if i not in already_used_ids:
    #                 already_used_ids.append(i)
    #                 new_identifiers.append(i)
    #                 break

    #     return new_identifiers

    # def pick_color(self):

    #     if isinstance(self.dialog, QDialog):
    #         self.dialog.hide()

    #     pick = PickColorInput()
    #     if not pick.complete:
    #         return list()

    #     return pick.color

    # def pick_color_for_item(self, row, col):

    #     picked_color = self.pick_color()
    #     if not picked_color:
    #         return True

    #     self.set_color_to_item(row, col, picked_color)
    #     self.tableWidget_fluid_data.item(row, 0).setSelected(True)

    # def set_color_to_item(self, row: int, col: int, rgb_color: list):
    #     item = QTableWidgetItem()
    #     item.setBackground(Color(*rgb_color).to_qt())
    #     item.setForeground(Color(*rgb_color).to_qt())
    #     self.tableWidget_fluid_data.setItem(row, col, item)

    # def get_confirmation_to_proceed(self):

    #     title = "Fluids library reset"
    #     message = "Would you like to reset the fluid library to default?"

    #     buttons_config = {  "left_button_label" : "No",
    #                         "right_button_label" : "Yes",
    #                         "left_button_size" : 80,
    #                         "right_button_size" : 80}

    #     read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

    #     if read._cancel:
    #         return False

    #     if read._continue:
    #         return True

    # def reset_library_callback(self):
    #     if self.get_confirmation_to_proceed():
    #         self.reset_library_to_default()
    #         return True
    #     return False

    # def reset_library_to_default(self):

    #     # read fluid library data from file
    #     fluid_library_data = app().file.read_fluid_library_from_file()

    #     # get the fluid identifiers to be removed from properties
    #     fluid_identifiers = list()
    #     if isinstance(fluid_library_data, dict):
    #         fluid_identifiers = [int(fluid_id) for fluid_id in fluid_library_data.keys()]

    #     # reset the fluid library to default state
    #     default_fluid_library()

    #     if fluid_identifiers:
    #         self.reset_fluids_from_bodies_and_surfaces(fluid_identifiers)

    #     self.load_data_from_fluids_library()

    # def reset_fluids_from_bodies_and_surfaces(self, fluid_identifiers : list):

    #     surfaces_to_remove_fluid = list()
    #     volumes_to_remove_fluid = list()

    #     for key, data in self.properties.volume_properties.items():
    #         property, volume_id = key
    #         if property == "fluid":
    #             if isinstance(data, Fluid):
    #                 if data.identifier in fluid_identifiers:
    #                     volumes_to_remove_fluid.append(volume_id)
    #                     surface_ids = self.model.mesh.surfaces_from_volume[volume_id]
    #                     for surface_id in surface_ids:
    #                         surfaces_to_remove_fluid.append(surface_id)

    #     for vol_id in volumes_to_remove_fluid:
    #         self.model.properties._remove_volume_property("fluid", volume_id=vol_id)

    #     for surf_id in surfaces_to_remove_fluid:
    #         self.model.properties._remove_surface_property("fluid", surface_id=surf_id)

    #     app().file.write_model_properties_in_file()

    #     if isinstance(self.dialog, QDialog):
    #         self.dialog.load_model_info()

    # def call_refprop_interface(self, selected_fluid: Fluid | None = None):

    #     if isinstance(self.dialog, QDialog):
    #         self.dialog.hide()

    #     self.refprop = SetFluidCompositionInputs(
    #         fluid_to_edit=selected_fluid,
    #         state_properties=self.state_properties,
    #     )

    #     if not self.refprop.complete:
    #         self.refprop = None
    #         app().main_window.set_input_widget(self)
    #         return True

    #     self.after_getting_fluid_properties_from_refprop()
    #     self.refprop = None

    # def after_getting_fluid_properties_from_refprop(self):

    #     if not self.refprop.complete:
    #         return

    #     refprop_fluids_data = deepcopy(self.refprop.refprop_fluids_data)
    #     fluid_properties = refprop_fluids_data.get("properties")

    #     if refprop_fluids_data.get("thermodynamic_states") == "multiple_states":
    #         fluids_data = list(fluid_properties.values())
    #     else:
    #         fluids_data = [fluid_properties]

    #     if self.add_fluid_data_in_file(fluids_data, from_refprop=True):
    #         return

    #     self.load_data_from_fluids_library()

    #     app().processEvents()
    #     self.set_scroll_bar_to_maximum()

    #     self.tableWidget_fluid_data.blockSignals(False)

    # def load_compressor_info(self):

    #     if self.state_properties:

    #         if isinstance(self.dialog, QDialog):
    #             return

    #             volume_id = self.state_properties['volume_id']
    #             self.dialog.comboBox_attribution_type.setCurrentIndex(1)
    #             self.dialog.write_ids(volume_id)
    #             self.dialog.lineEdit_selection_id.setDisabled(True)
    #             if self.fluid_data_refprop:
    #                 fluid_name = self.fluid_data_refprop["name"]
    #                 self.dialog.lineEdit_fluid_name.setText(fluid_name)

    #             connection_type_comp = self.state_properties['connection type']
    #             connection_label = "discharge" if connection_type_comp else "suction"

    #             self.dialog.setWindowTitle(f"Set a fluid thermodynamic state at the compressor {connection_label}")

    # def update_compressor_fluid_temperature_and_pressure(self):
    #     return

    #     temperature_lineEdits = [self.lineEdit_temperature, self.lineEdit_temperature_rp]
    #     pressure_lineEdits = [self.lineEdit_pressure, self.lineEdit_pressure_rp]

    #     for temperature_lineEdit in temperature_lineEdits:
    #         temperature_lineEdit.setText(str(round(self.temperature_comp,4)))
    #         temperature_lineEdit.setDisabled(True)

    #     for pressure_lineEdit in pressure_lineEdits:
    #         pressure_lineEdit.setText(str(round(self.pressure_comp,4)))
    #         pressure_lineEdit.setDisabled(True)

    # def keyPressEvent(self, event):

    #     if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
    #         if isinstance(self.dialog, QDialog):
    #             self.dialog.attribute_callback()

    #     elif event.key() == Qt.Key_Delete:
    #         self.remove_selected_column()

    #     elif event.key() == Qt.Key_Escape:
    #         if isinstance(self.dialog, QDialog):
    #             self.dialog.close()
    #         else:
    #             self.close()
