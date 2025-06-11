from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

from vibra import app, __version__
from vibra.interface.ui_generated.messages.get_user_confirmation_ui import GetUserConfirmation_UI
from vibra.interface.formatters.icons import *


class GetUserConfirmationInput(GetUserConfirmation_UI):
    def __init__(self, title, message, *args, **kwargs):
        super().__init__(*args)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.action_model_workspace_callback()

        self.project = app().project
        self.model = self.project.model
        self.properties = self.model.properties

        self.title = title
        self.message = message
        self.buttons_config = kwargs.get("buttons_config", dict())
        self.window_title = kwargs.get('window_title', f'Vibra v{__version__}')

        self._config_window()
        self._reset_variables()
        self._create_connections()

        self._configure_labels()
        self._configure_buttons()
        self.exec()

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle(self.window_title)

    def _reset_variables(self):
        self._stop = True
        self._continue = False
        self._cancel = True

    def _create_connections(self):
        self.pushButton_rightButton.clicked.connect(self.confirm_action)
        self.pushButton_leftButton.clicked.connect(self.force_to_close)

    def _configure_buttons(self):
        if self.buttons_config:
            if "left_button_label" in self.buttons_config.keys():
                self.pushButton_leftButton.setText(self.buttons_config["left_button_label"])
            if "right_button_label" in self.buttons_config.keys():
                self.pushButton_rightButton.setText(self.buttons_config["right_button_label"])
            if "left_toolTip" in self.buttons_config.keys():
                self.pushButton_leftButton.setToolTip(self.buttons_config["left_toolTip"])
            if "right_toolTip" in self.buttons_config.keys():
                self.pushButton_rightButton.setToolTip(self.buttons_config["right_toolTip"])
            if "left_button_size" in self.buttons_config.keys():
                self.pushButton_leftButton.setFixedWidth(self.buttons_config["left_button_size"])
            if "right_button_size" in self.buttons_config.keys():
                self.pushButton_rightButton.setFixedWidth(self.buttons_config["right_button_size"])

    def _configure_labels(self):
        self.label_title.setText(self.title)
        self.label_message.setText(self.message)
        self.label_message.setWordWrap(True)
        self.label_message.setAlignment(Qt.AlignJustify)
        self.label_message.setAlignment(Qt.AlignCenter)
        self.label_message.setMargin(12)
        self.label_message.adjustSize()
        self.adjustSize()

    def confirm_action(self):
        self._cancel = False
        self._continue = True
        self._stop = False
        self.close()

    def force_to_close(self):
        self._cancel = False
        self._continue = False
        self._stop = True
        self.close()