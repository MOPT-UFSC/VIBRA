from PyQt5.QtWidgets import QApplication, QMainWindow

def get_main_window():
    """
    Returns the instance of the MainWindow from children.
    Very usefull to keep menus uncoupled from each other.
    """
    for w in QApplication.topLevelWidgets():
        if isinstance(w, QMainWindow):
            return w
    raise RuntimeError("Count not find MainWindow instance.")
