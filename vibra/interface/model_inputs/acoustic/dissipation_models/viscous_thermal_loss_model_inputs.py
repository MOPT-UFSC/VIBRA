import warnings
from collections import defaultdict
from enum import IntEnum

import numpy as np
from PySide6.QtCore import QItemSelectionModel, QPoint, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QTreeWidgetItem

from vibra import app
from vibra.engine.dissipation_models.viscous_thermal_loss_models import ViscousThermalLossModels
from vibra.engine.properties.fluid import Fluid
from vibra.interface import error_title
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.acoustic.definitions.enums import AttributionBodiesType, PlotTypesTab
from vibra.interface.model_inputs.acoustic.dissipation_models.circular_duct_data import CircularDuctData
from vibra.interface.model_inputs.acoustic.dissipation_models.rectangular_duct_data import RectangularDuctData
from vibra.interface.model_inputs.fluid.set_fluid_inputs_simplified import SetFluidInputsSimplified
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.ui_generated.model.acoustic.dissipation_models.viscous_thermal_model_inputs_ui import ViscousThermalModelInputs_UI


class TabType(IntEnum):
    RECTANGULAR = 0
    CIRCULAR = 1
    EDIT = 2
    LIST = 3


class SectionType(IntEnum):
    RECTANGULAR = 0
    QUADRANGULAR = 1
    NARROW_SLIT = 2


class FormulationModelTab(IntEnum):
    STINSON_MODEL = 0
    LRF_MODEL = 1


class ViscousThermalLossModelInputs(ViscousThermalModelInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()
        app().main_window.selection.volume_selection_mode = True

        self._initialize()
        self._config_window()
        self._create_connections()
        self.load_info()

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
        self.selected_fluid = None
        self.keep_window_open = True
        self.material_model_data = dict()
        self.models: list[RectangularDuctData | CircularDuctData] = []
        self.last_tab = self.tabWidget_main.currentIndex()
        self.tree_item_clicked = False

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_section_type.currentIndexChanged.connect(self.rectangular_section_type_callback)
        self.comboBox_plot_type.currentIndexChanged.connect(self.plot_type_callback)
        #
        self.lineEdit_width_rectangular.textChanged.connect(self.update_rectangular_duct_area)
        self.lineEdit_height_rectangular.textChanged.connect(self.update_rectangular_duct_area)
        self.lineEdit_diameter_circular.textChanged.connect(self.update_circular_duct_area)
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.tableWidget_rectangular.cellChanged.connect(lambda row, column: self.cell_changed_callback(row, column, "rectangular"))
        self.tableWidget_circular.cellChanged.connect(lambda row, column: self.cell_changed_callback(row, column, "circular"))
        #
        self.treeWidget_viscous_thermal_model.itemClicked.connect(self.on_click_item)
        self.treeWidget_viscous_thermal_model.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.geometry_selection_callback()
        self.attribution_type_callback()
        self.update_plot_buttons_access()

    def geometry_selection_callback(self):
        if self.tabWidget_main.currentIndex() == TabType.LIST:
            self.verify_if_selected_volumes_are_in_tree_widget_viscous_thermal_model()
            return

        volumes = app().main_window.selection.geometry_volumes
        if not volumes:
            return

        text = ", ".join([str(i) for i in volumes])
        self.lineEdit_selection_id.setText(text)
        if self.comboBox_attribution_type.currentIndex() != AttributionBodiesType.SELECTED_BODIES:
            self.comboBox_attribution_type.setCurrentIndex(AttributionBodiesType.SELECTED_BODIES)

        if self.tabWidget_main.currentIndex() != TabType.CIRCULAR:
            return
        
        self.load_diameter_from_selected_volumes(volumes)

    def actions_to_finalize(self, close_window: bool = False):
        self.load_info()
        app().project.update_model_properties_file()
        app().main_window.update_symbols()

        if close_window:
            self.close()

    def update_plot_buttons_access(self):
        state = self.selected_fluid is None
        self.comboBox_plot_type.setDisabled(state)
        self.pushButton_plot_data.setDisabled(state)
        self.plot_type_callback()

    def plot_type_callback(self):
        if self.comboBox_plot_type.currentIndex() < PlotTypesTab.SURFACE_IMPEDANCE:
            self.doubleSpinBox_evaluated_depth.setDisabled(True)
        else:
            self.doubleSpinBox_evaluated_depth.setDisabled(False)

    def update_rectangular_duct_area(self):
        try:
            height = float(self.lineEdit_height_rectangular.text())
            if self.comboBox_section_type.currentIndex() == SectionType.QUADRANGULAR:
                self.lineEdit_width_rectangular.setText(f"{round(height, 6)}")
            width = float(self.lineEdit_width_rectangular.text())
            area = width * height
            self.lineEdit_area_rectangular.setText(f"{round(area, 6)}")
        except Exception:
            self.lineEdit_area_rectangular.setText("--")

    def update_circular_duct_area(self):
        try:
            diameter = float(self.lineEdit_diameter_circular.text())
            area = (np.pi / 4) * (diameter**2)
            self.lineEdit_radius_circular.setText(f"{round(diameter / 2, 6)}")
            self.lineEdit_area_circular.setText(f"{round(area, 6)}")
        except Exception:
            self.lineEdit_area_circular.setText("--")

    def remove_callback(self):
        selected_items = self.treeWidget_viscous_thermal_model.selectedItems()

        if not selected_items:
            return

        for item in selected_items:
            selection_id = int(item.text(0))
            model_id = int(item.text(1))
            model = self.map_model_id_to_models[model_id]

            self.properties._remove_volume_property("viscous_thermal_model", selection_id)

            if len(self.map_model_id_to_volumes[model_id]) == 1:
                self.models.remove(model)

        self.pushButton_remove.setDisabled(True)
        self.clear_line_edit_selection_id()

        app().main_window.selection.clear_selection()
        self.actions_to_finalize()

        if self.map_model_id_to_volumes:
            self.tabWidget_main.setCurrentIndex(TabType.LIST)

    def reset_callback(self):

        title = "Viscous-thermal dissipation model reset"
        message = "Would you like to remove the Viscous-thermal dissipation effects from the model?"

        buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            self.properties._reset_property("viscous_thermal_model")

        self.models.clear()
        self.actions_to_finalize()

    def tab_event_callback(self):
        current_tab = self.tabWidget_main.currentIndex()
        for index in (self.last_tab, current_tab):
            if index in [TabType.LIST, TabType.EDIT]:
                app().main_window.selection.clear_selection()
                self.clear_line_edit_selection_id()
    
        self.last_tab = current_tab
        list_or_edit_tab = current_tab in [TabType.LIST, TabType.EDIT]

        self.pushButton_apply.setDisabled(list_or_edit_tab)
        self.pushButton_apply_and_close.setDisabled(list_or_edit_tab)

        if current_tab == TabType.EDIT:
            self.comboBox_attribution_type.setCurrentIndex(AttributionBodiesType.SELECTED_BODIES)
            self.comboBox_attribution_type.setDisabled(True)
            self.lineEdit_selection_id.setDisabled(True)
            self.frame_fluid_info.setDisabled(True)
            self.frame_plot_buttons.setDisabled(True)

        elif current_tab == TabType.LIST:
            self.pushButton_remove.setDisabled(True)
            self.lineEdit_selection_id.setDisabled(True)
            self.treeWidget_viscous_thermal_model.clearSelection()

        else:

            if self.tabWidget_main.currentIndex() == TabType.CIRCULAR:
                volumes = app().main_window.selection.geometry_volumes
                if volumes:
                    self.load_diameter_from_selected_volumes(volumes)

            current_index = self.comboBox_attribution_type.currentIndex()
            self.comboBox_attribution_type.currentIndexChanged.emit(current_index)

            self.frame_fluid_info.setDisabled(False)
            self.frame_plot_buttons.setDisabled(False)

            self.comboBox_attribution_type.setDisabled(False)
            if self.comboBox_attribution_type.currentIndex() == AttributionBodiesType.ALL_BODIES:
                return

            self.lineEdit_selection_id.setDisabled(False)

    def on_click_item(self, item):
        self.tree_item_clicked = True

        volume_ids = self.get_selected_volumes_from_tree_widget_viscous_thermal_model()
        if not volume_ids:
            return

        app().main_window.selection.set_geometry_selection(volumes=volume_ids)

        self.set_selection_text(volume_ids)
        self.pushButton_remove.setEnabled(True)

        self.tree_item_clicked = False

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def get_selected_volumes_from_tree_widget_viscous_thermal_model(self) -> list:
        selected_items = self.treeWidget_viscous_thermal_model.selectedItems()

        if not selected_items:
            return []

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

    def rectangular_section_type_callback(self):

        section_index = self.comboBox_section_type.currentIndex()

        if section_index in [SectionType.QUADRANGULAR, SectionType.NARROW_SLIT]:
            self.lineEdit_width_rectangular.setDisabled(True)
            if section_index == SectionType.NARROW_SLIT:
                self.spinBox_number_of_terms.setDisabled(True)
                self.lineEdit_width_rectangular.setText("2*a >> 2*b")
            else:
                self.spinBox_number_of_terms.setEnabled(True)
                height = self.lineEdit_height_rectangular.text()
                self.lineEdit_width_rectangular.setText(height)

        else:
            self.spinBox_number_of_terms.setEnabled(True)
            self.lineEdit_width_rectangular.setDisabled(False)

            self.lineEdit_width_rectangular.setText("")

    def attribution_type_callback(self):

        attribution_type = self.comboBox_attribution_type.currentIndex()
        if attribution_type == AttributionBodiesType.ALL_BODIES:
            self.lineEdit_selection_id.setText("All bodies")

        elif attribution_type == AttributionBodiesType.SELECTED_BODIES:
            volumes = app().main_window.selection.geometry_volumes
            if not volumes:
                self.lineEdit_selection_id.setText("")

            self.lineEdit_selection_id.setEnabled(True)
            self.label_12.setDisabled(False)

    def cell_changed_callback(self, row: int, column: int, section_type: str):
        item = None
        model_id = None

        if section_type == "rectangular":
            item = self.tableWidget_rectangular.item(row, column)
            model_id = int(self.tableWidget_rectangular.item(0, column).text())

        else:
            item = self.tableWidget_circular.item(row, column)
            model_id = int(self.tableWidget_circular.item(0, column).text())

        new_parameter_value = None
        value_error = False

        model = self.map_model_id_to_models[model_id]
        parameters_positions = model.get_parameters_position()
        parameter_position = row - 1
        parameter = parameters_positions[parameter_position]

        try:
            if parameter == "number_of_terms":
                new_parameter_value = int(float(item.text()))
                item.setText(str(new_parameter_value))
            else:
                new_parameter_value = float(item.text())
        except Exception:
            value_error = True

        if value_error:
            new_parameter_value = getattr(model, parameter)
            item.setText(str(new_parameter_value))
        else:
            setattr(model, parameter, new_parameter_value)

            model_data = model.get_data()

            if model_id in self.map_model_id_to_volumes:
                volumes = self.map_model_id_to_volumes[model_id]

                for volume in volumes:
                    self.properties._set_property("viscous_thermal_model", model_data, volume=volume)

            app().project.update_model_properties_file()

    def map_existing_viscous_thermal_loss_models(self):
        self.map_model_id_to_models: defaultdict[int, RectangularDuctData | CircularDuctData] = defaultdict()
        self.map_model_id_to_volumes: defaultdict[int, list[int]] = defaultdict(list)

        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "viscous_thermal_model":
                model = None
                section_type = data["section_type"]

                if section_type in ["Rectangular duct", "Quadrangular duct", "Narrow slit duct"]:
                    model = RectangularDuctData.set_data(data)
                else:
                    model = CircularDuctData.set_data(data)

                if model not in self.models:
                    self.models.append(model)

                model_id = self.models.index(model) + 1
                self.map_model_id_to_models[model_id] = model
                self.map_model_id_to_volumes[model_id].append(volume_id)

    def update_viscous_thermall_loss_tree_widget(self):
        self.treeWidget_viscous_thermal_model.clear()
        self.treeWidget_viscous_thermal_model.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for model_id, volumes_ids in self.map_model_id_to_volumes.items():
            for volume_id in volumes_ids:
                new = QTreeWidgetItem([str(volume_id), str(model_id)])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_viscous_thermal_model.addTopLevelItem(new)

    def configure_tables_and_tabs_widgets(self):
        rectangular_duct_counter = 0
        circular_duct_counter = 0

        for model in self.map_model_id_to_models.values():
            if isinstance(model, RectangularDuctData):
                rectangular_duct_counter += 1
            else:
                circular_duct_counter += 1

        self.tableWidget_rectangular.clearContents()
        self.tableWidget_rectangular.blockSignals(True)
        self.tableWidget_rectangular.setRowCount(6)
        self.tableWidget_rectangular.setColumnCount(rectangular_duct_counter)

        self.tableWidget_circular.clearContents()
        self.tableWidget_circular.blockSignals(True)
        self.tableWidget_circular.setRowCount(4)
        self.tableWidget_circular.setColumnCount(circular_duct_counter)

        self.tabWidget_main.setTabVisible(TabType.EDIT, False)
        self.tabWidget_main.setTabVisible(TabType.LIST, False)

        self.tabWidget_models.setTabVisible(TabType.RECTANGULAR, False)
        self.tabWidget_models.setTabVisible(TabType.CIRCULAR, False)

    def update_tableWidget_rectangular_items(self):
        for i in range(self.tableWidget_rectangular.rowCount()):
            for j in range(self.tableWidget_rectangular.columnCount()):
                item = self.tableWidget_rectangular.item(i, j)

                if item is None:
                    item = QTableWidgetItem()
                    self.tableWidget_rectangular.setItem(i, j, item)
                    item.setFlags(Qt.ItemIsSelectable)

                item.setTextAlignment(Qt.AlignCenter)

        self.tableWidget_rectangular.blockSignals(False)

    def update_tableWidget_circular_items(self):
        for i in range(self.tableWidget_circular.rowCount()):
            for j in range(self.tableWidget_circular.columnCount()):
                item = self.tableWidget_circular.item(i, j)

                if item is None:
                    item = QTableWidgetItem()
                    self.tableWidget_circular.setItem(i, j, item)
                    item.setFlags(Qt.ItemIsSelectable)

                item.setTextAlignment(Qt.AlignCenter)

        self.tableWidget_circular.blockSignals(False)

    def update_edit_tab_widget(self):
        rectangular_counter = 0
        circular_counter = 0

        is_there_rectangular_model = False
        is_there_circular_model = False

        model_ids = []
        for model_id in self.map_model_id_to_models:
            model_ids.append(model_id)

        model_ids.sort()

        for model_id in model_ids:
            model_id_item = QTableWidgetItem(str(model_id))
            model_id_item.setFlags(Qt.ItemIsSelectable)

            model = self.map_model_id_to_models[model_id]
            model_data = model.get_data()

            if isinstance(model, RectangularDuctData):
                self.tableWidget_rectangular.setItem(0, rectangular_counter, model_id_item)

                for i, data in enumerate(model_data.values()):
                    if data is None:
                        data = "---"

                    item = QTableWidgetItem(str(data))
                    if isinstance(data, str):
                        item.setFlags(Qt.ItemIsSelectable)

                    self.tableWidget_rectangular.setItem(i + 1, rectangular_counter, item)

                rectangular_counter += 1
                is_there_rectangular_model = True

            else:
                self.tableWidget_circular.setItem(0, circular_counter, model_id_item)

                for i, data in enumerate(model_data.values()):
                    item = QTableWidgetItem(str(data))
                    if isinstance(data, str):
                        item.setFlags(Qt.ItemIsSelectable)

                    self.tableWidget_circular.setItem(i + 1, circular_counter, item)

                circular_counter += 1
                is_there_circular_model = True

            if is_there_rectangular_model or is_there_circular_model:
                self.tabWidget_main.setTabVisible(TabType.EDIT, True)
                self.tabWidget_main.setTabVisible(TabType.LIST, True)
                self.tabWidget_main.setCurrentIndex(TabType.EDIT)

            if is_there_rectangular_model:
                self.tabWidget_models.setTabVisible(TabType.RECTANGULAR, True)

            if is_there_circular_model:
                self.tabWidget_models.setTabVisible(TabType.CIRCULAR, True)

    def load_info(self):
        self.map_existing_viscous_thermal_loss_models()

        self.configure_tables_and_tabs_widgets()
        self.update_edit_tab_widget()

        self.update_viscous_thermall_loss_tree_widget()
        self.update_tabs_visibility()

        self.update_tableWidget_rectangular_items()
        self.update_tableWidget_circular_items()

    def update_tabs_visibility(self):

        for key in self.properties.volume_properties:
            property, _ = key
            if property != "viscous_thermal_model":
                continue

            self.tabWidget_main.setTabVisible(TabType.EDIT, True)
            return

        self.tabWidget_main.setTabVisible(TabType.EDIT, False)
        self.tabWidget_main.setCurrentIndex(TabType.RECTANGULAR)

    def load_diameter_from_selected_volumes(self, volume_ids: list[int]):
        if not volume_ids:
            return

        surfaces_from_volumes = self.get_surfaces_from_selected_volumes(volume_ids)
        diameters = self.get_diameters_from_surfaces(surfaces_from_volumes)

        if len(diameters) == 1:
            self.lineEdit_diameter_circular.setText(f"{diameters[0]}")

    def get_surfaces_from_selected_volumes(self, volume_ids: list[int]):
        surfaces_from_volumes = []
        for volume_id in volume_ids:
            for surface_id in self.mesh.surfaces_from_volume.get(volume_id):
                if surface_id is None:
                    continue

                if surface_id in surfaces_from_volumes:
                    continue

                surfaces_from_volumes.append(surface_id)
        
        return surfaces_from_volumes

    def get_diameters_from_surfaces(self, surface_ids: list[int]):
        diameters = []
        for surface_id in surface_ids:
            diameter = self.mesh.cylindrical_surfaces_data.get(surface_id)
            if diameter is None:
                continue
            
            _diameter = round(diameter, 6)
            if _diameter in diameters:
                continue

            diameters.append(_diameter)

        return diameters

    def verify_if_selected_volumes_are_in_tree_widget_viscous_thermal_model(self):
        if self.tree_item_clicked:
            return

        selected_volumes = app().main_window.selection.geometry_volumes

        if not selected_volumes:
            return

        self.clear_line_edit_selection_id()
        self.treeWidget_viscous_thermal_model.clearSelection()
        self.pushButton_remove.setDisabled(True)

        map_id_to_model_index = self.get_tree_widget_viscous_thermal_model_items_map()
        selected_ids = set(map_id_to_model_index.keys())
        selected_volumes_in_tree_widget = selected_volumes.intersection(selected_ids)

        if not selected_volumes_in_tree_widget:
            return

        self.pushButton_remove.setEnabled(True)

        model_selector = self.treeWidget_viscous_thermal_model.selectionModel()

        for volume_id in selected_volumes_in_tree_widget:
            model_index = map_id_to_model_index[volume_id]

            model_selector.select(model_index, QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)

        self.treeWidget_viscous_thermal_model.setSelectionMode(QAbstractItemView.SingleSelection)
        self.set_selection_text(selected_volumes_in_tree_widget)

    def get_tree_widget_viscous_thermal_model_items_map(self) -> dict:
        map_id_to_model_index = dict()

        index = self.treeWidget_viscous_thermal_model.indexAt(QPoint(0, 0))
        while index.isValid():
            item = self.treeWidget_viscous_thermal_model.itemFromIndex(index)
            volume_id = int(item.text(0))

            map_id_to_model_index[volume_id] = index

            index = self.treeWidget_viscous_thermal_model.indexBelow(index)

        return map_id_to_model_index

    def get_rectangular_duct_inputs(self) -> RectangularDuctData:

        section_type = self.comboBox_section_type.currentIndex()

        if section_type in [SectionType.RECTANGULAR, SectionType.QUADRANGULAR]:
            lineEdit = self.lineEdit_width_rectangular
            width, stop = self.check_inputs(lineEdit, "Width (rectangular duct)")
            if stop:
                lineEdit.setFocus()
                return dict()

        lineEdit = self.lineEdit_height_rectangular
        height, stop = self.check_inputs(lineEdit, "Height (rectangular duct)")
        if stop:
            lineEdit.setFocus()
            return dict()

        section_types = ["Rectangular duct", "Quadrangular duct", "Narrow slit duct"]

        if section_type in [SectionType.RECTANGULAR, SectionType.QUADRANGULAR]:
            model_data = RectangularDuctData(section_types[section_type], "Stinson model", height, width, self.spinBox_number_of_terms.value())

        else:
            model_data = RectangularDuctData(section_types[section_type], "Stinson model", height, None, None)

        return model_data

    def get_circular_duct_inputs(self) -> CircularDuctData:

        lineEdit = self.lineEdit_diameter_circular
        diameter, stop = self.check_inputs(lineEdit, "Diameter (circular duct)")
        if stop:
            lineEdit.setFocus()
            return dict()

        if self.comboBox_formulation.currentIndex() == FormulationModelTab.STINSON_MODEL:
            formulation = "Stinson model"
        else:
            formulation = "LRF model"

        return CircularDuctData("Circular duct", formulation, diameter)

    def apply_callback(self, close_window: bool = False):

        model = None
        if self.tabWidget_main.currentIndex() == TabType.RECTANGULAR:
            model = self.get_rectangular_duct_inputs()

        elif self.tabWidget_main.currentIndex() == TabType.CIRCULAR:
            model = self.get_circular_duct_inputs()

        if not model:
            return

        assignment_type = self.comboBox_attribution_type.currentIndex()

        if assignment_type in [AttributionBodiesType.ALL_BODIES, AttributionBodiesType.SELECTED_BODIES]:
            volume_ids = []
            if assignment_type == AttributionBodiesType.ALL_BODIES:
                self.models = []

                if "volumes" in self.mesh.geometry_information:
                    volume_ids = self.mesh.geometry_information["volumes"]

            else:
                input_ids = self.lineEdit_selection_id.text()
                volume_ids, error_data = self.model.check_selected_ids(
                    input_ids,
                    "volumes",
                    domain="acoustic",
                )

                if error_data is not None:
                    self.lineEdit_selection_id.setFocus()
                    PrintMessageInput(error_data)
                    return

                self.verify_and_remove_model_conflicts_if_it_exists(volume_ids)

            if model not in self.models:
                self.models.append(model)

            model_data = model.get_data()

            for volume_id in volume_ids:
                self.properties._set_property("viscous_thermal_model", model_data, volume=volume_id)
        
        self.actions_to_finalize(close_window)

    def verify_and_remove_model_conflicts_if_it_exists(self, volume_ids: list[int] = None):
        for volume_id in volume_ids:
            for model_id, volumes in self.map_model_id_to_volumes.items():
                if volume_id in volumes and len(volumes) == 1:
                    model = self.map_model_id_to_models[model_id]
                    self.models.remove(model)

    def check_inputs(self, lineEdit, label, _float=True):

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
            return None, True
        else:
            return out, False

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

        warnings.filterwarnings("ignore")

        frequencies = app().project.model.frequencies
        if frequencies is None:
            df = 5
            f_min = 5
            f_max = 1400
            frequencies = np.arange(f_min, f_max + df, df)

        if frequencies[0] == 0:
            freq = frequencies[1:]
        else:
            freq = frequencies

        # frequencies vector in radians
        omega = 2 * np.pi * freq

        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == TabType.RECTANGULAR:
            tv_data = self.get_rectangular_duct_inputs()

        elif tab_index == TabType.CIRCULAR:
            tv_data = self.get_circular_duct_inputs()

        if tv_data:
            model = ViscousThermalLossModels(self)

            if tab_index == TabType.RECTANGULAR:
                if self.comboBox_section_type.currentIndex() in [AttributionBodiesType.ALL_BODIES, AttributionBodiesType.SELECTED_BODIES]:
                    rho_eff, C_eff = model.get_rectangular_section_effective_properties(omega, fluid, tv_data)

                else:
                    rho_eff, C_eff = model.get_narrow_slit_section_effective_properties(omega, fluid, tv_data)

            elif tab_index == TabType.CIRCULAR:
                if self.comboBox_formulation.currentIndex() == FormulationModelTab.STINSON_MODEL:
                    rho_eff, C_eff = model.get_circular_section_effective_properties_for_Stinson_model(omega, fluid, tv_data)
                else:
                    rho_eff, C_eff = model.get_circular_section_effective_properties_for_LRF_model(omega, fluid, tv_data)

            k_cr = omega / C_eff

            return freq, rho_eff, C_eff, k_cr

        return None, None, None, None

    def get_viscous_thermal_loss_model(self):
        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == TabType.RECTANGULAR:
            section_index = self.comboBox_section_type.currentIndex()
            if section_index == SectionType.RECTANGULAR:
                return "Rectangular duct"
            elif section_index == SectionType.QUADRANGULAR:
                return "Quadrangular duct"
            else:
                return "Narrow slit duct"

        elif tab_index == TabType.CIRCULAR:
            return "Circular duct"

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

        tv_model = self.get_viscous_thermal_loss_model()
        self.plot_data(freq, rho_eff, "effective fluid density", tv_model)

    def plot_effective_speed_of_sound(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        freq, _, C_eff, _ = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        tv_model = self.get_viscous_thermal_loss_model()
        self.plot_data(freq, C_eff, "effective speed of sound", tv_model)

    def plot_surface_impedance(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        h = self.spinBox_number_of_terms.value()
        Z_0 = self.selected_fluid.speed_of_sound * self.selected_fluid.fluid_density

        freq, rho_eff, C_eff, k_cr = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        Z_pm = rho_eff * C_eff
        Z_s = Z_pm * (1 / np.tanh(k_cr * h))
        Z_norm = Z_s / Z_0

        tv_model = self.get_viscous_thermal_loss_model()
        self.plot_data(freq, Z_norm, "normalized surface impedance", tv_model)

    def plot_absorption_coefficient(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        h = self.spinBox_number_of_terms.value()
        Z_0 = self.selected_fluid.speed_of_sound * self.selected_fluid.fluid_density

        freq, rho_eff, C_eff, k_cr = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        Z_pm = rho_eff * C_eff
        Z_s = Z_pm * (1 / np.tanh(k_cr * h))

        R_r = (Z_s - Z_0) / (Z_s + Z_0)
        alpha_n = 1 - np.abs(R_r) ** 2

        pm_model = self.get_viscous_thermal_loss_model()
        self.plot_data(freq, alpha_n, "absorption coefficient", pm_model)

    def join_model_data(self, x_data, y_data, label: str, section_label: str):

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
        title = f"Effective Properties for {section_label}"

        key = ("property", (None))

        self.data_to_plot[key] = {
            "x_data": x_data,
            "y_data": y_data,
            "x_label": "Frequency [Hz]",
            "y_label": y_label,
            "title": title,
            "data_type": f"effective fluid properties for {section_label}",
            "legend": legend_label,
            "unit": unit_label,
            "color": [0, 0, 1],
            "linestyle": "-",
        }

    def plot_data(self, x_data, y_data, label, pm_label):
        self.join_model_data(x_data, y_data, label, pm_label)
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.data_to_plot)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Control:
            self.treeWidget_viscous_thermal_model.setSelectionMode(QAbstractItemView.MultiSelection)
        elif event.key() == Qt.Key_Shift:
            self.treeWidget_viscous_thermal_model.setSelectionMode(QAbstractItemView.ContiguousSelection)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.treeWidget_viscous_thermal_model.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection.volume_selection_mode = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)
