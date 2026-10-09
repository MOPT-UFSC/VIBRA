from vibra.interface.ui_generated.general.shortcuts_help_ui import ShortcutsHelp_UI
from vibra.interface.shortcuts import SHORTCUTS
from PySide6.QtWidgets import QTableWidgetItem



class ShortcutsHelp(ShortcutsHelp_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Keyboard Shortcuts")
        self.setup_shortcuts_table()
        self.exec()

    def setup_shortcuts_table(self):
        table = self.tableWidget_shortcuts
        table.setRowCount(len(SHORTCUTS))

        for row, (keys, (target, description)) in enumerate(SHORTCUTS.items()):
            table.setItem(row, 0, QTableWidgetItem(keys))
            table.setItem(row, 1, QTableWidgetItem(description))

        table.resizeColumnsToContents()
