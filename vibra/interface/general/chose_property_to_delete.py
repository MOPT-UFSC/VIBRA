from PySide6.QtCore import Qt

from vibra import app, __version__
from vibra.interface.ui_generated.general.chose_propertyto_delete_ui import ChosePropertytoDelete_UI


class ChosePropertytoDelete(ChosePropertytoDelete_UI):
    def __init__(self, title, message, options, *args, **kwargs):
        super().__init__(*args)

        self.title = title
        self.message = message
        self.buttons_config = kwargs.get("buttons_config", dict())
        self.window_title = kwargs.get('window_title', f'Vibra v{__version__}')
        
        self.property_comboBox.addItems(options)

        self._config_window()
        self._configure_labels()
        self._create_connections()
        self._reset_variables()
        self._configure_buttons()
        self.exec()

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle(self.window_title)
    
    def _create_connections(self):
        self.confirm_pushButton.clicked.connect(self.confirm_action)
    
    def _reset_variables(self):
        self._confirm = False
        self._cancel = True

    def _configure_labels(self):
        self.message_label.setText(self.message)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignJustify)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setMargin(12)
        self.message_label.adjustSize()
        self.adjustSize()
    
    def _configure_buttons(self):
        if self.buttons_config:
            if "left_button_label" in self.buttons_config.keys():
                self.cancel_pushButton.setText(self.buttons_config["left_button_label"])
            if "right_button_label" in self.buttons_config.keys():
                self.confirm_pushButton.setText(self.buttons_config["right_button_label"])
            if "left_toolTip" in self.buttons_config.keys():
                self.cancel_pushButton.setToolTip(self.buttons_config["left_toolTip"])
            if "right_toolTip" in self.buttons_config.keys():
                self.confirm_pushButton.setToolTip(self.buttons_config["right_toolTip"])
            if "left_button_size" in self.buttons_config.keys():
                self.cancel_pushButton.setFixedWidth(self.buttons_config["left_button_size"])
            if "right_button_size" in self.buttons_config.keys():
                self.confirm_pushButton.setFixedWidth(self.buttons_config["right_button_size"])

    def confirm_action(self):
        self._confirm = True
        self._stop = False
        self._property_to_delete = self.property_comboBox.currentText()
        self.close()
    
