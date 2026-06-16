from PySide6.QtCore import Qt

from vibra.interface.ui_generated.project.splash_ui import Splash_UI


class SplashScreen(Splash_UI):
    def __init__(self, parent):
        super().__init__()

        self._config_widget()
        self.update_position(parent)
        self.update_progress(5)

    def _config_widget(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.progressBar.setStyleSheet("""  
            QProgressBar{background-color : rgba(255, 255, 255, 0); border-radius: 6px; border-style: ridge; border-width: 0px;}
            QProgressBar::chunk {background-color : rgb(45, 110, 190); border-radius: 6px; border-style: ridge; border-width: 0px;}
            """)

    def update_position(self, app):
        desktop_geometry = app.primaryScreen().geometry()
        pos_x = int((desktop_geometry.width() - self.width()) / 2)
        pos_y = int((desktop_geometry.height() - self.height()) / 2)
        self.setGeometry(pos_x, pos_y, self.width(), self.height())

    def update_progress(self, value : int):
        self.progressBar.setValue(value)