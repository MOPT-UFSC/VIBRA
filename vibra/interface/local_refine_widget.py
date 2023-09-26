from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
)



class LocalRefineWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.banana = QLabel("banana")
        self.maca = QLabel("maçã")
        self.botao_mesh_size = QPushButton("texto")
        self.textbox = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.banana)
        layout.addWidget(self.maca)
        layout.addWidget(self.botao_mesh_size)
        layout.addWidget(self.textbox)
        self.setLayout(layout)
        self.resize(500,500)



        self.botao_mesh_size.clicked.connect(self.botao_mesh_size_callback)






        self.exec_()

    def botao_mesh_size_callback(self):
        # print("banana")
        self.banana.setText("alala")
    