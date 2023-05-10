from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow

from vibra.interface.help_window import HelpWindow
from vibra.interface.viewer_3d.viewer_3d import Viewer3D
from vibra.project import Project


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.project = Project()
        self.load_icons()
        self.config()
        self.create_actions()
        self.create_basic_layout()
        self.create_menu_bar()

    def load_icons(self):
        self.vibra_icon = QIcon(str(Path("data/vibra.ico")))  # logo do vibra
        self.help_icon = QIcon(str(Path("data/help.png")))
        self.new_project_icon = QIcon(str(Path("data/new-file.png")))
        self.file_import_icon = QIcon(str(Path("data/file-import.png")))
        self.exit_import_icon = QIcon(str(Path("data/door-exit.png")))
        self.save_icon = QIcon(str(Path("data/save-solid.png")))
        self.save_as_icon = QIcon(str(Path("data/save_blue.png")))

    def config(self):
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setWindowIcon(self.vibra_icon)
        self.setWindowTitle("Vibra")

    def create_actions(self):
        self.vibra_action = QAction(self.new_project_icon, "New Project", self)
        self.file_import_action = QAction(self.file_import_icon, "Import Project", self)
        self.exit_import_action = QAction(self.exit_import_icon, "Exit", self)
        self.save_action = QAction(self.save_icon, "Save", self)
        self.save_as_action = QAction(self.save_as_icon, "Save as", self)
        self.help_action = QAction(self.help_icon, "About Vibra", self)
        self.view_up = QAction("Up View", self)
        self.view_down = QAction("Down View", self)
        self.view_left = QAction("Left View", self)
        self.view_right = QAction("Right View", self)
        self.view_orthogonal = QAction("Orthogonal View", self)
        self.view_front = QAction("Front View", self)
        self.view_back = QAction("Back View", self)
        self.save_action.triggered.connect(self.project.save)
        self.help_action.triggered.connect(self.show_help_window)

    def create_basic_layout(self):
        self.viewer_3d = Viewer3D()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        self.project_menu = menu_bar.addMenu("Project")
        self.help_menu = menu_bar.addMenu("Help")
        self.views_menu = menu_bar.addMenu("Views")
        self.load_project_menu()
        self.load_views_menu()
        self.load_help_menu()

    def load_project_menu(self):
        self.project_menu.clear()
        self.project_menu.addAction(self.vibra_action)
        self.project_menu.addAction(self.file_import_action)
        self.project_menu.addAction(self.save_action)
        self.project_menu.addAction(self.save_as_action)
        self.project_menu.addAction(self.exit_import_action)

    def load_views_menu(self):
        self.views_menu.addAction(self.view_up)
        self.views_menu.addAction(self.view_down)
        self.views_menu.addAction(self.view_left)
        self.views_menu.addAction(self.view_right)
        self.views_menu.addAction(self.view_front)
        self.views_menu.addAction(self.view_back)
        self.views_menu.addAction(self.view_orthogonal)

    def load_help_menu(self):
        self.help_menu.addAction(self.help_action)

    def show_help_window(self):
        help_window = HelpWindow()
        help_window.exec()
