from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QMenu
from molde.render_widgets import CommonRenderWidget

from vibra import ICON_DIR
from vibra.utils.icons import load_icon


class ViewsMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Views")

        self.create_actions()
        self.create_layout()

    def create_actions(self):
        color = QColor("#448cff")
        self.top_view_icon = load_icon(ICON_DIR / "views/top.png", color)
        self.bottom_view_icon = load_icon(ICON_DIR / "views/bottom.png", color)
        self.right_view_icon = load_icon(ICON_DIR / "views/right.png", color)
        self.left_view_icon = load_icon(ICON_DIR / "views/left.png", color)
        self.back_view_icon = load_icon(ICON_DIR / "views/back.png", color)
        self.front_view_icon = load_icon(ICON_DIR / "views/front.png", color)
        self.isometric_view_icon = load_icon(ICON_DIR / "views/orthogonal.png", color)
        self.top_view_action = QAction(self.top_view_icon, "Top View", self)
        self.bottom_view_action = QAction(self.bottom_view_icon, "Bottom View", self)
        self.left_view_action = QAction(self.left_view_icon, "Left View", self)
        self.right_view_action = QAction(self.right_view_icon, "Right View", self)
        self.front_view_action = QAction(self.front_view_icon, "Front View", self)
        self.back_view_action = QAction(self.back_view_icon, "Back View", self)
        self.isometric_view_action = QAction(self.isometric_view_icon, "Isometric View", self)
        self.top_view_action.triggered.connect(self.show_top_view_callback)
        self.bottom_view_action.triggered.connect(self.show_bottom_view_callback)
        self.left_view_action.triggered.connect(self.show_left_view_callback)
        self.right_view_action.triggered.connect(self.show_right_view_callback)
        self.front_view_action.triggered.connect(self.show_front_view_callback)
        self.back_view_action.triggered.connect(self.show_back_view_callback)
        self.isometric_view_action.triggered.connect(self.show_isometric_view_callback)

    def create_layout(self):
        self.addAction(self.top_view_action)
        self.addAction(self.bottom_view_action)
        self.addAction(self.left_view_action)
        self.addAction(self.right_view_action)
        self.addAction(self.front_view_action)
        self.addAction(self.back_view_action)
        self.addAction(self.isometric_view_action)

    def show_top_view_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_top_view()

    def show_bottom_view_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_bottom_view()

    def show_left_view_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_left_view()

    def show_right_view_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_right_view()

    def show_front_view_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_front_view()

    def show_back_view_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_back_view()

    def show_isometric_view_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_isometric_view()
