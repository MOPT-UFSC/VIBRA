from PySide6.QtWidgets import QDialog, QFileDialog, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import * 
from PySide6.QtCore import Qt

from vibra import app, UI_DIR
from vibra.interface.general.print_message_input import PrintMessageInput

import os
# import openpyxl
import numpy as np
import platform
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"

class ExportModelResults(QFileDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()

    def _initialize(self):
        self.data = dict()

    def _set_data_to_export(self, data: dict, **kwargs):
        self.data = data
        if data:
            self.call_file_dialog_and_export_data(**kwargs)

    def export_data_in_text_format(self, export_path: str, delimiter: str = ","):

        for data in self.data.values():

            x_data = data["x_data"]
            y_data = data["y_data"]
            unit = data["unit"]
            
            if isinstance(y_data[0], complex):
                header = f"Frequency[Hz], Real part [{unit}], Imaginary part [{unit}], Absolute [{unit}]"
                data_to_export = np.array([x_data, np.real(y_data), np.imag(y_data), np.abs(y_data)]).T      
            else:
                data_type = data["data_type"]
                header = f"Frequency[Hz], {data_type.capitalize()} [{unit}]"
                data_to_export = np.array([x_data, y_data]).T

            np.savetxt(export_path, data_to_export, delimiter=delimiter, header=header)

    def export_data_in_spreadsheet_format(self, export_path: str, **kwargs):

        from openpyxl import load_workbook
        from pandas import ExcelWriter, DataFrame, read_excel

        existing_data_frames = dict()
        existing_path = kwargs.get("existing_path", "")

        if Path(existing_path).exists():
            ext = existing_path.split(".")[-1]
            if ext in ["xls", "xlsx"]:
                wb = load_workbook(existing_path)
                sheetnames = wb.sheetnames

                for sheet_name in sheetnames:
                    existing_data_frames[sheet_name] = read_excel(
                                                                    existing_path, 
                                                                    sheet_name = sheet_name, 
                                                                    header = 0, 
                                                                    usecols = [0,1,2,3]
                                                                    )

        with ExcelWriter(export_path) as writer:

            for key, existing_df in existing_data_frames.items():
                existing_df: DataFrame
                existing_df.to_excel(writer, sheet_name=key, index=False)

            count = 0
            for key, data in self.data.items():

                if len(key) == 2:
                    if key[1] is None:
                        sheet_name = f"{key[0]}"
                    else:
                        selection_type, selection_id = key
                        sheet_name = f"{selection_type}_{selection_id}"
                else:
                    count += 1
                    sheet_name = f"sheet_{count}"

                x_data = data["x_data"]
                y_data = data["y_data"]
                unit = data["unit"]

                if isinstance(y_data[0], complex):
                    header = ["Frequency[Hz]", f"Real part [{unit}]", f"Imaginary part [{unit}]", f"Absolute [{unit}]"]
                    data_to_export = np.array([x_data, np.real(y_data), np.imag(y_data), np.abs(y_data)]).T 
                else:
                    data_type = data["data_type"]
                    header = ["Frequency[Hz]", f"{data_type.capitalize()} [{unit}]"]
                    data_to_export = np.array([x_data, y_data]).T

                df = DataFrame(data_to_export, columns=header)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def call_file_dialog_and_export_data(self, **kwargs):

        existing_path = kwargs.get("existing_path", "")

        if existing_path == "":

            caption = "Export the model results"

            path = app().config.get_last_folder_for("exported_data_folder")
            if path is None:
                directory_path = os.path.expanduser("~")
            else:
                directory_path = path

            if len(self.data) == 1:
                _filter = "Text file (*.csv);; Spreadsheet (*.xlsx);; Text file (*.dat);;Text file (*.txt)"
            else:
                _filter = "Spreadsheet (*.xlsx)"

            kwargs = dict()
            if platform.system() == "Linux":
                kwargs["options"] = QFileDialog.Option.DontUseNativeDialog
            file_path, file_extension = self.getSaveFileName(app().main_window, 
                                                    caption, 
                                                    directory_path, 
                                                    filter = _filter,
                                                    **kwargs)
            
            if not file_extension:
                return

        else:
            file_path = existing_path

        app().config.write_last_folder_path_in_file("exported_data_folder", file_path)

        ext = file_path.split(".")[-1]      
        if ext in ["xls", "xlsx"]:
            self.export_data_in_spreadsheet_format(file_path, existing_path=existing_path)
        else:
            self.export_data_in_text_format(file_path)

        # self.print_final_message()

    def print_final_message(self):
        title = "Information"
        message = "The results have been exported."
        PrintMessageInput([window_title_2, title, message], auto_close=True)