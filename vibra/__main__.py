import logging
import sys

from PyQt5.QtWidgets import QApplication

from vibra.interface.main_window import MainWindow


def configure_logs():
    """
    Configures the logging library.
    Format includes time, log level (info, debug, error and so on).

    The main level is set to NOSET, so every handler can select its
    own filters.
    """
    formatter = logging.Formatter("%(asctime)s \t | %(levelname)s \t | %(message)s")
    file_handler = logging.FileHandler("logs.log", "w+")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)
    logger.addHandler(file_handler)


if __name__ == "__main__":
    configure_logs()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
