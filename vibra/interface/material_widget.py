import random
from pathlib import Path

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

from vibra.engine.properties.material import (
    Material,
    load_material_list,
    save_material_list,
)

from vibra import ICON_DIR
from vibra.utils.icons import load_icon


class MaterialWidget(QDialog):
    material_list = []

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set Material")
        self.color = QColor("#448cff")
        self.instance = None

        toolbar_layout = QHBoxLayout()
        add_material_button = QPushButton()
        add_material_button.setFocusPolicy(Qt.NoFocus)
        add_material_icon = load_icon(ICON_DIR / "plus-thick.png", self.color)
        add_material_button.setIconSize(QSize(30, 30))
        add_material_button.setIcon(add_material_icon)

        add_material_button.setFixedSize(30, 30)
        add_material_button.clicked.connect(self.add_material)
        toolbar_layout.addWidget(add_material_button)

        trash_button = QPushButton()
        trash_button.setFocusPolicy(Qt.NoFocus)
        trash_icon = load_icon(ICON_DIR / "delete.png", self.color)
        trash_button.setIconSize(QSize(30, 30))
        trash_button.setIcon(trash_icon)
        trash_button.setFixedSize(30, 30)
        trash_button.clicked.connect(self.trash_button_callback)
        toolbar_layout.addWidget(trash_button)

        toolbar_layout.addStretch(1)
        reset_button = QPushButton("Reset")
        reset_button.setFocusPolicy(Qt.NoFocus)
        reset_button.clicked.connect(self.reset_widgets)
        toolbar_layout.addWidget(reset_button)
        toolbar_layout.setAlignment(Qt.AlignTop)

        header = [
            "Name",
            "Density\n[kg/m3]",
            "Young Modulus\n[GPa]",
            "Poisson",
            "Expansion cofficient\n[m/K]",
            "Color",
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
        self.setMinimumSize(650, 500)

        self.load_material_list()
        self.update_table()
        self.exec_()

    def load_material_list(self):
        path = Path("material_library.json")
        if not path.exists():
            return
        self.material_list = load_material_list(path)

    def update_table(self):
        self.table.setRowCount(len(self.material_list))
        for i, material in enumerate(self.material_list):
            self.table.setItem(i, 0, QTableWidgetItem(str(material.name)))
            self.table.setItem(i, 1, QTableWidgetItem(str(material.density)))
            self.table.setItem(i, 2, QTableWidgetItem(str(material.young_modulus)))
            self.table.setItem(i, 3, QTableWidgetItem(str(material.poisson_ratio)))
            self.table.setItem(i, 4, QTableWidgetItem(str(material.thermal_expansion_coefficient)))

            item = QTableWidgetItem()
            item.setBackground(QColor(*material.color))
            self.table.setItem(i, 5, item)

    def add_material(self):
        instance = MaterialAdd()

        if not instance.completed:
            return

        r, g, b, _ = instance.color.getRgb()
        new_material = Material(
            name=str(instance.line_edit_material_name.text()),
            color=(r, g, b),
            density=float(instance.line_edit_density.text()),
            young_modulus=float(instance.line_edit_young_modulus.text()) * 1e9,
            poisson_ratio=float(instance.line_edit_poisson.text()),
        )

        self.material_list.append(new_material)
        save_material_list("material_library.json", self.material_list)
        self.update_table()

    def on_table_clicked(self, row, column):
        if column == 5:
            color = QColorDialog.getColor()

            if color.isValid():
                item = self.table.item(row, column)
                if item is not None:
                    item.setBackground(color)

    def trash_button_callback(self):
        current_row = self.table.currentRow()
        self.material_list.pop(current_row)
        self.update_table()

    def reset_widgets(self):
        self.table.setRowCount(0)

    def apply_to_all_button_callback(self):
        pass

    def apply_to_selection_button_callback(self):
        pass


class MaterialAdd(QDialog):
    def __init__(self):
        super().__init__()

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        self.color = QColor(r, g, b)

        self.setWindowTitle("New Material")
        layout1 = QGridLayout()
        layout1.setAlignment(Qt.AlignTop)

        material_name_label = QLabel("Material Name")
        self.line_edit_material_name = QLineEdit()
        density_label = QLabel("Density[kg/m3]")
        self.line_edit_density = QLineEdit()
        poisson_label = QLabel("Poisson")
        self.line_edit_poisson = QLineEdit()
        expansion_label = QLabel("Expansion cofficient[m/K]")
        self.line_edit_expansion_cofficient = QLineEdit()
        young_label = QLabel("Young Modulus[GPa]")
        self.line_edit_young_modulus = QLineEdit()
        color_label = QLabel("Color")
        self.color_button = QPushButton("")
        self.color_button.setFocusPolicy(Qt.NoFocus)
        self.add_new_material_button = QPushButton("Add New Material")
        self.cancel_button = QPushButton("Cancel")

        self.add_new_material_button.setMinimumSize(40, 40)
        self.add_new_material_button.clicked.connect(self.confirm_button_callback)

        self.cancel_button.setMinimumSize(40, 40)
        self.cancel_button.clicked.connect(self.cancel_button_callback)

        self.color_button.clicked.connect(self.color_button_callback)

        self.setLayout(layout1)
        self.setMinimumSize(500, 100)

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

        if self.line_edit_material_name.text():
            self.error_label_material_name.setText("")
            self.line_edit_material_name.setStyleSheet(border_color)
            self.line_edit_material_name.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_material_name.setText("Please put a material name")
            self.error_label_material_name.setStyleSheet(f"color: {red_color.name()};")
            self.line_edit_material_name.setStyleSheet(border_color)

        if self.line_edit_density.text() and self.line_edit_density.text().isnumeric():
            self.error_label_density.setText("")
            self.line_edit_density.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_density.setText("Please put a density")
            self.error_label_density.setStyleSheet(f"color: {red_color.name()};")
            self.line_edit_density.setStyleSheet(border_color)

        if self.line_edit_young_modulus.text() and self.line_edit_young_modulus.text().isnumeric():
            self.error_label_young.setText("")
            self.line_edit_young_modulus.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_young.setText("Please put a number")
            self.error_label_young.setStyleSheet(f"color: {red_color.name()};")
            self.line_edit_young_modulus.setStyleSheet(border_color)

        if (
            self.line_edit_expansion_cofficient.text()
            and self.line_edit_expansion_cofficient.text().isnumeric()
        ):
            self.error_label_expansion.setText("")
            self.line_edit_expansion_cofficient.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_expansion.setText("Please put a number")
            self.error_label_expansion.setStyleSheet(f"color: {red_color.name()};")
            self.line_edit_expansion_cofficient.setStyleSheet(border_color)

        if self.line_edit_poisson.text() and self.line_edit_poisson.text().isnumeric():
            self.error_label_poisson.setText("")
            self.line_edit_poisson.setStyleSheet(none_color)
        else:
            error = True
            self.error_label_poisson.setText("Please put a number")
            self.error_label_poisson.setStyleSheet(f"color: {red_color.name()};")
            self.line_edit_poisson.setStyleSheet(border_color)

        return error

    def cancel_button_callback(self):
        self.close()

    def color_button_callback(self):
        self.color = QColorDialog.getColor()
        pick_color = self.color.name()
        self.color_button.setStyleSheet(f"background-color: {pick_color};")
