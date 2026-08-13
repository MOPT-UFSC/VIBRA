from PySide6.QtWidgets import QApplication

from vibra import TEMP_PROJECT_DIR
from vibra.interface.splash_screen import SplashScreen
from vibra.utils.time_utils import warn_delay_since_start
from vibra.interface.data.icons.theme_resources import set_icon_theme


class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        warn_delay_since_start("Initialization before Splash Screen", maximum_time=1)

        # create the splash screen
        self.splash = SplashScreen(self)
        self.splash.show()
        self.processEvents()

        # global params
        from vibra.interface.config import Config

        self.config = Config()
        set_icon_theme(self.config.user_preferences.interface_theme)

        from vibra.engine.project import Project

        self.project = Project(TEMP_PROJECT_DIR)

        # gui
        from vibra.interface.main_window import MainWindow

        self.main_window = MainWindow()
        self.main_window.configure_main_window()
        self.filter_scroll_by_wheel_event()

    def filter_scroll_by_wheel_event(self):
        from PySide6.QtCore import QEvent, QObject
        from PySide6.QtWidgets import QComboBox, QTabBar

        class Filter(QObject):
            def eventFilter(self, obj, event):
                if event.type() != QEvent.Wheel:
                    return False

                widgets = [QTabBar, QComboBox]
                for widget in widgets:
                    if isinstance(obj, widget):
                        return True
                return False

        filter = Filter(self)
        self.installEventFilter(filter)
