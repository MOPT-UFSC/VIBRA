from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication

from vibra import TEMP_PROJECT_FILE
from vibra.interface.config2 import Config
from vibra.interface.main_window import MainWindow
from vibra.interface.splash_screen import SplashScreen

from vibra.project_files.load_project import LoadProject
from vibra.project_files.project import Project
from vibra.project_files.project_file import ProjectFile

class Application(QApplication):
    selection_changed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the splash screen
        self.splash = SplashScreen(self)
        self.splash.show()
        self.processEvents()

        # global params
        self.config = Config()

        self.file = ProjectFile(TEMP_PROJECT_FILE)
        self.project = Project()
        self.load_project = LoadProject()

        # gui
        self.main_window = MainWindow()
        self.main_window.configure_main_window()

        self.update()
        self.filter_tab_scroll_by_wheel()

    def update(self):
        return
        self.geometry_toolbox.update()
        self.main_window.update()

    def filter_tab_scroll_by_wheel(self):
        from PySide6.QtWidgets import QTabBar
        from PySide6.QtCore import QObject, QEvent

        class Filter(QObject):
            def eventFilter(self, obj, event):
                if isinstance(obj, QTabBar) and (event.type() == QEvent.Wheel):
                    return True
                else:
                    return False

        filter = Filter(self)
        self.installEventFilter(filter)
