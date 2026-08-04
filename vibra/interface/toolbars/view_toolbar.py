from molde.render_widgets import CommonRenderWidget
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QStackedWidget, QToolBar

from vibra.interface.viewer_3d.render_tools import GrabTool, RenderTool, RotationTool, SelectionTool, ZoomTool
from vibra.interface.formatters.icons import Icon


class ViewToolbar(QToolBar):
    render_tool_changed = Signal(RenderTool)

    def __init__(self, render_widget_stack: QStackedWidget):
        super().__init__()
        self.render_widget_stack = render_widget_stack

        self._load_icons()
        self._create_actions()
        self._configure_layout()
        self._configure_actions()
        self._configure_appearance()

        self.setWindowTitle("View toolbar")

    def _load_icons(self):
        self.top_icon = Icon(":/icons/views/top.png")
        self.bottom_icon = Icon(":/icons/views/bottom.png")
        self.right_icon = Icon(":/icons/views/right.png")
        self.left_icon = Icon(":/icons/views/left.png")
        self.front_icon = Icon(":/icons/views/front.png")
        self.back_icon = Icon(":/icons/views/back.png")
        self.isometric_icon = Icon(":/icons/views/orthogonal.png")
        self.zoom_to_fit_icon = Icon(":/icons/views/zoom_icon.png")
        self.selection_tool_icon = Icon(":/icons/selection_icon.png")
        self.grab_tool_icon = Icon(":/icons/grab_icon.png")
        self.rotation_tool_icon = Icon(":/icons/rotation_icon.png")
        self.zoom_tool_icon = Icon(":/icons/zoom_icon.png")

    def _create_actions(self):
        self.action_top_view = QAction(self.top_icon, "Top View", self)
        self.action_top_view.setShortcut("Ctrl+1")
        self.action_top_view.triggered.connect(self.set_top_view)

        self.action_bottom_view = QAction(self.bottom_icon, "Bottom View", self)
        self.action_bottom_view.setShortcut("Ctrl+2")
        self.action_bottom_view.triggered.connect(self.set_bottom_view)

        self.action_right_view = QAction(self.right_icon, "Right View", self)
        self.action_right_view.setShortcut("Ctrl+3")
        self.action_right_view.triggered.connect(self.set_right_view)

        self.action_left_view = QAction(self.left_icon, "Left View", self)
        self.action_left_view.setShortcut("Ctrl+4")
        self.action_left_view.triggered.connect(self.set_left_view)

        self.action_front_view = QAction(self.front_icon, "Front View", self)
        self.action_front_view.setShortcut("Ctrl+5")
        self.action_front_view.triggered.connect(self.set_front_view)

        self.action_back_view = QAction(self.back_icon, "Back View", self)
        self.action_back_view.setShortcut("Ctrl+6")
        self.action_back_view.triggered.connect(self.set_back_view)

        self.action_isometric_view = QAction(self.isometric_icon, "Isometric View", self)
        self.action_isometric_view.setShortcut("Ctrl+7")
        self.action_isometric_view.triggered.connect(self.set_isometric_view)

        self.action_zoom_to_fit = QAction(self.zoom_to_fit_icon, "Zoom To Fit", self)
        self.action_zoom_to_fit.triggered.connect(self.zoom_to_fit)

        self.action_selection_tool = QAction(self.selection_tool_icon, "Selection Tool", self)
        self.action_selection_tool.triggered.connect(self.action_selection_tool_callback)

        self.action_grab_tool = QAction(self.grab_tool_icon, "Grab Tool", self)
        self.action_grab_tool.triggered.connect(self.action_grab_tool_callback)

        self.action_rotation_tool = QAction(self.rotation_tool_icon, "Rotation Tool", self)
        self.action_rotation_tool.triggered.connect(self.action_rotation_tool_callback)

        self.action_zoom_tool = QAction(self.zoom_tool_icon, "Zoom Tool", self)
        self.action_zoom_tool.triggered.connect(self.action_zoom_tool_callback)

    def _configure_layout(self):
        self.addAction(self.action_selection_tool)
        self.addAction(self.action_grab_tool)
        self.addAction(self.action_rotation_tool)
        self.addAction(self.action_zoom_tool)
        # self.addSeparator()
        self.addAction(self.action_top_view)
        self.addAction(self.action_bottom_view)
        self.addAction(self.action_right_view)
        self.addAction(self.action_left_view)
        self.addAction(self.action_front_view)
        self.addAction(self.action_back_view)
        self.addAction(self.action_isometric_view)
        self.addAction(self.action_zoom_to_fit)

    def _configure_actions(self):
        self._render_tool_actions = [
            self.action_selection_tool, self.action_grab_tool,
            self.action_rotation_tool, self.action_zoom_tool,
        ]

        for action in self._render_tool_actions:
            action.setCheckable(True)

        for action in (
            self.action_top_view,
            self.action_bottom_view,
            self.action_right_view,
            self.action_left_view,
            self.action_front_view,
            self.action_back_view,
            self.action_isometric_view,
        ):
            action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)

        self.action_selection_tool.setChecked(True)

    def _configure_appearance(self):
        self.setMovable(True)
        self.setOrientation(Qt.Vertical)
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
        
    def action_grab_tool_callback(self):
        if self.action_grab_tool.isChecked():
            self.discheck_all_actions_of_render_tools_toolbar_except(self.action_grab_tool)
            self.render_tool_changed.emit(GrabTool)
        else:
            self.action_selection_tool_callback()

    def action_selection_tool_callback(self):
        self.discheck_all_actions_of_render_tools_toolbar_except(self.action_selection_tool)
        self.render_tool_changed.emit(SelectionTool)

    def action_rotation_tool_callback(self):
        if self.action_rotation_tool.isChecked():
            self.discheck_all_actions_of_render_tools_toolbar_except(self.action_rotation_tool)
            self.render_tool_changed.emit(RotationTool)
        else:
            self.action_selection_tool_callback()

    def action_zoom_tool_callback(self):
        if self.action_zoom_tool.isChecked():
            self.discheck_all_actions_of_render_tools_toolbar_except(self.action_zoom_tool)
            self.render_tool_changed.emit(ZoomTool)
        else:
            self.action_selection_tool_callback()

    def discheck_all_actions_of_render_tools_toolbar_except(self, action: QAction):
        for _action in self._render_tool_actions:
            _action.setChecked(False)

        action.setChecked(True)
    
    def enable_selection_tool(self):
        self.action_selection_tool.setEnabled(True)

    def disable_selection_tool(self):
        self.action_selection_tool.setEnabled(False)

    def show_render_tools(self):
        for action in self._render_tool_actions:
            action.setVisible(True)

    def hide_render_tools(self):
        for action in self._render_tool_actions:
            action.setVisible(False)
