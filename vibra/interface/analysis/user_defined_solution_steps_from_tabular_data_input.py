from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QHeaderView, QTableWidgetItem, QWidget
from PySide6.QtGui import Qt, QIcon

from vibra import app, ICON_DIR
from vibra.interface import error_title
from vibra.interface.formatters.icons import change_icon_color
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.ui_generated.analysis.user_defined_solution_steps_from_tabular_data_input_ui import UserDefinedSolutionStepsFromTabularDataInput_UI

import numpy as np


class UserDefinedSolutionStepsFromTabularDataInput(UserDefinedSolutionStepsFromTabularDataInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        # app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self._paint_icons()

        self._create_connections()
        self._load_analysis_setup()

        self.pushButton_select_unselect_all.setIcon(self.unselect_icon)

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.setup_defined = False
        self.solve_analysis = False
        self.keep_window_open = True
        self.index_to_check_box = dict()
        self.user_defined_solution_steps = list()

        self.select_all_icon = QIcon(str(ICON_DIR / "select_all_icon.png"))
        self.unselect_icon = QIcon(str(ICON_DIR / "deselect_icon.png"))

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Analysis setup")

    def _create_connections(self):
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_okay.clicked.connect(self.confirm_callback)
        self.pushButton_select_unselect_all.clicked.connect(self.select_unselect_all_callback)
        #
        app().main_window.theme_changed.connect(self._paint_icons)

    def _paint_icons(self):
        icon_color = None
        theme = app().config.user_preferences.interface_theme

        from vibra import LIGHT_ICON_COLOR, DARK_ICON_COLOR
        if theme == "dark":
            icon_color = DARK_ICON_COLOR.to_qt()
        else:
            icon_color = LIGHT_ICON_COLOR.to_qt()

        change_icon_color(self.select_all_icon, icon_color)
        change_icon_color(self.unselect_icon, icon_color)

    def select_unselect_all_callback(self):
        select_all = self.pushButton_select_unselect_all.text() == "Select all"
        new_text = "Deselect all" if select_all else "Select all"
        icon = self.unselect_icon if select_all else self.select_all_icon

        self.pushButton_select_unselect_all.setText(new_text)
        self.pushButton_select_unselect_all.setIcon(icon)

        for check_box in self.index_to_check_box.values():
            check_box: QCheckBox
            check_box.setChecked(select_all)

    def _load_analysis_setup(self):

        self.index_to_check_box.clear()

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
            check_box = QCheckBox()
            check_box.setStyleSheet("QCheckBox::indicator { width: 18px; height: 18px; }")
            self.index_to_check_box[index] = check_box

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

        solution_steps_mask = app().project.model.solution_steps_mask

        for index, _bool in enumerate(solution_steps_mask):
            step_check_box = self.index_to_check_box[index]
            step_check_box: QCheckBox
            step_check_box.setChecked(_bool)

    def deactivate_solution_step_by_key_event(self):
        selected_items = self.tableWidget_frequencies.selectedItems()
        for item in selected_items:
            str_index = self.tableWidget_frequencies.item(item.row(), 0).text()
            if str_index == "":
                continue

            index = int(str_index)
            self.index_to_check_box[index].setChecked(False)

    def confirm_callback(self):
            
        for index, check_box in self.index_to_check_box.items():

            check_box: QCheckBox
            if not check_box.isChecked():
                continue

            self.user_defined_solution_steps.append(self.table_frequencies[index])

        if len(self.user_defined_solution_steps) == 0:
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
        elif event.key() == Qt.Key_Delete:
            self.deactivate_solution_step_by_key_event()
        elif event.key() == Qt.Key_Escape:
            self.close()