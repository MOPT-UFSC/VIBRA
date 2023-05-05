from PySide6 import QtWidgets

from vibra.interface.main_window import MainWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()