import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget

from vibra.utils import ProgressStatus


class ProgressBarLogUpdater(logging.Handler):
    def __init__(self, level=0, *, progress_bar=None) -> None:
        super().__init__(level)
        self.progress_bar = progress_bar

    def emit(self, record):
        if not isinstance(record.msg, ProgressStatus):
            return

        if self.progress_bar is None:
            return

        percentage = 100 * record.msg.step // record.msg.max_steps
        self.progress_bar.setValue(percentage)


class LoadingWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_label = QLabel(self)
        self.progress_bar = QProgressBar(self)

        layout = QVBoxLayout()
        layout.addWidget(self.text_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        self.customize_style()
        self.configure_window()

    def customize_style(self):
        self.text_label.setAlignment(Qt.AlignCenter)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 3px solid grey;
                border-radius: 13px;
                text-align: center;
                background-color: grey;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #0055DD;
                border-top-right-radius: 10px;
                border-top-left-radius: 10px;
                border-bottom-right-radius: 10px;
                border-bottom-left-radius: 10px;
            }
        """
        )

    def configure_window(self):
        self.setWindowTitle("Loading")
        self.setGeometry(200, 200, 400, 150)

        self.setWindowFlags(
            Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowStaysOnTopHint
        )
