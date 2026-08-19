import logging
import platform
import sys
from functools import partial
from pathlib import Path
from shutil import rmtree

import gmsh
from molde import stylesheets
from molde.render_widgets import CommonRenderWidget
from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QMenu, QMessageBox

from vibra import SUPPORTED_GEOMETRY_EXTENSIONS, SUPPORTED_MESH_EXTENSIONS, TEMP_PROJECT_DIR, app
from vibra.engine.assemblers import AcousticAssembler
from vibra.engine.solvers import HarmonicSolver
from vibra.interface.data.icons.theme_resources import set_icon_theme
from vibra.interface.data_handler.export_mesh_data import ExportMeshData
from vibra.interface.formatters.icons import Icon, get_vibra_icon
from vibra.interface.general.entity_visibility_handler import EntityVisibilityHandler
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.selection_handler import SelectionHandler
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.menus.model_setup_widget import ModelSetupWidget
from vibra.interface.menus.results_viewer_widget import ResultsViewerWidget
from vibra.interface.model_inputs.general.choose_property_to_delete import ChoosePropertyToDelete
from vibra.interface.model_inputs.general.mesher_setup_inputs import MesherSetupInputs
from vibra.interface.plots.acoustic.export_element_transfer_data_inputs import ExportElementTransferDataInputs
from vibra.interface.project.save_project_data_selector import SaveProjectDataSelector
from vibra.interface.section_plane_widget import SectionPlaneWidget
from vibra.interface.status_bar import StatusBar
from vibra.interface.toolbars.analysis_toolbar import AnalysisToolbar
from vibra.interface.toolbars.view_toolbar import ViewToolbar
from vibra.interface.ui_generated.main_window_ui import MainWindow_UI
from vibra.interface.user_input.about_vibra import AboutVibraInput
from vibra.interface.user_input.input_ui import InputUi
from vibra.interface.user_input.render_user_preferences import RendererUserPreferencesInput
from vibra.interface.viewer_3d.render_widgets import GeometryRenderWidget, MeshRenderWidget, ResultsRenderWidget
from vibra.interface.welcome_widget import WelcomeWidget
from vibra.utils.interface_utils import GeometryColorMode, VisualizationFilter, block_signals, qt_extensions


class MainWindow(MainWindow_UI):
    theme_changed = Signal(str)
    visualization_changed = Signal()
    render_widget_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.selection = SelectionHandler(app().project)
        self.entity_visibility = EntityVisibilityHandler(app().project)

        self.selection.selection_changed.connect(self.selection_changed_callback)
        self.entity_visibility.changed.connect(self.update_hidden_plots)

        self.hidden_mesh_faces = set()
        self.hidden_mesh_solids = set()
        self.distinguished_solids = set()

        self.show_menu_items = True
        self.last_render_index = None
        self._initialize()

    def _initialize(self):
        self.dialog = None
        self.user_path = Path().home()

    def _connect_actions(self):
        """
        Instead of connecting every action manually, one by one,
        this function loops through every action and connects it
        to a function ending with "_callback".

        For example an action named "action_new" will be connected to
        the function named "action_new_callback" if it exists.
        """
        for action in self.findChildren(QAction):
            action: QAction
            function_name = action.objectName() + "_callback"
            function_exists = hasattr(self, function_name)
            if not function_exists:
                continue

            function = getattr(self, function_name)
            if callable(function):
                action.triggered.connect(function)

    def _create_basic_layout(self):
        self.status_bar = StatusBar(self)
        self.analysis_toolbar = AnalysisToolbar()

        self.create_recents_menu()
        self.create_status_bar()

        self.clear_render_widgets_stack()
        self.render_widgets_stack.addWidget(self.geometry_widget)
        self.render_widgets_stack.addWidget(self.mesh_widget)
        self.render_widgets_stack.addWidget(self.results_widget)
        self.render_widgets_stack.addWidget(self.welcome_widget)
        self.view_toolbar = ViewToolbar(self.render_widgets_stack)

        self.set_toolbars_visible(False)

        self.render_widgets_stack.currentChanged.connect(self.render_changed_callback)
        self.visualization_changed.connect(self.reload_visualization_filter)
        self.render_widget_changed.connect(self.reload_visualization_filter)
        self.reload_visualization_filter()

        self.stacked_setup.addWidget(self.model_setup_widget)
        self.stacked_setup.addWidget(self.results_viewer_widget)

        self.addToolBar(self.analysis_toolbar)
        self.insertToolBarBreak(self.analysis_toolbar)

        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.view_toolbar)

        for render in self.get_renderer_widgets():
            self.view_toolbar.render_tool_changed.connect(render.add_render_tool)

        self.set_toolbars_enabled(False)
        # self.update_toolbars_stylesheets()
        self.action_export_element_transfer_data.setDisabled(True)

        self.splitter.setSizes([100, 400])
        self.splitter.widget(0).setVisible(False)
        self.splitter.widget(0).setMinimumWidth(360)

    def _config_window(self):
        self.setMinimumHeight(768)
        self.showMinimized()
        self.vibra_icon = get_vibra_icon()
        self.setWindowIcon(self.vibra_icon)
        self.setWindowTitle("Vibra")
        self.installEventFilter(self)

        # to ensure everything has been processed before proceeding
        app().processEvents()

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
        self._config_window()
        self._connect_actions()

        app().splash.update_progress(30)
        self._load_render_widgets()
        self._load_menu_widgets()

        app().splash.update_progress(60)
        self._create_basic_layout()
        self._configure_render_widgets_stack()
        self._configure_stacked_setup()

        app().splash.update_progress(90)
        self.load_user_preferences()
        self.config_tool_tip_appearance()
        self.create_temporary_vibra_folder()

        app().splash.close()
        self.showMaximized()

        app().processEvents()

        if not self.is_temporary_vibra_folder_empty():
            self.recovery_dialog()

        else:
            self.try_to_open_argv_path()

    def update_toolbars_stylesheets(self):
        if self.analysis_toolbar.styleSheet() == "":
            style_sheet = self.get_toolbars_stylesheet()
            self.analysis_toolbar.setStyleSheet(style_sheet)
            self.view_toolbar.setStyleSheet(style_sheet)
            self.renderer_toolbar.setStyleSheet(style_sheet)
            self.workspaces_toolbar.setStyleSheet(style_sheet)
            return

        self.analysis_toolbar.setStyleSheet("")
        self.view_toolbar.setStyleSheet("")
        self.renderer_toolbar.setStyleSheet("")
        self.workspaces_toolbar.setStyleSheet("")

    def get_toolbars_stylesheet(self):
        style_sheet = """
            QToolBar {
                border-style: solid;
                border-width: 0.5px;
                border-color: #888888;
            }
            """
        return style_sheet

    def try_to_open_argv_path(self):
        """
        Check every argument passed in the command line and try to open it if it is a valid file.
        """

        if len(sys.argv) <= 1:
            return

        for arg in sys.argv[1:]:
            path = Path(arg)

            if not path.is_file():
                continue

            if not path.exists():
                continue

            if path.suffix == ".vibra":
                self.open_project(path)
                break

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

        set_icon_theme(theme)

        self.theme_changed.emit(theme)

    def update_mesh_information(self):
        self.status_bar.update_mesh_information()

    def update_geometry_information(self):
        self.status_bar.update_geometry_information()

    def _configure_render_widgets_stack(self):
        self.render_widgets_stack.setCurrentWidget(self.welcome_widget)

    def _configure_stacked_setup(self):
        self.stacked_setup.setCurrentWidget(self.model_setup_widget)

    def create_status_bar(self):
        self.setStatusBar(self.status_bar)

    def config_tool_tip_appearance(self):
        tool_tip_style = "QToolTip { color: rgb(0, 0, 0); background-color: rgb(255, 255, 255) }"
        self.setStyleSheet(tool_tip_style)

    def _load_render_widgets(self):
        self.section_plane = SectionPlaneWidget(self)
        self.geometry_widget = GeometryRenderWidget()
        self.mesh_widget = MeshRenderWidget()
        self.results_widget = ResultsRenderWidget()

        self.welcome_widget = WelcomeWidget()

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

    def create_recents_menu(self):
        self.recent_icon = Icon(":/icons/recent.png")

        self.recents_menu = QMenu("Recent projects", self)
        self.recents_menu.setIcon(self.recent_icon)
        self.update_recents_menu()

        self.menu_project.insertMenu(self.action_save, self.recents_menu)
        self.menu_project.insertSeparator(self.action_save)

    def update_recents_menu(self):
        self.recents_menu.clear()
        recent_paths = app().config.get_recent_files()
        for path in recent_paths:
            import_action = QAction(str(path), self)
            import_action.triggered.connect(partial(self.open_project, path))
            self.recents_menu.addAction(import_action)

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

    def selection_changed_callback(self):
        self.status_bar.set_selection(
            self.selection.geometry_points,
            self.selection.geometry_lines,
            self.selection.geometry_surfaces,
            self.selection.geometry_volumes,
        )

    def action_section_plane_callback(self, condition: bool):
        if condition:
            self.section_plane.show()
        else:
            self.section_plane.cutting = False
            self.section_plane.keep_section_plane = False
            self.section_plane.close()
            self.section_plane.value_changed.emit()

    def action_theme_callback(self):
        self.theme_sun_icon = Icon(":/icons/sun_icon.png")
        self.theme_moon_icon = Icon(":/icons/moon_icon.png")

        if app().config.user_preferences.interface_theme == "light":
            app().config.user_preferences.set_dark_theme()
            self.set_theme("dark")
            self.action_theme.setIcon(self.theme_sun_icon)

            if hasattr(self.welcome_widget, "update_logo"):
                self.welcome_widget.update_logo("vibra_colored_dark_background.png")

        elif app().config.user_preferences.interface_theme == "dark":
            app().config.user_preferences.set_light_theme()
            self.set_theme("light")
            self.action_theme.setIcon(self.theme_moon_icon)

            if hasattr(self.welcome_widget, "update_logo"):
                self.welcome_widget.update_logo("vibra_colored_light_background.png")

        app().config.update_config_file()

    def action_show_empty_callback(self, condition: bool):
        if condition:
            self.geometry_widget.visualization_filter.color_mode = GeometryColorMode.EMPTY
        else:
            self.geometry_widget.visualization_filter.color_mode = GeometryColorMode.COLORED
        self.visualization_changed.emit()

    def get_renderer_widgets(self) -> list[CommonRenderWidget]:
        return [self.geometry_widget, self.mesh_widget, self.results_widget]

    def action_user_preferences_callback(self):
        self.close_dialogs()
        self.render_user_preferences = RendererUserPreferencesInput()

    def action_points_callback(self):
        self.selection.select_all_points()
        self.action_model_workspace_callback()

    def action_faces_callback(self):
        self.selection.select_all_surfaces()
        self.action_model_workspace_callback()

    def action_solid_callback(self):
        self.selection.select_all_volumes()
        self.action_model_workspace_callback()

    def action_all_entities_geometry_callback(self):
        self.selection.select_all_geometry()
        self.action_model_workspace_callback()

    def action_all_entities_mesh_callback(self):
        self.selection.select_all_mesh()
        self.action_mesh_workspace_callback()

    def action_nodes_callback(self):
        self.selection.select_all_nodes()
        self.action_mesh_workspace_callback()

    def action_surface_elements_callback(self):
        self.selection.select_all_faces()
        self.action_mesh_workspace_callback()

    def action_solid_elements_callback(self):
        self.selection.select_all_solids()
        self.action_mesh_workspace_callback()

    def action_clear_selection_callback(self):
        self.selection.clear_selection()

    def action_volume_selection_mode_callback(self, checked):
        self.selection.volume_selection_mode = checked
        self.selection.selection_changed.emit()

    def action_invert_selection_callback(self):
        self.selection.invert_selection()

    def configure_results_render_widget(self):
        self.stacked_setup.setCurrentWidget(self.results_viewer_widget)
        self.results_viewer_widget.hide_bottom_widget()
        self.results_viewer_widget.results_viewer_items.clear_last_item()
        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)

        self.action_results_workspace.setEnabled(True)
        self.action_results_workspace.setChecked(True)
        self.action_mesh_workspace.setChecked(False)
        self.action_model_workspace.setChecked(False)
        self.reload_visualization_filter()

    def show_geometry_render_widget(self):
        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)
        self.view_toolbar.enable_selection_tool()

    def show_mesh_render_widget(self):
        self.render_widgets_stack.setCurrentWidget(self.mesh_widget)
        self.view_toolbar.enable_selection_tool()

    def clear_render_widgets_stack(self):
        for _ in range(self.render_widgets_stack.count()):
            widget = self.render_widgets_stack.widget(0)
            self.render_widgets_stack.removeWidget(widget)

    def update_plots(self, reset_camera=True):
        self.model_setup_widget.model_setup_items.update_items_appearance()
        renders_number = self.render_widgets_stack.count()
        for i in range(renders_number):
            logging.info(f"Updating renders... [{i + 1}/{renders_number}]")
            widget = self.render_widgets_stack.widget(i)
            if isinstance(widget, CommonRenderWidget):
                widget.update_plot(reset_camera)

    def update_symbols(self):
        self.model_setup_widget.model_setup_items.update_items_appearance()
        for i in range(self.render_widgets_stack.count()):
            widget = self.render_widgets_stack.widget(i)
            if hasattr(widget, "update_symbols"):
                widget.update_symbols()

    def update_info_text(self):
        for i in range(self.render_widgets_stack.count()):
            widget = self.render_widgets_stack.widget(i)
            if hasattr(widget, "update_info_text"):
                widget.update_info_text()

    def update_scale_bar(self, show: bool):
        for i in range(self.render_widgets_stack.count()):
            widget = self.render_widgets_stack.widget(i)
            if hasattr(widget, "scale_bar_actor"):
                widget.scale_bar_actor.SetVisibility(show)

    def update_renderer_font_size(self):
        for i in range(self.render_widgets_stack.count()):
            widget = self.render_widgets_stack.widget(i)
            if hasattr(widget, "update_renderer_font_size"):
                widget.update_renderer_font_size()

    def workspace_updating_for_model_setup(self):
        mesh_workspace = app().main_window.action_mesh_workspace.isChecked()
        if mesh_workspace:
            app().main_window.action_model_workspace_callback()

    def action_model_workspace_callback(self):
        self.action_node_view.setToolTip("Points view")
        self.action_model_workspace.setChecked(True)
        self.action_mesh_workspace.setChecked(False)
        self.action_results_workspace.setChecked(False)

        self.view_toolbar.enable_selection_tool()

        valid_solution = app().project.is_there_a_valid_solution()
        self.action_results_workspace.setEnabled(valid_solution)

        self.stacked_setup.setCurrentWidget(self.model_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)
        self.model_setup_widget.model_setup_items.expand_menu_items()

        self.splitter.widget(0).setVisible(True)

        self.reload_visualization_filter()

        nodal_normals = self.results_widget.visualization_filter.nodal_normal_symbols
        element_normals = self.results_widget.visualization_filter.element_normal_symbols
        if nodal_normals or element_normals:
            self.results_widget.visualization_filter.nodal_normal_symbols = False
            self.results_widget.visualization_filter.element_normal_symbols = False
            self.update_symbols()

    def action_mesh_workspace_callback(self):
        self.action_node_view.setToolTip("Nodes view")
        self.action_mesh_workspace.setChecked(True)
        self.action_model_workspace.setChecked(False)
        self.action_results_workspace.setChecked(False)

        self.view_toolbar.enable_selection_tool()

        if app().project.model.is_the_mesh_setup_defined():
            obj = MesherSetupInputs(close_after_generate=True)
            if not obj.complete:
                self.action_model_workspace_callback()
                return

        valid_solution = app().project.is_there_a_valid_solution()
        self.action_results_workspace.setEnabled(valid_solution)

        self.update_mesh_information()
        self.stacked_setup.setCurrentWidget(self.model_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.mesh_widget)
        self.model_setup_widget.model_setup_items.expand_menu_items()

        self.splitter.widget(0).setVisible(True)

        self.reload_visualization_filter()

    def action_results_workspace_callback(self):
        if not app().project.is_there_a_valid_solution():
            return

        self.action_results_workspace.setEnabled(True)
        self.action_results_workspace.setChecked(True)
        self.action_model_workspace.setChecked(False)
        self.action_mesh_workspace.setChecked(False)

        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)
        self.stacked_setup.setCurrentWidget(self.results_viewer_widget)
        self.results_viewer_widget.results_viewer_items.update_items()
        self.analysis_toolbar.update_analysis_combo_boxes()

        self.reload_visualization_filter()

    def action_new_project_callback(self):
        self.new_project_dialog()

    def action_open_project_callback(self):
        self.open_project_dialog()

    def action_home_exit_callback(self):
        self.close_dialogs()
        self.action_section_plane_callback(False)
        self.action_section_plane.setChecked(False)

        self.setWindowTitle("Vibra")
        self.stacked_setup.setVisible(False)
        self.set_toolbars_visible(False)
        self.results_viewer_widget.hide_bottom_widget()
        self.welcome_widget.update_recent_projects()
        self.model_setup_widget.model_setup_items.reset_items_appearance()
        self.render_widgets_stack.setCurrentWidget(self.welcome_widget)

        self.selection.clear_selection()
        self.results_widget.remove_all_actors()
        self.mesh_widget.remove_all_actors()
        self.geometry_widget.remove_all_actors()
        app().project.reset_variables()
        app().project.clear_working_directory()
        self.action_unhide_all_callback()

        self.set_toolbars_enabled(False)
        self.action_export_element_transfer_data.setDisabled(True)

    def action_import_mesh_callback(self):
        self.import_mesh_dialog()

    def action_import_geometry_callback(self):
        self.import_geometry_dialog()

    def action_hide_selection_callback(self):
        mesh = app().project.model.mesh

        if not mesh.are_there_volumes_in_geometry():
            PrintMessageInput(
                [
                    "Warning",
                    "No volumes were found in the geometry",
                    "Since the current geometry does not contains volumes, the operation can not be performed.",
                ]
            )

        self.entity_visibility.hide_surfaces(self.selection.geometry_surfaces)
        self.entity_visibility.hide_volumes(self.selection.geometry_volumes)
        self.selection.clear_selection()

    def has_hidden_part(self) -> bool:
        return any(
            [
                self.entity_visibility.has_hidden_entity(),
                len(self.distinguished_solids) != 0,
                self.section_plane.cutting,
                bool(app().project.model.mesh.collapsed_elements_data),
                bool(app().project.model.mesh.disconnected_nodes_data),
            ]
        )

    def distinguish_mesh_solids(self, solid_elements):

        self.distinguished_solids = set(solid_elements)
        if any(solid_elements):
            self.show_mesh_render_widget()
        else:
            self.show_geometry_render_widget()

        self.reload_visualization_filter()
        self.visualization_changed.emit()

    def action_unhide_all_callback(self):
        self.entity_visibility.unhide_all()

    def action_save_callback(self):
        self.save_project_dialog()

    def create_temporary_vibra_folder(self):
        temp_path = self.user_path / "temp_vibra"
        if not temp_path.exists():
            temp_path.mkdir(parents=True)
        return temp_path

    def reset_temporary_vibra_folder(self):
        if TEMP_PROJECT_DIR.exists():
            rmtree(TEMP_PROJECT_DIR)  # delete the directory
        TEMP_PROJECT_DIR.mkdir(parents=True, exist_ok=True)  # create a new empty directory

    def is_temporary_vibra_folder_empty(self):
        if TEMP_PROJECT_DIR.exists():
            return not any(TEMP_PROJECT_DIR.iterdir())
        else:
            return True

    def recovery_dialog(self):
        caption = "The recovery project data has been detected in the application backup files. "
        caption += "Would you like to try to recover the last project files?"

        obj = QMessageBox.question(
            self,
            "Project recovery",
            caption,
            QMessageBox.Yes | QMessageBox.No,
        )

        if obj == QMessageBox.Yes:
            self.open_project()
        else:
            self.reset_temporary_vibra_folder()
            self.try_to_open_argv_path()

    def new_project_dialog(self):
        if self.import_geometry_or_mesh_dialog():
            return

    def import_geometry_or_mesh_dialog(self):
        self.close_dialogs()

        path = app().config.get_last_folder_for("geometry_mesh_folder", default=self.user_path)

        geo = qt_extensions(SUPPORTED_GEOMETRY_EXTENSIONS)
        mesh = qt_extensions(SUPPORTED_MESH_EXTENSIONS)

        ext_filter = (
            f"All Accepted Files ({geo} {mesh})"
            f";;Geometry Files ({geo})"
            f";;Mesh Files ({mesh})"
            ";;All Files (*)"
        )  # fmt: skip

        load_path, check = QFileDialog.getOpenFileName(
            self,
            "Select a geometry or mesh file to start your project.",
            str(path),
            filter=ext_filter,
        )

        if not check:
            return True

        app().config.write_last_folder_path_in_file(
            "geometry_mesh_folder",
            load_path,
        )

        self.setWindowTitle("New project")
        self.reset_temporary_vibra_folder()
        self._import_geometry_or_mesh(load_path)

    def _import_geometry_or_mesh(self, load_path: Path):
        ext = Path(load_path).suffix.strip(".").lower()
        if ext in SUPPORTED_GEOMETRY_EXTENSIONS:
            app().project.reset_project()
            self.import_geometry(load_path)

        elif ext in SUPPORTED_MESH_EXTENSIONS:
            app().project.reset_project()
            self.import_mesh(load_path)

        else:
            raise ValueError(f"File extension {ext} not supported")

    def import_geometry_dialog(self):
        path = app().config.get_last_folder_for("geometry_mesh_folder", default=self.user_path)

        geo = qt_extensions(SUPPORTED_GEOMETRY_EXTENSIONS)
        ext_filter = f"Geometry Files ({geo});; All Files (*)"

        load_path, check = QFileDialog.getOpenFileName(
            self,
            "Select a geometry file to import.",
            str(path),
            filter=ext_filter,
        )

        if not check:
            return

        current_fluid_library = app().project.model.properties.fluid_library
        current_material_library = app().project.model.properties.material_library

        app().project.reset_project()
        app().project.model.properties.fluid_library = current_fluid_library
        app().project.model.properties.material_library = current_material_library

        self.import_geometry(load_path)

    def import_mesh_dialog(self):
        path = app().config.get_last_folder_for("geometry_mesh_folder", default=self.user_path)

        mesh = qt_extensions(SUPPORTED_MESH_EXTENSIONS)
        ext_filter = f"Mesh Files ({mesh});; All Files (*)"

        load_path, check = QFileDialog.getOpenFileName(
            self,
            "Select a mesh file to import.",
            str(path),
            filter=ext_filter,
        )

        if not check:
            return

        current_fluid_library = app().project.model.properties.fluid_library
        current_material_library = app().project.model.properties.material_library

        app().project.reset_project()
        app().project.model.properties.fluid_library = current_fluid_library
        app().project.model.properties.material_library = current_material_library

        self.import_mesh(load_path)

    def save_project_dialog(self):
        save_path = app().project.save_path
        if save_path is None:
            return self.save_project_as_dialog()
        else:
            self.save_project_as(save_path)
            return True

    def save_project_as_dialog(self):
        obj = SaveProjectDataSelector()
        if not obj.complete:
            return False

        save_dir = app().config.get_last_folder_for("project_folder", default=self.user_path)

        kwargs = dict()
        if platform.system() == "Linux":
            kwargs["options"] = QFileDialog.Option.DontUseNativeDialog

        file_path, check = QFileDialog.getSaveFileName(
            self,
            "Save As",
            str(save_dir),
            filter="Vibra File (*.vibra)",
            **kwargs,
        )

        if not check:
            return False

        if obj.ignore_results_data:
            # TODO: check if app().new_project.reset_solution() makes more sense
            app().project.project_writer.delete_results_data()

        if obj.ignore_mesh_data:
            app().project.project_writer.delete_mesh_data()

        if not file_path.endswith(".vibra"):
            file_path += ".vibra"

        self.save_project_as(file_path)

        return True

    def save_project_as(self, path: str):
        def save_data(path):
            project = app().project

            path = Path(path)
            app().config.add_recent_file(path)
            app().config.write_last_folder_path_in_file("project_folder", path)
            logging.info("Saving project data... [30/100]")

            project.save_project(path, name=path.stem)
            logging.info("Saving project data... [75/100]")

            # Update interface
            self.update_recents_menu()
            self.setWindowTitle(project.model.name)
            logging.info("The project data has been saved. [100/100]")

        LoadingWindow(save_data).run(path)

        from datetime import datetime

        message = f"The project data has been saved: {datetime.now()}"
        print(message)

    def open_project_dialog(self):
        path = app().config.get_last_folder_for("project_folder", default=self.user_path)

        project_path, check = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            str(path),
            filter="Vibra File (*.vibra)",
        )

        if not check:
            return

        self.open_project(project_path)

    def import_geometry(self, path: Path | str):
        app().config.write_last_folder_path_in_file(
            "geometry_mesh_folder",
            path,
        )

        path = Path(path)
        LoadingWindow(app().project.import_geometry).run(path)
        LoadingWindow(app().project.generate_visual_mesh).run()

        # Interface update
        LoadingWindow(self.geometry_widget.update_plot).run()
        self.update_geometry_information()
        self.update_toolbar_and_menu_items_after_load_project()
        self.set_toolbars_visible(True)
        self.view_toolbar.show_render_tools()
        self.set_toolbars_enabled(True)
        self.action_model_workspace_callback()

    def import_mesh(self, path: Path | str):
        app().config.write_last_folder_path_in_file(
            "geometry_mesh_folder",
            path,
        )

        path = Path(path)
        LoadingWindow(app().project.import_mesh).run(path)

        # Interface update
        LoadingWindow(self.geometry_widget.update_plot).run()
        LoadingWindow(self.mesh_widget.update_plot).run()
        self.update_geometry_information()
        self.update_toolbar_and_menu_items_after_load_project()
        self.set_toolbars_visible(True)
        self.view_toolbar.show_render_tools()
        self.set_toolbars_enabled(True)
        self.action_mesh_workspace_callback()

    def open_project(self, project_path: str | Path | None = None):
        """
        This function loads a new project into a temporary folder.
        If you pass a valid vibra file to this function, it will first copy
        the file to a temporary folder and then load it.
        """

        # Actual loading
        project = app().project
        config = app().config
        project_recovery = project_path is None

        if project_recovery:
            LoadingWindow(project.read_from_working_dir).run()
            project.model.name = "Recover project"
        else:
            LoadingWindow(project.load_project).run(project_path)
            config.add_recent_file(project_path)
            config.write_last_folder_path_in_file("project_folder", project_path)

        # Interface update
        self.update_recents_menu()
        self.setWindowTitle(project.model.name)
        self.view_toolbar.set_front_view()

        self.status_bar.update_geometry_information()
        self.status_bar.update_mesh_information()

        self.model_setup_widget.model_setup_items.expand_menu_items()

        self.set_toolbars_enabled(True)
        self.update_toolbar_and_menu_items_after_load_project()
        self.analysis_toolbar.check_analysis_setup_callback()
        self.analysis_toolbar.update_reset_solution_button_accessibility()

        LoadingWindow(self.geometry_widget.update_plot).run()
        LoadingWindow(self.mesh_widget.update_plot).run()

        self.action_model_workspace_callback()

        self.set_toolbars_visible(True)
        self.view_toolbar.set_front_view()

        if app().project.model.can_resume_solution:
            window_title = "Acoustic Harmonic results"
            title = "Missing solution frequency records"
            message = 'Click on the "Resume the analysis" button to solve remaining frequencies'
            PrintMessageInput([window_title, title, message])

    def set_toolbars_visible(self, state: bool):
        self.analysis_toolbar.setVisible(state)
        self.view_toolbar.setVisible(state)
        self.renderer_toolbar.setVisible(state)
        self.workspaces_toolbar.setVisible(state)
        self.status_bar.setVisible(state)

    def set_toolbars_enabled(self, state: bool):
        self.analysis_toolbar.setEnabled(state)
        self.view_toolbar.setEnabled(state)
        self.renderer_toolbar.setEnabled(state)
        self.workspaces_toolbar.setEnabled(state)

    def remove_property(self):
        self.close_dialogs()
        ChoosePropertyToDelete()

    def update_toolbar_and_menu_items_after_load_project(self):
        self.model_setup_widget.model_setup_items.filter_available_items_and_analyzes_according_to_geometry_information()
        self.model_setup_widget.model_setup_items.modify_general_settings_items_access()
        self.model_setup_widget.model_setup_items.update_items_appearance()
        self.analysis_toolbar.update_resume_soluton_button_visibility()

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

        widget = self.render_widgets_stack.currentWidget()
        if isinstance(widget, CommonRenderWidget):
            image = widget.get_screenshot()
            with open(path, "wb") as file:
                image.save(file)

    def action_exit_callback(self):
        self.close_app()

    def action_face_view_callback(self):
        self.visualization_changed_callback()

    def action_line_view_callback(self):
        self.visualization_changed_callback()

    def action_node_view_callback(self):
        self.visualization_changed_callback()

    def action_hide_show_symbols_callback(self):
        self.visualization_changed_callback()

    def action_ghost_view_callback(self):
        self.visualization_changed_callback()

    def get_current_render_widget(self) -> CommonRenderWidget | None:
        return self.render_widgets_stack.currentWidget()

    def get_current_visualization_filter(self) -> VisualizationFilter | None:
        render_widget = self.get_current_render_widget()
        if not hasattr(render_widget, "visualization_filter"):
            return None
        return render_widget.visualization_filter

    def visualization_changed_callback(self):
        if visualization_filter := self.get_current_visualization_filter():
            self.update_visualization_filter(visualization_filter)
        self.visualization_changed.emit()

    def apply_visualization_filter(self, filter: VisualizationFilter):
        with block_signals(self):
            self.action_node_view.setChecked(filter.points)
            self.action_line_view.setChecked(filter.lines)
            self.action_face_view.setChecked(filter.faces or filter.solids)
            self.action_ghost_view.setChecked(filter.ghost)

    def update_visualization_filter(self, filter: VisualizationFilter):
        filter.points = self.action_node_view.isChecked()
        filter.lines = self.action_line_view.isChecked()
        filter.faces = self.action_face_view.isChecked()
        filter.solids = self.action_face_view.isChecked()
        filter.ghost = self.action_ghost_view.isChecked()
        filter.symbols = self.action_hide_show_symbols.isChecked()

    def reload_visualization_filter(self):
        if visualization_filter := self.get_current_visualization_filter():
            self.apply_visualization_filter(visualization_filter)

    def action_about_vibra_callback(self):
        self.close_dialogs()
        AboutVibraInput()

    def close_app(self):
        self.minimize_dialogs()

        condition_1 = app().project.save_path is None
        condition_2 = not app().project.project_paths.is_empty()
        condition_3 = app().project.needs_saving
        condition = (condition_1 and condition_2) or condition_3

        if condition:
            close = QMessageBox.question(
                self,
                "QUIT",
                "Would you like to save the project data before exit?",
                QMessageBox.Cancel | QMessageBox.Discard | QMessageBox.Save,
            )

            if close == QMessageBox.Cancel:
                self.restore_open_dialogs()
                return

            elif close == QMessageBox.Save:
                if not self.save_project_dialog():
                    return

        else:
            close = QMessageBox.question(
                self,
                "QUIT",
                "Would you like to close the application?",
                QMessageBox.Yes | QMessageBox.No,
            )

            if close == QMessageBox.No:
                self.restore_open_dialogs()
                return

        self.reset_temporary_vibra_folder()

        # finalize the gmsh before closing the application
        if gmsh.isInitialized():
            gmsh.finalize()
            app().processEvents()

        app().quit()

    def close_dialogs(self):
        for window in app().topLevelWidgets():
            if isinstance(window, MainWindow):
                continue

            if isinstance(window, LoadingWindow):
                continue

            window.close()

    def hide_dialogs(self):
        for window in app().topLevelWidgets():
            if isinstance(window, MainWindow):
                continue

            if isinstance(window, LoadingWindow):
                continue

            if window.isVisible():
                window.hide()

    def minimize_dialogs(self):
        for window in app().topLevelWidgets():
            if isinstance(window, MainWindow):
                continue

            if isinstance(window, LoadingWindow):
                continue

            if window.isVisible():
                window.showMinimized()

    def restore_open_dialogs(self):
        for window in app().topLevelWidgets():
            if isinstance(window, MainWindow):
                continue

            if isinstance(window, LoadingWindow):
                continue

            if window.isVisible():
                window.showNormal()

    def action_export_element_transfer_data_callback(self):
        if not isinstance(app().project.solver, HarmonicSolver):
            return

        if not isinstance(app().project.assembler, AcousticAssembler):
            return

        ExportElementTransferDataInputs()

    def update_hidden_plots(self):
        def update_plot_callback():
            N = self.render_widgets_stack.count()
            for i in range(self.render_widgets_stack.count()):
                widget = self.render_widgets_stack.widget(i)
                if hasattr(widget, "update_hidden_plot"):
                    logging.info(f"Updating render... [{i + 1}/{N}]")
                    widget.update_hidden_plot()

        LoadingWindow(update_plot_callback).run()

    def eventFilter(self, obj, event: QEvent):
        modifiers = app().keyboardModifiers()
        alt_pressed = modifiers & Qt.KeyboardModifier.AltModifier
        if event.type() == QEvent.Type.ShortcutOverride:
            if event.key() == Qt.Key.Key_F5:
                self.update_plots()

            elif alt_pressed and (event.key() == Qt.Key.Key_P):
                if self.section_plane.isVisible():
                    return super(MainWindow, self).eventFilter(obj, event)

                active = self.action_section_plane.isChecked()
                self.action_section_plane.blockSignals(True)
                self.action_section_plane.setChecked(not active)
                self.action_section_plane.blockSignals(False)
                self.section_plane.cutting = not active
                self.section_plane.value_changed.emit()

            elif event.key() == Qt.Key.Key_Delete:
                self.remove_property()

        return super(MainWindow, self).eventFilter(obj, event)

    def closeEvent(self, event: QEvent):
        self.close_app()
        event.ignore()
