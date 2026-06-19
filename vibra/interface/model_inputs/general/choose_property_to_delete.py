from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem

from vibra import app
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.ui_generated.model.general.choose_property_to_delete_ui import ChoosePropertyToDelete_UI


class ChoosePropertyToDelete(ChoosePropertyToDelete_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        app().main_window.set_input_widget(self)

        self._initialize()
        self._configure_table()
        self._load_properties_data_and_update_table()

        if not self.properties_formated:
            return

        if len(self.properties_formated) == 1:
            self.tableWidget.selectAll()
            self.remove_callback()

        self._config_window()
        self._create_connections()
        self._configure_filter_timer()
        self._configure_lineEdit()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.keep_window_open = True
        self.properties_formated: list[dict[str, str]] = list()

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowTitle("Vibra")

    def _create_connections(self):
        self.lineEdit_filter.textChanged.connect(self._start_timer)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_cancel.clicked.connect(self.close)

    def _configure_lineEdit(self):
        self.lineEdit_filter.setPlaceholderText("Filter properties by name, entity type, or ID...")

        style = """
        QLineEdit::placeholder {
            color: #cccccc;
            font-style: italic;
        }
        """
        self.lineEdit_filter.setStyleSheet(style)
        self.lineEdit_filter.setFocus()

    def _configure_table(self):
        # table will always have 3 collumns
        labels = ["Entity ID", "Entity", "Property name"]

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.tableWidget.setColumnCount(len(labels))
        self.tableWidget.setHorizontalHeaderLabels(labels)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        # self.tableWidget.resizeColumnsToContents()

        for i, width in enumerate([100, 100]):
            self.tableWidget.setColumnWidth(i, width)

        self.tableWidget.horizontalHeader().setStretchLastSection(True)

    def _configure_filter_timer(self):
        self.filter_timer = QTimer()
        self.filter_timer.setInterval(100)
        self.filter_timer.setSingleShot(True)
        self.filter_timer.timeout.connect(self.filter_table)

    def _start_timer(self):
        self.filter_timer.start()

    def _load_properties_data_and_update_table(self):

        self.tableWidget.clearContents()
        self.properties_formated.clear()

        selected_entities = {
            "points": app().main_window.selection.geometry_points,
            "lines": app().main_window.selection.geometry_lines,
            "surfaces": app().main_window.selection.geometry_surfaces,
            "volumes": app().main_window.selection.geometry_volumes,
        }

        prop = app().project.model.properties.get_properties_from_points(selected_entities.get("points"))
        prop = [{"id": str(id_number), "entity": "point", "name": name} for name, id_number in prop]
        self.properties_formated.extend(prop)

        prop = app().project.model.properties.get_properties_from_lines(selected_entities.get("lines"))
        prop = [{"id": str(id_number), "entity": "line", "name": name} for name, id_number in prop]
        self.properties_formated.extend(prop)

        prop = app().project.model.properties.get_properties_from_surfaces(selected_entities.get("surfaces"))
        prop = [{"id": str(id_number), "entity": "surface", "name": name} for name, id_number in prop]
        self.properties_formated.extend(prop)

        prop = app().project.model.properties.get_properties_from_volumes(selected_entities.get("volumes"))
        prop = [{"id": str(id_number), "entity": "volume", "name": name} for name, id_number in prop]
        self.properties_formated.extend(prop)

        # filters the property list, removing fields
        def filter_properties_to_not_show(prop: dict[str, str]) -> bool:
            return prop.get("name") not in ["fluid", "material", "degrees_of_freedom_decoupling", "perforated_plate_model", "transfer_impedance"]

        def filter_physical_domain_properties(prop: dict[str, str]) -> bool:
            current_physical_domain = app().main_window.analysis_toolbar.combo_box_physical_domain.currentText().lower()
            prop_physical_domain = app().project.model.properties.get_data_group_label(prop.get("name", ""))
            return prop_physical_domain == current_physical_domain

        self.properties_formated = list(filter(filter_properties_to_not_show, self.properties_formated))
        self.properties_formated = list(filter(filter_physical_domain_properties, self.properties_formated))
        self.properties_formated.sort(key=lambda item: item.get("name", ""))

        self._fill_table(self.properties_formated)

    def _fill_table(self, properties_list: list[dict[str, str]]):
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setRowCount(len(properties_list))

        for row_index, line in enumerate(properties_list):
            for column_index, cell_data in enumerate(line.values()):
                item = None
                if cell_data.isnumeric():
                    item = QTableWidgetItem()
                    item.setData(Qt.ItemDataRole.DisplayRole, int(cell_data))
                else:
                    item = QTableWidgetItem(str(cell_data).replace("_", " ").capitalize())

                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(row_index, column_index, item)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.selectAll()

    def filter_table(self):
        filter_text = self.lineEdit_filter.text().lower().replace(" ", "_")

        def filter_properties_formated(prop: dict[str, str]) -> bool:
            return filter_text in prop.get("name", "") or filter_text in prop.get("entity", "") or filter_text == prop.get("id", "")

        properties_filtered = list(filter(filter_properties_formated, self.properties_formated))
        self._fill_table(properties_filtered)

    def _get_user_confirmation(self, properties_count: int) -> bool:

        if properties_count > 1:
            text = "properties"
        else:
            text = "property"

        title = f"Remove selected {text}"
        message = f"Would you like to remove the selected {text} from the model?"

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Remove",
            "right_toolTip": "Remove selected items",
        }

        self.hide()
        read = GetUserConfirmationInput(
            title, message, buttons_config=buttons_config, window_title="Vibra"
        )

        return read._continue

    def remove_callback(self):
        # starts from index 0
        rows_selected: list[int] = list()
        for sr in self.tableWidget.selectedRanges():
            rows_selected.extend(range(sr.topRow(), sr.bottomRow() + 1))

        properties_count: int = len(rows_selected)
        if properties_count == 0:
            self.hide()
            title = "No property selected"
            message = "Please select at least one property."
            PrintMessageInput(["Error", title, message])
            return

        user_accept = self._get_user_confirmation(properties_count)
        if not user_accept:
            return

        for row in rows_selected:
            entity_id_table_item = self.tableWidget.item(row, 0)
            entity_name_table_item = self.tableWidget.item(row, 1)
            property_selected_table_item = self.tableWidget.item(row, 2)

            if (
                property_selected_table_item is None
                or entity_name_table_item is None
                or entity_id_table_item is None
            ):
                continue

            property_selected = property_selected_table_item.text().lower().replace(" ", "_")
            entity_name = entity_name_table_item.text().lower()
            entity_id = int(entity_id_table_item.text())

            if entity_name == "point":
                app().project.model.properties.remove_table_files_from_point(entity_id, property_selected)
                app().project.model.properties._remove_point_property(property_selected, entity_id)

            elif entity_name == "line":
                app().project.model.properties.remove_table_files_from_line(entity_id, property_selected)
                app().project.model.properties._remove_line_property(property_selected, entity_id)

            elif entity_name == "surface":
                app().project.model.properties.remove_table_files_from_surface(entity_id, property_selected)
                app().project.model.properties._remove_surface_property(property_selected, entity_id)

            elif entity_name == "volume":
                app().project.model.properties.remove_table_files_from_volume(entity_id, property_selected)
                app().project.model.properties._remove_volume_property(property_selected, entity_id)

        self._load_properties_data_and_update_table()
        self.actions_to_finalize()

    def actions_to_finalize(self):
        app().main_window.update_info_text()
        app().project.update_model_properties_file()
        app().main_window.update_symbols()

        if not self.properties_formated:
            self.close()

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Delete]:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        return

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)
