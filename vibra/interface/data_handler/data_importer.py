from PySide6.QtWidgets import QFileDialog

from vibra import app
from vibra.interface.data_handler.imported_data import ImportedData

from typing import List
from pathlib import Path
import numpy as np
import platform
import os


class DataImporter:
  
    @staticmethod
    def __import_files(caption: str, last_folder: str, file_extensions: List[str], multiple_files: bool = False):
        path = app().config.get_last_folder_for(last_folder)
        if path is None:
            folder_path = os.path.expanduser("~")
        else:
            folder_path = path

        kwargs = dict()
        if platform.system() == "Linux":
                kwargs["options"] = QFileDialog.Option.DontUseNativeDialog

        str_extensions = "Files ("
        for extension in file_extensions:
            str_extensions += "*."
            str_extensions += extension
            str_extensions += " "
        
        str_extensions = str_extensions.strip()
        str_extensions += ")"

        imported_paths, file_extension = None, None
        if (multiple_files):
            imported_paths, file_extension = QFileDialog.getOpenFileNames( None, 
                                                                caption, 
                                                                folder_path, 
                                                                str_extensions,
                                                                **kwargs)
        else:
            imported_paths, file_extension = QFileDialog.getOpenFileName( None, 
                                                                caption, 
                                                                folder_path, 
                                                                str_extensions,
                                                                **kwargs)
        
        if not file_extension:
            return
        
        last_imported_file = imported_paths
        position_of_last_imported_file = len(imported_paths) - 1
        if isinstance(imported_paths, list):
            last_imported_file = imported_paths[position_of_last_imported_file]
        

        app().config.write_last_folder_path_in_file(last_folder, last_imported_file)

        imported_data = list()
        for imported_path in imported_paths:
            imported_data.append(DataImporter.__read_data_in_file(imported_path))
        
        return imported_data

    @staticmethod
    def import_multiple_files(last_folder: str, file_extensions: List[str], caption: str = "Open file") -> List[ImportedData]:
        return DataImporter.__import_files(caption, last_folder, file_extensions, True)
    
    @staticmethod
    def import_single_file(last_folder: str, file_extensions: List[str], caption: str = "Open File") -> ImportedData:
        return DataImporter.__import_files(caption, last_folder, file_extensions)[0]
    
    @staticmethod
    def __read_data_in_file(file_path: str):
        from pandas import read_excel
        from openpyxl import load_workbook
        import warnings

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
               
            sufix = Path(file_path).suffix
            filename = os.path.basename(file_path)

            if sufix in [".txt", ".dat", ".csv"]:
                loaded_data = np.loadtxt(file_path, 
                                        delimiter = ",", 
                                        )
                
                loaded_data = DataImporter._remove_unnecesary_header_in_data(loaded_data)

                return ImportedData(loaded_data, filename, sufix)
                
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

                    sheet_data = DataImporter.__remove_unnecesary_header_in_data(sheet_data)

                    return ImportedData(sheet_data, filename, sufix, sheetname)

    @staticmethod                      
    def __remove_unnecesary_header_in_data(data: np.ndarray) -> np.ndarray:
        filtered_data = [row for row in data if not isinstance(row[0], str)]
        return np.array(filtered_data)

