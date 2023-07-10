from PyQt5.QtWidgets import QMessageBox

from vibra.errors import VibraException


class CommonExceptionMessage(QMessageBox):
    def __init__(self, exception):
        self.setText(str(exception))
        if isinstance(exception, VibraException):
            self.setInformativeText(exception.context)


class ErrorMessage(CommonExceptionMessage):
    def __init__(self, exception):
        super().__init__(exception)
        self.setWindowTitle("Error")
        self.setIcon(QMessageBox.Critical)
        self.exec()


class WarningMessage(CommonExceptionMessage):
    def __init__(self, exception):
        super().__init__(exception)
        self.setWindowTitle("Warning")
        self.setIcon(QMessageBox.Warning)
        self.exec()
