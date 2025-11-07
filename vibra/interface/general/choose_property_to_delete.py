from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem, QTreeWidgetItem

from vibra import app, __version__
from vibra.interface.ui_generated.general.choose_property_to_delete_ui import ChoosePropertyToDelete_UI


class ChoosePropertytoDelete(ChoosePropertyToDelete_UI):
    def __init__(self, title, message, options, *args, **kwargs):
        super().__init__(*args)

        self.title = title
        self.message = message
        self.options = options
        self.buttons_config = kwargs.get("buttons_config", dict())
        self.window_title = kwargs.get('window_title', f'Vibra v{__version__}')

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
        self.setWindowTitle(self.title)
    
    def _create_connections(self):
        ...
        # self.cancel_pushButton.clicked.connect(self.cancel_action)
        # self.confirm_pushButton.clicked.connect(self.confirm_action)
    
    def _reset_variables(self):
        self._remove = False
        self._cancel = True
        self._property_to_delete = None

    def _configure_labels(self):
        self.label_title.setText("Remove Property")
        self.label_title.setWordWrap(True)
        self.label_title.setAlignment(Qt.AlignJustify)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setMargin(12)
        self.label_title.adjustSize()
        self.adjustSize()
    
    def _configure_buttons(self):
        return
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

    def _fill_list_widget(self):
        return
        for prop in self.options:
            item = QListWidgetItem(prop)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)

    def confirm_action(self):
        self._remove = True
        self._cancel = False
        self.close()
    
    def cancel_action(self):
        self._remove = False
        self._cancel = True
        self._property_to_delete = None
        self.close()
