
import logging
from copy import deepcopy

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QTreeWidgetItem

from vibra import app
from vibra.interface import warning_title
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.model_inputs.structural.definitions.enums import SetupTabType
from vibra.interface.ui_generated.model.dof_decoupling.degrees_of_freedom_decoupling_inputs_ui import DegreesOfFreedomDecouplingInputs_UI
from vibra.utils.bidict import bidict


class DegreesOfFreedomDecouplingInputs(DegreesOfFreedomDecouplingInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._configure_qt_variables()
        self._create_connections()

        self.load_model_info()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.assignment_complete = False
        self.keep_window_open = True
        self.cache_surface_properties = deepcopy(self.properties.surface_properties)
        self.decoupling_map = bidict()

    def _configure_qt_variables(self):
        #
        for i, width in enumerate([140]):
            self.treeWidget_selection_info.setColumnWidth(i, width)
            self.treeWidget_dof_decoupling.setColumnWidth(i, width)
            self.treeWidget_selection_info.headerItem().setTextAlignment(i, Qt.AlignCenter)           
            self.treeWidget_dof_decoupling.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_dof_decoupling.itemClicked.connect(self.on_click_item)
        self.treeWidget_dof_decoupling.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)

    def tab_event_callback(self):
        tab_list = self.tabWidget_main.currentIndex() == SetupTabType.LIST
        self.lineEdit_selection_id.setText("")
        self.lineEdit_selection_id.setDisabled(tab_list)
        self.pushButton_apply.setDisabled(tab_list)
        self.pushButton_apply_and_close.setDisabled(tab_list)

        if tab_list:
            self.on_click_item(None)

    def geometry_selection_callback(self):

        surfaces = app().main_window.selection.geometry_surfaces

        if surfaces:
            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)

            surface_ids = [int(surf_id) for surf_id in surfaces]
            surface_ids.sort()
            self.update_volumes_from_faces(surface_ids)  
            return

        self.lineEdit_selection_id.setText("")

    def update_volumes_from_faces(self, surface_ids: list[int]):

        self.treeWidget_selection_info.clear()

        for surface_id in surface_ids:
            volumes_from_surface = self.model.mesh.volumes_from_surface[surface_id]
            item = QTreeWidgetItem([str(surface_id), str(volumes_from_surface)])
            for i in range(2):
                item.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_selection_info.addTopLevelItem(item)

        return

    def apply_callback(self, close_window: bool = False):

        if self.tabWidget_main.currentIndex() == SetupTabType.LIST:
            return

        input_ids = self.lineEdit_selection_id.text()
        surface_ids, message_log = self.mesh.check_selected_ids(input_ids, selection="surfaces")

        if message_log is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(message_log)
            return

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
                self.hide()
                title = "Invalid surface selected"
                PrintMessageInput([warning_title, title, message])
                return

            data = {"volume_to_decouple" : volumes_from_surface[0]}
            self.properties._set_property("degrees_of_freedom_decoupling", data, surface=surface_id)

        self.assignment_complete = True

        self.hide()
        self.actions_to_finalize(close_window)

    def remove_all_surface_properties_from_surface(self, new_surface_ids: list[int]):
        if not new_surface_ids:
            return

        surface_properties = deepcopy(self.properties.surface_properties)
        for new_surface_id in new_surface_ids:
            for (property, surf_id) in surface_properties.keys():
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
                    if line_from_surface != line_id:
                        continue

                    self.properties._remove_line_property(property, line_id)

    def remove_callback(self):

        for selected_item in self.treeWidget_dof_decoupling.selectedItems():
            if selected_item.text(0):
                surface_id = int(selected_item.text(0))

            data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_id)
            if not isinstance(data, dict):
                continue

            new_surface_id = data.get("new_surface_id")
            if not isinstance(new_surface_id, int):
                continue

            self.remove_all_surface_properties_from_surface([new_surface_id])
            self.remove_all_line_properties_boundind_surface([new_surface_id]) 
            self.properties._remove_surface_property("degrees_of_freedom_decoupling", surface_id)

        self.actions_to_finalize()
        self.restore_mesh_data_modified_by_decoupling()

    def reset_callback(self):

        self.hide()

        title = "Degrees of freedom decoupling resetting"
        message = "Would you like to revert the acoustic degrees of freedom decoupling from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            new_surface_ids = list()
            for (property, _), data in self.properties.surface_properties.items():
                if property == "degrees_of_freedom_decoupling":
                    data: dict
                    new_surface_id = data.get("new_surface_id")
                    if isinstance(new_surface_id, int):
                        new_surface_ids.append(new_surface_id)

            self.remove_all_surface_properties_from_surface([new_surface_id])
            self.remove_all_line_properties_boundind_surface([new_surface_id]) 
            self.properties._reset_property("degrees_of_freedom_decoupling")

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
        if not self.mesh.has_decoupling():
            return

        self.mesh.restore_data_from_cache()
        self.mesh.process_upwards_adjacencies_from_entities()

        # if self.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):
        #     self.mesh.cache_mesh_information()

        self.process_decoupling_actions()

    def get_selected_surfaces_from_tree_widget_transfer_impedance(self) -> list:
        selected_items = self.treeWidget_dof_decoupling.selectedItems()
        if not selected_items:
            return list()

        return [int(item.text(0)) for item in selected_items]

    def set_selection_text(self, selected_surfaces: list | set):
        selected_surfaces_decoupled = list()

        for selected_surface in selected_surfaces:
            decouple_surface = self.decoupling_map.get(selected_surface)
            if decouple_surface is None:
                decouple_pair = [selected_surface, "Awaiting uncoupling"]

            else:
                decouple_pair = [selected_surface, decouple_surface]
                decouple_pair.sort()
                       
            decouple_pair = tuple(decouple_pair)
            selected_surfaces_decoupled.append(str(decouple_pair))

        selection_text = ", ".join(selected_surfaces_decoupled)

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)

    def on_click_item(self, item: QTreeWidgetItem):

        surface_ids = self.get_selected_surfaces_from_tree_widget_transfer_impedance()
        if not surface_ids:
            return

        app().main_window.selection.set_geometry_selection(surfaces=surface_ids)

        self.decoupling_map.clear()
        for surface_id in surface_ids:
            decoupling_data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_id)

            if isinstance(decoupling_data, dict):
                new_surface_id = decoupling_data.get("new_surface_id")
                if new_surface_id is None:
                    continue

                self.decoupling_map[surface_id] = new_surface_id

        self.pushButton_remove.setEnabled(True)
        self.set_selection_text(surface_ids)

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def load_model_info(self):
        self.treeWidget_dof_decoupling.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property != "degrees_of_freedom_decoupling":
                continue

            data: dict
            pp_data =  self.properties._get_property("perforated_plate_model", surface=surface_id)
            if isinstance(pp_data, dict):
                continue

            ti_data =  self.properties._get_property("transfer_impedance", surface=surface_id)
            if isinstance(ti_data, dict):
                continue

            volume_id = data.get("volume_to_decouple")
            if volume_id is None:
                continue

            new = QTreeWidgetItem([str(surface_id), str(volume_id)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_dof_decoupling.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        for (property, surface_id) in self.properties.surface_properties.keys():
            if property != "degrees_of_freedom_decoupling":
                continue

            pp_data = self.properties._get_property("perforated_plate_model", surface=surface_id)
            if isinstance(pp_data, dict):
                continue

            self.tabWidget_main.setTabVisible(1, True)
            return

        self.tabWidget_main.setTabVisible(1, False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            return

    def process_degress_of_freedom_decoupling(self):
        if not self.assignment_complete:
            return False

        if not self.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):
            return False

        if not app().project.model.is_there_a_valid_mesh():
            self.hide()
            app().main_window.input_ui.mesh_setup()
            app().main_window.set_input_widget(self)
            if not app().project.model.is_there_a_valid_mesh():
                return True
            else:
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

    def closeEvent(self, event: QCloseEvent | None) -> None:

        self.hide()
        if self.process_degress_of_freedom_decoupling():
            return

        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)

        return super().closeEvent(event)