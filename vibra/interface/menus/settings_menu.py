from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QMenu

from vibra.utils.icons import load_icon
from vibra.utils.interface_functions import get_main_window


class VisibilitySettingsMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)

        self.main_window = get_main_window()
        self.setTitle("Visibility settings")
        self.create_and_connect_actions()
        self.create_layout()
        self.bool_state = True
        self.load_user_preference_state()

    def create_and_connect_actions(self):
        color = QColor("#448cff")
        #
        self.new_project_icon = load_icon(Path("data/icons/new_file.png"), color)
        self.theme_sun_icon = load_icon(Path("data/icons/sun_icon.png"), color)
        self.theme_moon_icon = load_icon(Path("data/icons/moon_icon.png"), color)
        #
        self.show_or_hide_menu_items_action = QAction(self.new_project_icon, "Hide menu items", self)
        self.theme_action = QAction(self.theme_sun_icon, "Theme", self)
        #
        self.show_or_hide_menu_items_action.triggered.connect(self.call_show_or_hide_menu_items)
        self.theme_action.triggered.connect(self.theme_callback)

    def create_layout(self):
        self.clear()
        self.addAction(self.show_or_hide_menu_items_action)
        self.addAction(self.theme_action)
        # self.addAction(self.hide_menu_items_action)

    def call_show_or_hide_menu_items(self):
        if self.bool_state:
            text = "Show menu items"
        else:
            text = "Hide menu items"

        self.main_window.set_menu_items_visibility_state(self.bool_state)
        self.show_or_hide_menu_items_action.setText(text)
        self.bool_state = not self.bool_state
        self.main_window.menu_widget.setVisible(self.bool_state)
        self.main_window.vertical_line.setVisible(self.bool_state)
        self.main_window.analysis_filter.setVisible(self.bool_state)

    def theme_callback(self):
        if self.parent().user_config.theme == "light":
            self.parent().set_theme("dark")
            self.theme_action.setIcon(self.theme_sun_icon)

        elif self.parent().user_config.theme == "dark":
            self.parent().set_theme("light")
            self.theme_action.setIcon(self.theme_moon_icon)

    def load_user_preference_state(self):
        self.bool_state = self.main_window.user_config.menu_items_visible
        self.call_show_or_hide_menu_items()
