from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLineEdit, QColorDialog, QLabel, QVBoxLayout, QGridLayout, QPushButton, QDialog, QHBoxLayout, QTableWidget, QTableWidgetItem
from pathlib import Path
from vibra.utils.icons import load_icon

class MaterialWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set Material")
        color = QColor("#0055DD")
        self.instance = None

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

        self.no_list = ["             Name             ", "Density\n[kg/m3]", "Young Modulus\n[GPa]", "Poisson", "Expansion cofficient\n[m/K]", "Color"]
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.no_list)) 
        self.table.setHorizontalHeaderLabels(self.no_list)
        self.table.setSelectionBehavior(1)
        self.table.resizeColumnsToContents()

        final_layout = QGridLayout()
        final_layout.setAlignment(Qt.AlignRight)

        main_layout = QVBoxLayout()
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.table)

        apply_to_all_button = QPushButton("Apply to all")
        apply_to_selection_button = QPushButton("Apply to selection")
        apply_to_all_button.setFixedSize(120,40)
        apply_to_selection_button.setFixedSize(120,40)

        apply_to_all_button.clicked.connect(self.apply_to_all_button_callback)
        apply_to_selection_button.clicked.connect(self.apply_to_selection_button_callback)
        apply_to_all_button.setFocusPolicy(Qt.NoFocus)
        apply_to_selection_button.setFocusPolicy(Qt.NoFocus)

        final_layout.addWidget(apply_to_all_button, 0, 1)
        final_layout.addWidget(apply_to_selection_button, 0, 0)

        main_layout.addLayout(final_layout)

        self.setLayout(main_layout)
        self.setMinimumSize(526,500)



        self.exec_()

    def add_material(self):
        instance = MaterialAdd()

        if instance.completed:

            name_material = instance.line_edit_material_name.text()
            density = instance.line_edit_density.text()
            young = instance.line_edit_young_modulus.text()
            poisson = instance.line_edit_poisson.text()
            expansion = instance.line_edit_expansion_cofficient.text()

            self.table.verticalHeader().setVisible(False)

            row_count = self.table.rowCount()
            self.table.insertRow(row_count)  
            self.table.setItem(row_count, 0, QTableWidgetItem(name_material))
            self.table.setItem(row_count, 1, QTableWidgetItem(density))
            self.table.setItem(row_count, 2, QTableWidgetItem(young))
            self.table.setItem(row_count, 3, QTableWidgetItem(poisson))
            self.table.setItem(row_count, 4, QTableWidgetItem(expansion))

            item = QTableWidgetItem()
            item.setBackground(instance.color)
            self.table.setItem(row_count, 5, item)

    def open_widget2(self):
        current_row = self.table.currentRow()
        self.table.removeRow(current_row)

    def reset_widgets(self):
        self.table.setRowCount(0)

    def apply_to_all_button_callback(self):
        pass

    def apply_to_selection_button_callback(self):
        pass

class MaterialAdd(QDialog):

    def __init__(self):
        super().__init__()

        self.color = QColor("#0055DD")

        self.setWindowTitle("New Material")
        layout1 = QGridLayout()
        layout1.setAlignment(Qt.AlignTop)

        material_name_label = QLabel("Material Name")
        self.line_edit_material_name =  QLineEdit()
        density_label = QLabel("Density[kg/m3]")
        self.line_edit_density =  QLineEdit()
        poisson_label = QLabel("Poisson")
        self.line_edit_poisson =  QLineEdit()
        expansion_label = QLabel("Expansion cofficient[m/K]")
        self.line_edit_expansion_cofficient =  QLineEdit()
        young_label = QLabel("Young Modulus[GPa]")
        self.line_edit_young_modulus =  QLineEdit()
        color_label = QLabel("Color")
        self.color_button =  QPushButton("")
        self.add_new_material_button = QPushButton("Add New Material")
        self.cancel_button = QPushButton("Cancel")

        self.add_new_material_button.setMinimumSize(40,40)
        self.add_new_material_button.clicked.connect(self.confirm_button_callback)
        
        self.cancel_button.setMinimumSize(40,40)
        self.cancel_button.clicked.connect(self.cancel_button_callback)

        self.color_button.clicked.connect(self.color_button_callback)

        self.setLayout(layout1)
        self.setMinimumSize(500,100)

        self.error_label = QLabel("")

        layout1.addWidget(material_name_label, 0, 0)
        layout1.addWidget(self.line_edit_material_name, 1, 0)
        
        layout1.addWidget(density_label, 0, 1)
        layout1.addWidget(self.line_edit_density, 1, 1)
        layout1.addWidget(self.error_label, 2, 0)
        layout1.addWidget(self.line_edit_poisson, 3, 0)
        layout1.addWidget(young_label, 0, 2)
        layout1.addWidget(self.line_edit_young_modulus, 1, 2)
        layout1.addWidget(expansion_label, 2, 1)
        layout1.addWidget(self.line_edit_expansion_cofficient, 3, 1)
        layout1.addWidget(color_label, 2, 2)
        layout1.addWidget(self.color_button, 3, 2)
        layout1.addWidget(self.add_new_material_button, 6, 2)
        layout1.addWidget(self.cancel_button, 6, 0)

        self.completed = False
        
        self.exec_()

    def confirm_button_callback(self):
        if not self.verify_error():
            self.completed = True
            self.close()

    def verify_error(self):
        error = False

        if self.line_edit_material_name.text():
            self.error_label.setText("")

        else:
            error = True
            self.error_label.setText("deu erro andre")
        return error

            

    def cancel_button_callback(self):
        self.close()

    def color_button_callback(self):
        self.color = QColorDialog.getColor()
        pick_color = self.color.name()
        self.color_button.setStyleSheet(f"background-color: {pick_color};")

        
    