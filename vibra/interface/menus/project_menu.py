from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QFileDialog, QMenu

from vibra.interface.loading_bar import load_function
from vibra.interface.viewer_3d.vtk_widget import VTKWidget
from vibra.utils.icons import load_icon


class ProjectMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Project")

        self.create_actions()
        self.create_layout()

    def create_actions(self):
        color = QColor("#0055DD")
        self.vibra_icon = load_icon(Path("data/icons/logo_vibra.png"), color)
        self.help_icon = load_icon(Path("data/icons/help.png"), color)
        self.new_project_icon = load_icon(Path("data/icons/new_file.png"), color)
        self.load_project_icon = load_icon(Path("data/icons/import.png"), color)
        self.exit_import_icon = load_icon(Path("data/icons/exit.png"), color)
        self.save_icon = load_icon(Path("data/icons/save.png"), color)
        self.save_as_icon = load_icon(Path("data/icons/save_as.png"), color)
        self.save_as_png_icon = load_icon(Path("data/icons/png.png"), color)
        self.recent_icon = load_icon(Path("data/icons/recent.png"), color)
        self.theme_sun_icon = load_icon(Path("data/icons/sun_icon.png"), color)
        self.theme_moon_icon = load_icon(Path("data/icons/moon_icon.png"), color)
        self.import_geometry_icon = load_icon(Path("data/icons/cube-scan.png"), color)
        self.capture_image_icon = load_icon(Path("data/icons/image-plus.png"), color)
        self.new_project_action = QAction(self.new_project_icon, "New Project", self)
        self.load_project_action = QAction(self.load_project_icon, "Load Project", self)
        self.exit_import_action = QAction(self.exit_import_icon, "Exit", self)
        self.import_geometry_action = QAction(self.capture_image_icon, "Import geometry", self)
        self.capture_image_action = QAction(self.import_geometry_icon, "Capture image", self)
        self.save_action = QAction(self.save_icon, "Save", self)
        self.save_as_action = QAction(self.save_as_icon, "Save as", self)
        self.help_action = QAction(self.help_icon, "About Vibra", self)
        self.recent_action = QAction(self.recent_icon, "Recent", self)
        self.theme_action = QAction(self.theme_sun_icon, "Theme", self)
        self.import_geometry_action.triggered.connect(self.import_geometry_callback)
        self.capture_image_action.triggered.connect(self.capture_image_callback)
        self.save_action.triggered.connect(self.save_callback)
        self.help_action.triggered.connect(self.help_callback)
        self.exit_import_action.triggered.connect(self.exit_callback)
        self.theme_action.triggered.connect(self.theme_callback)
        self.help_action.setShortcut("F1")

    def create_layout(self):
        self.clear()
        self.addAction(self.new_project_action)
        self.addAction(self.load_project_action)
        self.addAction(self.save_action)
        self.addAction(self.save_as_action)
        self.addAction(self.import_geometry_action)
        self.addAction(self.capture_image_action)
        self.addAction(self.recent_action)
        self.addAction(self.theme_action)
        self.addAction(self.exit_import_action)

    def save_callback(self):
        self.parent().project.save()

    def help_callback(self):
        self.parent().viewer_tabs.show_help()

    def exit_callback(self):
        loaded_function = load_function(self.parent().project.long_function, self)
        loaded_function()

    def theme_callback(self):
        if self.parent().user_config.theme == "light":
            self.parent().set_theme("dark")
            self.theme_action.setIcon(self.theme_sun_icon)

        elif self.parent().user_config.theme == "dark":
            self.parent().set_theme("light")
            self.theme_action.setIcon(self.theme_moon_icon)

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
        loaded_import_geometry = load_function(self.parent().project.import_geometry, self)
        loaded_import_geometry(path)

        self.parent().viewer_tabs.show_model()
        self.parent().viewer_tabs.update_plots()
        self.parent().set_theme(self.parent().user_config.theme)

    # TODO: Create and connect actions for these
    def show_model_callback(self):
        self.parent().viewer_tabs.show_model()

    def show_example_callback(self):
        self.parent().viewer_tabs.show_example()

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
