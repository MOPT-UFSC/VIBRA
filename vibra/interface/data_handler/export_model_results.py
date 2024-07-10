from PyQt5.QtWidgets import QDialog, QFileDialog, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.interface.general.print_message_input import PrintMessageInput

import os
import openpyxl
import numpy as np
import pandas as pd

window_title1 = "Error"
window_title2 = "Warning"

class ExportModelResults(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "data_handler/export_model_results.ui"
        uic.loadUi(ui_path, self)

        self._load_icons()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()

    def _load_icons(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Export model results")

    def _reset_variables(self):
        self.user_path = os.path.expanduser('~')
        self.save_path = ""
        self.data = dict()

    def _define_qt_variables(self):

        # QLabel
        self.label_data_information : QLabel

        # QLineEdit
        self.lineEdit_file_name : QLineEdit
        self.lineEdit_save_results_path : QLineEdit

        # QPushButton
        self.pushButton_choose_folder_export : QPushButton
        self.pushButton_export_results : QPushButton

    def _create_connections(self):
        self.pushButton_choose_folder_export.clicked.connect(self._choose_path_export_results)
        self.pushButton_export_results.clicked.connect(self._export_results)

    def _set_data_to_export(self, data):
        self.data = data
        if data:
            self._load_data_information()
            self.exec()

    def _load_data_information(self):

        if len(self.data) == 1:
            for key, data in self.data.items():
                if "data_information" in data.keys():
                    text = "Data information: "
                    text += data["data_information"]
        else:
            text = "Multiple selection"

        self.label_data_information.setText(text)
        self.lineEdit_file_name.setFocus()

    def _choose_path_export_results(self):

        if self.save_path == "":
            _path = self.user_path
        else:
            _path = self.save_path

        self.save_path = QFileDialog.getExistingDirectory(None, 'Choose a folder to export the results', _path)
        self.save_name = os.path.basename(self.save_path)
        self.lineEdit_save_results_path.setText(str(self.save_path))

    def _export_results(self):
        
        if self.lineEdit_file_name.text() != "":
            if self.save_path == "":
                title = "None folder selected"
                message = "Plese, choose a folder before trying export the results."
                PrintMessageInput([window_title1, title, message])
                return
        else:
            title = "Empty file name"
            message = "Inform a file name before trying export the results."
            PrintMessageInput([window_title1, title, message])
            return

        format_index = 1

        if format_index == 0:
            self.export_data_in_text_format()

        elif format_index == 1:
            self.export_data_in_spreadsheet_format()

        self.close()
        title = "Information"
        message = "The results have been exported."
        PrintMessageInput([window_title2, title, message], auto_close=True)

    def export_data_in_text_format(self, delimiter=","):

        for key, data in self.data.items():
            
            selection_type, selection_id = key
            suffix = f"{selection_type}_{selection_id}"

            file_name = self.lineEdit_file_name.text() + suffix + ".dat"
            export_path = os.path.join(self.save_path, file_name)
            
            x_data = data["x_data"]
            y_data = data["y_data"]
            unit = data["unit"]
            
            header = f"Frequency[Hz], Real part [{unit}], Imaginary part [{unit}], Absolute [{unit}]"
            data_to_export = np.array([x_data, np.real(y_data), np.imag(y_data), np.abs(y_data)]).T      
    
            np.savetxt(export_path, data_to_export, delimiter=delimiter, header=header)

    def export_data_in_spreadsheet_format(self):

        file_name = self.lineEdit_file_name.text() + ".xlsx"
        export_path = os.path.join(self.save_path, file_name)

        with pd.ExcelWriter(export_path) as writer:

            for key, data in self.data.items():

                selection_type, selection_id = key
                sheet_name = f"{selection_type}_{selection_id}"

                x_data = data["x_data"]
                y_data = data["y_data"]
                unit = data["unit"]

                if isinstance(y_data[0], complex):
                    header = ["Frequency[Hz]", f"Real part [{unit}]", f"Imaginary part [{unit}]", f"Absolute [{unit}]"]
                    data_to_export = np.array([x_data, np.real(y_data), np.imag(y_data), np.abs(y_data)]).T 
                else:
                    header = ["Frequency[Hz]", f"Values [{unit}]"]
                    data_to_export = [x_data, y_data]

                df = pd.DataFrame(data_to_export, columns=header)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self._export_results()
        elif event.key() == Qt.Key_Escape:
            self.close()