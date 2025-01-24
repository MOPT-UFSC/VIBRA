from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea, QTableWidget
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.model_inputs.structural.material.material_widget import MaterialWidget
from vibra.interface.general.print_message_input import PrintMessageInput

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
        uic.loadUi(ui_path, self)

        self.cache_selected_lines = kwargs.get("cache_selected_lines", list())

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()

        self.project = app().project
        self.model = app().project.model
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        
        ConfigWidgetAppearance(self, tool_tip=True)

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
        self.complete = False
        self.material = None
        self.selected_column = None

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type = self.findChild(QComboBox, 'comboBox_attribution_type')

        # QFrame
        self.frame_main_widget = self.findChild(QFrame, 'frame_main_widget')

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        # QLineEdit
        self.lineEdit_selection_id = self.findChild(QLineEdit, 'lineEdit_selection_id')
        self.lineEdit_selected_material_name = self.findChild(QLineEdit, 'lineEdit_selected_material_name')

        # QScrollArea
        self.scrollArea_table_of_materials : QScrollArea
        self.scrollArea_table_of_materials.setLayout(self.grid_layout)
        self._add_material_widget()
        self.scrollArea_table_of_materials.adjustSize()

        # QPushButtonget_comboBox_index
        self.pushButton_attribute = self.findChild(QPushButton, 'pushButton_attribute')
        self.pushButton_exit = self.findChild(QPushButton, 'pushButton_exit')

        # QTableWidget
        self.tableWidget_material_data = self.findChild(QTableWidget, 'tableWidget_material_data')

    def _add_material_widget(self):
        self.material_widget = MaterialWidget()
        self.grid_layout.addWidget(self.material_widget)
        self.material_widget.pushButton_remove_column.clicked.connect(self.reset_selected_material_lineEdit)

    def reset_selected_material_lineEdit(self):
        self.lineEdit_selected_material_name.setText("")

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.update_attribution_type)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.material_widget.pushButton_reset_library.clicked.connect(self.reset_material_library_callback)
        #
        self.tableWidget_material_data.currentCellChanged.connect(self.current_cell_changed)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.update_attribution_type()

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.selected_column = current_col
        self.update_material_selection()

    def reset_material_library_callback(self):
        self.hide()
        self.material_widget.reset_library_callback()

    def geometry_selection_callback(self):

        volumes = self.main_window.selected_geometry_volumes

        if volumes:
            self.comboBox_attribution_type.setCurrentIndex(1)
            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selection_id.setText(text)

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

    def update_attribution_type(self):

        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selection_id.setText("All bodies/faces")
        elif index == 1:
            self.lineEdit_selection_id.setText("")

        self.lineEdit_selection_id.setEnabled(bool(index))
        # self.comboBox_attribution_type.setCurrentIndex(index)

    def attribute_callback(self):

        selected_material = self.material_widget.get_selected_material()

        if selected_material is None:
            self.title = "No materials selected"
            self.message = "Select a material in the list before confirming the material attribution."
            PrintMessageInput([window_title_1, self.title, self.message])
            return

        try:

            if self.comboBox_attribution_type.currentIndex():

                input_ids = self.lineEdit_selection_id.text()
                stop, volume_ids = self.model.mesh.check_selected_ids(input_ids, selection = "volumes", single_id = False)
                if stop:
                    self.lineEdit_selection_id.setFocus()
                    return True

                for volume_id in volume_ids:
                    app().project.set_material(selected_material, volume=volume_id)
                    for surface_id in self.model.mesh.surfaces_from_volumes[volume_id]:
                        app().project.set_material(selected_material, surface=surface_id)
        
                if len(volume_ids) <= 20:
                    print("[Set Material] - {} defined at bodies: {}".format(selected_material.name, volume_ids))
                else:
                    print("[Set Material] - {} defined at {} bodies".format(selected_material.name, len(volume_ids)))

            else:
                
                volume_ids = list()
                if "volumes" in self.model.mesh.geometry_information.keys():
                    volume_ids = self.model.mesh.geometry_information["volumes"]

                surface_ids = list()
                if "surfaces" in self.model.mesh.geometry_information.keys():
                    surface_ids = self.model.mesh.geometry_information["surfaces"]

                for volume_id in volume_ids:
                    app().project.set_material(selected_material, volume=volume_id)

                for surface_id in surface_ids:
                    app().project.set_material(selected_material, surface=surface_id)

                print("[Set Material] - {} defined at all bodies.".format(selected_material.name))

            app().file.write_model_properties_in_file()
            self.main_window.viewer_tabs.geometry_widget.update_info_text()
            self.main_window.viewer_tabs.mesh_widget.update_info_text()
            self.complete = True
            self.close()

        except Exception as error_log:
            title = "Error detected on material list data"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)