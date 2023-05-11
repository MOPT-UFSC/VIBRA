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
        self.view_up_icon = QIcon(str(Path("data/top.png")))
        self.view_down_icon = QIcon(str(Path("data/bottom.png")))
        self.view_right_icon = QIcon(str(Path("data/right.png")))
        self.view_left_icon = QIcon(str(Path("data/left.png")))
        self.view_back_icon = QIcon(str(Path("data/back.png")))
        self.view_front_icon =QIcon(str(Path("data/front.png")))
        self.view_orthogonal_icon = QIcon(str(Path("data/orthogonal.png")))
        self.view_mode_line_icon = QIcon(str(Path("data/lines.png")))
        self.view_mode_nodes_icon = QIcon(str(Path("data/nodes.png")))
        self.view_mode_face_icon = QIcon(str(Path("data/faces.png")))
        

        

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
        self.view_up_action = QAction(self.view_up_icon, "Up View", self)
        self.view_down_action = QAction(self.view_down_icon, "Down View", self)
        self.view_left_action = QAction(self.view_left_icon, "Left View", self)
        self.view_right_action = QAction(self.view_right_icon, "Right View", self)
        self.view_front_action = QAction(self.view_front_icon, "Front View", self)
        self.view_back_action = QAction(self.view_back_icon, "Back View", self)
        self.view_orthogonal_action = QAction(self.view_orthogonal_icon, "Orthogonal View", self)
        self.view_mode_face_icon = QAction(self.view_mode_face_icon, "Face View", self)
        self.view_mode_line_icon = QAction(self.view_mode_line_icon, "Line View", self)
        self.view_mode_nodes_icon = QAction(self.view_mode_nodes_icon, "Node View", self)
        self.save_action.triggered.connect(self.project.save)
        self.help_action.triggered.connect(self.show_help_window)

    def create_basic_layout(self):
        self.viewer_3d = Viewer3D()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        self.project_menu = menu_bar.addMenu("Project")
        self.views_menu = menu_bar.addMenu("Views")
        self.views_mode_menu = menu_bar.addMenu("View Mode")
        self.help_menu = menu_bar.addMenu("Help")
        
        self.load_project_menu()
        self.load_views_menu()
        self.load_help_menu()
        self.load_views_mode_menu()

    def load_project_menu(self):
        self.project_menu.clear()
        self.project_menu.addAction(self.vibra_action)
        self.project_menu.addAction(self.file_import_action)
        self.project_menu.addAction(self.save_action)
        self.project_menu.addAction(self.save_as_action)
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
        self.views_mode_menu.addAction(self.view_mode_nodes_icon)
        self.views_mode_menu.addAction(self.view_mode_line_icon)
        self.views_mode_menu.addAction(self.view_mode_face_icon)

    def load_help_menu(self):
        self.help_menu.addAction(self.help_action)

    def show_help_window(self):
        help_window = HelpWindow()
        help_window.exec()
