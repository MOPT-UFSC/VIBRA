from PySide6.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea, QTableWidget,  QTabWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from vibra import app, UI_DIR
from vibra.engine.properties.material import Material
from vibra.interface.model_inputs.structural.material.material_widget import MaterialWidget
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from molde import load_ui

window_title_1 = "Error"
window_title_2 = "Warning"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class SetMaterialInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/material/set_material.ui"
        load_ui(ui_path, self, ui_path.parent)

        self.cache_selected_lines = kwargs.get("cache_selected_lines", list())

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.action_model_workspace_callback()

        self.model = app().project.model
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
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

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type : QComboBox

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        # QLineEdit
        self.lineEdit_selection_id : QLineEdit
        self.lineEdit_selected_material_name : QLineEdit

        # QScrollArea
        self.scrollArea_table_of_materials : QScrollArea
        self.scrollArea_table_of_materials.setLayout(self.grid_layout)
        self._add_material_widget()
        self.scrollArea_table_of_materials.adjustSize()

        # QPushButton
        self.pushButton_attribute = self.material_widget.pushButton_attribute
        self.pushButton_exit = self.material_widget.pushButton_exit
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton

        # QTableWidget
        self.tableWidget_material_data = self.material_widget.tableWidget_material_data

        # QTreeWidget
        self.tabWidget_main : QTabWidget

        # QTreeWidget
        self.treeWidget_material : QTreeWidget

    def _add_material_widget(self):
        self.material_widget = MaterialWidget(dialog=self)
        self.grid_layout.addWidget(self.material_widget)
        self.material_widget.pushButton_remove_column.clicked.connect(self.reset_selected_material_lineEdit)

    def reset_selected_material_lineEdit(self):
        self.lineEdit_selected_material_name.setText("")

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
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_material.itemClicked.connect(self.on_click_item)
        self.treeWidget_material.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.attribution_type_callback()

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.selected_column = current_col
        self.update_material_selection()

    def reset_material_library_callback(self):
        self.hide()
        self.material_widget.reset_library_callback()

    def geometry_selection_callback(self):

        if self.tabWidget_main.currentIndex() == 1:
            return

        volumes = app().main_window.selected_geometry_volumes
        surfaces = app().main_window.selected_geometry_surfaces

        if volumes:
            selected_ids = volumes
            self.comboBox_attribution_type.setCurrentIndex(3)
            
        elif surfaces:
            selected_ids = surfaces
            self.comboBox_attribution_type.setCurrentIndex(4)
        
        else:
            selected_ids = set()

        if len(selected_ids):
            text = ", ".join([str(i) for i in selected_ids])
            self.lineEdit_selection_id.setText(text)

    def _config_widgets(self):
        #
        for i, width in enumerate([100, 130, 150, 120, 80]):
            self.treeWidget_material.setColumnWidth(i, width)
            self.treeWidget_material.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def update_material_selection(self):

        if self.selected_column is None:
            return

        item = self.tableWidget_material_data.item(0, self.selected_column)
        if item is None:
            return

        material_name = item.text()
        self.lineEdit_selected_material_name.setText("")
        if material_name != "":
            self.lineEdit_selected_material_name.setText(material_name)

    def attribution_type_callback(self):

        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selection_id.setText("All bodies/faces")
        elif index == 1:
            self.lineEdit_selection_id.setText("All bodies")
        elif index == 2:
            self.lineEdit_selection_id.setText("All faces")
        else:
            self.lineEdit_selection_id.setText("")

        if index in [0, 1, 2]:
            self.lineEdit_selection_id.setEnabled(False)
        else:
            self.lineEdit_selection_id.setEnabled(True)

    def attribute_callback(self):

        selected_material = self.material_widget.get_selected_material()

        if selected_material is None:
            self.hide()
            self.title = "No materials selected"
            self.message = "Select a material in the list before confirming the material attribution."
            PrintMessageInput([window_title_1, self.title, self.message])
            return

        attribution_type = self.comboBox_attribution_type.currentIndex()

        if attribution_type in [0, 1, 2]:

            if attribution_type in [0, 1]:
                volume_ids = list()
                if "volumes" in self.model.mesh.geometry_information.keys():
                    volume_ids = self.model.mesh.geometry_information["volumes"]

                for volume_id in volume_ids:
                    self.properties._set_property("material", selected_material, volume=volume_id)

            if attribution_type in [0, 2]:
                surface_ids = list()
                if "surfaces" in self.model.mesh.geometry_information.keys():
                    surface_ids = self.model.mesh.geometry_information["surfaces"]

                for surface_id in surface_ids:
                    self.properties._set_property("material", selected_material, surface=surface_id)

        elif attribution_type in [3, 5]:

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
                self.properties._set_property("material", selected_material, volume=volume_id)

                if attribution_type == 5:
                    for surface_id in self.model.mesh.surfaces_from_volumes[volume_id]:
                        self.properties._set_property("material", selected_material, surface=surface_id)

        elif attribution_type == 4:

            input_ids = self.lineEdit_selection_id.text()
            surface_ids = self.model.mesh.check_selected_ids(
                                                                input_ids, 
                                                                selection = "surfaces", 
                                                                single_id = False
                                                                )

            if surface_ids is None:
                self.lineEdit_selection_id.setFocus()
                return True

            for surface_id in surface_ids:
                self.properties._set_property("material", selected_material, surface=surface_id)

        self.actions_to_finalize()
        self.close()

    def remove_callback(self):

        text = self.lineEdit_selection_id.text()

        if "-" in text:

            selection, _selected_id = text.split("-")
            selected_id = int(_selected_id)

            if selection == "Surface":
                self.properties._remove_surface_property("material", selected_id)
                self.properties._remove_surface_property("material_id", selected_id)

            elif selection == "Volume":
                self.properties._remove_volume_property("material", selected_id)
                self.properties._remove_volume_property("material_id", selected_id)

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

        self.lineEdit_selection_id.setText("")
        self.lineEdit_selected_material_name.setText("")

        self.load_model_info()
        app().main_window.update_info_text()
        # app().main_window.geometry_widget.update_info_text()
        # app().main_window.mesh_widget.update_info_text()
        app().file.write_model_properties_in_file()
        self.complete = True

    def load_model_info(self):

        self.treeWidget_material.clear()
        properties = {
                      "Surface" : self.properties.surface_properties,
                      "Volume" : self.properties.volume_properties
                      }

        for selection, _property in properties.items():
            for key, data in _property.items():
                property, surface_id = key
                if property == "material":

                    data : Material
                    material_name = data.name
                    elasticity_modulus = round(data.elasticity_modulus / 1e9, 3)
                    density = round(data.density, 3)
                    poisson_ratio = round(data.poisson_ratio, 3)

                    new = QTreeWidgetItem([f"{selection}-{surface_id}", material_name, str(elasticity_modulus), str(density), str(poisson_ratio)])
                    for col in range(5):
                        new.setTextAlignment(col, Qt.AlignCenter)

                    self.treeWidget_material.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        for key in self.properties.volume_properties.keys():
            property, _ = key
            if property == "material":
                self.tabWidget_main.setTabVisible(1, True)
                return

        for key in self.properties.surface_properties.keys():
            property, _ = key
            if property == "material":
                self.tabWidget_main.setTabVisible(1, True)
                return

        self.tabWidget_main.setTabVisible(1, False)

    def tab_event_callback(self):

        self.lineEdit_selected_material_name.setText("")

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
            self.lineEdit_selected_material_name.setText(item.text(1))

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