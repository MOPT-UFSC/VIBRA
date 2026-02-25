from enum import IntEnum
from typing import Optional

from molde import Color
from molde.colors import color_names
from numpy.random import randint
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QAbstractItemDelegate, QAbstractItemView, QDialog, QHeaderView, QTableWidgetItem

from vibra import app
from vibra.engine.properties import FluidLibrary
from vibra.engine.properties.fluid import Fluid
from vibra.errors import InvalidFluidError
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.pick_color_input import PickColorInput
from vibra.interface.ui_generated.model.setup.fluid.fluid_widget_ui import FluidWidget_UI
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
    modified = Signal()

    def __init__(self, *argas, **kwargs):
        super().__init__()

        app().main_window.action_model_workspace_callback()

        self.dialog = kwargs.get("dialog", None)
        self.state_properties = kwargs.get("state_properties", dict())

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

            self._update_size_policy()
        self.modified.emit()

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
        self.modified.emit()

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

        self._update_size_policy()
        app().main_window.selection.clear_selection()
        self.modified.emit()

    def reset_library_callback(self):
        """
        Resets the library to default and removes all fluid assignments.
        """
        if not self._get_reset_library_confirmation():
            return

        properties = app().new_project.model.properties
        fluids_to_remove = list(properties.fluid_library.values())
        for fluid in fluids_to_remove:
            properties.remove_fluid(fluid)
        properties.fluid_library = FluidLibrary.default()
        self.reload_table_of_fluids()
        app().main_window.selection.clear_selection()
        self.modified.emit()

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

        self.modified.emit()

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
