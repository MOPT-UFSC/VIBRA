from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QColorDialog,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)



class LocalRefineWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.banana = QLabel("banana")
        self.maca = QLabel("maçã")
        self.apply_button = QPushButton("Apply")
        self.global_mesh_size_textbox = QLineEdit()
        
        # apply_button
        
        self.apply_button.resize





        # header
        header = ["Refining mesh size", "Faces list"]
        self.table = QTableWidget()
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        self.table.resizeColumnsToContents()
        # self.table.














        layout = QVBoxLayout()
        layout.addWidget(self.banana)
        layout.addWidget(self.maca)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.global_mesh_size_textbox)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.setWindowTitle("Mesh parameters")
        self.resize(500,500)

        self.apply_button.clicked.connect(self.apply_button_callback)

        self.exec_()

    def apply_button_callback(self):
        self.banana.setText("Changes applied")
    