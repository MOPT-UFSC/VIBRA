from PyQt5.QtWidgets import QMainWindow
from pathlib import Path
from PyQt5.QtGui import QIcon
from vibra.interface.viewer_3d.viewer_3d import Viewer3D
from PyQt5.QtWidgets import QAction

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.load_icons()
        self.config()
        self.create_actions()
        self.create_basic_layout()
        self.create_menu_bar()
        

        
    
    def load_icons(self):
        self.vibra_icon = QIcon(str(Path("data/vibra.ico")))  #logo do vibra
        self.help_icon = QIcon(str(Path("data/help.png")))
        self.new_project_icon = QIcon(str(Path("data/new-file.png")))
        self.file_import_icon = QIcon(str(Path("data/file-import.png")))
        self.exit_import_icon = QIcon(str(Path("data/door-exit.png")))
        self.save_icon = QIcon(str(Path("data/save-solid.png")))
        self.save_as_icon = QIcon(str(Path("data/save_blue.png")))

    def config(self):
        self.showMaximized()
        self.setWindowIcon(self.vibra_icon)
        self.setWindowTitle("Vibra")
    
    def create_actions(self):
        self.vibra_icon = QAction(self.new_project_icon, "New Project", self)
        self.file_import = QAction(self.file_import_icon, "Import Project", self)
        self.exit_import_icon = QAction(self.exit_import_icon, "Exit", self)
        self.save_icon = QAction(self.save_icon, "Save", self)
        self.save_as_icon = QAction(self.save_as_icon, "Save as", self)
        self.help_icon = QAction(self.help_icon , "About Vibra" , self)


    def create_basic_layout(self):
        self.viewer_3d = Viewer3D()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        self.project_menu = menu_bar.addMenu("Project")
        self.help_menu = menu_bar.addMenu("Help")
        self.load_project_menu()

    def load_project_menu(self):
        self.project_menu.clear()
        self.project_menu.addAction(self.vibra_icon)
        self.project_menu.addAction(self.file_import)
        self.project_menu.addAction(self.save_icon)
        self.project_menu.addAction(self.save_as_icon)
        self.project_menu.addAction(self.exit_import_icon)
        self.help_menu.addAction(self.help_icon)





    
