from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vibra import UI_DIR
from vibra.engine.mesher.element_type import *
from vibra.interface.general.call_double_confirmation_input import CallDoubleConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.interface_functions import get_main_window


class MesherInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "mesh/element_setup.ui"
        uic.loadUi(ui_path, self)

        icon_path = str(Path("data/icons/logo_vibra.png"))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Mesher setup")

        self.main_window = get_main_window()
        self.main_window.set_input_widget(self)

        self.complete = False
        self._define_qt_variables()
        self._create_connections()
        self._config_window()
        self.exec()

    def _define_qt_variables(self):
        # Papai do céu está triste com tanto camelCase em vez de snake_case =(

        # QCheckBox objects
        self.checkBox_size_factor = self.findChild(QCheckBox, "checkBox_size_factor")
        self.checkBox_recomb_all_triangular_mesh = self.findChild(
            QCheckBox, "checkBox_recomb_all_triangular_mesh"
        )
        self.checkBox_use_incomplete_elements = self.findChild(
            QCheckBox, "checkBox_use_incomplete_elements"
        )
        self.checkBox_recomb_all_triangular_mesh = self.findChild(
            QCheckBox, "checkBox_recomb_all_triangular_mesh"
        )
        self.checkBox_use_incomplete_elements = self.findChild(
            QCheckBox, "checkBox_use_incomplete_elements"
        )

        # QComboBox objects
        self.comboBox_element_shape = self.findChild(QComboBox, "comboBox_element_shape")
        self.comboBox_shape_function = self.findChild(QComboBox, "comboBox_shape_function")
        self.comboBox_2D_algorithm = self.findChild(QComboBox, "comboBox_2D_algorithm")
        self.comboBox_3D_algorithm = self.findChild(QComboBox, "comboBox_3D_algorithm")
        self.comboBox_2D_recomb_algorithm = self.findChild(
            QComboBox, "comboBox_2D_recomb_algorithm"
        )
        self.comboBox_subdivision_algorithm = self.findChild(
            QComboBox, "comboBox_subdivision_algorithm"
        )
        self.comboBox_element_order = self.findChild(QComboBox, "comboBox_element_order")

        # QLabel objects
        self.label_size_factor = self.findChild(QLabel, "label_size_factor")
        self.label_minimum_element_size_gen = self.findChild(
            QLabel, "label_minimum_element_size_gen"
        )
        self.label_maximum_element_size_gen = self.findChild(
            QLabel, "label_maximum_element_size_gen"
        )

        # QLineEdit objects
        self.lineEdit_size_factor_gen = self.findChild(QLineEdit, "lineEdit_size_factor_gen")
        self.lineEdit_minimum_element_size_gen = self.findChild(
            QLineEdit, "lineEdit_minimum_element_size_gen"
        )
        self.lineEdit_maximum_element_size_gen = self.findChild(
            QLineEdit, "lineEdit_maximum_element_size_gen"
        )
        self.lineEdit_geometry_tolerance_gen = self.findChild(
            QLineEdit, "lineEdit_geometry_tolerance_gen"
        )
        self.lineEdit_smoothing_steps = self.findChild(QLineEdit, "lineEdit_smoothing_steps")
        self.lineEdit_size_factor_adv = self.findChild(QLineEdit, "lineEdit_size_factor_adv")
        self.lineEdit_minimum_element_size_adv = self.findChild(
            QLineEdit, "lineEdit_minimum_element_size_adv"
        )
        self.lineEdit_maximum_element_size_adv = self.findChild(
            QLineEdit, "lineEdit_maximum_element_size_adv"
        )
        self.lineEdit_geometry_tolerance_adv = self.findChild(
            QLineEdit, "lineEdit_geometry_tolerance_adv"
        )
        self.lineEdit_minimum_element_size_adv = self.findChild(
            QLineEdit, "lineEdit_minimum_element_size_adv"
        )

        # QPushButton object
        self.pushButton_confirm_mesh_setup = self.findChild(
            QPushButton, "pushButton_confirm_mesh_setup"
        )

        # QTabWidget object
        self.tabWidget_element_options = self.findChild(QTabWidget, "tabWidget_element_options")
        self.tabWidget_element_options.setTabEnabled(1, False)

    def _create_connections(self):
        self.checkBox_size_factor.clicked.connect(self._update_visibility)
        self.checkBox_recomb_all_triangular_mesh.clicked.connect(self._update_visibility)
        self.checkBox_use_incomplete_elements.clicked.connect(self._update_visibility)
        self.pushButton_confirm_mesh_setup.clicked.connect(self.confirm_mesh_setup)
        self.tabWidget_element_options.currentChanged.connect(self.update_tab_selection)
        self._update_visibility()

    def _config_window(self):
        return
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

    def reset_mesh_setup_variables(self):
        #
        self.size_factor = 0.0
        self.smoothing_steps = 0.0
        self.minimum_element_size = 0.0
        self.maximum_element_size = 0.0
        self.mesh_setup = {}
        #

    def check_inputs_for_general_tab(self):
        #
        self.reset_mesh_setup_variables()
        element_shape = self.comboBox_element_shape.currentText()[2:]
        shape_function = self.comboBox_shape_function.currentText()[2:]
        #
        if element_shape == "Tetrahedral" and shape_function == "Linear":
            self.element_type = TETRAHEDRON_4
        elif element_shape == "Tetrahedral" and shape_function == "Quadratic":
            self.element_type = TETRAHEDRON_10
        elif element_shape == "Hexahedral" and shape_function == "Linear":
            self.element_type = HEXAHEDRON_8
        elif element_shape == "Hexahedral" and shape_function == "Quadratic":
            self.element_type = HEXAHEDRON_20
        else:
            raise NotImplementedError(f"Element type not defined!")
        #
        lineEdit = self.lineEdit_geometry_tolerance_gen
        self.geometry_tolerance = self.check_inputs(lineEdit, "Geometry tolerance")
        if self.geometry_tolerance is None:
            return True
        #
        if self.checkBox_size_factor.isChecked():
            lineEdit = self.lineEdit_size_factor_gen
            self.size_factor = self.check_inputs(lineEdit, "Size factor")
            if self.size_factor is None:
                return True

        else:
            lineEdit = self.lineEdit_minimum_element_size_gen
            self.minimum_element_size = self.check_inputs(lineEdit, "Minimum element size")
            if self.minimum_element_size is None:
                return True

            lineEdit = self.lineEdit_maximum_element_size_gen
            self.maximum_element_size = self.check_inputs(lineEdit, "Maximum element size")
            if self.maximum_element_size is None:
                return True

    def check_inputs_for_advanced_tab(self):
        #
        self.reset_mesh_setup_variables()
        #
        _algorithm_2D = self.comboBox_2D_algorithm.currentIndex()
        _algorithm_3D = self.comboBox_3D_algorithm.currentIndex()
        _recomb_algorithm_2D = self.comboBox_2D_recomb_algorithm.currentIndex()
        _subdivision_algorithm = self.comboBox_subdivision_algorithm.currentIndex()
        _element_order = self.comboBox_element_order.currentIndex()

        _recomb_all_triang_mesh = self.checkBox_recomb_all_triangular_mesh.isChecked()
        _use_incomplete_elements = self.checkBox_use_incomplete_elements.isChecked()

        self.element_type = ElementType(
            algorithm_2d=_algorithm_2D,
            algorithm_3d=_algorithm_3D,
            subdivision_algorithm=_subdivision_algorithm,
            recombination_algorithm=_recomb_algorithm_2D,
            recombine_all=_recomb_all_triang_mesh,
            second_order_incomplete=_use_incomplete_elements,
            element_order=_element_order,
        )

        lineEdit = self.lineEdit_smoothing_steps
        self.smoothing_steps = self.check_inputs(lineEdit, "Smoothing steps")
        if self.smoothing_steps is None:
            return True

        lineEdit = self.lineEdit_size_factor_adv
        self.size_factor = self.check_inputs(lineEdit, "Size factor")
        if self.size_factor is None:
            return True

        lineEdit = self.lineEdit_minimum_element_size_adv
        self.minimum_element_size = self.check_inputs(lineEdit, "Minimum element size")
        if self.minimum_element_size is None:
            return True

        lineEdit = self.lineEdit_maximum_element_size_adv
        self.maximum_element_size = self.check_inputs(lineEdit, "Maximum element size")
        if self.maximum_element_size is None:
            return True

        lineEdit = self.lineEdit_geometry_tolerance_adv
        self.geometry_tolerance = self.check_inputs(lineEdit, "Geometry tolerance")
        if self.geometry_tolerance is None:
            return True

    def confirm_mesh_setup(self):
        #
        if self.tabWidget_element_options.currentIndex() == 0:
            if self.check_inputs_for_general_tab():
                return
        #
        elif self.tabWidget_element_options.currentIndex() == 1:
            if self.check_inputs_for_advanced_tab():
                return
        #
        self.mesh_setup = {
            "element_type": self.element_type,
            "geometry_tolerance": self.geometry_tolerance,
            "size_factor": self.size_factor,
            "minimum_element_size": self.minimum_element_size,
            "maximum_element_size": self.maximum_element_size,
        }
        #
        self.complete = True
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
