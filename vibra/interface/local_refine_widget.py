# fmt: off
from pathlib import Path

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QColor, QPixmap

from PyQt5.QtWidgets import (   QColorDialog,
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
                                QCheckBox   )

from vibra.engine.mesher.element_type import *
from vibra.interface.general.print_message_input2 import PrintMessageInput
from vibra.interface.loading_bar import load_function
from vibra.utils.interface_functions import get_main_window


class LocalRefineWidget(QDialog):
    def __init__(self, **kwargs):
        super().__init__()

        icon_path = str(Path("data/icons/logo_vibra.png"))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Mesher setup")

        self.main_window = get_main_window()
        self.main_window.set_input_widget(self)
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)

        self.close_after_generate = kwargs.get("close_after_generate", False)
        self.complete = False
        self._create_and_config_widgets()
        self._create_connections()
        self.exec()

    def _create_and_config_widgets(self):
        
        self.layout_mesh_parameters = QGridLayout()
        
        # global mesh size
        self.global_mesh_size_textbox_label = QLabel(self)
        self.global_mesh_size_textbox_label.setText("Global mesh size:")
        self.layout_mesh_parameters.addWidget(self.global_mesh_size_textbox_label, 1, 1)
        self.lineEdit_global_mesh_size = QLineEdit(self)
        self.lineEdit_global_mesh_size.setText("100")
        self.lineEdit_global_mesh_size.setAlignment(Qt.AlignHCenter)
        self.layout_mesh_parameters.addWidget(self.lineEdit_global_mesh_size, 2, 1)
        
        # self.error_global_mesh_size = QLabel("")
        # self.layout_mesh_parameters.addWidget(self.error_global_mesh_size, 3, 1)

        # geometry tolerance
        self.geometry_tolerance_textbox_label = QLabel(self)
        self.geometry_tolerance_textbox_label.setText("Geometry tolerance:")
        self.layout_mesh_parameters.addWidget(self.geometry_tolerance_textbox_label, 1, 2)
        self.lineEdit_geometry_tolerance = QLineEdit(self)
        self.lineEdit_geometry_tolerance.setText("1e-6")
        self.lineEdit_geometry_tolerance.setAlignment(Qt.AlignHCenter)
        self.layout_mesh_parameters.addWidget(self.lineEdit_geometry_tolerance, 2, 2)

        # element type list
        self.element_type_label = QLabel(self)
        self.element_type_label.setText("Element type:")
        self.layout_mesh_parameters.addWidget(self.element_type_label, 1, 3)
        self.comboBox_element_type = QComboBox()
        self.comboBox_element_type.addItems(["Tetrahedral", "Hexahedral", "Triangular", "Quadrangular"])
        self.layout_mesh_parameters.addWidget(self.comboBox_element_type, 2, 3)

        # shape function list
        self.shape_function_label = QLabel(self)
        self.shape_function_label.setText("Shape function:")
        self.layout_mesh_parameters.addWidget(self.shape_function_label, 1, 4)
        self.comboBox_shape_function = QComboBox()
        self.comboBox_shape_function.addItems(["Linear", "Quadratic"])
        self.layout_mesh_parameters.addWidget(self.comboBox_shape_function, 2, 4)

        # checkboxes
        self.layout_checkboxes = QVBoxLayout()

        # mesh connection checkbox
        self.mesh_connection_layout = QHBoxLayout()
        self.mesh_connection_checkbox = QCheckBox("Merge nodes from neighbour volumes")
        self.mesh_connection_layout.addWidget(self.mesh_connection_checkbox)
        self.mesh_connection_checkbox.setChecked(True)
        self.mesh_connection_layout.addStretch()
        self.layout_checkboxes.addLayout(self.mesh_connection_layout)

        # space 
        self.space = QLabel("")
        self.layout_checkboxes.addWidget(self.space)

        layout_refining_parameters = QGridLayout()

        # refining textbox/lineedit
        self.refining_size_textbox_label = QLabel(self)
        self.refining_size_textbox_label.setText("Refined size:")
        self.lineEdit_refining_size = QLineEdit(self)
        
        layout_refining_parameters.addWidget(self.refining_size_textbox_label, 1, 1)
        layout_refining_parameters.addWidget(self.lineEdit_refining_size, 2, 1)

        # faces list textbox/lineedit
        self.faces_list_textbox_label = QLabel(self)
        self.faces_list_textbox_label.setText("Faces list:")
        self.lineEdit_faces_list = QLineEdit(self)
        
        layout_refining_parameters.addWidget(self.faces_list_textbox_label, 1, 2)
        layout_refining_parameters.addWidget(self.lineEdit_faces_list, 2, 2)

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

        # generate_mesh_button
        self.generate_mesh_button = QPushButton("Generate mesh")

        # layout
        layout_main = QVBoxLayout()
        layout_main.addLayout(self.layout_mesh_parameters)
        layout_main.addLayout(self.layout_checkboxes)
        layout_main.addLayout(layout_refining_parameters)
        layout_main.addWidget(self.table)
        layout_main.addWidget(self.generate_mesh_button)

        self.setLayout(layout_main)
        # self.resize(500,500)
        self.setFixedSize(500,400)

    def _create_connections(self):
        self.add_button.clicked.connect(self.add_button_callback)
        self.trash_button.clicked.connect(self.trash_button_callback)
        self.generate_mesh_button.clicked.connect(self.generate_mesh_button_callback)

    def generate_mesh_button_callback(self):

        if self.check_mesh_inputs():
            return
        
        self.main_window.project.set_mesh_setup(self.mesh_setup)
        generate_mesh = load_function(self.main_window.project.generate_mesh, self.main_window)
        generate_mesh()
        self.main_window.viewer_tabs.show_mesh()
        self.main_window.viewer_tabs.update_plots()
        self.complete = True
        if self.close_after_generate:
            self.close()

    def trash_button_callback(self):
        current_row = self.table.currentRow()
        self.table.removeRow(current_row)

    def add_button_callback(self):
        a = self.table.rowCount()
        self.table.setRowCount(a+1) 
        self.table.setItem(a, 0, QTableWidgetItem(self.lineEdit_refining_size.text()))
        self.table.setItem(a, 1, QTableWidgetItem(self.lineEdit_faces_list.text()))
        self.lineEdit_refining_size.setText("")
        self.lineEdit_faces_list.setText("")

    def geometry_selection_callback(self, points, lines, faces):
        faces_list = ", ".join([str(i) for i in faces])
        self.lineEdit_faces_list.setText(faces_list)
    
    def get_inputs_table(self):
        faces_and_refined_size_list = []
        for i in range(self.table.rowCount()):
            mesh_text = float(self.table.item(i,0).text())
            faces_text = self.table.item(i,1).text()
            faces_text = [int(i) for i in faces_text.split(",")]
            faces_and_refined_size_list.append((mesh_text,faces_text))
        
        return faces_and_refined_size_list
        
    def check_mesh_inputs(self):

        lineEdit = self.lineEdit_global_mesh_size
        global_mesh_size = self.check_inputs(lineEdit, "Global mesh size")
        if self.stop:
            lineEdit.setFocus()
            return True
        
        lineEdit = self.lineEdit_geometry_tolerance
        geometry_tolerance = self.check_inputs(lineEdit, "Geometry tolerance")
        if self.stop:
            lineEdit.setFocus()
            return True

        _element_type = self.comboBox_element_type.currentText()
        _shape_function = self.comboBox_shape_function.currentText()

        if _element_type == "Tetrahedral" and _shape_function == "Linear":
            solid_element = TETRAHEDRON_4
        elif _element_type == "Tetrahedral" and _shape_function == "Quadratic":
            solid_element = TETRAHEDRON_10
        elif _element_type == "Hexahedral" and _shape_function == "Linear":
            solid_element = HEXAHEDRON_8
        elif _element_type == "Hexahedral" and _shape_function == "Quadratic":
            solid_element = HEXAHEDRON_20
        else:
            raise NotImplementedError(f"Element type not defined!")

        self.mesh_setup = { "element_type": solid_element,
                            "geometry_tolerance": geometry_tolerance,
                            "size_factor": 0,
                            "minimum_element_size": global_mesh_size,
                            "maximum_element_size": global_mesh_size,
                            "mesh_refinement_parameters": self.get_inputs_table(),
                            "mesh_connection": self.mesh_connection_checkbox.isChecked() }
 
    def check_inputs(self, lineEdit, label, only_positive=True, zero_included=False, _float=True):
        self.stop = False
        message = ""
        title = "Invalid input at mesh setup"
        window_title = "ERROR"
        if lineEdit.text() != "":
            try:
                if _float:
                    out = float(lineEdit.text())
                else:
                    out = int(lineEdit.text())

                if only_positive:
                    if zero_included:
                        if out < 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is allowed."
                    else:
                        if out <= 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is not allowed."

            except Exception as _err:
                message = "Dear user, you have typed and invalid value at the \n"
                message += f"{label} input field.\n\n"
                message += str(_err)

        else:
            if zero_included:
                return float(0)
            else:
                message = f"Insert some value at the {label} input field."

        if message != "":
            PrintMessageInput([window_title, title, message])
            self.stop = True
            return None
        return out

    # fmt: on