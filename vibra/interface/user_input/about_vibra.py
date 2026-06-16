from PySide6.QtGui import QCloseEvent, QDesktopServices
from PySide6.QtCore import Qt, QUrl

from vibra import app, RELEASE_DATE, VERSION
from vibra.interface.ui_generated.menu.about_vibra_ui import AboutVibra_UI
from vibra.interface.general.print_message_input import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class AboutVibraInput(AboutVibra_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._define_logo_variables()
        self.update_logo_text()
        self._create_connections()
        self.adjustSize()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("VIBRA")
    
    def _initialize(self):
        self.keep_window_open = True

        self.version_info = f"v{VERSION} {RELEASE_DATE}"
        self.licensing_info = "Copyright (c) 2024 Project VIBRA Contributors, GPL v3 License."
        
        self.main_info = "Vibra is an open-source software developed in Python for modeling vibroacoustic problems using the Finite Element Method (FEM).  "
        self.main_info += "In its current version, the software has been validated for performing modal analysis, complex modal analysis, and time-harmonic analysis of linear acoustic problems. "
        self.main_info += "Further information is available in the VIBRA repository at GitHub"

    def _define_qt_variables(self):
        self.label_licensing_information.setText(self.licensing_info)
        self.label_main_info.setText(self.main_info)
        self.label_version_information.setText(self.version_info)

    def _create_connections(self):
        self.pushButton_repository.clicked.connect(self.open_gitHub_repository)
        app().main_window.theme_changed.connect(self.update_logo_text)
    
    def _define_logo_variables(self):
        self.light_logo_text = """<html><head/><body style=\"font-size: 35pt; font-family: 'Bauhaus 93';
                                \"><p><span style=\" color:#0055ff;\">V</span><span style=\" color:#4F4F4F;\">IBRA</span></p></body></html>"""
    
        self.dark_logo_text = """<html><head/><body style=\"font-size: 35pt; font-family: 'Bauhaus 93';
                                \"><p><span style=\" color:#0055ff;\">V</span><span style=\" color:#c8c8c8;\">IBRA</span></p></body></html>"""

    def update_logo_text(self):
        if app().config.user_preferences.interface_theme == "dark":
            self.logo_label.setText(self.dark_logo_text)
        else:
            self.logo_label.setText(self.light_logo_text)

    def open_gitHub_repository(self):
        title = "Error reached while trying to access the project repository"

        try:
            self.hide()
            url = QUrl('https://github.com/MOPT-UFSC/VIBRA') 
            if not QDesktopServices.openUrl(url):
                message = "The VIBRA repository at the GitHub's site cannot be accessed.\n"
                message += "We recommend trying again later."
                PrintMessageInput([title, message, window_title_1])

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])

        self.close()

    def continueButtonEvent(self):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.open_gitHub_repository()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)