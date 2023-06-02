import logging
from pathlib import Path
from time import sleep

import qdarktheme
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QAction,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
)

from vibra.config import UserConfig
from vibra.interface.loading_bar import load_function
from vibra.interface.menus.help_menu import HelpMenu
from vibra.interface.menus.project_menu import ProjectMenu
from vibra.interface.menus.view_mode_menu import ViewModeMenu
from vibra.interface.menus.views_menu import ViewsMenu
from vibra.interface.renderer_toolbar import RendererToolbar
from vibra.interface.viewer_3d.viewer_3d import Viewer3D
from vibra.interface.viewer_3d.vtk_widget import VTKWidget
from vibra.interface.viewer_tabs import ViewerTabs
from vibra.project import Project
from vibra.utils.icons import load_icon


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.project = Project()
        self.viewer_3d = Viewer3D(self)
        self.user_config = UserConfig()

        self.load_icons()
        self.configure_window()
        self.create_basic_layout()
        self.create_menu_bar()
        self.create_tool_bars()
        self.create_status_bar()
        self.load_user_preferences()

    def load_icons(self):
        color = QColor("#0055DD")
        self.vibra_icon = load_icon(Path("data/icons/logo_vibra.png"), color)

    def configure_window(self):
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setWindowIcon(self.vibra_icon)
        self.setWindowTitle("Vibra")

        # for qdarktheme
        self.custom_colors = {
            "[dark]": {
                "toolbar.background": "#202124",
            }
        }

    def create_basic_layout(self):
        self.viewer_tabs = ViewerTabs(self, self.project, self.user_config)
        self.setCentralWidget(self.viewer_tabs)

    def load_user_preferences(self):
        self.set_theme(self.user_config.theme)

    def long_exit_function(self):
        loaded_function = self.load_function()
        loaded_function()

    def create_menu_bar(self):
        self.menu_bar = self.menuBar()

        self.help_menu = HelpMenu(self)
        self.view_mode_menu = ViewModeMenu(self)
        self.views_menu = ViewsMenu(self)
        self.project_menu = ProjectMenu(self)
        self.menu_bar.addMenu(self.project_menu)
        self.menu_bar.addMenu(self.views_menu)
        self.menu_bar.addMenu(self.view_mode_menu)
        self.menu_bar.addMenu(self.help_menu)

    def create_tool_bars(self):
        self.renderer_toolbar = RendererToolbar(self, self.viewer_tabs)
        self.addToolBar(self.renderer_toolbar)

    def create_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("This is status bar")
        self.label_1 = QLabel("Label 1")
        self.label_1.move(100, 100)
        self.status_bar.setStyleSheet("background-image : url(data/icons/png.png);")
        self.label_2 = QLabel("Label 2")
        self.label_1.setStyleSheet(
            """
                border :2px solid;
                border-width: 1px;
                border-color: #888888;
                border-radius: 3px"""
        )

        # adding label to status bar
        self.status_bar.addPermanentWidget(self.label_1)
        self.status_bar.addPermanentWidget(self.label_2)

    def load_views_menu(self):
        self.views_menu.addAction(self.view_up_action)
        self.views_menu.addAction(self.view_down_action)
        self.views_menu.addAction(self.view_left_action)
        self.views_menu.addAction(self.view_right_action)
        self.views_menu.addAction(self.view_front_action)
        self.views_menu.addAction(self.view_back_action)
        self.views_menu.addAction(self.view_orthogonal_action)

    def load_views_mode_menu(self):
        self.views_mode_menu.addAction(self.view_mode_nodes_action)
        self.views_mode_menu.addAction(self.view_mode_line_action)
        self.views_mode_menu.addAction(self.view_mode_face_action)

    def load_help_menu(self):
        self.help_menu.addAction(self.help_action)

    def set_theme(self, theme: str):
        """
        Changes Qt stylesheets using qdarktheme library and the
        renderer background colors.

        The input is a string "light" or "dark".
        """
        qdarktheme.setup_theme(theme, custom_colors=self.custom_colors)
        self.viewer_tabs.set_theme(theme)
        self.user_config.theme = theme

    def closeEvent(self, event):
        close = QMessageBox.question(
            self, "QUIT", "Are you sure want to stop process?", QMessageBox.Yes | QMessageBox.No
        )
        if close == QMessageBox.Yes:
            self.user_config.save()
            event.accept()
        else:
            event.ignore()
