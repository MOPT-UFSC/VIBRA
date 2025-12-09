from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.ui_generated.model.setup.structural.surface_thickness_inputs_ui import SurfaceThicknessInputs_UI
from vibra.interface.model_inputs.data_filter.change_frequency_data_handler import ChangeFrequencyDataRangeInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput


window_title_1 = "Error"
window_title_2 = "Warning"


class SurfaceThicknessInputs(SurfaceThicknessInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
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
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.imported_values = None
        self.keep_window_open = True

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_surface_thickness.itemClicked.connect(self.on_click_item)
        self.treeWidget_surface_thickness.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.attribution_type_callback()
        app().main_window.selection_changed.connect(self.geometry_selection_callback)

    def geometry_selection_callback(self):

        faces = app().main_window.selected_geometry_surfaces

        if faces:

            self.comboBox_attribution_type.setCurrentIndex(1)

            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)

            if len(faces) == 1:
                surface_id = list(faces)[0]
                self.load_property_data(surface_id)

    def _config_widgets(self):
        #
        for i, width in enumerate([80, 120, 110]):
            self.treeWidget_surface_thickness.setColumnWidth(i, width)
            self.treeWidget_surface_thickness.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def load_property_data(self, surface_id: int):

        if self.tabWidget_main.currentIndex() == 1:
            return

        data = self.model.properties._get_property("surface_thickness", surface=surface_id)

        if isinstance(data, dict):
            self.tabWidget_main.setCurrentIndex(0)
            self.lineEdit_surface_thickness.setText(str(data["surface_thickness"]))
            self.comboBox_thickness_offset.setCurrentText(data["thickness_offset"])

    def tab_event_callback(self):
        if self.tabWidget_main.currentIndex() == 1:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.pushButton_attribute.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)
            self.pushButton_attribute.setEnabled(True)

    def attribution_type_callback(self):

        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selection_id.setText("All surfaces")
        elif index == 1:
            self.lineEdit_selection_id.setText("")

        self.lineEdit_selection_id.setEnabled(bool(index))

    def attribute_callback(self):

        if self.comboBox_attribution_type.currentIndex() == 0:
            surface_ids = self.model.mesh.geometry_information["surfaces"]
        
        else:
            input_ids = self.lineEdit_selection_id.text()
            surface_ids, error_data = self.mesh.check_selected_ids(
                                                                input_ids, 
                                                                selection = "surfaces"
                                                                )

            if error_data is not None:
                self.hide()
                self.lineEdit_selection_id.setFocus()
                PrintMessageInput(error_data)
                return

        surface_thickness = self.check_input_parameters(self.lineEdit_surface_thickness, "Surface thickness")

        if surface_thickness is None:
            self.hide()
            self.lineEdit_surface_thickness.setFocus()
            return

        thickness_offset = self.comboBox_thickness_offset.currentText()

        data = {
                "surface_thickness": surface_thickness,
                "thickness_offset": thickness_offset,
                }

        for surface_id in surface_ids:
            self.properties._set_property("surface_thickness", data, surface=surface_id)

        self.actions_to_finalize()

        # print(f"The surface thickness has been assigned to surface(s) {surface_ids}")

        if self.comboBox_attribution_type.currentIndex() == 0:
            self.close()

    def check_input_parameters(self, lineEdit: QLineEdit, label: str, _float=True):

        title = "Input error"
        value_string = lineEdit.text()

        if value_string != "":

            value_string = value_string.replace(",", ".")

            try:

                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string)

                if value < 0:
                    message = f"You cannot input a negative value to the {label}."
                    PrintMessageInput([window_title_1, title, message])
                    return None
                else:
                    return value

            except Exception:
                message = f"You have typed an invalid value to the {label}."
                PrintMessageInput([window_title_1, title, message])
                return None

        else:
            message = f"None value has been typed to the {label}."
            PrintMessageInput([window_title_1, title, message])
            return None

    def remove_callback(self):

        if self.lineEdit_selection_id.text() != "":

            surface_id = int(self.lineEdit_selection_id.text())

            self.properties._remove_surface_property("surface_thickness", surface_id)
            self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Surface thickness resetting"
        message = "Would you like to remove the all assigned surface thickness from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            surface_ids = list()
            for (property, *args) in self.properties.surface_properties.keys():
                if property == "surface_thickness":

                    surface_id = args[0]
                    surface_ids.append(surface_id)

            self.properties._reset_property("surface_thickness")
            self.actions_to_finalize()

    def actions_to_finalize(self):
        self.load_model_info()
        app().main_window.update_info_text()
        app().file.write_model_properties_in_file()
        app().file.write_imported_table_data_in_file()
        app().main_window.update_symbols()
        app().main_window.update_symbols()

    def update_tabs_visibility(self):
        surface_ids = list()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "surface_thickness":
                surface_ids.append(surface_id)

        if len(surface_ids) == 0:
            self.tabWidget_main.setTabVisible(1, False)
        else:
            self.tabWidget_main.setTabVisible(1, True)

    def on_click_item(self, item):
        if item.text(0) != "":
            surface_id = int(item.text(0))
            self.lineEdit_selection_id.setText(item.text(0))
            app().main_window.selection.set_geometry_selection(surfaces=[surface_id])

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def load_model_info(self):
        self.treeWidget_surface_thickness.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "surface_thickness":

                surface_thickness = data["surface_thickness"]
                thickness_offset = data["thickness_offset"]

                new = QTreeWidgetItem([str(surface_id), str(surface_thickness), thickness_offset])
                for col in range(3):
                    new.setTextAlignment(col, Qt.AlignCenter)

                self.treeWidget_surface_thickness.addTopLevelItem(new)

        self.update_tabs_visibility()

    def process_surfaces_according_with_thickness_setup(self):

        surfaces_to_hide = list()
        surface_ids = self.model.mesh.geometry_information["surfaces"]

        for surface_id in surface_ids:
            surface_data = self.properties._get_property("surface_thickness", surface=surface_id)
            if surface_data is None:
                surfaces_to_hide.append(surface_id)

        if surfaces_to_hide:

            if len(surface_ids) == len(surfaces_to_hide):
                return

            for _surface_id in surfaces_to_hide:
                app().main_window.hidden_surfaces.add(_surface_id)
    
            app().main_window.update_hidden_plots()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            return

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        self.process_surfaces_according_with_thickness_setup()
        return super().closeEvent(a0)