from PySide6.QtCore import Qt, QTimer

from vibra import app
from vibra.interface.ui_generated.messages.print_message_ui import PrintMessage_UI
from vibra.interface.formatters.icons import get_error_icon, get_warning_icon

from time import sleep, time 

class PrintMessageInput(PrintMessage_UI):
    def __init__(self, text_info, *args, **kwargs):
        super().__init__()

        self.auto_close = kwargs.get("auto_close", False)
        self.window_title, self.title, self.message = text_info

        self._config_window()
        self._define_qt_variables()
        self._create_connections()

        self._config_widgets()
        self._set_texts()
        self._adjust_size(kwargs)

        if kwargs.get("exec", True):
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _define_qt_variables(self):
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
        self.label_message.adjustSize()
        self.label_message.setMargin(12)

        if self.window_title in ["Error", "ERROR"]:
            icon = get_error_icon()
        elif self.window_title in ["Warning", "WARNING"]:
            icon = get_warning_icon()
        else:
            icon = app().main_window.vibra_icon

        self.setWindowIcon(icon)
        self.setWindowTitle(self.window_title)

        self.adjustSize()
        self.label_message.setAlignment(Qt.AlignCenter)
        if self.auto_close:
            self.timer.timeout.connect(self.message_close)
            self.timer.start(50)

    def _adjust_size(self, kwargs: dict):

        height = kwargs.get("height", None)
        if isinstance(height, int):
            self.setFixedHeight(height)

        width = kwargs.get("width", None)
        if isinstance(width, int):
            self.setFixedWidth(width)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.message_close()
        elif event.key() == Qt.Key_Escape:
            self.close()