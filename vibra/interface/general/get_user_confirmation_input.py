from PySide6.QtCore import Qt

from vibra import VERSION, app
from vibra.interface.ui_generated.messages.get_user_confirmation_ui import GetUserConfirmation_UI


class GetUserConfirmationInput(GetUserConfirmation_UI):
    def __init__(self, title, message, *args, **kwargs):
        super().__init__(*args)

        app().main_window.set_input_widget(self)

        self.model = app().project.model
        self.properties = self.model.properties

        self.title = title
        self.message = message
        self.buttons_config = kwargs.get("buttons_config", {})
        self.window_title = kwargs.get('window_title', f'Vibra v{VERSION}')

        self._config_window()
        self._reset_variables()
        self._create_connections()

        self._configure_labels()
        self._configure_buttons()

        app().main_window.hide_dialogs()
        self.exec()

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle(self.window_title)

    def _reset_variables(self):
        self._continue = False
        self._cancel = True

    def _create_connections(self):
        self.pushButton_rightButton.clicked.connect(self.confirm_action)
        self.pushButton_leftButton.clicked.connect(self.force_to_close)

    def _configure_buttons(self):
        if not self.buttons_config:
            return

        if "left_button_label" in self.buttons_config:
            self.pushButton_leftButton.setText(self.buttons_config["left_button_label"])
        if "right_button_label" in self.buttons_config:
            self.pushButton_rightButton.setText(self.buttons_config["right_button_label"])
            self.pushButton_rightButton.setAutoDefault(True)
        if "left_toolTip" in self.buttons_config:
            self.pushButton_leftButton.setToolTip(self.buttons_config["left_toolTip"])
        if "right_toolTip" in self.buttons_config:
            self.pushButton_rightButton.setToolTip(self.buttons_config["right_toolTip"])
        if "left_button_size" in self.buttons_config:
            self.pushButton_leftButton.setFixedWidth(self.buttons_config["left_button_size"])
        if "right_button_size" in self.buttons_config:
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
        self.close()

    def force_to_close(self):
        self._cancel = True
        self._continue = False
        self.close()
