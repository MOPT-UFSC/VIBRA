
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QToolBar

from molde.render_widgets import CommonRenderWidget

from vibra import ICON_DIR, app
from vibra.utils.icons import load_icon

from pathlib import Path

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
            }
            """
        )

    def create_actions(self):
        color = QColor("#448cff")

        #
        top_view_icon = load_icon(ICON_DIR / "views/top.png", color)
        self.top_view_action = QAction(top_view_icon, "Top View", self)
        self.top_view_action.triggered.connect(self.top_view_callback)
        self.top_view_action.setShortcut("Ctrl+Shift+1")

        bottom_icon = load_icon(ICON_DIR / "views/bottom.png", color)
        self.bottom_view_action = QAction(bottom_icon, "Bottom View", self)
        self.bottom_view_action.triggered.connect(self.bottom_view_callback)
        self.bottom_view_action.setShortcut("Ctrl+Shift+2")

        right_view_icon = load_icon(ICON_DIR / "views/right.png", color)
        self.right_view_action = QAction(right_view_icon, "Right View", self)
        self.right_view_action.triggered.connect(self.right_view_callback)
        self.right_view_action.setShortcut("Ctrl+Shift+4")

        left_view_icon = load_icon(ICON_DIR / "views/left.png", color)
        self.left_view_action = QAction(left_view_icon, "Left View", self)
        self.left_view_action.triggered.connect(self.left_view_callback)
        self.left_view_action.setShortcut("Ctrl+Shift+3")

        back_view_icon = load_icon(ICON_DIR / "views/back.png", color)
        self.back_view_action = QAction(back_view_icon, "Back View", self)
        self.back_view_action.triggered.connect(self.back_view_callback)
        self.back_view_action.setShortcut("Ctrl+Shift+6")

        front_view_icon = load_icon(ICON_DIR / "views/front.png", color)
        self.front_view_action = QAction(front_view_icon, "Front View", self)
        self.front_view_action.triggered.connect(self.front_view_callback)
        self.front_view_action.setShortcut("Ctrl+Shift+5")

        view_orthogonal_icon = load_icon(ICON_DIR / "views/orthogonal.png", color)
        self.isometric_view_action = QAction(view_orthogonal_icon, "Isometric View", self)
        self.isometric_view_action.triggered.connect(self.isometric_view_callback)
        self.isometric_view_action.setShortcut("Ctrl+Shift+7")

        #
        show_points_icon = load_icon(ICON_DIR / "visibility/nodes.png", color)
        self.show_points_action = QAction(show_points_icon, "Node View", self)
        self.show_points_action.triggered.connect(self.show_points_callback)

        show_lines_icon = load_icon(ICON_DIR / "visibility/lines.png", color)
        self.show_lines_action = QAction(show_lines_icon, "Line View", self)
        self.show_lines_action.triggered.connect(self.show_lines_callback)

        show_faces_icon = load_icon(ICON_DIR / "visibility/faces.png", color)
        self.show_faces_action = QAction(show_faces_icon, "Face View", self)
        self.show_faces_action.triggered.connect(self.show_faces_callback)

        hide_show_symbols_icon = load_icon(ICON_DIR / "visibility/show_symbols.png", color)
        self.hide_show_symbols_action = QAction(hide_show_symbols_icon, "Hide/Show Symbols", self)
        self.hide_show_symbols_action.setCheckable(True)
        self.hide_show_symbols_action.triggered.connect(self.hide_show_symbols_callback)

        clip_plane_show_icon = load_icon(ICON_DIR / "visibility/section_plane_view.png", color)
        self.section_plane_show_action = QAction(clip_plane_show_icon, "View Section Plane", self)
        self.section_plane_show_action.setCheckable(True)
        # self.section_plane_show_action.triggered.connect(self.section_plane_show_callback)

        clip_plane_config_icon = load_icon(ICON_DIR / "visibility/section_plane_config.png", color)
        self.action_section_plane = QAction(clip_plane_config_icon, "Configure Section Plane", self)
        self.action_section_plane.setCheckable(True)
        self.action_section_plane.triggered.connect(self.section_plane_config_callback)

        hide_icon = load_icon(ICON_DIR / "visibility/hide_icon.png", color)
        self.hide_selection = QAction(hide_icon, "Hide Selection", self)
        self.hide_selection.setShortcut("Ctrl + H")
        self.hide_selection.triggered.connect(self.hide_selection_callback)

        unhide_all_icon = load_icon(ICON_DIR / "visibility/unhide_all_icon.png", color)
        self.unhide_all = QAction(unhide_all_icon, "Unhide All", self)
        self.unhide_all.setShortcut("Ctrl + Shift + H")
        self.unhide_all.triggered.connect(self.unhide_all_callback)

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
        self.addAction(self.show_points_action)
        self.addAction(self.show_lines_action)
        self.addAction(self.show_faces_action)
        self.addAction(self.hide_show_symbols_action)
        self.addSeparator()
        # self.addAction(self.section_plane_show_action)
        self.addAction(self.action_section_plane)
        self.addSeparator()
        self.addAction(self.hide_selection)
        self.addAction(self.unhide_all)

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
        widget = app().main_window.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_points()

    def show_lines_callback(self):
        widget = app().main_window.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_lines()

    def show_faces_callback(self):
        widget = app().main_window.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_faces()

    def hide_show_symbols_callback(self):

        symbols_actor = app().main_window.viewer_tabs.mesh_widget.symbols_actor

        if symbols_actor is None:
            return

        if symbols_actor.GetVisibility():
            symbols_actor.VisibilityOff()
        else:
            symbols_actor.VisibilityOn()

        app().main_window.viewer_tabs.mesh_widget.update()

    # def section_plane_show_callback(self, option: bool):
    #     app().main_window.section_plane.cutting = option
    #     app().main_window.section_plane.value_changed.emit()

    def section_plane_config_callback(self, condition):
        app().main_window.action_section_plane_callback(condition)

    def hide_selection_callback(self):
        app().main_window.hide_selection_callback()

    def unhide_all_callback(self):
        app().main_window.unhide_all_callback()
