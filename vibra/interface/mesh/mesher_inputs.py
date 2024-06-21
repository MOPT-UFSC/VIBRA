# fmt: off

from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QLineEdit, QPushButton, QDoubleSpinBox, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from vibra import UI_DIR
from vibra.engine.mesher.element_type import *
from vibra.interface.general.print_message_input2 import PrintMessageInput
from vibra.interface.loading_bar import load_function
from vibra.utils.interface_functions import get_main_window

from pathlib import Path

class MesherInputs(QDialog):
    def __init__(self, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "mesh/mesher_setup.ui"
        uic.loadUi(ui_path, self)

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
        self._define_qt_variables()
        self._create_connections()
        self.exec()

    def _define_qt_variables(self):
        # QCheckbox objects
        self.checkBox_mesh_connection = self.findChild(QCheckBox, 'checkBox_mesh_connection')
        # QComboBox objects
        self.comboBox_element_type = self.findChild(QComboBox, 'comboBox_element_type')
        self.comboBox_shape_function = self.findChild(QComboBox, 'comboBox_shape_function')
        # QDoubleSpinBox
        self.doubleSpinBox_maximum_element_size_factor = self.findChild(QDoubleSpinBox, 'doubleSpinBox_maximum_element_size_factor')
        self.doubleSpinBox_minimum_element_size_factor = self.findChild(QDoubleSpinBox, 'doubleSpinBox_minimum_element_size_factor')
        # QLineEdit objects
        self.lineEdit_maximum_element_size = self.findChild(QLineEdit, 'lineEdit_maximum_element_size')
        self.lineEdit_geometry_tolerance = self.findChild(QLineEdit, 'lineEdit_geometry_tolerance')
        self.lineEdit_refining_size = self.findChild(QLineEdit, 'lineEdit_refining_size')
        self.lineEdit_faces_list = self.findChild(QLineEdit, 'lineEdit_faces_list')
        # QPushButton objects
        self.pushButton_add = self.findChild(QPushButton, 'pushButton_add')
        self.pushButton_delete = self.findChild(QPushButton, 'pushButton_delete')
        self.pushButton_generate_mesh = self.findChild(QPushButton, 'pushButton_generate_mesh')
        # QTableWidget objects
        self.tableWidget_refining_mesh_data = self.findChild(QTableWidget, 'tableWidget_refining_mesh_data')
        self._config_tableWidget_appearance()

    def _config_tableWidget_appearance(self):
        header = ["Refining mesh size", "Faces list"]
        self.tableWidget_refining_mesh_data.setColumnCount(len(header))
        self.tableWidget_refining_mesh_data.setHorizontalHeaderLabels(header)
        self.tableWidget_refining_mesh_data.setSelectionBehavior(1)
        self.tableWidget_refining_mesh_data.resizeColumnsToContents()
        self.tableWidget_refining_mesh_data.horizontalHeader().setSectionResizeMode(0)
        self.tableWidget_refining_mesh_data.horizontalHeader().setStretchLastSection(True)

    def _create_connections(self):
        self.pushButton_add.clicked.connect(self.add_button_callback)
        self.pushButton_delete.clicked.connect(self.trash_button_callback)
        self.pushButton_generate_mesh.clicked.connect(self.pushButton_generate_mesh_callback)

    def pushButton_generate_mesh_callback(self):

        if self.check_mesh_inputs():
            return

        self.main_window.project.reset_solutions()
        self.main_window.project.set_mesh_setup(self.mesh_setup)
        generate_mesh = load_function(self.main_window.project.generate_mesh, self.main_window)
        generate_mesh()

        self.main_window.viewer_tabs.show_mesh()
        self.main_window.viewer_tabs.close_analysis_tabs()
        self.main_window.viewer_tabs.update_plots()

        self.complete = True
        if self.close_after_generate:
            self.close()

    def trash_button_callback(self):
        current_row = self.tableWidget_refining_mesh_data.currentRow()
        self.tableWidget_refining_mesh_data.removeRow(current_row)

    def add_button_callback(self):
        a = self.tableWidget_refining_mesh_data.rowCount()
        self.tableWidget_refining_mesh_data.setRowCount(a+1) 
        self.tableWidget_refining_mesh_data.setItem(a, 0, QTableWidgetItem(self.lineEdit_refining_size.text()))
        self.tableWidget_refining_mesh_data.setItem(a, 1, QTableWidgetItem(self.lineEdit_faces_list.text()))
        self.lineEdit_refining_size.setText("")
        self.lineEdit_faces_list.setText("")

    def geometry_selection_callback(self, points, lines, faces):
        faces_list = ", ".join([str(i) for i in faces])
        self.lineEdit_faces_list.setText(faces_list)
    
    def get_inputs_table(self):
        faces_and_refined_size_list = []
        for i in range(self.tableWidget_refining_mesh_data.rowCount()):
            mesh_text = float(self.tableWidget_refining_mesh_data.item(i,0).text())
            faces_text = self.tableWidget_refining_mesh_data.item(i,1).text()
            faces_text = [int(i) for i in faces_text.split(",")]
            faces_and_refined_size_list.append((mesh_text,faces_text))
        
        return faces_and_refined_size_list
        
    def check_mesh_inputs(self):

        maximum_element_size = self.doubleSpinBox_maximum_element_size_factor.value()
        min_factor = self.doubleSpinBox_minimum_element_size_factor.value()

        lineEdit = self.lineEdit_geometry_tolerance
        geometry_tolerance = self.check_inputs(lineEdit, "Geometry tolerance")
        if self.stop:
            lineEdit.setFocus()
            return True

        _element_type = self.comboBox_element_type.currentText()
        _shape_function = self.comboBox_shape_function.currentText()

        if _element_type == " Tetrahedral" and _shape_function == " Linear":
            solid_element = TETRAHEDRON_4
        elif _element_type == " Tetrahedral" and _shape_function == " Quadratic":
            solid_element = TETRAHEDRON_10
        elif _element_type == " Hexahedral" and _shape_function == " Linear":
            solid_element = HEXAHEDRON_8
        elif _element_type == " Hexahedral" and _shape_function == " Quadratic":
            solid_element = HEXAHEDRON_20
        else:
            raise NotImplementedError(f"Element type not defined!")
        
        connected_mesh = self.checkBox_mesh_connection.isChecked()
        self.mesh_setup = { "element_type": solid_element,
                            "geometry_tolerance": geometry_tolerance,
                            "size_factor": 0,
                            "minimum_element_size": min_factor*maximum_element_size,
                            "maximum_element_size": maximum_element_size,
                            "mesh_refinement_parameters": self.get_inputs_table(),
                            "mesh_connection": connected_mesh}
 
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