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
    QComboBox,
)



class LocalRefineWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.layout_mesh_parameters = QGridLayout()
        
        
        # global mesh size
        self.global_mesh_size_textbox_label = QLabel(self)
        self.global_mesh_size_textbox_label.setText("Global mesh size:")
        self.layout_mesh_parameters.addWidget(self.global_mesh_size_textbox_label, 1, 1)
        self.global_mesh_size_textbox = QLineEdit(self)
        self.layout_mesh_parameters.addWidget(self.global_mesh_size_textbox, 2, 1)


        # element type list
        self.element_type_list_label = QLabel(self)
        self.element_type_list_label.setText("Element type:")
        self.layout_mesh_parameters.addWidget(self.element_type_list_label, 1, 2)
        self.element_type_list = QComboBox()
        self.element_type_list.addItems(["Tetrahedral", "Hexahedral", "Triangular", "Quadrangular"])
        self.layout_mesh_parameters.addWidget(self.element_type_list, 2, 2)


        # shape function list
        self.shape_function_list_label = QLabel(self)
        self.shape_function_list_label.setText("Shape function:")
        self.layout_mesh_parameters.addWidget(self.shape_function_list_label, 1, 3)
        self.shape_function_list = QComboBox()
        self.shape_function_list.addItems(["Linear", "Quadratic"])
        self.layout_mesh_parameters.addWidget(self.shape_function_list, 2, 3)



        layout_refining_parameters = QGridLayout()

        # refining textbox/lineedit
        self.refining_size_textbox_label = QLabel(self)
        self.refining_size_textbox_label.setText("Refined size:")
        self.refining_size_textbox = QLineEdit(self)
        
        layout_refining_parameters.addWidget(self.refining_size_textbox_label, 1, 1)
        layout_refining_parameters.addWidget(self.refining_size_textbox, 2, 1)

        # faces list textbox/lineedit
        self.faces_list_textbox_label = QLabel(self)
        self.faces_list_textbox_label.setText("Faces List:")
        self.faces_list_textbox = QLineEdit(self)
        
        layout_refining_parameters.addWidget(self.faces_list_textbox_label, 1, 2)
        layout_refining_parameters.addWidget(self.faces_list_textbox, 2, 2)

        # add_button
        self.add_button = QPushButton("Add")
        layout_refining_parameters.addWidget(self.add_button, 2, 3)


        # trash_button
        self.trash_button = QPushButton("Delete")
        layout_refining_parameters.addWidget(self.trash_button, 2, 4)

        # table
        header = ["Refining mesh size", "Faces list"]
        self.table = QTableWidget()
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        self.table.resizeColumnsToContents()
        
        # apply_button
        self.apply_button = QPushButton("Apply")


        # layout
        layout_main = QVBoxLayout()
        layout_main.addLayout(self.layout_mesh_parameters)
        layout_main.addLayout(self.layout_mesh_parameters)
        layout_main.addLayout(layout_refining_parameters)
        layout_main.addWidget(self.table)
        layout_main.addWidget(self.apply_button)

        self.setLayout(layout_main)
        self.setWindowTitle("Mesh setup")
        self.resize(500,500)

        # self.apply_button.clicked.connect(self.apply_button_callback)

        self.exec_()

    def apply_button_callback(self):
        self.banana.setText("Changes applied")
    