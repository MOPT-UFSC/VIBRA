from collections import defaultdict
from enum import IntEnum

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QGridLayout, QHeaderView, QTableWidgetItem

from vibra import app
from vibra.engine.properties.fluid import Fluid
from vibra.interface import error_title
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.fluid.fluid_widget import FluidWidget
from vibra.interface.ui_generated.model.fluid.set_fluid_inputs_ui import SetFluidInputs_UI


class TabType(IntEnum):
    SETUP = 0
    LIST = 1


class AttributionType(IntEnum):
    ALL_BODIES = 0
    SELECTED_BODIES = 1


class SetFluidInputs(SetFluidInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.state_properties = kwargs.get("state_properties", {})

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()
        app().main_window.selection.volume_selection_mode = True

        self._initialize()
        self._config_window()
        self._config_widgets()
        self._add_fluid_widget()
        self._create_connections()

        if self.state_properties:
            self.fluid_widget.load_state_properties_info()

        self.load_model_info()

        while self.keep_window_open:
            self.exec()

    @property
    def properties(self):
        return app().project.model.properties

    @property
    def mesh(self):
        return app().project.model.mesh

    def _initialize(self):
        self.fluid = None
        self.keep_window_open = True
        self.complete = False
        self.table_model_fluids_cell_clicked = False
        self.selected_items = defaultdict(list)

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _add_fluid_widget(self):

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.scrollArea_table_of_fluids.setLayout(self.grid_layout)

        self.fluid_widget = FluidWidget(state_properties=self.state_properties)
        self.grid_layout.addWidget(self.fluid_widget)

    def reset_selected_fluid_lineEdit(self):
        self.lineEdit_selected_fluid_name.clear()

    def _config_widgets(self):
        self.tableWidget_model_fluids.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))
        self.tableWidget_model_fluids.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget_model_fluids.setEditTriggers(QAbstractItemView.EditTrigger(0))
        self.tableWidget_model_fluids.setSelectionBehavior(QAbstractItemView.SelectRows)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.fluid_widget.modified.connect(self.load_model_info)
        self.fluid_widget.pushButton_apply.clicked.connect(self.apply_callback)
        self.fluid_widget.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.fluid_widget.pushButton_cancel.clicked.connect(self.close)
        self.fluid_widget.pushButton_remove_column.clicked.connect(self.reset_selected_fluid_lineEdit)
        self.fluid_widget.pushButton_reset_library.clicked.connect(self.reset_fluid_library_callback)
        self.fluid_widget.pushButton_export_library.clicked.connect(self.export_fluid_library_callback)
        self.fluid_widget.pushButton_import_library.clicked.connect(self.import_fluid_library_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.fluid_widget.tableWidget_fluid_data.currentCellChanged.connect(self.current_cell_changed)
        self.tableWidget_model_fluids.cellClicked.connect(self.cell_clicked_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.attribution_type_callback()
        self.geometry_selection_callback()

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.update_fluid_selection(current_col)

    def cell_clicked_callback(self, row, col):
        self.table_model_fluids_cell_clicked = True

        selection_text = self.set_selected_items_and_get_selection_text()

        if not self.selected_items:
            return

        app().main_window.selection.set_geometry_selection(**self.selected_items)

        self.pushButton_remove.setEnabled(True)
        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)

        app().main_window.action_model_workspace_callback()

        self.table_model_fluids_cell_clicked = False

    def reset_fluid_library_callback(self):
        self.hide()
        if self.fluid_widget.reset_library_callback():
            self.actions_to_finalize()

    def export_fluid_library_callback(self):
        self.hide()
        if self.fluid_widget.export_library_callback():
            self.actions_to_finalize()

    def import_fluid_library_callback(self):
        self.hide()
        if self.fluid_widget.import_library_callback():
            self.actions_to_finalize()

    def geometry_selection_callback(self):
        if self.tabWidget_main.currentIndex() == TabType.LIST:
            self.verify_if_selected_volumes_belongs_to_table_model_fluids()
            return

        volumes = app().main_window.selection.geometry_volumes
        if volumes:
            self.comboBox_attribution_type.setCurrentIndex(AttributionType.SELECTED_BODIES)

            if len(volumes):
                text = ", ".join([str(i) for i in volumes])
                self.lineEdit_selection_id.setText(text)
    
    def verify_if_selected_volumes_belongs_to_table_model_fluids(self):
        if self.table_model_fluids_cell_clicked:
            return

        selected_volumes = app().main_window.selection.geometry_volumes

        if not selected_volumes:
            return

        table_model_fluids_map = self.get_table_widget_model_fluids_items_map()

        self.clear_line_edit_seletction_id()
        self.tableWidget_model_fluids.clearSelection()
        self.pushButton_remove.setDisabled(True)

        selected_ids = set(table_model_fluids_map)
        volumes_in_table_widget = selected_volumes.intersection(selected_ids)

        if not volumes_in_table_widget:
            return

        self.pushButton_remove.setEnabled(True)
        self.tableWidget_model_fluids.setSelectionMode(QAbstractItemView.MultiSelection)

        self.selected_items["volumes"].clear()

        for volume in volumes_in_table_widget:
            self.tableWidget_model_fluids.selectRow(table_model_fluids_map[volume])
            self.selected_items["volumes"].append(volume)

        self.set_selection_text(volumes_in_table_widget)
        self.tableWidget_model_fluids.setSelectionMode(QAbstractItemView.SingleSelection)

    def get_table_widget_model_fluids_items_map(self) -> dict:
        num_of_rows = self.tableWidget_model_fluids.rowCount()
        map_id_to_row = {}

        for row in range(num_of_rows):
            selected_item = self.tableWidget_model_fluids.item(row, 0)

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

    def update_fluid_selection(self, selected_column: int):

        if not isinstance(selected_column, int):
            return

        item = self.fluid_widget.tableWidget_fluid_data.item(0, selected_column)
        if item is None:
            return

        fluid_name = item.text()
        self.lineEdit_selected_fluid_name.clear()

        if fluid_name != "":
            self.lineEdit_selected_fluid_name.setText(fluid_name)

    def attribution_type_callback(self):
        
        index = self.comboBox_attribution_type.currentIndex()

        text = ""
        if index == AttributionType.ALL_BODIES:
            text = "All bodies"

        self.lineEdit_selection_id.setText(text)
        self.lineEdit_selection_id.setEnabled(bool(index))

    def apply_callback(self, close_window: bool = False):

        selected_fluid = self.fluid_widget.get_selected_fluid()

        if selected_fluid is None:
            self.title = "No fluids selected"
            self.message = "Select a fluid in the list before confirming the fluid attribution."
            PrintMessageInput([error_title, self.title, self.message])
            return

        volume_ids = []
        attribution_type = self.comboBox_attribution_type.currentIndex()

        if attribution_type == AttributionType.ALL_BODIES:
            if "volumes" in self.mesh.geometry_information:
                volume_ids = self.mesh.geometry_information["volumes"]

        else:
            input_ids = self.lineEdit_selection_id.text()
            volume_ids, error_data = self.mesh.check_selected_ids(
                input_ids,
                selection="volumes",
                single_id=False,
            )

            if error_data is not None:
                self.lineEdit_selection_id.setFocus()
                PrintMessageInput(error_data)
                return

        if not volume_ids:
            return

        for volume_id in volume_ids:
            # we cannot have two physical domains active on the same volume
            self.properties._remove_volume_property("material", volume_id)
            self.properties._set_property("fluid", selected_fluid, volume=volume_id)

            for surface_id in self.mesh.surfaces_from_volume[volume_id]:
                self.properties._set_property("fluid", selected_fluid, surface=surface_id)

        self.actions_to_finalize(close_window)

    def remove_callback(self):
        if not self.selected_items:
            return

        for selection_type, ids in self.selected_items.items():
            for id in ids:
                if selection_type == "surfaces":
                    self.properties._remove_surface_property("fluid", id)
                    self.properties._remove_surface_property("fluid_id", id)

                elif selection_type == "volumes":
                    self.properties._remove_volume_property("fluid", id)
                    self.properties._remove_volume_property("fluid_id", id)
                    for surface_id in self.mesh.surfaces_from_volume[id]:
                        self.properties._remove_surface_property("fluid", surface_id)
                        self.properties._remove_surface_property("fluid_id", surface_id)
    
        self.clear_line_edit_seletction_id()
        self.pushButton_remove.setDisabled(True)

        self.actions_to_finalize()
        app().main_window.selection.set_geometry_selection()

    def reset_callback(self):

        title = "Fluids reset"
        message = "Would you like to remove the all assigned fluids from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if obj._cancel:
            return

        if obj._continue:
            self.properties._reset_property("fluid")
            self.properties._reset_property("fluid_id")
            self.actions_to_finalize()

            app().main_window.selection.set_geometry_selection()

    def actions_to_finalize(self, close_window: bool = False):
        self.load_model_info()
        self.clear_line_edit_seletction_id()
        self.lineEdit_selected_fluid_name.clear()
        self.pushButton_remove.setDisabled(True)

        app().main_window.update_info_text()
        app().main_window.selection.clear_selection()  # this also updates
        app().main_window.update_symbols()
        app().project.update_model_properties_file()

        self.complete = True

        if close_window:
            self.close()

    def load_model_info(self):

        properties = {
            #"Surface" : self.properties.surface_properties,
            "Volume" : self.properties.volume_properties,
            }

        self.model_fluids = {}

        for selection, _property in properties.items():
            for key, data in _property.items():
                property, surface_id = key
                if property != "fluid":
                    continue

                if not isinstance(data, Fluid):
                    continue

                selection_id = f"{selection}-{surface_id}"
                self.model_fluids[(data.identifier, selection_id)] = data

        self.load_table_info()
        self.update_tabs_visibility()

    def load_table_info(self):

        self.tableWidget_model_fluids.clearContents()
        self.tableWidget_model_fluids.blockSignals(True)
        self.tableWidget_model_fluids.setRowCount(len(self.model_fluids))
        self.tableWidget_model_fluids.setColumnCount(5)

        for i, (key, fluid) in enumerate(self.model_fluids.items()):
            fluid: Fluid
            _, selection_id = key
            if isinstance(fluid, Fluid):
                
                self.tableWidget_model_fluids.setItem(i, 0, QTableWidgetItem(selection_id))
                self.tableWidget_model_fluids.setItem(i, 1, QTableWidgetItem(str(fluid.name)))
                self.tableWidget_model_fluids.setItem(i, 2, QTableWidgetItem(str(fluid.identifier)))
                self.tableWidget_model_fluids.setItem(i, 3, QTableWidgetItem(str(fluid.fluid_density)))
                self.tableWidget_model_fluids.setItem(i, 4, QTableWidgetItem(str(fluid.speed_of_sound)))
                self.tableWidget_model_fluids.setItem(i, 5, QTableWidgetItem(f"{fluid.dynamic_viscosity : .4e}"))

        for i in range(self.tableWidget_model_fluids.rowCount()):
            for j in range(self.tableWidget_model_fluids.columnCount()):
                self.tableWidget_model_fluids.item(i, j).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_model_fluids.blockSignals(False)

    def update_tabs_visibility(self):

        for key in self.properties.volume_properties:
            property, _ = key
            if property != "fluid":
                continue

            self.tabWidget_main.setTabVisible(TabType.LIST, True)
            return

        for key in self.properties.surface_properties:
            property, _ = key
            if property != "fluid":
                continue

            self.tabWidget_main.setTabVisible(TabType.LIST, True)
            return

        self.tabWidget_main.setTabVisible(TabType.LIST, False)

    def tab_event_callback(self):
        app().main_window.selection.clear_selection()
        self.clear_line_edit_seletction_id()
        tab_list = self.tabWidget_main.currentIndex() == TabType.LIST

        if tab_list:
            self.pushButton_remove.setDisabled(True)
            self.lineEdit_selection_id.setDisabled(True)
            self.tableWidget_model_fluids.clearSelection()

        else:
            self.lineEdit_selected_fluid_name.clear()
            self.lineEdit_selection_id.setDisabled(False)
            self.attribution_type_callback()
        
        self.label_selected_fluid.setVisible(not tab_list)
        self.comboBox_attribution_type.setVisible(not tab_list)
        self.lineEdit_selected_fluid_name.setVisible(not tab_list)

    def set_selected_items_and_get_selection_text(self) -> str:
        selected_cells = self.tableWidget_model_fluids.selectedItems()

        if not selected_cells:
            return str()
        
        selected_items = defaultdict(list)
        selection_text = str()

        num_of_columns = self.tableWidget_model_fluids.columnCount()

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()

        elif event.key() == Qt.Key_Delete:
            self.remove_callback()

        elif event.key() == Qt.Key_Escape:
            self.close()
        
        elif event.key() == Qt.Key_Control:
            self.tableWidget_model_fluids.setSelectionMode(QAbstractItemView.MultiSelection)
        
        elif event.key() == Qt.Key_Shift:
            self.tableWidget_model_fluids.setSelectionMode(QAbstractItemView.ContiguousSelection)
        
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.tableWidget_model_fluids.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection.volume_selection_mode = False
        return super().closeEvent(a0)