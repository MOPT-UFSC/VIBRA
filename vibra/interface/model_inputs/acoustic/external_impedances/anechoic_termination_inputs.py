import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QTreeWidgetItem

from vibra import app
from vibra.interface import warning_title
from vibra.interface.common.common_interface import filter_outside_surfaces
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.acoustic.definitions.enums import SetupTabType
from vibra.interface.ui_generated.model.acoustic.external_impedances.anechoic_termination_inputs_ui import AnechoicTerminationInputs_UI


class AnechoicTerminationInputs(AnechoicTerminationInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

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

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.keep_window_open = True
        self.anechoic_termination = None

    def _create_connections(self):
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_anechoic_termination.itemClicked.connect(self.on_click_item)
        self.treeWidget_anechoic_termination.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.geometry_selection_callback()

    def _config_widgets(self):

        self.lineEdit_selection_id.setDisabled(True)
        self.treeWidget_selection_info.setSelectionMode(QAbstractItemView.NoSelection)
    
        for i, w in enumerate([120]):
            self.treeWidget_selection_info.setColumnWidth(i, w)
            self.treeWidget_selection_info.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_anechoic_termination.setColumnWidth(i, w)
            self.treeWidget_anechoic_termination.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def tab_event_callback(self):
        self.clear_line_edit_selection_id()
        app().main_window.selection.clear_selection()

        self.pushButton_remove.setDisabled(True)
        self.treeWidget_selection_info.clear()
        self.treeWidget_anechoic_termination.clearSelection()

        tab_list = self.tabWidget_main.currentIndex() == SetupTabType.LIST
        # self.lineEdit_selection_id.setDisabled(tab_list)
        self.pushButton_apply.setDisabled(tab_list)
        self.pushButton_apply_and_close.setDisabled(tab_list)

    def geometry_selection_callback(self):
        if self.tabWidget_main.currentIndex() == SetupTabType.LIST:
            selected_surfaces = self.get_selected_surfaces_from_tree_widget()
            if not selected_surfaces:
                return

            self.set_selection_text(selected_surfaces)
            return

        surfaces = app().main_window.selection.geometry_surfaces
        if not surfaces:
            return

        (outside_surfaces, _) = filter_outside_surfaces(list(surfaces), "anechoic termination")
        if not outside_surfaces:
            return

        self.set_selection_text(outside_surfaces)
        self.load_specific_impedance_of_selected_surfaces()

    def load_specific_impedance_of_selected_surfaces(self):

        self.treeWidget_selection_info.clear()
        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(input_ids, selection="surfaces")

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        for surf_id in np.sort(surface_ids):

            str_impedance = None
            if self.model.is_surface_impedance_frequency_dependent(surf_id):
                str_impedance = "Spectral data"

            else:
                density, speed_of_sound = self.model.get_surface_density_and_speed_of_sound(surf_id)
                if density is None:
                    str_impedance = "Not defined fluid"

                else:
                    impedance = density * speed_of_sound
                    str_impedance = f"{impedance : .6f}"

            if not isinstance(str_impedance, str):
                continue

            item = QTreeWidgetItem([str(surf_id), str_impedance])
            for j in range(2):
                item.setTextAlignment(j, Qt.AlignCenter)

            self.treeWidget_selection_info.addTopLevelItem(item)

    def apply_callback(self, close_window: bool = False):

        if self.tabWidget_main.currentIndex() == SetupTabType.LIST:
            return
        
        input_ids = self.lineEdit_selection_id.text()
        surface_ids, error_data = self.mesh.check_selected_ids(input_ids, selection="surfaces")

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return

        self.remove_conflicting_excitations(surface_ids)

        for surface_id in surface_ids:

            volume_ids = self.model.mesh.volumes_from_surface[surface_ids[0]]
            if len(surface_ids) > 1 and len(volume_ids) > 1:

                title = "Undefined volume"
                
                # message = f"The selected face ID [{face_id}] is associated to the volumes {volume_ids}. "
                message = "The multiple selection of faces related to more than one volume is not allowed. "
                message += "In this case, it is necessary to select the Face ID and the respective Volume ID "
                message += "to proceed."
                PrintMessageInput([warning_title, title, message])
                return

            data = {
                "anechoic_termination": True,
                "volume_id": volume_ids[0],
            }

            self.properties._set_property("specific_impedance", data, surface=surface_id)

        self.actions_to_finalize(close_window)

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().project.update_model_properties_file()

    def remove_conflicting_excitations(self, surface_ids: int | list):

        if isinstance(surface_ids, int):
            surface_ids = [surface_ids]

        labels = [
            "absorption_surface",
            "specific_impedance",
            "incident_plane_wave",
            ]

        for surface_id in surface_ids:
            for label in labels:
                table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_id : list):
        table_names = self.properties.get_property_related_table_names("specific_impedance", surface_id, "surfaces")
        self.process_table_file_removal(table_names)

    def remove_callback(self):
        selected_surfaces = self.get_selected_surfaces_from_tree_widget()
        if not selected_surfaces:
            return

        for surface_id in selected_surfaces:
            self.remove_table_files_from_surfaces(surface_id)
            self.properties._remove_surface_property("specific_impedance", surface_id)

        self.clear_line_edit_selection_id()
        self.pushButton_remove.setDisabled(True)

        app().main_window.selection.clear_selection()
        self.actions_to_finalize()

    def reset_callback(self):

        title = "Anechoic termination resetting"
        message = "Would you like to remove the all applied anechoic termination from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        surface_ids = list()
        for (property, *args), data in self.properties.surface_properties.items():
            if property != "specific_impedance":
                continue

            if "anechoic_termination" not in data.keys():
                continue

            surface_id = args[0]
            surface_ids.append(surface_id)

        self.remove_table_files_from_surfaces(surface_ids)
        self.properties._reset_property("specific_impedance")
        self.actions_to_finalize()

    def actions_to_finalize(self, close_window: bool = False):
        self.load_model_info()
        app().main_window.update_info_text()
        app().project.update_model_properties_file()
        app().main_window.update_symbols()

        if close_window:
            self.close()

    def update_tabs_visibility(self):

        for key, data in self.properties.surface_properties.items():
            property, *args = key
            if property != "specific_impedance":
                continue

            if "anechoic_termination" in data.keys():
                self.tabWidget_main.setTabVisible(SetupTabType.LIST, True)
                return

        self.tabWidget_main.setCurrentIndex(SetupTabType.SETUP)
        self.tabWidget_main.setTabVisible(SetupTabType.LIST, False)

    def on_click_item(self, item: QTreeWidgetItem):
        surface_ids = self.get_selected_surfaces_from_tree_widget()
        if not surface_ids:
            return
    
        app().main_window.selection.set_geometry_selection(surfaces=surface_ids)
        self.pushButton_remove.setEnabled(True)

    def on_doubleclick_item(self, item: QTreeWidgetItem):
        self.on_click_item(item)

    def get_selected_surfaces_from_tree_widget(self) -> list:
        selected_items = self.treeWidget_anechoic_termination.selectedItems()
        if not selected_items:
            return list()

        return [int(item.text(0)) for item in selected_items]
    
    def set_selection_text(self, selected_surfaces: list | set):
        self.clear_line_edit_selection_id()
        selected_surfaces = list(selected_surfaces)
        selected_surfaces.sort()

        selected_surfaces = map(str, selected_surfaces)
        selection_text = ", ".join(selected_surfaces)

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)
    
    def clear_line_edit_selection_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")

    def load_model_info(self):
        self.treeWidget_anechoic_termination.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property != "specific_impedance":
                continue

            if "anechoic_termination" not in data.keys():
                continue

            volume_id = data.get("volume_id")
            if volume_id is None:
                continue

            density, speed_of_sound = self.model.get_surface_density_and_speed_of_sound(surface_id)
            if density is None:
                continue

            if isinstance(density, np.ndarray):
                str_impedance = "Spectral data"
            else:
                impedance = density * speed_of_sound
                str_impedance = f"{impedance : .6f}"

            item = QTreeWidgetItem([str(surface_id), str_impedance])
            for j in range(2):
                item.setTextAlignment(j, Qt.AlignCenter)
            
            self.treeWidget_anechoic_termination.addTopLevelItem(item)

        self.update_tabs_visibility()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Control:
            self.treeWidget_anechoic_termination.setSelectionMode(QAbstractItemView.MultiSelection)
        elif event.key() == Qt.Key_Shift:
            self.treeWidget_anechoic_termination.setSelectionMode(QAbstractItemView.ContiguousSelection)
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.treeWidget_anechoic_termination.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)
    
# fmt: on