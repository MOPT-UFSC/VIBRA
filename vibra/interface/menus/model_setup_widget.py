from PySide6.QtGui import QAction, QIcon, Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QMenu, QTreeWidgetItem, QWidget

from vibra import ICON_DIR, app
from vibra.interface.formatters.icons import change_icon_color_for_widgets
from vibra.interface.general.choose_property_to_delete import ChoosePropertyToDelete
from vibra.interface.menus.model_setup_items import ModelSetupItems, ChildTreeWidgetItem


class ModelSetupWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._config_widget()
        self._create_connections()

    def _config_widget(self):
        self.main_frame = QFrame()
        self.model_setup_items = ModelSetupItems()

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.main_frame.setLayout(self.grid_layout)
        self.grid_layout.addWidget(self.model_setup_items, 0, 0)

        self.setLayout(self.grid_layout)
        self.adjustSize()

        self.model_setup_items.setContextMenuPolicy(Qt.CustomContextMenu)
        self.model_setup_items.setToolTip("Right-click to add or delete a property")

    def _create_connections(self):
        self.model_setup_items.customContextMenuRequested.connect(self.show_context_menu)
    
    def get_item(self):
        return self.model_setup_items

    def show_context_menu(self, pos):
        item = self.model_setup_items.itemAt(pos)
        if not item:
            return

        menu = QMenu(app().main_window)
        add_icon = str(ICON_DIR / "add_narrow.png")
        remove_icon = str(ICON_DIR / "remove.png")

        action_add = QAction("Add a property", self)
        action_add.setIcon(QIcon(add_icon))

        action_remove_all = QAction("Remove a property", self)
        action_remove_all.setIcon(QIcon(remove_icon))

        action_remove_selected = QAction("Remove selected property", self)
        action_remove_selected.setIcon(QIcon(remove_icon))

        menu.addAction(action_add)
        menu.addAction(action_remove_all)
        menu.addAction(action_remove_selected)

        change_icon_color_for_widgets(menu.actions(), app().main_window.icon_color)

        action_add.triggered.connect(lambda: self.add_property_callback(item))
        action_remove_all.triggered.connect(lambda: self.remove_property_all_callback(item))
        action_remove_selected.triggered.connect(lambda: self.remove_selected_property_callback(item))

        menu.exec_(self.model_setup_items.viewport().mapToGlobal(pos))

    def add_property_callback(self, item: QTreeWidgetItem):
        pass

    def remove_property_all_callback(self, item: QTreeWidgetItem):
        if item is None:
            return

        app().main_window.close_dialogs()
        ChoosePropertyToDelete(all_properties=True)

    def remove_selected_property_callback(self, item: QTreeWidgetItem):        
        if not isinstance(item, ChildTreeWidgetItem):
            return

        property_to_filter = item.property_name

        app().main_window.close_dialogs()
        ChoosePropertyToDelete(property_to_filter=property_to_filter)