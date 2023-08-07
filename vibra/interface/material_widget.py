from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLineEdit, QTableWidgetItem, QColorDialog, QLabel, QVBoxLayout, QGridLayout, QPushButton, QDialog, QHBoxLayout, QTableWidget, QTableWidgetItem
from pathlib import Path
from vibra.utils.icons import load_icon

class MaterialWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set Material")
        self.color = QColor("#0055DD")
        self.instance = None

        toolbar_layout = QHBoxLayout()
        add_material_button = QPushButton()
        add_material_button.setFocusPolicy(Qt.NoFocus)
        add_material_icon = load_icon(Path("data/icons/plus-thick.png"), self.color)
        add_material_button.setIconSize(QSize(30, 30))
        add_material_button.setIcon(add_material_icon)
    
        add_material_button.setFixedSize(30, 30)
        add_material_button.clicked.connect(self.add_material)
        toolbar_layout.addWidget(add_material_button)

        trash_button = QPushButton()
        trash_button.setFocusPolicy(Qt.NoFocus)
        trash_icon = load_icon(Path("data/icons/delete.png"), self.color)
        trash_button.setIconSize(QSize(30, 30))
        trash_button.setIcon(trash_icon)
        trash_button.setFixedSize(30, 30)
        trash_button.clicked.connect(self.open_widget2)
        toolbar_layout.addWidget(trash_button)

        toolbar_layout.addStretch(1)
        reset_button = QPushButton("Reset")
        reset_button.setFocusPolicy(Qt.NoFocus)
        reset_button.clicked.connect(self.reset_widgets)
        toolbar_layout.addWidget(reset_button)

        toolbar_layout.setAlignment(Qt.AlignTop)
        
        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA Name AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        header = [
            "Name",
            "Density\n[kg/m3]",
            "Young Modulus\n[GPa]",
            "Poisson",
            "Expansion cofficient\n[m/K]",
            "Color"
        ]
        self.table = QTableWidget()
        self.table.setColumnCount(len(header)) 
        self.table.setHorizontalHeaderLabels(header)
        self.table.setSelectionBehavior(1)
        self.table.resizeColumnsToContents()

        self.table.horizontalHeader().setSectionResizeMode(0)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().resizeSection(0, 150)  #  spacing for Name

        self.table.cellClicked.connect(self.on_table_clicked)

        final_layout = QGridLayout()
        final_layout.setAlignment(Qt.AlignRight)

        main_layout = QVBoxLayout()
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.table)

        apply_to_all_button = QPushButton("Apply to all")
        apply_to_selection_button = QPushButton("Apply to selection")

        apply_to_all_button.clicked.connect(self.apply_to_all_button_callback)
        apply_to_selection_button.clicked.connect(self.apply_to_selection_button_callback)
        apply_to_all_button.setFocusPolicy(Qt.NoFocus)
        apply_to_selection_button.setFocusPolicy(Qt.NoFocus)

        final_layout.addWidget(apply_to_all_button, 0, 1)
        final_layout.addWidget(apply_to_selection_button, 0, 0)

        main_layout.addLayout(final_layout)

        self.setLayout(main_layout)
        self.setMinimumSize(650,500)

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

            self.row_count = self.table.rowCount()
            self.table.insertRow(self.row_count)  
            self.table.setItem(self.row_count, 0, QTableWidgetItem(name_material))
            self.table.setItem(self.row_count, 1, QTableWidgetItem(density))
            self.table.setItem(self.row_count, 2, QTableWidgetItem(young))
            self.table.setItem(self.row_count, 3, QTableWidgetItem(poisson))
            self.table.setItem(self.row_count, 4, QTableWidgetItem(expansion))

            self.item = QTableWidgetItem()
            self.item.setBackground(instance.color)
            self.table.setItem(self.row_count, 5, self.item)

    def on_table_clicked(self, row, column):
        if column == 5:
            color = QColorDialog.getColor()

            if color.isValid():
                item = self.table.item(row, column)
                if item is not None:
                    item.setBackground(color)
        
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
        self.color_button.setFocusPolicy(Qt.NoFocus)
        self.add_new_material_button = QPushButton("Add New Material")
        self.cancel_button = QPushButton("Cancel")

        self.add_new_material_button.setMinimumSize(40,40)
        self.add_new_material_button.clicked.connect(self.confirm_button_callback)
        
        self.cancel_button.setMinimumSize(40,40)
        self.cancel_button.clicked.connect(self.cancel_button_callback)

        self.color_button.clicked.connect(self.color_button_callback)

        self.setLayout(layout1)
        self.setMinimumSize(500,100)

        self.error_label_material_name = QLabel("")
        self.error_label_density = QLabel("")
        self.error_label_young = QLabel("")
        self.error_label_poisson = QLabel("")
        self.error_label_expansion = QLabel("")

        layout1.addWidget(material_name_label, 0, 0)
        layout1.addWidget(self.line_edit_material_name, 1, 0)
        layout1.addWidget(density_label, 0, 1)
        layout1.addWidget(self.line_edit_density, 1, 1)
        layout1.addWidget(self.error_label_material_name, 2, 0)   
        layout1.addWidget(poisson_label, 3, 0)  
        layout1.addWidget(self.line_edit_poisson, 4, 0)
        layout1.addWidget(self.error_label_poisson, 5, 0)  
        layout1.addWidget(young_label, 0, 2)   
        layout1.addWidget(self.line_edit_young_modulus, 1, 2)
        layout1.addWidget(self.error_label_density, 2, 1)  
        layout1.addWidget(expansion_label, 3, 1)   
        layout1.addWidget(self.line_edit_expansion_cofficient, 4, 1)
        layout1.addWidget(self.error_label_expansion, 5, 1)  
        layout1.addWidget(self.error_label_young, 2, 2) 
        layout1.addWidget(color_label, 3, 2)   
        layout1.addWidget(self.color_button, 4, 2)  
        layout1.addWidget(self.add_new_material_button, 8, 2)
        layout1.addWidget(self.cancel_button, 8, 0)
    
        self.completed = False
        
        self.exec_()

    def confirm_button_callback(self):
        if not self.verify_error():
            self.completed = True
            self.close()

    def verify_error(self):
        error = False
        red_color = QColor(224, 73, 70)
        border_color = f"border: 0.5px solid {red_color.name()};"
        none_color = f"border: 0px solid {None}"

        if self.line_edit_material_name.text():
            self.error_label_material_name.setText("")
            self.line_edit_material_name.setStyleSheet(border_color)
            self.line_edit_material_name.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_material_name.setText("Please put a material name")
            self.error_label_material_name.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_material_name.setStyleSheet(border_color)

        if self.line_edit_density.text() and self.line_edit_density.text().isnumeric():
            self.error_label_density.setText("")
            self.line_edit_density.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_density.setText("Please put a density")
            self.error_label_density.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_density.setStyleSheet(border_color)
        
        if self.line_edit_young_modulus.text() and self.line_edit_young_modulus.text().isnumeric():
            self.error_label_young.setText("")
            self.line_edit_young_modulus.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_young.setText("Please put a number")
            self.error_label_young.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_young_modulus.setStyleSheet(border_color)
        
        if self.line_edit_expansion_cofficient.text() and self.line_edit_expansion_cofficient.text().isnumeric():
            self.error_label_expansion.setText("")
            self.line_edit_expansion_cofficient.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_expansion.setText("Please put a number")
            self.error_label_expansion.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_expansion_cofficient.setStyleSheet(border_color)

        if self.line_edit_poisson.text() and self.line_edit_poisson.text().isnumeric():
            self.error_label_poisson.setText("")
            self.line_edit_poisson.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_poisson.setText("Please put a number")
            self.error_label_poisson.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_poisson.setStyleSheet(border_color)
        
        return error

    def cancel_button_callback(self):
        self.close()

    def color_button_callback(self):
        self.color = QColorDialog.getColor()
        pick_color = self.color.name()
        self.color_button.setStyleSheet(f"background-color: {pick_color};")

        
    