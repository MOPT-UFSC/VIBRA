from PySide6.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea, QTableWidget, QTabWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from vibra import app
from vibra.interface.ui_generated.model.setup.fluid.set_fluid_input_ui import SetFluidInput_UI
from vibra.engine.properties.fluid import Fluid
from vibra.interface.model_inputs.acoustic.fluid.fluid_widget import FluidWidget
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))


class SetFluidInput(SetFluidInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.cache_selected_lines = kwargs.get("cache_selected_lines", list())
        self.state_properties = kwargs.get("state_properties", dict())

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.action_model_workspace_callback()

        self.project = app().project
        self.model = app().project.model
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._configure_qt_variables()
        self._create_connections()
        self._config_widgets()

        if self.state_properties:
            self.load_compressor_info()

        self.load_model_info()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Set fluid")

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

    def _add_fluid_widget(self):
        self.fluid_widget = FluidWidget(dialog=self, state_properties=self.state_properties)
        self.grid_layout.addWidget(self.fluid_widget)
        self.fluid_widget.pushButton_remove_column.clicked.connect(self.reset_selected_fluid_lineEdit)

    def reset_selected_fluid_lineEdit(self):
        self.lineEdit_selected_fluid_name.setText("")

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
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_fluid.itemClicked.connect(self.on_click_item)
        self.treeWidget_fluid.itemDoubleClicked.connect(self.on_double_click_item)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.attribution_type_callback()

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.selected_column = current_col
        self.update_fluid_selection()

    def reset_fluid_library_callback(self):
        self.hide()
        self.fluid_widget.reset_library_callback()

    def geometry_selection_callback(self):

        volumes = self.main_window.selected_geometry_volumes

        if volumes:
            self.comboBox_attribution_type.setCurrentIndex(1)
            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selection_id.setText(text)

    def _config_widgets(self):
        #
        for i, width in enumerate([100, 160, 120, 140, 80]):
            self.treeWidget_fluid.setColumnWidth(i, width)
            self.treeWidget_fluid.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def update_fluid_selection(self):

        if self.selected_column is None:
            return

        item = self.tableWidget_fluid_data.item(0, self.selected_column)
        if item is None:
            return

        fluid_name = item.text()
        self.lineEdit_selected_fluid_name.setText("")
        if fluid_name != "":
            self.lineEdit_selected_fluid_name.setText(fluid_name)

    def attribution_type_callback(self):

        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selection_id.setText("All bodies")
        elif index == 1:
            self.lineEdit_selection_id.setText("")

        self.lineEdit_selection_id.setEnabled(bool(index))
        # self.comboBox_attribution_type.setCurrentIndex(index)

    def attribute_callback(self):

        selected_fluid = self.fluid_widget.get_selected_fluid()

        if selected_fluid is None:
            self.title = "No fluids selected"
            self.message = "Select a fluid in the list before confirming the fluid attribution."
            PrintMessageInput([window_title_1, self.title, self.message])
            return

        try:

            if self.comboBox_attribution_type.currentIndex():

                input_ids = self.lineEdit_selection_id.text()
                volume_ids = self.model.mesh.check_selected_ids(
                                                                input_ids, 
                                                                selection = "volumes", 
                                                                single_id = False
                                                                )

                if volume_ids is None:
                    self.lineEdit_selection_id.setFocus()
                    return True

                for volume_id in volume_ids:
                    self.properties._set_property("fluid", selected_fluid, volume=volume_id)
                    for surface_id in self.model.mesh.surfaces_from_volumes[volume_id]:
                        self.properties._set_property("fluid", selected_fluid, surface=surface_id)

                if len(volume_ids) <= 20:
                    print("[Set Fluid] - {} defined at bodies: {}".format(selected_fluid.name, volume_ids))
                else:
                    print("[Set Fluid] - {} defined at {} bodies".format(selected_fluid.name, len(volume_ids)))

            else:

                if "volumes" in self.model.mesh.geometry_information.keys():
                    volume_ids = self.model.mesh.geometry_information["volumes"]

                if "surfaces" in self.model.mesh.geometry_information.keys():
                    surface_ids = self.model.mesh.geometry_information["surfaces"]

                for volume_id in volume_ids:
                    self.properties._set_property("fluid", selected_fluid, volume=volume_id)

                for surface_id in surface_ids:
                    self.properties._set_property("fluid", selected_fluid, surface=surface_id)

                print("[Set Fluid] - {} defined at all bodies.".format(selected_fluid.name))

            app().file.write_model_properties_in_file()
            self.main_window.geometry_widget.update_info_text()
            self.main_window.mesh_widget.update_info_text()
            self.complete = True
            self.close()

        except Exception as error_log:
            title = "Error detected on fluid list data"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return

    def remove_callback(self):

        text = self.lineEdit_selection_id.text()

        if "-" in text:

            selection, _selected_id = text.split("-")
            selected_id = int(_selected_id)

            if selection == "Surface":
                self.properties._remove_surface_property("fluid", selected_id)
                self.properties._remove_surface_property("fluid_id", selected_id)

            elif selection == "Volume":
                self.properties._remove_volume_property("fluid", selected_id)
                self.properties._remove_volume_property("fluid_id", selected_id)

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

        self.lineEdit_selection_id.setText("")
        self.lineEdit_selected_fluid_name.setText("")

        self.load_model_info()
        app().main_window.update_info_text()
        app().file.write_model_properties_in_file()
        self.complete = True

    def load_model_info(self):

        self.treeWidget_fluid.clear()
        properties = {
                      "Surface" : self.properties.surface_properties,
                      "Volume" : self.properties.volume_properties
                      }

        for selection, _property in properties.items():
            for key, data in _property.items():
                property, surface_id = key
                if property == "fluid":

                    selection_id = f"{selection}-{surface_id}"

                    data : Fluid
                    fluid_name = data.name
                    density = f"{data.fluid_density : .6}"
                    speed_of_sound = f"{data.speed_of_sound : .4f}"
                    dynamic_viscosity = f"{data.dynamic_viscosity : .4e}"

                    new = QTreeWidgetItem([selection_id, 
                                           fluid_name, 
                                           density, 
                                           speed_of_sound, 
                                           dynamic_viscosity])

                    for col in range(5):
                        new.setTextAlignment(col, Qt.AlignCenter)

                    self.treeWidget_fluid.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        for key in self.properties.volume_properties.keys():
            property, _ = key
            if property == "fluid":
                self.tabWidget_main.setTabVisible(1, True)
                return

        for key in self.properties.surface_properties.keys():
            property, _ = key
            if property == "fluid":
                self.tabWidget_main.setTabVisible(1, True)
                return

        self.tabWidget_main.setTabVisible(1, False)

    def tab_event_callback(self):

        self.lineEdit_selected_fluid_name.setText("")

        if self.tabWidget_main.currentIndex() == 1:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_remove.setDisabled(True)
            self.comboBox_attribution_type.setDisabled(True)

        else:
            self.comboBox_attribution_type.setDisabled(False)
            self.attribution_type_callback()

    def on_click_item(self, item):

        self.pushButton_remove.setDisabled(False)

        if item.text(0) != "":
            selection, _selected_id = item.text(0).split("-")
            selected_id = int(_selected_id)

            if selection == "Surface":
                app().main_window.set_geometry_selection(surfaces = [int(selected_id)])

            elif selection == "Volume":
                app().main_window.set_geometry_selection(volumes = [int(selected_id)])

            app().main_window.action_model_workspace_callback()

            self.lineEdit_selection_id.setText(item.text(0))
            self.lineEdit_selected_fluid_name.setText(item.text(1))

    def on_double_click_item(self, item):
        self.on_click_item(item)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()

        elif event.key() == Qt.Key_Delete:
            self.remove_callback()

        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)