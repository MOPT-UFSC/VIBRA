from PySide6.QtWidgets import QApplication

from vibra import TEMP_PROJECT_DIR
from vibra.interface.splash_screen import SplashScreen


class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the splash screen
        self.splash = SplashScreen(self)
        self.splash.show()
        self.processEvents()

        # global params
        from vibra.interface.config import Config

        self.config = Config()

        from vibra.engine.project import Project

        self.project = Project(TEMP_PROJECT_DIR)

        # gui
        from vibra.interface.main_window import MainWindow

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
