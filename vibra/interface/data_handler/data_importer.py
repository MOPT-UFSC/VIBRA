from PySide6.QtWidgets import QFileDialog

from vibra import app

from pathlib import Path
import numpy as np
import platform
import os


class DataImporter:

    def __init__(self):
        self.imported_data = dict()

    
    def _import_files(self, multiple_files: bool = False):
        path = app().config.get_last_folder_for("imported_data_folder")
        if path is None:
            folder_path = os.path.expanduser("~")
        else:
            folder_path = path

        kwargs = dict()
        if platform.system() == "Linux":
                kwargs["options"] = QFileDialog.Option.DontUseNativeDialog


        imported_paths, file_extension = None, None
        if (multiple_files):
            imported_paths, file_extension = QFileDialog.getOpenFileNames( None, 
                                                                'Open file', 
                                                                folder_path, 
                                                                'Files (*.csv *.dat *.txt *.xlsx *.xls)',
                                                                **kwargs)
        else:
            imported_paths, file_extension = QFileDialog.getOpenFileName( None, 
                                                                'Open file', 
                                                                folder_path, 
                                                                'Files (*.csv *.dat *.txt *.xlsx *.xls)',
                                                                **kwargs)
        
        position_of_last_imported_file = len(imported_paths) - 1
        
        if not file_extension:
            return

        app().config.write_last_folder_path_in_file("imported_data_folder", imported_paths[position_of_last_imported_file])

        for imported_path in imported_paths:
            self._read_data_in_file(imported_path)
        
        return self.imported_data

    def import_multiple_files(self):
        return self._import_files(True)
    
    def import_single_file(self):
        return self._import_files()
    
    def _read_data_in_file(self, file_path: str):
        from pandas import read_excel
        from openpyxl import load_workbook
        import warnings

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
               
            sufix = Path(file_path).suffix
            filename = os.path.basename(file_path)

            key = len(self.imported_data)
            if sufix in [".txt", ".dat", ".csv"]:
                loaded_data = np.loadtxt(file_path, 
                                        delimiter = ",", 
                                        )
                
                loaded_data = self._remove_unnecesary_header_in_data(loaded_data)
            
                self.imported_data[key] = {  "data" : loaded_data,
                                                "filename" : filename,
                                                "extension" : sufix  }
                
            elif sufix in [".xls", ".xlsx"]:
                wb = load_workbook(file_path)
                sheetnames = wb.sheetnames

                for sheetname in sheetnames:
                    try:
                        sheet_data = read_excel(
                                                file_path, 
                                                sheet_name = sheetname,  
                                                usecols = [0,1,2],
                                                engine="openpyxl"
                                                ).to_numpy()
                    except:
                        sheet_data = read_excel(
                                                file_path, 
                                                sheet_name = sheetname, 
                                                usecols = [0,1],
                                                engine="openpyxl"
                                                ).to_numpy()

                    sheet_data = self._remove_unnecesary_header_in_data(sheet_data)

                    self.imported_data[key] = {  "data" : sheet_data,
                                                    "filename" : filename,
                                                    "sheetname" : sheetname,
                                                    "extension" : sufix  }
                                        
    def _remove_unnecesary_header_in_data(self, data: np.ndarray) -> np.ndarray:
        filtered_data = [row for row in data if not isinstance(row[0], str)]
        return np.array(filtered_data)

