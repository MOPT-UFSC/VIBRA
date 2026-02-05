from PySide6.QtWidgets import QCheckBox, QDialog, QHBoxLayout, QHeaderView, QLineEdit, QPushButton, QTableWidgetItem, QWidget
from PySide6.QtGui import Qt, QIcon

from vibra import app, ICON_DIR
from vibra.engine import AnalysisID
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.ui_generated.analysis.user_defined_frequencies_by_manual_input_ui import UserDefinedFrequenciesByManualInput_UI

import numpy as np
from copy import deepcopy

error_title = "Error"


class UserDefinedFrequenciesByManualInput(UserDefinedFrequenciesByManualInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        # app().main_window.close_dialogs()
        # app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self._create_connections()
        self.load_analysis_setup()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.setup_defined = False
        self.solve_analysis = False
        self.keep_window_open = True
        self.user_defined_frequencies = list()

        self.remove_icon = QIcon(str(ICON_DIR / "delete.png"))

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Analysis setup")

    def _create_connections(self):
        #
        self.pushButton_add.clicked.connect(self.add_solution_step_callback)
        self.pushButton_confirm.clicked.connect(self.confirm_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_reset.clicked.connect(self.reset_callback)

    def reset_callback(self):

        self.hide()

        title = "Solution steps reset"
        message = "Would you like to remove all solution steps that have already been added?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            self.user_defined_frequencies.clear()
            self.update_solution_steps_table()

    def load_analysis_setup(self):

        self.index_to_push_buttons = dict()
        if app().project.model.properties.check_if_there_are_tables_at_the_model():
            return

        self.user_defined_frequencies = app().project.model.analysis_setup.get("user_defined_frequencies", list())
        self.update_solution_steps_table()

    def update_solution_steps_table(self):

        self.tableWidget_frequencies.clearContents()
        self.tableWidget_frequencies.setRowCount(len(self.user_defined_frequencies))
        self.tableWidget_frequencies.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        if not self.user_defined_frequencies:
            return

        for index, freq in enumerate(self.user_defined_frequencies):

            # Creates the QPushButton to control the solution step removal
            remove_button = QPushButton()
            remove_button.setIcon(self.remove_icon)
            remove_button.setCheckable(True)
            remove_button.setFixedSize(24,24)
            remove_button.clicked.connect(self.remove_solution_step_callback)
            self.index_to_push_buttons[index] = remove_button

            button_container = QWidget()
            cointeiner_layout = QHBoxLayout(button_container)
            cointeiner_layout.addStretch()
            cointeiner_layout.addWidget(self.index_to_push_buttons[index])
            cointeiner_layout.addStretch()
            cointeiner_layout.setContentsMargins(0, 0, 0, 0)

            self.tableWidget_frequencies.setItem(index, 0, QTableWidgetItem(str(index)))
            self.tableWidget_frequencies.setItem(index, 1, QTableWidgetItem(str(freq)))
            self.tableWidget_frequencies.setCellWidget(index, 2, button_container)

            for j in range(2):
                self.tableWidget_frequencies.item(index, j).setTextAlignment(Qt.AlignCenter)

    def check_inputs(self, line_edit: QLineEdit, label: str, zero_included: bool = False, int_value: bool = False):

        message = ""
        str_value = line_edit.text()
        str_value = str_value.replace(",", ".")

        if str_value != "":
            try:
                if int_value:
                    value = int(str_value)
                else:
                    value = float(str_value)

                if zero_included:
                    if value < 0:
                        message = f"Enter a positive value in the {label} input field. "
                else:
                    if value <= 0:
                        message = f"Enter a positive value in the {label} input field. "
                        message += "The zero value is not allowed."

            except Exception as _err:
                message = f"The value entered in the {label} input field is invalid.\n\n"
                message += str(_err)

        else:
            if zero_included:
                return float(0)
            else:
                message = f"Enter a positive value in the '{label}' input field."

        if message != "":
            self.hide()
            title = "Invalid input to the analysis setup"
            PrintMessageInput([error_title, title, message])
            return None

        return value
    
    def add_solution_step_callback(self):

        solution_step = self.check_inputs(self.lineEdit_solution_step, "solution step")
        if solution_step is None:
            self.lineEdit_solution_step.setFocus()
            return True
        
        if solution_step in self.user_defined_frequencies:
            return

        self.user_defined_frequencies.append(solution_step)
        self.user_defined_frequencies.sort()
        self.update_solution_steps_table()
        self.lineEdit_solution_step.setText("")
        self.lineEdit_solution_step.setFocus()

    def remove_solution_step_callback(self):

        for index, push_button in self.index_to_push_buttons.items():
            if push_button.isChecked():
                break
       
        if not isinstance(index, int):
            return
    
        solution_step_to_remove = float(self.tableWidget_frequencies.item(index, 1).text())
        if solution_step_to_remove in self.user_defined_frequencies:
            self.user_defined_frequencies.remove(solution_step_to_remove)
            self.update_solution_steps_table()

    def confirm_callback(self):

        if not self.user_defined_frequencies:
            self.hide()
            title = "No solution step was selected"
            message = "Select at least one solution step to proceed "
            message += "with the model solution."
            PrintMessageInput([error_title, title, message])
            return

        self.setup_defined = True
        self.close()

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.add_solution_step_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()