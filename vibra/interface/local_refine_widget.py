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
    QCheckBox,
    
)
from vibra.engine.mesher.element_type import *
from vibra.utils.interface_functions import get_main_window



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

        # checkboxes
        self.layout_checkboxes = QVBoxLayout()

        # mesh connection checkbox
        self.mesh_connection_layout = QHBoxLayout()
        self.mesh_connection_checkbox = QCheckBox(self)
        self.mesh_connection_layout.addWidget(self.mesh_connection_checkbox)
        self.mesh_connection_checkbox.setChecked(True)
        self.mesh_connection_checkbox_label = QLabel(self)
        self.mesh_connection_checkbox_label.setText("Merge nodes from neighbour volumes")
        self.mesh_connection_layout.addWidget(self.mesh_connection_checkbox_label)
        self.layout_checkboxes.addLayout(self.mesh_connection_layout)
        self.mesh_connection_layout.addStretch()



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
        self.table.setSelectionBehavior(1)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(0)
        self.table.horizontalHeader().setStretchLastSection(True)

        # apply_button
        self.apply_button = QPushButton("Apply")


        # layout
        layout_main = QVBoxLayout()
        layout_main.addLayout(self.layout_mesh_parameters)
        layout_main.addLayout(self.layout_checkboxes)
        layout_main.addLayout(layout_refining_parameters)
        layout_main.addWidget(self.table)
        layout_main.addWidget(self.apply_button)

        self.setLayout(layout_main)
        self.setWindowTitle("Mesh setup")
        self.resize(500,500)

        self.add_button.clicked.connect(self.add_button_callback)
        self.trash_button.clicked.connect(self.trash_button_callback)
        self.apply_button.clicked.connect(self.apply_button_callback)

        self.exec_()

    def apply_button_callback(self):
        self.get_inputs_table()
        self.check_inputs()

    def trash_button_callback(self):
        current_row = self.table.currentRow()
        self.table.removeRow(current_row)


    def add_button_callback(self):
        a = self.table.rowCount()
        self.table.setRowCount(a+1) 
        self.table.setItem(a, 0, QTableWidgetItem(self.refining_size_textbox.text()))
        self.table.setItem(a, 1, QTableWidgetItem(self.faces_list_textbox.text()))
    
    def get_inputs_table(self):
        faces_and_refined_size_list = []
        for i in range(self.table.rowCount()):
            mesh_text = float(self.table.item(i,0).text())
            faces_text = self.table.item(i,1).text()
            faces_text = [int(i) for i in faces_text.split(",")]
            faces_and_refined_size_list.append((mesh_text,faces_text))
        
        return faces_and_refined_size_list
        
    def check_inputs(self):
        element_shape = self.element_type_list.currentText().lower()
        shape_function = self.shape_function_list.currentText().lower()
        global_mesh_size = int(self.global_mesh_size_textbox.text())
        faces_list = self.faces_list_textbox.text()
        refined_size = self.refining_size_textbox.text()
        # if refined_size != "":
        #     refined_size.split(",")
        #     refined_size = [int(i) for i in refined_size]
        # if faces_list != "":
        #     faces_list.split(",")
        #     faces_list = [int(i) for i in faces_list]

        if element_shape == "tetrahedral" and shape_function == "linear":
            self.element_type = TETRAHEDRON_4
        elif element_shape == "tetrahedral" and shape_function == "quadratic":
            self.element_type = TETRAHEDRON_10
        elif element_shape == "hexahedral" and shape_function == "linear":
            self.element_type = HEXAHEDRON_8
        elif element_shape == "hexahedral" and shape_function == "quadratic":
            self.element_type = HEXAHEDRON_20
        else:
            raise NotImplementedError(f"Element type not defined!")

        self.mesh_setup = {
            "element_type": self.element_type,
            "geometry_tolerance": 1e-6, # for now, implementing another textbox for this is needed (is it?)
            "size_factor": 0,
            "minimum_element_size": global_mesh_size,
            "maximum_element_size": global_mesh_size,
            "mesh_refinement_parameters": self.get_inputs_table(),
            "mesh_connection": self.mesh_connection_checkbox.isChecked(),
        }
        
        main_window = get_main_window()
        main_window.project.set_mesh_setup(self.mesh_setup)
        main_window.project.generate_mesh()
        main_window.viewer_tabs.show_mesh()
        main_window.viewer_tabs.update_plots()




        
    