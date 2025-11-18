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

        self.exec()

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle(self.window_title)
    
    def _initialize(self):
        ...
        # self.keep_window_open = True
    
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
        labels = ["Property", "Entity ID", "Entity"]

        self.tableWidget.setColumnCount(len(labels))
        self.tableWidget.setHorizontalHeaderLabels(labels)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def _mount_properties_list_from_data(self):
        properties_found: list[tuple[str, str, int]] = list()

        def filter_properties_to_not_show(prop: tuple[str, str, int]) -> list[tuple[str, str]]:
            return prop[0] not in ["fluid", "material"]

        prop = app().project.model.properties.get_properties_from_points(self.data.get("points"))
        prop = [(name, id_number, "point") for name, id_number in prop]
        properties_found.extend(prop)

        prop = app().project.model.properties.get_properties_from_lines(self.data.get("lines"))
        prop = [(name, id_number, "line") for name, id_number in prop]
        properties_found.extend(prop)

        prop = app().project.model.properties.get_properties_from_surfaces(self.data.get("surfaces"))
        prop = [(name, id_number, "surface") for name, id_number in prop]
        properties_found.extend(prop)

        prop = app().project.model.properties.get_properties_from_volumes(self.data.get("volumes"))
        prop = [(name, id_number, "volume") for name, id_number in prop]
        properties_found.extend(prop)

        # it is filtered to exclude properties that are not meant to be removed
        properties_found = list(filter(filter_properties_to_not_show, properties_found))
        properties_found.sort(key=lambda item: item[0])

        self._fill_table(properties_found)
    
    def _fill_table(self, data: list[tuple[str, str, int]]):
        self.tableWidget.setRowCount(len(data))

        for row_index, line in enumerate(data):
            for column_index, cell_data in enumerate(line):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, column_index, item)

        self.tableWidget.resizeColumnsToContents()

    def actions_to_finalize(self):
        app().main_window.update_symbols()

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
        # self.keep_window_open = False
        return super().closeEvent(a0)