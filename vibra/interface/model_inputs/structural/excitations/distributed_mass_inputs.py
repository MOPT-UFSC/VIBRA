
from collections import defaultdict
from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.interface import error_title
from vibra.interface.common.common_interface import update_entities_selection
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.ui_generated.model.structural.excitations.distributed_mass_inputs_ui import DistributedMassInputs_UI


class TabType(IntEnum):
    CONSTANT_DATA = 0
    LIST = 1


class AssignmentType(IntEnum):
    SURFACES = 0
    LINES = 1
    MULTIPLE = 2


class DistributedMassInputs(DistributedMassInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._configure_validators()
        self._create_connections()

        self._config_widgets()
        self.geometry_selection_callback()
        self.load_model_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.keep_window_open = True
        self.element_types = ["2d_element", "3d_element"]

    def _configure_validators(self):
        self.lineEdit_mass_to_distribute.setValidator(StrictDoubleValidator(1e-16, 1e16, 8))

    def _config_widgets(self):

        self.comboBox_element_type.setEnabled(False)
        self.treeWidget_distributed_mass.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        for i, w in enumerate([80, 120, 100]):
            self.treeWidget_distributed_mass.setColumnWidth(i, w)
            self.treeWidget_distributed_mass.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):

        # QComboBox connections
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_callback)

        # QPushButtons connetions
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)

        # QTabWidget connections
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)

        # QTreeWidget connections
        self.treeWidget_distributed_mass.itemClicked.connect(self.item_clicked_callback)
        self.treeWidget_distributed_mass.itemDoubleClicked.connect(self.item_double_clicked_callback)
        self.treeWidget_distributed_mass.itemSelectionChanged.connect(self.item_selection_clicked_callback)

        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        self.update_element_type_based_on_geometry_information()

    def geometry_selection_callback(self):

        lines = app().main_window.selection.geometry_lines
        surfaces = app().main_window.selection.geometry_surfaces

        if self.tabWidget_main.currentIndex() == TabType.LIST and (lines and surfaces):
            self.lineEdit_selection_id.setText("mult. entities")
            self.comboBox_assignment_type.setEnabled(False)
            self.comboBox_assignment_type.setCurrentIndex(AssignmentType.MULTIPLE)
            view = self.comboBox_assignment_type.view()
            view.setRowHidden(2, False)
            return

        self.comboBox_assignment_type.setEnabled(True)

        if surfaces:

            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_assignment_type.setCurrentIndex(0)

            if len(surfaces) == 1:
                surface_id = next(iter(surfaces))
                data = self.properties._get_property("distributed_mass", surface=surface_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(surface_id=surface_id)

        elif lines:

            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_assignment_type.setCurrentIndex(1)

            if len(lines) == 1:
                line_id = next(iter(lines))
                data = self.properties._get_property("distributed_mass", line=line_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(line_id=line_id)

    def update_input_fields(self, data: dict | None):

        if data is None:
            return

        self.reset_input_fields()

        element_type = data.get("element_type")
        self.comboBox_element_type.setCurrentIndex(self.element_types.index(element_type))

        mass = np.real(data.get("values"))
        self.lineEdit_mass_to_distribute.setText(f"{round(float(mass), 8)}")

    def update_formulation_callback(self, line_id: int | None = None, surface_id: int | None = None):

        if isinstance(surface_id, int):
            data = self.properties._get_property("surface_thickness", surface=surface_id)
            if isinstance(data, dict):
                self.comboBox_element_type.setCurrentIndex(0)
                return

        if isinstance(line_id, int):
            for node_id in self.mesh.get_nodes_from_line(line_id):
                for _surface_id in self.mesh.get_surfaces_from_node(node_id):
                    data = self.properties._get_property("surface_thickness", surface=_surface_id)
                    if isinstance(data, dict):
                        self.comboBox_element_type.setCurrentIndex(0)
                        return

    def element_type_callback(self):
        return

    def update_element_type_based_on_geometry_information(self):
        volume_exists = self.mesh.are_there_volumes_in_geometry()
        self.comboBox_element_type.setCurrentIndex(int(volume_exists))

    def check_input_value(self, str_value: str):

        if str_value == "":
            return None
    
        try:
            str_value = str_value.replace(",", ".")
            return float(str_value)

        except Exception:
            title = "Invalid value detected"
            message = "An invalid value has been detected at the 'mass' input field. "
            message += "Enter a positive value to proceed with the assignment."
            PrintMessageInput([error_title, title, message])
            return None

    def constant_values_attribution(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_assignment = self.comboBox_assignment_type.currentIndex() == AssignmentType.SURFACES

        selection = "surfaces" if surface_assignment else "lines"
        selected_ids, error_data = self.model.check_selected_ids(
            input_ids,
            selection,
            domain="structural",
        )

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        update_entities_selection(self.lineEdit_selection_id, selection, selected_ids)
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)       

        self.remove_duplicated_attributions(selected_ids, selection)
        self.remove_conflicting_excitations(selected_ids, selection)

        etype_index = self.comboBox_element_type.currentIndex()
        element_type = self.element_types[etype_index]

        mass = self.check_input_value(self.lineEdit_mass_to_distribute.text())
        if mass is None:
            title = "Additional inputs required"
            message = "You must to enter at least one distributed load value before confirming the assignment."
            PrintMessageInput([error_title, title, message])
            return True

        distributed_mass = [mass]

        real_values = [value if value is None else np.real(value) for value in distributed_mass]
        imag_values = [value if value is None else np.imag(value) for value in distributed_mass]

        for selected_id in selected_ids:

            data = {
                "element_type": element_type,
                "real_values": real_values,
                "imag_values": imag_values,
                "unit": "kg",
            }

            if surface_assignment:
                self.properties._set_property("distributed_mass", data, surface=selected_id)

            else:
                self.properties._set_property("distributed_mass", data, line=selected_id)

    def lineEdit_reset(self, lineEdit: QLineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def remove_duplicated_attributions(self, selected_ids: list, selection: str):

        for selected_id in selected_ids:

            if selection == "surfaces":
                for line_id in self.mesh.lines_from_surface[selected_id]:
                    data = self.properties._get_property("distributed_mass", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("distributed_mass", line_id)

            elif selection == "lines":
                for surface_id in self.mesh.surfaces_from_line[selected_id]:
                    data = self.properties._get_property("distributed_mass", surface=surface_id)
                    if isinstance(data, dict):
                        self.properties._remove_surface_property("distributed_mass", surface_id)

    def apply_callback(self, close_window: bool=False):

        if self.tabWidget_main.currentIndex() == TabType.LIST:
            return

        if self.constant_values_attribution():
            return

        self.actions_to_finalize(close_window)

    def load_model_info(self):

        properties = {
            "line" : self.properties.line_properties,
            "surface" : self.properties.surface_properties,
        }

        self.treeWidget_distributed_mass.clear()

        for key, property in properties.items():
            for (prop_label, *args), data in property.items():

                if prop_label != "distributed_mass":
                    continue
            
                value = np.real(data["values"])[0]
                str_value = f"{value}"

                new = QTreeWidgetItem([f"{args[0]}", key, str_value])

                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_distributed_mass.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        properties_to_check = [
            self.properties.surface_properties,
            self.properties.line_properties,
        ]

        for current_property in properties_to_check:
            for (property, _) in current_property:
                if property != "distributed_mass":
                    continue

                self.tabWidget_main.setTabVisible(TabType.LIST, True)
                return

        self.tabWidget_main.setTabVisible(TabType.LIST, False)
        self.tabWidget_main.setCurrentIndex(TabType.CONSTANT_DATA)
        self.lineEdit_mass_to_distribute.setFocus()

        app().main_window.selection.set_geometry_selection()

    def tab_event_callback(self):
        list_tab = self.tabWidget_main.currentIndex() == TabType.LIST
        self.comboBox_assignment_type.setDisabled(list_tab)
        self.lineEdit_selection_id.setDisabled(list_tab)
        self.pushButton_apply.setDisabled(list_tab)
        self.pushButton_apply_and_close.setDisabled(list_tab)
        self.pushButton_remove.setDisabled(True)

        if list_tab:
            app().main_window.selection.set_geometry_selection()
        else:
            view = self.comboBox_assignment_type.view() 
            view.setRowHidden(2, True)
            self.comboBox_assignment_type.setCurrentIndex(AssignmentType.SURFACES)

        self.lineEdit_selection_id.setText("")
        self.treeWidget_distributed_mass.clearSelection()

    def item_selection_clicked_callback(self):
        self.item_clicked_callback(None)

    def item_clicked_callback(self, item):

        self.pushButton_remove.setDisabled(False)

        selected_items = self.treeWidget_distributed_mass.selectedItems()
        if not selected_items:
            self.lineEdit_selection_id.clear()
            self.pushButton_remove.setDisabled(True)
            return

        entities_mapping = defaultdict(list)
        for _item in selected_items:
            entity = _item.text(1)
            entities_mapping[entity].append(int(_item.text(0)))

        if not entities_mapping:
            return

        app().main_window.selection.set_geometry_selection(
            surfaces = entities_mapping.get("surface"),
            lines = entities_mapping.get("line"),
            )

    def item_double_clicked_callback(self, item):
        self.item_clicked_callback(item)

    def remove_conflicting_excitations(self, selected_ids: int | list, selection: str):

        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        if selection == "surfaces":
            remove_function = self.properties._remove_surface_property

        elif selection == "lines":
            remove_function = self.properties._remove_line_property

        for selected_id in selected_ids:
            remove_function("distributed_mass", selected_id)

    def remove_callback(self):

        selected_items = self.treeWidget_distributed_mass.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            selected_id = int(item.text(0))
            selection = item.text(1)

            if selection == "surface":
                self.properties._remove_surface_property("distributed_mass", selected_id)

            elif selection == "line":
                self.properties._remove_line_property("distributed_mass", selected_id)

        self.actions_to_finalize()

        app().main_window.selection.set_geometry_selection()
        app().main_window.selection.set_mesh_selection()

    def reset_callback(self):

        title = "Distributed masses reset"
        message = "Would you like to remove the all distributed masses from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if obj._cancel:
            return

        if obj._continue:
            self.properties._reset_property("distributed_mass")
            self.actions_to_finalize()

            app().main_window.selection.set_geometry_selection()
            app().main_window.selection.set_mesh_selection()

    def actions_to_finalize(self, close_window: bool = False):
        self.load_model_info()
        self.reset_input_fields(reset_all=True)
        app().main_window.update_info_text()
        app().project.update_model_properties_file()
        app().main_window.update_symbols()

        if close_window:
            self.close()

    def reset_input_fields(self, reset_all: bool = False):

        if reset_all:
            self.lineEdit_selection_id.clear()

        self.lineEdit_mass_to_distribute.clear()

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