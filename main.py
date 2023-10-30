import logging
import os
import sys

import vtk
from PyQt5.QtWidgets import QApplication

from vibra.interface.main_window import MainWindow


def configure_logs():
    """
    Configures the logging library.
    Format includes time, log level (info, debug, error and so on).

    The main level is set to NOSET, so every handler can select its
    own filters.

    All info logs are saved in the file, but only warnings or error
    are shown to users.
    """
    file_formatter = logging.Formatter("%(asctime)s \t | %(levelname)s \t | %(message)s")
    file_handler = logging.FileHandler("logs.log", "w+")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    stream_formatter = logging.Formatter(logging.BASIC_FORMAT)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARN)
    stream_handler.setFormatter(stream_formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


if __name__ == "__main__":
    configure_logs()

    # disables the terrible vtk error handler and its logs
    # you may want to enable them while debugging something
    vtk.vtkObject.GlobalWarningDisplayOff()
    vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)

    # Make the window scale evenly for every monitor
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())