from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication

from vibra import ICON_DIR, UI_DIR
from vibra.interface.config import Config
from vibra.interface.main_window import MainWindow
from vibra.interface.splash_screen import SplashScreen


class Application(QApplication):
    selection_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the splash screen
        self.splash = SplashScreen(self)
        self.splash.show()
        self.processEvents()

        # global params
        self.config = Config()

        # gui
        self.main_window = MainWindow()
        self.main_window.configure_main_window()

        self.update()

    def update(self):
        return
        self.geometry_toolbox.update()
        self.main_window.update()