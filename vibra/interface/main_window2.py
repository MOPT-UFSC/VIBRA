from pathlib import Path
from vibra import UI_DIR

import qdarktheme
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from PyQt5 import uic

from vibra.interface.exception_message import ErrorMessage
from vibra.interface.loading_bar import load_function
from vibra.utils.icons import load_icon
from vibra.interface.clip_plane_widget import ClipPlaneWidget
from vibra.project import Project
from vibra.interface.viewer_tabs import ViewerTabs
from vibra.config import UserConfig
from vibra.interface.analysis_filter_menu import AnalysisFilter
from vibra.interface.status_bar import StatusBar
from vibra.interface.menu_items import MenuItems
from vibra.interface.data_handler.export_mesh_data import ExportMeshData
from vibra.interface.set_fluid_widget import FluidWidget
from vibra.interface.material_widget import MaterialWidget
from vibra.interface.mesh.mesher_inputs import MesherInputs
from vibra.interface.viewer_3d.render_widgets.common_render_widget import (
    CommonRenderWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        ui_path = UI_DIR / 'main_window.ui'
        uic.loadUi(ui_path, self)

        self.project = Project()
        self.user_config = UserConfig.load()
        self.viewer_tabs = ViewerTabs(self, self.project, self.user_config)
        self.status_bar = StatusBar(self)
        self.menu_items = MenuItems()
        self.analysis_filter = AnalysisFilter()  #ANDRE

        self.configure_window()

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
    
    def create_connections(self):
        pass
    
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
    
    def _config_window(self):
        self.setMinimumSize(1300, 700)
        self.showMaximized()
        self.setWindowIcon(load_icon(Path("data/icons/logo_vibra.png"), QColor("#448cff")))
        self.setWindowTitle("Vibra")
        self.splitter.addWidget(self.viewer_tabs)
        self.splitter.setSizes([100, 400])
        self.setStatusBar(self.status_bar)
        self.stacked_setup.addWidget(self.menu_items)
        self.stacked_setup.setCurrentWidget(self.menu_items)
        self.dialog = None  #ANDRE

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

    def load_user_preferences(self):
        self.set_theme(self.user_config.theme)

    def configure_window(self):
        self._config_window()
        self._connect_actions()
        self.load_user_preferences()
    
    def closeEvent(self, event):
        self.close_app()
        event.ignore()
    
    def update_geometry_information(self):
        self.status_bar.update_geometry_information()
    
    def update_mesh_information(self, nodes, face_elements, solid_elements):
        self.status_bar.update_mesh_information(nodes, face_elements, solid_elements)
    
    def action_clip_plane_callback(self):
        print("Oi")
        self.clip_plane = ClipPlaneWidget(self)

        self.clip_plane.slider_pressed.connect(self.slider_pressed_callback)
        self.clip_plane.value_changed.connect(self.slider_moved_callback)
        self.clip_plane.slider_released.connect(self.slider_released_callback)
        self.clip_plane.closed.connect(self.disable_cut)
    
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
    
    def action_theme_callback(self):
        color = QColor("#448cff")

        self.new_project_icon = load_icon(Path("data/icons/new_file.png"), color)
        self.theme_sun_icon = load_icon(Path("data/icons/sun_icon.png"), color)
        self.theme_moon_icon = load_icon(Path("data/icons/moon_icon.png"), color)

        if self.user_config.theme == "light":
            self.set_theme("dark")
            self.action_theme.setIcon(self.theme_sun_icon)

        elif self.user_config.theme == "dark":
            self.set_theme("light")
            self.action_theme.setIcon(self.theme_moon_icon)
    
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
            self, "Open Project", filter="Vibra File (*.vibra)"
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
    
    def save_project_as(self, path):
        path = Path(path)
        self.project.name = path.stem
        self.project.save(path)
        self.user_config.save()  # why not
    
    def action_save_as_callback(self):
        self.save_project_as_dialog()

    def new_project_dialog(self):
        self.project = Project()
        self.import_geometry_dialog()
    
    def action_import_geometry_callback(self):
        self.import_geometry_dialog()

    def import_geometry_dialog(self):
        path, check = QFileDialog.getOpenFileName(
            self,
            "Select Geometry",
            filter="Geometry Files (*.stp *.step *.iges)",
        )

        if not check:
            return

        self.import_geometry(path)
    
    def import_geometry(self, path):
        # Slow function running with loading bar
        import_geometry = load_function(self.project.import_geometry, self)
        import_geometry(path)

        self.viewer_tabs.close_mesh_tabs()
        self.viewer_tabs.show_geometry()

        self.tool_bar.setDisabled(False)
        #self.analysis_filter.setDisabled(False)  don't know where it is
        self.menu_items.modify_items_access_after_geometry_importing()

    
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
    
    def action_set_fluid_callback(self):
        FluidWidget()
    
    def action_set_material_callback(self):
        MaterialWidget()
    
    def action_mesher_setup_callback(self):
        mesher = MesherInputs()
        if mesher.complete:
            self.project.set_mesh_setup(mesher.mesh_setup)
            #self.generate_mesh_action.setDisabled(False)
            self.menu_items.item_child_generate_mesh.setDisabled(False)

    def action_face_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_faces()
    
    def action_face_view_2_callback(self):
        self.action_face_view_callback()
    
    def action_line_view_callback(self):
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_lines()
        
    def action_line_view_2_callback(self):
        self.action_line_view_callback()
    
    def action_node_view_callback(self):  #ANDRE
        widget = self.viewer_tabs.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.show_points()
    
    def action_node_view_2_callback(self):
        self.action_node_view_callback()
    
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
        close = QMessageBox.question(
            self, "QUIT", "Are you sure want to close Vibra?", QMessageBox.Yes | QMessageBox.No
        )

        if close == QMessageBox.Yes:
            self.user_config.save()
            exit()