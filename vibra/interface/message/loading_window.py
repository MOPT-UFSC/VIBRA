import logging
import re
from typing import Callable

from PySide6.QtCore import QEvent, QObject, QRunnable, Qt, QThread, QThreadPool, Signal
from PySide6.QtWidgets import QApplication

from vibra.interface.ui_generated.messages.loading_window_ui import LoadingWindow_UI

# Catches every message that contains something like [n/N]
PROGRESS_FRACTION_REGEX = re.compile(r"(?<=\[)\d+/\d+(?=\])")


class LoadTask:
    """
    Decorator to run a function while displaying a loading window.

    The decorated functions runs in a secondary thread by default,
    but if you pass use_threads=False it will run in the main thread.
    To update functions that affect the interface you need to run it
    in the main thread to avoid deadlocks.

    The loading window label and progress bar will be updated according
    to the logging messages that contains the text "[n/N]", representing
    the fraction of the task that has already been completed.
    """
    def __init__(self, function: Callable, *, allow_cancel=False, use_threads=True):
        super().__init__()
        self.function = function
        self.allow_cancel = allow_cancel
        self.use_threads = use_threads

    def run(self, *args, **kwargs):
        # If it is already running in another thread, just run 
        # the function without creating any window
        if not self.on_main_thread():
            return self.function(*args, **kwargs)

        loading_window = LoadingWindow(self.allow_cancel)
        loading_window.canceled.connect(self.cancel_callback)

        # Creates a handler to update progress_bar and progress_label
        # every time a logging containing [n/N] appears
        progress_log_handler = ProgressBarLogUpdater(
            logging.DEBUG, loading_window=loading_window
        )
        logging.getLogger().addHandler(progress_log_handler)

        # Starts using the wait cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        worker = Worker(self.function, *args, **kwargs)
        worker.signal.finished.connect(loading_window.close)

        if self.use_threads:
            threadpool = QThreadPool()
            threadpool.start(worker)
            loading_window.exec()
        else:
            loading_window.show()
            QApplication.processEvents()  # Flushes the event loop to avoid freezing
            worker.run()

        # Restores the previous cursor
        QApplication.restoreOverrideCursor()

        # Removes the logging handler as it is not necessary anymore
        logging.getLogger().removeHandler(progress_log_handler)

        # If there was an exception in the loaded function, raise it
        if worker.exception is not None:
            raise worker.exception

        # Otherwise just return the result
        return worker.result

    def set_cancel_callback(self, callback: Callable):
        # Yes, python allows me to just override the method like this
        self.cancel_callback = callback

    def cancel_callback(self): ...

    def on_main_thread(self):
        return QThread.currentThread() == QApplication.instance().thread()

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)


class LoadingWindow(LoadingWindow_UI):
    """
    Loading window that shows a progress bar and a label
    """

    canceled = Signal()

    def __init__(self, allow_cancel=False):
        super().__init__()
        self.show()

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowMinimizeButtonHint
        )

        # Controls if the X button to close the window is enabled
        if allow_cancel:
            self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, on=True)

        self.update_position()

    def update_position(self):
        """
        Position the window on the center of the screen.
        """
        desktop_geometry = QApplication.primaryScreen().size()
        pos_x = int((desktop_geometry.width() - self.width()) / 2)
        pos_y = int((desktop_geometry.height() - self.height()) / 2)
        self.setGeometry(pos_x, pos_y, self.width(), self.height())

    def closeEvent(self, event: QEvent):
        # This means that window was closed by the user, not by code
        if event.spontaneous():
            self.canceled.emit()


# QRunnable is not a QObject, so I need this
# workaround to be able to emit signals
class WorkerSignal(QObject):
    finished = Signal()
    error = Signal(Exception)


class Worker(QRunnable):
    """
    Class needed to run a function using QThreadPool
    """

    def __init__(self, function: Callable, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.exception = None
        self.signal = WorkerSignal()

    def run(self):
        try:
            self.result = self.function(*self.args, **self.kwargs)
        except Exception as e:
            self.exception = e
            self.signal.error.emit(e)
        finally:
            self.signal.finished.emit()


class ProgressBarLogUpdater(logging.Handler):
    """
    This class is an log observer. It is meant to watch logs
    and use it to update an instance of LoadingWindow
    """

    def __init__(self, level=0, *, loading_window: LoadingWindow | None = None) -> None:
        super().__init__(level)
        self.loading_window = loading_window

    def emit(self, record):
        """
        This function is fired when something is logged.
        If the log have a marker like [n/N] or "..." in its message it
        will update the LoadingWindow associated with this class.
        """

        if self.loading_window is None:
            return

        # Updates QT to prevent freezing
        QApplication.processEvents()

        percent = self.get_percentage(record.msg)

        if percent is not None:
            self.loading_window.progress_label.setText(record.msg)
            self.loading_window.progress_bar.setValue(percent)

        elif "..." in record.msg:
            self.loading_window.progress_label.setText(record.msg)

        # Updates QT to show the window modifications
        QApplication.processEvents()

    def get_percentage(self, message: str):
        """
        Uses regex to check if the message have a marker like [2/10]
        If it does, it extracts the step (2) and the max_step (10) and
        calculates the percentage (20%).
        Otherwise it just returns None.
        """

        if not isinstance(message, str):
            return

        first_match = PROGRESS_FRACTION_REGEX.search(message)
        if first_match:
            step, max_step = map(int, first_match.group().split("/"))
            return 100 * int(step) // int(max_step)

        return None
