from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QToolBar

from vibra.interface.viewer_3d.vtk_widget import VTKWidget
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
        color = QColor("#0055DD")

        #
        view_up_icon = load_icon(Path("data/icons/top.png"), color)
        self.view_up_action = QAction(view_up_icon, "Up View", self)
        self.view_up_action.triggered.connect(self.view_up_callback)
        self.view_up_action.setShortcut("Ctrl+Shift+1")

        view_down_icon = load_icon(Path("data/icons/bottom.png"), color)
        self.view_down_action = QAction(view_down_icon, "Down View", self)
        self.view_down_action.triggered.connect(self.view_down_callback)
        self.view_down_action.setShortcut("Ctrl+Shift+2")

        view_right_icon = load_icon(Path("data/icons/right.png"), color)
        self.view_right_action = QAction(view_right_icon, "Right View", self)
        self.view_right_action.triggered.connect(self.view_right_callback)
        self.view_right_action.setShortcut("Ctrl+Shift+4")

        view_left_icon = load_icon(Path("data/icons/left.png"), color)
        self.view_left_action = QAction(view_left_icon, "Left View", self)
        self.view_left_action.triggered.connect(self.view_left_callback)
        self.view_left_action.setShortcut("Ctrl+Shift+3")

        view_back_icon = load_icon(Path("data/icons/back.png"), color)
        self.view_back_action = QAction(view_back_icon, "Back View", self)
        self.view_back_action.triggered.connect(self.view_back_callback)
        self.view_back_action.setShortcut("Ctrl+Shift+6")

        view_front_icon = load_icon(Path("data/icons/front.png"), color)
        self.view_front_action = QAction(view_front_icon, "Front View", self)
        self.view_front_action.triggered.connect(self.view_front_callback)
        self.view_front_action.setShortcut("Ctrl+Shift+5")

        view_orthogonal_icon = load_icon(Path("data/icons/orthogonal.png"), color)
        self.view_orthogonal_action = QAction(view_orthogonal_icon, "Orthogonal View", self)
        self.view_orthogonal_action.triggered.connect(self.view_orthogonal_callback)
        self.view_orthogonal_action.setShortcut("Ctrl+Shift+7")

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
        self.addAction(self.view_up_action)
        self.addAction(self.view_down_action)
        self.addAction(self.view_right_action)
        self.addAction(self.view_left_action)
        self.addAction(self.view_front_action)
        self.addAction(self.view_back_action)
        self.addAction(self.view_orthogonal_action)
        self.addSeparator()
        self.addAction(self.show_lines_action)
        self.addAction(self.show_points_action)
        self.addAction(self.show_faces_action)
        self.addSeparator()
        self.addAction(self.clip_plane_action)

    # Callbacks
    def view_up_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_up()

    def view_down_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_down()

    def view_left_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_left()

    def view_right_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_right()

    def view_front_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_front()

    def view_back_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_back()

    def view_orthogonal_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_orthogonal()

    def show_points_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.show_points()

    def show_lines_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.show_lines()

    def show_faces_callback(self):
        widget = self.parent().viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.show_faces()

    def clip_plane_callback(self):
        self.parent().clip_plane.show()
        self.parent().slider_moved_callback()
        self.parent().slider_released_callback()