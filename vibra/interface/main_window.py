import logging
import random
from pathlib import Path
from time import sleep

import qdarktheme
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
)

from vibra.config import UserConfig
from vibra.interface.clip_plane_widget import ClipPlaneWidget
from vibra.interface.loading_bar import load_function
from vibra.interface.menus.help_menu import HelpMenu
from vibra.interface.menus.project_menu import ProjectMenu
from vibra.interface.menus.view_mode_menu import ViewModeMenu
from vibra.interface.menus.views_menu import ViewsMenu
from vibra.interface.menus.mesher_menu import MesherMenu
from vibra.interface.renderer_toolbar import RendererToolbar
from vibra.interface.status_bar import StatusBar
from vibra.interface.viewer_tabs import ViewerTabs
from vibra.project import Project
from vibra.utils.icons import load_icon


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.project = Project()
        # self.viewer_3d = Viewer3D(self)
        self.user_config = UserConfig()
        self.status_bar = StatusBar(self)
        self.clip_plane = ClipPlaneWidget(self)
        self.viewer_tabs = ViewerTabs(self, self.project, self.user_config)

        self.configure_window()
        self.create_basic_layout()
        self.load_user_preferences()

        self.viewer_tabs.model_widget.selection_changed.connect(self.selection_changed_callback)
        self.clip_plane.slider_pressed.connect(self.slider_pressed_callback)
        self.clip_plane.value_changed.connect(self.slider_moved_callback)
        self.clip_plane.slider_released.connect(self.slider_released_callback)
        self.clip_plane.closed.connect(self.disable_cut)

    def selection_changed_callback(self, points, lines, faces):
        if points:
            self.status_bar.show_points(points)
        elif lines:
            self.status_bar.show_lines(lines)
        elif faces:
            self.status_bar.show_faces(faces)
        else:
            self.status_bar.clear_selections()

    def slider_pressed_callback(self):
        if self.viewer_tabs.example_analisys_widget is None:
            return
        self.viewer_tabs.example_analisys_widget.show_plane()
        self.viewer_tabs.example_analisys_widget.disable_cut()

    def slider_moved_callback(self):
        if self.viewer_tabs.example_analisys_widget is None:
            return
        pos = self.clip_plane.get_position()
        orientation = self.clip_plane.get_rotation()
        self.viewer_tabs.example_analisys_widget.configure_plane(pos, orientation)

    def slider_released_callback(self):
        if self.viewer_tabs.example_analisys_widget is None:
            return
        pos = self.clip_plane.get_position()
        orientation = self.clip_plane.get_rotation()
        self.viewer_tabs.example_analisys_widget.apply_cut(pos, orientation)
        self.viewer_tabs.example_analisys_widget.hide_plane()

    def disable_cut(self):
        if self.viewer_tabs.example_analisys_widget is None:
            return
        self.viewer_tabs.example_analisys_widget.disable_cut()

    def configure_window(self):
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setWindowIcon(load_icon(Path("data/icons/logo_vibra.png"), QColor("#0055DD")))
        self.setWindowTitle("Vibra")

        # for qdarktheme
        self.custom_colors = {
            "[dark]": {
                "toolbar.background": "#202124",
            }
        }

    def create_basic_layout(self):
        self.setCentralWidget(self.viewer_tabs)

        self.create_menu_bar()
        self.create_tool_bars()
        self.create_status_bar()

    def load_user_preferences(self):
        self.set_theme(self.user_config.theme)

    def create_menu_bar(self):
        self.menu_bar = self.menuBar()
        self.menu_bar.addMenu(ProjectMenu(self))
        self.menu_bar.addMenu(MesherMenu(self))
        self.menu_bar.addMenu(ViewsMenu(self))
        self.menu_bar.addMenu(ViewModeMenu(self))
        self.menu_bar.addMenu(HelpMenu(self))

    def create_tool_bars(self):
        self.renderer_toolbar = RendererToolbar(self, self.viewer_tabs)
        self.addToolBar(self.renderer_toolbar)

    def create_status_bar(self):
       self.setStatusBar(self.status_bar)

    def closeEvent(self, event):
        self.close_app()
        event.ignore()

    # External functions that may be usefull
    def set_theme(self, theme: str):
        """
        Changes Qt stylesheets using qdarktheme library and the
        renderer background colors.

        The input is a string "light" or "dark".
        """
        qdarktheme.setup_theme(theme, custom_colors=self.custom_colors)
        self.viewer_tabs.set_theme(theme)
        self.user_config.theme = theme

    def capture_image(self):
        path, check = QFileDialog.getSaveFileName(
            self,
            "PNG",
            filter="PNG (*.png)",
        )

        if not check:
            return

        # self.viewer_3d.save_png(path)

    def import_geometry(self):
        path, check = QFileDialog.getOpenFileName(
            self,
            "Open File",
            filter="Geometry Files (*.stp; *.step; *.iges)",
        )

        if not check:
            return

        # Slow function running with loading bar
        import_geometry = load_function(self.project.import_geometry, self)
        import_geometry(path)

        self.viewer_tabs.show_model()
        self.viewer_tabs.update_plots()
        self.set_theme(self.user_config.theme)

    def close_app(self):
        close = QMessageBox.question(
            self, "QUIT", "Are you sure want to close Vibra?", QMessageBox.Yes | QMessageBox.No
        )

        if close == QMessageBox.Yes:
            self.user_config.save()
            exit()
