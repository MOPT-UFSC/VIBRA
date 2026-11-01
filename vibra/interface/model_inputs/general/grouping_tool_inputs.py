from collections import defaultdict
from copy import deepcopy
from enum import IntEnum

import numpy as np
from PySide6.QtCore import QItemSelectionModel, QPoint, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.extensions import SUPPORTED_SPREADSHEET_EXTENSIONS, SUPPORTED_TEXT_EXTENSIONS
from vibra.interface import error_title
from vibra.interface.common.common_interface import InputDataType, check_input_entries, update_analysis_setup_in_file, update_entities_selection
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.acoustic.definitions.enums import StandardTabType
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.numeric_checks.int_list_validator import IntListValidator
from vibra.interface.ui_generated.model.general.grouping_tool_inputs_ui import GroupingToolInputs_UI
from vibra.interface.user_input.data_handler.file_dialog_service import FileDialogService
from vibra.interface.user_input.data_handler.file_handlers.file_handler import FileHandler


class SelectionMode(IntEnum):
    SELECT_ALL = 0
    SELECT_BY_SIDE = 1


class SelectionFilter(IntEnum):
    VOLUMES = 0
    SURFACES = 1
    LINES = 2


class DomainFilter(IntEnum):
    NONE = 0
    ACOUSTIC = 1
    STRUCTURAL = 2


class GroupingToolInputs(GroupingToolInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()
        
        self._config_window()
        self._initialize()
        self._configure_widgets()
        self._create_connections()
        self._configure_validators()

        # while self.keep_window_open:
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

    def _configure_widgets(self):
        pass

    def _configure_validators(self):
        pass

    def _create_connections(self):

        # QComboBox connection
        self.comboBox_domain_filter.currentIndexChanged.connect(self.domain_filter_callback)
        self.comboBox_selector_filter.currentIndexChanged.connect(self.selection_filter_callback)

        # QPushButton connections
        self.pushButton_select.clicked.connect(self.select_entities_callback)

        # QTabWidget connection
        # self.tabWidget_main.currentChanged.connect(self.tab_event_callback)

        # QTreeWidget connections
        # self.treeWidget_specific_impedance.itemClicked.connect(self.item_clicked_callback)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

        self.geometry_selection_callback()

    def geometry_selection_callback(self):

        volumes = app().main_window.selection.geometry_volumes
        surfaces = app().main_window.selection.geometry_surfaces
        lines = app().main_window.selection.geometry_lines

        select_all = self.comboBox_mode.currentIndex() == SelectionMode.SELECT_ALL
        single_selection = len(volumes) + len(surfaces) + len(lines) == 1

        self.pushButton_select.setEnabled(select_all or single_selection)

        # if surfaces:
        #     text = ", ".join([str(i) for i in surfaces])
        #     self.lineEdit_selection_id.setText(text)

    def domain_filter_callback(self):
        pass
    
    def selection_filter_callback(self):
        pass

    def select_entities_callback(self):
        mode = self.comboBox_mode.currentIndex()
        match mode:
            case  SelectionMode.SELECT_ALL:
                self.select_all_callback()
            case SelectionMode.SELECT_BY_SIDE:
                self.select_by_size_callback()
            case _:
                pass

    def select_by_size_callback(self):

        volumes = app().main_window.selection.geometry_volumes
        if len(volumes) == 1:
            equal_volumes = self.model.model_selection_tools.select_volumes_by_size(next(iter(volumes))) 
            app().main_window.selection.set_geometry_selection(volumes=equal_volumes)

        surfaces = app().main_window.selection.geometry_surfaces
        if len(surfaces) == 1:
            equal_surfaces = self.model.model_selection_tools.select_surfaces_by_size(next(iter(surfaces))) 
            app().main_window.selection.set_geometry_selection(surfaces=equal_surfaces)

        lines = app().main_window.selection.geometry_lines
        if len(lines) == 1:
            equal_lines = self.model.model_selection_tools.select_lines_by_size(next(iter(lines)))
            app().main_window.selection.set_geometry_selection(lines=equal_lines)

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