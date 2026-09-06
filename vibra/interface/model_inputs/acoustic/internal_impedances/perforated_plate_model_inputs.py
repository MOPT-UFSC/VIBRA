import logging
import warnings
from collections import defaultdict
from copy import deepcopy
from enum import IntEnum
from pathlib import Path
from typing import Dict, List

import numpy as np
from PySide6.QtCore import QItemSelectionModel, QPoint, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QLineEdit, QTableWidgetItem, QTreeWidgetItem

from vibra import app
from vibra.engine.properties.fluid import Fluid
from vibra.engine.transfer_impedances.perforated_plate_models import PerforatedPlateModels
from vibra.interface import error_title, warning_title
from vibra.interface.common.common_interface import update_analysis_setup_in_file, update_entities_selection
from vibra.interface.data.data_manager import get_spectral_data_from_array
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.model_inputs.acoustic.definitions.enums import SetupTabType
from vibra.interface.model_inputs.acoustic.internal_impedances.perforated_plate_data import PerforatedPlateData
from vibra.interface.model_inputs.fluid.set_fluid_inputs_simplified import SetFluidInputsSimplified
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.ui_generated.model.acoustic.internal_impedances.perforated_plate_model_inputs_ui import PerforatedPlateModelInputs_UI
from vibra.utils.bidict import bidict


class PPMMainTabType(IntEnum):
    SETUP = SetupTabType.SETUP
    EDIT = 1
    LIST = 2


class PPlateModelsTabType(IntEnum):
    CIRCULAR_HOLES = 0


class PlotTypeBoxType(IntEnum):
    ACOUSTIC_IMPEDANCE = 0


class IncludeEffectsBoxType(IntEnum):
    NONE = 0
    NON_LINEAR = 1
    USER_DEFINED = 2
    NON_LINEAR_AND_USER_DEFINED = 3


class PerforatedPlateModelInputs(PerforatedPlateModelInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.model_setup_workspace()
        self._initialize()
        self._config_window()
        self._config_widgets()
        self._create_connections()
        self.load_model_info()

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

    def model_setup_workspace(self):
        mesh_workspace = app().main_window.action_mesh_workspace.isChecked()
        if mesh_workspace:
            app().main_window.action_model_workspace_callback()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.selected_fluid = None
        self.imported_values = None
        self.assignment_complete = False
        self.keep_window_open = True
        self.last_tab = self.tabWidget_main.currentIndex()
        self.tree_item_clicked = False
        self.decoupling_map = bidict()

    def _create_connections(self):
        #
        self.comboBox_plot_type.currentIndexChanged.connect(self.plot_type_callback)
        self.comboBox_include_effects.currentIndexChanged.connect(self.include_effects_callback)
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_load_path.clicked.connect(self.load_user_defined_transfer_impedance)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        self.pushButton_clean_inputs.clicked.connect(self.clear_all_inputs)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_perforated_plate_model.itemClicked.connect(self.on_tree_widget_click_item)
        self.treeWidget_perforated_plate_model.itemDoubleClicked.connect(self.on_tree_widget_doubleclick_item)
        #
        self.edit_tableWidget.cellChanged.connect(self.edit_table_widget_item)
        self.edit_tableWidget.cellDoubleClicked.connect(self.edit_fluid_or_transfer_impedance)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.geometry_selection_callback()
        self.include_effects_callback()

    def geometry_selection_callback(self):
        current_tab = self.tabWidget_main.currentIndex()

        if current_tab == PPMMainTabType.LIST:
            self.verify_if_selected_surfaces_are_in_tree_widget_perforated_plate_model()
            return
    
        if current_tab != PPMMainTabType.SETUP:
            return

        surfaces = app().main_window.selection.geometry_surfaces
        if surfaces:
            surface_ids = list(surfaces)
            surface_ids.sort()

            text = ", ".join([str(i) for i in surface_ids])
            self.lineEdit_selection_id.setText(text)

            if len(surface_ids) == 1:
                pp_data = self.properties._get_property("perforated_plate_model", surface=surface_ids[0])
                if pp_data is None:
                    return

                self.load_perforated_plate_inputs(pp_data)

    def load_perforated_plate_inputs(self, data: dict):

        formulation = data.get("formulation")
        if formulation == "circular_hole":
            self.tabWidget_perforated_plate_models.setCurrentIndex(PPlateModelsTabType.CIRCULAR_HOLES)

        t_p = data.get("plate_thickness")
        if isinstance(t_p, float | int):
            self.lineEdit_plate_thickness.setText(str(t_p))

        d_h = data.get("hole_diameter")
        if isinstance(d_h, float | int):
            self.lineEdit_hole_diameter.setText(str(d_h))

        sigma = data.get("porosity")
        if isinstance(sigma, float | int):
            self.lineEdit_porosity.setText(str(sigma))

        Cd_lin = data.get("linear_discharge_coefficient")
        if isinstance(Cd_lin, float | int):
            self.lineEdit_linear_discharge_coefficient.setText(str(Cd_lin))

        Cd_nl = data.get("non_linear_discharge_coefficient")
        if isinstance(Cd_nl, float | int):
            self.lineEdit_non_linear_discharge_coefficient.setEnabled(True)
            self.lineEdit_non_linear_discharge_coefficient.setText(str(Cd_nl))
        else:
            self.lineEdit_non_linear_discharge_coefficient.setEnabled(False)

        f_nl = data.get("non_linear_correction_factor")
        if isinstance(f_nl, float | int):
            self.lineEdit_non_linear_correction_factor.setEnabled(True)
            self.lineEdit_non_linear_correction_factor.setText(str(f_nl))
        else:
            self.lineEdit_non_linear_correction_factor.setEnabled(False)

        table_path = data.get("table_paths")
        if table_path is None:
            if self.lineEdit_non_linear_discharge_coefficient.isEnabled():
                self.comboBox_include_effects.setCurrentIndex(IncludeEffectsBoxType.NON_LINEAR)

            self.pushButton_load_path.setEnabled(False)
            self.lineEdit_user_defined_transfer_impedance_path.clear()
            self.lineEdit_user_defined_transfer_impedance_path.setToolTip("")
            self.lineEdit_user_defined_transfer_impedance_path.setEnabled(False)

        elif isinstance(table_path, list):
            if self.lineEdit_non_linear_discharge_coefficient.isEnabled():
                self.comboBox_include_effects.setCurrentIndex(IncludeEffectsBoxType.NON_LINEAR_AND_USER_DEFINED)
            else:
                self.comboBox_include_effects.setCurrentIndex(IncludeEffectsBoxType.USER_DEFINED)

            self.pushButton_load_path.setEnabled(True)
            self.lineEdit_user_defined_transfer_impedance_path.setEnabled(True)
            self.lineEdit_user_defined_transfer_impedance_path.setText(table_path[0])
            self.lineEdit_user_defined_transfer_impedance_path.setToolTip(table_path[0])
        
    def verify_if_selected_surfaces_are_in_tree_widget_perforated_plate_model(self):
        if self.tree_item_clicked:
            return

        selected_surfaces = app().main_window.selection.geometry_surfaces

        if not selected_surfaces:
            return
                
        self.clear_line_edit_selection_id()
        self.treeWidget_perforated_plate_model.clearSelection()
        self.pushButton_remove.setDisabled(True)

        map_id_to_model_index = self.get_tree_widget_perforated_plate_model_items_map()

        selected_ids = set(map_id_to_model_index.keys())
        selected_surfaces_in_tree_widget = selected_surfaces.intersection(selected_ids)

        if not selected_surfaces_in_tree_widget:
            return
        
        self.pushButton_remove.setEnabled(True)
        
        model_selector = self.treeWidget_perforated_plate_model.selectionModel()

        for surface_id in selected_surfaces_in_tree_widget:
            model_index = map_id_to_model_index[surface_id]

            model_selector.select(model_index, QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)

        self.treeWidget_perforated_plate_model.setSelectionMode(QAbstractItemView.SingleSelection)

        self.set_selection_text(selected_surfaces_in_tree_widget)

    def get_tree_widget_perforated_plate_model_items_map(self) -> dict:
        map_id_to_model_index = dict()

        index = self.treeWidget_perforated_plate_model.indexAt(QPoint(0, 0))
        while index.isValid():
            item = self.treeWidget_perforated_plate_model.itemFromIndex(index)

            surface_id = int(item.text(0))
            map_id_to_model_index[surface_id] = index

            decoupling_data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_id)

            if isinstance(decoupling_data, dict):
                new_surface_id = decoupling_data.get("new_surface_id")
                map_id_to_model_index[new_surface_id] = index

                self.decoupling_map[surface_id] = new_surface_id

            index = self.treeWidget_perforated_plate_model.indexBelow(index)
        
        return map_id_to_model_index

    def clear_all_inputs(self):
        self.lineEdit_plate_thickness.clear()
        self.lineEdit_hole_diameter.clear()
        self.lineEdit_porosity.clear()
        self.lineEdit_linear_discharge_coefficient.clear()
        self.lineEdit_non_linear_discharge_coefficient.clear()
        self.lineEdit_non_linear_correction_factor.clear()
        self.lineEdit_user_defined_transfer_impedance_path.clear()

    def update_plot_buttons_access(self):
        state = self.selected_fluid is None
        self.comboBox_plot_type.setDisabled(state)
        self.plot_type_callback()

    def plot_type_callback(self):
        return

    def include_effects_callback(self):

        self.lineEdit_non_linear_discharge_coefficient.setDisabled(True)
        self.lineEdit_non_linear_correction_factor.setDisabled(True)
        self.lineEdit_user_defined_transfer_impedance_path.setDisabled(True)
        self.pushButton_load_path.setDisabled(True)

        included_effects = self.comboBox_include_effects.currentText()
        if included_effects == "None":
            return

        if "Non-linear" in included_effects:
            self.lineEdit_non_linear_discharge_coefficient.setEnabled(True)
            self.lineEdit_non_linear_correction_factor.setEnabled(True)

        if "User-defined" in included_effects:
            self.lineEdit_user_defined_transfer_impedance_path.setEnabled(True)
            self.pushButton_load_path.setEnabled(True)

    def _config_widgets(self):

        for i in range(2):
            self.treeWidget_perforated_plate_model.headerItem().setTextAlignment(i, Qt.AlignCenter)

        self.treeWidget_perforated_plate_model.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
    def tab_event_callback(self):
        current_tab = self.tabWidget_main.currentIndex()
        tab_list = current_tab == PPMMainTabType.LIST

        if self.last_tab == PPMMainTabType.LIST or tab_list:
            app().main_window.selection.clear_selection()
            self.clear_line_edit_selection_id()

        self.last_tab = current_tab

        if tab_list:
            self.pushButton_remove.setDisabled(True)
            self.lineEdit_selection_id.setDisabled(True)
            self.treeWidget_perforated_plate_model.clearSelection()

            return

        self.geometry_selection_callback()
        self.lineEdit_selection_id.setEnabled(True)

    def on_tree_widget_click_item(self, item):
        self.tree_item_clicked = True

        surface_ids = self.get_selected_surfaces_from_tree_widget_perforated_plate_model()

        if not surface_ids:
            return

        for surface_id in surface_ids:
            decoupling_data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_id)

            if isinstance(decoupling_data, dict):
                new_surface_id = decoupling_data.get("new_surface_id")
                self.decoupling_map[surface_id] = new_surface_id

        app().main_window.selection.set_geometry_selection(surfaces=surface_ids)

        self.pushButton_remove.setEnabled(True)
        self.set_selection_text(surface_ids)
    
        self.tree_item_clicked = False

    def on_tree_widget_doubleclick_item(self, item):
        self.on_tree_widget_click_item(item)
    
    def get_selected_surfaces_from_tree_widget_perforated_plate_model(self) -> list:
        selected_items = self.treeWidget_perforated_plate_model.selectedItems()

        if not selected_items:
            return []
        
        return [int(item.text(0)) for item in selected_items]

    def set_selection_text(self, selected_surfaces: list | set):
        selected_surfaces_decoupled = []

        for selected_surface in selected_surfaces:
            decouple_surface = self.decoupling_map[selected_surface] if selected_surface in self.decoupling_map.keys() else self.decoupling_map.inverse[selected_surface][0]

            decouple_pair = [selected_surface, decouple_surface]
            decouple_pair.sort()
            decouple_pair = tuple(decouple_pair)

            selected_surfaces_decoupled.append(str(decouple_pair))

        selection_text = ", ".join(selected_surfaces_decoupled)

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)
    
    def clear_line_edit_selection_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")

    def check_selection_type(self, surface_ids: list[int]) -> bool:

        title = "Invalid selection detected"

        for surface_id in surface_ids:
            if len(self.mesh.volumes_from_surface[surface_id]) != 2:
                message = f"The selected surface ID #{surface_id} does not correspond to an inside surface "
                message += "(surfaces that connect two neighboohrs volumes). The perforated plate "
                message += "assignment will be ignored until all requirements are met."
                PrintMessageInput([error_title, title, message])
                return True

    def load_model_info(self):
        self.map_existing_perforated_plate_models()
        self.configure_edit_table_widget()
        self.update_pp_model_tree_widget()
        self.update_edit_table_widget()
        self.update_tabs_visibility()
    
    def map_existing_perforated_plate_models(self):
        self.map_model_id_to_model : Dict[int, PerforatedPlateData] = dict()
        self.map_model_id_to_surfaces : Dict[int, List[int]] = defaultdict(list)

        models = []
        for key, data in deepcopy(self.properties.surface_properties).items():
            property, surface_id = key
            if property != "perforated_plate_model":
                continue

            model = PerforatedPlateData.set_data(data)
            model_aux = deepcopy(model)

            # NOTE: we must convert the values from np.ndarray into 
            # a list of values and remove the table_names to get 
            # the expected model mapping 
            if isinstance(model_aux.values, list) and len(model_aux.values) == 1:
                model_aux.values = [complex(value) for value in model.values[0]]
                model_aux.table_names = None

            if model_aux not in models:
                models.append(model_aux)

            model_id = models.index(model_aux) + 1

            self.map_model_id_to_model[model_id] = model
            self.map_model_id_to_surfaces[model_id].append(surface_id)

    def update_pp_model_tree_widget(self):
        self.treeWidget_perforated_plate_model.clear()

        for model_id, surface_ids in self.map_model_id_to_surfaces.items():
            for surface_id in surface_ids:
                new = QTreeWidgetItem([str(surface_id), str(model_id)])
                for i in range(2):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_perforated_plate_model.addTopLevelItem(new)
    
    def configure_edit_table_widget(self):
        self.edit_tableWidget.clearContents()
        self.edit_tableWidget.blockSignals(True)
        self.edit_tableWidget.setRowCount(13)
        self.edit_tableWidget.setColumnCount(len(self.map_model_id_to_model))
    
    def update_edit_table_widget(self):
        for column, model_info in enumerate(self.map_model_id_to_model.items()):
            model_id, model = model_info
        
            model_id_item = QTableWidgetItem(str(model_id))
            model_id_item.setTextAlignment(Qt.AlignCenter)
            model_id_item.setFlags(Qt.ItemIsSelectable)

            self.edit_tableWidget.setItem(0, column, model_id_item)

            for row, fluid_data in enumerate(model.get_fluid_data_to_fill_edit_table_widget()):
                item_text = str(fluid_data)

                fluid_item = QTableWidgetItem(item_text)
                fluid_item.setTextAlignment(Qt.AlignCenter)

                if not isinstance(fluid_data, str):
                    fluid_item.setFlags(Qt.ItemIsSelectable)

                if isinstance(fluid_data, str):
                    tool_tip = f"{item_text} \n\nDouble click to choose a new fluid"
                    fluid_item.setToolTip(tool_tip)

                self.edit_tableWidget.setItem(row + 1, column, fluid_item)
            
            for row, pp_data in enumerate(model.get_data_to_fill_edit_table_widget()):
                item_text = str(pp_data) if not isinstance(pp_data, Path) else pp_data.name

                pp_item = QTableWidgetItem(item_text)
                pp_item.setTextAlignment(Qt.AlignCenter)

                if isinstance(pp_data, str):
                    pp_item.setFlags(Qt.ItemIsSelectable)
                    pp_item.setToolTip(item_text)

                elif isinstance(pp_data, Path):
                    tool_tip = f"{str(pp_data)} \n\nDouble click to import a new transfer impedance file"
                    pp_item.setToolTip(tool_tip)

                self.edit_tableWidget.setItem(row + 5, column, pp_item)
        
        self.edit_tableWidget.blockSignals(False)
    
    def edit_fluid_or_transfer_impedance(self, row, column):
        if row not in [1, 12]:
            return

        model_id = int(self.edit_tableWidget.item(0, column).text())
        model = self.map_model_id_to_model[model_id]
        surface_ids = self.map_model_id_to_surfaces[model_id]

        map_table_names = dict()
        for surface_id in surface_ids:
            pp_data = self.properties._get_property("perforated_plate_model", surface=surface_id)
            if pp_data.get("table_names") is None:
                continue
            map_table_names[surface_id] = pp_data.get("table_names")

        if row == 1:
            self.get_fluid_callback()

            if self.selected_fluid:
                setattr(model, "fluid", self.selected_fluid)

            for surface_id in surface_ids:
                pp_model_data = deepcopy(model.get_data())
                if surface_id in map_table_names.keys():
                    pp_model_data["table_names"] = map_table_names.get(surface_id)

                self.properties._set_property("perforated_plate_model", pp_model_data, surface=surface_id)

        else:

            for surface_id in surface_ids:
                self.include_user_defined_transfer_impedance(model, surface_id)
                pp_model_data = deepcopy(model.get_data())
                if surface_id in map_table_names.keys():
                    pp_model_data["table_names"] = map_table_names.get(surface_id)

                self.properties._set_property("perforated_plate_model", pp_model_data, surface=surface_id)

            self.imported_values = None
            self.lineEdit_user_defined_transfer_impedance_path.clear()
            app().main_window.results_viewer_widget.plot_acoustic_harmonic._initialize()

        app().project.update_model_properties_file()
        if row == 12:
            app().project.update_model_properties_file()

        self.load_model_info()

    def edit_table_widget_item(self, row, column):
        item = self.edit_tableWidget.item(row, column)
        model_id = int(self.edit_tableWidget.item(0, column).text())

        new_item_value = None
        unnaceptable_value_error = False

        try:
            input_value = item.text().replace(",", ".")
            new_item_value = float(input_value)
            if new_item_value <= 0.:
                new_item_value = None
                unnaceptable_value_error = True

        except Exception:
            unnaceptable_value_error = True

        model = self.map_model_id_to_model[model_id]
        indexed_attributes = model.get_indexed_attributes()

        attribute = indexed_attributes[row - 3]

        if unnaceptable_value_error:
            new_item_value = getattr(model, attribute)
            item.setText(str(new_item_value))
        else:
            setattr(model, attribute, new_item_value)

        surfaces_ids = self.map_model_id_to_surfaces[model_id]
        for surface_id in surfaces_ids:
            self.properties._set_property("perforated_plate_model", model.get_data(), surface=surface_id)

        app().project.update_model_properties_file()
        self.load_model_info()
    
    def update_tabs_visibility(self):

        if len(self.map_model_id_to_model) > 0:
            self.tabWidget_main.setTabVisible(PPMMainTabType.EDIT, True)
            self.tabWidget_main.setTabVisible(PPMMainTabType.LIST, True)

            return

        self.tabWidget_main.setCurrentIndex(PPMMainTabType.SETUP)
        self.tabWidget_main.setTabVisible(PPMMainTabType.EDIT, False)
        self.tabWidget_main.setTabVisible(PPMMainTabType.LIST, False)

    def load_table(self, lineEdit : QLineEdit = None, direct_load: bool=False) -> np.ndarray:

        title = "Error reached while loading 'user-defined transfer impedance' table"
        imported_values = None

        try:
            if direct_load:
                imported_table_path = lineEdit.text()
                imported_values = DataImporter.read_data_in_file(imported_table_path)[0].data

            else:
                imported_data = DataImporter.import_single_file("imported_table_folder",
                        ["csv", "dat", "txt", "xlsx", "xls"], "Choose a table to import the user-defined transfer impedance")
               
                if not imported_data:
                    return
                
                imported_values = imported_data.data
                lineEdit.setText(imported_data.path)

            if imported_values.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have three columns in the form: frequencies, real and imaginary values."
                PrintMessageInput([error_title, title, message])
                return None

            # filter the zero-frequency component
            mask = imported_values[:, 0] > 0
            _imported_values = imported_values[mask, :]

            return _imported_values

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            lineEdit.setFocus()
            return None

    def load_user_defined_transfer_impedance(self):
        self.imported_values = self.load_table(self.lineEdit_user_defined_transfer_impedance_path)

    def save_table_values(self, table_name: str, imported_values: np.ndarray):

        # define the frequencies vector
        _frequencies = imported_values[:, 0]

        if app().project.model.change_analysis_frequency_setup(list(_frequencies)):
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        update_analysis_setup_in_file(_frequencies)

        # real values vector
        real_values = imported_values[:, 1]

        # imaginary values vector
        imag_values = imported_values[:, 2]

        data = np.array([_frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def get_inputs_for_perforated_plate_with_circular_holes(self) -> PerforatedPlateData:

        if self.tabWidget_perforated_plate_models.currentIndex() != PPlateModelsTabType.CIRCULAR_HOLES:
            return
        
        if self.selected_fluid is None:
            self.get_fluid_callback()

        if not isinstance(self.selected_fluid, Fluid):
            return

        lineEdit = self.lineEdit_plate_thickness
        plate_thickness = self.check_inputs(lineEdit, "Plate thickness")
        if plate_thickness is None:
            lineEdit.setFocus()
            return

        lineEdit = self.lineEdit_hole_diameter
        hole_diameter = self.check_inputs(lineEdit, "Hole diameter")
        if hole_diameter is None:
            lineEdit.setFocus()
            return

        lineEdit = self.lineEdit_porosity
        porosity = self.check_inputs(lineEdit, "Porosity")
        if porosity is None:
            lineEdit.setFocus()
            return

        lineEdit = self.lineEdit_linear_discharge_coefficient
        linear_discharge_coefficient = self.check_inputs(lineEdit, "Linear discharge coefficient")
        if linear_discharge_coefficient is None:
            lineEdit.setFocus()
            return
        
        model = PerforatedPlateData()

        pp_data_general = dict(
                                fluid = self.selected_fluid,
                                formulation = "circular_hole",
                                plate_thickness = plate_thickness,
                                hole_diameter = hole_diameter,
                                porosity = porosity,
                                include_effects = self.comboBox_include_effects.currentText(),
                                linear_discharge_coefficient = linear_discharge_coefficient,
                                )

        model.set_general_data(pp_data_general)

        if "Non-linear" in self.comboBox_include_effects.currentText():

            lineEdit = self.lineEdit_non_linear_discharge_coefficient
            non_linear_discharge_coefficient = self.check_inputs(lineEdit, "Non-linear discharge coefficient")
            if non_linear_discharge_coefficient is None:
                lineEdit.setFocus()
                return

            lineEdit = self.lineEdit_non_linear_correction_factor
            non_linear_correction_factor = self.check_inputs(lineEdit, "Non-linear correction factor")
            if non_linear_correction_factor is None:
                lineEdit.setFocus()
                return

            model.set_non_linear_data(non_linear_discharge_coefficient, non_linear_correction_factor)
        
        return model

    def check_selected_surfaces(self):

        surface_ids = []

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.model.check_selected_ids(
            input_ids,
            "surfaces",
            domain="acoustic",
            )

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return []

        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        update_entities_selection(self.lineEdit_selection_id, "surfaces", surface_ids)
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

        if self.check_selection_type(surface_ids):
            return []

        surface_ids.sort()

        return surface_ids

    def map_volumes_to_surfaces(self, surface_ids: list[int]) -> None | dict:

        surfaces_from_volume = defaultdict(list)

        for surface_id in surface_ids:

            message = ""
            volumes_from_surface = self.model.mesh.volumes_from_surface.get(surface_id)

            if volumes_from_surface is None:
                message = "The selected surface is not connected to any volume. "
                message += "You must select an internal surface connected "
                message += "with two volumes to proceed with dofs decoupling."

            elif len(volumes_from_surface) == 1:
                message = "The selected surface is connected to one volume, this means that an external " 
                message += "surface has been selected. You must select an internal surface connected "
                message += "with two volumes to proceed with dofs decoupling."

            if message != "":
                title = "Invalid surface selected"
                PrintMessageInput([warning_title, title, message])
                return

            for volume_id in volumes_from_surface:
                if surface_id in surfaces_from_volume.get(volume_id, []):
                    continue

                surfaces_from_volume[volume_id].append(surface_id)

        # check if there is a common volume touching the selected surfaces
        for vol_id, surf_ids in surfaces_from_volume.items():
            if len(surf_ids) == len(surface_ids):
                return {surf_id : vol_id for surf_id in surface_ids}

        surface_to_volume_map = {}

        # select volumes with reduced number of solid elements to decouple the DOF
        for _surface_id in surface_ids:
            volumes_from_surface = self.model.mesh.volumes_from_surface.get(_surface_id)
            if len(volumes_from_surface) != 2:
                continue

            n_el1 = len(self.mesh.elements_from_volume.get(volumes_from_surface[0]))
            n_el2 = len(self.mesh.elements_from_volume.get(volumes_from_surface[1]))

            vol_id = volumes_from_surface[0] if n_el1 > n_el2 else volumes_from_surface[1]

            surface_to_volume_map[_surface_id] = vol_id

        return surface_to_volume_map

    def apply_callback(self, close_window: bool = False):

        if self.tabWidget_main.currentIndex() != SetupTabType.SETUP:
            return

        surface_ids = self.check_selected_surfaces()
        if not surface_ids:
            return

        self.remove_conflicting_excitations(surface_ids)
        model = self.get_inputs_for_perforated_plate_with_circular_holes()

        if not model:
            return

        volume_to_surface_map = self.map_volumes_to_surfaces(surface_ids)
        if volume_to_surface_map is None:
            return

        for surface_id in surface_ids:
            volume_id = volume_to_surface_map.get(surface_id)
            if volume_id is None:
                continue

            data = {"volume_to_decouple" : volume_id}

            if "User-defined" in self.comboBox_include_effects.currentText():
                self.include_user_defined_transfer_impedance(model, surface_id)

            self.properties._set_property("perforated_plate_model", model.get_data(), surface=surface_id)
            self.properties._set_property("degrees_of_freedom_decoupling", data, surface=surface_id)

        self.assignment_complete = True
        self.clear_line_edit_selection_id()

        self.hide()
        self.actions_to_finalize(close_window)

    def include_user_defined_transfer_impedance(self, model: PerforatedPlateData, surface_id: int | list[int]):

        if self.imported_values is None:
            self.load_user_defined_transfer_impedance()

        if self.imported_values is None:
            return

        if not isinstance(self.imported_values, np.ndarray):
            return

        if self.imported_values.shape[1] < 3:
            return

        if self.imported_values[0, 0] == 0:
            self.imported_values = self.imported_values[1:, :]

        table_name = f"user_defined_transfer_impedance_at_surface_{surface_id}"

        if self.save_table_values(table_name, self.imported_values):
            self.lineEdit_user_defined_transfer_impedance_path.setFocus()
            self.imported_values = None
            return

        # complex values computed from tabular data
        complex_values = get_spectral_data_from_array(self.imported_values)

        # table path from imported tabular data
        table_path = self.lineEdit_user_defined_transfer_impedance_path.text()

        model.set_table_data([table_name], [table_path], [complex_values])

    def remove_conflicting_excitations(self, surface_ids: int | list[int]):

        if isinstance(surface_ids, int):
            surface_ids = [surface_ids]

        labels = [
            "perforated_plate_model", 
            "interior_impedance",
            ]

        for surface_id in surface_ids:
            for label in labels:
                self.properties._remove_surface_property(label, surface_id)

    def remove_all_surface_properties_from_surface(self, new_surface_ids: list[int]):
        if not new_surface_ids:
            return

        surface_properties = deepcopy(self.properties.surface_properties)
        for new_surface_id in new_surface_ids:
            for (property, surf_id) in surface_properties:
                if surf_id == new_surface_id:
                    self.properties._remove_surface_property(property, new_surface_id)

    def remove_all_line_properties_boundind_surface(self, new_surface_ids: list[int]):
        if not new_surface_ids:
            return

        line_properties = deepcopy(self.properties.line_properties)
        for new_surface_id in new_surface_ids:
            lines_from_surface = self.mesh.lines_from_surface.get(new_surface_id)
            if lines_from_surface is None:
                continue

            for line_from_surface in lines_from_surface:
                for (property, line_id) in line_properties:
                    if line_from_surface == line_id:
                        self.properties._remove_line_property(property, line_id)

    def remove_callback(self):
        input_ids = self.get_selected_surfaces_from_tree_widget_perforated_plate_model()

        if not input_ids:
            return

        surface_ids, error_data = self.model.check_selected_ids(
            input_ids,
            "surfaces",
            domain="acoustic",
            )

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        for surface_id in surface_ids:
            self.properties._remove_surface_property("perforated_plate_model", surface_id)

            data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_id)
            if isinstance(data, dict):
                new_surface_id = data.get("new_surface_id")
                if isinstance(new_surface_id, int):   
                    self.remove_all_surface_properties_from_surface([new_surface_id])
                    self.remove_all_line_properties_boundind_surface([new_surface_id]) 

                self.properties._remove_surface_property("degrees_of_freedom_decoupling", surface_id)
        
        self.clear_line_edit_selection_id()
        self.pushButton_remove.setDisabled(True)

        self.hide()
        self.actions_to_finalize()
        self.restore_mesh_data_modified_by_decoupling()
        app().main_window.selection.clear_selection()

    def reset_callback(self):

        surface_ids = []
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "perforated_plate_model":
                surface_ids.append(surface_id)

        if not surface_ids:
            return

        title = "Perforated plate model reset"
        message = "Would you like to remove the perforated plate from the acoustic model?"

        buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        new_surface_ids = []
        for surf_id in surface_ids:
            data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surf_id)
            if isinstance(data, dict):
                new_surface_id = data.get("new_surface_id")
                if isinstance(new_surface_id, int):
                    new_surface_ids.append(new_surface_id)
    
                self.properties._remove_surface_property("degrees_of_freedom_decoupling", surf_id)

        self.remove_all_surface_properties_from_surface(new_surface_ids)
        self.remove_all_line_properties_boundind_surface(new_surface_ids)
        self.properties._reset_property("perforated_plate_model")

        self.actions_to_finalize()
        self.restore_mesh_data_modified_by_decoupling()

    def actions_to_finalize(self, close_window: bool = False):

        def callback():

            logging.info("Processing the post-assignment actions... [10/100]")
            self.load_model_info()

            logging.info("Processing the post-assignment actions... [20/100]")
            app().main_window.analysis_toolbar.reset_solution()

            logging.info("Processing the post-assignment actions... [30/100]")
            app().project.project_writer.delete_mesh_data()

            logging.info("Processing the post-assignment actions... [60/100]")
            app().project.update_model_properties_file()

            logging.info("Processing the post-assignment actions... [80/100]")
            app().main_window.update_info_text()

            logging.info("Processing the post-assignment actions... [90/100]")
            app().main_window.update_symbols()

            logging.info("Processing the post-assignment actions... [95/100]")
            app().main_window.selection.set_geometry_selection()

        LoadingWindow(callback).run()

        if close_window:
            self.close()

    def process_decoupling_actions(self):

        def callback():
            logging.info("Processing degress of freedom decoupling... [10/100]")
            self.model.process_degrees_of_freedom_decoupling()

            logging.info("Processing degress of freedom decoupling... [70/100]")
            app().project.write_to_working_dir()

            # the degrees of freedom modifies the surfaces properties
            logging.info("Processing degress of freedom decoupling... [80/100]")
            app().project.update_model_properties_file()

            logging.info("Processing degress of freedom decoupling... [85/100]")
            app().main_window.update_mesh_information()

            logging.info("Processing degress of freedom decoupling... [90/100]")
            app().main_window.update_geometry_information()

            logging.info("Processing degress of freedom decoupling... [92/100]")
            app().project.model.mesh.process_disconnected_nodes_criterion()

            logging.info("Processing degress of freedom decoupling... [95/100]")
            app().main_window.update_plots()

        LoadingWindow(callback).run()

    def restore_mesh_data_modified_by_decoupling(self):

        if self.mesh.cache_nodal_coordinates is None:
            return

        self.mesh.restore_data_from_cache()
        self.mesh.process_upwards_adjacencies_from_entities()

        # if self.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):
        #     self.mesh.cache_mesh_information()

        self.process_decoupling_actions()

    def check_inputs(self, lineEdit: QLineEdit, label, _float=True):

        self.stop = False
        message = ""

        title = "Invalid value typed"
        input_str = lineEdit.text()

        if input_str != "":

            input_str = input_str.replace(",", ".")

            try:
                if _float:
                    out = float(input_str)
                else:
                    out = int(input_str)

                if out <= 0:
                    message = f"Insert a positive value to the {label}."
                    message += "\n\nNote: zero value is not allowed."

            except Exception as _err:
                message = f"You have typed an invalid value at the {label} input field.\n\n"
                message += str(_err)

        else:
            message = f"Insert some value at the {label} input field."

        if message != "":
            PrintMessageInput([error_title, title, message])
            return None
        else:
            return out

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
            self.lineEdit_fluid_identifier.setText(f"{self.selected_fluid.identifier}")
            self.lineEdit_fluid_density.setText(f"{self.selected_fluid.fluid_density}")
            self.lineEdit_speed_of_sound.setText(f"{self.selected_fluid.speed_of_sound}")

    def get_perforated_plate_impendance(self, fluid: Fluid):

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

        model = PerforatedPlateModels(self.model)

        pp_data = None
        pp_data = self.get_inputs_for_perforated_plate_with_circular_holes()

        if pp_data is None:
            return None, None
        
        U_rms = 0
        normalized_impedances = model.get_transfer_impedance_for_circular_holes(omega, pp_data.get_data())
        if normalized_impedances is None:
            return None, None

        z_orifice, z_end, z_nl_urms, z_ud, Z_0 = normalized_impedances
        Z_tr = Z_0 * (z_orifice + z_end + z_ud + z_nl_urms*U_rms)

        return freq, Z_tr
    
    def get_perforated_plate_model(self):
        tab_index = self.tabWidget_main.currentIndex()
        
        if tab_index == PPMMainTabType.SETUP:
            return "circular hole"

    def plot_data_callback(self):
        plot_key = self.comboBox_plot_type.currentIndex()
        if plot_key == PlotTypeBoxType.ACOUSTIC_IMPEDANCE:
            self.plot_perforated_plate_impedance()

    def plot_perforated_plate_impedance(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        if self.selected_fluid is None:
            return

        freq, Z_tr = self.get_perforated_plate_impendance(self.selected_fluid)

        if freq is None:
            return

        pp_model = self.get_perforated_plate_model()
        self.plot_data(freq, Z_tr, "Acoustic transfer impedance", pp_model)

    def join_model_data(self, x_data, y_data, label: str, section_label: str):

        self.hide()
        self.data_to_plot = dict()

        y_label = label
        unit_label = "kg/m².s"

        legend_label = label
        title = f"{label} for {section_label}"

        key = ("property", (None))

        self.data_to_plot[key] = { 
                                    "x_data" : x_data,
                                    "y_data" : y_data,
                                    "x_label" : "Frequency [Hz]",
                                    "y_label" : y_label,
                                    "title" : title,
                                    "data_type" : f"effective fluid properties for {section_label}",
                                    "legend" : legend_label,
                                    "unit" : unit_label,
                                    "color" : [0,0,1],
                                    "linestyle" : "-"
                                   }

    def plot_data(self, x_data, y_data, label, pm_label):
        self.join_model_data(x_data, y_data, label, pm_label)
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.data_to_plot)
    
    def process_degress_of_freedom_decoupling(self):

        if not self.assignment_complete:
            return False
        
        if not self.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):
            return False

        if not app().project.model.is_there_a_valid_mesh():
            self.hide()
            app().main_window.input_ui.mesh_setup()
            app().main_window.set_input_widget(self)
            return False

        if self.mesh.cache_nodal_coordinates is None:
            # self.mesh.cache_mesh_information()
            pass

        else:
            self.mesh.restore_data_from_cache()
            self.mesh.process_upwards_adjacencies_from_entities()
            # self.mesh.cache_mesh_information()

        self.process_decoupling_actions()

        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Control:
            self.treeWidget_perforated_plate_model.setSelectionMode(QAbstractItemView.MultiSelection)
        elif event.key() == Qt.Key_Shift:
            self.treeWidget_perforated_plate_model.setSelectionMode(QAbstractItemView.ContiguousSelection)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.treeWidget_perforated_plate_model.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        self.hide()

        try:
            warnings.filterwarnings('default')
        except TypeError:
            pass

        if self.process_degress_of_freedom_decoupling():
            return

        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)

        return super().closeEvent(a0)