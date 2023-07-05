from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QMenu

from vibra.utils.icons import load_icon
from vibra.utils.interface_functions import get_main_window


class SettingsMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)

        self.main_window = get_main_window()
        self.setTitle("Settings")
        self.create_and_connect_actions()
        self.create_layout()
        self.bool_state = True
        self.load_user_preference_state()

    def create_and_connect_actions(self):
        color = QColor("#0055DD")
        #
        self.new_project_icon = load_icon(Path("data/icons/new_file.png"), color)
        #
        self.show_or_hide_menu_items_action = QAction(
            self.new_project_icon, "Hide menu items", self
        )
        #
        self.show_or_hide_menu_items_action.triggered.connect(self.call_show_or_hide_menu_items)

    def create_layout(self):
        self.clear()
        self.addAction(self.show_or_hide_menu_items_action)
        # self.addAction(self.hide_menu_items_action)

    def call_show_or_hide_menu_items(self):
        if self.bool_state:
            text = "Show menu items"
            self.main_window.set_menu_items_visibility_state("0")
        else:
            text = "Hide menu items"
            self.main_window.set_menu_items_visibility_state("1")

        self.show_or_hide_menu_items_action.setText(text)
        self.bool_state = not self.bool_state
        self.main_window.menu_widget.setVisible(self.bool_state)

    def load_user_preference_state(self):
        if self.main_window.user_config.menu_items_visible == "0":
            self.bool_state = True
        elif self.main_window.user_config.menu_items_visible == "1":
            self.bool_state = False
        self.call_show_or_hide_menu_items()
