from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar, QSizePolicy

from vibra.interface.viewer_3d.render_tools import GrabTool, RotationTool, ZoomTool, RenderTool, SelectionTool


class RenderToolsToolbar(QToolBar):
    render_tool_changed = Signal(RenderTool)
    def __init__(self, parent=None):
        super().__init__(parent)

        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy1)
        self.setStyleSheet(u"\n"
                                                "            QToolBar {\n"
                                                "                border-style: solid;\n"
                                                "                border-width: 1px;\n"
                                                "                border-color: #888888;\n"
                                                "            }")

        self.action_grab_tool = QAction(self)
        self.action_grab_tool.setObjectName(u"action_grab_tool")
        self.action_grab_tool.setCheckable(True)
        icon34 = QIcon(":/icons/pan_icon.png")
        self.action_grab_tool.setIcon(icon34)
        self.action_selection_tool = QAction(self)
        self.action_selection_tool.setObjectName(u"action_selection_tool")
        self.action_selection_tool.setCheckable(True)
        self.action_selection_tool.setChecked(True)
        icon35 = QIcon(":/icons/selection_icon.png")
        self.action_selection_tool.setIcon(icon35)
        self.action_rotation_tool = QAction(self)
        self.action_rotation_tool.setObjectName(u"action_rotation_tool")
        self.action_rotation_tool.setCheckable(True)
        icon36 = QIcon(":/icons/rotation_icon.png")
        self.action_rotation_tool.setIcon(icon36)
        self.action_zoom_in = QAction(self)
        self.action_zoom_in.setObjectName(u"action_zoom_in")
        self.action_zoom_in.setCheckable(True)
        icon37 = QIcon(":/icons/zoom_in_icon.png")
        self.action_zoom_in.setIcon(icon37)

        self.action_selection_tool.triggered.connect(self.action_selection_tool_callback)
        self.action_grab_tool.triggered.connect(self.action_grab_tool_callback)
        self.action_rotation_tool.triggered.connect(self.action_rotation_tool_callback)
        self.action_zoom_in.triggered.connect(self.action_zoom_in_callback)

        self.addSeparator()
        self.addAction(self.action_selection_tool)
        self.addSeparator()
        self.addAction(self.action_grab_tool)
        self.addSeparator()
        self.addAction(self.action_rotation_tool)
        self.addSeparator()
        self.addAction(self.action_zoom_in)

    def action_grab_tool_callback(self):
        if self.action_grab_tool.isChecked():
            self.discheck_all_actions_of_render_tools_toolbar_except(self.action_grab_tool)

            tool = GrabTool()
            self.render_tool_changed.emit(tool)
        else:
            self.action_selection_tool_callback()

    def action_selection_tool_callback(self):
        self.discheck_all_actions_of_render_tools_toolbar_except(self.action_selection_tool)
        tool = SelectionTool()
        self.render_tool_changed.emit(tool)

    def action_rotation_tool_callback(self):
        if self.action_rotation_tool.isChecked():
            self.discheck_all_actions_of_render_tools_toolbar_except(self.action_rotation_tool)

            tool = RotationTool()
            self.render_tool_changed.emit(tool)
        else:
            self.action_selection_tool_callback()

    def action_zoom_in_callback(self):
        if self.action_zoom_in.isChecked():
            self.discheck_all_actions_of_render_tools_toolbar_except(self.action_zoom_in)

            tool = ZoomTool()
            self.render_tool_changed.emit(tool)
        else:
            self.action_selection_tool_callback()

    def discheck_all_actions_of_render_tools_toolbar_except(self, action: QAction):
        for _action in self.actions():
            _action.setChecked(False)

        action.setChecked(True)
