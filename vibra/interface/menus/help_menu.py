from pathlib import Path

from PySide6.QtGui import QColor, QAction
from PySide6.QtWidgets import QMenu

from vibra import ICON_DIR
from vibra.utils.icons import load_icon


class HelpMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)

        self.setTitle("Help")
        self.create_actions()
        self.create_layout()

    def create_actions(self):
        color = QColor("#448cff")
        help_icon = load_icon(ICON_DIR / "help.png", color)
        self.help_action = QAction(help_icon, "About Vibra", self)
        self.help_action.triggered.connect(self.help_callback)

    def create_layout(self):
        self.addAction(self.help_action)

    #
    def help_callback(self):
        self.parent().viewer_tabs.show_help()
