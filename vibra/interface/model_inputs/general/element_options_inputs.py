from enum import IntEnum

from PySide6.QtCore import Qt

from vibra import app
from vibra.engine.elements.element_options import HEX8_structural
from vibra.engine.mesher.mesh_setup import HEXAHEDRON_8, HEXAHEDRON_20, TETRAHEDRON_4, TETRAHEDRON_10, ElementTopology
from vibra.engine.mesher.mesh_setup import MeshSetup

# from vibra.interface import error_title, warning_title
# from vibra.interface.general.print_message_input import PrintMessageInput
# from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.ui_generated.model.general.element_options_input_ui import ElementOptionsInput_UI


class TabType(IntEnum):
    HEX8 = 0
    HEX20 = 1
    TET4 = 2
    TET10 = 3


# class ElementGeometry(StrEnum):
#     HEXAHEDRAL = "hexahedral"
#     TETRAHEDRAL = "tetrahedral"


# class ShapeOrder(StrEnum):
#     LINEAR = "linear"
#     QUADRATIC = "quadratic"


class ElementOptionsInputs(ElementOptionsInput_UI):
    def __init__(self, **kwargs):
        super().__init__()

        app().main_window.set_input_widget(self)
        self.model = app().project.model

        self._initialize()
        self._config_window()
        self._config_widgets()
        self._create_connections()
        self.update_tab_visibility()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.complete = False
        self.keep_window_open = True

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _config_widgets(self):
        # hide temporarily unused hex8 element options
        self.label_option_2.setVisible(False)
        self.label_option_3.setVisible(False)
        self.comboBox_option_2.setVisible(False)
        self.comboBox_option_3.setVisible(False)

    def _create_connections(self):
        self.pushButton_apply.clicked.connect(self.set_element_options_callback)
        self.pushButton_cancel.clicked.connect(self.close)

    def load_advanced_options(self):

        advanced_element_options = self.model.properties._get_property("advanced_element_options")
        if not isinstance(advanced_element_options, dict):
            return

        if self.tabWidget_main.currentIndex() == TabType.HEX8:
            hex8_options = advanced_element_options.get("hex8", dict)
            if not isinstance(hex8_options, dict):
                return

            extra_shape_function = hex8_options.get("extra_shape_functions")
            self.comboBox_extra_shape_functions.setCurrentText("enabled" if extra_shape_function else "disabled")

    def update_tab_visibility(self):

        mesh_setup = app().project.model.mesh_setup
        if not isinstance(mesh_setup, MeshSetup):
            return
        
        element_type = app().project.model.element_topology
        if not isinstance(element_type, ElementTopology):
            NotImplementedError("ElementTopology not found")
            return

        for i in range(4):
            self.tabWidget_main.setTabVisible(i, False)

        if element_type == TETRAHEDRON_4:
            self.tabWidget_main.setTabVisible(TabType.TET4, True)

        elif element_type == TETRAHEDRON_10:
            self.tabWidget_main.setTabVisible(TabType.TET10, True)

        elif element_type == HEXAHEDRON_8:
            self.tabWidget_main.setTabVisible(TabType.HEX8, True)

        elif element_type == HEXAHEDRON_20:
            self.tabWidget_main.setTabVisible(TabType.HEX20, True)

        else:
            NotImplementedError("Invalid ElementType")
            return

        self.load_advanced_options()

    def set_element_options_callback(self):
        advanced_options = dict()
        if self.tabWidget_main.currentIndex() == TabType.HEX8:
            hex8_options = HEX8_structural()
            hex8_options.extra_shape_functions = self.comboBox_extra_shape_functions.currentText() == "enabled"
            advanced_options["hex8"] = hex8_options.get_data()

        if not advanced_options:
            return

        self.model.properties._set_property("advanced_element_options", advanced_options)
        app().project.update_model_properties_file()

        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.close()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)