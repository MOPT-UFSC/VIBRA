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

        self.configure_window()
        self.create_basic_layout()
        self.load_user_preferences()

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
        self.viewer_tabs = ViewerTabs(self, self.project, self.user_config)
        self.setCentralWidget(self.viewer_tabs)

        self.create_menu_bar()
        self.create_tool_bars()
        self.create_status_bar()

    def load_user_preferences(self):
        self.set_theme(self.user_config.theme)

    def create_menu_bar(self):
        self.menu_bar = self.menuBar()
        self.menu_bar.addMenu(ProjectMenu(self))
        self.menu_bar.addMenu(ViewsMenu(self))
        self.menu_bar.addMenu(ViewModeMenu(self))
        self.menu_bar.addMenu(HelpMenu(self))

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

        self.viewer_3d.save_png(path)

    def import_geometry(self):
        path, check = QFileDialog.getOpenFileName(
            self,
            "Open File",
            filter="Geometry Files (*.stp *.step *.iges)",
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
