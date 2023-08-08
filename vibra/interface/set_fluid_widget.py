from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLineEdit, QTableWidgetItem, QColorDialog, QLabel, QVBoxLayout, QGridLayout, QPushButton, QDialog, QHBoxLayout, QTableWidget, QTableWidgetItem
from pathlib import Path
from vibra.utils.icons import load_icon
import random

class FluidWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set Fluid")
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
        reset_button.setFixedSize(50, 25)
        reset_button.clicked.connect(self.reset_widgets)
        toolbar_layout.addWidget(reset_button)

        toolbar_layout.setAlignment(Qt.AlignTop)

        header = [      "Name",
                        "Fluid Density\n[kg/m3]", 
                        "Speed of sound\n[m/s]",
                        "Specific heat Cp\n[J/kgK]",
                        "Temperature\n[K]","Pressure [Pa]",
                        "Thermal\nconductivity" ,
                        "Dynamic viscosity\n[N.s/m2]",
                        "Impedance\n[kg/ms2]",
                        "Isentropic\nexponent",
                        "Color"]
        
        self.table = QTableWidget()
        self.table.setColumnCount(len(header)) 
        self.table.setHorizontalHeaderLabels(header)
        self.table.setSelectionBehavior(1)
        self.table.resizeColumnsToContents()
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
        self.setMinimumSize(700,500)

        self.exec_()

    def add_material(self):
        instance = FluidAdd()

        if instance.completed:

            self.fluid_name = instance.line_edit_fluid_name.text()
            self.density = instance.line_edit_density.text()
            self.temperature = instance.line_edit_temperature.text()
            self.pressure = instance.line_edit_pressure.text()
            self.speed = instance.line_edit_speed.text()
            self.specific = instance.line_edit_specific.text()
            self.thermal = instance.line_edit_thermal.text()
            self.dynamic = instance.line_edit_dynamic.text()
            self.impedance = instance.line_edit_impedance.text()
            self.isentropic = instance.line_edit_isentropic.text()

            self.table.verticalHeader().setVisible(False)

            self.row_count = self.table.rowCount()
            self.table.insertRow(self.row_count)  
            self.table.setItem(self.row_count, 0, QTableWidgetItem(self.fluid_name))
            self.table.setItem(self.row_count, 1, QTableWidgetItem(self.density))
            self.table.setItem(self.row_count, 2, QTableWidgetItem(self.speed))
            self.table.setItem(self.row_count, 3, QTableWidgetItem(self.specific))
            self.table.setItem(self.row_count, 4, QTableWidgetItem(self.temperature))
            self.table.setItem(self.row_count, 5, QTableWidgetItem(self.pressure))
            self.table.setItem(self.row_count, 6, QTableWidgetItem(self.thermal))
            self.table.setItem(self.row_count, 7, QTableWidgetItem(self.dynamic))
            self.table.setItem(self.row_count, 8, QTableWidgetItem(self.impedance))
            self.table.setItem(self.row_count, 9, QTableWidgetItem(self.isentropic))

            self.item = QTableWidgetItem()
            self.item.setBackground(instance.color)
            self.table.setItem(self.row_count, 10, self.item)

    def on_table_clicked(self, row, column):
        if column == 10:
            color = QColorDialog.getColor()

            if color.isValid():
                item = self.table.item(row, column)
                if item is not None:
                    item.setBackground(color)
        else:
            pass
        
    def open_widget2(self):
        current_row = self.table.currentRow()
        self.table.removeRow(current_row)

    def reset_widgets(self):
        self.table.setRowCount(0)

    def apply_to_all_button_callback(self):
        pass

    def apply_to_selection_button_callback(self):
        pass

class FluidAdd(QDialog):

    def __init__(self):
        super().__init__()

        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)


        self.color = QColor(r,g,b)

        self.setWindowTitle("New Fluid")
        layout1 = QGridLayout()
        layout1.setAlignment(Qt.AlignTop)

        fluid_name_label = QLabel("Fluid Name")
        self.line_edit_fluid_name =  QLineEdit()
        density_label = QLabel(" Fluid Density[kg/m3]")
        self.line_edit_density =  QLineEdit()
        temperature_label = QLabel("Temperature [K]")
        self.line_edit_temperature =  QLineEdit()
        expansion_pressure = QLabel("Pressure [Pa]")
        self.line_edit_pressure =  QLineEdit()
        speed_label = QLabel("Speed of sound [m/s]")
        self.line_edit_speed =  QLineEdit()
        impedance_label =  QLabel("Impedance[kg/ms2]")
        self.line_edit_impedance = QLineEdit()
        isentropic_label =  QLabel("Isentropic exponent")
        self.line_edit_isentropic = QLineEdit()
        thermal_label =  QLabel("Thermal conductivity")
        self.line_edit_thermal = QLineEdit()
        specific_label =  QLabel("Specific heat Cp [J/kgK]")
        self.line_edit_specific = QLineEdit()
        dynamic_label =  QLabel("Dynamic viscosity [N.s/m2]")
        self.line_edit_dynamic = QLineEdit()
        color_label = QLabel("Color")
        self.color_button =  QPushButton("")
        self.color_button.setFocusPolicy(Qt.NoFocus)
        self.add_new_fluid_button = QPushButton("Add New Fluid")
        self.cancel_button = QPushButton("Cancel")

        self.add_new_fluid_button.setMinimumSize(40,40)
        self.add_new_fluid_button.clicked.connect(self.confirm_button_callback)
        
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
        self.error_label_specific = QLabel("")
        self.error_label_thermal = QLabel("")
        self.error_label_dynamic = QLabel("")
        self.error_label_isentropic = QLabel("")
        self.error_label_impedance = QLabel("")

        layout1.addWidget(fluid_name_label, 0, 0)
        layout1.addWidget(self.line_edit_fluid_name, 1, 0)
        layout1.addWidget(density_label, 0, 1)
        layout1.addWidget(self.line_edit_density, 1, 1)
        layout1.addWidget(self.error_label_material_name, 2, 0)   
        layout1.addWidget(temperature_label, 3, 0)  
        layout1.addWidget(self.line_edit_temperature, 4, 0)
        layout1.addWidget(self.error_label_poisson, 5, 0)  
        layout1.addWidget(speed_label, 0, 2)   
        layout1.addWidget(self.line_edit_speed, 1, 2)
        layout1.addWidget(self.error_label_density, 2, 1)  
        layout1.addWidget(expansion_pressure, 3, 1)   
        layout1.addWidget(self.line_edit_pressure, 4, 1)
        layout1.addWidget(self.error_label_expansion, 5, 1)  
        layout1.addWidget(self.error_label_young, 2, 2) 
        layout1.addWidget(thermal_label, 3, 2)   
        layout1.addWidget(self.line_edit_thermal, 4, 2)  
        layout1.addWidget(self.add_new_fluid_button, 9, 3)
        layout1.addWidget(self.cancel_button, 9, 0)
        layout1.addWidget(impedance_label, 6, 0)
        layout1.addWidget(self.line_edit_impedance, 7, 0)
        layout1.addWidget(isentropic_label, 6, 1)
        layout1.addWidget(self.line_edit_isentropic, 7, 1)
        layout1.addWidget(color_label, 6, 2)
        layout1.addWidget(self.color_button, 7, 2)
        layout1.addWidget(specific_label, 0, 3)
        layout1.addWidget(self.line_edit_specific, 1, 3)
        layout1.addWidget(dynamic_label, 3, 3)
        layout1.addWidget(self.line_edit_dynamic, 4, 3)
        layout1.addWidget(self.error_label_specific , 2, 3)
        layout1.addWidget(self.error_label_dynamic, 5, 3)
        layout1.addWidget(self.error_label_thermal, 5, 2)
        layout1.addWidget(self.error_label_isentropic, 8, 1)
        layout1.addWidget(self.error_label_impedance, 8, 0)


        pick_color = self.color.name()
        self.color_button.setStyleSheet(f"background-color: {pick_color};")
        
    
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

        if self.line_edit_fluid_name.text():
            self.error_label_material_name.setText("")
            self.line_edit_fluid_name.setStyleSheet(border_color)
            self.line_edit_fluid_name.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_material_name.setText("Please put a name")
            self.error_label_material_name.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_fluid_name.setStyleSheet(border_color)

        if self.line_edit_density.text() and self.line_edit_density.text().isnumeric():
            self.error_label_density.setText("")
            self.line_edit_density.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_density.setText("Please put a number")
            self.error_label_density.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_density.setStyleSheet(border_color)
        
        if self.line_edit_speed.text() and self.line_edit_speed.text().isnumeric():
            self.error_label_young.setText("")
            self.line_edit_speed.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_young.setText("Please put a number")
            self.error_label_young.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_speed.setStyleSheet(border_color)
        
        if self.line_edit_pressure.text() and self.line_edit_pressure.text().isnumeric():
            self.error_label_expansion.setText("")
            self.line_edit_pressure.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_expansion.setText("Please put a number")
            self.error_label_expansion.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_pressure.setStyleSheet(border_color)

        if self.line_edit_temperature.text() and self.line_edit_temperature.text().isnumeric():
            self.error_label_poisson.setText("")
            self.line_edit_temperature.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_poisson.setText("Please put a number")
            self.error_label_poisson.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_temperature.setStyleSheet(border_color)
        
        if self.line_edit_dynamic.text() and self.line_edit_dynamic.text().isnumeric():
            self.error_label_dynamic.setText("")
            self.line_edit_dynamic.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_dynamic.setText("Please put a number")
            self.error_label_dynamic.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_dynamic.setStyleSheet(border_color)

        if self.line_edit_thermal.text() and self.line_edit_thermal.text().isnumeric():
            self.error_label_thermal.setText("")
            self.line_edit_thermal.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_thermal.setText("Please put a number")
            self.error_label_thermal.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_thermal.setStyleSheet(border_color)
        
        if self.line_edit_specific.text() and self.line_edit_specific.text().isnumeric():
            self.error_label_specific.setText("")
            self.line_edit_specific.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_specific.setText("Please put a number")
            self.error_label_specific.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_specific.setStyleSheet(border_color)

        if self.line_edit_isentropic.text() and self.line_edit_isentropic.text().isnumeric():
            self.error_label_isentropic.setText("")
            self.line_edit_isentropic.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_isentropic.setText("Please put a number")
            self.error_label_isentropic.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_isentropic.setStyleSheet(border_color)

        if self.line_edit_impedance.text() and self.line_edit_impedance.text().isnumeric():
            self.error_label_impedance.setText("")
            self.line_edit_impedance.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_impedance.setText("Please put a number")
            self.error_label_impedance.setStyleSheet(f'color: {red_color.name()};')
            self.line_edit_impedance.setStyleSheet(border_color)
        
        return error

    def cancel_button_callback(self):
        self.close()

    def color_button_callback(self):
        self.color = QColorDialog.getColor()
        pick_color = self.color.name()
        self.color_button.setStyleSheet(f"background-color: {pick_color};")

        
    