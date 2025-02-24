from pathlib import Path

from PySide6.QtGui import QColor, QAction
from PySide6.QtWidgets import QMenu
from molde.render_widgets import CommonRenderWidget

from vibra import ICON_DIR
from vibra.utils.icons import load_icon


class ViewModeMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("View mode")

        self.create_actions()
        self.create_layout()

    def create_actions(self):
        color = QColor("#448cff")
        self.view_mode_line_icon = load_icon(ICON_DIR / "visibility/lines.png", color)
        self.view_mode_nodes_icon = load_icon(ICON_DIR / "visibility/nodes.png", color)
        self.view_mode_face_icon = load_icon(ICON_DIR / "visibility/faces.png", color)
        self.view_mode_face_action = QAction(self.view_mode_face_icon, "Face View", self)
        self.view_mode_line_action = QAction(self.view_mode_line_icon, "Line View", self)
        self.view_mode_nodes_action = QAction(self.view_mode_nodes_icon, "Node View", self)
        self.view_mode_face_action.triggered.connect(self.show_faces_callback)
        self.view_mode_line_action.triggered.connect(self.show_edges_callback)
        self.view_mode_nodes_action.triggered.connect(self.show_points_callback)

    def create_layout(self):
        self.addAction(self.view_mode_face_action)
        self.addAction(self.view_mode_line_action)
        self.addAction(self.view_mode_nodes_action)

    #
    def show_points_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_points()

    def show_edges_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_lines()

    def show_faces_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_faces()
