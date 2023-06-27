from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QMenu

from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget
from vibra.utils.icons import load_icon


class ViewsMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Views")

        self.create_actions()
        self.create_layout()

    def create_actions(self):
        color = QColor("#0055DD")
        self.view_up_icon = load_icon(Path("data/icons/top.png"), color)
        self.view_down_icon = load_icon(Path("data/icons/bottom.png"), color)
        self.view_right_icon = load_icon(Path("data/icons/right.png"), color)
        self.view_left_icon = load_icon(Path("data/icons/left.png"), color)
        self.view_back_icon = load_icon(Path("data/icons/back.png"), color)
        self.view_front_icon = load_icon(Path("data/icons/front.png"), color)
        self.view_orthogonal_icon = load_icon(Path("data/icons/orthogonal.png"), color)
        self.view_up_action = QAction(self.view_up_icon, "Up View", self)
        self.view_down_action = QAction(self.view_down_icon, "Down View", self)
        self.view_left_action = QAction(self.view_left_icon, "Left View", self)
        self.view_right_action = QAction(self.view_right_icon, "Right View", self)
        self.view_front_action = QAction(self.view_front_icon, "Front View", self)
        self.view_back_action = QAction(self.view_back_icon, "Back View", self)
        self.view_orthogonal_action = QAction(self.view_orthogonal_icon, "Orthogonal View", self)
        self.view_up_action.triggered.connect(self.show_view_up_callback)
        self.view_down_action.triggered.connect(self.show_view_down_callback)
        self.view_left_action.triggered.connect(self.show_view_left_callback)
        self.view_right_action.triggered.connect(self.show_view_right_callback)
        self.view_front_action.triggered.connect(self.show_view_front_callback)
        self.view_back_action.triggered.connect(self.show_view_back_callback)
        self.view_orthogonal_action.triggered.connect(self.show_view_orthogonal_callback)

    def create_layout(self):
        self.addAction(self.view_up_action)
        self.addAction(self.view_down_action)
        self.addAction(self.view_left_action)
        self.addAction(self.view_right_action)
        self.addAction(self.view_front_action)
        self.addAction(self.view_back_action)
        self.addAction(self.view_orthogonal_action)

    def show_view_up_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_view_up()

    def show_view_down_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_view_down()

    def show_view_left_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_view_left()

    def show_view_right_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_view_right()

    def show_view_front_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_view_front()

    def show_view_back_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_view_back()

    def show_view_orthogonal_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_view_orthogonal()
