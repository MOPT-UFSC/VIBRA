from collections import defaultdict
from enum import IntEnum

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QGridLayout,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from vibra import app
from vibra.engine.properties.material import Material
from vibra.interface import error_title
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.material.material_widget import MaterialWidget
from vibra.interface.ui_generated.model.material.set_material_ui import SetMaterial_UI


class TabType(IntEnum):
    SETUP = 0
    LIST = 1


class MaterialInputs(SetMaterial_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self._initialize()
        self._config_window()
        self._configure_qt_variables()
        self._create_connections()
        self._config_widgets()

        self.load_model_info()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    @property
    def properties(self):
        return app().project.model.properties

    @property
    def mesh(self):
        return app().project.model.mesh

    def _initialize(self):
        self.keep_window_open = True
        self.material = None
        self.selected_items = defaultdict(list)
        self.table_model_materials_cell_clicked = False

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Set material")

    def _configure_qt_variables(self):

        self._add_material_widget()
        self.scrollArea_table_of_materials.adjustSize()

        self.tableWidget_material_data = self.material_widget.tableWidget_material_data
        self.tableWidget_model_materials: QTableWidget

    def _add_material_widget(self):

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_table_of_materials.setLayout(self.grid_layout)

        self.material_widget = MaterialWidget(dialog=self)
        self.grid_layout.addWidget(self.material_widget)
        self.scrollArea_table_of_materials.adjustSize()

    def reset_selected_material_lineEdit(self):
        self.lineEdit_selected_material_name.clear()

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.material_widget.modified.connect(self.load_model_info)
        self.material_widget.pushButton_apply.clicked.connect(self.apply_callback)
        self.material_widget.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.material_widget.pushButton_cancel.clicked.connect(self.close)
        self.material_widget.pushButton_remove_column.clicked.connect(self.reset_selected_material_lineEdit)
        self.material_widget.pushButton_reset_library.clicked.connect(self.reset_material_library_callback)
        self.material_widget.pushButton_export_library.clicked.connect(self.export_material_library_callback)
        self.material_widget.pushButton_import_library.clicked.connect(self.import_material_library_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tableWidget_material_data.currentCellChanged.connect(self.current_cell_changed)
        self.tableWidget_model_materials.cellClicked.connect(self.cell_clicked_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.attribution_type_callback()
        self.update_selection_combo_box_texts()

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.update_material_selection(current_col)

    def cell_clicked_callback(self, row, col):
        selection_text = self.set_selected_items_and_get_selection_text()

        if not self.selected_items:
            return

        self.table_model_materials_cell_clicked = True

        app().main_window.selection.set_geometry_selection(**self.selected_items)

        self.pushButton_remove.setEnabled(True)
        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)

        app().main_window.action_model_workspace_callback()

        self.table_model_materials_cell_clicked = False

    def set_selected_items_and_get_selection_text(self) -> str:
        selected_cells = self.tableWidget_model_materials.selectedItems()

        if not selected_cells:
            return str()

        selected_items = defaultdict(list)
        selection_text = str()

        num_of_columns = self.tableWidget_model_materials.columnCount()

        for row in range(len(selected_cells) // num_of_columns):
            index = row * num_of_columns

            selected_item = selected_cells[index].text()

            selected_type, selected_id = selected_item.split("-")
            selected_type = selected_type.lower() + "s"

            selected_items[selected_type].append(int(selected_id))

        for selected_type, ids in selected_items.items():
            ids.sort()

            ids = map(str, ids)
            selection_text += selected_type.capitalize() + ": " + ", ".join(ids) + " "

        self.selected_items = selected_items

        return selection_text

    def reset_material_library_callback(self):
        self.hide()
        if self.material_widget.reset_library_callback():
            self.actions_to_finalize()

    def export_material_library_callback(self):
        self.hide()
        if self.material_widget.export_library_callback():
            self.actions_to_finalize()

    def import_material_library_callback(self):
        self.hide()
        if self.material_widget.import_library_callback():
            self.actions_to_finalize()

    def geometry_selection_callback(self):

        if self.tabWidget_main.currentIndex() == TabType.LIST:
            self.verify_if_selected_volumes_belongs_to_table_model_materials()
            return

        volumes = app().main_window.selection.geometry_volumes
        surfaces = app().main_window.selection.geometry_surfaces

        volume_exists = self.mesh.are_there_volumes_in_geometry()
        index = self.comboBox_attribution_type.currentIndex()

        selected_ids = set()
        if volume_exists:
            if volumes:
                selected_ids = volumes
                self.comboBox_attribution_type.setCurrentIndex(1)
            elif surfaces and index == 1:
                self.clear_line_edit_seletction_id()
        else:
            if surfaces:
                selected_ids = surfaces
                self.comboBox_attribution_type.setCurrentIndex(1)
            elif volumes and index == 1:
                self.clear_line_edit_seletction_id()
        if len(selected_ids):
            text = ", ".join([str(i) for i in selected_ids])
            self.lineEdit_selection_id.setText(text)

    def verify_if_selected_volumes_belongs_to_table_model_materials(self):
        if self.table_model_materials_cell_clicked:
            return

        selected_volumes = app().main_window.selection.geometry_volumes

        if not selected_volumes:
            return

        table_model_materials_map = self.get_table_widget_model_materials_items_map()

        self.clear_line_edit_seletction_id()
        self.tableWidget_model_materials.clearSelection()
        self.pushButton_remove.setDisabled(True)

        selected_ids = set(table_model_materials_map.keys())
        volumes_in_table_widget = selected_volumes.intersection(selected_ids)

        if not volumes_in_table_widget:
            return

        self.pushButton_remove.setEnabled(True)
        self.tableWidget_model_materials.setSelectionMode(QAbstractItemView.MultiSelection)

        self.selected_items["volumes"].clear()

        for volume in volumes_in_table_widget:
            self.tableWidget_model_materials.selectRow(table_model_materials_map[volume])

            self.selected_items["volumes"].append(volume)

        self.set_selection_text(volumes_in_table_widget)
        self.tableWidget_model_materials.setSelectionMode(QAbstractItemView.SingleSelection)

    def get_table_widget_model_materials_items_map(self) -> dict:
        num_of_rows = self.tableWidget_model_materials.rowCount()
        map_id_to_row = dict()

        for row in range(num_of_rows):
            selected_item = self.tableWidget_model_materials.item(row, 0)

            _, id = selected_item.text().split("-")

            map_id_to_row[int(id)] = row

        return map_id_to_row

    def set_selection_text(self, selected_volumes: list | set):
        selected_volumes = list(selected_volumes)
        selected_volumes.sort()

        selected_volumes = map(str, selected_volumes)
        selection_text = "Volumes: "
        selection_text += ", ".join(selected_volumes)

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)

    def clear_line_edit_seletction_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")

    def _config_widgets(self):
        self.tableWidget_model_materials.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_model_materials.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget_model_materials.setEditTriggers(QAbstractItemView.EditTrigger(0))
        self.tableWidget_model_materials.setSelectionBehavior(QAbstractItemView.SelectRows)

    def update_material_selection(self, selected_column: int):

        if not isinstance(selected_column, int):
            return

        item = self.material_widget.tableWidget_material_data.item(0, selected_column)
        if item is None:
            return

        material_name = item.text()
        self.lineEdit_selected_material_name.clear()

        if material_name != "":
            self.lineEdit_selected_material_name.setText(material_name)

    def attribution_type_callback(self):

        if self.comboBox_attribution_type.currentIndex():
            self.clear_line_edit_seletction_id()
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

    def apply_callback(self, close_window: bool = False):

        selected_material = self.material_widget.get_selected_material()

        if selected_material is None:
            self.title = "No materials selected"
            self.message = "Select a material in the list before confirming the material attribution."
            PrintMessageInput([error_title, self.title, self.message])
            return

        current_text = self.comboBox_attribution_type.currentText()

        if "surfaces" in current_text:
            if "All" in current_text:
                surface_ids = []
                if "surfaces" in self.mesh.geometry_information.keys():
                    surface_ids = self.mesh.geometry_information["surfaces"]

            else:
                input_ids = self.lineEdit_selection_id.text()
                surface_ids, error_data = self.mesh.check_selected_ids(input_ids, selection="surfaces", single_id=False)

                if error_data is not None:
                    self.lineEdit_selection_id.setFocus()
                    PrintMessageInput(error_data)
                    return True

            for surface_id in surface_ids:
                self.properties._set_property("material", selected_material, surface=surface_id)

        if "volumes" in current_text:
            if "All" in current_text:
                volume_ids = []
                if "volumes" in self.mesh.geometry_information:
                    volume_ids = self.mesh.geometry_information["volumes"]

            else:
                input_ids = self.lineEdit_selection_id.text()
                volume_ids, error_data = self.mesh.check_selected_ids(input_ids, selection="volumes", single_id=False)

                if error_data is not None:
                    self.lineEdit_selection_id.setFocus()
                    PrintMessageInput(error_data)
                    return True

            for volume_id in volume_ids:
                # we cannot have two physical domains active on the same volume
                self.properties._remove_volume_property("fluid", volume_id)
                self.properties._set_property("material", selected_material, volume=volume_id)

        self.actions_to_finalize(close_window)

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

        self.clear_line_edit_seletction_id()
        self.pushButton_remove.setDisabled(True)

        self.actions_to_finalize()
        app().main_window.selection.set_geometry_selection()

    def reset_callback(self):

        title = "Materials reset"
        message = "Would you like to remove the all assigned materials from model?"

        buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
        obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if obj._cancel:
            return

        if obj._continue:
            self.properties._reset_property("material")
            self.properties._reset_property("material_id")
            self.actions_to_finalize()

            app().main_window.selection.set_geometry_selection()

    def actions_to_finalize(self, close_window: bool = False):
        self.clear_line_edit_seletction_id()
        self.lineEdit_selected_material_name.clear()
        self.pushButton_remove.setDisabled(True)

        self.load_model_info()
        app().main_window.update_info_text()
        app().main_window.selection.clear_selection()  # this also updates
        app().main_window.update_symbols()
        app().project.update_model_properties_file()

        if close_window:
            self.close()

    def load_model_info(self):

        properties = {"Surface": self.properties.surface_properties, "Volume": self.properties.volume_properties}

        self.materials_from_model = dict()

        for selection, _property in properties.items():
            for key, data in _property.items():
                property, surface_id = key
                if property == "material":
                    data: Material
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

        for key in self.properties.volume_properties:
            property, _ = key
            if property != "material":
                continue

            self.tabWidget_main.setTabVisible(TabType.LIST, True)
            return

        for key in self.properties.surface_properties:
            property, _ = key
            if property == "material":
                continue

            self.tabWidget_main.setTabVisible(TabType.LIST, True)
            return

        self.tabWidget_main.setTabVisible(TabType.LIST, False)

    def tab_event_callback(self):
        app().main_window.selection.clear_selection()
        self.clear_line_edit_seletction_id()
        self.lineEdit_selected_material_name.clear()
        tab_list = self.tabWidget_main.currentIndex() == TabType.LIST

        if tab_list:
            self.pushButton_remove.setDisabled(True)
            self.lineEdit_selection_id.setDisabled(True)
            self.tableWidget_model_materials.clearSelection()

        else:
            self.attribution_type_callback()

        self.label_selected_material.setVisible(not tab_list)
        self.comboBox_attribution_type.setVisible(not tab_list)
        self.lineEdit_selected_material_name.setVisible(not tab_list)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()

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
