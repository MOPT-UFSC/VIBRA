from PySide6.QtCore import Qt

from vibra import app, __version__
from vibra.interface.ui_generated.general.choose_property_to_delete_ui import ChoosePropertyToDelete_UI


class ChoosePropertytoDelete(ChoosePropertyToDelete_UI):
    def __init__(self, title, message, options, *args, **kwargs):
        super().__init__(*args)

        self.title = title
        self.message = message
        self.buttons_config = kwargs.get("buttons_config", dict())
        self.window_title = kwargs.get('window_title', f'Vibra v{__version__}')
        
        self.property_comboBox.addItems(options)
        self.confirm_pushButton.setDefault(True)

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
        self.cancel_pushButton.clicked.connect(self.cancel_action)
        self.remove_all_pushButton.clicked.connect(self.remove_all_action)
        self.confirm_pushButton.clicked.connect(self.confirm_action)
    
    def _reset_variables(self):
        self._confirm = False
        self._remove_all = False
        self._cancel = True
        self._property_to_delete = None

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
            if "middle_button_label" in self.buttons_config.keys():
                self.remove_all_pushButton.setText(self.buttons_config["middle_button_label"])
            if "right_button_label" in self.buttons_config.keys():
                self.confirm_pushButton.setText(self.buttons_config["right_button_label"])
            
            if "left_toolTip" in self.buttons_config.keys():
                self.cancel_pushButton.setToolTip(self.buttons_config["left_toolTip"])
            if "middle_toolTip" in self.buttons_config.keys():
                self.remove_all_pushButton.setToolTip(self.buttons_config["middle_toolTip"])
            if "right_toolTip" in self.buttons_config.keys():
                self.confirm_pushButton.setToolTip(self.buttons_config["right_toolTip"])
            
            if "left_button_size" in self.buttons_config.keys():
                self.cancel_pushButton.setFixedWidth(self.buttons_config["left_button_size"])
            if "middle_button_size" in self.buttons_config.keys():
                self.remove_all_pushButton.setFixedWidth(self.buttons_config["middle_button_size"])
            if "right_button_size" in self.buttons_config.keys():
                self.confirm_pushButton.setFixedWidth(self.buttons_config["right_button_size"])

    def confirm_action(self):
        self._confirm = True
        self._remove_all = False
        self._cancel = False
        self._property_to_delete = self.property_comboBox.currentText()
        self.close()
    
    def remove_all_action(self):
        self._confirm = False
        self._remove_all = True
        self._cancel = False
        self._property_to_delete = None
        self.close()
    
    def cancel_action(self):
        self._confirm = False
        self._remove_all = False
        self._cancel = True
        self._property_to_delete = None
        self.close()
