
from os.path import basename

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem

from vibra import app
from vibra.interface import error_title
from vibra.interface.common.common_interface import update_analysis_setup_in_file
from vibra.interface.data_handler.data_importer import DataImporter
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.structural.definitions.enums import StandardTabType
from vibra.interface.ui_generated.model.structural.excitations.distributed_loads_inputs_ui import DistributedLoadsInputs_UI


class DistributedLoadsInputs(DistributedLoadsInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._create_list_lineEdits()
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
        self.reset_table_variables()

    def reset_table_variables(self):

        self.Fx_table_values = None
        self.Fy_table_values = None
        self.Fz_table_values = None

        self.Fx_array = None
        self.Fy_array = None
        self.Fz_array = None

        self.Fx_table_path = None
        self.Fy_table_path = None
        self.Fz_table_path = None

        self.Fx_table_name = None
        self.Fy_table_name = None
        self.Fz_table_name = None

    def _create_list_lineEdits(self):
        self.list_lineEdit_constant_values = [
            [self.lineEdit_real_Fx, self.lineEdit_imag_Fx],
            [self.lineEdit_real_Fy, self.lineEdit_imag_Fy],
            [self.lineEdit_real_Fz, self.lineEdit_imag_Fz],
        ]

        self.table_lineEdits = {
            "Fx": self.lineEdit_path_table_Fx,
            "Fy": self.lineEdit_path_table_Fy,
            "Fz": self.lineEdit_path_table_Fz,
        }

    def _config_widgets(self):
        #
        self.comboBox_element_type.setEnabled(False)
        #
        for i, w in enumerate([110, 150, 100]):
            self.treeWidget_distributed_loads.setColumnWidth(i, w)
            self.treeWidget_distributed_loads.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_callback)
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_load_Fx_table.clicked.connect(self.load_Fx_table)
        self.pushButton_load_Fy_table.clicked.connect(self.load_Fy_table)
        self.pushButton_load_Fz_table.clicked.connect(self.load_Fz_table)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_distributed_loads.itemClicked.connect(self.on_click_item)
        self.treeWidget_distributed_loads.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        self.update_element_type_based_on_geometry_information()

    def geometry_selection_callback(self):

        faces = app().main_window.selection.geometry_surfaces
        lines = app().main_window.selection.geometry_lines

        if faces:

            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(0)

            if len(faces) == 1:
                surface_id = list(faces)[0]
                data = self.properties._get_property("distributed_loads", surface=surface_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(surface_id=surface_id)

        elif lines:

            text = ", ".join([str(i) for i in lines])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(1)

            if len(lines) == 1:
                line_id = list(lines)[0]
                data = self.properties._get_property("distributed_loads", line=line_id)
                self.update_input_fields(data)
                if data is None:
                    self.update_formulation_callback(line_id=line_id)

    def update_input_fields(self, data: dict | None):

        if data is None:
            return

        self.reset_input_fields()

        element_type = data.get("element_type", None)
        if element_type == "2d_element":
            self.comboBox_element_type.setCurrentIndex(0)
        else:
            self.comboBox_element_type.setCurrentIndex(1)

        values = data.get("values", None)
        if "table_paths" in data.keys():
            table_paths = data["table_paths"]
            for index, lineEdit_table in enumerate(self.table_lineEdits.values()):
                table_path = table_paths[index]
                if table_path is not None:                   
                    lineEdit_table.setText(table_path)

        else:
            for index, [lineEdit_real, lineEdit_imag] in enumerate(self.list_lineEdit_constant_values):

                if element_type == "3d_element" and index >= 3:
                    continue
                
                elif index <= 5 and values[index] is not None:
                    lineEdit_real.setText(str(np.real(values[index])))
                    lineEdit_imag.setText(str(np.imag(values[index])))

    def update_formulation_callback(self, **kwargs):

        surface_id = kwargs.get("surface_id", None)
        line_id = kwargs.get("line_id", None)

        if isinstance(surface_id, int):
            data = self.properties._get_property("surface_thickness", surface=surface_id)
            if isinstance(data, dict):
                self.comboBox_element_type.setCurrentIndex(0)
                return
            
        if isinstance(line_id, int):
            for node_id in self.mesh.get_nodes_from_line(line_id):
                for surface_id in self.mesh.get_surfaces_from_node(node_id):
                    data = self.properties._get_property("surface_thickness", surface=surface_id)
                    if isinstance(data, dict):
                        self.comboBox_element_type.setCurrentIndex(0)
                        return

    def attribution_type_callback(self):
        if self.comboBox_attribution_type.currentIndex() == 0:
            unit_label = "[N/m²]"
            load_label = "F{} / area:".format
        else:
            unit_label = "[N/m]"
            load_label = "F{} / length:".format

        self.label_unit_Fx.setText(unit_label)
        self.label_unit_Fy.setText(unit_label)
        self.label_unit_Fz.setText(unit_label)

        self.label_constant_Fx.setText(load_label("x"))
        self.label_constant_Fy.setText(load_label("y"))
        self.label_constant_Fz.setText(load_label("z"))

        self.label_table_Fx.setText(load_label("x"))
        self.label_table_Fy.setText(load_label("y"))
        self.label_table_Fz.setText(load_label("z"))

    def element_type_callback(self):
        return

    def update_element_type_based_on_geometry_information(self):
        volume_exists = self.mesh.are_there_volumes_in_geometry()
        self.comboBox_element_type.setCurrentIndex(int(volume_exists))

    def check_complex_entries(self, real_input: str, imag_input: str, label: str):

        _real = None
        if real_input != "":
            try:
                real_input = real_input.replace(",", ".")
                _real = float(real_input)

            except Exception:
                self.hide()
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([error_title, title, message])
                return True, None

        _imag = None
        if imag_input != "":
            try:
                imag_input = imag_input.replace(",", ".")
                _imag = float(imag_input)

            except Exception:
                self.hide()
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for imaginary part of {label}."
                PrintMessageInput([error_title, title, message])
                return True, None

        if _real is None and _imag is None:
            values = None
        elif _real is None:
            values = 1j * _imag
        elif _imag is None:
            values = complex(_real)
        else:
            values = _real + 1j * _imag

        output = values

        return False, output

    def constant_values_attribution(self):

        input_ids = self.lineEdit_selection_id.text()
        attribution_type = self.comboBox_attribution_type.currentIndex()

        if attribution_type == 0:
            selection = "surfaces"
            unit = "N/m²"

        elif attribution_type == 1:
            selection = "lines"
            unit = "N/m"

        selected_ids, error_data = self.mesh.check_selected_ids(input_ids, selection=selection, single_id=False)

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        self.remove_duplicated_attributions(selected_ids, selection)
        self.remove_conflicting_excitations(selected_ids, selection)

        index = self.comboBox_element_type.currentIndex()
        element_type = self.element_types[index]

        stop, Fx= self.check_complex_entries(self.lineEdit_real_Fx.text(), self.lineEdit_imag_Fx.text(), "Fx")
        if stop:
            return True

        stop, Fy= self.check_complex_entries(self.lineEdit_real_Fy.text(), self.lineEdit_imag_Fy.text(), "Fy")
        if stop:
            return True

        stop, Fz= self.check_complex_entries(self.lineEdit_real_Fz.text(), self.lineEdit_imag_Fz.text(), "Fz")
        if stop:
            return True

        distributed_loads = [Fx, Fy, Fz]

        condition_1 = element_type == "2d_element" and distributed_loads.count(None) == 3
        condition_2 = element_type == "3d_element" and distributed_loads.count(None) == 3

        if condition_1 or condition_2:
            self.hide()
            title = "Additional inputs required"
            message = "You must to enter at least one distributed load value before confirming the assignment."
            PrintMessageInput([error_title, title, message])
            return True

        real_values = [value if value is None else np.real(value) for value in distributed_loads]
        imag_values = [value if value is None else np.imag(value) for value in distributed_loads]

        for selected_id in selected_ids:

            data = {
                "element_type": element_type,
                "values": distributed_loads,
                "real_values": real_values,
                "imag_values": imag_values,
                "unit": unit,
            }

            if attribution_type == 0:
                self.properties._set_property("distributed_loads", data, surface=selected_id)

            elif attribution_type == 1:
                self.properties._set_property("distributed_loads", data, line=selected_id)

    def load_table(self, lineEdit : QLineEdit, load_label: str, direct_load = False):

        title = "Error while loading table"
        imported_file = None
        try:
            if direct_load:
                if lineEdit.text() == "":
                    return None, None

                imported_table_path = lineEdit.text()
                imported_file = DataImporter.read_data_in_file(imported_table_path)[0].data

            else:
                imported_data = DataImporter.import_single_file("imported_table_folder",
                    ["csv", "dat", "txt", "xlsx", "xls"], f"Choose a table to import the {load_label} data")
                
                if not imported_data:
                    return None, None

                imported_file = imported_data.data
                lineEdit.setText(imported_data.path)
                imported_table_path = imported_data.path

            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum "
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([error_title, title, message])
                lineEdit.setFocus()
                return None, None

            imported_values = imported_file[:, 1] + 1j * imported_file[:, 2]
            self.frequencies = imported_file[:, 0]

            return imported_values, imported_table_path

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            lineEdit.setFocus()
            return None, None

    def lineEdit_reset(self, lineEdit: QLineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def load_Fx_table(self):
        self.Fx_table_values, self.Fx_table_path = self.load_table(self.lineEdit_path_table_Fx, "Fx")
        if  self.Fx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Fx)

    def load_Fy_table(self):
        self.Fy_table_values, self.Fy_table_path = self.load_table(self.lineEdit_path_table_Fy, "Fy")
        if self.Fy_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Fy)
            
    def load_Fz_table(self):
        self.Fz_table_values, self.Fz_table_path = self.load_table(self.lineEdit_path_table_Fz, "Fz")
        if self.Fz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Fz)

    def save_table_files(self, load_label: str, selected_id: int, selection: str, values: np.ndarray):

        if self.frequencies[0] == 0:
            self.frequencies[0] = float(1e-6)

        if self.frequencies[0] == float(1e-6):
            self.frequencies[0] = 0

        if self.model.change_analysis_frequency_setup(list(self.frequencies)):

            self.hide()
            lineEdit = self.table_lineEdits[load_label]
            imported_filename = basename(lineEdit.text())
            self.lineEdit_reset(lineEdit)

            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup"
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\nFile name: {imported_filename}"
            PrintMessageInput([error_title, title, message])

            return None, None

        table_name = f"distributed_loads_{load_label}_from_{selection[:-1]}_{selected_id}"

        real_values = np.real(values)
        imag_values = np.imag(values)
        data = np.array([self.frequencies, real_values, imag_values], dtype=float).T

        update_analysis_setup_in_file(self.frequencies)

        self.properties.add_imported_tables("structural", table_name, data)

        return table_name, data

    def table_values_attribution(self):

        input_ids = self.lineEdit_selection_id.text()
        attribution_type = self.comboBox_attribution_type.currentIndex()

        if attribution_type == 0:
            selection = "surfaces"
            unit = "N/m²"

        elif attribution_type == 1:
            selection = "lines"
            unit = "N/m"

        selected_ids, error_data = self.mesh.check_selected_ids(input_ids, selection=selection, single_id=False)

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            PrintMessageInput(error_data)
            return True

        self.remove_duplicated_attributions(selected_ids, selection)
        self.remove_conflicting_excitations(selected_ids, selection)

        index = self.comboBox_element_type.currentIndex()
        element_type = self.element_types[index]

        if self.Fx_table_path is None:
            self.Fx_table_values, self.Fx_table_path = self.load_table(self.lineEdit_path_table_Fx, "Fx", direct_load = True)

        if self.Fy_table_path is None:
            self.Fy_table_values, self.Fy_table_path = self.load_table(self.lineEdit_path_table_Fy, "Fy", direct_load = True)

        if self.Fz_table_path is None:
            self.Fz_table_values, self.Fz_table_path = self.load_table(self.lineEdit_path_table_Fz, "Fz", direct_load = True)

        for selected_id in selected_ids:
            
            if self.Fx_table_values is not None:
                self.Fx_table_name, self.Fx_array = self.save_table_files("Fx", selected_id, selection, self.Fx_table_values)
                if self.Fx_array is None:
                    return True

            if self.Fy_table_values is not None:
                self.Fy_table_name, self.Fy_array = self.save_table_files("Fy", selected_id, selection, self.Fy_table_values)
                if self.Fy_array is None:
                    return True

            if self.Fz_table_values is not None:
                self.Fz_table_name, self.Fz_array = self.save_table_files("Fz", selected_id, selection, self.Fz_table_values)
                if self.Fz_array is None:
                    return True

            table_names = [self.Fx_table_name, self.Fy_table_name, self.Fz_table_name]
            table_paths = [self.Fx_table_path, self.Fy_table_path, self.Fz_table_path]
            distributed_loads = [self.Fx_table_values, self.Fy_table_values, self.Fz_table_values]

            condition_1 = element_type == "2d_element" and table_names.count(None) == 3
            condition_2 = element_type == "3d_element" and table_names.count(None) == 3

            if condition_1 or condition_2:
                self.hide()
                title = "Additional inputs required"
                message = "You must to enter at leat one distributed load table path before confirming the assignment."
                PrintMessageInput([error_title, title, message]) 
                return True

            data = {
                "element_type" : element_type,
                "table_names" : table_names,
                "table_paths" : table_paths,
                "values" : distributed_loads,
                "unit" : unit,
            }

            if attribution_type == 0:
                self.properties._set_property("distributed_loads", data, surface=selected_id)

            elif attribution_type == 1:
                self.properties._set_property("distributed_loads", data, line=selected_id)

        self.reset_table_variables()

    def remove_duplicated_attributions(self, selected_ids: list, selection: str):

        table_names = list()
        for selected_id in selected_ids:

            if selection == "surfaces":
                for line_id in self.mesh.lines_from_surface[selected_id]:
                    data = self.properties._get_property("distributed_loads", line=line_id)
                    if isinstance(data, dict):
                        self.properties._remove_line_property("distributed_loads", line_id)
                        table_names.extend(self.properties.get_property_related_table_names("distributed_loads", line_id, "lines"))

            elif selection == "lines":
                for surface_id in self.mesh.surfaces_from_line[selected_id]:
                    data = self.properties._get_property("distributed_loads", surface=surface_id)
                    if isinstance(data, dict):
                        self.properties._remove_surface_property("distributed_loads", surface_id)
                        table_names.extend(self.properties.get_property_related_table_names("distributed_loads", surface_id, "surfaces"))

            self.process_table_file_removal(table_names)

    def apply_callback(self, close_window: bool=False):

        if self.tabWidget_main.currentIndex() == StandardTabType.LIST:
            return

        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == StandardTabType.CONSTANT_DATA:
            if self.constant_values_attribution():
                return

        elif tab_index == StandardTabType.TABULAR_DATA:
            if self.table_values_attribution():
                return

        self.actions_to_finalize(close_window)

    def text_label(self, mask):

        load_labels = np.array(['Fx','Fy','Fz'])
        labels = load_labels[mask]

        if list(mask).count(True) == 3:
            return "[{}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 2:
            return "[{}, {}]".format(*labels)
        elif list(mask).count(True) == 1:
            return "[{}]".format(*labels)

    def load_model_info(self):

        self.treeWidget_distributed_loads.clear()
        for (property, *args), data in self.properties.surface_properties.items():

            if property == "distributed_loads":
                values = data["values"]
                element_type = data["element_type"]
                constrained_loads_mask = [False if value is None else True for value in values]
                dof_labels = str(self.text_label(constrained_loads_mask))
                new = QTreeWidgetItem([f"Surface-{args[0]}", dof_labels, element_type])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_distributed_loads.addTopLevelItem(new)

        for (property, *args), data in self.properties.line_properties.items():

            if property == "distributed_loads":
                values = data["values"]
                element_type = data["element_type"]
                constrained_loads_mask = [False if value is None else True for value in values]
                dof_labels = str(self.text_label(constrained_loads_mask))
                new = QTreeWidgetItem([f"Line-{args[0]}", dof_labels, element_type])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_distributed_loads.addTopLevelItem(new)

        for (property, *args), data in self.properties.point_properties.items():

            if property == "distributed_loads":
                values = data["values"]
                element_type = data["element_type"]
                constrained_loads_mask = [False if value is None else True for value in values]
                dof_labels = str(self.text_label(constrained_loads_mask))
                new = QTreeWidgetItem([f"Point-{args[0]}", dof_labels, element_type])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_distributed_loads.addTopLevelItem(new)

        for (property, *args), data in self.properties.nodal_properties.items():

            if property == "distributed_loads":
                values = data["values"]
                element_type = data["element_type"]
                constrained_loads_mask = [False if value is None else True for value in values]
                dof_labels = str(self.text_label(constrained_loads_mask))
                new = QTreeWidgetItem([f"Node-{args[0]}", dof_labels, element_type])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_distributed_loads.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        properties_to_check = [
                               self.properties.surface_properties,
                               self.properties.line_properties,
                               self.properties.point_properties,
                               self.properties.nodal_properties,
                               ]

        for current_property in properties_to_check:
            for (property, _) in current_property.keys():
                if property == "distributed_loads":
                    self.tabWidget_main.setTabVisible(StandardTabType.LIST, True)
                    return

        self.tabWidget_main.setTabVisible(StandardTabType.LIST, False)
        self.tabWidget_main.setCurrentIndex(StandardTabType.CONSTANT_DATA)
        self.lineEdit_real_Fx.setFocus()
        app().main_window.selection.set_geometry_selection()

    def tab_event_callback(self):
        list_tab = self.tabWidget_main.currentIndex() == StandardTabType.LIST
        self.lineEdit_selection_id.setDisabled(list_tab)
        self.pushButton_apply.setDisabled(list_tab)
        self.pushButton_apply_and_close.setDisabled(list_tab)
        self.pushButton_remove.setDisabled(True)

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
                app().main_window.selection.set_geometry_selection(surfaces = [int(selected_id)])

            elif selection == "Line":
                app().main_window.selection.set_geometry_selection(lines = [int(selected_id)])

            # app().main_window.action_model_workspace_callback()
            self.lineEdit_selection_id.setText(item.text(0))

    def on_double_click_item(self, item):
        self.on_click_item(item)

    def process_table_file_removal(self, table_names: list):

        if len(table_names) == 0:
            return

        for table_name in table_names:
            self.properties.remove_imported_tables("structural", table_name)

        app().project.update_model_properties_file()

    def remove_conflicting_excitations(self, selected_ids: int | list, selection: str):

        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        if selection == "surfaces":
            remove_function = self.properties._remove_surface_property

        elif selection == "lines":
            remove_function = self.properties._remove_line_property

        properties = ["distributed_loads", "prescribed_dof"]

        for selected_id in selected_ids:
            for property in properties:
                table_names = self.properties.get_property_related_table_names(property, selected_id, selection)
                remove_function(property, selected_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from(self, selected_id : list, selection: str):
        table_names = self.properties.get_property_related_table_names("distributed_loads", selected_id, selection)
        self.process_table_file_removal(table_names)

    def remove_callback(self):

        text = self.lineEdit_selection_id.text()

        if "-" in text:

            selection, _selected_id = text.split("-")
            selected_id = int(_selected_id)

            if selection == "Surface":
                self.properties._remove_surface_property("distributed_loads", selected_id)

            elif selection == "Line":
                self.properties._remove_line_property("distributed_loads", selected_id)

            elif selection == "Point":
                self.properties._remove_point_property("distributed_loads", selected_id)

            elif selection == "Node":
                self.properties._remove_nodal_property("distributed_loads", selected_id)

            self.remove_table_files_from(selected_id, f"{selection.lower()}s")
            self.actions_to_finalize()

            app().main_window.selection.set_geometry_selection()
            app().main_window.selection.set_mesh_selection()

    def reset_callback(self):

        self.hide()

        title = "Distributed loads resetting"
        message = "Would you like to remove the all distributed loads from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if obj._cancel:
            return

        if obj._continue:

            for (property, *args) in self.properties.surface_properties.keys():
                if property == "distributed_loads":
                    self.remove_table_files_from(args[0], "surfaces")

            for (property, *args) in self.properties.line_properties.keys():
                if property == "distributed_loads":
                    self.remove_table_files_from(args[0], "lines")

            self.properties._reset_property("distributed_loads")
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

    def reset_input_fields(self, reset_all=False):

        if reset_all:
            self.lineEdit_selection_id.setText("")

        for lineEdit_real, lineEdit_imag in self.list_lineEdit_constant_values:
            lineEdit_real.setText("")
            lineEdit_imag.setText("")

        for lineEdit_table in self.table_lineEdits.values():
            lineEdit_table.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)