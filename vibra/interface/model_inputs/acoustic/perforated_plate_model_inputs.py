from PySide6.QtWidgets import QFileDialog, QLineEdit, QTreeWidgetItem
from PySide6.QtCore import Qt, QEvent, QObject, Signal
from PySide6.QtGui import QCloseEvent, QColor

from vibra import app
from vibra.interface.formatters.icons import change_icon_color_for_widgets
from vibra.interface.ui_generated.model.setup.acoustic.perforated_plate_model_inputs_ui import PerforatedPlateModelInputs_UI
from vibra.engine.properties.fluid import Fluid
from vibra.engine.transfer_impedances.perforated_plate_models import PerforatedPlateModels
from vibra.interface.model_inputs.acoustic.fluid.simplified_fluid_inputs import SimplifiedFluidInputs
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.message.loading_window import LoadTask

from copy import deepcopy

import logging, os, warnings
import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class PerforatedPlateModelInputs(PerforatedPlateModelInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.action_model_workspace_callback()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._config_widgets()
        self._create_connections()
        self._paint_icons()

        self.load_model_info()

        while self.keep_window_open:
            self.exec()

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
        self.pp_data = dict()

    def _create_connections(self):
        #
        self.comboBox_plot_type.currentIndexChanged.connect(self.plot_type_callback)
        self.comboBox_include_effects.currentIndexChanged.connect(self.include_effects_callback)
        self.comboBox_selection_type.currentIndexChanged.connect(self.selection_type_callback)
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.attribute_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_load_path.clicked.connect(self.load_user_defined_transfer_impedance)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        self.pushButton_clean_inputs.clicked.connect(self.clear_all_inputs)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_perforated_plate_model.itemClicked.connect(self.on_click_item)
        self.treeWidget_perforated_plate_model.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
        self.main_window.theme_changed.connect(self._paint_icons)
        #
        self.clickable(self.lineEdit_selection_id_A).connect(self.lineEdit_selection_A_clicked)
        self.clickable(self.lineEdit_selection_id_B).connect(self.lineEdit_selection_B_clicked)
        #
        self.geometry_selection_callback()
        self.include_effects_callback()
        self.selection_type_callback()

    def clickable(self, widget: QLineEdit):
        class Filter(QObject):
            clicked = Signal()

            def eventFilter(self, obj, event):
                if obj == widget and event.type() == QEvent.MouseButtonRelease and obj.rect().contains(event.pos()):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def lineEdit_selection_A_clicked(self):
        app().main_window.set_geometry_selection()
        self.current_line_edit = self.lineEdit_selection_id_A
        self.highlight_line_edit()

    def lineEdit_selection_B_clicked(self):
        app().main_window.set_geometry_selection()
        if self.lineEdit_selection_id_B.isEnabled():
            self.current_line_edit = self.lineEdit_selection_id_B
            self.highlight_line_edit()

    def highlight_line_edit(self):
        self.current_line_edit.setStyleSheet("border-color: rgb(255,0,0); border-width: 2px")
        if self.current_line_edit == self.lineEdit_selection_id_A:
            self.lineEdit_selection_id_B.setStyleSheet("")
        else:
            self.lineEdit_selection_id_A.setStyleSheet("")

    def geometry_selection_callback(self):

        if self.tabWidget_main.currentIndex() == 1:
            return

        surfaces = self.main_window.selected_geometry_surfaces
        if surfaces:

            if len(surfaces) == 1:
                surface_ids = list(surfaces)[0]
            elif len(surfaces) > 1:
                surface_ids = list(surfaces)
                surface_ids.sort()
                surface_ids = tuple(surface_ids)
            else:
                return

            self.update_selected_ids(surface_ids)
            # self.update_selection_type_based_on_surface_ids(surface_ids)

            pp_data = self.properties._get_property("perforated_plate_model", surface=surface_ids)
            if pp_data is None:
                return

            self.load_perforated_plate_inputs(pp_data)

    def update_selection_type_based_on_surface_ids(self, surface_ids: int | tuple[int]):

        if isinstance(surface_ids, int | np.int64):
            if len(self.mesh.volumes_from_surface[surface_ids]) == 2:
                self.comboBox_selection_type.setCurrentIndex(0)

        elif isinstance(surface_ids, tuple):
            if len(surface_ids) == 2:
                volumes_from_surface_A = self.mesh.volumes_from_surface[surface_ids[0]]
                volumes_from_surface_B = self.mesh.volumes_from_surface[surface_ids[1]]
                if len(volumes_from_surface_A) == len(volumes_from_surface_B) == 1:
                    self.comboBox_selection_type.setCurrentIndex(1)

        else:
            return

    def update_selected_ids(self, surface_ids: int | tuple[int]):

        if isinstance(surface_ids, int | np.int64):
            surface_ids = [surface_ids]

        text = ", ".join([str(i) for i in surface_ids])
        self.current_line_edit.setText(text)

    def clear_all_inputs(self):
        self.lineEdit_plate_thickness.setText("")
        self.lineEdit_hole_diameter.setText("")
        self.lineEdit_porosity.setText("")
        self.lineEdit_linear_discharge_coefficient.setText("")
        self.lineEdit_non_linear_discharge_coefficient.setText("")
        self.lineEdit_non_linear_correction_factor.setText("")
        self.lineEdit_user_defined_transfer_impedance_path.setText("")

    def update_plot_buttons_access(self):
        state = self.selected_fluid is None
        self.comboBox_plot_type.setDisabled(state)
        self.plot_type_callback()

    def selection_type_callback(self):
        if self.comboBox_selection_type.currentText() == "Inside surfaces":
            self.label_selection_B.setEnabled(False)
            self.lineEdit_selection_id_B.setEnabled(False)
        else:
            self.label_selection_B.setEnabled(True)
            self.lineEdit_selection_id_B.setEnabled(True)

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
        #
        self.current_line_edit = self.lineEdit_selection_id_A
        #
        for i, w in enumerate([120, 130, 200]):
            self.treeWidget_perforated_plate_model.setColumnWidth(i, w)
            self.treeWidget_perforated_plate_model.headerItem().setTextAlignment(i, Qt.AlignCenter)
        
    def _paint_icons(self):
        icon_color = None
        theme = app().config.user_preferences.interface_theme
        
        if theme == "dark":
            icon_color = QColor("#5f9af4")
        else:
            icon_color = QColor("#1a73e8")

        widgets = [self.pushButton_clean_inputs, self.pushButton_load_path]
        change_icon_color_for_widgets(widgets, icon_color)


    def tab_event_callback(self):

        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 1:
            self.lineEdit_selection_id_A.setText("")
            self.lineEdit_selection_id_B.setText("")
            self.lineEdit_selection_id_A.setDisabled(True)

        else:

            if ("(" or ")") in self.lineEdit_selection_id_A.text():
                self.lineEdit_selection_id_A.setText("")
                self.lineEdit_selection_id_B.setText("")
                app().main_window.set_geometry_selection()

            else:
                self.geometry_selection_callback()

            self.lineEdit_selection_id_A.setDisabled(False)

    def on_click_item(self, item):

        self.pushButton_remove.setEnabled(True)
        self.lineEdit_selection_id_A.setText(item.text(0))

        text = item.text(0).replace("(", "").replace(")", "").replace(",", "")
        str_surface_ids = text.split()
        surface_ids = [int(surf_id) for surf_id in str_surface_ids]

        app().main_window.set_geometry_selection(surfaces=surface_ids)

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def check_selection_type(self, surface_ids: list[int]):

        title = "Invalid selection detected"

        selection_type = self.comboBox_selection_type.currentText()
        if selection_type == "Inside surfaces":
            for surface_id in surface_ids:
                if len(self.mesh.volumes_from_surface[surface_id]) != 2:
                    self.hide()
                    message = f"The selected surface ID #{surface_id} does not correspond to an inside surface "
                    message += "(surfaces that connect two neighboohrs volumes). The perforated plate "
                    message += "assignment will be ignored until all requirements are met."
                    PrintMessageInput([window_title_1, title, message])
                    self.pp_data.clear()
                    return

        else:

            for surface_id in surface_ids:
                if len(self.mesh.volumes_from_surface[surface_id]) != 1:
                    self.hide()
                    message = f"The selected surface ID #{surface_id} does not correspond to an outside surface. "
                    message += "Outside surfaces are surfaces associated to only one volume. The perforated plate "
                    message += "attribution will be ignored until all requirements are met."
                    PrintMessageInput([window_title_1, title, message])
                    self.pp_data.clear()
                    return

        self.pp_data["coupling_type"] = selection_type.lower().replace(" ", "_")

    def load_model_info(self):

        self.treeWidget_perforated_plate_model.clear()

        for key, data in self.properties.surface_properties.items():

            property, surface_id = key
            if property == "perforated_plate_model":
                data: dict

                model_inputs = list()
                for key, value in data.items():

                    if key in ["formulation", "fluid_data", "values", "table_names", "table_paths"]:
                        continue

                    if key == "coupling_type":
                        coupling_type = data.get("coupling_type")
                    else:
                        model_inputs.append(value)

                new = QTreeWidgetItem([str(surface_id), coupling_type, str(model_inputs)])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_perforated_plate_model.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        for key, _ in self.properties.surface_properties.items():
            property, _ = key
            if property == "perforated_plate_model":
                self.tabWidget_main.setTabVisible(1, True)
                return

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_main.setTabVisible(1, False)

    def load_perforated_plate_inputs(self, data: dict):

        surfaces_A = data.get("surfaces_A")
        if isinstance(surfaces_A, list):
            self.current_line_edit = self.lineEdit_selection_id_A
            self.update_selected_ids(surfaces_A)

        surfaces_B = data.get("surfaces_B")
        if isinstance(surfaces_B, list):
            self.current_line_edit = self.lineEdit_selection_id_B
            self.update_selected_ids(surfaces_B)

        formulation = data.get("formulation")
        if formulation == "circular_hole":
            self.tabWidget_perforated_plate_models.setCurrentIndex(0)

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
                self.comboBox_include_effects.setCurrentIndex(1)

            self.pushButton_load_path.setEnabled(False)
            self.lineEdit_user_defined_transfer_impedance_path.setText("")
            self.lineEdit_user_defined_transfer_impedance_path.setToolTip("")
            self.lineEdit_user_defined_transfer_impedance_path.setEnabled(False)

        elif isinstance(table_path, list):
            if self.lineEdit_non_linear_discharge_coefficient.isEnabled():
                self.comboBox_include_effects.setCurrentIndex(3)
            else:
                self.comboBox_include_effects.setCurrentIndex(2)

            self.pushButton_load_path.setEnabled(True)
            self.lineEdit_user_defined_transfer_impedance_path.setEnabled(True)
            self.lineEdit_user_defined_transfer_impedance_path.setText(table_path[0])
            self.lineEdit_user_defined_transfer_impedance_path.setToolTip(table_path[0])

    def load_table(self, lineEdit : QLineEdit, direct_load: bool=False):

        title = "Error reached while loading 'user-defined transfer impedance' table"

        try:
            if direct_load:
                imported_table_path = lineEdit.text()

            else:

                last_path = app().config.get_last_folder_for("imported_table_folder")
                if last_path is None:
                    path = os.path.expanduser("~")
                else:
                    path = last_path

                caption = "Choose a table to import the user-defined transfer impedance"
                imported_table_path, check = QFileDialog.getOpenFileName(  None, 
                                                                            caption, 
                                                                            path, 
                                                                            "Files (*.csv; *.dat; *.txt)"
                                                                        )

                if not check:
                    return None

            lineEdit.setText(imported_table_path)
            lineEdit.setToolTip(f"User-defined normalized transfer impedance table path: {imported_table_path}")
            app().config.write_last_folder_path_in_file("imported_table_folder", imported_table_path)

            imported_values = np.loadtxt(imported_table_path, delimiter=",")

            if imported_values.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have three columns in the form: frequencies, real and imaginary values."
                PrintMessageInput([window_title_1, title, message])
                return None

            mask = imported_values[:, 0] > 0

            return imported_values[mask, :]

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            lineEdit.setFocus()
            return None

    def load_user_defined_transfer_impedance(self):
        self.imported_values = self.load_table(self.lineEdit_user_defined_transfer_impedance_path)

    def save_table_values(self, table_name: str, imported_values: np.ndarray):

        _frequencies = imported_values[:, 0]

        if app().project.model.change_analysis_frequency_setup(list(_frequencies)):
            self.hide()
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([window_title_1, title, message])
            return True

        self.update_analysis_setup_in_file(_frequencies)

        real_values = imported_values[:, 1]
        imag_values = imported_values[:, 2]

        data = np.array([_frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def update_analysis_setup_in_file(self, frequencies: np.ndarray):

        analysis_setup = app().project.file.read_analysis_setup_from_file()
        if analysis_setup is None:
            analysis_setup = dict()

        f_min = frequencies[0]
        f_max = frequencies[-1]
        f_step = frequencies[1] - frequencies[0] 

        analysis_setup["f_min"] = float(f_min)
        analysis_setup["f_max"] = float(f_max)
        analysis_setup["f_step"] = float(f_step)

        app().project.set_analysis_setup(analysis_setup)
        app().project.file.write_analysis_setup_in_file(analysis_setup)

    def get_inputs_for_perforated_plate_with_circular_holes(self):

        if self.tabWidget_perforated_plate_models.currentIndex() != 0:
            return dict()
        
        if self.selected_fluid is None:
            self.get_fluid_callback()

        if not isinstance(self.selected_fluid, Fluid):
            return dict()

        self.pp_data["fluid_data"] = dict(
                                          name = self.selected_fluid.name,
                                          fluid_density = self.selected_fluid.fluid_density,
                                          speed_of_sound = self.selected_fluid.speed_of_sound,
                                          isentropic_exponent = self.selected_fluid.isentropic_exponent,
                                          thermal_conductivity = self.selected_fluid.thermal_conductivity,
                                          specific_heat_Cp = self.selected_fluid.specific_heat_Cp,
                                          dynamic_viscosity = self.selected_fluid.dynamic_viscosity,
                                          temperature = self.selected_fluid.temperature,
                                          pressure = self.selected_fluid.pressure,
                                          molar_mass = self.selected_fluid.molar_mass,
                                          )

        lineEdit = self.lineEdit_plate_thickness
        plate_thickness = self.check_inputs(lineEdit, "Plate thickness")
        if plate_thickness is None:
            lineEdit.setFocus()
            return dict()

        lineEdit = self.lineEdit_hole_diameter
        hole_diameter = self.check_inputs(lineEdit, "Hole diameter")
        if hole_diameter is None:
            lineEdit.setFocus()
            return dict()

        lineEdit = self.lineEdit_porosity
        porosity = self.check_inputs(lineEdit, "Porosity")
        if porosity is None:
            lineEdit.setFocus()
            return dict()

        lineEdit = self.lineEdit_linear_discharge_coefficient
        linear_discharge_coefficient = self.check_inputs(lineEdit, "Linear discharge coefficient")
        if linear_discharge_coefficient is None:
            lineEdit.setFocus()
            return dict()

        pp_data_general = dict(
                                formulation = "circular_hole",
                                plate_thickness = plate_thickness,
                                hole_diameter = hole_diameter,
                                porosity = porosity,
                                linear_discharge_coefficient = linear_discharge_coefficient,
                                )

        self.pp_data.update(pp_data_general)

        if "Non-linear" in self.comboBox_include_effects.currentText():

            lineEdit = self.lineEdit_non_linear_discharge_coefficient
            non_linear_discharge_coefficient = self.check_inputs(lineEdit, "Non-linear discharge coefficient")
            if non_linear_discharge_coefficient is None:
                lineEdit.setFocus()
                return dict()

            lineEdit = self.lineEdit_non_linear_correction_factor
            non_linear_correction_factor = self.check_inputs(lineEdit, "Non-linear correction factor")
            if non_linear_correction_factor is None:
                lineEdit.setFocus()
                return dict()

            self.pp_data["non_linear_discharge_coefficient"] = non_linear_discharge_coefficient
            self.pp_data["non_linear_correction_factor"] = non_linear_correction_factor

    def check_selected_surfaces(self):

        surface_ids = list()
        if self.comboBox_selection_type.currentText() == "Inside surfaces":

            input_ids_A = self.lineEdit_selection_id_A.text()
            surface_ids, error_data = self.mesh.check_selected_ids(
                                                                    input_ids_A,
                                                                    selection = "surfaces",
                                                                    single_id = False,
                                                                    )

            if error_data is not None:
                self.hide()
                self.lineEdit_selection_id_A.setFocus()
                PrintMessageInput(error_data)
                return list()

            self.check_selection_type(surface_ids)
            if not self.pp_data:
                return list()

            surface_ids.sort()

        else:

            input_ids_A = self.lineEdit_selection_id_A.text()
            surface_ids_A, error_data = self.mesh.check_selected_ids(
                                                                     input_ids_A, 
                                                                     selection = "surfaces", 
                                                                     single_id = False,
                                                                     )

            if error_data is not None:
                self.hide()
                self.lineEdit_selection_id_A.setFocus()
                PrintMessageInput(error_data)
                return list()

            input_ids_B = self.lineEdit_selection_id_B.text()
            surface_ids_B, error_data = self.mesh.check_selected_ids(
                                                                     input_ids_B, 
                                                                     selection = "surfaces", 
                                                                     single_id = False,
                                                                     )

            if error_data is not None:
                self.hide()
                self.lineEdit_selection_id_B.setFocus()
                PrintMessageInput(error_data)
                return list()

            self.check_selection_type(surface_ids_A)
            if not self.pp_data:
                return list()

            self.check_selection_type(surface_ids_B)
            if not self.pp_data:
                return list()

            surface_ids_A.sort()
            surface_ids_B.sort()
            self.pp_data["surfaces_A"] = surface_ids_A
            self.pp_data["surfaces_B"] = surface_ids_B
            surface_ids.extend(surface_ids_A)
            surface_ids.extend(surface_ids_B)

        surface_ids.sort()

        return surface_ids

    def attribute_callback(self):

        self.pp_data.clear()
        if self.tabWidget_main.currentIndex():
            return

        surface_ids = self.check_selected_surfaces()
        if not surface_ids:
            return

        self.remove_conflicting_excitations(surface_ids)
        self.get_inputs_for_perforated_plate_with_circular_holes()

        if not self.pp_data:
            return

        if self.pp_data.get("coupling_type") == "inside_surfaces":

            for surface_id in surface_ids:
                if "User-defined" in self.comboBox_include_effects.currentText():
                    self.include_user_defined_transfer_impedance(surface_id)
                    if not self.pp_data:
                        return

                pp_data = deepcopy(self.pp_data)
                self.properties._set_property("perforated_plate_model", pp_data, surface=surface_id)
                self.decouple_degrees_of_freedom(surface_id)

        else:

            if "User-defined" in self.comboBox_include_effects.currentText():
                self.include_user_defined_transfer_impedance(surface_ids)
                if not self.pp_data:
                    return

            pp_data = deepcopy(self.pp_data)
            self.properties._set_property("perforated_plate_model", self.pp_data, surface=tuple(surface_ids))

        self.assignment_complete = True
        self.lineEdit_selection_id_A.setText("")
        self.lineEdit_selection_id_B.setText("")

        self.hide()
        self.actions_to_finalize()

    def include_user_defined_transfer_impedance(self, surface_id: int | list[int]):

        if self.imported_values is None:
            self.imported_values = self.load_user_defined_transfer_impedance()

        if self.imported_values is None:
            self.pp_data.clear()
            return

        if not isinstance(self.imported_values, np.ndarray):
            self.pp_data.clear()
            return

        if self.imported_values.shape[1] < 3:
            self.pp_data.clear()
            return

        if self.imported_values[0, 0] == 0:
            self.imported_values = self.imported_values[1:, :]

        if isinstance(surface_id, int):
            table_name = f"user_defined_transfer_impedance_at_surface_{surface_id}"
        else:
            table_name = f"user_defined_transfer_impedance_between_surfaces_{surface_id[0]}_{surface_id[1]}"

        if self.save_table_values(table_name, self.imported_values):
            self.lineEdit_user_defined_transfer_impedance_path.setFocus()
            self.imported_values = None
            self.pp_data.clear()
            return

        complex_values = self.imported_values[:, 1] + 1j * self.imported_values[:, 2]
        table_path = self.lineEdit_user_defined_transfer_impedance_path.text()

        self.pp_data["table_names"] = [table_name]
        self.pp_data["table_paths"] = [table_path]
        self.pp_data["values"] = [complex_values]

    def decouple_degrees_of_freedom(self, surface_id: int):

        volumes_from_surface = self.mesh.volumes_from_surface.get(surface_id)
        if volumes_from_surface is None:
            return 

        volume_id = volumes_from_surface[0]
        data = {"volume_to_decouple" : volume_id}
        self.properties._set_property("degrees_of_freedom_decoupling", data, surface=surface_id)

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().project.file.write_imported_table_data_in_file()

    def remove_conflicting_excitations(self, surface_ids: int | list[int]):

        if self.comboBox_selection_type.currentText() == "Inside surfaces":
            if isinstance(surface_ids, int):
                surface_ids = [surface_ids]
        else:
            surface_ids = [tuple(surface_ids)]

        labels = ["perforated_plate_model", "interior_impedance"]

        for surface_id in surface_ids:
            for label in labels:
                table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
                self.properties._remove_surface_property(label, surface_id)
                self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_ids : int | tuple[int]):
        table_names = self.properties.get_property_related_table_names("perforated_plate_model", surface_ids, "surfaces")
        self.process_table_file_removal(table_names)

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
                for (property, line_id) in line_properties.keys():
                    if line_from_surface == line_id:
                        self.properties._remove_line_property(property, line_id)

    def remove_callback(self):

        input_ids = self.lineEdit_selection_id_A.text()

        if input_ids != "":
            input_ids = input_ids.replace("(", "").replace(")", "")
            surface_ids, error_data = self.mesh.check_selected_ids(
                                                                   input_ids, 
                                                                   selection = "surfaces", 
                                                                   single_id = False,
                                                                   )

            if error_data is not None:
                self.hide()
                self.lineEdit_selection_id_A.setFocus()
                PrintMessageInput(error_data)
                return

            if len(surface_ids) == 1:
                surface_ids = surface_ids[0]
            else:
                surface_ids = tuple(surface_ids)

            self.remove_table_files_from_surfaces(surface_ids)
            self.properties._remove_surface_property("perforated_plate_model", surface_ids)

            data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_ids)
            if isinstance(data, dict):
                new_surface_id = data.get("new_surface_id")
                if isinstance(new_surface_id, int):   
                    self.remove_all_surface_properties_from_surface([new_surface_id])
                    self.remove_all_line_properties_boundind_surface([new_surface_id]) 

                self.properties._remove_surface_property("degrees_of_freedom_decoupling", surface_ids)

            self.hide()
            self.actions_to_finalize()
            self.restore_mesh_data_modified_by_decoupling()
            self.pushButton_remove.setDisabled(True)

    def reset_callback(self):

        surface_ids = list()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "perforated_plate_model":
                surface_ids.append(surface_id)

        if not surface_ids:
            return

        self.hide()

        title = "Perforated plate model resetting"
        message = "Would you like to remove the perforated plate from the acoustic model?"

        buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        new_surface_ids = list()
        for surf_id in surface_ids:
            self.remove_table_files_from_surfaces(surf_id)
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

    def actions_to_finalize(self):

        def callback():

            logging.info("Processing the post-assignment actions... [10/100]")
            self.load_model_info()

            logging.info("Processing the post-assignment actions... [20/100]")
            app().project.reset_solutions()

            logging.info("Processing the post-assignment actions... [30/100]")
            app().project.file.remove_mesh_data_from_project_file()

            logging.info("Processing the post-assignment actions... [40/100]")
            app().project.file.remove_results_data_from_project_file()

            logging.info("Processing the post-assignment actions... [50/100]")
            app().project.file.write_model_properties_in_file()

            logging.info("Processing the post-assignment actions... [60/100]")
            app().project.file.write_imported_table_data_in_file()

            logging.info("Processing the post-assignment actions... [70/100]")
            app().main_window.recompute_hidden_volumes()

            logging.info("Processing the post-assignment actions... [80/100]")
            app().main_window.update_info_text()

            logging.info("Processing the post-assignment actions... [95/100]")
            app().main_window.set_geometry_selection()

            logging.info("Processing the post-assignment actions... [100/100]")
            app().main_window.analysis_toolbar.pushButton_reset_solution.setDisabled(True)

        LoadTask(callback, use_threads=False).run()

    def process_decoupling_actions(self):

        def callback():
            logging.info("Processing degress of freedom decoupling... [10/100]")
            self.model.process_degrees_of_freedom_decoupling()

            logging.info("Processing degress of freedom decoupling... [70/100]")
            app().project.file.write_mesh_data_in_file()
            
            logging.info("Processing degress of freedom decoupling... [75/100]")
            app().project.file.write_geometry_data_in_file()

            # the degrees of freedom modifies the surfaces properties
            logging.info("Processing degress of freedom decoupling... [80/100]")
            app().project.file.write_model_properties_in_file()

            logging.info("Processing degress of freedom decoupling... [85/100]")
            app().main_window.update_mesh_information()

            logging.info("Processing degress of freedom decoupling... [90/100]")
            app().main_window.update_geometry_information()
        
            logging.info("Processing degress of freedom decoupling... [95/100]")
            app().main_window.update_plots()

        LoadTask(callback, use_threads=False).run()

    def restore_mesh_data_modified_by_decoupling(self):

        if self.mesh.cache_nodal_coordinates is None:
            return

        self.mesh.restore_data_from_cache()
        self.mesh.process_upwards_adjacencies_from_entities()

        if self.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):
            self.mesh.cache_mesh_information()

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
                message = f"You have typed and invalid value at the {label} input field.\n\n"
                message += str(_err)

        else:
            message = f"Insert some value at the {label} input field."

        if message != "":
            self.hide()
            PrintMessageInput([window_title_1, title, message])
            return None
        else:
            return out

    def get_fluid_callback(self):
        self.hide()
        self.fluid_dialog = SimplifiedFluidInputs()
        self.fluid_dialog.fluid_widget.pushButton_attribute.setText("Select fluid")
        self.fluid_dialog.pushButton_attribute.clicked.connect(self.get_selected_fluid)
        self.fluid_dialog.exec()
        self.main_window.set_input_widget(self)

    def get_selected_fluid(self):
        self.selected_fluid = self.fluid_dialog.get_selected_fluid()
        if isinstance(self.selected_fluid, Fluid):
            self.fluid_dialog.close()
            self.update_plot_buttons_access()
            self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
            self.lineEdit_fluid_density.setText(f"{self.selected_fluid.fluid_density}")
            self.lineEdit_speed_of_sound.setText(f"{self.selected_fluid.speed_of_sound}")

    def get_perforated_plate_impendance(self, fluid: Fluid):

        warnings.filterwarnings('ignore')

        frequencies = None
        analysis_setup = app().project.analysis_setup
        if isinstance(analysis_setup, dict):
            frequencies = analysis_setup.get("frequencies")

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

        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == 0:
            self.get_inputs_for_perforated_plate_with_circular_holes()

        if self.pp_data:
            if tab_index == 0:

                U_rms = 0
                normalized_impedances = model.get_transfer_impedance_for_circular_holes(omega, self.pp_data)
                if normalized_impedances is None:
                    return

                z_orifice, z_end, z_nl_urms, z_ud, Z_0 = normalized_impedances
                Z_tr = Z_0 * (z_orifice + z_end + z_ud + z_nl_urms*U_rms)

            return freq, Z_tr

        return None, None

    def get_perforated_plate_model(self):
        tab_index = self.tabWidget_main.currentIndex()
        
        if tab_index == 0:
            return "circular hole"

    def plot_data_callback(self):
        plot_key = self.comboBox_plot_type.currentIndex()
        if plot_key == 0:
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

        if not app().project.model.generated_mesh:
            self.hide()
            app().main_window.input_ui.mesh_setup()
            app().main_window.set_input_widget(self)
            return False

        if self.mesh.cache_nodal_coordinates is None:
            self.mesh.cache_mesh_information()
        else:
            self.mesh.restore_data_from_cache()
            self.mesh.process_upwards_adjacencies_from_entities()
            self.mesh.cache_mesh_information()

        self.process_decoupling_actions()

        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        self.hide()

        try:
            warnings.filterwarnings('default')
        except TypeError:
            pass

        if self.process_degress_of_freedom_decoupling():
            return

        self.keep_window_open = False
        return super().closeEvent(a0)
