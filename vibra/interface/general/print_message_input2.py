from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QProgressBar, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.interface.formatters.icons import *

from time import sleep, time 

class PrintMessageInput(QDialog):
    def __init__(self, text_info, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "messages/print_message.ui"
        uic.loadUi(ui_path, self)

        self.auto_close = kwargs.get("auto_close", False)
        self.window_title, self.title, self.message = text_info
                
        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()

        self.project = self.main_window.project
        self.model = self.project.model
        self.properties = self.model.properties

        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self._set_texts()
        self.exec()

    def _load_icons(self):
        self.icon = app().main_window.vibra_icon

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)

    def _define_qt_variables(self):

        # QFrame
        self.frame_button : QFrame
        self.frame_message : QFrame
        self.frame_progress_bar : QFrame
        self.frame_title : QFrame

        # QLabel
        self.label_title : QLabel
        self.label_message : QLabel

        # QProgressBar
        self.progress_bar_timer : QProgressBar

        # QPushButton
        self.pushButton_close : QPushButton

        # QTimer
        self.timer = QTimer()

    def _create_connections(self):
        self.pushButton_close.clicked.connect(self.message_close)
        self.timer.timeout.connect(self.update_progress_bar)

    def _config_widgets(self):

        if self.auto_close:
            self.frame_button.setVisible(False)
        else:
            self.frame_progress_bar.setVisible(False)

        self.pushButton_close.setVisible(True)

    def message_close(self):
        self.timer.stop()
        self.close()

    def update_progress_bar(self):
        self.timer.stop()
        t0 = time()
        elapsed_time = 0
        duration = 2.5
        while elapsed_time <= duration:
            sleep(0.1)
            elapsed_time = time() - t0
            value = int(100*(elapsed_time/duration))
            self.progress_bar_timer.setValue(value)
        self.close()

    def _set_texts(self):
        self.title2 = f"   {self.title}   "
        self.label_title.setText(self.title2)
        self.label_message.setText(self.message)
        self.setWindowTitle(self.window_title)

        if self.window_title in ["Error", "ERROR"]:
            icon = get_error_icon(QColor(255,0,0,200))
            self.setWindowIcon(icon)
        elif self.window_title in ["Warning", "WARNING"]:
            icon = get_warning_icon()
            self.setWindowIcon(icon)
        
        self.adjustSize()
        self.label_message.setAlignment(Qt.AlignCenter)
        if self.auto_close:
            self.timer.timeout.connect(self.message_close)
            self.timer.start(50) 

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.message_close()
        elif event.key() == Qt.Key_Escape:
            self.close()


# class PrintMessageInput(QDialog):
#     def __init__(self, text_info, auto_close=False, *args, **kwargs):
#         super().__init__()

#         uic.loadUi(Path('data/ui_files/general/print_messages2.ui'), self)

#         self.window_title, self.title, self.message = text_info
#         self.auto_close = auto_close

#         self._load_icons()
#         self._config_window()
#         self._define_qt_variables()
#         self._set_texts()
#         self.exec()

#     def _load_icons(self):
#         icons_path = str(Path("data/icons/logo_vibra.png"))
#         self.icon = QIcon(icons_path)

#     def _config_window(self):
#         self.setWindowIcon(self.icon)
#         self.setWindowFlags(Qt.WindowStaysOnTopHint)
#         self.setWindowModality(Qt.WindowModal)

#     def _define_qt_variables(self):
#         self.frame_message = self.findChild(QFrame, 'frame_message')
#         self.frame_title = self.findChild(QFrame, 'frame_title')
#         self.label_title = self.findChild(QLabel, 'label_title')
#         self.label_message = self.findChild(QLabel, 'label_message')
#         self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
#         self.timer = QTimer()
#         self.pushButton_close.clicked.connect(self.message_close)
#         self.pushButton_close.setVisible(True)

#     def _set_texts(self):
#         self.title2 = f"   {self.title}   "
#         self.label_message.setMargin(12)
#         self.label_title.setText(self.title2)
#         self.label_message.setText(self.message)
#         self.setWindowTitle(self.window_title)
#         self.adjustSize()
#         self.label_message.setAlignment(Qt.AlignJustify)
#         self.label_message.setAlignment(Qt.AlignVCenter)
#         if self.auto_close:
#             # self.pushButton_close.setVisible(False)
#             self.timer.timeout.connect(self.message_close)
#             self.timer.start(2000)

#     def message_close(self):
#         self.timer.stop()
#         self.close()

#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
#             self.message_close()
#         elif event.key() == Qt.Key_Escape:
#             self.close()