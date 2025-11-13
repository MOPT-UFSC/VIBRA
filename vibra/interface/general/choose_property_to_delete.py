import pprint
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QListWidgetItem, QTableWidgetItem, QTreeWidgetItem, QHeaderView

from vibra import app, __version__
from vibra.interface.ui_generated.general.choose_property_to_delete_ui import ChoosePropertyToDelete_UI


class ChoosePropertytoDelete(ChoosePropertyToDelete_UI):
    def __init__(self, title, message, data: dict[set], *args, **kwargs):
        super().__init__(*args)

        app().main_window.set_input_widget(self)

        self.title = title
        self.message = message
        self.data = data
        self.window_title = kwargs.get('window_title', f'Vibra v{__version__}')

        self._config_window()
        self._initialize()
        self._configure_labels()
        self._configure_buttons()
        self._create_connections()
        self._reset_variables()
        self._configure_table()
        self._mount_properties_list_from_data()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle(self.window_title)
    
    def _initialize(self):
        self.keep_window_open = True
    
    def _create_connections(self):
        self.pushButton_remove.clicked.connect(self.remove_action)
        self.pushButton_cancel.clicked.connect(self.cancel_action)
    
    def _configure_buttons(self):
        self.pushButton_cancel.setText("Cancel")
        self.pushButton_remove.setText("Remove")
    
    def _reset_variables(self):
        self._remove = False
        self._cancel = True
        self._property_to_delete = None

    def _configure_labels(self):
        self.label_title.setText("Remove Property")
        self.label_title.setWordWrap(True)
        self.label_title.setAlignment(Qt.AlignJustify)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setMargin(12)
        self.label_title.adjustSize()
        self.adjustSize()

    def _configure_table(self):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["id", "property", "entity"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode(value=3))

    def _mount_properties_list_from_data(self):
        properties_founded: list[tuple[str, int, str]] = list()

        not_to_remove = ["fluid", "material"]

        properties = app().project.model.properties.point_properties.keys()
        for point_id in self.data.get("points"):
            prop = [(id, prop, "points") for prop, id in properties if (point_id == id and prop not in not_to_remove)]
            properties_founded.extend(prop)
        
        properties = app().project.model.properties.line_properties.keys()
        for line_id in self.data.get("lines"):
            prop = [(id, prop, "lines") for prop, id in properties if (line_id == id and prop not in not_to_remove)]
            properties_founded.extend(prop)
        
        properties = app().project.model.properties.surface_properties.keys()
        for surface_id in self.data.get("surfaces"):
            prop = [(id, prop, "surface") for prop, id in properties if (surface_id == id and prop not in not_to_remove)]
            properties_founded.extend(prop)
        
        self._fill_table(properties_founded)
    
    def _fill_table(self, data: list[tuple[int, str, str]]):
        self.tableWidget.setRowCount(len(data))

        for row_index, line in enumerate(data):
            for column_index, cell_data in enumerate(line):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, column_index, item)

        self.tableWidget.resizeColumnsToContents()

    def actions_to_finalize(self):
        self.update_symbols()

    def remove_action(self):
        self._remove = True
        self._cancel = False
        self.actions_to_finalize()
        self.close()
    
    def cancel_action(self):
        self._remove = False
        self._cancel = True
        self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)