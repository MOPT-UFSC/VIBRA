from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget


class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vibra")
        layout = QVBoxLayout(self)
        texto = QLabel()
        texto.setText("texto do vibra")
        layout.addWidget(texto)
