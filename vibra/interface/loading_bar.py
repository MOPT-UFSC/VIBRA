import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)
from time import sleep
from vibra.utils import ProgressStatus


class ProgressBarLogUpdater(logging.Handler):
    '''
    This class is an log observer. It is meant to watch logs 
    and use it to update a progressbar and/or some labels.
    '''

    def __init__(self, level=0, *, progress_bar=None, label=None) -> None:
        super().__init__(level)
        self.progress_bar = progress_bar
        self.label = label

    def emit(self, record):
        if not isinstance(record.msg, ProgressStatus):
            return

        if self.label is not None:
            self.label.setText(record.msg.message)
            QApplication.processEvents()

        if self.progress_bar is not None:
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


def load_function(function, parent):
    '''
    This function works just like a decorator.

    The function passed is transformed so it will show a
    progressbar while running. The text and progress of the 
    progressbar is given by logs containing ProgressStatus 
    class in it.
    
    I know that this isn't an elegant solution, and I hope
    someone, someday can fix this. But I just can't figure
    out a better way to create a working loading bar.
    to redeem myself for this monstruosity I am explaining
    every step, but I really hope no one ever need to 
    modify this.

    Example:
    --------

    loaded_func = self.load_function(func)
    loaded_func(args, of, the, original=0, function=1)
    '''
    
    # Creates the modified function that does the same
    # thing as the input function, but while updating
    # a loading bar 
    def wrapper(*args, **kwargs):

        # Creates a loading window
        loading_window = LoadingWindow(parent)

        # Creates a handler to update the loading bar
        # every time a progress log appears
        progress_handler = ProgressBarLogUpdater(
            progress_bar=loading_window.progress_bar, 
            label=loading_window.text_label
        )
        progress_handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(progress_handler)

        try:
            # Waits some previous pyqt window and update
            sleep(0.1)
            QApplication.processEvents()

            # Changes the cursor to wait
            QApplication.setOverrideCursor(Qt.WaitCursor)

            # Shows the empty progress bar
            loading_window.show()

            # Waits the loading bar to appear and uptates pyqt
            sleep(0.1)
            QApplication.processEvents()

            # Calls the actual function
            function(*args, **kwargs)

            # Shows the full progress bar and closes
            loading_window.progress_bar.setValue(100)
            sleep(0.1)  # A small delay so we can see the 100%
            loading_window.hide()

            # Returns the value to 0 for the next use
            loading_window.progress_bar.setValue(0)

            # Restores the previous cursor
            QApplication.restoreOverrideCursor()

        except AttributeError:
            logging.warn("No loading window found")

        finally:
            logging.getLogger().removeHandler(progress_handler)

    return wrapper
