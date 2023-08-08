from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QToolBar

from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget
from vibra.utils.icons import load_icon


class RendererToolbar(QToolBar):
    def __init__(self, parent, viewer_tabs):
        super().__init__(parent)

        self.viewer_tabs = viewer_tabs

        self.create_actions()
        self.configure_layout()
        self.configure_appearance()

    def configure_appearance(self):
        self.setMovable(True)
        self.setFloatable(True)
        self.setStyleSheet(
            """
            QToolBar {
                border-style: solid;
                border-width: 1px;
                border-color: #888888;
                border-radius: 3px
            }
            """
        )

    def create_actions(self):
        color = QColor("#448cff")

        #
        top_view_icon = load_icon(Path("data/icons/top.png"), color)
        self.top_view_action = QAction(top_view_icon, "Top View", self)
        self.top_view_action.triggered.connect(self.top_view_callback)
        self.top_view_action.setShortcut("Ctrl+Shift+1")

        bottom_icon = load_icon(Path("data/icons/bottom.png"), color)
        self.bottom_view_action = QAction(bottom_icon, "Bottom View", self)
        self.bottom_view_action.triggered.connect(self.bottom_view_callback)
        self.bottom_view_action.setShortcut("Ctrl+Shift+2")

        right_view_icon = load_icon(Path("data/icons/right.png"), color)
        self.right_view_action = QAction(right_view_icon, "Right View", self)
        self.right_view_action.triggered.connect(self.right_view_callback)
        self.right_view_action.setShortcut("Ctrl+Shift+4")

        left_view_icon = load_icon(Path("data/icons/left.png"), color)
        self.left_view_action = QAction(left_view_icon, "Left View", self)
        self.left_view_action.triggered.connect(self.left_view_callback)
        self.left_view_action.setShortcut("Ctrl+Shift+3")

        back_view_icon = load_icon(Path("data/icons/back.png"), color)
        self.back_view_action = QAction(back_view_icon, "Back View", self)
        self.back_view_action.triggered.connect(self.back_view_callback)
        self.back_view_action.setShortcut("Ctrl+Shift+6")

        front_view_icon = load_icon(Path("data/icons/front.png"), color)
        self.front_view_action = QAction(front_view_icon, "Front View", self)
        self.front_view_action.triggered.connect(self.front_view_callback)
        self.front_view_action.setShortcut("Ctrl+Shift+5")

        view_orthogonal_icon = load_icon(Path("data/icons/orthogonal.png"), color)
        self.isometric_view_action = QAction(view_orthogonal_icon, "Isometric View", self)
        self.isometric_view_action.triggered.connect(self.isometric_view_callback)
        self.isometric_view_action.setShortcut("Ctrl+Shift+7")

        #
        show_points_icon = load_icon(Path("data/icons/nodes.png"), color)
        self.show_points_action = QAction(show_points_icon, "Node View", self)
        self.show_points_action.triggered.connect(self.show_points_callback)

        show_lines_icon = load_icon(Path("data/icons/lines.png"), color)
        self.show_lines_action = QAction(show_lines_icon, "Line View", self)
        self.show_lines_action.triggered.connect(self.show_lines_callback)

        show_faces_icon = load_icon(Path("data/icons/faces.png"), color)
        self.show_faces_action = QAction(show_faces_icon, "Face View", self)
        self.show_faces_action.triggered.connect(self.show_faces_callback)

        clip_plane_icon = load_icon(Path("data/icons/tube_cut.png"), color)
        self.clip_plane_action = QAction(clip_plane_icon, "Clip Plane", self)
        self.clip_plane_action.triggered.connect(self.clip_plane_callback)

    def configure_layout(self):
        self.addSeparator()
        self.addAction(self.top_view_action)
        self.addAction(self.bottom_view_action)
        self.addAction(self.right_view_action)
        self.addAction(self.left_view_action)
        self.addAction(self.front_view_action)
        self.addAction(self.back_view_action)
        self.addAction(self.isometric_view_action)
        self.addSeparator()
        self.addAction(self.show_lines_action)
        self.addAction(self.show_points_action)
        self.addAction(self.show_faces_action)
        self.addSeparator()
        self.addAction(self.clip_plane_action)

    # Callbacks
    def top_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_top_view()

    def bottom_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_bottom_view()

    def left_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_left_view()

    def right_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_right_view()

    def front_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_front_view()

    def back_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_back_view()

    def isometric_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_isometric_view()

    def show_points_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_points()

    def show_lines_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_lines()

    def show_faces_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_faces()

    def clip_plane_callback(self):
        self.parent().clip_plane.show()
        self.parent().slider_moved_callback()
        self.parent().slider_released_callback()
