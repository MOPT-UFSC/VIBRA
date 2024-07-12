from PyQt5.QtWidgets import QDialog, QFileDialog, QFrame, QGridLayout, QMainWindow, QMessageBox
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import pyqtSignal

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

from vibra.project_files.project import Project
from vibra.project_files.load_project import LoadProject

from vibra.project_files.project_file_io import ProjectFileIO

import qdarktheme

import sys
import logging
import random
from pathlib import Path
from shutil import rmtree
from time import sleep


class MainWindow(QMainWindow):
    theme_changed = pyqtSignal(str)
    visualization_changed = pyqtSignal()
    selection_changed = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.selected_mesh_nodes = set()
        self.selected_mesh_faces = set()
        self.selected_mesh_solids = set()
        self.selected_geometry_points = set()
        self.selected_geometry_lines = set()
        self.selected_geometry_surfaces = set()
        self.selected_geometry_volumes = set()
        
        self.dialog = None
        self.project = Project()
        self.user_config = UserConfig.load()

        self._initialize()

    def _initialize(self):
        self.project_path = ""    
        self.dialog = None

    def _define_qt_variables(self):
        pass

    def _create_connections(self):
        self.viewer_tabs.geometry_widget.selection_changed.connect(self.selection_changed_callback)
        self.clip_plane.slider_pressed.connect(self.slider_pressed_callback)
        self.clip_plane.value_changed.connect(self.slider_moved_callback)
        self.clip_plane.slider_released.connect(self.slider_released_callback)
        self.clip_plane.closed.connect(self.disable_cut)

    def set_mesh_selection(self, *, nodes=None, faces=None, solids=None, join=False, remove=True):
        if nodes is None:
            nodes = set()

        if faces is None:
            faces = set()

        if solids is None:
            solids = set()

        if join and remove:
            self.selected_mesh_nodes ^= set(nodes)
            self.selected_mesh_faces ^= set(faces)
            self.selected_mesh_solids ^= set(solids)
        elif join:
            self.selected_mesh_nodes |= set(nodes)
            self.selected_mesh_faces |= set(faces)
            self.selected_mesh_solids |= set(solids)
        elif remove:
            self.selected_mesh_nodes -= set(nodes)
            self.selected_mesh_faces -= set(faces)
            self.selected_mesh_solids -= set(solids)
        else:
            self.selected_mesh_nodes = set(nodes)
            self.selected_mesh_faces = set(faces)
            self.selected_mesh_solids = set(solids)

            # Clear the other type of selection
            self.selected_geometry_points.clear()
            self.selected_geometry_lines.clear()
            self.selected_geometry_surfaces.clear()
            self.selected_geometry_volumes.clear()

        self.selection_changed.emit()

    def set_geometry_selection(self, *, nodes=None, lines=None, surfaces=None, volumes=None, join=False, remove=True):
        if nodes is None:
            nodes = set()
        
        if lines is None:
            lines = set()

        if surfaces is None:
            surfaces = set()

        if volumes is None:
            volumes = set()

        # Select all the elements in mesh associated 
        # with the selected geometry
        mesh = self.project.model.mesh
        mesh_faces = []
        for surface in surfaces:
            mesh_faces.extend(mesh.elements_from_surface.get(surface, []))
        self.set_mesh_selection(faces=mesh_faces, join=join, remove=remove)

        if join and remove:
            self.selected_geometry_points ^= set(nodes)
            self.selected_geometry_lines ^= set(lines)
            self.selected_geometry_surfaces ^= set(surfaces)
            self.selected_geometry_volumes ^= set(volumes)
        elif join:
            self.selected_geometry_points |= set(nodes)
            self.selected_geometry_lines |= set(lines)
            self.selected_geometry_surfaces |= set(surfaces)
            self.selected_geometry_volumes |= set(volumes)
        elif remove:
            self.selected_geometry_points -= set(nodes)
            self.selected_geometry_lines -= set(lines)
            self.selected_geometry_surfaces -= set(surfaces)
            self.selected_geometry_volumes -= set(volumes)
        else:
            self.selected_geometry_points = set(nodes)
            self.selected_geometry_lines = set(lines)
            self.selected_geometry_surfaces = set(surfaces)
            self.selected_geometry_volumes = set(volumes)

        self.selection_changed.emit()

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
        self.status_bar = StatusBar(self)

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
        self.viewer_tabs = ViewerTabs(self)
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

    def create_temporary_vibra_folder(self):
        user_path = os.path.expanduser("~")
        self.project_folder_path = Path(user_path) / "temp_vibra"
        self.project_path = str(self.project_folder_path / "tmp.vibra")
        create_new_folder(user_path, "temp_vibra")

    def reset_temporary_vibra_folder(self):
        user_path = os.path.expanduser("~")
        project_folder_path = Path(user_path) / "temp_vibra"
        if os.path.exists(project_folder_path):
            for filename in os.listdir(project_folder_path).copy():
                file_path = project_folder_path / filename
                if os.path.exists(file_path):
                    if "." in filename:
                        os.remove(file_path)
                    else:
                        rmtree(file_path)

    def is_temporary_vibra_folder_empty(self):
        user_path = os.path.expanduser("~")
        project_folder_path = Path(user_path) / "temp_vibra"
        if os.path.exists(project_folder_path):
            if os.listdir(project_folder_path):
                self.project_path = str(project_folder_path / "tmp.vibra")
                return False
        return True
    
    def new_project_dialog(self):
        if not self.is_temporary_vibra_folder_empty():

            caption = "The recovery project data has been detected in the application backup files. "
            caption += "Would you like to try to recover the last project files?"

            close = QMessageBox.question(   
                                            self, 
                                            "Project recovery", 
                                            caption, 
                                            QMessageBox.Yes | QMessageBox.No
                                        )

            if close == QMessageBox.Yes:
                self.project = Project()
                self.file = ProjectFileIO(self.project_path, override=False)
                self.open_project()

            else:
                self.reset_temporary_vibra_folder()
                self.import_geometry_dialog()

        else:
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

        last_path = app().config.get_last_folder_for("project folder")
        if last_path is None:
            path = os.path.expanduser("~")
        else:
            path = last_path

        self.project_path, check = QFileDialog.getOpenFileName( 
                                                                self, 
                                                                "Open Project", 
                                                                path, 
                                                                filter = "Vibra File (*.vibra)"
                                                                )

        if not check:
            return

        app().config.write_last_folder_path_in_file("project folder", self.project_path)

        self.project = Project()
        self.file = ProjectFileIO(self.project_path, override=False)

        self.open_project()

    def import_geometry_dialog(self):

        last_path = app().config.get_last_folder_for("geometry folder")
        if last_path is None:
            path = os.path.expanduser("~")
        else:
            path = last_path

        geometry_path, check = QFileDialog.getOpenFileName(
                                                            self,
                                                            "Select Geometry",
                                                            path,
                                                            filter = "Geometry Files (*.stp *.step *.igs *.iges)",
                                                            )

        if not check:
            return

        app().config.write_last_folder_path_in_file("geometry folder", geometry_path)

        self.project = Project()
        self.create_temporary_vibra_folder()

        self.file = ProjectFileIO(self.project_path)
        self.file.write_geometry_in_file(geometry_path)
        geometry_paths = self.file.read_geometry_from_file()

        self.import_geometry(geometry_paths)

    def save_project_as(self, path):
        path = Path(path)
        self.project.name = path.stem
        self.project.save(path)
        self.user_config.save()  # why not

    def export_mesh(self):
        ExportMeshData()

    def open_project(self):

        self.load_project = LoadProject()
        self.load_project.load()

        # self.project.load()
        # self.user_config.add_recent_file(path)

        self.viewer_tabs.close_mesh_tabs()
        self.viewer_tabs.show_geometry()
        self.viewer_tabs.show_mesh()

    def import_geometry(self, paths):
        # Slow function running with loading bar
        import_geometry = load_function(self.project.import_geometry, self)
        import_geometry(paths)

        self.viewer_tabs.reset_tab_visibility()
        self.viewer_tabs.show_geometry()

        self.renderer_toolbar.setDisabled(False)
        self.analysis_filter.setDisabled(False)
        self.menu_widget.modify_items_access_after_geometry_importing()

        self.project.reset_solutions()
        self.project.model.properties._reset_variables()

    def close_app(self):

        self.close_dialogs()
        close = QMessageBox.question(
            self, "QUIT", "Are you sure want to close Vibra?", QMessageBox.Yes | QMessageBox.No
        )

        if close == QMessageBox.Yes:
            self.user_config.save()
            self.reset_temporary_vibra_folder()
            sys.exit()

    def set_input_widget(self, dialog):
        self.dialog = dialog

    def close_dialogs(self):
        if isinstance(self.dialog, (QDialog, QWidget)):
            self.dialog.close()

def create_new_folder(path, folder_name):
    folder_path = os.path.join(path, folder_name)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return folder_path

def create_new_folder(path, folder_name):
    folder_path = os.path.join(path, folder_name)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return folder_path