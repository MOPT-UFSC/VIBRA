from enum import Enum, auto

from PySide6.QtCore import QObject, Signal


class ViewAction(Enum):
    VIEW_FIT = auto()
    VIEW_TOP = auto()
    VIEW_BOTTOM = auto()
    VIEW_FRONT = auto()
    VIEW_BACK = auto()
    VIEW_LEFT = auto()
    VIEW_RIGHT = auto()
    VIEW_ISO = auto()


class ViewService(QObject):
    on_view_change = Signal()
    on_view_action = Signal(str)

    def __init__(self):
        super().__init__()
        self.transparency = False

    def viewChanged(self):
        self.on_view_change.emit()

    def setViewAction(self, value: str):
        self.on_view_action.emit(value)

    def setTransparency(self, value: bool):
        self.transparency = value
        self.viewChanged()
