from PySide6.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea, QTableWidget
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from vibra import app, UI_DIR
from vibra.interface.model_inputs.acoustic.fluid.fluid_widget import FluidWidget
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

class SetFluidInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/fluid/set_fluid_input.ui"
        load_ui(ui_path, self, ui_path.parent)

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
        self._define_qt_variables()
        self._create_connections()

        if self.state_properties:
            self.load_compressor_info()

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

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type : QComboBox

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        # QLineEdit
        self.lineEdit_selection_id : QLineEdit
        self.lineEdit_selected_fluid_name : QLineEdit

        # QScrollArea
        self.scrollArea_table_of_fluids : QScrollArea
        self.scrollArea_table_of_fluids.setLayout(self.grid_layout)
        self._add_fluid_widget()

        # QPushButton
        self.pushButton_attribute = self.fluid_widget.pushButton_attribute
        self.pushButton_exit = self.fluid_widget.pushButton_exit

        # QTableWidget
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
        self.comboBox_attribution_type.currentIndexChanged.connect(self.update_attribution_type)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.fluid_widget.pushButton_reset_library.clicked.connect(self.reset_fluid_library_callback)
        #
        self.tableWidget_fluid_data.currentCellChanged.connect(self.current_cell_changed)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.update_attribution_type()

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

    def update_attribution_type(self):

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
                    app().project.set_fluid(selected_fluid, volume=volume_id)
                    for surface_id in self.model.mesh.surfaces_from_volumes[volume_id]:
                        app().project.set_fluid(selected_fluid, surface=surface_id)

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
                    app().project.set_fluid(selected_fluid, volume=volume_id)

                for surface_id in surface_ids:
                    app().project.set_fluid(selected_fluid, surface=surface_id)

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        # elif event.key() == Qt.Key_Delete:
        #     self.fluid_widget.remove_selected_row()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)