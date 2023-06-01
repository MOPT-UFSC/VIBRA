from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPixmap

from PyQt5.QtWidgets import (
    QAction,
    QToolBar,
)
from pathlib import Path
from vibra.interface.viewer_3d.vtk_widget import VTKWidget

def load_icon(path, color):
    pixmap = QPixmap(str(path))
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    return QIcon(pixmap)


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
        view_mode_nodes_icon = load_icon(Path("data/icons/nodes.png"), color)
        self.view_mode_nodes_action = QAction(view_mode_nodes_icon, "Node View", self)

        view_mode_line_icon = load_icon(Path("data/icons/lines.png"), color)
        self.view_mode_line_action = QAction(view_mode_line_icon, "Line View", self)
        
        view_mode_face_icon = load_icon(Path("data/icons/faces.png"), color)
        self.view_mode_face_action = QAction(view_mode_face_icon, "Face View", self)

    
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
        self.addAction(self.view_mode_line_action)
        self.addAction(self.view_mode_nodes_action)
        self.addAction(self.view_mode_face_action)
        self.addSeparator()

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
