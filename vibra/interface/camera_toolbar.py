from molde.render_widgets import CommonRenderWidget
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QStackedWidget, QToolBar

from vibra import LIGHT_ICON_COLOR
from vibra.utils.icons import load_icon


class CameraToolbar(QToolBar):
    def __init__(self, render_widget_stack: QStackedWidget):
        super().__init__()
        self.render_widget_stack = render_widget_stack

        self._load_icons()
        self._create_actions()
        self._configure_layout()
        self._configure_appearance()

        self.setWindowTitle("Camera toolbar")

    def _load_icons(self):
        color = LIGHT_ICON_COLOR.to_qt()

        self.top_icon = load_icon(":/icons/views/top.png", color)
        self.bottom_icon = load_icon(":/icons/views/bottom.png", color)
        self.right_icon = load_icon(":/icons/views/right.png", color)
        self.left_icon = load_icon(":/icons/views/left.png", color)
        self.front_icon = load_icon(":/icons/views/front.png", color)
        self.back_icon = load_icon(":/icons/views/back.png", color)
        self.isometric_icon = load_icon(":/icons/views/orthogonal.png", color)
        self.zoom_to_fit_icon = load_icon(":/icons/views/zoom_icon.png", color)

    def _create_actions(self):
        self.action_top_view = QAction(self.top_icon, "Top View", self)
        self.action_top_view.setShortcut("Ctrl+Shift+1")
        self.action_top_view.triggered.connect(self.set_top_view)

        self.action_bottom_view = QAction(self.bottom_icon, "Bottom View", self)
        self.action_bottom_view.setShortcut("Ctrl+Shift+2")
        self.action_bottom_view.triggered.connect(self.set_bottom_view)

        self.action_right_view = QAction(self.right_icon, "Right View", self)
        self.action_right_view.setShortcut("Ctrl+Shift+3")
        self.action_right_view.triggered.connect(self.set_right_view)

        self.action_left_view = QAction(self.left_icon, "Left View", self)
        self.action_left_view.setShortcut("Ctrl+Shift+4")
        self.action_left_view.triggered.connect(self.set_left_view)

        self.action_front_view = QAction(self.front_icon, "Front View", self)
        self.action_front_view.setShortcut("Ctrl+Shift+5")
        self.action_front_view.triggered.connect(self.set_front_view)

        self.action_back_view = QAction(self.back_icon, "Back View", self)
        self.action_back_view.setShortcut("Ctrl+Shift+6")
        self.action_back_view.triggered.connect(self.set_back_view)

        self.action_isometric_view = QAction(self.isometric_icon, "Isometric View", self)
        self.action_isometric_view.setShortcut("Ctrl+Shift+7")
        self.action_isometric_view.triggered.connect(self.set_isometric_view)

        self.action_zoom_to_fit = QAction(self.zoom_to_fit_icon, "Zoom To Fit", self)
        self.action_zoom_to_fit.triggered.connect(self.zoom_to_fit)

    def _configure_layout(self):
        self.addAction(self.action_top_view)
        self.addAction(self.action_bottom_view)
        self.addAction(self.action_right_view)
        self.addAction(self.action_left_view)
        self.addAction(self.action_front_view)
        self.addAction(self.action_back_view)
        self.addAction(self.action_isometric_view)
        self.addAction(self.action_zoom_to_fit)

    def _configure_appearance(self):
        self.setMovable(True)
        self.setFloatable(True)

    def _current_render_widget(self):
        return self.render_widget_stack.currentWidget()

    def set_top_view(self):
        widget = self._current_render_widget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_top_view()

    def set_bottom_view(self):
        widget = self._current_render_widget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_bottom_view()

    def set_right_view(self):
        widget = self._current_render_widget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_right_view()

    def set_left_view(self):
        widget = self._current_render_widget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_left_view()

    def set_front_view(self):
        widget = self._current_render_widget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_front_view()

    def set_back_view(self):
        widget = self._current_render_widget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_back_view()

    def set_isometric_view(self):
        widget = self._current_render_widget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_isometric_view()

    def zoom_to_fit(self):
        widget = self._current_render_widget()
        if isinstance(widget, CommonRenderWidget):
            widget.renderer.ResetCamera()
            widget.update()
