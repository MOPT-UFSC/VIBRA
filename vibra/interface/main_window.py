from PyQt5.QtWidgets import QDialog, QFileDialog, QFrame, QGridLayout, QMainWindow, QMessageBox, QAction, QMenu, QStackedWidget, QToolBar, QSplitter, QAbstractButton, QComboBox
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

from vibra import *
# from vibra.config import UserConfig
from vibra.interface.analysis_filter_menu import AnalysisFilter
from vibra.interface.section_plane_widget import SectionPlaneWidget
from vibra.interface.data_handler.export_mesh_data import ExportMeshData
from vibra.interface.exception_message import ErrorMessage
from vibra.interface.loading_bar import load_function
from vibra.interface.menu_items import MenuItems
from vibra.interface.menus.help_menu import HelpMenu
from vibra.interface.menus.mesher_menu import MesherMenu
from vibra.interface.menus.project_menu import ProjectMenu
from vibra.interface.menus.settings_menu import VisibilitySettingsMenu
from vibra.interface.menus.view_mode_menu import ViewModeMenu
from vibra.interface.menus.advanced_results_menu import AdvancedResultsMenu
from vibra.interface.menus.views_menu import ViewsMenu
from vibra.interface.project.save_project_data_selector import SaveProjectDataSelector
from vibra.interface.renderer_toolbar import RendererToolbar
from vibra.interface.status_bar import StatusBar
from vibra.interface.viewer_tabs import ViewerTabs
from vibra.interface.formatters.icons import *
from vibra.interface.general.print_message_input import PrintMessageInput
from molde.render_widgets import CommonRenderWidget

from vibra.utils.progress_status import ProgressStatus
from vibra.utils.icons import load_icon

from vibra.project_files.load_project import LoadProject
from vibra.project_files.project import Project
from vibra.project_files.project_file import ProjectFile

import qdarktheme

import sys
import logging
from pathlib import Path
from shutil import rmtree, copy
from time import sleep, time


class MainWindow(QMainWindow):
    theme_changed = pyqtSignal(str)
    visualization_changed = pyqtSignal()
    selection_changed = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        ui_path = UI_DIR / 'main_window.ui'
        uic.loadUi(ui_path, self)

        self.selected_mesh_nodes = set()
        self.selected_mesh_faces = set()
        self.selected_mesh_solids = set()
        self.selected_geometry_points = set()
        self.selected_geometry_lines = set()
        self.selected_geometry_surfaces = set()
        self.selected_geometry_volumes = set()

        self.hidden_mesh_faces = set()
        self.hidden_mesh_solids = set()
        
        self.hidden_surfaces = set()
        self.hidden_volumes = set()

        self.dialog = None

        self._initialize()

    def _initialize(self):
        self.dialog = None
        self.project_data_modified = False
        self.user_path = Path().home()

    def _define_qt_variables(self):
        '''
        This function is doing nothing. Every variable was
        already defined in the UI file.

        Despite that, it is nice to list the variables to
        help future maintainers and the code editor with
        type inference.
        '''
        
        # QAction
        self.action_new_project: QAction
        self.action_open_project: QAction
        self.action_reset_project: QAction
        self.action_top_view: QAction
        self.action_bottom_view: QAction
        self.action_right_view: QAction
        self.action_left_view: QAction
        self.action_front_view: QAction
        self.action_back_view: QAction
        self.action_isometric_view: QAction
        self.action_node_view: QAction
        self.action_line_view: QAction
        self.action_face_view: QAction
        self.action_clip_plane: QAction
        self.action_zoom_to_fit: QAction
        self.action_action_symbols: QAction
        self.action_structural_workspace: QAction
        self.action_acoustic_workspace: QAction
        self.action_coupled_workspace: QAction

        #QSplitter
        self.splitter: QSplitter

        #QStacked
        self.stacked_setup: QStackedWidget

        # QMenu
        self.menu_project: QMenu
        self.menu_settings: QMenu
        self.menu_model_setup: QMenu
        self.menu_view_mode: QMenu
        self.menu_help: QMenu

        # QToolBar
        self.tool_bar: QToolBar
    
    def _connect_actions(self):
        '''
        Instead of connecting every action manually, one by one,
        this function loops through every action and connects it
        to a function ending with "_callback".

        For example an action named "action_new" will be connected to 
        the function named "action_new_callback" if it exists.
        '''
        for action in self.findChildren(QAction):
            function_name = action.objectName() + "_callback"
            function_exists = hasattr(self, function_name)
            if not function_exists:
                continue

            function = getattr(self, function_name)
            if callable(function):
                action.triggered.connect(function)

    def create_basic_layout(self):
        # self.unhide_all = QAction("Unhide All")
        # self.unhide_all.setShortcut("ctrl+shift+h")
        # self.unhide_all.triggered.connect(self.unhide_all_callback)
        # self.addAction(self.unhide_all)
        
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
        left_widget.setMinimumWidth(300)
        left_widget.setMaximumWidth(360)

        self.vertical_line = QFrame()
        self.vertical_line.setLineWidth(4)
        self.vertical_line.setFrameShape(QFrame.VLine)
        self.vertical_line.setFrameShadow(QFrame.Sunken)

        self.setCentralWidget(None)
        # self.create_menu_bar()
        # self.create_tool_bars()
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
    
    def _config_window(self):
        self.setMinimumSize(800, 600)
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
        # for qdarktheme
        self.custom_colors = {
            "[dark]": {
                "toolbar.background": "#202124",
            }
        }
    
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
        self.menu_items._configItems()

        if theme == "dark":
            icon_color = QColor("#5f9af4")
        elif theme == "light":
            icon_color = QColor("#1a73e8")

        widgets = self.findChildren((QAction, QAbstractButton))
        change_icon_color_for_widgets(widgets, icon_color)

    def load_user_preferences(self):
        self.set_theme(self.user_config.theme)
    
    def _load_render_widgets(self):
        self.viewer_tabs = ViewerTabs(self, self.project, self.user_config)

    def configure_window(self):
        self._config_window()
        self._connect_actions()
        self.load_user_preferences()
        self._create_workspaces_toolbar()
    
    def closeEvent(self, event):
        self.close_app()
        event.ignore()
    
    def config_tool_tip_appearance(self):
        tool_tip_style = "QToolTip { color: rgb(0, 0, 0); background-color: rgb(255, 255, 255) }"
        self.setStyleSheet(tool_tip_style)
    
    # def _create_workspaces_toolbar(self):
    #     actions = {
    #         Workspace.STRUCTURAL_SETUP: self.action_structural_workspace,
    #         Workspace.ACOUSTIC_SETUP: self.action_acoustic_workspace,
    #         Workspace.COUPLED: self.action_coupled_workspace
    #     }

    #     self.combo_box_workspaces = QComboBox()
    #     self.combo_box_workspaces.setMinimumSize(170, 26)

    #     # iterating sorted items make the icons appear in the same 
    #     # order as defined in the Workspace enumerator
    #     for _, action in sorted(actions.items()):
    #         self.combo_box_workspaces.addItem(action.text())

    #     self.combo_box_workspaces.currentIndexChanged.connect(self.update_combobox_indexes)
    #     self.combo_box_workspaces.currentIndexChanged.connect(lambda x: actions[x].trigger())
    #     self.tool_bar.addWidget(self.combo_box_workspaces)

    #     self.combo_box_workspaces.currentIndexChanged.connect(self.menu_items.filter_analysis_type)
    
    def update_combobox_indexes(self):
        pass
    
    def update_geometry_information(self):
        self.status_bar.update_geometry_information()
    
    def update_mesh_information(self, nodes, face_elements, solid_elements):
        self.status_bar.update_mesh_information(nodes, face_elements, solid_elements)
    
    def action_section_plane_callback(self):
        self.section_plane = SectionPlaneWidget(self)

    def _create_connections(self):
        self.viewer_tabs.geometry_widget.selection_changed.connect(self.selection_changed_callback)
        self.section_plane.slider_pressed.connect(self.slider_pressed_callback)
        self.section_plane.value_changed.connect(self.slider_moved_callback)
        self.section_plane.slider_released.connect(self.slider_released_callback)
        self.section_plane.closed.connect(self.disable_section_plane_visibility)

    def set_mesh_selection(self, *, nodes=None, faces=None, solids=None, join=False, remove=False):
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

    def set_geometry_selection(self, *, points=None, lines=None, surfaces=None, volumes=None, join=False, remove=False):
        s = time()
        if points is None:
            points = set()
        
        if lines is None:
            lines = set()

        if surfaces is None:
            surfaces = set()

        if volumes is None:
            volumes = set()

        mesh = app().project.model.mesh

        # Select the surfaces associated to the selected volumes
        for volume in volumes:
            volume_surfaces = mesh.surfaces_from_volumes.get(volume, [])
            surfaces |= set(volume_surfaces)

        # Select the mesh elements associated with the selected geometry
        # mesh_faces = []
        # mesh_solids = []
        # for surface in surfaces:
        #     mesh_faces.extend(mesh.elements_from_surface.get(surface, []))
        # for volume in volumes:
        #     mesh_solids.extend(mesh.elements_from_volume.get(volume, []))
        # self.set_mesh_selection(faces=mesh_faces, solids=mesh_solids, join=join, remove=remove)

        if join and remove:
            self.selected_geometry_points ^= set(points)
            self.selected_geometry_lines ^= set(lines)
            self.selected_geometry_surfaces ^= set(surfaces)
            self.selected_geometry_volumes ^= set(volumes)
        elif join:
            self.selected_geometry_points |= set(points)
            self.selected_geometry_lines |= set(lines)
            self.selected_geometry_surfaces |= set(surfaces)
            self.selected_geometry_volumes |= set(volumes)
        elif remove:
            self.selected_geometry_points -= set(points)
            self.selected_geometry_lines -= set(lines)
            self.selected_geometry_surfaces -= set(surfaces)
            self.selected_geometry_volumes -= set(volumes)
        else:
            self.selected_geometry_points = set(points)
            self.selected_geometry_lines = set(lines)
            self.selected_geometry_surfaces = set(surfaces)
            self.selected_geometry_volumes = set(volumes)

        self.selection_changed.emit()
        # print("COMBINING SELECTION", time() - s)

    def selection_changed_callback(self, points, lines, faces, volumes):
        self.status_bar.set_selection(points, lines, faces, volumes)

    def update_mesh_information(self, nodes, face_elements, solid_elements):
        self.status_bar.update_mesh_information(nodes, face_elements, solid_elements)

    def update_geometry_information(self, geometry_info: dict):
        self.status_bar.update_geometry_information(geometry_info)

    def show_hide_section_plane_callback(self, option):
        if option:
            self.viewer_tabs.start_cutting_mode()
        else:
            self.viewer_tabs.stop_cutting_mode()

    def show_config_section_plane(self):
        pass

    def slider_pressed_callback(self):
        self.viewer_tabs.start_cutting_mode()

    def slider_moved_callback(self):
        position = self.section_plane.get_position("sliders")
        orientation = self.section_plane.get_rotation("sliders")
        self.viewer_tabs.configure_cutting_plane(position, orientation)

    def slider_released_callback(self):
        position = self.section_plane.get_position("sliders")
        orientation = self.section_plane.get_rotation("sliders")
        self.viewer_tabs.apply_cutting_plane(position, orientation, self.section_plane.invert_value)

    def disable_cut(self):
        self.viewer_tabs.stop_cutting_mode()
    
    def action_theme_callback(self):
        color = QColor("#448cff")

        self.new_project_icon = load_icon(Path("data/icons/new_file.png"), color)
        self.theme_sun_icon = load_icon(Path("data/icons/sun_icon.png"), color)
        self.theme_moon_icon = load_icon(Path("data/icons/moon_icon.png"), color)

    def disable_section_plane_visibility(self):
        for tab in self.viewer_tabs.tabs():
            if hasattr(tab, "plane_actor") and tab.plane_actor is not None:
                tab.plane_actor.VisibilityOff()
    
    def action_show_menu_items_callback(self):
        visible = self.stacked_setup.isVisible()
        if visible:
            text = "Show menu items"
        else:
            text = "Hide menu items"

        self.set_menu_items_visibility_state(visible)
        self.action_show_menu_items.setText(text)
        self.stacked_setup.setVisible(not visible)

    def set_menu_items_visibility_state(self, state: bool):
        self.user_config.menu_items_visible = state
    
    def action_open_project_callback(self):
        self.open_project_dialog()
    
    def open_project_dialog(self):
        path, check = QFileDialog.getOpenFileName(
            self, "Open Project", filter="Vibra File (*.vibra)")

    def hide_selection_callback(self):
        mesh = app().project.model.mesh

        volumes_to_hide = set()
        if self.selected_geometry_volumes:
            volumes_to_hide |= self.selected_geometry_volumes
        elif self.selected_geometry_surfaces:
            for surface in self.selected_geometry_surfaces:
                volumes_to_hide |= set(mesh.volume_from_surface[surface])
        elif self.selected_mesh_solids:
            for element in self.selected_mesh_solids:
                volumes_to_hide.add(mesh.volume_from_element[element])

        selected_volume_surfaces = set()
        visible_volume_surfaces = set()
        for volume, surfaces in mesh.surfaces_from_volumes.items():
            if volume in volumes_to_hide:
                selected_volume_surfaces |= set(surfaces)
            elif volume not in self.hidden_volumes:
                visible_volume_surfaces |= set(surfaces)
        surfaces_to_keep_visible = set.intersection(selected_volume_surfaces,
                                                    visible_volume_surfaces)

        self.hidden_volumes |= volumes_to_hide
        self.hidden_surfaces |= selected_volume_surfaces - surfaces_to_keep_visible
        self.viewer_tabs.update_hidden_plots()

        # Clear selection
        self.set_mesh_selection()
        self.set_geometry_selection()

    def unhide_all_callback(self):
        self.hidden_surfaces.clear()
        self.hidden_volumes.clear()
        self.viewer_tabs.update_hidden_plots()

    def create_status_bar(self):
        self.setStatusBar(self.status_bar)

    # def create_tool_bars(self):
    #     self.renderer_toolbar = RendererToolbar(self, self.viewer_tabs)
    #     self.addToolBar(self.renderer_toolbar)
    #     self.renderer_toolbar.setDisabled(True)
    #     self.analysis_filter.setDisabled(True)

    def config_tool_tip_appearance(self):
        tool_tip_style = "QToolTip { color: rgb(0, 0, 0); background-color: rgb(255, 255, 255) }"
        self.setStyleSheet(tool_tip_style)

    def _load_render_widgets(self):
        self.section_plane = SectionPlaneWidget(self)
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
        self.create_temporary_vibra_folder()

        app().splash.close()
        self.showMaximized()

        app().processEvents()

        if len(sys.argv) > 1:
            self.open_project(Path(sys.argv[1]))

        elif not self.is_temporary_vibra_folder_empty():
            self.recovery_dialog()

    def load_user_preferences(self):
        self.set_theme(app().user_config.theme)

    def get_user_config(self):
        return app().user_config

    # External functions that may be usefull
    def set_theme(self, theme: str):
        """
        Changes Qt stylesheets using qdarktheme library and the
        renderer background colors.

        The input is a string "light" or "dark".
        """
        qdarktheme.setup_theme(theme, custom_colors=self.custom_colors)
        app().user_config.theme = theme
        self.menu_widget._configItems()
        self.theme_changed.emit(theme)

    def set_menu_items_visibility_state(self, state: bool):
        app().user_config.menu_items_visible = state

    def capture_image(self):
        path, check = QFileDialog.getSaveFileName(
            self,
            "PNG",
            filter="PNG (*.png)",
        )

        if not check:
            return

        self.open_project(path)

    def open_project(self, path):
        path = Path(path)
        self.project = Project.load(path)
        # self.user_config.add_recent_file(path)

        self.viewer_tabs.close_mesh_tabs()
        self.viewer_tabs.show_geometry()
        self.viewer_tabs.show_mesh()
    
    def action_save_callback(self):
      self.save_project_dialog()

    def create_temporary_vibra_folder(self):
        create_new_folder(self.user_path, "temp_vibra")

    def reset_temporary_vibra_folder(self):
        if TEMP_PROJECT_DIR.exists():
            for filename in os.listdir(TEMP_PROJECT_DIR).copy():
                file_path = TEMP_PROJECT_DIR / filename
                if os.path.exists(file_path):
                    if "." in filename:
                        os.remove(file_path)
                    else:
                        rmtree(file_path)

    def is_temporary_vibra_folder_empty(self):
        if TEMP_PROJECT_DIR.exists():
            if os.listdir(TEMP_PROJECT_DIR):
                return False
        return True

    def recovery_dialog(self):

        caption = "The recovery project data has been detected in the application backup files. "
        caption += "Would you like to try to recover the last project files?"

        obj = QMessageBox.question(   
            self, 
            "Project recovery", 
            caption, 
            QMessageBox.Yes | QMessageBox.No
        )

        if obj == QMessageBox.Yes:
            self.open_project()
        else:
            self.reset_temporary_vibra_folder()

    def new_project_dialog(self):
        self.reset_temporary_vibra_folder()
        self.import_geometry_dialog()

    def save_project_dialog(self):
        if app().project.save_path is None:
            return self.save_project_as_dialog()
        else:
            self.save_project_as(app().project.save_path)
            return True

    def save_project_as_dialog(self):

        obj = SaveProjectDataSelector()
        if obj.complete:

            last_path = app().config.get_last_folder_for("project folder")
            if last_path is None:
                path = os.path.expanduser("~")
            else:
                path = last_path

            file_path, check = QFileDialog.getSaveFileName(
                                                            self,
                                                            "Save As",
                                                            path,
                                                            filter = "Vibra File (*.vibra)",
                                                        )

            if not check:
                return

            if obj.ignore_results_data:
                app().file.remove_results_data_from_project_file()
            
            if obj.ignore_mesh_data:
                app().file.remove_mesh_data_from_project_file()

            self.save_project_as(file_path)

        return obj.complete

    def save_project_as(self, path):

        def save_data(path):
            path = Path(path)
            app().project.name = path.stem
            app().project.save_path = path
            app().file.write_thumbnail()
            app().config.add_recent_file(path)
            logging.info("Saving project data..." + ProgressStatus(10, 100))

            app().config.write_last_folder_path_in_file("project folder", path)
            self.project_menu.update_recents_menu()
            logging.info("Saving project data..." + ProgressStatus(60, 100))
            
            copy(TEMP_PROJECT_FILE, path)
            self.update_window_title(path)
            self.project_data_modified = False
            logging.info("The project data has been saved." + ProgressStatus(100, 100))

        save_func = load_function(save_data, self)
        save_func(path)

        from datetime import datetime
        message = f"The project data has been saved @{datetime.now()}"
        print(message)

    def open_project_dialog(self):

        last_path = app().config.get_last_folder_for("project folder")
        if last_path is None:
            path = os.path.expanduser("~")
        else:
            path = last_path

        project_path, check = QFileDialog.getOpenFileName( 
                                                            self, 
                                                            "Open Project", 
                                                            path, 
                                                            filter = "Vibra File (*.vibra)"
                                                         )

        if not check:
            return

        self.open_project(project_path)

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
            return False

        app().config.write_last_folder_path_in_file("geometry folder", geometry_path)

        app().project.reset_variables()
        app().project.reset_solutions()

        # self.file = ProjectFile(TEMP_PROJECT_FILE)
        app().file.write_geometry_in_file(geometry_path)

        def remove_callback():
            logging.info("Removing the model properties from project file..." + ProgressStatus(10, 100))
            app().file.remove_model_properties_from_project_file()
            
            logging.info("Removing the mesh data from project file..." + ProgressStatus(40, 100))
            app().file.remove_mesh_data_from_project_file()

            logging.info("Removing the results data from project file..." + ProgressStatus(75, 100))
            app().file.remove_results_data_from_project_file()

        remove = load_function(remove_callback, self)
        remove()

        _geometry_path = app().file.read_geometry_from_file()
        self.import_geometry(_geometry_path)

        return True

    def export_mesh(self):
        ExportMeshData()

    def update_window_title(self, project_path : str | Path):
        if isinstance(project_path, str):
            project_path = Path(project_path)
        project_name = project_path.stem
        self.setWindowTitle(f"{project_name}")

    def open_project(self, project_path: str | Path | None = None):
        '''
        This function loads a new project in a temporary folder.
        If you pass a valid vibra file to this function, it will first copy 
        the file to a temporary folder and then load it.
        '''

        if project_path is not None:
            app().config.add_recent_file(project_path)
            app().config.write_last_folder_path_in_file("project folder", project_path)
            self.project_menu.update_recents_menu()
            copy(project_path, TEMP_PROJECT_FILE)
            self.update_window_title(project_path)

        app().project.reset_variables()
        app().project.reset_solutions()

        # self.file = ProjectFile(TEMP_PROJECT_FILE, override=False)

        if project_path is not None:
            path = Path(project_path)
            app().project.name = path.stem
            app().project.save_path = path

        # self.load_project = LoadProject()
        app().load_project.initialize()
        load = load_function(app().load_project.load, self)
        load()

    def import_geometry(self, path : str):

        import_geometry = load_function(app().project.import_geometry, self)
        if import_geometry(path) == -1:
            return

        try:

            self.viewer_tabs.reset_tab_visibility()
            self.viewer_tabs.show_geometry()

            self.renderer_toolbar.setDisabled(False)
            self.analysis_filter.setDisabled(False)
            self.menu_widget.modify_items_access_after_geometry_importing()

            app().project.reset_solutions()
            app().project.model.properties._reset_variables()

        except Exception as error_log:
            window_title = "Error"
            title = "Error while processing geometry"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])

    def closeEvent(self, event):
        self.close_app()
        event.ignore()

    
    def action_export_mesh_callback(self):
        self.export_mesh()
    
    def export_mesh(self):
        ExportMeshData()
    
    def set_input_widget(self, dialog):
        self.dialog = dialog

    def action_capture_image_callback(self):
        self.capture_image()
    
    def capture_image(self):
        path, check = QFileDialog.getSaveFileName(
            self,
            "PNG",
            filter="PNG (*.png)",
        )

        if not check:
            return

        # self.viewer_3d.save_png(path)
    
    def action_exit_callback(self):
        loaded_solve = load_function(self.solve_example_analysis_callback, self)
        loaded_solve()

    def solve_example_analysis_callback(self):
        try:
            self.project.solve_modal_acoustic()
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            self.viewer_tabs.show_acoustic_modal_analysis()
    
    # def action_set_fluid_callback(self):
    #     FluidWidget()
    
    # def action_set_material_callback(self):
    #     MaterialWidget()
    
    # def action_mesher_setup_callback(self):
    #     mesher = MesherInputs()
    #     if mesher.complete:
    #         self.project.set_mesh_setup(mesher.mesh_setup)
    #         #self.generate_mesh_action.setDisabled(False)
    #         self.menu_items.item_child_generate_mesh.setDisabled(False)

    def action_face_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_faces()
    
    def action_line_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_lines()
    
    def action_node_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_points()
    
    def action_about_vibra_callback(self):
        self.viewer_tabs.show_help()
    
    def action_top_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_top_view()
    
    def action_bottom_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_bottom_view()
    
    def action_right_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_right_view()
        
    def action_left_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_left_view()
        
    def action_front_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_front_view()
        
    def action_back_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_back_view()
        
    def action_isometric_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_isometric_view()

    def action_zoom_to_fit_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.renderer.ResetCamera()
            widget.update()
        
    def close_app(self):

        self.close_dialogs()

        condition_1 = app().project.save_path is None
        condition_2 = os.path.exists(TEMP_PROJECT_FILE)
        condition_3 = self.project_data_modified
        condition = (condition_1 and condition_2) or condition_3

        if condition:
            close = QMessageBox.question(   
                                            self, 
                                            "QUIT", 
                                            "Would you like to save the project data before exit?", 
                                            QMessageBox.Cancel | QMessageBox.Discard | QMessageBox.Save
                                        )

            if close == QMessageBox.Cancel:
                return

            elif close == QMessageBox.Save:
                if not self.save_project_dialog():
                    return

        else:
            close = QMessageBox.question(
                                            self, 
                                            "QUIT", 
                                            "Would you like to close the application?", 
                                            QMessageBox.Yes | QMessageBox.No
                                        )

            if close == QMessageBox.No:
                return

        app().user_config.save()
        self.reset_temporary_vibra_folder()
        sys.exit()

    def set_input_widget(self, dialog):
        self.dialog = dialog

    def close_dialogs(self):
        if isinstance(self.dialog, (QDialog, QWidget)):
            self.dialog.close()

def create_new_folder(path : Path, folder_name : str) -> Path:
    folder_path = path / folder_name
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return folder_path
