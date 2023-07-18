from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QGridLayout, QScrollArea, QPushButton, QDialog, QHBoxLayout

class MaterialWidget(QDialog):
    def __init__(self):
        super().__init__()

        # Create the toolbar
        toolbar_layout = QHBoxLayout()
        icon1_button = QPushButton("Icon 1")
        icon1_button.setFixedSize(50, 50)  # Definir tamanho quadrado
        icon1_button.clicked.connect(self.open_widget1)
        toolbar_layout.addWidget(icon1_button)

        icon2_button = QPushButton("Icon 2")
        icon2_button.setFixedSize(50, 50)  # Definir tamanho quadrado
        icon2_button.clicked.connect(self.open_widget2)
        toolbar_layout.addWidget(icon2_button)

        icon3_button = QPushButton("Icon 3")
        icon3_button.setFixedSize(50, 50)  # Definir tamanho quadrado
        icon3_button.clicked.connect(self.open_widget3)
        toolbar_layout.addWidget(icon3_button)

        toolbar_layout.setAlignment(Qt.AlignTop)

        # Create the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(toolbar_layout)
        self.setLayout(main_layout)
        self.setFixedSize(500, 500)

        self.exec_()

    def open_widget1(self):
        widget1 = QDialog()
        widget1.exec_()

    def open_widget2(self):
        widget2 = QDialog()
        widget2.exec_()

    def open_widget3(self):
        widget3 = QDialog()
        widget3.exec_()
