from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QMenu

from vibra.interface.loading_bar import load_function
from vibra.utils.icons import load_icon


class SettingsMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)

        self.main_window = self.parent()
        self.setTitle("Settings")
        self.create_and_connect_actions()
        self.create_layout()
        self.bool_state = True


    def create_and_connect_actions(self):
        color = QColor("#0055DD")
        #
        self.new_project_icon = load_icon(Path("data/icons/new_file.png"), color)
        #
        self.show_or_hide_menu_items_action = QAction(self.new_project_icon, "Hide menu items", self)
        # self.hide_menu_items_action = QAction(self.new_project_icon, "Hide menu items", self)
        self.show_or_hide_menu_items_action.triggered.connect(self.call_show_or_hide_menu_items)
        # self.hide_menu_items_action.triggered.connect(self.call_hide_menu_items)


    def create_layout(self):
        self.clear()
        self.addAction(self.show_or_hide_menu_items_action)
        # self.addAction(self.hide_menu_items_action)


    def call_show_or_hide_menu_items(self):
        if self.bool_state:
            text = "Show menu items"
        else:
            text = "Hide menu items"
        self.show_or_hide_menu_items_action.setText(text)        
        self.bool_state = not self.bool_state
        self.main_window.menu_widget.setVisible(self.bool_state)


    # def call_hide_menu_items(self):
    #     self.main_window.menu_widget.setVisible(False)
