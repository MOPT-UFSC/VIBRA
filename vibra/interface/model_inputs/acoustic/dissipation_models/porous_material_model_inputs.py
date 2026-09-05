import warnings
from collections import defaultdict
from enum import IntEnum
from typing import Dict, List

import numpy as np
from PySide6.QtCore import QItemSelectionModel, QPoint, Qt
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QDialog, QDoubleSpinBox, QMenu, QTableWidgetItem, QTreeWidgetItem

from vibra import app
from vibra.engine.dissipation_models.porous_materials_models import (
    PorousMaterialModels,
    get_DB_standard_constants,
    get_DBM_standard_constants,
    get_user_defined_constants,
)
from vibra.engine.properties.fluid import Fluid
from vibra.interface import error_title
from vibra.interface.formatters.icons import Icon
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.acoustic.definitions.enums import AttributionBodiesType, PlotTypesTab
from vibra.interface.model_inputs.acoustic.dissipation_models.dbm_data import DelanyBazleyMikiData
from vibra.interface.model_inputs.acoustic.dissipation_models.jcal_data import JhonsonChampouxAllardLafargeData
from vibra.interface.model_inputs.acoustic.dissipation_models.show_porous_material_model_equations import ShowPorousMaterialModelEquations
from vibra.interface.model_inputs.fluid.set_fluid_inputs_simplified import SetFluidInputsSimplified
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.ui_generated.model.acoustic.dissipation_models.porous_material_model_inputs_ui import PorousMaterialModelInputs_UI


class TabType(IntEnum):
    DBM_MODELS = 0
    JCAL_MODELS = 1
    EDIT = 2
    LIST = 3


class PMEditModelsTab(IntEnum):
    DB_DBM = 0
    JCA_JCAL = 1


class DBMConstants(IntEnum):
    DELANY_BAZLEY = 0
    DELANY_BAZLEY_MIKI = 1
    USER_DEFINED = 2


class FlowResistivityNormalization(IntEnum):
    NONE = 0
    BY_DENSITY = 1


class JCALMaterialModel(IntEnum):
    JCA = 0
    JCAL = 1


class PorousMaterialModelInputs(PorousMaterialModelInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()
        app().main_window.selection.volume_selection_mode = True

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._configure_widgets()
        self._create_connections()
        self.load_info()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _configure_widgets(self):
        #
        for i, width in enumerate([120, 160]):
            self.treeWidget_porous_material_model.setColumnWidth(i, width)
        #
        self.tableWidget_DBM.verticalHeader().setVisible(True)
        self.tableWidget_JCAL.verticalHeader().setVisible(True)

    def _initialize(self):
        self.selected_fluid = None
        self.auxiliar_dialog = None
        self.update_tabs = True
        self.keep_window_open = True
        self.material_model_data = dict()
        self.last_tab = self.tabWidget_main.currentIndex()
        self.tree_item_clicked = False
        app().main_window.selection.volume_selection_mode = True

    def _create_connections(self):
        #
        self.checkBox_advanced_porous_material_plots.stateChanged.connect(self.advanced_porous_material_callback)
        self.checkBox_load_material_data_from_selection.stateChanged.connect(self.geometry_selection_callback)
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.update_attribution_type)
        self.comboBox_DBM_constants.currentIndexChanged.connect(self.update_DBM_constants_callback)
        self.comboBox_plot_type.currentIndexChanged.connect(self.plot_type_callback)
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        self.pushButton_DB_equations.clicked.connect(self.show_equations_for_DBM_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_porous_material_model)
        #
        self.tableWidget_DBM.cellChanged.connect(lambda row, column: self.cell_changed_callback(row, column, model="delany"))
        self.tableWidget_JCAL.cellChanged.connect(lambda row, column: self.cell_changed_callback(row, column, model="jca"))
        #
        self.treeWidget_porous_material_model.itemClicked.connect(self.on_click_item)
        self.treeWidget_porous_material_model.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.update_attribution_type()
        self.update_plot_buttons_access()
        self.advanced_porous_material_callback()
        self.configure_right_click_actions_to_copy_porous_material_parameters()

    def configure_right_click_actions_to_copy_porous_material_parameters(self):
        self.tableWidget_DBM.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget_JCAL.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget_DBM.customContextMenuRequested.connect(self.show_context_menu_DBM)
        self.tableWidget_JCAL.customContextMenuRequested.connect(self.show_context_menu_JCAL)

        self.tableWidget_DBM.setToolTip("Right-click to copy the porous material parameters")
        self.tableWidget_JCAL.setToolTip("Right-click to copy the porous material parameters")

    def show_context_menu_DBM(self, pos):
        item = self.tableWidget_DBM.itemAt(pos)
        if not item:
            return

        menu = QMenu(self)

        action_DBM = QAction("Copy porous material", self)
        action_DBM.setIcon(Icon(":/icons/copy_icon.png"))
        menu.addAction(action_DBM)

        action_DBM.triggered.connect(lambda: self.copy_DBM_porous_material_parameters(item))
        menu.exec_(self.tableWidget_DBM.viewport().mapToGlobal(pos))

    def show_context_menu_JCAL(self, pos):
        item = self.tableWidget_JCAL.itemAt(pos)
        if not item:
            return

        menu = QMenu(self)

        action_JCAL = QAction("Copy porous material", self)
        action_JCAL.setIcon(Icon(":/icons/copy_icon.png"))
        menu.addAction(action_JCAL)

        action_JCAL.triggered.connect(lambda: self.copy_JCAL_porous_material_parameters(item))
        menu.exec_(self.tableWidget_JCAL.viewport().mapToGlobal(pos))

    def copy_DBM_porous_material_parameters(self, item: QTableWidgetItem):
        item_0 = self.tableWidget_DBM.item(0, item.column())
        if item_0 is None:
            return

        identifier = int(item_0.text())
        pm_data = self.map_model_id_to_model.get(identifier)
        if not isinstance(pm_data, DelanyBazleyMikiData):
            return

        self.load_porous_material_model_inputs(pm_data.get_data())

    def copy_JCAL_porous_material_parameters(self, item: QTableWidgetItem):
        item_0 = self.tableWidget_JCAL.item(0, item.column())
        if item_0 is None:
            return

        identifier = int(item_0.text())
        pm_data = self.map_model_id_to_model.get(identifier)
        if not isinstance(pm_data, JhonsonChampouxAllardLafargeData):
            return

        self.load_porous_material_model_inputs(pm_data.get_data())

    def actions_to_finalize(self, close_window: bool = False):
        self.load_info()
        app().main_window.update_symbols()
        app().project.update_model_properties_file()

        if close_window:
            self.close()

    def advanced_porous_material_callback(self):
        enabled = self.checkBox_advanced_porous_material_plots.isChecked()
        self.frame_plot_setup.setVisible(enabled)
        self.frame_plot_buttons.setVisible(enabled)
    
    def geometry_selection_callback(self):
        current_tab = self.tabWidget_main.currentIndex()
        if current_tab == TabType.LIST:
            self.verify_if_selected_volumes_are_in_tree_widget_porous_material_model()
            self.comboBox_attribution_type.setCurrentIndex(AttributionBodiesType.SELECTED_BODIES)
            return

        volumes = app().main_window.selection.geometry_volumes
        if not volumes:
            return

        if self.comboBox_attribution_type.currentIndex() == AttributionBodiesType.ALL_BODIES:
            self.comboBox_attribution_type.setCurrentIndex(AttributionBodiesType.SELECTED_BODIES)

        text = ", ".join([str(i) for i in volumes])
        self.lineEdit_selection_id.setText(text)

        if not self.checkBox_load_material_data_from_selection.isChecked():
            return

        if len(volumes) == 1 and self.update_tabs:
            volume_id = list(volumes)[0]
            pm_data = self.properties._get_property("porous_material_model", volume=volume_id)
            if pm_data is None:
                return

            self.load_porous_material_model_inputs(pm_data)
    
    def verify_if_selected_volumes_are_in_tree_widget_porous_material_model(self):
        if self.tree_item_clicked:
            return

        selected_volumes = app().main_window.selection.geometry_volumes

        if not selected_volumes:
            return

        self.clear_line_edit_selection_id()
        self.treeWidget_porous_material_model.clearSelection()
        self.pushButton_remove.setDisabled(True)

        map_id_to_model_index = self.get_tree_widget_porous_material_model_items_map()
        selected_ids = set(map_id_to_model_index.keys())
        selected_volumes_in_tree_widget = selected_volumes.intersection(selected_ids)

        if not selected_volumes_in_tree_widget:
            return
        
        self.pushButton_remove.setEnabled(True)
        
        model_selector = self.treeWidget_porous_material_model.selectionModel()

        for volume_id in selected_volumes_in_tree_widget:
            model_index = map_id_to_model_index[volume_id]

            model_selector.select(model_index, QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)

        self.treeWidget_porous_material_model.setSelectionMode(QAbstractItemView.SingleSelection)
        self.set_selection_text(selected_volumes_in_tree_widget)

    def get_tree_widget_porous_material_model_items_map(self) -> dict:
        map_id_to_model_index = dict()

        index = self.treeWidget_porous_material_model.indexAt(QPoint(0, 0))
        while index.isValid():
            item = self.treeWidget_porous_material_model.itemFromIndex(index)
            volume_id = int(item.text(0))

            map_id_to_model_index[volume_id] = index

            index = self.treeWidget_porous_material_model.indexBelow(index)
        
        return map_id_to_model_index

    def have_DBM_constants_modified(self, pm_data: dict):

        pm_model = pm_data.get("model")
        if pm_model == "User-defined (DBM)":
            return True

        current_constants = dict()
        for i in range(8):
            key = f"C{i+1}"
            value = pm_data.get(key)
            current_constants[key] = value

        if pm_model == "Delany-Bazley":
            DB_standard_constants = get_DB_standard_constants()
            return current_constants != DB_standard_constants

        elif pm_model == "Delany-Bazley-Miki":
            DBM_standard_constants = get_DBM_standard_constants()
            return current_constants != DBM_standard_constants

    def load_porous_material_model_inputs(self, pm_data: dict):

        pm_model = pm_data.get("model")

        DBM_models = ["Delany-Bazley", "Delany-Bazley-Miki", "User-defined (DBM)"]
        JCAL_models = ["Jhonson-Champoux-Allard", "Jhonson-Champoux-Allard-Lafarge"]

        if pm_model in DBM_models:
            index = DBM_models.index(pm_model)
            user_defined = index == DBMConstants.USER_DEFINED

            # check if the DBM constants have been modified (to ensure the backwards compatibility)
            if not user_defined and self.have_DBM_constants_modified(pm_data):
                user_defined = True
                index = DBMConstants.USER_DEFINED

            self.comboBox_DBM_constants.setCurrentIndex(index)
            self.tabWidget_main.setCurrentIndex(TabType.DBM_MODELS)

            normalize_flow_resistivity = pm_data.get("normalize_flow_resistivity", False)
            self.comboBox_normalize_flow_resistivity.setCurrentIndex(int(normalize_flow_resistivity))

            for key, value in pm_data.items():
                if key in ["model", "normalize_flow_resistivity"]:
                    continue

                elif key == "flow_resistivity":
                    self.doubleSpinBox_flow_resistivity_DBM.setValue(value)

                else:
                    widget = getattr(self, f"doubleSpinBox_{key}_DBM")
                    if not isinstance(widget, QDoubleSpinBox):
                        continue

                    widget.setEnabled(user_defined)
                    widget.setValue(value)

        elif pm_model in JCAL_models:
            index = JCAL_models.index(pm_model)
            self.comboBox_JCAL_pm_model.setCurrentIndex(index)
            self.tabWidget_main.setCurrentIndex(TabType.JCAL_MODELS)
            self.doubleSpinBox_porosity_JCAL.setValue(pm_data["porosity"])
            self.doubleSpinBox_tortuosity_JCAL.setValue(pm_data["tortuosity"])
            self.lineEdit_thermal_characteristic_length_JCAL.setText(str(pm_data["thermal_characteristic_length"]))
            self.lineEdit_viscous_characteristic_length_JCAL.setText(str(pm_data["viscous_characteristic_length"]))
            self.doubleSpinBox_flow_resistivity_JCAL.setValue(pm_data["flow_resistivity"])

    def show_equations_for_DBM_callback(self):
        self.auxiliar_dialog = ShowPorousMaterialModelEquations()

    def update_plot_buttons_access(self):
        state = self.selected_fluid is None
        self.comboBox_plot_type.setDisabled(state)
        self.pushButton_plot_data.setDisabled(state)
        self.plot_type_callback()

    def plot_type_callback(self):
        if self.comboBox_plot_type.currentIndex() < PlotTypesTab.SURFACE_IMPEDANCE:
            self.doubleSpinBox_porous_material_depth.setDisabled(True)
        else:
            self.doubleSpinBox_porous_material_depth.setDisabled(False)

    def remove_callback(self):
        selected_volumes = self.get_selected_volumes_from_tree_widget_porous_material_model()

        if not selected_volumes:
            return
        
        for volume_id in selected_volumes:
            self.properties._remove_volume_property("porous_material_model", volume_id)
            
        self.clear_line_edit_selection_id()
        self.pushButton_remove.setDisabled(True)

        app().main_window.selection.clear_selection()
        self.actions_to_finalize()

        if len(self.map_model_id_to_model) > 0:
            self.tabWidget_main.setCurrentIndex(TabType.LIST)

    def reset_callback(self):

        title = "Porous material model reset"
        message = "Would you like to remove the porous material effects from the model?"

        buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            self.properties._reset_property("porous_material_model")
            self.actions_to_finalize()

    def tab_event_porous_material_model(self):
        current_tab = self.tabWidget_main.currentIndex()
        edit_or_list_tabs = [TabType.EDIT, TabType.LIST]
        pm_tab = current_tab <= TabType.JCAL_MODELS

        if self.last_tab in edit_or_list_tabs or current_tab in edit_or_list_tabs:
            self.comboBox_attribution_type.setCurrentIndex(AttributionBodiesType.SELECTED_BODIES)
            app().main_window.selection.clear_selection()
            self.clear_line_edit_selection_id()

        self.frame_plot_setup.setVisible(pm_tab)
        self.frame_plot_buttons.setVisible(pm_tab)
        self.pushButton_apply.setEnabled(pm_tab)
        self.comboBox_attribution_type.setEnabled(pm_tab)

        self.last_tab = current_tab

        if pm_tab:
            if self.comboBox_attribution_type.currentIndex() == AttributionBodiesType.ALL_BODIES:
                return

            self.lineEdit_selection_id.setDisabled(False)

        else:
            self.lineEdit_selection_id.setDisabled(True)

            self.pushButton_remove.setDisabled(True)
            self.treeWidget_porous_material_model.clearSelection()

    def on_click_item(self, item):
        self.tree_item_clicked = True

        volume_ids = self.get_selected_volumes_from_tree_widget_porous_material_model()

        if not volume_ids:
            return

        self.update_tabs = False

        app().main_window.selection.set_geometry_selection(volumes=volume_ids)
        self.pushButton_remove.setDisabled(False)
        self.set_selection_text(volume_ids)
        self.update_tabs = True

        self.tree_item_clicked = False

    def on_doubleclick_item(self, item):
        self.on_click_item(item)
    
    def get_selected_volumes_from_tree_widget_porous_material_model(self) -> list:
        selected_items = self.treeWidget_porous_material_model.selectedItems()

        if not selected_items:
            return list()

        return [int(item.text(0)) for item in selected_items]

    def set_selection_text(self, selected_volumes: list | set):
        selected_volumes = list(selected_volumes)
        selected_volumes.sort()

        selected_volumes = map(str, selected_volumes)
        selection_text = ", ".join(selected_volumes)

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)
    
    def clear_line_edit_selection_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")

    def cell_changed_callback(self, row, column, model):        
        item = None
        model_id = None
        parameter_position = row - 2

        if model == "delany":
            item = self.tableWidget_DBM.item(row, column)
            model_id = int(self.tableWidget_DBM.item(0, column).text())
        else:
            item = self.tableWidget_JCAL.item(row, column)
            model_id = int(self.tableWidget_JCAL.item(0, column).text())

        new_parameter_value = None
        value_error = False
        
        try:
            new_parameter_value = float(item.text())
        except Exception:
            value_error = True
        
        parameters_position = self.map_model_id_to_model[model_id].get_parameters_position()
        model = self.map_model_id_to_model[model_id]

        if value_error:
            new_parameter_value = getattr(model, parameters_position[parameter_position])
            item.setText(str(new_parameter_value))
        else:
            setattr(model, parameters_position[parameter_position], new_parameter_value)

            volumes = self.map_model_id_to_volumes[model_id]

            for volume in volumes:
                self.properties._set_property("porous_material_model", model.get_data(), volume=volume)
            
            app().project.update_model_properties_file()

    def update_DBM_constants_callback(self):
        index = self.comboBox_DBM_constants.currentIndex()
        user_defined = index == DBMConstants.USER_DEFINED

        model_constants = dict()  
        if index == DBMConstants.DELANY_BAZLEY:
            model_constants = get_DB_standard_constants()

        elif index == DBMConstants.DELANY_BAZLEY_MIKI:
            model_constants = get_DBM_standard_constants()

        elif index == DBMConstants.USER_DEFINED:
            model_constants = get_user_defined_constants()

        for key, value in model_constants.items():
            widget = getattr(self, f"doubleSpinBox_{key}_DBM")
            if not isinstance(widget, QDoubleSpinBox):
                continue

            widget.setValue(value)
            widget.setEnabled(user_defined)

        if not user_defined:
            return

        for _widget in self.findChildren(QDoubleSpinBox):
            if "doubleSpinBox_C" in _widget.objectName():
                _widget.setEnabled(user_defined)
           
    def update_attribution_type(self):
        index = self.comboBox_attribution_type.currentIndex()
        if index == AttributionBodiesType.ALL_BODIES:
            self.lineEdit_selection_id.setText("All bodies")
            self.lineEdit_selection_id.setEnabled(False)

        elif index == AttributionBodiesType.SELECTED_BODIES:
            self.clear_line_edit_selection_id()
            self.lineEdit_selection_id.setEnabled(True)

    def map_existing_porous_materials(self):
        self.map_model_id_to_volumes: Dict[int, List[str]] = defaultdict(list)
        self.map_model_id_to_model: Dict[int, DelanyBazleyMikiData|JhonsonChampouxAllardLafargeData] = dict()

        models = list()
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key

            if property != "porous_material_model":
                continue

            if not isinstance(data, dict):
                continue

            try:
                model = None
                if data.get("model") in ["Delany-Bazley", "Delany-Bazley-Miki", "User-defined (DBM)"]:
                    model = DelanyBazleyMikiData.set_data(data)
                else:
                    model = JhonsonChampouxAllardLafargeData.set_data(data)

                if model not in models:
                    models.append(model)

                model_id = models.index(model) + 1
                self.map_model_id_to_model[model_id] = model

                if volume_id not in self.map_model_id_to_volumes[model_id]:
                    self.map_model_id_to_volumes[model_id].append(volume_id)

            except Exception:
                title = "Porous Material Model Error"
                message = "An error occurred while trying to load the porous material model data "
                message += "from the project file. The porous material model will be deleted."
                PrintMessageInput([error_title, title, message])

                self.properties._reset_property("porous_material_model")
                app().main_window.update_symbols()

                return

    def load_info(self):
        self.map_existing_porous_materials()

        self.treeWidget_porous_material_model.clear()
        self.update_treeWidget_porous_materials()
        self.configure_tables_and_tabs_widgets()

        delany_counter = 0
        jca_counter = 0

        there_is_delany_model = False
        there_is_jca_model = False

        DBM_models = ["Delany-Bazley", "Delany-Bazley-Miki", "User-defined (DBM)"]
        JCAL_models = ["Jhonson-Champoux-Allard", "Jhonson-Champoux-Allard-Lafarge"]

        for _, (model_id, model_data) in enumerate(self.map_model_id_to_model.items()):
            model = model_data.model
            model_data_dict = model_data.get_data()

            model_id_item = QTableWidgetItem(str(model_id))
            model_item = QTableWidgetItem(self.abbreviate_porous_material_model_name(model))
            model_id_item.setFlags(Qt.ItemIsSelectable)
            model_item.setFlags(Qt.ItemIsSelectable)
            model_item.setToolTip(model)
        
            if model in DBM_models:
                there_is_delany_model = True

                self.tableWidget_DBM.setItem(0, delany_counter, model_id_item)
                self.tableWidget_DBM.setItem(1, delany_counter, model_item)

                for k, model_input in enumerate(model_data_dict.values()):

                    if isinstance(model_input, str):
                        continue

                    self.tableWidget_DBM.setItem(2+k, delany_counter, QTableWidgetItem(str(model_input)))

                delany_counter += 1

            elif model in JCAL_models:
                there_is_jca_model = True

                self.tableWidget_JCAL.setItem(0, jca_counter, model_id_item)
                self.tableWidget_JCAL.setItem(1, jca_counter, model_item)

                for k, model_input in enumerate(model_data_dict.values()):

                    if isinstance(model_input, str):
                        continue

                    self.tableWidget_JCAL.setItem(2+k, jca_counter, QTableWidgetItem(str(model_input)))

                jca_counter += 1

        if there_is_jca_model:
            self.tabWidget_models.setTabVisible(PMEditModelsTab.JCA_JCAL, True)
        
        if there_is_delany_model:
            self.tabWidget_models.setTabVisible(PMEditModelsTab.DB_DBM, True)
            self.tabWidget_models.setCurrentIndex(PMEditModelsTab.DB_DBM)

        if there_is_jca_model or there_is_delany_model:
            self.tabWidget_main.setTabVisible(TabType.EDIT, True)
            self.tabWidget_main.setTabVisible(TabType.LIST, True)
        
        self.update_tableWidget_DBM_items()
        self.update_tableWidget_JCAL_items()
    
    def update_treeWidget_porous_materials(self):
        for model_id, volume_ids in self.map_model_id_to_volumes.items():
            model_data = self.map_model_id_to_model[model_id]

            for volume_id in volume_ids:
                new = QTreeWidgetItem([str(volume_id), self.abbreviate_porous_material_model_name(model_data.model), str(model_id)])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_porous_material_model.addTopLevelItem(new)
        
    def configure_tables_and_tabs_widgets(self):
        delany_count = 0
        jca_count = 0

        for model in self.map_model_id_to_model.values():
            if isinstance(model, DelanyBazleyMikiData):
                delany_count += 1
            else:
                jca_count += 1

        self.tableWidget_DBM.clearContents()
        self.tableWidget_DBM.blockSignals(True)
        self.tableWidget_DBM.setRowCount(11)
        self.tableWidget_DBM.setColumnCount(delany_count)

        self.tableWidget_JCAL.clearContents()
        self.tableWidget_JCAL.blockSignals(True)
        self.tableWidget_JCAL.setRowCount(7)
        self.tableWidget_JCAL.setColumnCount(jca_count)

        self.tabWidget_models.setTabVisible(PMEditModelsTab.DB_DBM, False)
        self.tabWidget_models.setTabVisible(PMEditModelsTab.JCA_JCAL, False)

        self.tabWidget_main.setTabVisible(TabType.EDIT, False)
        self.tabWidget_main.setTabVisible(TabType.LIST, False)
    
    def update_tableWidget_DBM_items(self):
        for i in range(self.tableWidget_DBM.rowCount()):
            for j in range(self.tableWidget_DBM.columnCount()):
                item = self.tableWidget_DBM.item(i, j)

                if item is None:
                    item = QTableWidgetItem()
                    self.tableWidget_DBM.setItem(i, j, item)
                    item.setFlags(Qt.ItemIsSelectable)

                item.setTextAlignment(Qt.AlignCenter)
        
        self.tableWidget_DBM.blockSignals(False)
    
    def update_tableWidget_JCAL_items(self):
        for i in range(self.tableWidget_JCAL.rowCount()):
            for j in range(self.tableWidget_JCAL.columnCount()):
                item = self.tableWidget_JCAL.item(i, j)

                if item is None:
                    item = QTableWidgetItem()
                    self.tableWidget_JCAL.setItem(i, j, item)
                    item.setFlags(Qt.ItemIsSelectable)

                item.setTextAlignment(Qt.AlignCenter)

        self.tableWidget_JCAL.blockSignals(False)

    def abbreviate_porous_material_model_name(self, model:str) -> str:
        if model == "Delany-Bazley":
            return "DB"

        elif model == "Delany-Bazley-Miki":
            return "DBM"

        elif model == "Jhonson-Champoux-Allard":
            return "JCA"

        return "JCAL"

    def get_Delany_Bazley_Miki_model_data(self, material_model: str) -> DelanyBazleyMikiData:
        return DelanyBazleyMikiData(
            material_model,
            self.doubleSpinBox_C1_DBM.value(),
            self.doubleSpinBox_C2_DBM.value(),
            self.doubleSpinBox_C3_DBM.value(),
            self.doubleSpinBox_C4_DBM.value(),
            self.doubleSpinBox_C5_DBM.value(),
            self.doubleSpinBox_C6_DBM.value(),
            self.doubleSpinBox_C7_DBM.value(),
            self.doubleSpinBox_C8_DBM.value(),
            self.doubleSpinBox_flow_resistivity_DBM.value(),
            normalize_flow_resistivity=self.comboBox_normalize_flow_resistivity.currentIndex() == FlowResistivityNormalization.BY_DENSITY,
        )

    def get_Jhonson_Champoux_Allard_Lafarge_model_data(self, material_model: str) -> JhonsonChampouxAllardLafargeData:

        lineEdit = self.lineEdit_viscous_characteristic_length_JCAL
        vcl = self.check_inputs(lineEdit, "Viscous characteristic length", only_positive=True)
        if self.stop:
            lineEdit.setFocus()
            return dict()

        lineEdit = self.lineEdit_thermal_characteristic_length_JCAL
        tcl = self.check_inputs(lineEdit, "Thermal characteristic length", only_positive=True)
        if self.stop:
            lineEdit.setFocus()
            return dict()

        return JhonsonChampouxAllardLafargeData(
            self.doubleSpinBox_porosity_JCAL.value(),
            self.doubleSpinBox_tortuosity_JCAL.value(),
            vcl,
            tcl,
            self.doubleSpinBox_flow_resistivity_JCAL.value(),
            material_model,
        )

    def get_DBM_material_model(self):
        index = self.comboBox_DBM_constants.currentIndex()
        if index == DBMConstants.DELANY_BAZLEY:
            return "Delany-Bazley"
        elif index == DBMConstants.DELANY_BAZLEY_MIKI:
            return "Delany-Bazley-Miki"
        else:
            return "User-defined (DBM)"

    def get_JCAL_material_model(self):
        if self.comboBox_JCAL_pm_model.currentIndex() == JCALMaterialModel.JCA:
            return "Jhonson-Champoux-Allard"
        else:
            return "Jhonson-Champoux-Allard-Lafarge"

    def apply_callback(self, close_window: bool = False):

        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == TabType.DBM_MODELS:
            pm_model = self.get_DBM_material_model()
            model_data = self.get_Delany_Bazley_Miki_model_data(pm_model)

        elif tab_index == TabType.JCAL_MODELS:
            pm_model = self.get_JCAL_material_model()
            model_data = self.get_Jhonson_Champoux_Allard_Lafarge_model_data(pm_model)

        else:
            return

        attribute_type = self.comboBox_attribution_type.currentIndex()
        if attribute_type in [AttributionBodiesType.ALL_BODIES, AttributionBodiesType.SELECTED_BODIES]:
            
            volume_ids = list()
            if attribute_type == AttributionBodiesType.ALL_BODIES:
                if "volumes" in self.mesh.geometry_information:
                    volume_ids = self.mesh.geometry_information["volumes"]

            elif attribute_type == AttributionBodiesType.SELECTED_BODIES:

                input_ids = self.lineEdit_selection_id.text()
                volume_ids, error_data = self.model.check_selected_ids(
                    input_ids,
                    "volumes",
                    domain="acoustic",
                )

                if error_data is not None:
                    self.lineEdit_selection_id.setFocus()
                    PrintMessageInput(error_data)
                    return True

            for volume_id in volume_ids:
                self.properties._set_property("porous_material_model", model_data.get_data(), volume=volume_id)

            self.actions_to_finalize(close_window)

    def check_inputs(self, lineEdit, label, only_positive=False, zero_included=True, _float=True):

        self.stop = False
        message = ""

        title = "Invalid input at dissipation model"
        input_str = lineEdit.text()

        if input_str != "":

            input_str = input_str.replace(",", ".")

            try:
                if _float:
                    out = float(input_str)
                else:
                    out = int(input_str)

                if only_positive:
                    if zero_included:
                        if out < 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is allowed."
                    else:
                        if out <= 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is not allowed."

            except Exception as _err:
                message = "Dear user, you have typed an invalid value at the \n"
                message += f"{label} input field.\n\n"
                message += str(_err)

        else:
            if zero_included:
                return float(0)
            else:
                message = f"Insert some value at the {label} input field."

        if message != "":
            PrintMessageInput([error_title, title, message])
            self.stop = True
            return None
        return out

    # Plot viscous-thermal effective properties

    def get_fluid_callback(self):
        self.hide()
        self.fluid_dialog = SetFluidInputsSimplified()
        self.fluid_dialog.fluid_widget.pushButton_apply.setVisible(False)
        self.fluid_dialog.fluid_widget.pushButton_apply_and_close.clicked.connect(self.get_selected_fluid)
        self.fluid_dialog.exec()
        app().main_window.set_input_widget(self)

    def get_selected_fluid(self):
        self.selected_fluid = self.fluid_dialog.get_selected_fluid()
        if isinstance(self.selected_fluid, Fluid):
            self.fluid_dialog.close()
            self.update_plot_buttons_access()
            self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
            self.lineEdit_fluid_density.setText(f"{self.selected_fluid.fluid_density}")
            self.lineEdit_speed_of_sound.setText(f"{self.selected_fluid.speed_of_sound}")

    def get_effective_properties(self, fluid: Fluid):

        warnings.filterwarnings('ignore')

        frequencies = app().project.model.frequencies
        if frequencies is None:
            df = 5
            f_min = 5
            f_max = 1400
            frequencies = np.arange(f_min, f_max+df, df)

        if frequencies[0] == 0:
            freq = frequencies[1:]
        else:
            freq = frequencies

        omega = 2 * np.pi * freq

        model = PorousMaterialModels(self.model)

        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == TabType.DBM_MODELS:
            pm_model = self.get_DBM_material_model()
            pm_data = self.get_Delany_Bazley_Miki_model_data(pm_model)
            rho_eff, C_eff = model.get_Delany_Bazley_Miki_effective_properties(omega, fluid, pm_data.get_data())

        elif tab_index == TabType.JCAL_MODELS:
            pm_model = self.get_JCAL_material_model()
            pm_data = self.get_Jhonson_Champoux_Allard_Lafarge_model_data(pm_model)
            rho_eff, C_eff = model.get_JCAL_effective_properties(omega, fluid, pm_data.get_data())

        else:
            return None, None

        k_cr = omega / C_eff

        return freq, rho_eff, C_eff, k_cr

    def get_porous_material_model(self):
        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == TabType.DBM_MODELS:
            return self.comboBox_DBM_constants.currentText()

        elif tab_index == TabType.JCAL_MODELS:
            return self.comboBox_JCAL_pm_model.currentText()

    def plot_data_callback(self):
        plot_key = self.comboBox_plot_type.currentIndex()
        if plot_key == PlotTypesTab.FLUID_DENSITY:
            self.plot_effective_fluid_density()

        elif plot_key == PlotTypesTab.SPEED_OF_SOUND:
            self.plot_effective_speed_of_sound()

        elif plot_key == PlotTypesTab.SURFACE_IMPEDANCE:
            self.plot_surface_impedance()

        else:
            self.plot_absorption_coefficient()

    def plot_effective_fluid_density(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        freq, rho_eff, _, _ = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        pm_model = self.get_porous_material_model()
        self.plot_data(freq, rho_eff, "effective fluid density", pm_model)

    def plot_effective_speed_of_sound(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        freq, _, C_eff, _ = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        pm_model = self.get_porous_material_model()
        self.plot_data(freq, C_eff, "effective speed of sound", pm_model)

    def plot_surface_impedance(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        h = self.doubleSpinBox_porous_material_depth.value()
        Z_0 = self.selected_fluid.speed_of_sound * self.selected_fluid.fluid_density

        freq, rho_eff, C_eff, k_cr = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        Z_pm = rho_eff * C_eff
        Z_s = Z_pm * (1 / np.tanh(k_cr * h))
        Z_norm = Z_s / Z_0

        pm_model = self.get_porous_material_model()
        self.plot_data(freq, Z_norm, "normalized surface impedance", pm_model)

    def plot_absorption_coefficient(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        h = self.doubleSpinBox_porous_material_depth.value()
        Z_0 = self.selected_fluid.speed_of_sound * self.selected_fluid.fluid_density

        freq, rho_eff, C_eff, k_cr = self.get_effective_properties(self.selected_fluid)

        Z_pm = rho_eff * C_eff
        Z_s = Z_pm * (1 / np.tanh(k_cr * h))

        R_r = (Z_s - Z_0) / (Z_s + Z_0)
        alpha_n = 1 - np.abs(R_r)**2

        if freq is None:
            return

        pm_model = self.get_porous_material_model()
        self.plot_data(freq, alpha_n, "absorption coefficient", pm_model)

    def join_model_data(self, x_data, y_data, label: str, pm_label: str):

        self.hide()
        self.data_to_plot = dict()

        if label == "effective fluid density":
            unit_label = "kg/m³"
            y_label = "Effective fluid density"

        elif label == "effective speed of sound":
            unit_label = "m/s"
            y_label = "Effective speed of sound"

        elif label == "normalized surface impedance":
            unit_label = "--"
            y_label = "Normalized surface impedance"

        else:
            unit_label = "--"
            y_label = "Absorption coeffient"

        legend_label = label
        title = f"{pm_label} Porous Material Curve"

        key = (label.replace(" ", "_"), None)

        self.data_to_plot[key] = { 
                                    "x_data" : x_data,
                                    "y_data" : y_data,
                                    "x_label" : "Frequency [Hz]",
                                    "y_label" : y_label,
                                    "title" : title,
                                    "data_type" : "porous material data",
                                    "legend" : legend_label,
                                    "unit" : unit_label,
                                    "color" : [0,0,1],
                                    "linestyle" : "-"
                                   }

    def plot_data(self, x_data, y_data, label, pm_label):
        self.join_model_data(x_data, y_data, label, pm_label)
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.data_to_plot)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Control:
            self.treeWidget_porous_material_model.setSelectionMode(QAbstractItemView.MultiSelection)
        elif event.key() == Qt.Key_Shift:
            self.treeWidget_porous_material_model.setSelectionMode(QAbstractItemView.ContiguousSelection)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.treeWidget_porous_material_model.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        self.keep_window_open = False
        warnings.filterwarnings('default')

        if isinstance(self.auxiliar_dialog, QDialog):
            self.auxiliar_dialog.close()

        app().main_window.selection.volume_selection_mode = False

        return super().closeEvent(a0)