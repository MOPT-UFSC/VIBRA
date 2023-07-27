from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QGridLayout, QScrollArea, QPushButton, QDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

class MaterialWidget(QDialog):
    def __init__(self):
        super().__init__()


        toolbar_layout = QHBoxLayout()
        icon1_button = QPushButton("Icon 1")
        icon1_button.setFixedSize(50, 50)  
        icon1_button.clicked.connect(self.open_widget1)
        toolbar_layout.addWidget(icon1_button)

        icon2_button = QPushButton("Icon 2")
        icon2_button.setFixedSize(50, 50)  
        icon2_button.clicked.connect(self.open_widget2)
        toolbar_layout.addWidget(icon2_button)

        toolbar_layout.addStretch(1)
        reset_button = QPushButton("Reset")
        reset_button.setFixedSize(50, 50)
        reset_button.clicked.connect(self.reset_widgets)
        toolbar_layout.addWidget(reset_button)

        toolbar_layout.setAlignment(Qt.AlignTop)

        no_list = ["Name", "Id", "Density[kg/m3]", "Young Modulus[GPa]", "Poisson", "Expansion cofficient[m/K]", "Color"]
        self.table = QTableWidget()
        self.table.setColumnCount(len(no_list))
        self.table.setRowCount(1)  
        self.table.setHorizontalHeaderLabels(no_list)
        self.table.setItem(0,0,QTableWidgetItem(1))
        self.table.resizeColumnsToContents()
        main_layout = QVBoxLayout()
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)
        self.setMinimumSize(610,500)
          

        self.exec_()

    def open_widget1(self):
        self.table.setRowCount(2)
        
    def open_widget2(self):
        self.table.setRowCount(3)

    def reset_widgets(self):
        for widget in self.findChildren(QWidget):
            if isinstance(widget, QDialog):
                widget.reject()
