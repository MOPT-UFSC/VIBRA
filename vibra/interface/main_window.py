import logging
import random
from pathlib import Path
from time import sleep
import sys

import qdarktheme
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vibra import app

from vibra.config import UserConfig
from vibra.interface.analysis_filter_menu import AnalysisFilter
from vibra.interface.clip_plane_widget import ClipPlaneWidget
from vibra.interface.data_handler.export_mesh_data import ExportMeshData
from vibra.interface.exception_message import ErrorMessage
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
from vibra.interface.formatters.icons import *
from vibra.project import Project

from vibra.utils.icons import load_icon


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        
        self.dialog = None
        self.project = Project()
        self.user_config = UserConfig.load()
        self.status_bar = StatusBar(self)

    def _define_qt_variables(self):
        pass

    def _create_connections(self):
        self.viewer_tabs.geometry_widget.selection_changed.connect(self.selection_changed_callback)
        self.clip_plane.slider_pressed.connect(self.slider_pressed_callback)
        self.clip_plane.value_changed.connect(self.slider_moved_callback)
        self.clip_plane.slider_released.connect(self.slider_released_callback)
        self.clip_plane.closed.connect(self.disable_cut)

    def selection_changed_callback(self, points, lines, faces, volumes):
        self.status_bar.set_selection(points, lines, faces, volumes)

    def update_mesh_information(self, nodes, face_elements, solid_elements):
        self.status_bar.update_mesh_information(nodes, face_elements, solid_elements)

    def update_geometry_information(self):
        self.status_bar.update_geometry_information()

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

    def _config_window(self):
        self.setMinimumSize(1300, 700)
        # self.showMaximized()
        self.showMinimized()
        self.vibra_icon = get_vibra_icon()
        self.setWindowIcon(self.vibra_icon)
        self.setWindowTitle("Vibra")

        # for qdarktheme
        self.custom_colors = {
            "[dark]": {
                "toolbar.background": "#202124",
            }
        }

    def create_basic_layout(self):
        self.menu_widget = MenuItems()
        self.analysis_filter = AnalysisFilter()

        grid_layout_left = QGridLayout()
        grid_layout_left.addWidget(self.analysis_filter, 0, 0)
        grid_layout_left.addWidget(self.menu_widget, 1, 0)
        grid_layout_left.setContentsMargins(0, 0, 0, 0)
        grid_layout_left.setVerticalSpacing(0)

        left_widget = QWidget()
        left_widget.setLayout(grid_layout_left)
        # left_widget.setMinimumWidth(290)
        left_widget.setMaximumWidth(290)

        self.vertical_line = QFrame()
        self.vertical_line.setLineWidth(4)
        self.vertical_line.setFrameShape(QFrame.VLine)
        self.vertical_line.setFrameShadow(QFrame.Sunken)

        self.setCentralWidget(None)
        self.create_menu_bar()
        self.create_tool_bars()
        self.create_status_bar()

        grid_layout_central = QGridLayout()
        grid_layout_central.addWidget(left_widget, 0, 0)
        grid_layout_central.addWidget(self.vertical_line, 0, 1)
        grid_layout_central.addWidget(self.viewer_tabs, 0, 2)
        grid_layout_central.setContentsMargins(0, 0, 0, 0)
        grid_layout_central.setHorizontalSpacing(0)

        central_widget = QWidget()
        central_widget.setLayout(grid_layout_central)
        self.setCentralWidget(central_widget)

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
        self.analysis_filter.setDisabled(True)

    def config_tool_tip_appearance(self):
        tool_tip_style = "QToolTip { color: rgb(0, 0, 0); background-color: rgb(255, 255, 255) }"
        self.setStyleSheet(tool_tip_style)

    def _load_render_widgets(self):
        self.clip_plane = ClipPlaneWidget(self)
        # t0 = time()
        self.viewer_tabs = ViewerTabs(self, self.project, self.user_config)
        # dt = time() - t0
        # print(f"elapsed time to load class: {round(dt, 4)}")

    def configure_main_window(self):

        app().splash.update_progress(10)
        self._config_window()

        app().splash.update_progress(30)
        self._load_render_widgets()

        app().splash.update_progress(60)
        self._define_qt_variables()
        self._create_connections()
        self.create_basic_layout()

        app().splash.update_progress(90)
        self.load_user_preferences()
        self.config_tool_tip_appearance()

        app().splash.close()
        self.showMaximized()

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

    def set_menu_items_visibility_state(self, state: bool):
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

    def new_project_dialog(self):
        self.project = Project()
        self.import_geometry_dialog()

    def save_project_dialog(self):
        if self.project.save_path is None:
            self.save_project_as_dialog()
        else:
            self.save_project_as(self.project.save_path)

    def save_project_as_dialog(self):
        path, check = QFileDialog.getSaveFileName(
            self,
            "Save As",
            filter="Vibra File (*.vibra)",
        )

        if not check:
            return

        self.save_project_as(path)

    def open_project_dialog(self):
        path, check = QFileDialog.getOpenFileName(
            self, "Open Project", filter="Vibra File (*.vibra)"
        )

        if not check:
            return

        self.open_project(path)

    def import_geometry_dialog(self):
        path, check = QFileDialog.getOpenFileName(
            self,
            "Select Geometry",
            filter="Geometry Files (*.stp *.step *.iges *.igs)",
        )

        if not check:
            return

        self.import_geometry(path)

    def save_project_as(self, path):
        path = Path(path)
        self.project.name = path.stem
        self.project.save(path)
        self.user_config.save()  # why not

    def export_mesh(self):
        ExportMeshData()

    def open_project(self, path):
        path = Path(path)
        self.project = Project.load(path)
        # self.user_config.add_recent_file(path)

        self.viewer_tabs.close_mesh_tabs()
        self.viewer_tabs.show_geometry()
        self.viewer_tabs.show_mesh()

    def import_geometry(self, path):
        # Slow function running with loading bar
        import_geometry = load_function(self.project.import_geometry, self)
        import_geometry(path)

        self.viewer_tabs.reset_tab_visibility()
        self.viewer_tabs.show_geometry()

        self.renderer_toolbar.setDisabled(False)
        self.analysis_filter.setDisabled(False)
        self.menu_widget.modify_items_access_after_geometry_importing()

        self.project.reset_solutions()
        self.project.model.properties._reset_variables()

    def close_app(self):
        close = QMessageBox.question(
            self, "QUIT", "Are you sure want to close Vibra?", QMessageBox.Yes | QMessageBox.No
        )

        if close == QMessageBox.Yes:
            self.user_config.save()
            sys.exit()

    def process_acoustic_modal_analysis(self):
        try:
            self.project.solve_acoustic_modal_analysis()
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            self.viewer_tabs.show_acoustic_modal_analysis()

    def process_structural_modal_analysis(self):
        try:
            self.project.solve_structural_modal_analysis()
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            self.viewer_tabs.show_structural_modal_analysis()

    def process_acoustic_harmonic_analysis(self):
        try:
            self.project.solve_acoustic_harmonic_analysis()
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            self.viewer_tabs.show_acoustic_harmonic_analysis()

    def set_input_widget(self, dialog):
        self.dialog = dialog
