from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLineEdit, QColorDialog, QLabel, QVBoxLayout, QWidget, QGridLayout, QScrollArea, QPushButton, QDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from pathlib import Path
from vibra.utils.icons import load_icon

class MaterialWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set Material")
        color = QColor("#0055DD")


        toolbar_layout = QHBoxLayout()
        add_material_button = QPushButton()
        add_material_button.setFocusPolicy(Qt.NoFocus)
        add_material_icon = load_icon(Path("data/icons/plus-thick.png"), color)
        add_material_button.setIconSize(QSize(25, 25))
        add_material_button.setIcon(add_material_icon)
    
        
        add_material_button.setFixedSize(25, 25)  
        add_material_button.clicked.connect(self.add_material)
        toolbar_layout.addWidget(add_material_button)

        trash_button = QPushButton()
        trash_button.setFocusPolicy(Qt.NoFocus)
        trash_icon = load_icon(Path("data/icons/delete.png"), color)
        trash_button.setIconSize(QSize(25, 25))
        trash_button.setIcon(trash_icon)
        trash_button.setFixedSize(25, 25)  
        trash_button.clicked.connect(self.open_widget2)
        toolbar_layout.addWidget(trash_button)

        toolbar_layout.addStretch(1)
        reset_button = QPushButton("Reset")
        reset_button.setFocusPolicy(Qt.NoFocus)
        reset_button.setFixedSize(50, 25)
        reset_button.clicked.connect(self.reset_widgets)
        toolbar_layout.addWidget(reset_button)

        toolbar_layout.setAlignment(Qt.AlignTop)

        self.no_list = ["Name", "Density[kg/m3]", "Young Modulus[GPa]", "Poisson", "Expansion cofficient[m/K]", "Color"]
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.no_list)) 
        self.table.setRowCount(1) 
        self.table.setHorizontalHeaderLabels(self.no_list)
        self.table.setItem(0,0,QTableWidgetItem(1))
        self.table.setSelectionBehavior(1)
        self.table.resizeColumnsToContents()
        main_layout = QVBoxLayout()
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)
        self.setMinimumSize(571,500)

        self.exec_()


    def add_material(self):
        instance = MaterialAdd()

    def open_widget2(self):
        self.table.setRowCount(3)

    def reset_widgets(self):
        for widget in self.findChildren(QWidget):
            if isinstance(widget, QDialog):
                widget.reject()


class MaterialAdd(QDialog):

    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("New Material")
        layout1 = QGridLayout()
        layout1.setAlignment(Qt.AlignTop)

        material_name_label = QLabel("Material Name")
        self.line_edit_material_name =  QLineEdit()
        density_label = QLabel("Density[kg/m3]")
        line_edit_density =  QLineEdit()
        poisson_label = QLabel("Poisson")
        line_edit_poisson =  QLineEdit()
        expansion_label = QLabel("Expansion cofficient[m/K]")
        line_edit_expansion_cofficient =  QLineEdit()
        young_label = QLabel("Young Modulus[GPa]")
        line_edit_young_modulus =  QLineEdit()
        color_label = QLabel("Color")
        self.color_button =  QPushButton("")
        add_new_material_button = QPushButton("Add New Material")
        cancel_button = QPushButton("Cancel")
        add_new_material_button.setMinimumSize(40,40)
        cancel_button.setMinimumSize(40,40)


        self.color_button.clicked.connect(self.color_button_callback)
        

        self.setLayout(layout1)
        self.setMinimumSize(500,100)

        layout1.addWidget(material_name_label, 0, 0)
        layout1.addWidget(self.line_edit_material_name, 1, 0)
        layout1.addWidget(density_label, 0, 1)
        layout1.addWidget(line_edit_density, 1, 1)
        layout1.addWidget(poisson_label, 0, 2)
        layout1.addWidget(line_edit_poisson, 1, 2)
        layout1.addWidget(young_label, 2, 1)
        layout1.addWidget(line_edit_young_modulus, 3, 1)
        layout1.addWidget(expansion_label, 2, 0)
        layout1.addWidget(line_edit_expansion_cofficient, 3, 0)
        layout1.addWidget(color_label, 2, 2)
        layout1.addWidget(self.color_button, 3, 2)
        layout1.addWidget(add_new_material_button, 6, 2)
        layout1.addWidget(cancel_button, 6, 0)
        

        self.exec_()

    def color_button_callback(self):
        color = QColorDialog.getColor()
        pick_color = color.name()
        self.color_button.setStyleSheet(f"background-color: {pick_color};")

        
    