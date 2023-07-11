import logging
import random
from pathlib import Path
from time import sleep

import qdarktheme
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vibra.interface.clip_plane_widget import ClipPlaneWidget
from vibra.interface.loading_bar import load_function
from vibra.interface.menu_items import MenuItems
from vibra.interface.menus.help_menu import HelpMenu
from vibra.interface.menus.mesher_menu import MesherMenu
from vibra.interface.menus.project_menu import ProjectMenu
from vibra.interface.menus.settings_menu import VisibilitySettingsMenu
from vibra.interface.menus.view_mode_menu import ViewModeMenu
from vibra.interface.menus.views_menu import ViewsMenu
from vibra.interface.renderer_toolbar import RendererToolbar
from vibra.interface.status_bar import StatusBar
from vibra.interface.viewer_tabs import ViewerTabs

from vibra.config import UserConfig
from vibra.project import Project
from vibra.utils.icons import load_icon


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.project = Project()
        self.user_config = UserConfig()
        self.status_bar = StatusBar(self)
        self.clip_plane = ClipPlaneWidget(self)
        self.viewer_tabs = ViewerTabs(self, self.project, self.user_config)

        self.configure_window()
        self.create_basic_layout()
        self.load_user_preferences()
        self.config_tool_tip_appearance()

        self.viewer_tabs.geometry_widget.selection_changed.connect(self.selection_changed_callback)
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
        self.viewer_tabs.start_cutting_mode()

    def slider_moved_callback(self):
        position = self.clip_plane.get_position()
        orientation = self.clip_plane.get_rotation()
        self.viewer_tabs.configure_cutting_plane(position, orientation)

    def slider_released_callback(self):
        position = self.clip_plane.get_position()
        orientation = self.clip_plane.get_rotation()
        self.viewer_tabs.apply_cutting_plane(position, orientation)

    def disable_cut(self):
        self.viewer_tabs.stop_cutting_mode()

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
        self.menu_widget = MenuItems()

        self.setCentralWidget(None)
        self.create_menu_bar()
        self.create_tool_bars()
        self.create_status_bar()

        working_area = QSplitter(Qt.Horizontal)
        self.setCentralWidget(working_area)

        working_area.addWidget(self.menu_widget)
        working_area.addWidget(self.viewer_tabs)
        working_area.setSizes([50, 400])

    def create_menu_bar(self):
        self.menu_bar = self.menuBar()
        self.menu_bar.addMenu(ProjectMenu(self))
        self.menu_bar.addMenu(VisibilitySettingsMenu(self))
        self.menu_bar.addMenu(MesherMenu(self))
        # self.menu_bar.addMenu(ViewsMenu(self))
        self.menu_bar.addMenu(ViewModeMenu(self))
        self.menu_bar.addMenu(HelpMenu(self))

    def create_status_bar(self):
        self.setStatusBar(self.status_bar)

    def create_tool_bars(self):
        self.renderer_toolbar = RendererToolbar(self, self.viewer_tabs)
        self.addToolBar(self.renderer_toolbar)
        self.renderer_toolbar.setDisabled(True)

    def config_tool_tip_appearance(self):
        tool_tip_style = "QToolTip { color: rgb(0, 0, 0); background-color: rgb(255, 255, 255) }"
        self.setStyleSheet(tool_tip_style)

    def load_user_preferences(self):
        self.set_theme(self.user_config.theme)

    def closeEvent(self, event):
        self.close_app()
        event.ignore()

    def get_user_config(self):
        return self.user_config
    
    def get_project(self):
        return self.project

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
        self.menu_widget._configItems()

    def set_menu_items_visibility_state(self, state: str):
        self.user_config.menu_items_visible = state

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
            filter="Geometry Files (*.stp *.step *.iges)",
        )

        if not check:
            return

        # Slow function running with loading bar
        import_geometry = load_function(self.project.import_geometry, self)
        import_geometry(path)

        self.viewer_tabs.show_geometry()
        self.viewer_tabs.update_plots()
        self.renderer_toolbar.setDisabled(False)

    def close_app(self):
        close = QMessageBox.question(
            self, "QUIT", "Are you sure want to close Vibra?", QMessageBox.Yes | QMessageBox.No
        )

        if close == QMessageBox.Yes:
            self.user_config.save()
            exit()

    def process_acoustic_modal_analysis(self):
        self.project.solve_modal_acoustic()
        self.viewer_tabs.show_acoustic_modal_analysis()
