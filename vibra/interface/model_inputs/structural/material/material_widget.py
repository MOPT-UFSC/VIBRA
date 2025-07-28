from PySide6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QSize

from vibra import app, TEMP_PROJECT_FILE
from vibra.interface.ui_generated.model.setup.material.material_widget_ui import MaterialWidget_UI
from vibra.interface.formatters.icons import *

from vibra.interface.general.pick_color_input import PickColorInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput

from vibra.libraries.default_libraries import default_material_library
from vibra.engine.properties.material import Material

from molde import Color
from copy import deepcopy
from itertools import count

window_title_1 = "Error"
window_title_2 = "Warning"

COLOR_ROW = 6

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))


class MaterialWidget(MaterialWidget_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        app().main_window.action_model_workspace_callback()

        self.project = app().project
        self.model = self.project.model
        self.properties = self.model.properties

        self.dialog = kwargs.get("dialog", None)

        self._initialize()
        self._create_connections()
        self._config_widgets()
        self._paint_icons()
        self.load_data_from_materials_library()

    # def _config_window(self):
    #     self.setWindowFlags(Qt.WindowStaysOnTopHint)
    #     self.setWindowModality(Qt.WindowModal)
    #     self.setWindowIcon(app().main_window.vibra_icon)
    #     self.setWindowTitle("Vibra")

    # def _add_icon_and_title(self):
    #     self._config_window()

    def _initialize(self):

        self.row = None
        self.col = None

        self.materials_from_library = dict()

        self.material_data_keys = [
                                    "name",
                                    "identifier",
                                    "material_density",
                                    "elasticity_modulus",
                                    "poisson_ratio",
                                    "thermal_expansion_coefficient",
                                    "color"
                                    ]

    def _create_connections(self):
        #
        self.pushButton_add_column.clicked.connect(self.add_column)
        self.pushButton_duplicate.clicked.connect(self.duplicate_selected_material)
        self.pushButton_remove_column.clicked.connect(self.remove_selected_column)
        # self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)
        #
        self.tableWidget_material_data.itemChanged.connect(self.item_changed_callback)
        self.tableWidget_material_data.cellClicked.connect(self.cell_clicked_callback)
    
    def _config_widgets(self):
        self.tableWidget_material_data.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))
    
    def _update_size_policy(self):
        if len(self.materials_from_library) > 6:
            self.tableWidget_material_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        else:
            self.tableWidget_material_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

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

    def load_data_from_materials_library(self):

        if not TEMP_PROJECT_FILE.exists():
            self.reset_library_to_default()
            return

        config = app().project.file.read_material_library_from_file()
        if config is None:
            self.reset_library_to_default()
            return

        self.materials_from_library.clear()

        if not list(config.sections()):
            self.update_table()
            return

        for tag in config.sections():

            section = config[tag]
            identifier =  int(section['identifier'])

            material = Material(
                                name = section['name'],
                                identifier = identifier, 
                                material_density = float(section['material_density']),
                                poisson_ratio = float(section['poisson_ratio']),
                                elasticity_modulus = float(section['elasticity_modulus']),
                                thermal_expansion_coefficient = float(section['thermal_expansion_coefficient']), 
                                color = getColorRGB(section['color'])
                                )

            self.materials_from_library[identifier] = material

        self.update_table()

    def update_table(self):

        self.tableWidget_material_data.clearContents()
        self.tableWidget_material_data.blockSignals(True)
        self.tableWidget_material_data.setRowCount(COLOR_ROW + 1)
        self.tableWidget_material_data.setColumnCount(len(self.materials_from_library))

        for j, material in enumerate(self.materials_from_library.values()):
            if isinstance(material, Material):

                self.tableWidget_material_data.setItem(0, j, QTableWidgetItem(str(material.name)))
                self.tableWidget_material_data.setItem(1, j, QTableWidgetItem(str(material.identifier)))
                self.tableWidget_material_data.setItem(2, j, QTableWidgetItem(str(material.material_density)))
                self.tableWidget_material_data.setItem(3, j, QTableWidgetItem(f"{material.elasticity_modulus :.4e}"))
                self.tableWidget_material_data.setItem(4, j, QTableWidgetItem(str(material.poisson_ratio)))
                self.tableWidget_material_data.setItem(5, j, QTableWidgetItem(str(material.thermal_expansion_coefficient)))

                item = QTableWidgetItem()
                item.setBackground(Color(*material.color).to_qt())
                item.setForeground(Color(*material.color).to_qt())
                item.setSizeHint(QSize(80, 30))
                self.tableWidget_material_data.setItem(6, j, item)

        for i in range(self.tableWidget_material_data.rowCount()):
            for j in range(self.tableWidget_material_data.columnCount()):
                self.tableWidget_material_data.item(i, j).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_material_data.blockSignals(False)
        self._update_size_policy()

    def get_selected_column(self) -> int:
        selected_items = self.tableWidget_material_data.selectedIndexes()
        if not selected_items:
            return -1
        return selected_items[-1].column()

    def get_selected_material(self) -> Material | None:
        selected_column = self.get_selected_column()
        if selected_column < 0:
            return

        if selected_column >= len(self.materials_from_library):
            return
        
        item = self.tableWidget_material_data.item(1, selected_column)
        identifier = int(item.text())

        return self.materials_from_library.get(identifier)

    def add_column(self):
    
        self.tableWidget_material_data.blockSignals(True)

        table_size = self.tableWidget_material_data.columnCount()
        if table_size > len(self.materials_from_library):
            # it means that if you already have a new row
            # to insert data you don't need another one
            self.tableWidget_material_data.blockSignals(False)
            return 

        last_col = self.tableWidget_material_data.columnCount()
        self.tableWidget_material_data.insertColumn(last_col)

        for i in range(self.tableWidget_material_data.rowCount()):
            item = QTableWidgetItem()
            item.setSizeHint(QSize(80, 30))
            self.tableWidget_material_data.setItem(i, last_col, item)
            self.tableWidget_material_data.item(i, last_col).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_material_data.selectColumn(last_col)
        self.tableWidget_material_data.blockSignals(False)

    def remove_selected_column(self):

        selected_column = self.get_selected_column()
        if selected_column < 0:
            return

        if selected_column >= len(self.materials_from_library):
            # if it is the last item and a not an already configured
            # material, just remove the last line
            current_size = self.tableWidget_material_data.columnCount()
            self.tableWidget_material_data.setColumnCount(current_size - 1)

            self._update_size_policy()
            self.tableWidget_material_data.horizontalScrollBar().setSliderPosition(0)
            return

        item = self.tableWidget_material_data.item(1, selected_column)
        identifier = int(item.text())
        material = self.materials_from_library.get(identifier)

        self.remove_material_from_file(material)
        self._update_size_policy()

        self.tableWidget_material_data.horizontalScrollBar().setSliderPosition(0)

    def duplicate_selected_material(self):

        selected_column = self.get_selected_column()
        if selected_column < 0:
            return
        
        self.refprop = None
        item = self.tableWidget_material_data.item(1, selected_column)
        if item.text() == "":
            return

        identifier = int(item.text())
        material = self.materials_from_library.get(identifier)
        if not isinstance(material, Material):
            return

        dmaterial = deepcopy(material)
        new_identifier = self.new_identifier()

        dmaterial.identifier = new_identifier
        dmaterial.name = self.get_suffix_for_duplicated_material(dmaterial.name)
        self.materials_from_library[new_identifier] = dmaterial

        self.update_table()
        last_col = self.tableWidget_material_data.columnCount()

        self.add_material_to_file(last_col-1, material=dmaterial.__dict__)
        app().processEvents()
        self.set_scroll_bar_to_maximum()

    def get_suffix_for_duplicated_material(self, material_name: str):

        already_used_names = set()
        for material in self.materials_from_library.values():
            material: Material
            if material_name in material.name:
                already_used_names.add(material.name)

        for i in count(1):
            new_name = f"{material_name} ({i})"
            if new_name not in already_used_names:
                return new_name

    def set_scroll_bar_to_maximum(self):
        scroll_bar = self.tableWidget_material_data.horizontalScrollBar()
        scroll_bar.setSliderPosition(scroll_bar.minimum())
        app().processEvents()
        scroll_bar.setSliderPosition(scroll_bar.maximum())

    def item_changed_callback(self, item : QTableWidgetItem):

        self.tableWidget_material_data.blockSignals(True)

        if item.row() == 0:
            if self.column_has_invalid_name(item.column()):
                self.tableWidget_material_data.blockSignals(False)
                return

        elif item.row() == 1:
            if self.column_has_invalid_identifier(item.column()):
                self.tableWidget_material_data.blockSignals(False)
                return

        else:
            if self.item_is_invalid_number(item):
                self.tableWidget_material_data.blockSignals(False)
                return

        self.go_to_next_cell(item)
        if self.column_has_empty_items(item.column()):
            self.tableWidget_material_data.blockSignals(False)
            return

        self.add_material_to_file(item.column())
        self.load_data_from_materials_library()

        self.tableWidget_material_data.blockSignals(False)
        self.tableWidget_material_data.horizontalScrollBar().setSliderPosition(0)

    def go_to_next_cell(self, item : QTableWidgetItem):

        row = item.row()
        column = item.column()

        if row < COLOR_ROW - 1:
            next_item = self.tableWidget_material_data.item(row + 1, column)
            if next_item.text() == "":
                self.tableWidget_material_data.setCurrentItem(next_item)
                self.tableWidget_material_data.editItem(next_item)

        elif row == COLOR_ROW - 1:
            self.pick_color(row + 1, column)

    def column_has_invalid_name(self, column):

        item = self.tableWidget_material_data.item(0, column)
        if item is None:
            return True

        column_name = item.text()

        if not column_name:
            return True

        for material in self.materials_from_library.values():
            if material.name == column_name:
                return True

        return False 

    def column_has_invalid_identifier(self, column):

        item = self.tableWidget_material_data.item(1, column)

        already_used_ids = set()
        for material in self.materials_from_library.values():
            already_used_ids.add(material.identifier)
        
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

            item = self.tableWidget_material_data.item(row, column)
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
                        2 : "material_density", 
                        3 : "elasticity_modulus",
                        4 : "poisson_ratio",
                        5 : "thermal_expansion_coefficient"
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

    def cell_clicked_callback(self, row, col):
        if row == COLOR_ROW:
            self.pick_color(row, col)

    def add_material_to_file(self, column: int, material: None | dict = None):
        try:

            material_data = dict()

            for i, key in enumerate(self.material_data_keys):
                item = self.tableWidget_material_data.item(i, column)
                if key == "color":
                    color = item.background().color().getRgb()
                    material_data[key] = list(color[:3])

                else:
                    if material is None:
                        material_data[key] = item.text()
                    else:
                        material_data[key] = str(material.get(key))

            material_identifier = material_data["identifier"]
            if not material_identifier:
                return

            config = app().project.file.read_material_library_from_file()
            config[material_identifier] = material_data

            app().project.file.write_material_library_in_file(config)
                    
        except Exception as error_log:
            title = "Error while writing material data in file"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return True

    def remove_material_from_file(self, material: Material):

        config = app().project.file.read_material_library_from_file()

        identifier = str(material.identifier)

        if not identifier in config.sections():
            return

        config.remove_section(identifier)
        app().project.file.write_material_library_in_file(config)

        self.reset_materials_from_bodies_and_surfaces([material.identifier])
        self.load_data_from_materials_library()

    def new_identifier(self):
        already_used_ids = set()
        for material in self.materials_from_library.values():
            material: Material
            already_used_ids.add(material.identifier)

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
        self.tableWidget_material_data.setItem(row, col, item)
        self.tableWidget_material_data.item(row, 0).setSelected(True)

    def get_selected_material_id(self):
        material = self.get_selected_material()
        if material is None:
            return None
        return material.identifier
            
    def get_confirmation_to_proceed(self):

        title = "Additional confirmation required to proceed"
        message = "Would you like to reset the material library to default values?"

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

        config_cache = app().project.file.read_material_library_from_file()

        sections_cache = list()
        if config_cache is not None:
            sections_cache = config_cache.sections()

        default_material_library()

        config = app().project.file.read_material_library_from_file()

        material_identifiers = list()
        for section_cache in sections_cache:
            if section_cache not in config.sections():
                identifier = config_cache[section_cache]["identifier"]
                material_identifiers.append(int(identifier))

        self.reset_materials_from_bodies_and_surfaces(material_identifiers)
        self.load_data_from_materials_library()

    def reset_materials_from_bodies_and_surfaces(self, material_identifiers: list):

        surfaces_to_remove_material = list()
        volumes_to_remove_material = list()

        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "material":
                if isinstance(data, Material):
                    if data.identifier in material_identifiers:
                        volumes_to_remove_material.append(volume_id)
                        surface_ids = self.model.mesh.surfaces_from_volume[volume_id]
                        for surface_id in surface_ids:
                            surfaces_to_remove_material.append(surface_id)

        for vol_id in volumes_to_remove_material:
            self.model.properties._remove_volume_property("material", volume_id=vol_id)

        for surf_id in surfaces_to_remove_material:
            self.model.properties._remove_surface_property("material", surface_id=surf_id)

        app().project.file.write_model_properties_in_file()

        if isinstance(self.dialog, QDialog):
            self.dialog.load_model_info()

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

    def closeEvent(self, event):
        super().closeEvent(event)
        self.keep_window_open = False