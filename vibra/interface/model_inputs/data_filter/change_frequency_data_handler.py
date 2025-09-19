from PySide6.QtWidgets import QDialog, QDoubleSpinBox, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.ui_generated.model.setup.data_filter.change_frequency_data_range_input_ui import ChangeFrequencyDataRangeInput_UI
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

import os
import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class ChangeFrequencyDataRangeInput(ChangeFrequencyDataRangeInput_UI):
    def __init__(self, imported_values, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.action_model_workspace_callback()

        # self.project = app().project
        # self.model = app().project.model
        # self.mesh = app().project.model.mesh
        # self.properties = app().project.model.properties

        self.imported_values = imported_values

        self._config_window()
        self._initialize()
        self._configure_qt_variables()
        self._create_connections()

        self.load_freq_setup()
        
        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.filter_data = None
        self.keep_window_open = True

    def _configure_qt_variables(self):
        self.doubleSpinBox_freq_step.setDisabled(True)

    def _create_connections(self):
        self.pushButton_confirm.clicked.connect(self.confirm_frequency_range)

    def load_freq_setup(self):

        if self.imported_values is None:
            self.close()
            return

        frequencies = self.imported_values[:, 0]
        f_min = frequencies[0]
        f_max = frequencies[-1]
        f_step = frequencies[1] - frequencies[0]

        self.doubleSpinBox_freq_min.setValue(f_min)
        self.doubleSpinBox_freq_max.setValue(f_max)
        self.doubleSpinBox_freq_step.setValue(f_step)

        self.doubleSpinBox_freq_min.setSingleStep(f_step)
        self.doubleSpinBox_freq_max.setSingleStep(f_step)

    def confirm_frequency_range(self):

        if isinstance(self.imported_values, np.ndarray):

            frequencies = self.imported_values[:, 0]
            f_min = self.doubleSpinBox_freq_min.value()
            f_max = self.doubleSpinBox_freq_max.value()

            mask_min = frequencies >= f_min
            mask_max = frequencies <= f_max
            mask = mask_min * mask_max

            self.filter_data = self.imported_values[mask, :]

        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_frequency_range()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            return

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)