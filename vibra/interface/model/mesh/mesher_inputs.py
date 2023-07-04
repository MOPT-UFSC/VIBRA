from PyQt5.QtWidgets import *
from PyQt5 import uic

from interface.general.callDoubleConfirmationInput import CallDoubleConfirmationInput
from interface.general.printMessageInput import PrintMessageInput


class MesherInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super(QDialog, self).__init__(*args, **kwargs)

        uic.loadUi("data/ui_files/mesh/element_setup.ui", self)
        
        self._define_Qt_variables()
        self._create_connections()
        self._config_window()
        self.show()


    def _define_Qt_variables(self):

        # QCheckBox objects
        self.checkBox_size_factor = self.findChild(QCheckBox, "checkBox_size_factor")
        self.checkBox_recomb_all_triangular_mesh = self.findChild(QCheckBox, "checkBox_recomb_all_triangular_mesh")
        self.checkBox_use_incomplete_elements = self.findChild(QCheckBox, "checkBox_use_incomplete_elements")
        self.checkBox_recomb_all_triangular_mesh = self.findChild(QCheckBox, "checkBox_recomb_all_triangular_mesh")
        self.checkBox_use_incomplete_elements = self.findChild(QCheckBox, "checkBox_use_incomplete_elements")

        # QComboBox objects
        self.comboBox_element_shape = self.findChild(QComboBox, "comboBox_element_shape")
        self.comboBox_shape_functions = self.findChild(QComboBox, "comboBox_shape_functions")
        self.comboBox_2D_algorithm = self.findChild(QComboBox, "comboBox_2D_algorithm")
        self.comboBox_3D_algorithm = self.findChild(QComboBox, "comboBox_3D_algorithm")
        self.comboBox_2D_recomb_algorithm = self.findChild(QComboBox, "comboBox_2D_recomb_algorithm")
        self.comboBox_subdivision_algorithm = self.findChild(QComboBox, "comboBox_subdivision_algorithm")
        self.comboBox_element_order = self.findChild(QComboBox, "comboBox_element_order")
        
        # QLabel objects
        self.label_size_factor = self.findChild(QLabel, "label_size_factor")
        self.label_minimum_element_size_gen = self.findChild(QLabel, "label_minimum_element_size_gen")
        self.label_maximum_element_size_gen = self.findChild(QLabel, "label_maximum_element_size_gen")

        # QLineEdit objects
        self.lineEdit_size_factor_gen = self.findChild(QLineEdit, "lineEdit_size_factor_gen")
        self.lineEdit_minimum_element_size_gen = self.findChild(QLineEdit, "lineEdit_minimum_element_size_gen")
        self.lineEdit_maximum_element_size_gen = self.findChild(QLineEdit, "lineEdit_maximum_element_size_gen")
        self.lineEdit_geometry_tolerance_gen = self.findChild(QLineEdit, "lineEdit_geometry_tolerance_gen")
        self.lineEdit_smoothing_steps = self.findChild(QLineEdit, "lineEdit_smoothing_steps")
        self.lineEdit_size_factor_adv = self.findChild(QLineEdit, "lineEdit_size_factor_adv")
        self.lineEdit_minimum_element_size_adv = self.findChild(QLineEdit, "lineEdit_minimum_element_size_adv")
        self.lineEdit_maximum_element_size_adv = self.findChild(QLineEdit, "lineEdit_maximum_element_size_adv")
        self.lineEdit_geometry_tolerance_adv = self.findChild(QLineEdit, "lineEdit_geometry_tolerance_adv")
        self.lineEdit_minimum_element_size_adv = self.findChild(QLineEdit, "lineEdit_minimum_element_size_adv")

        # QPushButton object
        self.pushButton_confirm_mesh_setup = self.findChild(QPushButton, "pushButton_confirm_mesh_setup")

        # QTabWidget object
        self.tabWidget_element_options = self.findChild(QTabWidget, "tabWidget_element_options")

    
    def _create_connections(self):
        self.checkBox_size_factor.clicked.connect(self._update_visibility)
        self.checkBox_recomb_all_triangular_mesh.clicked.connect(self._update_visibility)
        self.checkBox_use_incomplete_elements.clicked.connect(self._update_visibility)
        self.pushButton_confirm_mesh_setup.clicked.connect(self.confirm_mesh_setup)
        self.tabWidget_element_options.currentChanged.connect(self.update_tab_selection)
        self._update_visibility()


    def _config_window(self):
        if self.tabWidget_element_options.currentIndex() == 0:
            self.setMinimumSize(604, 500)
            self.setMaximumSize(604, 500)
        elif self.tabWidget_element_options.currentIndex() == 1:
            self.setMinimumSize(604, 720)
            self.setMaximumSize(604, 720)


    def _update_visibility(self):
        if self.tabWidget_element_options.currentIndex() == 0:
            _bool = self.checkBox_size_factor.isChecked()
            #
            if _bool:
                self.checkBox_size_factor.setText("Enabled")
            else:
                self.checkBox_size_factor.setText("Disabled")
            #
            self.label_size_factor.setDisabled(not _bool)
            self.lineEdit_size_factor_gen.setDisabled(not _bool)
            self.label_minimum_element_size_gen.setDisabled(_bool)
            self.label_maximum_element_size_gen.setDisabled(_bool)
            self.lineEdit_minimum_element_size_gen.setDisabled(_bool)
            self.lineEdit_maximum_element_size_gen.setDisabled(_bool)

        elif self.tabWidget_element_options.currentIndex() == 1:
            #
            if self.checkBox_recomb_all_triangular_mesh.isChecked():
                self.checkBox_recomb_all_triangular_mesh.setText("Enabled")
            else:
                self.checkBox_recomb_all_triangular_mesh.setText("Disabled")
            #    
            if self.checkBox_use_incomplete_elements.isChecked():
                self.checkBox_use_incomplete_elements.setText("Enabled")
            else:
                self.checkBox_use_incomplete_elements.setText("Disabled")


    def update_tab_selection(self):
        self._config_window()


    def check_inputs_for_general_tab(self):

        element_shape = self.comboBox_element_shape.currentText()
        shape_function = self.comboBox_shape_functions.currentText()

        if self.checkBox_size_factor.isChecked():
        
            lineEdit = self.lineEdit_size_factor_gen
            size_factor = self.check_inputs(lineEdit, "Size factor")
            if size_factor is None:
                return True
        
        else:

            lineEdit = self.lineEdit_minimum_element_size_gen
            minimum_element_size = self.check_inputs(lineEdit, "Minimum element size")
            if minimum_element_size is None:
                return True
            
            lineEdit = self.lineEdit_maximum_element_size_gen
            maximum_element_size = self.check_inputs(lineEdit, "Maximum element size")
            if maximum_element_size is None:
                return True
        
        lineEdit = self.lineEdit_geometry_tolerance_gen
        geometry_tolerance = self.check_inputs(lineEdit, "Geometry tolerance")
        if geometry_tolerance is None:
            return True  


    def check_inputs_for_advanced_tab(self):

        _2D_algorithm = self.comboBox_2D_algorithm.currentText()
        _3D_algorithm = self.comboBox_3D_algorithm.currentText()
        _2D_recomb_algorithm = self.comboBox_2D_recomb_algorithm.currentText()
        _subdivision_algorithm = self.comboBox_subdivision_algorithm.currentText()
        _element_order = self.comboBox_element_order.currentText()

        _recomb_all_triang_mesh = self.checkBox_recomb_all_triangular_mesh.isChecked()
        _use_incomplete_elements = self.checkBox_use_incomplete_elements.isChecked()
                
        lineEdit = self.lineEdit_smoothing_steps
        smoothing_steps = self.check_inputs(lineEdit, "Smoothing steps")
        if smoothing_steps is None:
            return True
        
        lineEdit = self.lineEdit_size_factor_adv
        size_factor = self.check_inputs(lineEdit, "Size factor")
        if size_factor is None:
            return True
        
        lineEdit = self.lineEdit_minimum_element_size_gen
        minimum_element_size = self.check_inputs(lineEdit, "Minimum element size")
        if minimum_element_size is None:
            return True
        
        lineEdit = self.lineEdit_maximum_element_size_gen
        maximum_element_size = self.check_inputs(lineEdit, "Maximum element size")
        if maximum_element_size is None:
            return True      

        lineEdit = self.lineEdit_geometry_tolerance_adv
        geometry_tolerance = self.check_inputs(lineEdit, "Geometry tolerance")
        if geometry_tolerance is None:
            return True  

    
    def confirm_mesh_setup(self):
        if self.tabWidget_element_options.currentIndex() == 0:
            if self.check_inputs_for_general_tab():
                return
        elif self.tabWidget_element_options.currentIndex() == 1:
            if self.check_inputs_for_advanced_tab():
                return
        self.close()


    def check_inputs(self, lineEdit, label, only_positive=True, zero_included=False):
        self.stop = False
        window_title = "ERROR"
        title = "MESH SETUP INPUT ERROR"
        if lineEdit.text() != "":
            try:
                out = float(lineEdit.text())
                if only_positive:
                    if zero_included:
                        if out < 0:

                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is allowed."
                            PrintMessageInput([title, message, window_title])
                            self.stop = True
                            return None
                    else:
                        if out <= 0:

                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is not allowed."
                            PrintMessageInput([title, message, window_title])
                            self.stop = True
                            return None
            except Exception as _err:

                message = f"Wrong input for {label}.\n\n"
                message += str(_err)
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return None
        else:
            if zero_included:
                return float(0)
            else: 

                message = f"Insert some value at the {label} input field."
                PrintMessageInput([title, message, window_title])                   
                self.stop = True
                return None
        return out