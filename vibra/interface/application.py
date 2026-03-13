from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication

from vibra import TEMP_PROJECT_DIR
from vibra.engine.new_project import NewProject
from vibra.interface.config import Config
from vibra.interface.main_window import MainWindow
from vibra.interface.splash_screen import SplashScreen
from vibra.project_files.load_project import LoadProject
from vibra.project_files.old_project import OldProject
from vibra.project_files.project_file import ProjectFile

QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)


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

        self.new_project = NewProject(TEMP_PROJECT_DIR)

        self.file = ProjectFile(TEMP_PROJECT_DIR)
        self.old_project = OldProject(self.file)
        self.load_project = LoadProject()

        # gui
        self.main_window = MainWindow()
        self.main_window.configure_main_window()
        self.filter_tab_scroll_by_wheel()

    def filter_tab_scroll_by_wheel(self):
        from PySide6.QtCore import QEvent, QObject
        from PySide6.QtWidgets import QTabBar

        class Filter(QObject):
            def eventFilter(self, obj, event):
                if isinstance(obj, QTabBar) and (event.type() == QEvent.Wheel):
                    return True
                else:
                    return False

        filter = Filter(self)
        self.installEventFilter(filter)
