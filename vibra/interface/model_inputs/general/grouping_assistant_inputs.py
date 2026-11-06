
from enum import IntEnum

from PySide6.QtCore import QSignalBlocker, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QTreeWidgetItem

from vibra import app
from vibra.engine.model_domains_processor import GroupData
from vibra.interface import error_title
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.acoustic.definitions.enums import SetupTabType
from vibra.interface.numeric_checks.int_list_validator import IntListValidator
from vibra.interface.ui_generated.model.general.grouping_assistant_inputs_ui import GroupingAssistantInputs_UI


class SelectionMode(IntEnum):
    MANUAL = 0
    SELECT_ALL = 1
    SELECT_BY_SIDE = 2


class SelectionFilter(IntEnum):
    VOLUMES = 0
    SURFACES = 1
    LINES = 2


class DomainFilter(IntEnum):
    NONE = 0
    ACOUSTIC = 1
    STRUCTURAL = 2


class GroupingAssistantInputs(GroupingAssistantInputs_UI):
    def __init__(self, selector_mode: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()
        
        self._config_window()
        self._initialize()
        self._configure_widgets()
        self._create_connections()
        self._configure_validators()
        self.load_model_info()

        if selector_mode:
            self.change_to_selector_mode()
            return

        while self.keep_window_open:
            self.exec()

    @property
    def model(self):
        return app().project.model

    @property
    def mesh(self):
        return app().project.model.mesh

    @property
    def properties(self):
        return app().project.model.properties

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.imported_values = None
        self.keep_window_open = True
        self.last_tab = self.tabWidget_main.currentIndex()

    def _configure_widgets(self):

        self.lineEdit_selected_ids.setDisabled(True)
        self.pushButton_select.setDisabled(True)
        self.treeWidget_group_info.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        for i, w in enumerate([60, 120, 120, 180]):
            self.treeWidget_group_info.setColumnWidth(i, w)
            self.treeWidget_group_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _configure_validators(self):
        self.lineEdit_selected_ids.setValidator(IntListValidator())

    def _create_connections(self):

        # QComboBox connection
        self.comboBox_domain_filter.currentIndexChanged.connect(self.domain_filter_callback)
        self.comboBox_selector_filter.currentIndexChanged.connect(self.selection_filter_callback)
        self.comboBox_mode.currentIndexChanged.connect(self.selection_mode_callback)

        # QPushButton connections
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_select.clicked.connect(self.select_entities_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)

        # QTabWidget connection
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)

        # QTreeWidget connections
        self.treeWidget_group_info.itemClicked.connect(self.item_clicked_callback)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

        self.geometry_selection_callback()

    def geometry_selection_callback(self):

        volumes = app().main_window.selection.geometry_volumes
        surfaces = app().main_window.selection.geometry_surfaces
        lines = app().main_window.selection.geometry_lines

        if len(volumes) + len(surfaces) + len(lines) == 0:
            self.lineEdit_selected_ids.clear()
            return

        selection_filter = self.comboBox_selector_filter.currentIndex()

        def update_text_ids(entity_label: str, entities_ids: set[int]):
            text = ", ".join([str(i) for i in entities_ids])
            self.lineEdit_selected_ids.setText(text)
            self.label_selected_ids.setText(f"{entity_label.capitalize()} IDs:")

        if volumes and selection_filter == SelectionFilter.VOLUMES:
            update_text_ids("volume", volumes)

        elif surfaces and selection_filter == SelectionFilter.SURFACES:
            update_text_ids("surface", surfaces)

        elif lines and selection_filter == SelectionFilter.LINES:
            update_text_ids("line", lines)

    def domain_filter_callback(self):
        pass

    def selection_filter_callback(self):
        pass

    def selection_mode_callback(self):
        selection_mode = self.comboBox_mode.currentIndex()
        manual_selection = selection_mode == SelectionMode.MANUAL 
        self.pushButton_select.setDisabled(manual_selection)

    def select_entities_callback(self):
        selection_mode = self.comboBox_mode.currentIndex()
        match selection_mode:
            case  SelectionMode.MANUAL:
                self.manual_selection_callback()
            case  SelectionMode.SELECT_ALL:
                self.select_all_callback()
            case SelectionMode.SELECT_BY_SIDE:
                self.select_by_size_callback()
            case _:
                pass


    def manual_selection_callback(self):
        pass

    def select_by_size_callback(self):

        selected_volumes = []
        for volume in app().main_window.selection.geometry_volumes:
            for vol_id in self.model.model_selection_tools.select_volumes_by_size(volume):
                if vol_id in selected_volumes:
                    continue
                selected_volumes.append(vol_id)

        if selected_volumes:
            app().main_window.selection.set_geometry_selection(volumes=selected_volumes)
            with QSignalBlocker(self.comboBox_selector_filter):
                self.comboBox_selector_filter.setCurrentIndex(SelectionFilter.VOLUMES)

        selected_surfaces = []
        for surface in app().main_window.selection.geometry_surfaces:
            for surf_id in self.model.model_selection_tools.select_surfaces_by_size(surface):
                if surf_id in selected_surfaces:
                    continue
                selected_surfaces.append(surf_id)

        if selected_surfaces:
            app().main_window.selection.set_geometry_selection(surfaces=selected_surfaces)
            with QSignalBlocker(self.comboBox_selector_filter):
                self.comboBox_selector_filter.setCurrentIndex(SelectionFilter.SURFACES)

        selected_lines = []
        for line in app().main_window.selection.geometry_lines:
            for line_id in self.model.model_selection_tools.select_lines_by_size(line):
                if line_id in selected_lines:
                    continue
                selected_lines.append(line_id)

        if selected_lines:
            app().main_window.selection.set_geometry_selection(lines=selected_lines)
            with QSignalBlocker(self.comboBox_selector_filter):
                self.comboBox_selector_filter.setCurrentIndex(SelectionFilter.LINES)

    def select_all_callback(self):
        selection_filter = self.comboBox_selector_filter.currentIndex()
        domain_filter = self.comboBox_domain_filter.currentIndex()

        if selection_filter == SelectionFilter.VOLUMES:    
            if domain_filter == DomainFilter.NONE:
                all_volumes = self.model.mesh.all_volume_ids()
            elif domain_filter == DomainFilter.ACOUSTIC:
                all_volumes = self.model.model_selection_tools.all_acoustic_domains
            else:
                all_volumes = self.model.model_selection_tools.all_structural_domains
            
            if not all_volumes:
                return

            app().main_window.selection.set_geometry_selection(volumes=all_volumes)

        if selection_filter == SelectionFilter.SURFACES:    
            if domain_filter == DomainFilter.NONE:
                all_surfaces = self.model.mesh.all_surface_ids()
            elif domain_filter == DomainFilter.ACOUSTIC:
                all_surfaces = self.model.model_selection_tools.all_acoustic_surfaces
            else:
                all_surfaces = self.model.model_selection_tools.all_structural_surfaces
            
            if not all_surfaces:
                return

            app().main_window.selection.set_geometry_selection(surfaces=all_surfaces)

        if selection_filter == SelectionFilter.LINES:
            if domain_filter == DomainFilter.NONE:
                all_lines = self.model.mesh.all_line_ids()
            elif domain_filter == DomainFilter.ACOUSTIC:
                all_lines = self.model.model_selection_tools.all_acoustic_lines
            else:
                all_lines = self.model.model_selection_tools.all_structural_lines
            
            if not all_lines:
                return

            app().main_window.selection.set_geometry_selection(lines=all_lines)

    def get_new_group_id(self) -> int:

        used_ids = []
        for property, _id in self.properties.group_properties:
            if property != "selection_group":
                continue

            used_ids.append(_id)

        for new_id in range(1, 10001):
            if new_id in used_ids:
                continue

            return new_id

    def is_group_label_valid(self, group_label: str):
        for (property, _), data in self.properties.group_properties.items():
            if property != "selection_group":
                continue

            if not isinstance(data, dict):
                continue

            if group_label == data.get("group_label"):
                return False

        return True

    def apply_callback(self, close_window: bool = False):

        group_label = self.lineEdit_group_label.text()
        if group_label == "":
            title = "Invalid group label"
            message = "Enter a valid group label to proceed with creating the group selection."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_group_label.setFocus()
            return

        if not self.is_group_label_valid(group_label):
            title = "Invalid group label"
            message = f"The group label '{group_label}' already exists. Please, enter a different "
            message += "valid group label to proceed with creating the group selection."
            PrintMessageInput([error_title, title, message])
            self.lineEdit_group_label.setFocus()
            self.lineEdit_group_label.selectAll()
            return

        group_id = self.get_new_group_id()
        entity_type = self.comboBox_selector_filter.currentText()
        entities_id = [int(text) for text in self.lineEdit_selected_ids.text().replace(" ", "").split(",")]

        data = GroupData(group_label, entity_type, entities_id)
        self.properties._set_property("selection_group", data.as_dict(), group=group_id)

        self.lineEdit_group_label.clear()
        self.lineEdit_selected_ids.clear()

        self.actions_to_finalize(close_window)

    def load_model_info(self):
        self.treeWidget_group_info.clear()

        for (property, group_id), data in self.properties.group_properties.items():
            if property != "selection_group":
                continue

            if not isinstance(data, dict):
                continue

            group_label = data.get("group_label")
            entity_type = data.get("entity_type")
            entities_id = ", ".join([str(i) for i in data.get("entities_id")])

            item = QTreeWidgetItem([str(group_id), group_label, entity_type, entities_id])

            for i in range(4):
                item.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_group_info.addTopLevelItem(item)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        for property, _ in self.properties.group_properties:
            if property != "selection_group":
                continue

            self.tabWidget_main.setTabVisible(SetupTabType.LIST, True)
            return
 
        self.tabWidget_main.setTabVisible(SetupTabType.LIST, False)

    def remove_callback(self):

        selected_items = self.treeWidget_group_info.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            group_id = int(item.text(0))
            self.properties._remove_group_property("selection_group", group_id)

        self.pushButton_remove.setDisabled(True)

        app().main_window.selection.clear_selection()
        self.actions_to_finalize()

    def reset_callback(self):

        title = "Selection groups reset"
        message = "Would you like to remove all created selection groups from the model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            self.properties._reset_property("selection_group")
            self.actions_to_finalize()

    def item_clicked_callback(self):
        self.pushButton_remove.setEnabled(True)
        selected_items = self.treeWidget_group_info.selectedItems()
        if len(selected_items) != 1:
            return

        group_id = int(selected_items[0].text(0))
        data = self.properties.group_properties.get(("selection_group", group_id))

        if not isinstance(data, dict):
            return

        entity_type = data.get("entity_type")
        entities_id = data.get("entities_id")

        match entity_type:
            case "Volumes":
                app().main_window.selection.set_geometry_selection(volumes=entities_id)

            case "Surfaces":
                app().main_window.selection.set_geometry_selection(surfaces=entities_id)

            case "Lines":
                app().main_window.selection.set_geometry_selection(lines=entities_id)

    def tab_event_callback(self):
        current_tab = self.tabWidget_main.currentIndex()
        list_tab = current_tab == SetupTabType.LIST

        if self.last_tab == SetupTabType.LIST or list_tab:
            app().main_window.selection.clear_selection()

        self.pushButton_apply.setDisabled(list_tab)
        self.pushButton_apply_and_close.setDisabled(list_tab)
        self.pushButton_remove.setDisabled(True)

        self.last_tab = current_tab

    def actions_to_finalize(self, close_window: bool = False):
        self.load_model_info()
        app().project.update_model_properties_file()
        app().main_window.update_symbols()
        app().main_window.selection.clear_selection()

        if close_window:
            self.close()

    def change_to_selector_mode(self):
        self.frame_apply_buttons.setVisible(False)
        self.frame_reset_remove_buttons.setVisible(False)
        self.tabWidget_main.setTabVisible(SetupTabType.SETUP, False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)