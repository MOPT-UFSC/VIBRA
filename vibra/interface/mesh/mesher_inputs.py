# fmt: off

from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QLineEdit, QPushButton, QDoubleSpinBox, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.engine.mesher.element_type import *
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_bar import load_function

from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"


class MesherInputs(QDialog):
    def __init__(self, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "mesh/mesher_setup.ui"
        uic.loadUi(ui_path, self)

        self.close_after_generate = kwargs.get("close_after_generate", False)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)

        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

        self._load_current_mesh_setup()
        self.exec()

    def _initialize(self):
        self.complete = False

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.main_window.vibra_icon)
        self.setWindowTitle("Mesher setup")

    def _define_qt_variables(self):

        # QCheckbox
        self.checkBox_mesh_connection : QCheckBox

        # QComboBox
        self.comboBox_element_type : QComboBox
        self.comboBox_shape_function : QComboBox

        # QDoubleSpinBox
        self.doubleSpinBox_maximum_element_size : QDoubleSpinBox
        self.doubleSpinBox_minimum_element_size_factor : QDoubleSpinBox

        # QLineEdit
        self.lineEdit_maximum_element_size : QLineEdit
        self.lineEdit_geometry_tolerance : QLineEdit
        self.lineEdit_refining_size : QLineEdit
        self.lineEdit_faces_list : QLineEdit

        # QPushButton
        self.pushButton_add : QPushButton
        self.pushButton_delete : QPushButton
        self.pushButton_generate_mesh : QPushButton

        # QTableWidget
        self.tableWidget_refining_mesh_data : QTableWidget
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
        self.pushButton_generate_mesh.clicked.connect(self.generate_mesh_callback)

    def _load_current_mesh_setup(self):
        mesh_setup = app().main_window.project.model.mesh_setup
        if mesh_setup:
            try:
                element_type = mesh_setup["element_type"]
                geometry_tolerance = mesh_setup["geometry_tolerance"]
                minimum_element_size = mesh_setup["minimum_element_size"]
                maximum_element_size = mesh_setup["maximum_element_size"]
                size_factor = minimum_element_size / maximum_element_size
                # TODO: finalize in future updates
                # mesh_refinement_parameters = mesh_setup["mesh_refinement_parameters"]
                mesh_connection = mesh_setup["mesh_connection"]

                self.update_element_type(element_type)
                
                self.doubleSpinBox_maximum_element_size.setValue(maximum_element_size)
                self.doubleSpinBox_minimum_element_size_factor.setValue(size_factor)
                self.lineEdit_geometry_tolerance.setText(str(geometry_tolerance))
                self.checkBox_mesh_connection.setChecked(mesh_connection)

            except Exception as error_log:
                print(str(error_log))
                pass

    def update_element_type(self, element_type):
        if element_type == TETRAHEDRON_4:
            self.comboBox_element_type.setCurrentIndex(0)
            self.comboBox_shape_function.setCurrentIndex(0)
        elif element_type == TETRAHEDRON_10:
            self.comboBox_element_type.setCurrentIndex(0)
            self.comboBox_shape_function.setCurrentIndex(1)
        elif element_type == HEXAHEDRON_8:
            self.comboBox_element_type.setCurrentIndex(1)
            self.comboBox_shape_function.setCurrentIndex(0)
        elif element_type == HEXAHEDRON_20:
            self.comboBox_element_type.setCurrentIndex(1)
            self.comboBox_shape_function.setCurrentIndex(1)
        else:
            NotImplementedError()

    def generate_mesh_callback(self):

        if self.check_mesh_inputs():
            return

        condition = self.lineEdit_faces_list.text() == "" and self.lineEdit_refining_size.text() == ""
        if condition or self.close_after_generate:
            self.close()

        self.main_window.project.reset_solutions()
        self.main_window.project.set_mesh_setup(self.mesh_setup)
        app().main_window.file.write_mesh_setup_in_file(self.file_mesh_setup)

        generate_mesh = load_function(self.main_window.project.generate_mesh, self.main_window)
        generate_mesh()

        self.main_window.viewer_tabs.show_mesh()
        self.main_window.viewer_tabs.close_analysis_tabs()
        self.main_window.viewer_tabs.update_plots()


        # TODO: Remove this as soon as possible
        # try:

        #     # surf_tag = 5
        #     vol_tag = 1

        #     app().main_window.viewer_tabs.show_mesh()
        #     mesh_widget = app().main_window.viewer_tabs.mesh_widget
        #     # surface_elements = app().main_window.project.model.mesh.elements_from_surface[surf_tag]
        #     volume_elements = app().main_window.project.model.mesh.elements_from_volume[vol_tag]

        #     # mesh_widget.select_multiple_nodes(nodes)
        #     # mesh_widget.select_multiple_faces(surface_elements)
        #     # mesh_widget.select_multiple_volumes(volume_elements)

        # except:
        #     pass

        self.complete = True


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

        maximum_element_size = self.doubleSpinBox_maximum_element_size.value()
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
        self.mesh_setup = { 
                            "element_type" : solid_element,
                            "geometry_tolerance" : geometry_tolerance,
                            "size_factor" : 0,
                            "minimum_element_size" : min_factor*maximum_element_size,
                            "maximum_element_size" : maximum_element_size,
                            "mesh_refinement_parameters" : self.get_inputs_table(),
                            "mesh_connection" : connected_mesh
                            }
        
        self.file_mesh_setup = { 
                                "element_type" : self.comboBox_element_type.currentIndex(),
                                "shape_function" : self.comboBox_shape_function.currentIndex(),
                                "geometry_tolerance" : geometry_tolerance,
                                "size_factor" : 0,
                                "minimum_element_size" : min_factor*maximum_element_size,
                                "maximum_element_size" : maximum_element_size,
                                "mesh_refinement_parameters" : list(),
                                "mesh_connection" : connected_mesh
                                }

    def check_inputs(self, lineEdit, label, only_positive=True, zero_included=False, _float=True):

        self.stop = False
        message = ""
        title = "Invalid input at mesh setup"

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
            PrintMessageInput([window_title_1, title, message])
            self.stop = True
            return None
        return out

# fmt: on