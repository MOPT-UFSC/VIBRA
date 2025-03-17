import logging
import os
import sys
from pathlib import Path
from shutil import copy, rmtree
from time import time

from PySide6.QtWidgets import (
     QAbstractButton,
     QDialog,
     QFileDialog, QFrame,
     QGridLayout, 
     QMainWindow, 
     QMenu,
     QMessageBox,
     QSplitter,
     QStackedWidget,
     QToolBar,
     QWidget,
)
from PySide6.QtGui import QAction, QColor
from PySide6.QtCore import Signal

from vibra import UI_DIR, ICON_DIR, TEMP_PROJECT_DIR, TEMP_PROJECT_FILE, app
from vibra.interface.analysis_toolbar import AnalysisToolbar
from vibra.interface.animation_toolbar import AnimationToolbar
from vibra.interface.data_handler.export_mesh_data import ExportMeshData
from vibra.interface.formatters.icons import get_vibra_icon, change_icon_color_for_widgets
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.help_widget import HelpWidget
from vibra.interface.loading_bar import load_function
from vibra.interface.menus.model_setup_widget import ModelSetupWidget
from vibra.interface.menus.results_viewer_widget import ResultsViewerWidget
from vibra.interface.user_input.input_ui import InputUi
from vibra.interface.exception_message import ErrorMessage
from vibra.interface.plots.acoustic.export_element_transfer_data_input import (
    ExportElementTransferDataInput,
)
from vibra.interface.plots.acoustic.plot_particle_velocity_frequency_response_input import (
    PlotParticleVelocityFrequencyResponseInput,
)
from vibra.interface.plots.acoustic.plot_specific_acoustic_impedance_input import (
    PlotSpecificAcousticImpedanceInput,
)
from vibra.interface.project.save_project_data_selector import SaveProjectDataSelector

# from vibra.config import UserConfig
from vibra.interface.section_plane_widget import SectionPlaneWidget
from vibra.interface.status_bar import StatusBar
from vibra.interface.viewer_3d.render_widgets.acoustic_harmonic_analysis_render_widget import (
    AcousticHarmonicAnalysisRenderWidget,
)
from vibra.interface.viewer_3d.render_widgets.acoustic_modal_analysis_render_widget import (
    AcousticModalAnalysisRenderWidget,
)
from vibra.interface.viewer_3d.render_widgets.geometry_render_widget import GeometryRenderWidget
from vibra.interface.viewer_3d.render_widgets.mesh_render_widget import MeshRenderWidget
from vibra.interface.viewer_3d.render_widgets.structural_harmonic_analysis_render_widget import (
    StructuralHarmonicAnalysisRenderWidget,
)
from vibra.interface.viewer_3d.render_widgets.structural_modal_analysis_render_widget import (
    StructuralModalAnalysisRenderWidget,
)
from vibra.interface.welcome_widget import WelcomeWidget
from vibra.utils.icons import load_icon
from vibra.utils.interface_utils import VisualizationFilter
from vibra.utils.progress_status import ProgressStatus
from vibra.interface.user_input.render_user_preferences import RendererUserPreferencesInput

from molde.render_widgets import CommonRenderWidget
from molde import stylesheets
from molde import load_ui


class MainWindow(QMainWindow):
    theme_changed = Signal(str)
    visualization_changed = Signal()
    render_widget_changed = Signal()
    selection_changed = Signal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        ui_path = UI_DIR / 'main_window.ui'
        load_ui(ui_path, self, UI_DIR)
        
        self.visualization_filter = VisualizationFilter.all_true()

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

        self.show_menu_items = True
        self.last_render_index = None

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
        self.action_save: QAction
        self.action_save_as: QAction
        self.action_export_mesh: QAction
        self.action_top_view: QAction
        self.action_capture_image: QAction
        self.action_theme: QAction
        self.action_exit: QAction
        self.action_bottom_view: QAction
        self.action_right_view: QAction
        self.action_left_view: QAction
        self.action_front_view: QAction
        self.action_back_view: QAction
        self.action_isometric_view: QAction
        self.action_zoom_to_fit: QAction
        self.action_node_view: QAction
        self.action_line_view: QAction
        self.action_face_view: QAction
        self.action_hide_show_symbols: QAction
        self.action_section_plane: QAction
        self.action_plot_particle_velocity: QAction
        self.action_plot_specific_acoustic_impedance: QAction
        self.action_export_element_transfer_data: QAction
        self.action_model_workspace: QAction
        self.action_mesh_workspace: QAction
        self.action_results_workspace: QAction

        #QSplitter
        self.splitter: QSplitter

        # QMenu
        self.menu_project: QMenu
        self.menu_settings: QMenu
        self.menu_view_mode: QMenu
        self.menu_advanced_results: QMenu
        self.menu_help: QMenu

        # QToolBar
        self.renderer_toolbar: QToolBar
        self.animation_toolbar: QToolBar

        # QStackedWidget
        self.stacked_setup: QStackedWidget
        self.render_widgets_stack: QStackedWidget

        # QSplitter
        self.splitter : QSplitter
    
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
        self.status_bar = StatusBar(self)
        self.analysis_toolbar = AnalysisToolbar()
        self.animation_toolbar = AnimationToolbar()

        self.create_recents_menu()
        self.create_status_bar()

        self.render_widgets_stack.addWidget(self.geometry_widget)
        self.render_widgets_stack.addWidget(self.mesh_widget)
        self.render_widgets_stack.addWidget(self.structural_modal_analysis)
        self.render_widgets_stack.addWidget(self.structural_harmonic_analysis)
        self.render_widgets_stack.addWidget(self.acoustic_modal_analysis)
        self.render_widgets_stack.addWidget(self.acoustic_harmonic_analysis)
        self.render_widgets_stack.addWidget(self.help_widget)
        self.render_widgets_stack.addWidget(self.welcome_widget)
        self.render_widgets_stack.currentChanged.connect(self.render_changed_callback)

        self.stacked_setup.addWidget(self.model_setup_widget)
        self.stacked_setup.addWidget(self.results_viewer_widget)

        self.addToolBar(self.analysis_toolbar)
        self.insertToolBarBreak(self.analysis_toolbar)
        self.addToolBar(self.animation_toolbar)
        self.insertToolBarBreak(self.animation_toolbar)

        self.analysis_toolbar.setDisabled(True)
        self.renderer_toolbar.setDisabled(True)
        self.animation_toolbar.setDisabled(True)
        self.disable_advanced_acoustic_plots_buttons(True)

        self.splitter.setSizes([100, 400])
        self.splitter.widget(0).setMinimumWidth(360)
    
    def _config_window(self):
        self.setMinimumSize(800, 600)
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

    def configure_main_window(self):

        app().splash.update_progress(10)
        self.configure_window()

        app().splash.update_progress(30)
        self._load_menu_widgets()
        self._load_render_widgets()

        app().splash.update_progress(60)
        self._define_qt_variables()
        self.create_basic_layout()
        self._configure_render_widgets_stack()
        self._configure_stacked_setup()

        app().splash.update_progress(90)
        self.load_user_preferences()
        self.config_tool_tip_appearance()
        self.create_temporary_vibra_folder()

        app().splash.close()
        self.showMaximized()

        app().processEvents()

        if len(sys.argv) > 1:
            path = Path(sys.argv[1])
            if path.exists():
                self.open_project(path)

        elif not self.is_temporary_vibra_folder_empty():
            self.recovery_dialog()
    
    # External functions that may be usefull
    def set_theme(self, theme: str):
        """
        Changes Qt stylesheets using qdarktheme library and the
        renderer background colors.

        The input is a string "light" or "dark".
        """
        # qdarktheme.setup_theme(theme, custom_colors=self.custom_colors)
        app().config.user_preferences.interface_theme = theme
        stylesheets.set_theme(theme)

        if theme == "dark":
            icon_color = QColor("#5f9af4")
        elif theme == "light":
            icon_color = QColor("#1a73e8")

        widgets_type = [QAction, QAbstractButton]
        widgets = list()
        for widget_type in widgets_type:
            widgets += self.findChildren(widget_type)
        change_icon_color_for_widgets(widgets, icon_color)
        
        self.theme_changed.emit(theme)

    def set_menus_theme(self, theme: str):
        for i in range(self.stacked_setup.count()):
            menu_widget = self.stacked_setup.widget(i)
            if hasattr(menu_widget, "get_item"):
                menu_widget_item = menu_widget.get_item()
                menu_widget_item.set_theme(theme)
    
    def set_renderers_theme(self, theme: str):
        for i in range(self.render_widgets_stack.count()):
            widget = self.render_widgets_stack.widget(i)
            if hasattr(widget, "set_theme"):
                widget.set_theme(theme)

    def configure_window(self):
        self._config_window()
        self._connect_actions()
    
    def closeEvent(self, event):
        self.close_app()
        event.ignore()
    
    def update_mesh_information(self, nodes, face_elements, solid_elements):
        self.status_bar.update_mesh_information(nodes, face_elements, solid_elements)

    def update_geometry_information(self, geometry_info: dict):
        self.status_bar.update_geometry_information(geometry_info)
    
    def _configure_render_widgets_stack(self):
        self.render_widgets_stack.setCurrentWidget(self.welcome_widget)
    
    def _configure_stacked_setup(self):
        self.stacked_setup.setCurrentWidget(self.model_setup_widget)

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

    def create_status_bar(self):
        self.setStatusBar(self.status_bar)

    def config_tool_tip_appearance(self):
        tool_tip_style = "QToolTip { color: rgb(0, 0, 0); background-color: rgb(255, 255, 255) }"
        self.setStyleSheet(tool_tip_style)

    def _load_render_widgets(self):
        self.section_plane = SectionPlaneWidget(self)
        self.geometry_widget = GeometryRenderWidget()
        self.mesh_widget = MeshRenderWidget()
        self.structural_modal_analysis = StructuralModalAnalysisRenderWidget()
        self.structural_harmonic_analysis = StructuralHarmonicAnalysisRenderWidget()
        self.acoustic_modal_analysis = AcousticModalAnalysisRenderWidget()
        self.acoustic_harmonic_analysis = AcousticHarmonicAnalysisRenderWidget()
        self.welcome_widget = WelcomeWidget()
        self.help_widget = HelpWidget()
    
    def _load_menu_widgets(self):
        self.results_viewer_widget = ResultsViewerWidget()
        self.model_setup_widget = ModelSetupWidget()
        self.input_ui = InputUi(self)

    def load_user_preferences(self):
        theme = app().config.user_preferences.interface_theme
        self.set_theme(theme)

        show = app().config.user_preferences.show_reference_scale_bar
        self.update_scale_bar(show)
        self.update_renderer_font_size()

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
    
    def create_recents_menu(self):
        color = QColor("#448cff") 
        self.recent_icon = load_icon(ICON_DIR / "recent.png", color)

        self.recents_menu = QMenu("Recent projects", self)
        self.recents_menu.setIcon(self.recent_icon)
        self.update_recents_menu()

        self.menu_project.insertMenu(self.action_save, self.recents_menu)
        self.menu_project.insertSeparator(self.action_save)
    
    def update_recents_menu(self):
        self.recents_menu.clear()
        recent_paths = app().config.get_recent_files()
        recent_paths[-8:]
        for path in reversed(recent_paths):
            self.recents_menu.addAction(QAction(str(path), self))
    
    def render_changed_callback(self, new_index):
        if self.last_render_index is None:
            self.last_render_index = new_index
            return

        new_widget = self.render_widgets_stack.widget(new_index)
        if isinstance(new_widget, CommonRenderWidget):
            last_widget = self.render_widgets_stack.widget(self.last_render_index)
            new_widget.copy_camera_from(last_widget)
            # if last_widget is not a valid render the operation will be ignored

        self.last_render_index = new_index

    def selection_changed_callback(self, points, lines, faces, volumes):
        self.status_bar.set_selection(points, lines, faces, volumes)

    def action_section_plane_callback(self):
        self.section_plane.show()
        self.action_section_plane.setChecked(True)
    
    def action_theme_callback(self):
        color = QColor("#448cff")

        self.theme_sun_icon = load_icon(Path(ICON_DIR / "sun_icon.png"), color)
        self.theme_moon_icon = load_icon(Path(ICON_DIR / "moon_icon.png"), color)

        if app().config.user_preferences.interface_theme == "light":
            app().config.user_preferences.set_dark_theme()
            self.set_theme("dark")
            self.action_theme.setIcon(self.theme_sun_icon)

        elif app().config.user_preferences.interface_theme == "dark":
            app().config.user_preferences.set_light_theme()
            self.set_theme("light")
            self.action_theme.setIcon(self.theme_moon_icon)
        
        app().config.update_config_file()
        
    def action_user_preferences_callback(self):
        self.render_user_preferences = RendererUserPreferencesInput()
    
    def configure_mesh_information(self):
        nodes, face_elements, solid_elements = app().project.model.mesh.get_mesh_info()
        self.update_mesh_information(nodes, face_elements, solid_elements)
    
    def configure_acoustic_modal_analysis_render_widget(self, show_renderer_widget=False):
        self.acoustic_modal_analysis.update_plot()
        
        if show_renderer_widget:
            self.stacked_setup.setCurrentWidget(self.results_viewer_widget)
            self.results_viewer_widget.hide_bottom_widget()

            self.render_widgets_stack.setCurrentWidget(self.geometry_widget)
            
            self.action_results_workspace.setEnabled(False)
            if not self.action_model_workspace.isEnabled():
                self.action_model_workspace.setEnabled(True)
            if not self.action_mesh_workspace.isEnabled():
                self.action_mesh_workspace.setEnabled(True)

            self.animation_toolbar.setDisabled(True)
    
    def configure_structural_modal_analysis_render_widget(self, show_render_widget=False):
        self.structural_modal_analysis.update_plot()

        if show_render_widget:
            self.stacked_setup.setCurrentWidget(self.results_viewer_widget)
            self.results_viewer_widget.hide_bottom_widget()

            self.render_widgets_stack.setCurrentWidget(self.geometry_widget)

            self.action_results_workspace.setEnabled(False)
            if not self.action_model_workspace.isEnabled():
                self.action_model_workspace.setEnabled(True)
            if not self.action_mesh_workspace.isEnabled():
                self.action_mesh_workspace.setEnabled(True)
            
            self.animation_toolbar.setDisabled(True)
            
    def configure_structural_harmonic_analysis_render_widget(self, show_render_widget=False):
        self.structural_harmonic_analysis.update_plot()

        if show_render_widget:
            self.stacked_setup.setCurrentWidget(self.results_viewer_widget)
            self.results_viewer_widget.hide_bottom_widget()

            self.render_widgets_stack.setCurrentWidget(self.geometry_widget)

            self.action_results_workspace.setEnabled(False)
            if not self.action_model_workspace.isEnabled():
                self.action_model_workspace.setEnabled(True)
            if not self.action_mesh_workspace.isEnabled():
                self.action_mesh_workspace.setEnabled(True)
            
            self.animation_toolbar.setDisabled(True)

    def configure_acoustic_harmonic_analysis_render_widget(self, show_render_widget=False):
        self.acoustic_harmonic_analysis.update_plot()

        if show_render_widget:
            self.stacked_setup.setCurrentWidget(self.results_viewer_widget)
            self.results_viewer_widget.hide_bottom_widget()
            
            self.render_widgets_stack.setCurrentWidget(self.geometry_widget)

            self.action_results_workspace.setEnabled(False)
            if not self.action_model_workspace.isEnabled():
                self.action_model_workspace.setEnabled(True)
            if not self.action_mesh_workspace.isEnabled():
                self.action_mesh_workspace.setEnabled(True)
            
            self.animation_toolbar.setDisabled(True)
            
    def show_geometry_render_widget(self):
        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)

    def show_mesh_render_widget(self):
        self.render_widgets_stack.setCurrentWidget(self.mesh_widget)
    
    def update_plots(self, reset_camera=True):
        for i in range(self.render_widgets_stack.count()):
            widget = self.render_widgets_stack.widget(i)
            if isinstance(widget, CommonRenderWidget):
                widget.update_plot(reset_camera)
    
    def update_info_text(self):
        for i in range(self.render_widgets_stack.count()):
            widget = self.render_widgets_stack.widget(i)
            if hasattr(widget, "update_info_text"):
                widget.update_info_text()
            
    def update_scale_bar(self, show=True):
        for i in range(self.render_widgets_stack.count()):
            widget = self.render_widgets_stack.widget(i)
            if hasattr(widget, "scale_bar_actor"):
                if show:
                    widget.enable_scale_bar()
                else:
                    widget.disable_scale_bar()
                
    def update_renderer_font_size(self):
        for i in range(self.render_widgets_stack.count()):
            widget = self.render_widgets_stack.widget(i)
            if hasattr(widget, "update_renderer_font_size"):
                widget.update_renderer_font_size()
        
    def action_model_workspace_callback(self):
        self.action_model_workspace.setEnabled(False)

        if not self.action_mesh_workspace.isEnabled():
            self.action_mesh_workspace.setEnabled(True)
        if not self.action_results_workspace.isEnabled():
            self.action_results_workspace.setEnabled(True)

        self.stacked_setup.setCurrentWidget(self.model_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)
        self.model_setup_widget.model_setup_items.modify_items_access_after_geometry_importing()

        self.animation_toolbar.setDisabled(True)
        self.animation_toolbar.pause_animation()
    
    def action_mesh_workspace_callback(self):
        self.action_mesh_workspace.setEnabled(False)

        if not self.action_model_workspace.isEnabled():
            self.action_model_workspace.setEnabled(True)
        if not self.action_results_workspace.isEnabled():
            self.action_results_workspace.setEnabled(True)

        self.stacked_setup.setCurrentWidget(self.model_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.mesh_widget)
        self.configure_mesh_information()
        self.model_setup_widget.model_setup_items.modify_items_access_after_geometry_importing()

        self.animation_toolbar.setDisabled(True)
        self.animation_toolbar.pause_animation()

    def action_results_workspace_callback(self):
        if app().project.last_analysis is not None:
            self.action_results_workspace.setEnabled(False)

            if not self.action_model_workspace.isEnabled():
                self.action_model_workspace.setEnabled(True)
            if not self.action_mesh_workspace.isEnabled():
                self.action_mesh_workspace.setEnabled(True)
            
            self.render_widgets_stack.setCurrentWidget(self.geometry_widget)

            self.stacked_setup.setCurrentWidget(self.results_viewer_widget)
            self.results_viewer_widget.results_viewer_items.update_items()
            self.analysis_toolbar.update_analysis_combo_boxes()

    def action_new_project_callback(self):
        self.new_project_dialog()
    
    def action_open_project_callback(self):
        self.open_project_dialog()

    def action_hide_selection_callback(self):
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
        self.update_hidden_plots()

        # Clear selection
        self.set_mesh_selection()
        self.set_geometry_selection()
    
    def action_unhide_all_callback(self):
        self.hidden_surfaces.clear()
        self.hidden_volumes.clear()
        self.update_hidden_plots()

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

        if not os.path.exists(TEMP_PROJECT_FILE):
            return

        obj = SaveProjectDataSelector()
        if obj.complete:

            last_path = app().config.get_last_folder_for("project_folder")
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

            app().config.write_last_folder_path_in_file("project_folder", path)
            self.update_recents_menu()
            logging.info("Saving project data..." + ProgressStatus(60, 100))
            
            copy(TEMP_PROJECT_FILE, path)
            self.update_window_title(path)
            self.project_data_modified = False
            logging.info("The project data has been saved." + ProgressStatus(100, 100))

        save_func = load_function(save_data, self)
        save_func(path)

        from datetime import datetime
        message = f"The project data has been saved: {datetime.now()}"
        print(message)

    def open_project_dialog(self):

        last_path = app().config.get_last_folder_for("project_folder")
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

        last_path = app().config.get_last_folder_for("geometry_folder")
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

        app().config.write_last_folder_path_in_file("geometry_folder", geometry_path)

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
            app().config.write_last_folder_path_in_file("project_folder", project_path)
            self.update_recents_menu()
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

            self.action_model_workspace_callback()

            self.renderer_toolbar.setDisabled(False)
            self.analysis_toolbar.setDisabled(False)
            self.analysis_toolbar.load_analysis_settings()

            app().project.reset_solutions()
            app().project.model.properties._reset_variables()
            self.update_plots()

        except Exception as error_log:
            window_title = "Error"
            title = "Error while processing geometry"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])
    
    def action_save_as_callback(self):
        self.save_project_as_dialog()
    
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
        self.close_app()
    
    def action_face_view_callback(self, clicked: bool):
        self.visualization_filter.faces = clicked
        self.visualization_filter.solids = clicked
        self.visualization_changed.emit()
    
    def action_line_view_callback(self, clicked: bool):
        self.visualization_filter.lines = clicked
        self.visualization_changed.emit()
    
    def action_node_view_callback(self, clicked: bool):
        self.visualization_filter.points = clicked
        self.visualization_changed.emit()
    
    def action_about_vibra_callback(self):
        self.render_widgets_stack.setCurrentWidget(self.help_widget)

        self.action_model_workspace.setDisabled(False)
        self.action_mesh_workspace.setDisabled(False)
        self.action_results_workspace.setDisabled(False)
    
    def action_top_view_callback(self):
        widget = self.render_widgets_stack.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_top_view()
    
    def action_bottom_view_callback(self):
        widget = self.render_widgets_stack.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_bottom_view()
    
    def action_right_view_callback(self):
        widget = self.render_widgets_stack.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_right_view()
        
    def action_left_view_callback(self):
        widget = self.render_widgets_stack.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_left_view()
        
    def action_front_view_callback(self):
        widget = self.render_widgets_stack.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_front_view()
        
    def action_back_view_callback(self):
        widget = self.render_widgets_stack.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_back_view()
        
    def action_isometric_view_callback(self):
        widget = self.render_widgets_stack.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.set_isometric_view()

    def action_zoom_to_fit_callback(self):
        widget = self.render_widgets_stack.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            widget.renderer.ResetCamera()
            widget.update()
    
    def action_hide_show_symbols_callback(self, clicked: bool):
        # TODO: test this function.
        #  OBS: I do not know if it is working because I do not have any symbols to check
        self.visualization_filter.acoustic_symbols = clicked
        self.visualization_filter.structural_symbols = clicked
        self.visualization_changed.emit()
        
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

        self.reset_temporary_vibra_folder()
        app().quit()

    def close_dialogs(self):
        if isinstance(self.dialog, (QDialog, QWidget)):
            self.dialog.close()
            self.dialog = None

    def action_plot_specific_acoustic_impedance_callback(self):
            if app().project.acoustic_harmonic_solver.solution is None:
                return
            PlotSpecificAcousticImpedanceInput()

    def action_plot_particle_velocity_callback(self):
        if app().project.acoustic_harmonic_solver.solution is None:
            return
        PlotParticleVelocityFrequencyResponseInput()

    def action_export_element_transfer_data_callback(self):
        if app().project.acoustic_harmonic_solver.solution is None:
            return
        ExportElementTransferDataInput()
    
    def update_hidden_plots(self):
        for i in range(self.render_widgets_stack.count()):
            widget = self.render_widgets_stack.widget(i)
            if hasattr(widget, "update_hidden_plot"):
                widget.update_hidden_plot()
    
    def process_acoustic_modal_analysis(self):
        try:
            self.project.solve_acoustic_modal_analysis()
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            self.configure_acoustic_modal_analysis_render_widget(True)

    def process_structural_modal_analysis(self):
        try:
            self.project.solve_structural_modal_analysis()
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            self.configure_structural_modal_analysis_render_widget(True)
    
    def process_acoustic_harmonic_analysis(self):
        try:
            self.project.solve_acoustic_harmonic_analysis()
        except NotImplementedError as e:
            ErrorMessage(e)
        else:
            self.configure_acoustic_harmonic_analysis_render_widget(True)
    
    def disable_advanced_acoustic_plots_buttons(self, disabled : bool):
        self.action_plot_specific_acoustic_impedance.setDisabled(disabled)
        self.action_plot_particle_velocity.setDisabled(disabled)
        self.action_export_element_transfer_data.setDisabled(disabled)

def create_new_folder(path : Path, folder_name : str) -> Path:
    folder_path = path / folder_name
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return folder_path