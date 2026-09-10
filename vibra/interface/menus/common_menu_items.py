from pathlib import Path

from molde import Color
from molde.colors import color_names
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from vibra import ICON_DIR
from vibra.interface.menus.border_item_delegate import BorderItemDelegate
from vibra.interface.menus.tool_tip import ToolTip


class CommonMenuItems(QTreeWidget):
    """Common Menu Items

    This class simplifies the creation of menu items.

    """

    def __init__(self, selectable: bool = False):
        super().__init__()

        self._last_top_level = None
        self._callback_list = dict()
        self._last_item = None
        self._selectable = selectable

        self._config_tree()

    def add_top_item(self, name, icon=None, expanded=True):
        item = TopTreeWidgetItem(name)
        self._last_top_level = item
        self.addTopLevelItem(item)
        item.setExpanded(expanded)
        self.setUniformRowHeights(False)
        return item

    def add_item(self, name, callback=None):
        if self._last_top_level is None:
            self.add_top_item("")

        item = ChildTreeWidgetItem(name)
        self._last_top_level.addChild(item)
        item.setFont(0, self.font_item)

        if callable(callback):
            item.clicked.connect(callback)

        return item

    def clear_last_item(self):
        self._last_item = None
        item = self.currentItem()
        if item is not None:
            item.setSelected(False)

    def _config_tree(self):

        self.font_item = QFont()
        self.font_item.setPointSize(10)

        self.setHeaderHidden(True)
        self.setTabKeyNavigation(True)
        self.setRootIsDecorated(True)
        delegate = BorderItemDelegate(self, Qt.UserRole + 1)
        self.setItemDelegate(delegate)
        self.itemClicked.connect(self.item_clicked_callback)

    def item_clicked_callback(self, item: "ChildTreeWidgetItem", _):
        if item.isDisabled():
            return

        if not self._selectable:
            item.setSelected(False)

        elif item == self._last_item:
            return

        if not hasattr(item, "clicked"):
            return

        self._last_item = item
        item.clicked.emit()


# It is usually bad to have multiple classes in the same file
# but I will do it anyway >=)


class CustomBoundSignal:
    """
    Copies the funcionality of pyqtBoundSignal and is meant
    to be used in objects that are not instances of QObjects.
    """

    def __init__(self) -> None:
        self.callbacks = set()

    def connect(self, function):
        self.callbacks.add(function)

    def disconnect(self, function):
        self.callbacks.remove(function)

    def emit(self, *args, **kwargs):
        for function in self.callbacks:
            if callable(function):
                function(*args, **kwargs)


class TopTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, name):
        super().__init__([name])
        self.clicked = CustomBoundSignal()
        self._configure_appearance()

    def toggle_expansion(self):
        self.setExpanded(not self.isExpanded())

    def _configure_appearance(self):

        font = QFont()
        font.setBold(True)
        font.setWeight(QFont.Weight(60))
        font.setPointSize(10)
        self.setFont(0, font)
        self.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)
        self.setFlags(Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

    def set_warning(self, warning: bool):
        if warning:
            font = QFont()
            font.setBold(True)
            self.setFont(0, font)
            self.setForeground(0, Color(*color_names.RED_5.to_rgb()).to_qt())
            warning_icon = QIcon(str(ICON_DIR / "model_setup_items/warning_yellow.png"))
            self.setIcon(0, warning_icon)

        else:
            # Resets data to default
            self.setData(0, Qt.FontRole, None)  # reset color
            self.setData(0, Qt.ForegroundRole, None)  # reset color
            self.setData(0, Qt.DecorationRole, None)


class ChildTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, name):
        super().__init__([name])
        self.clicked = CustomBoundSignal()
        self.tool_tips = ToolTip()
        self.property_name = ""
        self.should_paint = False

    def set_property_name(self, name: str):
        name = name.lower()
        name = name.strip()
        self.property_name = name

    def set_warning(self, cond: bool, update_item_color: bool = True):
        if cond:
            if update_item_color:
                font = QFont()
                font.setBold(True)
                self.setFont(0, font)
                self.setForeground(0, Color(*color_names.YELLOW.to_rgb()).to_qt())

            warning_icon = QIcon(str(Path(ICON_DIR / "model_setup_items/warning_yellow.png")))
            self.setIcon(0, warning_icon)

        else:
            # Resets data to default
            self.setData(0, Qt.FontRole, None)  # reset color
            self.setData(0, Qt.ForegroundRole, None)  # reset color
            self.setData(0, Qt.DecorationRole, None)

    def set_error(self, cond: bool):
        if cond:
            font = QFont()
            font.setBold(True)
            self.setFont(0, font)
            self.setForeground(0, Color(*color_names.RED.to_rgb()).to_qt())
            # TODO: change the icon
            error_icon = QIcon(str(Path(ICON_DIR / "model_setup_items/error_red.png")))
            self.setIcon(0, error_icon)
        else:
            # Resets data to default
            self.setData(0, Qt.FontRole, None)  # reset color
            self.setData(0, Qt.ForegroundRole, None)  # reset color
            self.setData(0, Qt.DecorationRole, None)

    def set_icon(self, file_name: str = "", visible: bool = True):
        # to set an alternative icon
        file_name = file_name if file_name != "" else self.property_name

        if visible:
            path_image = str(Path(ICON_DIR / "model_setup_items" / str(file_name + ".png")))
            self.setIcon(0, QIcon(path_image))
        else:
            self.setIcon(0, QIcon())

    def set_tool_tip(self, property_name: str = "", requirement: bool = False, message_requirement: str = ""):
        if requirement and message_requirement == "":
            message_requirement = "<b style='color:red'>Required for the selected configuration.</b>"

        tool_tip = self.tool_tips.get_tooltip_QTextEdit(property_name)
        if tool_tip is not None:
            self.setToolTip(0, message_requirement + tool_tip.toHtml())
