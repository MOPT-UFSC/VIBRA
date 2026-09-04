from dataclasses import asdict
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QTreeWidgetItem, QWidget

from vibra import app
from vibra.extensions import SUPPORTED_SPREADSHEET_EXTENSIONS, SUPPORTED_TEXT_EXTENSIONS
from vibra.interface.ui_generated.data_handler.import_data_to_compare_ui import (
    ImportDataToCompare_UI,
)
from vibra.interface.user_input.data_handler.file_dialog_service import FileDialogService
from vibra.interface.user_input.data_handler.file_handlers.file_handler import FileHandler
from vibra.interface.user_input.data_handler.imported_data import ImportedData, SpreadsheetData, TextData

if TYPE_CHECKING:
    from vibra.interface.plots.general.frequency_response_plotter import (
        FrequencyResponsePlotter,
    )

import numpy as np


class ImportDataToCompare(ImportDataToCompare_UI):
    def __init__(self, plotter: "FrequencyResponsePlotter", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plotter = plotter

        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._create_connections()
        self._config_widgets()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")
        self.lineEdit_import_results_path.setDisabled(True)

    def _initialize(self):
        self.keep_window_open = True

        self.imported_data = None
        self.imported_results = dict()
        self.ids_to_checkBox = dict()
        self.checkButtons_state = dict()

        self.colors = ([0, 0, 0], [1, 0, 0], [1, 0, 1], [0, 1, 1], [0.75, 0.75, 0.75], [0.5, 0.5, 0.5], [0.25, 0.25, 0.25])

    def _create_connections(self):
        #
        self.pushButton_add_imported_data_to_plot.clicked.connect(self.add_imported_data_to_plot)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_reset_imported_data.clicked.connect(self.reset_imported_data)
        self.pushButton_search_file_to_import.clicked.connect(self.import_results)

    def _config_widgets(self):
        for i, width in enumerate([320, 60]):
            self.treeWidget_import_text_files.setColumnWidth(i, width)

        for i, width in enumerate([180, 180, 60]):
            self.treeWidget_import_sheet_files.setColumnWidth(i, width)

    def import_results(self):
        extensions = SUPPORTED_SPREADSHEET_EXTENSIONS + SUPPORTED_TEXT_EXTENSIONS

        imported_files = FileDialogService.open_multiple_files(file_extensions=extensions,
                                              last_folder="imported_data_folder")

        if imported_files is None:
            return

        self.imported_data = FileHandler.read(imported_files)
        
        self.organize_imported_results_according_to_file_type(self.imported_data)
        self.update_treeWidget_info()

    def organize_imported_results_according_to_file_type(self, imported_files: list[ImportedData]):
        for file in imported_files:
            key = len(self.imported_results)

            if isinstance(file, TextData):
                self.imported_results[key] = asdict(file)
                
            elif isinstance(file, SpreadsheetData):
                for sheet in file.sheets:
                    self.imported_results[key] = {key: value for key, value in asdict(file) if key != "sheets"} | asdict(sheet)
                    key = len(self.imported_results)

    def update_treeWidget_info(self):
        self.cache_checkButtons_state()
        self.treeWidget_import_text_files.clear()
        self.treeWidget_import_sheet_files.clear()
        #
        if len(self.imported_results) > 0:
            for i, (id, data) in enumerate(self.imported_results.items()):
                # Creates the QCheckButtons to control data to be plotted
                self.ids_to_checkBox[id] = QCheckBox()

                checkbox_container = QWidget()
                cointeiner_layout = QHBoxLayout(checkbox_container)
                cointeiner_layout.addStretch()
                cointeiner_layout.addWidget(self.ids_to_checkBox[id])
                cointeiner_layout.addStretch()
                cointeiner_layout.setContentsMargins(0, 0, 0, 0)

                if id in self.checkButtons_state.keys():
                    self.ids_to_checkBox[id].setChecked(self.checkButtons_state[id])

                if "sheetname" in data.keys():
                    _item = QTreeWidgetItem([str(data["filename"]), str(data["sheetname"])])
                    self.treeWidget_import_sheet_files.addTopLevelItem(_item)
                    self.treeWidget_import_sheet_files.setItemWidget(_item, 2, checkbox_container)

                    _item.setTextAlignment(2, Qt.AlignCenter)
                else:
                    _item = QTreeWidgetItem([str(data["filename"])])
                    self.treeWidget_import_text_files.addTopLevelItem(_item)
                    self.treeWidget_import_text_files.setItemWidget(_item, 1, checkbox_container)

                for i in range(5):
                    _item.setTextAlignment(i, Qt.AlignCenter)

    def join_imported_data(self):
        j = 0
        imported_results_data = dict()
        for id, checkBox in self.ids_to_checkBox.items():
            checkBox: QCheckBox

            if checkBox.isChecked():
                if len(imported_results_data) <= len(self.colors):
                    color = self.colors[j]
                    j += 1
                else:
                    color = np.random.randint(0, 255, 3) / 255

                data = self.imported_results[id]["data"]
                x_values = data[:, 0]

                if data.shape[1] == 2:
                    y_values = data[:, 1]
                else:
                    y_values = data[:, 1] + 1j * data[:, 2]

                if "sheetname" in self.imported_results[id].keys():
                    sheetname = self.imported_results[id]["sheetname"]
                    legend_label = f"{sheetname}"
                else:
                    legend_label = self.imported_results[id]["filename"]

                y_label = self.plotter.y_label.replace(" [dB]", "").split(" - ")[0]

                key = id
                imported_results_data[key] = {
                    "type": "imported_data",
                    "x_data": x_values,
                    "y_data": y_values,
                    "x_label": "Frequency [Hz]",
                    "y_label": y_label,
                    "legend": legend_label,
                    "unit": "",
                    "title": "",
                    "color": color,
                    "linestyle": "--",
                }

        self.plotter._set_imported_results_data_to_plot(imported_results_data)

    def cache_checkButtons_state(self):
        self.checkButtons_state = dict()
        for key, check in self.ids_to_checkBox.items():
            self.checkButtons_state[key] = check.isChecked()

    def reset_imported_data(self):
        self.lineEdit_import_results_path.setText("")
        self.treeWidget_import_sheet_files.clear()
        self.treeWidget_import_text_files.clear()
        self._initialize()
        self.plotter.reset_imported_results_data_to_plot()

    def add_imported_data_to_plot(self):
        self.join_imported_data()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.add_imported_data_to_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        # if self.exporter is not None:
        #     self.exporter.close()

        # if self.importer is not None:
        #     self.importer.close()

        self.keep_window_open = False
        return super().closeEvent(a0)
