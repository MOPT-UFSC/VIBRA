
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.ui_generated.model.setup.structural.dof_constraint_inputs_ui import DofConstraintInputs_UI
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.utils import are_there_values_different_from_zero

import numpy as np
from enum import IntEnum
from collections import defaultdict


error_title = "Error"
warning_title = "Warning"


class ElementFormulation(IntEnum):
    ELEMENT_2D = 0
    ELEMENT_3D = 1


class AssignmentType(IntEnum):
    SURFACES = 0
    LINES = 1
    POINTS = 2
    NODES = 3


class DofConstraintInputs(DofConstraintInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._create_connections()

        self._config_widgets()
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

    def _config_widgets(self):
        #
        self.comboBox_element_type.setEnabled(False)
        #
        for i, w in enumerate([110, 150, 100]):
            self.treeWidget_prescribed_dofs.setColumnWidth(i, w)
            self.treeWidget_prescribed_dofs.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_callback)
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_fixed_support.clicked.connect(self.fixed_support_callback)
        self.pushButton_unselect_all.clicked.connect(self.unselect_all_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_prescribed_dofs.itemClicked.connect(self.on_click_item)
        self.treeWidget_prescribed_dofs.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.geometry_selection_callback()
        self.update_element_type_based_on_geometry_information()

    def fixed_support_callback(self):
        self.set_all_checkboxes(True)

    def unselect_all_callback(self):
        self.set_all_checkboxes(False)

    def set_all_checkboxes(self, checked: bool):

        self.checkBox_constrain_ux.setChecked(checked)
        self.checkBox_constrain_uy.setChecked(checked)
        self.checkBox_constrain_uz.setChecked(checked)

        element_index = self.comboBox_element_type.currentIndex()
        if element_index == ElementFormulation.ELEMENT_2D:
            self.checkBox_constrain_rx.setChecked(checked)
            self.checkBox_constrain_ry.setChecked(checked)
            self.checkBox_constrain_rz.setChecked(checked)

    def geometry_selection_callback(self):

        surfaces = app().main_window.selected_geometry_surfaces
        lines = app().main_window.selected_geometry_lines
        points = app().main_window.selected_geometry_points
        nodes = app().main_window.selected_mesh_nodes

        if surfaces:

            text = ", ".join([str(i) for i in surfaces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(0)

            if len(surfaces) == 1:
                surface_id = list(surfaces)[0]
                data = self.properties._get_property("prescribed_dofs", surface=surface_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(surface_id=surface_id)

        elif lines:

            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(1)

            if len(lines) == 1:
                line_id = list(lines)[0]
                data = self.properties._get_property("prescribed_dofs", line=line_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(line_id=line_id)

        elif points:
            
            text = ", ".join([str(i) for i in points])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(2)

            if len(points) == 1:
                point_id = list(points)[0]
                data = self.properties._get_property("prescribed_dofs", point=point_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(point_id=point_id)

        elif nodes:
            
            text = ", ".join([str(i) for i in nodes])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(3)

            if len(nodes) == 1:
                node_id = list(nodes)[0]
                data = self.properties._get_property("prescribed_dofs", node=node_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(node_id=node_id)

    def update_input_fields(self, data: dict | None):

        if data is None:
            return
        
        values = data.get("values")
        element_type = data.get("element_type", None)

        if are_there_values_different_from_zero(values):
            return

        mask = [False if value is None else True for value in values]

        self.checkBox_constrain_ux.setChecked(mask[0])
        self.checkBox_constrain_uy.setChecked(mask[1])
        self.checkBox_constrain_uz.setChecked(mask[2])

        if element_type == "2d_element":
            self.checkBox_constrain_rx.setChecked(mask[3])
            self.checkBox_constrain_ry.setChecked(mask[4])
            self.checkBox_constrain_rz.setChecked(mask[5])
            self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)

        else:
            self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_3D)

    def attribution_type_callback(self):
        if self.comboBox_attribution_type.currentIndex() == 3:
            app().main_window.action_mesh_workspace_callback()
        else:
            app().main_window.action_model_workspace_callback()

    def element_type_callback(self):

        element_2d = self.comboBox_element_type.currentIndex() == ElementFormulation.ELEMENT_2D

        self.checkBox_constrain_rx.setVisible(element_2d)
        self.checkBox_constrain_ry.setVisible(element_2d)
        self.checkBox_constrain_rz.setVisible(element_2d)

    def update_element_type_based_on_geometry_information(self):
        volume_exists = self.mesh.are_there_volumes_in_geometry()
        self.comboBox_element_type.setCurrentIndex(int(volume_exists))

    def attribute_callback(self):

        input_ids = self.lineEdit_selection_id.text()
        assign_index = self.comboBox_attribution_type.currentIndex()

        assigment_types = ["surfaces", "lines", "points", "nodes"]
        selected_ids, error_data = self.mesh.check_selected_ids(
                                                                input_ids, 
                                                                selection = assigment_types[assign_index], 
                                                                single_id = False
                                                                )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return
        
        self.remove_duplicated_attributions(selected_ids, assigment_types[assign_index])
        self.remove_conflicting_excitations(selected_ids, assigment_types[assign_index])

        etype_index = self.comboBox_element_type.currentIndex()
        element_type = self.element_types[etype_index]

        ux = complex(0) if self.checkBox_constrain_ux.isChecked() else None
        uy = complex(0) if self.checkBox_constrain_uy.isChecked() else None
        uz = complex(0) if self.checkBox_constrain_uz.isChecked() else None

        constrained_dofs = [ux, uy, uz]

        if element_type == "2d_element":
            rx = complex(0) if self.checkBox_constrain_rx.isChecked() else None
            ry = complex(0) if self.checkBox_constrain_ry.isChecked() else None
            rz = complex(0) if self.checkBox_constrain_rz.isChecked() else None

            constrained_dofs.extend([rx, ry, rz])        

        condition_1 = element_type == "2d_element" and constrained_dofs.count(None) == 6
        condition_2 = element_type == "3d_element" and constrained_dofs.count(None) == 3

        if condition_1 or condition_2:
            self.hide()
            title = "Additional inputs required"
            message = "It is necessary to constrain at least one dof "
            message += "before confirming the property assignment."
            PrintMessageInput([error_title, title, message])
            return

        real_values = [value if value is None else np.real(value) for value in constrained_dofs]
        imag_values = [value if value is None else np.imag(value) for value in constrained_dofs]

        for selected_id in selected_ids:

            data = {
                    "element_type" : element_type,
                    "values" : constrained_dofs,
                    "real_values" : real_values,
                    "imag_values" : imag_values
                    }

            if  assign_index == AssignmentType.SURFACES:
                self.model.properties._set_property("prescribed_dofs", data, surface=selected_id)

            elif assign_index == AssignmentType.LINES:
                self.model.properties._set_property("prescribed_dofs", data, line=selected_id)

            elif assign_index == AssignmentType.POINTS:
                self.model.properties._set_property("prescribed_dofs", data, point=selected_id)

            elif assign_index == AssignmentType.NODES:
                self.model.properties._set_property("prescribed_dofs", data, node=selected_id)

        self.actions_to_finalize()

    def remove_duplicated_attributions(self, selected_ids: list, selection: str):

        table_names = list()
        nodes_to_remove = list()
        for selected_id in selected_ids:

            if selection == "surfaces":

                nodes_from_surface = self.mesh.nodes_from_surfaces[selected_id]
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "prescribed_dofs" and node_id in nodes_from_surface:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for line_id in self.mesh.lines_from_surface[selected_id]:
                    data = self.properties._get_property("prescribed_dofs", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("prescribed_dofs", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", line_id, "lines"))

                    for point_id in self.mesh.points_from_line[line_id]:
                        data = self.properties._get_property("prescribed_dofs", point=point_id)
                        if isinstance(data, dict):
                            self.properties._remove_point_property("prescribed_dofs", point_id)
                            table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", point_id, "points"))

            elif selection == "lines":

                nodes_from_line = self.mesh.nodes_from_lines[selected_id]
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "prescribed_dofs" and node_id in nodes_from_line:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for surface_id in self.mesh.surfaces_from_line[selected_id]:
                    data = self.properties._get_property("prescribed_dofs", surface=surface_id)
                    if isinstance(data, dict):
                        self.properties._remove_surface_property("prescribed_dofs", surface_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", surface_id, "surfaces"))

                for point_id in self.mesh.points_from_line[selected_id]:
                    data = self.properties._get_property("prescribed_dofs", point=point_id)
                    if isinstance(data, dict):
                        self.properties._remove_point_property("prescribed_dofs", point_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", point_id, "points"))

            elif selection == "points":

                nodes_from_point = self.mesh.nodes_from_points[selected_id]
                for (property, node_id) in self.properties.nodal_properties.keys():
                    if property == "prescribed_dofs" and node_id in nodes_from_point:
                        if node_id not in nodes_to_remove:
                            nodes_to_remove.append(node_id)

                for line_id in self.mesh.lines_from_point[selected_id]:
                    data = self.properties._get_property("prescribed_dofs", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("prescribed_dofs", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", line_id, "lines"))

                    for surface_id in self.mesh.surfaces_from_line[line_id]:
                        data = self.properties._get_property("prescribed_dofs", surface=surface_id)
                        if isinstance(data, dict):
                            self.properties._remove_surface_property("prescribed_dofs", surface_id)
                            table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", surface_id, "surfaces"))

            elif selection == "nodes":

                point_id = selected_id + 1
                data = self.properties._get_property("prescribed_dofs", point=point_id)
                if isinstance(data, dict):
                    self.properties._remove_point_property("prescribed_dofs", point_id)
                    table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", point_id, "points"))

                for line_id in self.mesh.lines_from_point[point_id]:
                    data = self.properties._get_property("prescribed_dofs", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("prescribed_dofs", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", line_id, "lines"))

                    for surface_id in self.mesh.surfaces_from_line[line_id]:
                        data = self.properties._get_property("prescribed_dofs", surface=surface_id)
                        if isinstance(data, dict):
                            self.properties._remove_surface_property("prescribed_dofs", surface_id)
                            table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", surface_id, "surfaces"))

            for node_id in nodes_to_remove:
                self.properties._remove_nodal_property("prescribed_dofs", node_id)
                table_names.extend(self.properties.get_property_related_table_names("prescribed_dofs", node_id, "nodes"))

            self.process_table_file_removal(table_names)

    def text_label(self, mask: list[bool]):

        text = ""
        if len(mask) == 6:
            dofs_labels = np.array(['Ux','Uy','Uz','Rx','Ry','Rz'])

        else:
            dofs_labels = np.array(['Ux','Uy','Uz'])

        labels = dofs_labels[mask]

        if list(mask).count(True) == 6:
            text = "[{}, {}, {}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 5:
            text = "[{}, {}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 4:
            text = "[{}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(*labels)
        elif list(mask).count(True) == 1:
            text = "[{}]".format(*labels)

        return text

    def add_model_info_in_treeWidget(self, entity: str):

        properties = {
                        "surface" : self.properties.surface_properties,
                        "line" : self.properties.line_properties,
                        "point" : self.properties.point_properties,
                        "node" : self.properties.nodal_properties,
                      }
        
        _property = properties.get(entity)
        if _property is None:
            return
        
        for (property, *args), data in _property.items():
            if property != "prescribed_dofs":
                continue

            values = data["values"]
            if are_there_values_different_from_zero(values):
                continue

            element_type = data["element_type"]
            constrained_dofs_mask = [False if value is None else True for value in values]
            dofs_labels = str(self.text_label(constrained_dofs_mask))

            new = QTreeWidgetItem([f"{entity.capitalize()}-{args[0]}", dofs_labels, element_type])
            for i in range(3):
                new.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_prescribed_dofs.addTopLevelItem(new)

    def load_model_info(self):

        self.treeWidget_prescribed_dofs.clear()

        self.add_model_info_in_treeWidget("surface")
        self.add_model_info_in_treeWidget("line")
        self.add_model_info_in_treeWidget("point")
        self.add_model_info_in_treeWidget("node")
        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        properties_to_check = [
                               self.properties.surface_properties,
                               self.properties.line_properties,
                               self.properties.point_properties,
                               self.properties.nodal_properties,
                               ]

        for current_property in properties_to_check:
            for (property, _), data in current_property.items():
                if property != "prescribed_dofs":
                    continue

                if are_there_values_different_from_zero((data.get("values"))):
                    continue

                self.tabWidget_main.setTabVisible(1, True)
                return

        self.tabWidget_main.setTabVisible(1, False)
        self.tabWidget_main.setCurrentIndex(0)
        app().main_window.set_geometry_selection()

    def tab_event_callback(self):

        list_tab = self.tabWidget_main.currentIndex() == 1
        self.lineEdit_selection_id.setDisabled(list_tab)
        self.pushButton_attribute.setDisabled(list_tab)
        self.pushButton_attribute.setDisabled(list_tab)

        if list_tab:
            self.lineEdit_selection_id.setText("")
            return

        else:
            text = self.lineEdit_selection_id.text()
            if "-" in text:
                selected_id = text.split("-")[1]
                self.lineEdit_selection_id.setText(selected_id)

    def on_click_item(self, item):

        self.pushButton_remove.setDisabled(False)

        if item.text(0) != "":

            selection, _selected_id = item.text(0).split("-")
            selected_id = int(_selected_id)

            if selection == "Surface":
                app().main_window.set_geometry_selection(surfaces = [int(selected_id)])

            elif selection == "Line":
                app().main_window.set_geometry_selection(lines = [int(selected_id)])

            elif selection == "Point":
                app().main_window.set_geometry_selection(points = [int(selected_id)])

            elif selection == "Node":
                app().main_window.set_mesh_selection(nodes=[int(selected_id)])

            if selection == "Node":
                app().main_window.action_mesh_workspace_callback()

            else:
                app().main_window.action_model_workspace_callback()

            self.lineEdit_selection_id.setText(item.text(0))

    def on_double_click_item(self, item):
        self.on_click_item(item)

    def process_table_file_removal(self, table_names: list):

        if len(table_names) == 0:
            return

        for table_name in table_names:
            self.properties.remove_imported_tables("structural", table_name)

        app().file.write_imported_table_data_in_file()

    def remove_conflicting_excitations(self, selected_ids: int | list, selection: str):

        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        if selection == "surfaces":
            remove_function = self.properties._remove_surface_property

        elif selection == "lines":
            remove_function = self.properties._remove_line_property

        elif selection == "points":
            remove_function = self.properties._remove_point_property

        elif selection == "nodes":
            remove_function = self.properties._remove_nodal_property

        properties = ["nodal_loads", "prescribed_dofs"]

        for selected_id in selected_ids:
            for property in properties:
                table_names = self.properties.get_property_related_table_names(property, selected_id, selection)
                remove_function(property, selected_id)
                self.process_table_file_removal(table_names)

    def remove_callback(self):

        text = self.lineEdit_selection_id.text()

        if "-" in text:

            selection, _selected_id = text.split("-")
            selected_id = int(_selected_id)

            if selection == "Surface":
                self.properties._remove_surface_property("prescribed_dofs", selected_id)

            elif selection == "Line":
                self.properties._remove_line_property("prescribed_dofs", selected_id)

            elif selection == "Point":
                self.properties._remove_point_property("prescribed_dofs", selected_id)

            elif selection == "Node":
                self.properties._remove_nodal_property("prescribed_dofs", selected_id)

            else:
                return

            self.actions_to_finalize()

            app().main_window.set_geometry_selection()
            app().main_window.set_mesh_selection()

    def reset_callback(self):

        self.hide()

        title = "DOF constraint reset"
        message = "Would you like to remove the all constrained DOF from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if obj._cancel:
            return

        if obj._continue:

            properties = {
                        "surfaces" : self.properties.surface_properties,
                        "lines" : self.properties.line_properties,
                        "points" : self.properties.point_properties,
                        "nodes" : self.properties.nodal_properties,
                        }

            entities_to_remove = defaultdict(list)

            for entity_label, _property in properties.items():
                for (property_label, *args), data in _property.items():
                    if property_label != "prescribed_dofs":
                        continue
    
                    if are_there_values_different_from_zero(data.get("values")):
                        continue
    
                    entities_to_remove[entity_label].append(args[0])

            for entity, selected_ids in entities_to_remove.items():
                for selected_id in selected_ids:
                    if entity == "surfaces":
                        self.properties._remove_surface_property("prescribed_dofs", selected_id)
                    elif entity == "lines":
                        self.properties._remove_line_property("prescribed_dofs", selected_id)
                    elif entity == "points":
                        self.properties._remove_point_property("prescribed_dofs", selected_id)
                    elif entity == "nodes":
                        self.properties._remove_nodal_property("prescribed_dofs", selected_id)

            self.actions_to_finalize()

            app().main_window.set_geometry_selection()
            app().main_window.set_mesh_selection()

    def actions_to_finalize(self):
        self.load_model_info()
        app().main_window.update_info_text()
        app().main_window.update_symbols()
        app().file.write_model_properties_in_file()
        app().file.write_imported_table_data_in_file()

    def check_model_frequency_controls(self):

        for key, data in self.properties.surface_properties.items():
            property, _ = key
            if property in ["nodal_loads", "prescribed_dofs"]:
                if "table_names" in data.keys():
                    return

        if isinstance(self.project.analysis_setup, dict):
            analysis_setup = self.project.analysis_setup
            self.project.set_analysis_setup(analysis_setup)
            app().file.write_analysis_setup_in_file(analysis_setup)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)

    #TODO: remove soon
    def update_formulation_callback(self, **kwargs):
        return

        surface_id = kwargs.get("surface_id", None)
        line_id = kwargs.get("line_id", None)
        point_id = kwargs.get("point_id", None)
        node_id = kwargs.get("node_id", None)

        if isinstance(surface_id, int):
            data = self.properties._get_property("surface_thickness", surface=surface_id)
            if isinstance(data, dict):
                self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
                return
            
        if isinstance(line_id, int):
            for node_id in self.mesh.nodes_from_lines[line_id]:
                for surface_id in self.mesh.surfaces_from_node[node_id]:
                    data = self.properties._get_property("surface_thickness", surface=surface_id)
                    if isinstance(data, dict):
                        self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
                        return

        if isinstance(point_id, int):
            node_id = self.mesh.nodes_from_points.get(point_id)
            if node_id is None:
                return

            for surface_id in self.mesh.surfaces_from_node[node_id]:
                data = self.properties._get_property("surface_thickness", surface=surface_id)
                if isinstance(data, dict):
                    self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
                    return

        if isinstance(node_id, int):
            for surface_id in self.mesh.surfaces_from_node[node_id]:
                data = self.properties._get_property("surface_thickness", surface=surface_id)
                if isinstance(data, dict):
                    self.comboBox_element_type.setCurrentIndex(ElementFormulation.ELEMENT_2D)
                    return