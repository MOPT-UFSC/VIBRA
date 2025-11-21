from PySide6.QtWidgets import QAbstractItemView, QGridLayout, QHeaderView, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from vibra import app
from vibra.interface.ui_generated.model.setup.material.set_material_ui import SetMaterial_UI
from vibra.engine.properties.material import Material
from vibra.interface.model_inputs.general.material.material_widget import MaterialWidget
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

from collections import defaultdict
from enum import IntEnum

window_title_1 = "Error"
window_title_2 = "Warning"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class TabType(IntEnum):
    SETUP = 0
    LIST = 1


class MaterialInputs(SetMaterial_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.cache_selected_lines = kwargs.get("cache_selected_lines", list())

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._configure_qt_variables()
        self._create_connections()
        self._config_widgets()

        self.load_model_info()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Set material")

    def _initialize(self):
        self.keep_window_open = True
        self.material = None
        self.selected_column = None

    def _configure_qt_variables(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        self.scrollArea_table_of_materials.setLayout(self.grid_layout)
        self._add_material_widget()
        self.scrollArea_table_of_materials.adjustSize()

        self.pushButton_attribute = self.material_widget.pushButton_attribute
        self.pushButton_exit = self.material_widget.pushButton_exit

        self.tableWidget_material_data = self.material_widget.tableWidget_material_data
        self.tableWidget_model_materials : QTableWidget

    def _add_material_widget(self):
        self.material_widget = MaterialWidget(dialog=self)
        self.grid_layout.addWidget(self.material_widget)
        self.material_widget.pushButton_remove_column.clicked.connect(self.reset_selected_material_lineEdit)

    def reset_selected_material_lineEdit(self):
        self.lineEdit_selected_material_name.clear()

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.material_widget.pushButton_reset_library.clicked.connect(self.reset_material_library_callback)
        #
        self.tableWidget_material_data.currentCellChanged.connect(self.current_cell_changed)
        self.tableWidget_model_materials.cellClicked.connect(self.cell_clicked_callback)       
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.attribution_type_callback()
        self.update_selection_combo_box_texts()

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.selected_column = current_col
        self.update_material_selection()

    def cell_clicked_callback(self, row, col):  
        selected_items, selection_text, material_text = self.get_selected_items_and_texts()

        if not selected_items:
            return
    
        app().main_window.set_geometry_selection(**selected_items)

        self.pushButton_remove.setEnabled(True)
        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)
        self.lineEdit_selected_material_name.setText(material_text)

        app().main_window.action_model_workspace_callback()
        
    def get_selected_items_and_texts(self) -> tuple[dict, str, str]:
        selected_cells = self.tableWidget_model_materials.selectedItems()

        if not selected_cells:
            return dict(), str(), str()

        selected_items = defaultdict(list)
        selection_text = str()
        material_types = set()

        for i in range(len(selected_cells) // 6):
            index = i * 6

            selected_item = selected_cells[index].text()
            material_type = selected_cells[index + 1].text()

            selected_type, selected_id = selected_item.split("-")
            selected_type = selected_type.lower() + "s"

            selected_items[selected_type].append(int(selected_id))
            material_types.add(material_type)
        
        material_text = material_types.pop() if len(material_types) == 1 else "--"

        for selected_type, ids in selected_items.items():
            ids.sort()

            ids = map(str, ids)
            selection_text += selected_type.capitalize() + ": " + ", ".join(ids) + " "

        self.selected_items = selected_items

        return selected_items, selection_text, material_text

    def reset_material_library_callback(self):
        self.hide()
        if self.material_widget.reset_library_callback():
            self.actions_to_finalize()

    def geometry_selection_callback(self):

        if self.tabWidget_main.currentIndex() == TabType.LIST:
            return

        volumes = app().main_window.selected_geometry_volumes
        surfaces = app().main_window.selected_geometry_surfaces

        volume_exists = self.mesh.are_there_volumes_in_geometry()
        index = self.comboBox_attribution_type.currentIndex()

        selected_ids = set()
        if volume_exists:
            if volumes:
                selected_ids = volumes
                self.comboBox_attribution_type.setCurrentIndex(1)
            elif surfaces and index == 1:
                self.lineEdit_selection_id.clear()
        else:
            if surfaces:
                selected_ids = surfaces
                self.comboBox_attribution_type.setCurrentIndex(1)
            elif volumes and index == 1:
                self.lineEdit_selection_id.clear()
        if len(selected_ids):
            text = ", ".join([str(i) for i in selected_ids])
            self.lineEdit_selection_id.setText(text)

    def _config_widgets(self):
        self.tableWidget_model_materials.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_model_materials.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget_model_materials.setEditTriggers(QAbstractItemView.EditTrigger(0))
        self.tableWidget_model_materials.setSelectionBehavior(QAbstractItemView.SelectRows)

    def update_material_selection(self):

        if self.selected_column is None:
            return

        item = self.tableWidget_material_data.item(0, self.selected_column)
        if item is None:
            return

        material_name = item.text()
        self.lineEdit_selected_material_name.clear()
        if material_name != "":
            self.lineEdit_selected_material_name.setText(material_name)

    def attribution_type_callback(self):

        if self.comboBox_attribution_type.currentIndex():
            self.lineEdit_selection_id.clear()
            self.lineEdit_selection_id.setEnabled(True)

        else:
            current_text = self.comboBox_attribution_type.currentText()
            self.lineEdit_selection_id.setText(current_text)
            self.lineEdit_selection_id.setEnabled(False)

    def update_selection_combo_box_texts(self):

        volumes_exists = self.mesh.are_there_volumes_in_geometry()
        if volumes_exists:
            labels = ["All volumes", "Selected volumes"]
        else:
            labels = ["All surfaces", "Selected surfaces"]

        self.comboBox_attribution_type.clear()
        self.comboBox_attribution_type.addItems(labels)

    def attribute_callback(self):

        selected_material = self.material_widget.get_selected_material()

        if selected_material is None:
            self.hide()
            self.title = "No materials selected"
            self.message = "Select a material in the list before confirming the material attribution."
            PrintMessageInput([window_title_1, self.title, self.message])
            return

        current_text = self.comboBox_attribution_type.currentText()

        if "surfaces" in current_text:

            if "All" in current_text:
                surface_ids = list()
                if "surfaces" in self.mesh.geometry_information.keys():
                    surface_ids = self.mesh.geometry_information["surfaces"]

            else:
                input_ids = self.lineEdit_selection_id.text()
                surface_ids, error_data = self.mesh.check_selected_ids(
                                                                    input_ids, 
                                                                    selection = "surfaces", 
                                                                    single_id = False
                                                                    )

                if error_data is not None:
                    self.hide()
                    self.lineEdit_selection_id.setFocus()
                    PrintMessageInput(error_data)
                    return True

            for surface_id in surface_ids:
                self.properties._set_property("material", selected_material, surface=surface_id)

        if "volumes" in current_text:

            if "All" in current_text:
                volume_ids = list()
                if "volumes" in self.mesh.geometry_information.keys():
                    volume_ids = self.mesh.geometry_information["volumes"]

            else:
                input_ids = self.lineEdit_selection_id.text()
                volume_ids, error_data = self.mesh.check_selected_ids(
                                                                    input_ids, 
                                                                    selection = "volumes", 
                                                                    single_id = False
                                                                    )

                if error_data is not None:
                    self.hide()
                    self.lineEdit_selection_id.setFocus()
                    PrintMessageInput(error_data)
                    return True

            for volume_id in volume_ids:
                self.properties._set_property("material", selected_material, volume=volume_id)

        self.actions_to_finalize()
        self.close()

    def remove_callback(self):
        if not self.selected_items:
            return

        for selection_type, ids in self.selected_items.items():
            for id in ids:
                if selection_type == "surfaces":
                    self.properties._remove_surface_property("material", id)
                    self.properties._remove_surface_property("material_id", id)

                elif selection_type == "volumes":
                    self.properties._remove_volume_property("material", id)
                    self.properties._remove_volume_property("material_id", id)
        
        self.lineEdit_selection_id.clear()
        self.pushButton_remove.setDisabled(True)

        self.actions_to_finalize()
        app().main_window.set_geometry_selection()

    def reset_callback(self):

        self.hide()

        title = "Materials resetting"
        message = "Would you like to remove the all assigned materials from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if obj._cancel:
            return

        if obj._continue:

            self.properties._reset_property("material")
            self.properties._reset_property("material_id")
            self.actions_to_finalize()

            app().main_window.set_geometry_selection()

    def actions_to_finalize(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selected_material_name.clear()
        self.pushButton_remove.setDisabled(True)

        self.load_model_info()
        app().main_window.update_info_text()
        app().main_window.clear_selection()  # this also updates
        app().main_window.update_symbols()
        app().file.write_model_properties_in_file()

    def load_model_info(self):

        properties = {
                      "Surface" : self.properties.surface_properties,
                      "Volume" : self.properties.volume_properties
                      }

        self.materials_from_model = dict()

        for selection, _property in properties.items():
            for key, data in _property.items():
                property, surface_id = key
                if property == "material":

                    data : Material
                    selection_id = f"{selection}-{surface_id}"
                    self.materials_from_model[(data.identifier, selection_id)] = data

        self.load_table_info()
        self.update_tabs_visibility()

    def load_table_info(self):

        self.tableWidget_model_materials.clearContents()
        self.tableWidget_model_materials.blockSignals(True)
        self.tableWidget_model_materials.setRowCount(len(self.materials_from_model))
        self.tableWidget_model_materials.setColumnCount(6)

        for i, (key, material) in enumerate(self.materials_from_model.items()):
            material: Material
            _, selection_id = key
            if isinstance(material, Material):
                
                self.tableWidget_model_materials.setItem(i, 0, QTableWidgetItem(selection_id))
                self.tableWidget_model_materials.setItem(i, 1, QTableWidgetItem(str(material.name)))
                self.tableWidget_model_materials.setItem(i, 2, QTableWidgetItem(str(material.identifier)))
                self.tableWidget_model_materials.setItem(i, 3, QTableWidgetItem(str(material.material_density)))
                self.tableWidget_model_materials.setItem(i, 4, QTableWidgetItem(str(material.elasticity_modulus)))
                self.tableWidget_model_materials.setItem(i, 5, QTableWidgetItem(str(material.poisson_ratio)))

        for i in range(self.tableWidget_model_materials.rowCount()):
            for j in range(self.tableWidget_model_materials.columnCount()):
                self.tableWidget_model_materials.item(i, j).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_model_materials.blockSignals(False)

    def update_tabs_visibility(self):

        for key in self.properties.volume_properties.keys():
            property, _ = key
            if property == "material":
                self.tabWidget_main.setTabVisible(TabType.LIST, True)
                return

        for key in self.properties.surface_properties.keys():
            property, _ = key
            if property == "material":
                self.tabWidget_main.setTabVisible(TabType.LIST, True)
                return

        self.tabWidget_main.setTabVisible(TabType.LIST, False)

    def tab_event_callback(self):
        app().main_window.clear_selection()
        
        self.lineEdit_selection_id.clear()
        self.lineEdit_selected_material_name.clear()

        if self.tabWidget_main.currentIndex() == TabType.LIST:
            self.pushButton_remove.setDisabled(True)
            self.lineEdit_selection_id.setDisabled(True)
            self.comboBox_attribution_type.setDisabled(True)

            self.tableWidget_model_materials.clearSelection()

        else:
            self.comboBox_attribution_type.setDisabled(False)
            self.attribution_type_callback()
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()

        elif event.key() == Qt.Key_Delete:
            self.remove_callback()

        elif event.key() == Qt.Key_Escape:
            self.close()
        
        elif event.key() == Qt.Key_Control:
            self.tableWidget_model_materials.setSelectionMode(QAbstractItemView.MultiSelection)
        
        elif event.key() == Qt.Key_Shift:
            self.tableWidget_model_materials.setSelectionMode(QAbstractItemView.ContiguousSelection)
        
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.tableWidget_model_materials.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)