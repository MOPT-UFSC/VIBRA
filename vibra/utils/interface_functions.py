from PySide6.QtWidgets import QApplication, QMainWindow

import vibra.interface.main_window as main_window


def get_main_window():
    """
    Returns the instance of the MainWindow from children.
    Very usefull to keep menus uncoupled from each other.
    """
    for w in QApplication.topLevelWidgets():
        if isinstance(w, main_window.MainWindow):
            return w
    raise RuntimeError("Count not find MainWindow instance.")
