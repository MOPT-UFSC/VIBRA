from enum import IntEnum

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.interface import error_title
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.structural.definitions.enums import SetupTabType
from vibra.interface.ui_generated.model.structural.shell.surface_thickness_inputs_ui import SurfaceThicknessInputs_UI


class AssignmentType(IntEnum):
    ALL_SURFACES = 0
    SELECTED_SURFACES = 1


class SurfaceThicknessInputs(SurfaceThicknessInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

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
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_surface_thickness.itemClicked.connect(self.on_click_item)
        self.treeWidget_surface_thickness.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.attribution_type_callback()
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

    def geometry_selection_callback(self):

        faces = app().main_window.selection.geometry_surfaces

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

        if self.tabWidget_main.currentIndex() == SetupTabType.LIST:
            return

        data = self.model.properties._get_property("surface_thickness", surface=surface_id)
        if not isinstance(data, dict):
            return
    
        self.tabWidget_main.setCurrentIndex(SetupTabType.SETUP)
        self.lineEdit_surface_thickness.setText(str(data["surface_thickness"]))
        self.comboBox_thickness_offset.setCurrentText(data["thickness_offset"])

    def tab_event_callback(self):
        list_tab = self.tabWidget_main.currentIndex() == SetupTabType.LIST
        self.lineEdit_selection_id.setDisabled(list_tab)
        self.pushButton_apply.setDisabled(list_tab)
        self.pushButton_apply_and_close.setDisabled(list_tab)
        self.pushButton_remove.setDisabled(True)

        if list_tab:
            self.lineEdit_selection_id.setText("")
            return

    def attribution_type_callback(self):
        index = self.comboBox_attribution_type.currentIndex()
        if index == AssignmentType.ALL_SURFACES:
            self.lineEdit_selection_id.setText("All surfaces")

        elif index == AssignmentType.SELECTED_SURFACES:
            self.lineEdit_selection_id.setText("")

        self.lineEdit_selection_id.setEnabled(bool(index))

    def apply_callback(self, close_window: bool = False):

        if self.comboBox_attribution_type.currentIndex() == AssignmentType.ALL_SURFACES:
            surface_ids = self.model.mesh.geometry_information["surfaces"]
        
        else:
            input_ids = self.lineEdit_selection_id.text()
            surface_ids, error_data = self.mesh.check_selected_ids(input_ids, selection="surfaces")

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

        data = {
            "surface_thickness": surface_thickness,
            "thickness_offset": self.comboBox_thickness_offset.currentText(),
        }

        for surface_id in surface_ids:
            self.properties._set_property("surface_thickness", data, surface=surface_id)

        self.actions_to_finalize(close_window)

        # print(f"The surface thickness has been assigned to surface(s) {surface_ids}")

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
                    PrintMessageInput([error_title, title, message])
                    return None
                else:
                    return value

            except Exception:
                message = f"You have typed an invalid value to the {label}."
                PrintMessageInput([error_title, title, message])
                return None

        else:
            message = f"None value has been typed to the {label}."
            PrintMessageInput([error_title, title, message])
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

    def actions_to_finalize(self, close_window: bool = False):
        self.load_model_info()
        app().main_window.update_info_text()
        app().project.update_model_properties_file()
        app().main_window.update_symbols()

        if close_window:
            self.close()

    def update_tabs_visibility(self):
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property != "surface_thickness":
                continue
        
            self.tabWidget_main.setTabVisible(SetupTabType.LIST, True)
            return

        self.tabWidget_main.setTabVisible(SetupTabType.LIST, False)


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

            app().main_window.entity_visibility.hide_surfaces(surfaces_to_hide)    
            app().main_window.update_hidden_plots()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
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