import configparser
import os
from pathlib import Path

import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDoubleSpinBox, QDialog, QLineEdit, QPushButton, QTabWidget

from vibra.interface.general.call_double_confirmation_input import (
    CallDoubleConfirmationInput,
)
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.interface_functions import get_main_window

window_title_1 = "Error"
window_title_2 = "Warning"


class SetPorousMaterialModel(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ui_path = UI_DIR / "model/acoustic/set_porous_material_model.ui"
        ui_path = Path("data/ui_files/model/acoustic/set_porous_material_model.ui")
        uic.loadUi(ui_path, self)

        self.main_window = get_main_window()
        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()
        self.project = self.main_window.project
        self.model = self.project.model
        self.properties = self.model.properties

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.load_info()
        self.exec()

    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set porous material model")

    def _initialize(self):
        self.material_model_data = dict()

    def _load_icons(self):
        icon_path = str(Path("data/icons/logo_vibra.png"))
        self.icon = QIcon(icon_path)

    def _define_qt_variables(self):
        
        # QDoubleSpinBox
        self.doubleSpinBox_C1 : QDoubleSpinBox
        self.doubleSpinBox_C2 : QDoubleSpinBox
        self.doubleSpinBox_C3 : QDoubleSpinBox
        self.doubleSpinBox_C4 : QDoubleSpinBox
        self.doubleSpinBox_C5 : QDoubleSpinBox
        self.doubleSpinBox_C6 : QDoubleSpinBox
        self.doubleSpinBox_C7 : QDoubleSpinBox
        self.doubleSpinBox_C8 : QDoubleSpinBox
        self.doubleSpinBox_flow_resistivity : QDoubleSpinBox

        # QLineEdit
        self.lineEdit_selection_id : QLineEdit

        # QPushButton
        self.pushButton_confirm : QPushButton

        # QPushButton
        self.tabWidget_main : QTabWidget

    def _create_connections(self):
        self.pushButton_confirm.clicked.connect(self.attribute_porous_material_to_selected_bodies)

    def load_info(self):
        pass

    def check_input_volume_id(self, lineEdit, single_ID=False):
        try:

            title = "Invalid entry to the Surface ID"
            message = ""
            tokens = lineEdit.strip().split(",")
            self.volume_ids = self.project.model.mesh.nodes_from_volumes.keys()

            try:
                tokens.remove("")
            except:
                pass

            _size = len(self.volume_ids)
            list_ids = list(map(int, tokens))

            if len(list_ids) == 0:
                message = "An empty input field for the Surface ID has been detected. Please, enter a valid Surface ID to proceed."

            elif len(list_ids) >= 1:
                if single_ID and len(list_ids) > 1:
                    message = "Multiple Selected IDs"
                else:
                    try:
                        for _id in list_ids:
                            if _id not in self.volume_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                                message += f"The input value(s) must be integer(s) number(s) N such that 1 <= N <= {_size}."
                                break
                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                        message += f"The input value(s) must be integer(s) number(s) N such that 1 <= N <= {_size}."
                        message += f"\n\n{str(error_log)}"

        except Exception as log_error:
            message = "Wrong input for the Selected ID's. "
            message += f"\n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([title, message, window_title_1])
            return True, []

        if single_ID:
            return False, list_ids[0]
        else:
            return False, list_ids

    def check_selected_bodies(self):
        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.typed_ids = self.check_input_volume_id(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return True

    def process_Delany_Bazley_model_inputs(self):
        self.material_model_data = {"model" : "Delany-Bazley",
                                    "C1" : self.doubleSpinBox_C1.value(),
                                    "C2" : self.doubleSpinBox_C2.value(),
                                    "C3" : self.doubleSpinBox_C3.value(),
                                    "C4" : self.doubleSpinBox_C4.value(),
                                    "C5" : self.doubleSpinBox_C5.value(),
                                    "C6" : self.doubleSpinBox_C6.value(),
                                    "C7" : self.doubleSpinBox_C7.value(),
                                    "C8" : self.doubleSpinBox_C8.value(),
                                    "flow resistivity" : self.doubleSpinBox_flow_resistivity.value()                              
                                    }

    def process_JCA_model_inptus(self):
        self.material_model_data = {"model" : "JCA"}

    def process_JCAL_model_inptus(self):
        self.material_model_data = {"model" : "JCAL"}

    def attribute_porous_material_to_selected_bodies(self):

        if self.check_selected_bodies():
            return

        index = self.tabWidget_main.currentIndex()
        if index == 0:
            self.process_Delany_Bazley_model_inputs()
        elif index == 1:
            self.process_JCA_model_inptus()
        elif index == 2:
            self.process_JCAL_model_inptus()
        else:
            return
        
        #TODO: set porous material model to selected bodies
        self.project.set_porous_material_model(self.typed_ids, self.material_model_data)
        # print(f"The porous material model has been attributed to volumes: {self.typed_ids}")
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_porous_material_to_selected_bodies()
        elif event.key() == Qt.Key_Escape:
            self.close()