from enum import IntEnum
from random import randint
from typing import Optional

from molde import Color
from molde.colors import color_names
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem

from vibra import app
from vibra.engine.properties import MaterialLibrary
from vibra.engine.properties.material import Material
from vibra.errors import InvalidMaterialError
from vibra.interface.formatters.icons import change_icon_color_for_widgets
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.pick_color_input import PickColorInput
from vibra.interface.ui_generated.model.setup.material.material_widget_ui import MaterialWidget_UI
from vibra.utils.interface_utils import block_signals, qt_run_delayed


class RowsEnum(IntEnum):
    NAME = 0
    IDENTIFIER = 1
    MATERIAL_DENSITY = 2
    ELASTICITY_MODULUS = 3
    POISSON_RATIO = 4
    THERMAL_EXPANSION_COEFFICIENT = 5
    COLOR = 6


class MaterialWidget(MaterialWidget_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        app().main_window.action_model_workspace_callback()

        self._create_connections()
        self._config_widgets()
        self._paint_icons()
        self.reload_table_of_materials()

    def _create_connections(self):
        self.pushButton_add_column.clicked.connect(self.add_buffer_column)
        self.pushButton_duplicate.clicked.connect(self.duplicate_selected_material)
        self.pushButton_remove_column.clicked.connect(self.remove_selected_column)

        self.tableWidget_material_data.cellClicked.connect(self.cell_clicked_callback)
        self.tableWidget_material_data.itemChanged.connect(self.item_changed_callback)

    def _config_widgets(self):
        self.tableWidget_material_data.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))
        self.tableWidget_material_data.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectColumns)
        self.tableWidget_material_data.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def reload_table_of_materials(self):
        properties = app().new_project.model.properties
        number_of_rows = len(RowsEnum)
        number_of_cols = len(properties.material_library)

        with block_signals(self.tableWidget_material_data):
            self.tableWidget_material_data.clearContents()
            self.tableWidget_material_data.setRowCount(number_of_rows)
            self.tableWidget_material_data.setColumnCount(number_of_cols)

            for i, material in enumerate(properties.material_library.values()):
                self._set_column_values(i, material)

            self._update_size_policy()

    def add_buffer_column(self):
        if self._has_buffer_column():
            self.scroll_to_end()
            return

        with block_signals(self.tableWidget_material_data):
            column_index = self._add_empty_column()
            self.scroll_to_end()

            color = Color.from_hsv(randint(0, 360), 100, 70)
            color_item = self.tableWidget_material_data.item(RowsEnum.COLOR, column_index)
            name_item = self.tableWidget_material_data.item(RowsEnum.NAME, column_index)

            if color_item is not None:
                color_item.setBackground(color.to_qt())

            if name_item is not None:
                name_item.setText("New material")
                self.tableWidget_material_data.setCurrentItem(name_item)
                self.tableWidget_material_data.editItem(name_item)

    def duplicate_selected_material(self):
        material = self.get_selected_material()
        if material is None:
            return

        properties = app().new_project.model.properties
        new_material = material.copy()
        new_material.name = properties.fluid_library.get_dupplicated_name(material.name)
        properties.material_library.add(new_material)

        self.reload_table_of_materials()
        self.scroll_to_end()

    def remove_selected_column(self):
        selected_column = self._get_selected_column()
        if selected_column < 0:
            return

        properties = app().new_project.model.properties
        material = properties.material_library.get_from_ordered_index(selected_column)
        if material is not None:
            properties.remove_material(material)

        with block_signals(self.tableWidget_material_data):
            self.tableWidget_material_data.removeColumn(selected_column)

        app().main_window.selection.clear_selection()

    def reset_library_callback(self):
        """
        Resets the library to default and removes all material assignments.
        """
        if not self._get_reset_library_confirmation():
            return

        properties = app().new_project.model.properties
        materials_to_remove = list(properties.material_library.values())
        for material in materials_to_remove:
            properties.remove_material(material)
        properties.material_library = MaterialLibrary.default()
        self.reload_table_of_materials()
        app().main_window.selection.clear_selection()

    def cell_clicked_callback(self, row, col):
        if row == RowsEnum.COLOR:
            self._pick_color(row, col)

    def item_changed_callback(self, item: QTableWidgetItem):
        material_library = app().new_project.model.properties.material_library

        with block_signals(self.tableWidget_material_data):
            match item.row():
                case RowsEnum.NAME:
                    name = item.text()
                    if name.strip() == "":
                        raise InvalidMaterialError("Every material needs a name")

                    material = material_library.find_by_name(name)
                    name_already_exists = material is not None
                    if name_already_exists:
                        item.setText("New material")
                        raise InvalidMaterialError(f'A material named "{name}" alredy exists')

                case RowsEnum.COLOR | RowsEnum.IDENTIFIER:
                    pass  # ignore

                case _:
                    try:
                        str_value = item.text().replace(",", ".")
                        float(str_value)
                    except Exception as e:
                        property_name = self.tableWidget_material_data.verticalHeaderItem(item.row()).text()
                        msg = f'Invalid value for property "{property_name}". It must be a positive real number.'
                        item.setText("")
                        raise InvalidMaterialError(msg) from e

            if self._column_has_empty_items(item.column()):
                return

            try:
                self._update_library_with_column(item.column())
            except Exception as e:
                msg = f"Column {item.column()} contains unnexpected errors."
                item.setText("")
                raise InvalidMaterialError(msg) from e

            self.go_to_next_cell(item)

    def go_to_previous_cell(self, item: QTableWidgetItem):
        self.edit_cell(item.row() - 1, item.column())

    def go_to_next_cell(self, item: QTableWidgetItem):
        self.edit_cell(item.row() + 1, item.column())

    @qt_run_delayed
    def edit_cell(self, row: int, col: int):
        if not (0 <= row < len(RowsEnum)):
            return

        item = self.tableWidget_material_data.item(row, col)
        if item is None:
            return

        if row == RowsEnum.COLOR:
            self._pick_color(row, col)
        else:
            self.tableWidget_material_data.setCurrentItem(item)
            self.tableWidget_material_data.editItem(item)

    def scroll_to_start(self):
        scroll_bar = self.tableWidget_material_data.horizontalScrollBar()
        scroll_bar.setSliderPosition(scroll_bar.minimum())

    def scroll_to_end(self):
        scroll_bar = self.tableWidget_material_data.horizontalScrollBar()
        scroll_bar.setSliderPosition(scroll_bar.minimum())
        app().processEvents()
        scroll_bar.setSliderPosition(scroll_bar.maximum())

    def get_selected_material(self) -> Optional[Material]:
        selected_column = self._get_selected_column()
        if selected_column < 0:
            return

        properties = app().new_project.model.properties
        return properties.material_library.get_from_ordered_index(selected_column)

    def keyPressEvent(self, event: QKeyEvent):
        match event.key():
            case Qt.Key.Key_Delete:
                self.remove_selected_column()
            case _:
                event.ignore()  # propagates the event to the parent classes

    def _get_reset_library_confirmation(self):
        title = "Material library reset"
        message = "Would you like to reset the material library to default values?"
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
        material_library = app().new_project.model.properties.material_library
        material = material_library.get_from_ordered_index(col)
        if material is None:
            # Create a temporary material to be updated
            material = Material("", 0, 0, 0, 0, 0)
            material_library.add(material)

        def to_num(val: str) -> int | float:
            val = val.strip()
            return int(val) if val.isdigit() else float(val)

        for row in RowsEnum:
            item = self.tableWidget_material_data.item(row, col)
            if item is None:
                continue

            text = item.text()
            match row:
                case RowsEnum.NAME:
                    material.name = text
                case RowsEnum.IDENTIFIER:
                    item.setText(str(material.identifier))
                case RowsEnum.COLOR:
                    material.color = Color(item.background().color()).to_rgb()
                case RowsEnum.MATERIAL_DENSITY:
                    material.material_density = to_num(text)
                case RowsEnum.ELASTICITY_MODULUS:
                    material.elasticity_modulus = to_num(text)
                case RowsEnum.POISSON_RATIO:
                    material.poisson_ratio = to_num(text)
                case RowsEnum.THERMAL_EXPANSION_COEFFICIENT:
                    material.thermal_expansion_coefficient = to_num(text)

    def _column_has_empty_items(self, col: int):
        for row in RowsEnum:
            if row == RowsEnum.COLOR:
                continue

            item = self.tableWidget_material_data.item(row, col)
            if item is None:
                return True

            if item.text().strip() == "":
                return True

        return False

    def _pick_color(self, row: int, col: int):
        item = self.tableWidget_material_data.item(row, col)

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
        self.tableWidget_material_data.setItem(row, col, item)

    def _get_selected_column(self) -> int:
        selected_items = self.tableWidget_material_data.selectedIndexes()
        if not selected_items:
            return -1
        return selected_items[-1].column()

    def _has_buffer_column(self):
        properties = app().new_project.model.properties
        return self.tableWidget_material_data.columnCount() > len(properties.material_library)

    def _add_empty_column(self):
        properties = app().new_project.model.properties
        column_index = len(properties.material_library)
        self.tableWidget_material_data.setColumnCount(column_index + 1)

        for i in range(self.tableWidget_material_data.rowCount()):
            item = QTableWidgetItem()
            item.setBackground(color_names.GRAY_5.to_qt())
            self.tableWidget_material_data.setItem(i, column_index, item)

        return column_index

    def _set_column_values(
        self,
        column: int,
        material: Material,
    ):
        attributes = [
            material.name,
            material.identifier,
            material.material_density,
            f"{material.elasticity_modulus:.4e}",
            material.poisson_ratio,
            material.thermal_expansion_coefficient,
            Color(*material.color),
        ]

        for i, value in enumerate(attributes):
            item = QTableWidgetItem()
            self.tableWidget_material_data.setItem(i, column, item)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if isinstance(value, Color):
                item.setBackground(value.to_qt())
                item.setForeground(value.to_qt())
                item.setSizeHint(QSize(80, 30))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            else:
                item.setText(str(value))

    def _update_size_policy(self):
        properties = app().new_project.model.properties

        if len(properties.material_library) > 6:
            self.tableWidget_material_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        else:
            self.tableWidget_material_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _paint_icons(self):
        icon_color = None
        theme = app().config.user_preferences.interface_theme
        from vibra import DARK_ICON_COLOR, LIGHT_ICON_COLOR

        if theme == "dark":
            icon_color = DARK_ICON_COLOR.to_qt()
        else:
            icon_color = LIGHT_ICON_COLOR.to_qt()

        widgets = [self.pushButton_duplicate]
        change_icon_color_for_widgets(widgets, icon_color)
