from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QMenu

from vibra.interface.loading_bar import load_function
from vibra.utils.icons import load_icon


class ProjectMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Project")

        self.create_actions()
        self.create_layout()

    def create_actions(self):
        color = QColor("#0055DD")

        self.new_project_icon = load_icon(Path("data/icons/new_file.png"), color)
        self.load_project_icon = load_icon(Path("data/icons/import.png"), color)
        self.recent_icon = load_icon(Path("data/icons/recent.png"), color)
        self.import_geometry_icon = load_icon(Path("data/icons/image-plus.png"), color)

        self.save_icon = load_icon(Path("data/icons/save.png"), color)
        self.save_as_icon = load_icon(Path("data/icons/save_as.png"), color)
        self.save_as_png_icon = load_icon(Path("data/icons/png.png"), color)

        self.theme_sun_icon = load_icon(Path("data/icons/sun_icon.png"), color)
        self.theme_moon_icon = load_icon(Path("data/icons/moon_icon.png"), color)
        self.capture_image_icon = load_icon(Path("data/icons/cube-scan.png"), color)
        self.exit_icon = load_icon(Path("data/icons/exit.png"), color)

        #
        self.new_project_action = QAction(self.new_project_icon, "New Project", self)
        self.load_project_action = QAction(self.load_project_icon, "Load Project", self)
        self.recent_action = QAction(self.recent_icon, "Recent", self)
        self.import_geometry_action = QAction(self.import_geometry_icon, "Import geometry", self)

        self.save_action = QAction(self.save_icon, "Save", self)
        self.save_as_action = QAction(self.save_as_icon, "Save as", self)

        self.capture_image_action = QAction(self.capture_image_icon, "Capture image", self)
        self.theme_action = QAction(self.theme_sun_icon, "Theme", self)
        self.exit_action = QAction(self.exit_icon, "Exit", self)

        #
        self.import_geometry_action.triggered.connect(self.import_geometry_callback)
        self.capture_image_action.triggered.connect(self.capture_image_callback)
        self.save_action.triggered.connect(self.save_callback)
        self.theme_action.triggered.connect(self.theme_callback)
        self.exit_action.triggered.connect(self.exit_callback)

    def create_layout(self):
        self.clear()
        self.addAction(self.new_project_action)
        self.addAction(self.load_project_action)
        self.addAction(self.recent_action)
        self.addAction(self.import_geometry_action)
        self.addSeparator()
        self.addAction(self.save_action)
        self.addAction(self.save_as_action)
        self.addSeparator()
        self.addAction(self.capture_image_action)
        self.addAction(self.theme_action)
        self.addAction(self.exit_action)

    def save_callback(self):
        self.parent().project.save()

    def help_callback(self):
        self.parent().viewer_tabs.show_help()

    def exit_callback(self):
        loaded_function = load_function(self.parent().project.long_function, self)
        loaded_function()
        self.solve_example_analisys_callback()

    def theme_callback(self):
        if self.parent().user_config.theme == "light":
            self.parent().set_theme("dark")
            self.theme_action.setIcon(self.theme_sun_icon)

        elif self.parent().user_config.theme == "dark":
            self.parent().set_theme("light")
            self.theme_action.setIcon(self.theme_moon_icon)

    def capture_image_callback(self):
        self.parent().capture_image()

    def import_geometry_callback(self):
        self.parent().import_geometry()

    # TODO: Create and connect actions for these
    def show_model_callback(self):
        self.parent().viewer_tabs.show_model()

    def show_example_callback(self):
        self.parent().viewer_tabs.show_example()

    #
    def solve_example_analisys_callback(self):
        self.parent().project.example_solver.solve()
        self.parent().viewer_tabs.show_example_analisys()
