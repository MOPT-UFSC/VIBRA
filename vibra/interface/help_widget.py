from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget


class HelpWidget(QWidget):
    def __init__(self):
        super().__init__()

        texto = QLabel()
        texto.setText("Texto de ajuda do vibra.")

        layout = QVBoxLayout(self)
        layout.addWidget(texto)
