import logging
from pathlib import Path
from time import sleep

import qdarktheme
from PyQt5.QtGui import QColor, QIcon, QPainter, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
)

from vibra.config import UserConfig
from vibra.interface.loading_bar import load_function
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
        self.create_actions()
        self.create_basic_layout()
        self.create_menu_bar()
        self.create_tool_bars()
        self.create_status_bar()
        self.load_user_preferences()

        self.viewer_3d.object_selected.connect(self.viewer_selection_callback)

    def load_icons(self):
        color = QColor("#0055DD")

        self.vibra_icon = load_icon(Path("data/icons/logo_vibra.png"), color)
        self.help_icon = load_icon(Path("data/icons/help.png"), color)
        self.new_project_icon = load_icon(Path("data/icons/new_file.png"), color)
        self.load_project_icon = load_icon(Path("data/icons/import.png"), color)
        self.exit_import_icon = load_icon(Path("data/icons/exit.png"), color)
        self.save_icon = load_icon(Path("data/icons/save.png"), color)
        self.save_as_icon = load_icon(Path("data/icons/save_as.png"), color)
        self.save_as_png_icon = load_icon(Path("data/icons/png.png"), color)
        self.view_up_icon = load_icon(Path("data/icons/top.png"), color)
        self.view_down_icon = load_icon(Path("data/icons/bottom.png"), color)
        self.view_right_icon = load_icon(Path("data/icons/right.png"), color)
        self.view_left_icon = load_icon(Path("data/icons/left.png"), color)
        self.view_back_icon = load_icon(Path("data/icons/back.png"), color)
        self.view_front_icon = load_icon(Path("data/icons/front.png"), color)
        self.view_orthogonal_icon = load_icon(Path("data/icons/orthogonal.png"), color)
        self.view_mode_line_icon = load_icon(Path("data/icons/lines.png"), color)
        self.view_mode_nodes_icon = load_icon(Path("data/icons/nodes.png"), color)
        self.view_mode_face_icon = load_icon(Path("data/icons/faces.png"), color)
        self.recent_icon = load_icon(Path("data/icons/recent.png"), color)
        self.theme_sun_icon = load_icon(Path("data/icons/sun_icon.png"), color)
        self.theme_moon_icon = load_icon(Path("data/icons/moon_icon.png"), color)
        self.import_geometry_icon = load_icon(Path("data/icons/cube-scan.png"), color)
        self.capture_image_icon = load_icon(Path("data/icons/image-plus.png"), color)

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

    def create_actions(self):
        self.new_project_action = QAction(self.new_project_icon, "New Project", self)
        self.load_project_action = QAction(self.load_project_icon, "Load Project", self)
        self.exit_import_action = QAction(self.exit_import_icon, "Exit", self)
        self.import_geometry_action = QAction(self.capture_image_icon, "Import geometry", self)
        self.capture_image_action = QAction(self.import_geometry_icon, "Capture image", self)
        self.save_action = QAction(self.save_icon, "Save", self)
        self.save_as_action = QAction(self.save_as_icon, "Save as", self)
        self.help_action = QAction(self.help_icon, "About Vibra", self)
        self.view_up_action = QAction(self.view_up_icon, "Up View", self)
        self.view_down_action = QAction(self.view_down_icon, "Down View", self)
        self.view_left_action = QAction(self.view_left_icon, "Left View", self)
        self.view_right_action = QAction(self.view_right_icon, "Right View", self)
        self.view_front_action = QAction(self.view_front_icon, "Front View", self)
        self.view_back_action = QAction(self.view_back_icon, "Back View", self)
        self.view_orthogonal_action = QAction(self.view_orthogonal_icon, "Orthogonal View", self)
        self.view_mode_face_action = QAction(self.view_mode_face_icon, "Face View", self)
        self.view_mode_line_action = QAction(self.view_mode_line_icon, "Line View", self)
        self.view_mode_nodes_action = QAction(self.view_mode_nodes_icon, "Node View", self)
        self.recent_action = QAction(self.recent_icon, "Recent", self)
        self.theme_action = QAction(self.theme_sun_icon, "Theme", self)

        self.import_geometry_action.triggered.connect(self.import_geometry_callback)
        self.capture_image_action.triggered.connect(self.capture_image_callback)
        self.save_action.triggered.connect(self.save_callback)
        self.help_action.triggered.connect(self.help_callback)
        self.exit_import_action.triggered.connect(self.exit_callback)
        self.view_mode_face_action.triggered.connect(self.show_faces_callback)
        self.view_mode_line_action.triggered.connect(self.show_edges_callback)
        self.view_mode_nodes_action.triggered.connect(self.show_points_callback)
        self.view_up_action.triggered.connect(self.show_view_up_callback)
        self.view_down_action.triggered.connect(self.show_view_down_callback)
        self.view_left_action.triggered.connect(self.show_view_left_callback)
        self.view_right_action.triggered.connect(self.show_view_right_callback)
        self.view_front_action.triggered.connect(self.show_view_front_callback)
        self.view_back_action.triggered.connect(self.show_view_back_callback)
        self.view_orthogonal_action.triggered.connect(self.show_view_orthogonal_callback)
        self.theme_action.triggered.connect(self.theme_callback)

        self.help_action.setShortcut("F1")

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
        self.project_menu = self.menu_bar.addMenu("Project")
        self.views_menu = self.menu_bar.addMenu("Views")
        self.views_mode_menu = self.menu_bar.addMenu("View Mode")
        self.help_menu = self.menu_bar.addMenu("Help")

        self.load_project_menu()
        self.load_views_menu()
        self.load_help_menu()
        self.load_views_mode_menu()

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

    def load_project_menu(self):
        self.project_menu.clear()
        self.project_menu.addAction(self.new_project_action)
        self.project_menu.addAction(self.load_project_action)
        self.project_menu.addAction(self.save_action)
        self.project_menu.addAction(self.save_as_action)
        self.project_menu.addAction(self.import_geometry_action)
        self.project_menu.addAction(self.capture_image_action)
        self.project_menu.addAction(self.recent_action)
        self.project_menu.addAction(self.theme_action)
        self.project_menu.addAction(self.exit_import_action)

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

    def save_callback(self):
        self.project.save()

    def help_callback(self):
        self.viewer_tabs.show_help()

    def exit_callback(self):
        loaded_function = load_function(self.project.long_function, self)
        loaded_function()

    def theme_callback(self):
        if self.user_config.theme == "light":
            self.set_theme("dark")
            self.theme_action.setIcon(self.theme_sun_icon)

        elif self.user_config.theme == "dark":
            self.set_theme("light")
            self.theme_action.setIcon(self.theme_moon_icon)

    def set_theme(self, theme: str):
        """
        Changes Qt stylesheets using qdarktheme library and the
        renderer background colors.

        The input is a string "light" or "dark".
        """
        qdarktheme.setup_theme(theme, custom_colors=self.custom_colors)
        self.viewer_tabs.set_theme(theme)
        self.user_config.theme = theme

    def capture_image_callback(self):
        path, check = QFileDialog.getSaveFileName(
            self,
            "PNG",
            filter="PNG (*.png)",
        )

        if not check:
            return

        self.viewer_3d.save_png(path)

    def import_geometry_callback(self):
        path, check = QFileDialog.getOpenFileName(
            self,
            "Open File",
            filter="Geometry Files (*.stp *.step *.iges)",
        )

        if not check:
            return

        # Slow function running with loading bar
        loaded_import_geometry = load_function(self.project.import_geometry, self)
        loaded_import_geometry(path)

        self.viewer_tabs.show_model()
        self.viewer_tabs.update_plots()
        self.set_theme(self.user_config.theme)

    def show_points_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.show_points()

    def show_edges_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.show_lines()

    def show_faces_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.show_faces()

    def show_view_up_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_up()

    def show_view_down_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_up()

    def show_view_left_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_up()

    def show_view_right_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_up()

    def show_view_front_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_up()

    def show_view_back_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_up()

    def show_view_orthogonal_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, VTKWidget):
            widget.set_view_up()

    # TODO: Create and connect actions for these
    def show_model_callback(self):
        self.viewer_tabs.show_model()

    def show_example_callback(self):
        self.viewer_tabs.show_example()

    def viewer_selection_callback(self):
        if self.viewer_3d.current_renderer == self.viewer_3d.model_renderer:
            points = self.viewer_3d.model_renderer.selected_points
            lines = self.viewer_3d.model_renderer.selected_lines
            faces = self.viewer_3d.model_renderer.selected_faces

            if points:
                print(f"Selected points: {points}")

            if lines:
                print(f"Selected lines: {lines}")

            if faces:
                print(f"Selected faces: {faces}")

    def closeEvent(self, event):
        close = QMessageBox.question(
            self, "QUIT", "Are you sure want to stop process?", QMessageBox.Yes | QMessageBox.No
        )
        if close == QMessageBox.Yes:
            self.user_config.save()
            event.accept()
        else:
            event.ignore()
