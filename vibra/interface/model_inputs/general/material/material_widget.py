from copy import deepcopy
from enum import IntEnum
from itertools import count
from random import randint
from typing import Optional

from molde import Color
from molde.colors import color_names
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QDialog, QHeaderView, QTableWidgetItem

from vibra import app
from vibra.engine.properties import MaterialLibrary
from vibra.engine.properties.material import Material
from vibra.errors import InvalidMaterialError
from vibra.interface.formatters.icons import change_icon_color_for_widgets
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.pick_color_input import PickColorInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.ui_generated.model.setup.material.material_widget_ui import MaterialWidget_UI
from vibra.utils.interface_utils import block_signals


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

        # app().main_window.action_model_workspace_callback()

        # self.mesh = app().new_project.model.mesh
        # self.properties = app().new_project.model.properties

        # self.dialog = kwargs.get("dialog", None)

        # self._initialize()
        self._create_connections()
        # self._config_widgets()
        # self._paint_icons()
        # self.load_data_from_materials_library()

        self.reload_table_of_materials()

    def _create_connections(self):
        self.pushButton_add_column.clicked.connect(self.add_buffer_column)
        self.pushButton_duplicate.clicked.connect(self.duplicate_selected_material)
        self.pushButton_remove_column.clicked.connect(self.remove_selected_column)

        self.tableWidget_material_data.cellClicked.connect(self.cell_clicked_callback)
        self.tableWidget_material_data.itemChanged.connect(self.item_changed_callback)

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
                        item.setText("")
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
        read = PickColorInput()
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
        material: Material | list,
        buffered: bool = False,
    ):
        if isinstance(material, Material):
            attributes = [
                material.name,
                material.identifier,
                material.material_density,
                f"{material.elasticity_modulus:.4e}",
                material.poisson_ratio,
                material.thermal_expansion_coefficient,
                Color(*material.color),
            ]
        else:
            attributes = material

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
                if buffered:
                    item.setBackground(color_names.GRAY_5.to_qt())

    def _update_size_policy(self):
        properties = app().new_project.model.properties

        if len(properties.material_library) > 6:
            self.tableWidget_material_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        else:
            self.tableWidget_material_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # def _initialize(self):

    #     self.row = None
    #     self.col = None

    #     self.materials_from_library = dict()

    #     self.material_data_keys = [
    #                                 "name",
    #                                 "identifier",
    #                                 "material_density",
    #                                 "elasticity_modulus",
    #                                 "poisson_ratio",
    #                                 "thermal_expansion_coefficient",
    #                                 "color"
    #                                 ]

    # def _create_connections(self):
    #     #
    #     self.pushButton_add_column.clicked.connect(self.add_column)
    #     self.pushButton_duplicate.clicked.connect(self.duplicate_selected_material)
    #     self.pushButton_remove_column.clicked.connect(self.remove_selected_column)
    #     # self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)
    #     #
    #     self.tableWidget_material_data.itemChanged.connect(self.item_changed_callback)
    #     self.tableWidget_material_data.cellClicked.connect(self.cell_clicked_callback)

    # def _update_size_policy(self):
    #     if len(self.materials_from_library) > 6:
    #         self.tableWidget_material_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    #     else:
    #         self.tableWidget_material_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

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

    # def get_selected_column(self) -> int:
    #     selected_items = self.tableWidget_material_data.selectedIndexes()
    #     if not selected_items:
    #         return -1
    #     return selected_items[-1].column()

    # def get_selected_material(self) -> Material | None:
    #     selected_column = self.get_selected_column()
    #     if selected_column < 0:
    #         return

    #     if selected_column >= len(self.materials_from_library):
    #         return

    #     item = self.tableWidget_material_data.item(1, selected_column)
    #     identifier = int(item.text())

    #     return self.materials_from_library.get(identifier)

    # def get_selected_material_id(self) -> int | None:
    #     material = self.get_selected_material()
    #     if material is None:
    #         return None

    #     return material.identifier

    # def add_column(self):

    #     self.tableWidget_material_data.blockSignals(True)

    #     table_size = self.tableWidget_material_data.columnCount()
    #     if table_size > len(self.materials_from_library):
    #         # it means that if you already have a new row
    #         # to insert data you don't need another one
    #         self.tableWidget_material_data.blockSignals(False)
    #         return

    #     last_col = self.tableWidget_material_data.columnCount()
    #     self.tableWidget_material_data.insertColumn(last_col)

    #     for i in range(self.tableWidget_material_data.rowCount()):
    #         item = QTableWidgetItem()
    #         item.setSizeHint(QSize(80, 30))
    #         self.tableWidget_material_data.setItem(i, last_col, item)
    #         self.tableWidget_material_data.item(i, last_col).setTextAlignment(Qt.AlignCenter)

    #     self.tableWidget_material_data.selectColumn(last_col)
    #     self.tableWidget_material_data.blockSignals(False)

    #     app().processEvents()
    #     self.set_scroll_bar_to_maximum()

    # def remove_selected_column(self):

    #     selected_column = self.get_selected_column()
    #     if selected_column < 0:
    #         return

    #     if selected_column >= len(self.materials_from_library):
    #         # if it is the last item and a not an already configured
    #         # material, just remove the last line
    #         current_size = self.tableWidget_material_data.columnCount()
    #         self.tableWidget_material_data.setColumnCount(current_size - 1)

    #         self._update_size_policy()
    #         self.tableWidget_material_data.horizontalScrollBar().setSliderPosition(0)
    #         return

    #     item = self.tableWidget_material_data.item(1, selected_column)
    #     identifier = int(item.text())
    #     material = self.materials_from_library.get(identifier)

    #     self.remove_material_from_file(material)
    #     self._update_size_policy()

    #     self.tableWidget_material_data.horizontalScrollBar().setSliderPosition(0)

    # def duplicate_selected_material(self):

    #     selected_column = self.get_selected_column()
    #     if selected_column < 0:
    #         return

    #     self.refprop = None
    #     item_identifier = self.tableWidget_material_data.item(1, selected_column)
    #     if item_identifier.text() == "":
    #         return

    #     identifier = int(item_identifier.text())
    #     material = self.materials_from_library.get(identifier)
    #     if not isinstance(material, Material):
    #         return

    #     dmaterial = deepcopy(material)
    #     dmaterial.identifier = self.new_identifier()
    #     dmaterial.name = self.get_suffix_for_duplicated_material(dmaterial.name)

    #     # material_data = {
    #     #                 "name" : new_name,
    #     #                 "identifier" : new_identifier,
    #     #                 "material_density" : dmaterial.material_density,
    #     #                 "poisson_ratio" : dmaterial.poisson_ratio,
    #     #                 "elasticity_modulus" : dmaterial.elasticity_modulus,
    #     #                 "thermal_expansion_coefficient" : dmaterial.thermal_expansion_coefficient,
    #     #                 "color" : dmaterial.color,
    #     #                 }

    #     if self.add_material_data_in_file(dmaterial.__dict__):
    #         return

    #     self.load_data_from_materials_library()

    #     app().processEvents()
    #     self.set_scroll_bar_to_maximum()

    # def get_suffix_for_duplicated_material(self, material_name: str):

    #     already_used_names = set()
    #     for material in self.materials_from_library.values():
    #         material: Material
    #         if material_name in material.name:
    #             already_used_names.add(material.name)

    #     for i in count(1):
    #         new_name = f"{material_name} ({i})"
    #         if new_name not in already_used_names:
    #             return new_name

    # def set_scroll_bar_to_maximum(self):
    #     scroll_bar = self.tableWidget_material_data.horizontalScrollBar()
    #     scroll_bar.setSliderPosition(scroll_bar.minimum())
    #     app().processEvents()
    #     scroll_bar.setSliderPosition(scroll_bar.maximum())

    # def cell_clicked_callback(self, row, col):
    #     if row == COLOR_ROW:
    #         self.pick_color(row, col)

    # def item_changed_callback(self, item : QTableWidgetItem):

    #     self.tableWidget_material_data.blockSignals(True)

    #     if item.row() == 0:
    #         if self.column_has_invalid_name(item.column()):
    #             self.tableWidget_material_data.blockSignals(False)
    #             return

    #     elif item.row() == 1:
    #         if self.column_has_invalid_identifier(item.column()):
    #             self.tableWidget_material_data.blockSignals(False)
    #             return

    #     else:
    #         if self.item_is_invalid_number(item):
    #             self.tableWidget_material_data.blockSignals(False)
    #             return

    #     self.go_to_next_cell(item)
    #     if self.column_has_empty_items(item.column()):
    #         self.tableWidget_material_data.blockSignals(False)
    #         return

    #     material_data = self.get_material_data_for_selected_column(item.column())
    #     if self.add_material_data_in_file(material_data):
    #         return

    #     self.load_data_from_materials_library()

    #     self.tableWidget_material_data.blockSignals(False)

    # def go_to_next_cell(self, item : QTableWidgetItem):

    #     row = item.row()
    #     column = item.column()

    #     if row < COLOR_ROW - 1:
    #         next_item = self.tableWidget_material_data.item(row + 1, column)
    #         if next_item.text() == "":
    #             self.tableWidget_material_data.setCurrentItem(next_item)
    #             self.tableWidget_material_data.editItem(next_item)

    #     elif row == COLOR_ROW - 1:
    #         self.pick_color(row + 1, column)

    # def column_has_invalid_name(self, column):

    #     item = self.tableWidget_material_data.item(0, column)
    #     if item is None:
    #         return True

    #     column_name = item.text()

    #     if not column_name:
    #         return True

    #     for material in self.materials_from_library.values():
    #         if material.name == column_name:
    #             return True

    #     return False

    # def column_has_invalid_identifier(self, column):

    #     item = self.tableWidget_material_data.item(1, column)

    #     already_used_ids = set()
    #     for material in self.materials_from_library.values():
    #         already_used_ids.add(material.identifier)

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

    #         item = self.tableWidget_material_data.item(row, column)
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
    #                     2 : "material_density",
    #                     3 : "elasticity_modulus",
    #                     4 : "poisson_ratio",
    #                     5 : "thermal_expansion_coefficient"
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

    # def add_material_data_in_file(self, material_data: dict):

    #     # check all inputs before proceeding
    #     for key in self.material_data_keys:
    #         value = material_data.get(key)
    #         if value is None:
    #             return True

    #     # material identifier
    #     identifier = material_data.get("identifier")

    #     # read material library data from file
    #     material_library_data = app().file.read_material_library_from_file()

    #     # add the new material data
    #     material_library_data[identifier] = material_data

    #     # save the modified material data in file
    #     app().file.write_material_library_in_file(material_library_data)

    # def get_material_data_for_selected_column(self, column: int):
    #     try:

    #         material_data = dict()
    #         for i, key in enumerate(self.material_data_keys):
    #             item = self.tableWidget_material_data.item(i, column)
    #             if key == "name":
    #                 material_data[key] = item.text()

    #             elif key == "color":
    #                 color = item.background().color().getRgb()
    #                 material_data[key] = list(color[:3])

    #             elif key == "identifier":
    #                 identifier = int(item.text())
    #                 material_data[key] = identifier

    #             else:
    #                 material_data[key] = float(item.text())

    #         return material_data

    #     except Exception as error_log:
    #         title = "Error while writing material data in file"
    #         message = str(error_log)
    #         PrintMessageInput([error_title, title, message])
    #         return None

    # def remove_material_from_file(self, material: Material):

    #     # read material library data from file
    #     material_library_data = app().file.read_material_library_from_file()

    #     str_material_id = str(material.identifier)
    #     if not str_material_id in material_library_data.keys():
    #         return

    #     # remove the selected material
    #     material_library_data.pop(str_material_id)

    #     # save the modified material data in file
    #     app().file.write_material_library_in_file(material_library_data)

    #     self.reset_materials_from_bodies_and_surfaces([material.identifier])
    #     self.load_data_from_materials_library()

    # def reset_library_callback(self):
    #     if self.get_confirmation_to_proceed():
    #         self.reset_library_to_default()
    #         return True
    #     return False

    # def reset_library_to_default(self):

    #     # read material library data from file
    #     material_library_data = app().file.read_material_library_from_file()

    #     # get the material identifiers to be removed from properties
    #     material_identifiers = list()
    #     if isinstance(material_library_data, dict):
    #         material_identifiers = [int(material_id) for material_id in material_library_data.keys()]

    #     # reset the material library to default state
    #     default_material_library()

    #     if material_identifiers:
    #         self.reset_materials_from_bodies_and_surfaces(material_identifiers)

    #     self.load_data_from_materials_library()

    # def load_data_from_materials_library(self):

    #     self.materials_from_library.clear()
    #     materials_from_library = app().load_project.load_material_library()

    #     if materials_from_library is None:
    #         self.reset_library_to_default()
    #         return

    #     elif isinstance(materials_from_library, dict):
    #         if not materials_from_library:
    #             self.reset_library_to_default()
    #             return

    #     self.materials_from_library = materials_from_library

    #     self.update_table_of_materials()

    # def update_table_of_materials(self):

    #     self.tableWidget_material_data.clearContents()
    #     self.tableWidget_material_data.blockSignals(True)
    #     self.tableWidget_material_data.setRowCount(COLOR_ROW + 1)
    #     self.tableWidget_material_data.setColumnCount(len(self.materials_from_library))

    #     for j, material in enumerate(self.materials_from_library.values()):
    #         if isinstance(material, Material):

    #             self.tableWidget_material_data.setItem(0, j, QTableWidgetItem(str(material.name)))
    #             self.tableWidget_material_data.setItem(1, j, QTableWidgetItem(str(material.identifier)))
    #             self.tableWidget_material_data.setItem(2, j, QTableWidgetItem(str(material.material_density)))
    #             self.tableWidget_material_data.setItem(3, j, QTableWidgetItem(f"{material.elasticity_modulus :.4e}"))
    #             self.tableWidget_material_data.setItem(4, j, QTableWidgetItem(str(material.poisson_ratio)))
    #             self.tableWidget_material_data.setItem(5, j, QTableWidgetItem(str(material.thermal_expansion_coefficient)))

    #             item = QTableWidgetItem()
    #             item.setBackground(Color(*material.color).to_qt())
    #             item.setForeground(Color(*material.color).to_qt())
    #             item.setSizeHint(QSize(80, 30))
    #             self.tableWidget_material_data.setItem(6, j, item)

    #     for i in range(self.tableWidget_material_data.rowCount()):
    #         for j in range(self.tableWidget_material_data.columnCount()):
    #             self.tableWidget_material_data.item(i, j).setTextAlignment(Qt.AlignCenter)

    #     self.tableWidget_material_data.blockSignals(False)
    #     self._update_size_policy()

    # def reset_materials_from_bodies_and_surfaces(self, material_identifiers: list):

    #     surfaces_to_remove_material = list()
    #     volumes_to_remove_material = list()

    #     for key, data in self.properties.volume_properties.items():
    #         property, volume_id = key
    #         if property == "material":
    #             if isinstance(data, Material):
    #                 if data.identifier in material_identifiers:
    #                     volumes_to_remove_material.append(volume_id)
    #                     surface_ids = self.mesh.surfaces_from_volume[volume_id]
    #                     for surface_id in surface_ids:
    #                         surfaces_to_remove_material.append(surface_id)

    #     for vol_id in volumes_to_remove_material:
    #         self.properties._remove_volume_property("material", volume_id=vol_id)

    #     for surf_id in surfaces_to_remove_material:
    #         self.properties._remove_surface_property("material", surface_id=surf_id)

    #     app().file.write_model_properties_in_file()

    #     if isinstance(self.dialog, QDialog):
    #         self.dialog.load_model_info()

    # def new_identifier(self):
    #     already_used_ids = set()
    #     for material in self.materials_from_library.values():
    #         material: Material
    #         already_used_ids.add(material.identifier)

    #     for i in count(1):
    #         if i not in already_used_ids:
    #             return i

    # def pick_color(self, row, col):

    #     read = PickColorInput()
    #     if not read.complete:
    #         return True

    #     picked_color = read.color
    #     item = QTableWidgetItem()
    #     item.setBackground(Color(*picked_color).to_qt())
    #     item.setForeground(Color(*picked_color).to_qt())
    #     self.tableWidget_material_data.setItem(row, col, item)
    #     self.tableWidget_material_data.item(row, 0).setSelected(True)

    # def keyPressEvent(self, event: QKeyEvent):
    #     if event.key() == Qt.Key_Delete:
    #         self.remove_selected_column()
    #     else:
    #         event.ignore()  # propagates the event to the parent classes

    # def closeEvent(self, event):
    #     super().closeEvent(event)
    #     self.keep_window_open = False
