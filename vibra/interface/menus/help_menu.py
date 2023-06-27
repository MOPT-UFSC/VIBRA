from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QMenu

from vibra.utils.icons import load_icon


class HelpMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)

        self.setTitle("Help")
        self.create_actions()
        self.create_layout()

    def create_actions(self):
        color = QColor("#0055DD")
        help_icon = load_icon(Path("data/icons/help.png"), color)
        self.help_action = QAction(help_icon, "About Vibra", self)
        self.help_action.triggered.connect(self.help_callback)

    def create_layout(self):
        self.addAction(self.help_action)

    #
    def help_callback(self):
        self.parent().viewer_tabs.show_help()
