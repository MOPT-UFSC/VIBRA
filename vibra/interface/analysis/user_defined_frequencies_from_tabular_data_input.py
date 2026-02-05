from PySide6.QtWidgets import QCheckBox, QDialog, QHBoxLayout, QHeaderView, QLineEdit, QTableWidgetItem, QWidget
from PySide6.QtGui import Qt

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.ui_generated.analysis.user_defined_frequencies_from_tabular_data_input_ui import UserDefinedFrequenciesFromTabularDataInput_UI

import numpy as np
from copy import deepcopy

error_title = "Error"


class UserDefinedFrequenciesFromTabularDataInput(UserDefinedFrequenciesFromTabularDataInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.analysis_id = kwargs.get("analysis_id")
        if self.analysis_id is None:
            self.analysis_id = app().project.analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

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

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Analysis setup")

    def _create_connections(self):
        #
        self.pushButton_confirm.clicked.connect(self.confirm_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_select_unselect_all.clicked.connect(self.select_unselect_all_callback)

    def select_unselect_all_callback(self):
        select_all = self.pushButton_select_unselect_all.text() == "Select all"
        new_text = "Deselect all" if select_all else "Select all"

        self.pushButton_select_unselect_all.setText(new_text)

        for check_box in self.index_to_check_box.values():
            check_box: QCheckBox
            check_box.setChecked(select_all)

    def load_analysis_setup(self):

        self.index_to_check_box = dict()
        self.analysis_id = app().project.analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

        table_frequencies = app().project.model.properties.process_all_tables_frequencies_vectors()
        self.tableWidget_frequencies.clearContents()
        self.tableWidget_frequencies.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        if len(table_frequencies) != 1:
            return
        
        self.table_frequencies = table_frequencies[0]
        self.tableWidget_frequencies.setRowCount(len(self.table_frequencies))
        self.load_frequency_setup_from_tables(self.table_frequencies)

        for index, freq in enumerate(self.table_frequencies):

            # Creates the QCheckButtons to control data to be plotted
            self.index_to_check_box[index] = QCheckBox()

            checkbox_container = QWidget()
            cointeiner_layout = QHBoxLayout(checkbox_container)
            cointeiner_layout.addStretch()
            cointeiner_layout.addWidget(self.index_to_check_box[index])
            cointeiner_layout.addStretch()
            cointeiner_layout.setContentsMargins(0, 0, 0, 0)

            self.tableWidget_frequencies.setItem(index, 0, QTableWidgetItem(str(index)))
            self.tableWidget_frequencies.setItem(index, 1, QTableWidgetItem(str(freq)))
            self.tableWidget_frequencies.setCellWidget(index, 2, checkbox_container)

            for j in range(2):
                self.tableWidget_frequencies.item(index, j).setTextAlignment(Qt.AlignCenter)

        self.set_enabled_frequencies_checked()

    def load_frequency_setup_from_tables(self, frequencies: list | np.ndarray):

        f_min = frequencies[0]
        f_max = frequencies[-1]
        f_step = frequencies[1] - frequencies[0]

        self.lineEdit_fmin.setDisabled(True)
        self.lineEdit_fmax.setDisabled(True)
        self.lineEdit_fstep.setDisabled(True)

        self.lineEdit_fmin.setText("{}".format(round(f_min, 14)))
        self.lineEdit_fmax.setText("{}".format(round(f_max, 14)))
        self.lineEdit_fstep.setText("{}".format(round(f_step, 14)))

    def set_enabled_frequencies_checked(self):
        if app().project.model.frequencies is None:
            return

        for index, tab_freq in enumerate(self.table_frequencies):
            is_freq_active = tab_freq in app().project.model.frequencies
            self.index_to_check_box[index].setChecked(is_freq_active)

    def confirm_callback(self):
            
        for index, check_box in self.index_to_check_box.items():
            check_box: QCheckBox
            if not check_box.isChecked():
                continue

            self.user_defined_frequencies.append(self.table_frequencies[index])

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
            self.confirm_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()