from PySide6.QtWidgets import QAbstractItemView, QGridLayout, QHeaderView, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from vibra import app
from vibra.interface.ui_generated.model.setup.fluid.set_fluid_inputs_ui import SetFluidInputs_UI
from vibra.engine.properties.fluid import Fluid
from vibra.interface.model_inputs.general.fluid.fluid_widget import FluidWidget
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

from collections import defaultdict
from enum import IntEnum

error_title = "Error"
warning_title = "Warning"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class TabType(IntEnum):
    SETUP = 0
    LIST = 1

class AttributionType(IntEnum):
    ALL_BODIES = 0
    SELECTED_BODIES = 1


class SetFluidInputs(SetFluidInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.cache_selected_lines = kwargs.get("cache_selected_lines", list())
        self.state_properties = kwargs.get("state_properties", dict())

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()
        app().main_window.volume_selection_mode = True

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._configure_qt_variables()
        self._create_connections()
        self._config_widgets()

        if self.state_properties:
            self.load_compressor_info()

        self.load_model_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.keep_window_open = True
        self.complete = False
        self.fluid = None
        self.selected_column = None

    def _configure_qt_variables(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        self.scrollArea_table_of_fluids.setLayout(self.grid_layout)
        self._add_fluid_widget()

        self.pushButton_attribute = self.fluid_widget.pushButton_attribute
        self.pushButton_exit = self.fluid_widget.pushButton_exit

        self.tableWidget_fluid_data = self.fluid_widget.tableWidget_fluid_data
        self.tableWidget_model_fluids : QTableWidget

    def _add_fluid_widget(self):
        self.fluid_widget = FluidWidget(dialog=self, state_properties=self.state_properties)
        self.grid_layout.addWidget(self.fluid_widget)
        self.fluid_widget.pushButton_remove_column.clicked.connect(self.reset_selected_fluid_lineEdit)

    def reset_selected_fluid_lineEdit(self):
        self.lineEdit_selected_fluid_name.clear()

    def load_compressor_info(self):
        self.fluid_widget.load_compressor_info()

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.fluid_widget.pushButton_reset_library.clicked.connect(self.reset_fluid_library_callback)
        #
        self.tableWidget_fluid_data.currentCellChanged.connect(self.current_cell_changed)
        self.tableWidget_model_fluids.cellClicked.connect(self.cell_clicked_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.attribution_type_callback()
        self.geometry_selection_callback()

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.selected_column = current_col
        self.update_fluid_selection()

    def cell_clicked_callback(self, row, col):
        selected_items, selection_text, fluid_text = self.get_selected_items_and_texts()

        if not selected_items:
            return

        app().main_window.set_geometry_selection(**selected_items)

        self.pushButton_remove.setEnabled(True)
        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)
        self.lineEdit_selected_fluid_name.setText(fluid_text)

        app().main_window.action_model_workspace_callback()

    def reset_fluid_library_callback(self):
        self.hide()
        if self.fluid_widget.reset_library_callback():
            self.actions_to_finalize()

    def geometry_selection_callback(self):
        if self.tabWidget_main.currentIndex() == TabType.LIST:
            return

        volumes = app().main_window.selected_geometry_volumes
        if volumes:
            self.comboBox_attribution_type.setCurrentIndex(AttributionType.SELECTED_BODIES)

            if len(volumes):
                text = ", ".join([str(i) for i in volumes])
                self.lineEdit_selection_id.setText(text)

    def _config_widgets(self):
        self.tableWidget_model_fluids.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))
        self.tableWidget_model_fluids.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget_model_fluids.setEditTriggers(QAbstractItemView.EditTrigger(0))
        self.tableWidget_model_fluids.setSelectionBehavior(QAbstractItemView.SelectRows)

    def update_fluid_selection(self):

        if self.selected_column is None:
            return

        item = self.tableWidget_fluid_data.item(0, self.selected_column)
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

    def attribute_callback(self):

        selected_fluid = self.fluid_widget.get_selected_fluid()

        if selected_fluid is None:
            self.hide()
            self.title = "No fluids selected"
            self.message = "Select a fluid in the list before confirming the fluid attribution."
            PrintMessageInput([error_title, self.title, self.message])
            return

        volume_ids = list()
        attribution_type = self.comboBox_attribution_type.currentIndex()

        if attribution_type == AttributionType.ALL_BODIES:
            if "volumes" in self.mesh.geometry_information.keys():
                volume_ids = self.mesh.geometry_information["volumes"]

        else:
            input_ids = self.lineEdit_selection_id.text()
            volume_ids, error_data = self.mesh.check_selected_ids(
                                                                   input_ids, 
                                                                   selection = "volumes", 
                                                                   single_id = False,
                                                                   )

            if error_data is not None:
                self.hide()
                self.lineEdit_selection_id.setFocus()
                PrintMessageInput(error_data)
                return

        if not volume_ids:
            return

        for volume_id in volume_ids:
            self.properties._set_property("fluid", selected_fluid, volume=volume_id)

            for surface_id in self.mesh.surfaces_from_volume[volume_id]:
                self.properties._set_property("fluid", selected_fluid, surface=surface_id)

        self.actions_to_finalize()

        if attribution_type == AttributionType.ALL_BODIES:
            self.close()

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
    
        self.lineEdit_selection_id.clear()
        self.pushButton_remove.setDisabled(True)

        self.actions_to_finalize()
        app().main_window.set_geometry_selection()

    def reset_callback(self):

        self.hide()

        title = "Fluids resetting"
        message = "Would you like to remove the all assigned fluids from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if obj._cancel:
            return

        if obj._continue:

            self.properties._reset_property("fluid")
            self.properties._reset_property("fluid_id")
            self.actions_to_finalize()

            app().main_window.set_geometry_selection()

    def actions_to_finalize(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selected_fluid_name.clear()
        self.pushButton_remove.setDisabled(True)

        self.load_model_info()
        app().main_window.update_info_text()
        app().main_window.clear_selection()  # this also updates
        app().main_window.update_symbols()
        app().file.write_model_properties_in_file()

        self.complete = True

    def load_model_info(self):

        properties = {
                    #   "Surface" : self.properties.surface_properties,
                      "Volume" : self.properties.volume_properties
                      }

        self.model_fluids = dict()

        for selection, _property in properties.items():
            for key, data in _property.items():
                property, surface_id = key
                if property == "fluid":
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

        for key in self.properties.volume_properties.keys():
            property, _ = key
            if property == "fluid":
                self.tabWidget_main.setTabVisible(TabType.LIST, True)
                return

        for key in self.properties.surface_properties.keys():
            property, _ = key
            if property == "fluid":
                self.tabWidget_main.setTabVisible(TabType.LIST, True)
                return

        self.tabWidget_main.setTabVisible(TabType.LIST, False)

    def tab_event_callback(self):
        app().main_window.clear_selection()

        self.lineEdit_selection_id.clear()
        self.lineEdit_selected_fluid_name.clear()

        if self.tabWidget_main.currentIndex() == TabType.LIST:
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_remove.setDisabled(True)
            self.comboBox_attribution_type.setDisabled(True)

            self.tableWidget_model_fluids.clearSelection()

        else:
            self.comboBox_attribution_type.setDisabled(False)
            self.attribution_type_callback()
    
    def get_selected_items_and_texts(self) -> tuple[dict, str, str]:
        selected_cells = self.tableWidget_model_fluids.selectedItems()

        if not selected_cells:
            return dict(), str(), str()

        selected_items = defaultdict(list)
        selection_text = str()
        fluid_types = set()

        for i in range(len(selected_cells) // 5):
            index = i * 5

            selected_item = selected_cells[index].text()
            fluid_type = selected_cells[index + 1].text()

            selected_type, selected_id = selected_item.split("-")
            selected_type = selected_type.lower() + "s"

            selected_items[selected_type].append(int(selected_id))
            fluid_types.add(fluid_type)
        
        fluid_text = fluid_types.pop() if len(fluid_types) == 1 else "--"

        for selected_type, ids in selected_items.items():
            ids.sort()

            ids = map(str, ids)
            selection_text += selected_type.capitalize() + ": " + ", ".join(ids) + " "

        self.selected_items = selected_items

        return selected_items, selection_text, fluid_text

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()

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
        app().main_window.volume_selection_mode = False
        return super().closeEvent(a0)