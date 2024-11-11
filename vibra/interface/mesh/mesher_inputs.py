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
from vibra.utils.progress_status import ProgressStatus

import logging

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

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.complete = False
        self.keep_window_open = True

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.main_window.vibra_icon)
        self.setWindowTitle("Mesher setup")

    def _define_qt_variables(self):

        # QCheckbox
        self.checkBox_mesh_connection: QCheckBox

        # QComboBox
        self.comboBox_element_type: QComboBox
        self.comboBox_shape_function: QComboBox

        # QDoubleSpinBox
        self.doubleSpinBox_maximum_element_size: QDoubleSpinBox
        self.doubleSpinBox_minimum_element_size_factor: QDoubleSpinBox

        # QLineEdit
        self.lineEdit_maximum_element_size: QLineEdit
        self.lineEdit_geometry_tolerance: QLineEdit
        self.lineEdit_refining_size: QLineEdit
        self.lineEdit_selected_ids: QLineEdit

        # QPushButton
        self.pushButton_add: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_delete: QPushButton
        self.pushButton_generate_mesh: QPushButton

        # QTableWidget
        self.tableWidget_refining_mesh_data: QTableWidget
        self._config_tableWidget_appearance()

    def _config_tableWidget_appearance(self):
        header = ["Refining mesh size [mm]", "Selection type", "Selection IDs"]
        self.tableWidget_refining_mesh_data.setColumnCount(len(header))
        self.tableWidget_refining_mesh_data.setHorizontalHeaderLabels(header)
        self.tableWidget_refining_mesh_data.setSelectionBehavior(1)
        self.tableWidget_refining_mesh_data.resizeColumnsToContents()
        self.tableWidget_refining_mesh_data.horizontalHeader().setSectionResizeMode(0)
        self.tableWidget_refining_mesh_data.horizontalHeader().setStretchLastSection(True)

    def _create_connections(self):
        self.pushButton_add.clicked.connect(self.add_button_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_delete.clicked.connect(self.trash_button_callback)
        self.pushButton_generate_mesh.clicked.connect(self.generate_mesh_callback)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)

    def _load_current_mesh_setup(self):
        mesh_setup = app().main_window.project.model.mesh_setup
        if mesh_setup:
            try:
                element_type = mesh_setup["element_type"]
                geometry_tolerance = mesh_setup["geometry_tolerance"]
                minimum_element_size = mesh_setup["minimum_element_size"]
                maximum_element_size = mesh_setup["maximum_element_size"]
                size_factor = minimum_element_size / maximum_element_size
                mesh_refinement_parameters = mesh_setup["mesh_refinement_parameters"]
                mesh_connection = mesh_setup["mesh_connection"]

                self.update_element_type(element_type)
                
                self.doubleSpinBox_maximum_element_size.setValue(maximum_element_size)
                self.doubleSpinBox_minimum_element_size_factor.setValue(size_factor)
                self.lineEdit_geometry_tolerance.setText(str(geometry_tolerance))
                self.checkBox_mesh_connection.setChecked(mesh_connection)

                if app().main_window.selected_geometry_volumes:
                    selection_type = "volumes"
                else:
                    selection_type = "surfaces"

                self.tableWidget_refining_mesh_data.clearContents()
                for e_size, surface_ids in mesh_refinement_parameters:

                    row = self.tableWidget_refining_mesh_data.rowCount()
                    rows = row + 1

                    str_surface_ids = ", ".join([str(i) for i in surface_ids])
                    self.tableWidget_refining_mesh_data.setRowCount(rows)

                    self.tableWidget_refining_mesh_data.setItem(row, 0, QTableWidgetItem(str(e_size)))
                    self.tableWidget_refining_mesh_data.setItem(row, 1, QTableWidgetItem(selection_type))
                    self.tableWidget_refining_mesh_data.setItem(row, 2, QTableWidgetItem(str_surface_ids))

                    for j in range(3):
                        self.tableWidget_refining_mesh_data.item(row, j).setTextAlignment(Qt.AlignCenter)

            except Exception as error_log:
                self.hide()
                title = "Error while loading mesh setup"
                message = str(error_log)
                PrintMessageInput([window_title_1, title, message])

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

        try:

            if self.check_mesh_inputs():
                return

            self.hide()

            def generate_function():

                logging.info("Processing mesh..." + ProgressStatus(20, 100))
                app().main_window.viewer_tabs.close_analysis_tabs()
                app().main_window.project.reset_solutions()

                logging.info("Processing mesh..." + ProgressStatus(30, 100))
                app().main_window.project.set_mesh_setup(self.mesh_setup)
                app().main_window.file.write_mesh_setup_in_file(self.file_mesh_setup)

                logging.info("Processing mesh..." + ProgressStatus(40, 100))
                app().main_window.project.generate_mesh()

            generate_mesh = load_function(generate_function, app().main_window)
            generate_mesh()

            app().main_window.file.write_mesh_data_in_file()

            actions_to_finalize = load_function(self.actions_to_finalize, self.main_window)
            actions_to_finalize()

            self.complete = True
            self.pushButton_cancel.setText("Exit")

        except Exception as error_log:
            window_title = "Error"
            title = "Error while processing mesh"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])

    def actions_to_finalize(self):
        if self.close_after_generate:
            self.close()
        logging.info("Updating render..." + ProgressStatus(95, 100))
        app().main_window.viewer_tabs.show_mesh()
        app().main_window.viewer_tabs.close_analysis_tabs()
        app().main_window.viewer_tabs.update_plots()

    def trash_button_callback(self):
        current_row = self.tableWidget_refining_mesh_data.currentRow()
        self.tableWidget_refining_mesh_data.removeRow(current_row)

    def add_button_callback(self):

        row = self.tableWidget_refining_mesh_data.rowCount()
        rows = row + 1
        self.tableWidget_refining_mesh_data.setRowCount(rows)

        if app().main_window.selected_geometry_volumes:
            selected_type = "volumes"
        else:
            selected_type = "surfaces"

        self.tableWidget_refining_mesh_data.setItem(row, 0, QTableWidgetItem(self.lineEdit_refining_size.text()))
        self.tableWidget_refining_mesh_data.setItem(row, 1, QTableWidgetItem(selected_type))
        self.tableWidget_refining_mesh_data.setItem(row, 2, QTableWidgetItem(self.lineEdit_selected_ids.text()))

        for j in range(3):
            self.tableWidget_refining_mesh_data.item(row, j).setTextAlignment(Qt.AlignCenter)

        self.lineEdit_refining_size.setText("")
        self.lineEdit_selected_ids.setText("")

    def geometry_selection_callback(self):

        faces = self.main_window.selected_geometry_surfaces
        volumes = self.main_window.selected_geometry_volumes

        if volumes:
            selection = volumes
        else:
            selection = faces

        if selection:
            text = ", ".join([str(i) for i in selection])
            self.lineEdit_selected_ids.setText(text)

    def get_inputs_table(self):

        refine_data = list()
        for i in range(self.tableWidget_refining_mesh_data.rowCount()):
            refine_size = float(self.tableWidget_refining_mesh_data.item(i, 0).text())
            selection_type = self.tableWidget_refining_mesh_data.item(i, 1).text()
            str_selection_ids = self.tableWidget_refining_mesh_data.item(i, 2).text()
            selection_ids = [int(i) for i in str_selection_ids.split(",")]
            refine_data.append((refine_size, selection_type, selection_ids))

        return refine_data
        
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
                                "element_type" : _element_type,
                                "shape_function" : _shape_function,
                                "geometry_tolerance" : geometry_tolerance,
                                "size_factor" : 0,
                                "minimum_element_size" : min_factor*maximum_element_size,
                                "maximum_element_size" : maximum_element_size,
                                "mesh_refinement_parameters" : self.get_inputs_table(),
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.generate_mesh_callback()
        elif event.key() == Qt.Key_Delete:
            return
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)

# fmt: on