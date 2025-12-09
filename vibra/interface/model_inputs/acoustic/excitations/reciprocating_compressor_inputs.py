from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem, QAbstractItemView
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt, QPoint, QItemSelectionModel

from vibra import app, USER_PATH, SUPPORTED_OUTPUT_DATA_EXTENSIONS
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.formatters.icons import change_icon_color_for_widgets
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.general.mesher_setup_inputs import MesherSetupInputs
from vibra.interface.model_inputs.general.fluid.set_fluid_inputs import SetFluidInputs
from vibra.interface.model_inputs.general.fluid.simplified_fluid_inputs import SimplifiedFluidInputs
from vibra.interface.ui_generated.model.setup.acoustic.reciprocating_compressor_inputs_ui import ReciprocatingCompressorInputs_UI
from vibra.interface.model_inputs.acoustic.definitions.enums import *

from vibra.engine.properties.fluid import Fluid
from vibra.model.machines.reciprocating_compressor_model import ReciprocatingCompressorModel

import numpy as np
from os.path import dirname
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"

psi_to_Pa = (0.45359237 * 9.80665) / ((0.0254)**2)
kgf_cm2_to_Pa = 9.80665e4
bar_to_Pa = 1e5


class ReciprocatingCompressorInputs(ReciprocatingCompressorInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._create_connections()
        self._config_widget()
        self._paint_icons()

        self.load_compressor_excitation_info()
        self.geometry_selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):

        self.complete = False
        self.keep_window_open = True

        self.aquisition_parameters_processed = False
        self.not_update_event = False

        self.exporter = None

        self.tree_item_clicked = False
        self.last_tab = self.tabWidget_main.currentIndex()

    def _config_widget(self):
        #
        widths = [100, 120, 120, 200]
        for i, width in enumerate(widths):
            if i < len(widths) - 1:
                self.treeWidget_compressor_excitation.setColumnWidth(i, width)
            self.treeWidget_compressor_excitation.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.checkBox_export_data.stateChanged.connect(self.export_data_checkbox_callback)
        #
        self.comboBox_acting_head.currentIndexChanged.connect(self.update_compressing_cylinders_setup)
        self.comboBox_fluid_data_source.currentIndexChanged.connect(self.fluid_data_source_callback)
        self.comboBox_frequency_resolution.currentIndexChanged.connect(self.comboBox_event_frequency_resolution)
        self.comboBox_pressure_units.currentIndexChanged.connect(self.pressure_unit_callback)
        self.comboBox_temperature_units.currentIndexChanged.connect(self.temperature_unit_callback)
        #
        self.lineEdit_isentropic_exponent.textChanged.connect(self.update_state_properties_at_discharge)
        self.lineEdit_pressure_at_suction.textChanged.connect(self.update_state_properties_at_discharge)
        self.lineEdit_pressure_ratio.textChanged.connect(self.update_state_properties_at_discharge)
        self.lineEdit_temperature_at_suction.textChanged.connect(self.update_state_properties_at_discharge)
        #
        self.pushButton_plot_PV_diagram_head_end.clicked.connect(self.plot_PV_diagram_head_end)
        self.pushButton_plot_PV_diagram_crank_end.clicked.connect(self.plot_PV_diagram_crank_end)
        self.pushButton_plot_PV_diagram_both_ends.clicked.connect(self.plot_PV_diagram_both_ends)
        self.pushButton_plot_volumetric_flow_rate_at_suction_time.clicked.connect(self.plot_volumetric_flow_rate_at_suction_time)
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time.clicked.connect(self.plot_volumetric_flow_rate_at_discharge_time)
        self.pushButton_plot_rod_pressure_load_frequency.clicked.connect(self.plot_rod_pressure_load_frequency)
        self.pushButton_plot_rod_pressure_load_time.clicked.connect(self.plot_rod_pressure_load_time)
        self.pushButton_plot_piston_position_and_velocity_time.clicked.connect(self.plot_piston_position_and_velocity_time)
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency.clicked.connect(self.plot_volumetric_flow_rate_at_suction_frequency)
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency.clicked.connect(self.plot_volumetric_flow_rate_at_discharge_frequency)
        self.pushButton_plot_pressure_head_end_angle.clicked.connect(self.plot_pressure_head_end_angle)
        self.pushButton_plot_volume_head_end_angle.clicked.connect(self.plot_volume_head_end_angle)
        self.pushButton_plot_pressure_crank_end_angle.clicked.connect(self.plot_pressure_crank_end_angle)
        self.pushButton_plot_volume_crank_end_angle.clicked.connect(self.plot_volume_crank_end_angle)
        self.pushButton_process_aquisition_parameters.clicked.connect(self.process_aquisition_parameters)
        self.pushButton_export_path.clicked.connect(self.export_path_callback)
        #
        self.pushButton_confirm.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_reset_entries.clicked.connect(self.reset_entries)
        #
        self.spinBox_number_of_points.valueChanged.connect(self.spinBox_event_number_of_points)        
        self.spinBox_max_frequency.valueChanged.connect(self.spinBox_event_max_frequency)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_compressor_excitation.itemClicked.connect(self.on_click_item)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        app().main_window.theme_changed.connect(self._paint_icons)
        #
        self.export_data_checkbox_callback()
        self.update_compressing_cylinders_setup()
        self.update_state_properties_at_discharge()
    
    def _paint_icons(self):
        icon_color = None
        theme = app().config.user_preferences.interface_theme
        from vibra import LIGHT_ICON_COLOR, DARK_ICON_COLOR
        if theme == "dark":
            icon_color = DARK_ICON_COLOR.to_qt()
        else:
            icon_color = LIGHT_ICON_COLOR.to_qt()

        widgets = [self.pushButton_reset_entries]
        change_icon_color_for_widgets(widgets, icon_color)

    def export_data_checkbox_callback(self):
        is_checked = self.checkBox_export_data.isChecked()
        self.comboBox_output_data_type.setEnabled(is_checked)
        self.label_data_type.setEnabled(is_checked)
        self.label_export_path.setEnabled(is_checked)
        self.lineEdit_export_path.setEnabled(is_checked)
        self.pushButton_export_path.setEnabled(is_checked)

    def fluid_data_source_callback(self):

        index = self.comboBox_fluid_data_source.currentIndex()

        if index == FluidDataComboBox.REF_PROP:
            self.lineEdit_isentropic_exponent.setDisabled(True)
            self.lineEdit_molar_mass.setDisabled(True)

        elif index == FluidDataComboBox.USER_DEFINED:
            self.lineEdit_molar_mass.setEnabled(True)

    def geometry_selection_callback(self):
        if self.tabWidget_main.currentIndex() == 2:
            self.verify_if_selected_surfaces_are_in_tree_widget_compressor_excitation()
            return

        selected_surfaces = app().main_window.selected_geometry_surfaces

        if selected_surfaces:

            surface_ids = [str(i) for i in selected_surfaces]
            self.lineEdit_selection_id.setText(surface_ids[0])

            input_ids = self.lineEdit_selection_id.text()
            surface_id, error_data = self.mesh.check_selected_ids(
                                                                   input_ids, 
                                                                   selection = "surfaces",
                                                                   single_id = True
                                                                   )

            if error_data is not None:
                self.hide()
                self.lineEdit_selection_id.setFocus()
                PrintMessageInput(error_data)
                return True

            data = self.properties._get_property("reciprocating_compressor_excitation", surface=surface_id)

            if isinstance(data, dict):
                self.update_compressor_inputs(data)
    
    def verify_if_selected_surfaces_are_in_tree_widget_compressor_excitation(self):
        if self.tree_item_clicked:
            return

        selected_surfaces = app().main_window.selected_geometry_surfaces

        if not selected_surfaces:
            return

        self.clear_line_edit_selection_id()
        self.treeWidget_compressor_excitation.clearSelection()
        self.pushButton_remove.setDisabled(True)

        map_id_to_model_index = self.get_tree_widget_compressor_excitation_items_map()
        selected_ids = set(map_id_to_model_index.keys())
        selected_surfaces_in_tree_widget = selected_surfaces.intersection(selected_ids)

        if not selected_surfaces_in_tree_widget:
            return
        
        self.pushButton_remove.setEnabled(True)
        
        model_selector = self.treeWidget_compressor_excitation.selectionModel()

        for surface_id in selected_surfaces_in_tree_widget:
            model_index = map_id_to_model_index[surface_id]

            model_selector.select(model_index, QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows)

        self.treeWidget_compressor_excitation.setSelectionMode(QAbstractItemView.SingleSelection)
        self.set_selection_text(selected_surfaces_in_tree_widget)

    def get_tree_widget_compressor_excitation_items_map(self) -> dict:
        map_id_to_model_index = dict()

        index = self.treeWidget_compressor_excitation.indexAt(QPoint(0, 0))
        while index.isValid():
            item = self.treeWidget_compressor_excitation.itemFromIndex(index)
            surface_id = int(item.text(0))

            map_id_to_model_index[surface_id] = index

            index = self.treeWidget_compressor_excitation.indexBelow(index)
        
        return map_id_to_model_index

    def tab_event_callback(self):
        current_tab = self.tabWidget_main.currentIndex()
        tab_list = current_tab == RCTabTypes.LIST

        self.pushButton_confirm.setDisabled(tab_list)
        self.lineEdit_selection_id.setDisabled(tab_list)

        if self.last_tab == RCTabTypes.LIST or tab_list:
            app().main_window.clear_selection()
            self.clear_line_edit_selection_id()

        if tab_list:
            self.lineEdit_connection_type.clear()   
            self.pushButton_remove.setDisabled(True)
            self.treeWidget_compressor_excitation.clearSelection()
        
        self.last_tab = current_tab

    def update_compressing_cylinders_setup(self):

        self.label_rod_diameter.setEnabled(True)
        self.label_rod_diameter_unit.setEnabled(True)
        self.label_crank_end_clearance.setEnabled(True)
        self.label_crank_end_clearance_unit.setEnabled(True)
        self.label_head_end_clearance.setEnabled(True)
        self.label_head_end_clearance_unit.setEnabled(True)

        self.lineEdit_rod_diameter.setEnabled(True)
        self.lineEdit_clearance_head_end.setEnabled(True)
        self.lineEdit_clearance_crank_end.setEnabled(True)

        self.pushButton_plot_PV_diagram_head_end.setEnabled(True)
        self.pushButton_plot_PV_diagram_crank_end.setEnabled(True)
        self.pushButton_plot_pressure_head_end_angle.setEnabled(True)
        self.pushButton_plot_pressure_crank_end_angle.setEnabled(True)
        self.pushButton_plot_volume_head_end_angle.setEnabled(True)
        self.pushButton_plot_volume_crank_end_angle.setEnabled(True)

        if self.comboBox_acting_head.currentIndex() == ActingHeadComboBox.HEAD_END:
            self.lineEdit_rod_diameter.setDisabled(True)
            self.lineEdit_clearance_crank_end.setDisabled(True)
            self.label_rod_diameter.setDisabled(True)
            self.label_rod_diameter_unit.setDisabled(True)
            self.label_crank_end_clearance.setDisabled(True)
            self.label_crank_end_clearance_unit.setDisabled(True)

            self.pushButton_plot_PV_diagram_crank_end.setDisabled(True)
            self.pushButton_plot_pressure_crank_end_angle.setDisabled(True)
            self.pushButton_plot_volume_crank_end_angle.setDisabled(True)

        elif self.comboBox_acting_head.currentIndex() == ActingHeadComboBox.CRANK_END:
            self.lineEdit_rod_diameter.setEnabled(True)
            self.lineEdit_clearance_head_end.setDisabled(True)
            self.lineEdit_clearance_crank_end.setEnabled(True)
            self.label_head_end_clearance.setDisabled(True)
            self.label_head_end_clearance_unit.setDisabled(True)

            self.pushButton_plot_PV_diagram_head_end.setDisabled(True)
            self.pushButton_plot_pressure_head_end_angle.setDisabled(True)
            self.pushButton_plot_volume_head_end_angle.setDisabled(True)
            
    def get_state_properties(self, check_all_entries: bool):

        if self.check_all_parameters(check_all_entries = check_all_entries):
            return None

        if self.comboBox_connection_type.currentIndex() == ConnectionTypeComboBox.SUCTION:
            pressure = self.P_suction
            temperature = self.T_suction

        else:

            pressure = self.P_discharge
            p_ratio = self.parameters['pressure_ratio']
            gamma = self.parameters.get("isentropic_exponent", 1.4)

            temperature = self.T_suction * (p_ratio**((gamma-1)/gamma))

        state_properties = {
                            "pressure" : pressure,
                            "temperature" : temperature,
                            "check_ideal_gas" : True
                            }

        return state_properties

    def get_fluid_callback(self):

        state_properties = self.get_state_properties(False)

        if state_properties:
            self.hide()
            self.fluid_dialog = SimplifiedFluidInputs(state_properties = state_properties)
            self.fluid_dialog.fluid_widget.pushButton_attribute.setText("Select fluid")
            self.fluid_dialog.pushButton_attribute.clicked.connect(self.get_selected_fluid)
            self.fluid_dialog.exec_and_keep_window_open()
            app().main_window.set_input_widget(self)

    def get_selected_fluid(self):

        self.selected_fluid = self.fluid_dialog.get_selected_fluid()

        if isinstance(self.selected_fluid, Fluid):

            self.fluid_dialog.close()
            if self.selected_fluid.name in self.fluid_dialog.fluid_widget.fluid_name_to_refprop_data.keys():
                self.comboBox_fluid_data_source.setCurrentIndex(FluidDataComboBox.REF_PROP)

            self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
            self.lineEdit_isentropic_exponent.setText(f"{self.selected_fluid.isentropic_exponent : .6f}")
            self.lineEdit_molar_mass.setText(f"{self.selected_fluid.molar_mass : .6f}")

    def change_aquisition_parameters_controls(self, _bool):
        self.pushButton_process_aquisition_parameters.setDisabled(_bool)
        self.spinBox_max_frequency.setDisabled(_bool)
        self.spinBox_number_of_points.setDisabled(_bool)
        self.comboBox_frequency_resolution.setDisabled(_bool)

    def get_aquisition_parameters(self, parameters: dict):

        frequencies = app().project.model.frequencies
        rotational_speed = parameters["rotational_speed"]

        f_min = frequencies[0]
        f_max = frequencies[-1]
        df = frequencies[1] - frequencies[0]

        N_rev = int((1 / df) / (60 / rotational_speed))
        self.N_rev = N_rev

        return f_min, f_max, df, N_rev

    def update_compressor_inputs(self, data: dict):

        if "connection_type" in data.keys():
            connection_type = data["connection_type"]
            if connection_type == 'suction':
                self.comboBox_connection_type.setCurrentIndex(ConnectionTypeComboBox.SUCTION)
            elif connection_type == 'discharge':
                self.comboBox_connection_type.setCurrentIndex(ConnectionTypeComboBox.DISCHARGE)

        parameters = data["parameters"]

        compression_stage = parameters.get("compression_stage")
        if isinstance(compression_stage, int):
            stage_index = compression_stage - 1
            self.comboBox_stage.setCurrentIndex(stage_index)
        elif isinstance(compression_stage, str):
            self.comboBox_stage.setCurrentText(parameters.get("compression_stage", ""))

        if "valves_per_head" in parameters.keys():
            self.spinBox_valves_per_head.setValue(parameters.get("valves_per_head", 1))

        if "bore_diameter" in parameters.keys():
            self.lineEdit_bore_diameter.setText(str(parameters.get("bore_diameter")))

        if "stroke" in parameters.keys():
            self.lineEdit_stroke.setText(str(parameters.get("stroke")))

        if "connecting_rod_length" in parameters.keys():
            self.lineEdit_connecting_rod_length.setText(str(parameters.get("connecting_rod_length")))

        if "rod_diameter" in parameters.keys():
            self.lineEdit_rod_diameter.setText(str(parameters.get("rod_diameter")))

        if "pressure_ratio" in parameters.keys():
            self.lineEdit_pressure_ratio.setText(str(parameters.get("pressure_ratio")))

        if "clearance_HE" in parameters.keys():
            self.lineEdit_clearance_head_end.setText(str(parameters.get("clearance_HE")))

        if "clearance_CE" in parameters.keys():
            self.lineEdit_clearance_crank_end.setText(str(parameters.get("clearance_CE")))

        for key in ["TDC_crank_angle", "TDC_crank_angle_1"]:
            if key in parameters.keys():
                self.spinBox_tdc1_crank_angle.setValue(int(parameters.get(key, 0)))
                break

        if "rotational_speed" in parameters.keys():
            self.doubleSpinBox_rotational_speed.setValue(parameters.get("rotational_speed"))

        if "capacity" in parameters.keys():
            self.spinBox_capacity.setValue(int(parameters.get("capacity")))

        if "isentropic_exponent" in parameters.keys():
            self.lineEdit_isentropic_exponent.setText(str(parameters.get("isentropic_exponent")))

        if "molar_mass" in parameters.keys():
            self.lineEdit_molar_mass.setText(str(parameters.get("molar_mass")))

        if "pressure_at_suction" in parameters.keys():
            self.lineEdit_pressure_at_suction.setText(str(parameters.get("pressure_at_suction")))

        pressure_units = ["kgf/cm² (a)", "bar (a)", "kgf/cm² (g)", "bar (g)"]
        if "pressure_unit" in parameters.keys():
            for i, p_unit in enumerate(pressure_units):
                if p_unit in parameters.get("pressure_unit"):
                    self.comboBox_pressure_units.setCurrentIndex(i)

        if "temperature_at_suction" in parameters.keys():
            self.lineEdit_temperature_at_suction.setText(str(parameters.get("temperature_at_suction")))

        temperature_units = ["K", "°C"]
        if "temperature_unit" in parameters.keys():
            for i, p_unit in enumerate(temperature_units):
                if p_unit in parameters.get("temperature_unit"):
                    self.comboBox_temperature_units.setCurrentIndex(i)

        if "acting_head" in parameters.keys():
            acting_heads = ["head_end", "crank_end", "both_ends"]
            acting_index = acting_heads.index(parameters.get("acting_head"))
            self.comboBox_acting_head.setCurrentIndex(acting_index)

        if "points_per_revolution" in parameters.keys():
            self.spinBox_number_of_points.setValue(int(parameters.get("points_per_revolution")))

        f_min, f_max, f_step, N_rev = self.get_aquisition_parameters(parameters)
        self.lineEdit_number_of_revolutions.setText(str(N_rev))
        self.spinBox_max_frequency.setValue(int(f_max))
        self.lineEdit_frequency_resolution.setText(str(f_step))

        f_steps = [0.1, 0.2, 0.5, 1.0, 2.0]
        if f_step in f_steps:
            index = f_steps.index(f_step)
            self.comboBox_frequency_resolution.setCurrentIndex(index)

    def reset_entries(self):
        self.comboBox_acting_head.setCurrentIndex(ActingHeadComboBox.HEAD_END)
        self.comboBox_stage.setCurrentIndex(CompressionStageComboBox.FIRST_STAGE)
        self.comboBox_pressure_units.setCurrentIndex(PressureUnitComboBox.KGF_CM2_A)
        self.comboBox_temperature_units.setCurrentIndex(TemperatureUnitComboBox.CELSIUS)
        self.doubleSpinBox_rotational_speed.setValue(360)
        self.lineEdit_bore_diameter.clear()
        self.lineEdit_stroke.clear()
        self.lineEdit_connecting_rod_length.clear()
        self.lineEdit_rod_diameter.clear()
        self.lineEdit_pressure_ratio.clear()
        self.lineEdit_clearance_head_end.clear()
        self.lineEdit_clearance_crank_end.clear()
        self.lineEdit_isentropic_exponent.clear()
        self.lineEdit_molar_mass.clear()
        self.lineEdit_pressure_at_suction.clear()
        self.lineEdit_temperature_at_suction.clear()
        self.spinBox_tdc1_crank_angle.setValue(0)
        self.spinBox_valves_per_head.setValue(1)
        self.spinBox_capacity.setValue(100)

    def generate_mesh(self):
        if not app().project.model.generated_mesh:
            mesher = MesherSetupInputs(close_after_generate=True)
            if not mesher.complete:
                return True

    def check_input_surfaces(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_id, error_data = self.model.mesh.check_selected_ids(
                                                                    input_ids, 
                                                                    selection = "surfaces", 
                                                                    single_id = True
                                                                    )

        if error_data is not None:
            self.hide()
            self.lineEdit_selection_id.setFocus()
            self.lineEdit_selection_id.selectAll()
            PrintMessageInput(error_data)
            return None

        volumes_from_surface = self.model.mesh.volumes_from_surface.get(surface_id)
        if len(volumes_from_surface) != 1:
            self.hide()
            title = "Invalid surface selected"
            message = "The selected surface does not correspond to the piping endings. "
            message += "It is necessary to change the selection to proceed with the "
            message += "compressor excitation attribution."
            PrintMessageInput([window_title_1, title, message])
            self.clear_line_edit_selection_id()
            return None

        return surface_id

    def check_input_parameters(self, lineEdit: QLineEdit, label: str, _float=True):

        title = "Input error"
        value_string = lineEdit.text()

        if value_string != "":

            value_string = value_string.replace(",", ".")

            try:

                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string)

                if value < 0:
                    message = f"You cannot input a negative value to the {label}."
                    PrintMessageInput([window_title_1, title, message])
                    return True
                else:
                    self.value = value

            except Exception:
                message = f"You have typed an invalid value to the {label}."
                PrintMessageInput([window_title_1, title, message])
                return True
        else:
            message = f"None value has been typed to the {label}."
            PrintMessageInput([window_title_1, title, message])
            return True
        return False

    def check_all_parameters(self, check_all_entries: bool = True):

        self.parameters = dict()

        if self.check_input_parameters(self.lineEdit_bore_diameter, "Bore diameters"):
            self.lineEdit_bore_diameter.setFocus()
            return True
        else:
            self.parameters['bore_diameter'] = self.value

        if self.check_input_parameters(self.lineEdit_stroke, "Stroke"):
            self.lineEdit_stroke.setFocus()
            return True
        else:
            self.parameters['stroke'] = self.value

        if self.check_input_parameters(self.lineEdit_connecting_rod_length, "Connecting rod length"):
            self.lineEdit_connecting_rod_length.setFocus()
            return True
        else:
            self.parameters['connecting_rod_length'] = self.value

        acting_head = self.comboBox_acting_head.currentText().lower().replace(" ", "_")
        if acting_head in ["crank_end", "both_ends"]:
            if self.check_input_parameters(self.lineEdit_rod_diameter, "Rod diameter"):
                self.lineEdit_rod_diameter.setFocus()
                return True
            else:
                self.parameters['rod_diameter'] = self.value

        if self.check_input_parameters(self.lineEdit_pressure_ratio, "Pressure ratio"):
            self.lineEdit_pressure_ratio.setFocus()
            return True
        else:
            self.parameters['pressure_ratio'] = self.value
        
        if acting_head in ["head_end", "both_ends"]:
            if self.check_input_parameters(self.lineEdit_clearance_head_end, "HE clearance"):
                self.lineEdit_clearance_head_end.setFocus()
                return True
            else:
                self.parameters['clearance_HE'] = self.value

        if acting_head in ["crank_end", "both_ends"]:
            if self.check_input_parameters(self.lineEdit_clearance_crank_end, "CE clearance"):
                self.lineEdit_clearance_crank_end.setFocus()
                return True
            else:
                self.parameters['clearance_CE'] = self.value

        self.parameters['TDC_crank_angle'] = self.spinBox_tdc1_crank_angle.value()
        self.parameters['rotational_speed'] = self.doubleSpinBox_rotational_speed.value()
        self.parameters['valves_per_head'] = self.spinBox_valves_per_head.value()
        self.parameters['capacity'] = self.spinBox_capacity.value()

        if check_all_entries:
            if self.check_input_parameters(self.lineEdit_molar_mass, "Mola mass"):
                self.lineEdit_molar_mass.setFocus()
                return True
            else:
                self.parameters['molar_mass'] = self.value

            if self.check_input_parameters(self.lineEdit_isentropic_exponent, "Isentropic exponent"):
                self.lineEdit_isentropic_exponent.setFocus()
                return True
            else:
                self.parameters['isentropic_exponent'] = self.value

        if self.check_input_parameters(self.lineEdit_pressure_at_suction, "Pressure at suction"):
            self.lineEdit_pressure_at_suction.setFocus()
            return True
        else:
            self.parameters['pressure_at_suction'] = self.value
            self.parameters['pressure_at_discharge'] = self.parameters['pressure_ratio'] * self.parameters['pressure_at_suction']

        # unit_labels = ["kgf/cm² (a)", "bar (a)", "kPa (a)", "Pa (a)", "kgf/cm² (g)", "bar (g)", "kPa (g)", "Pa (g)"]
        pressure_unit = self.comboBox_pressure_units.currentText()
        self.parameters['pressure_unit'] = pressure_unit

        if self.check_input_parameters(self.lineEdit_temperature_at_suction, "Temperature at suction"):
            self.lineEdit_temperature_at_suction.setFocus()
            return True
        else:
            self.parameters['temperature_at_suction'] = self.value

        # unit_labels = ["°C", "K"]
        temperature_unit = self.comboBox_temperature_units.currentText()
        self.parameters['temperature_unit'] = temperature_unit
        self.parameters['compression_stage'] = self.comboBox_stage.currentText()
        self.parameters['acting_head'] = acting_head

        if check_all_entries:
            self.compressor = ReciprocatingCompressorModel(self.parameters)

        if "kgf/cm²" in pressure_unit:
            self.P_suction = self.parameters['pressure_at_suction'] * kgf_cm2_to_Pa
            self.P_discharge = self.parameters['pressure_at_discharge'] * kgf_cm2_to_Pa

        elif "bar" in pressure_unit:
            self.P_suction = self.parameters['pressure_at_suction'] * bar_to_Pa
            self.P_discharge = self.parameters['pressure_at_discharge'] * bar_to_Pa

        elif "kPa" in pressure_unit:
            self.P_suction = self.parameters['pressure_at_suction'] * 1e3
            self.P_discharge = self.parameters['pressure_at_discharge'] * 1e3

        if "(g)" in pressure_unit:
            self.P_suction += 101325
            self.P_discharge += 101325

        if "°C" in temperature_unit:
            self.T_suction = self.parameters['temperature_at_suction'] + 273.15
            # self.T_discharge = self.parameters['temperature_at_discharge'] + 273.15

        elif "K" in temperature_unit:
            self.T_suction = self.parameters['temperature_at_suction']
            # self.T_discharge = self.parameters['temperature_at_discharge']

        return False

    def process_aquisition_parameters(self):

        self.currentIndex = self.comboBox_frequency_resolution.currentIndex()
        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.max_frequency = self.spinBox_max_frequency.value()

        T_rev = 60 / self.parameters['rotational_speed']
        list_T = [10, 5, 2, 1, 0.5]
        list_df = [0.1, 0.2, 0.5, 1, 2]

        T_selected = list_T[self.currentIndex]
        df_selected = list_df[self.currentIndex]

        if np.remainder(T_selected, T_rev) == 0:
            T = T_selected
            df = 1 / T

        else:
            i = 0
            df = 1 / T_rev
            while df > df_selected:
                i += 1
                df = 1 / (i*T_rev)

        self.N_rev = i

        final_df_label = '{} Hz'.format(round(df, 6))
        self.lineEdit_frequency_resolution.setText(final_df_label)
        self.lineEdit_number_of_revolutions.setText(str(self.N_rev))
        self.aquisition_parameters_processed = True

    def save_table_values(self, table_name: str, frequencies: np.ndarray, complex_values: np.ndarray):

        if app().project.model.change_analysis_frequency_setup(list(frequencies)):
            self.hide()
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([window_title_1, title, message])
            return True

        self.update_analysis_setup_in_file(frequencies)

        real_values = np.real(complex_values)
        imag_values = np.imag(complex_values)
        data = np.array([frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def update_analysis_setup_in_file(self, frequencies: np.ndarray):

        analysis_setup = app().file.read_analysis_setup_from_file()
        if analysis_setup is None:
            analysis_setup = dict()

        f_min = frequencies[0]
        f_max = frequencies[-1]
        f_step = frequencies[1] - frequencies[0] 

        analysis_setup["f_min"] = float(f_min)
        analysis_setup["f_max"] = float(f_max)
        analysis_setup["f_step"] = float(f_step)

        app().project.set_analysis_setup(analysis_setup)
        app().file.write_analysis_setup_in_file(analysis_setup)

    def update_state_properties_at_discharge(self):

        try:

            suction_pressure = float(self.lineEdit_pressure_at_suction.text())
            pressure_ratio = float(self.lineEdit_pressure_ratio.text())
            gamma = float(self.lineEdit_isentropic_exponent.text())
            discharge_pressure = pressure_ratio * suction_pressure

            if self.comboBox_pressure_units.currentIndex() in [3, 7]:
                self.lineEdit_pressure_at_discharge.setText(f"{discharge_pressure : .8e}")
            else:
                self.lineEdit_pressure_at_discharge.setText(f"{discharge_pressure : .6f}")

        except:
            return

        try:

            suction_temperature = float(self.lineEdit_temperature_at_suction.text())
            if self.comboBox_temperature_units.currentIndex() == TemperatureUnitComboBox.CELSIUS:
                suction_temperature += 273.15

            discharge_temperature = suction_temperature * (pressure_ratio**((gamma-1)/gamma))
            if self.comboBox_temperature_units.currentIndex() == TemperatureUnitComboBox.CELSIUS:
                discharge_temperature -= 273.15

            self.lineEdit_temperature_at_discharge.setText(f"{discharge_temperature : .6f}")

        except:
            return

    def attribute_callback(self):

        if self.generate_mesh():
            return

        surface_id = self.check_input_surfaces()
        if surface_id is None:
            return

        if self.check_all_parameters():
            return

        self.process_aquisition_parameters()

        if self.comboBox_connection_type.currentIndex() == ConnectionTypeComboBox.SUCTION:
            flow_label = "in_flow"
            connection_type = "suction"
        else:
            flow_label = "out_flow"
            connection_type = "discharge"

        volume_id = self.model.mesh.volumes_from_surface[surface_id]

        compressor_info = { 
                            "temperature_at_suction" : self.T_suction,
                            "suction_pressure" : self.P_suction,
                            "surface_id" : surface_id,
                            "volume_id" : volume_id[0],
                            "connection_type" : connection_type,
                            "isentropic_exponent" : self.parameters.get('isentropic_exponent', None),
                            "pressure_ratio" : self.parameters['pressure_ratio'],
                            "source" : "reciprocating_compressor",
                            "check_ideal_gas" : True,
                            }

        self.hide()
        read = SetFluidInputs(state_properties = compressor_info)
        app().main_window.set_input_widget(self)

        if not read.complete:
            return

        else:
            if read.fluid_widget.refprop is not None:
                if read.fluid_widget.refprop.complete:

                    self.parameters["molar_mass"] = round(read.fluid_widget.fluid_data_refprop["molar_mass"], 6)
                    self.parameters['isentropic_exponent'] = round(read.fluid_widget.fluid_data_refprop["isentropic_exponent"], 6)
                    self.parameters['fluid_properties_source'] = "refprop"
            else:
                self.parameters['fluid_properties_source'] = "user-defined"

            self.parameters['points_per_revolution'] = self.compressor.number_points
            self.compressor.process_state_properties_in_SI_units(self.parameters)

            self.model.mesh.process_face_elements_connected_to_nodes(surface_id)
            surface_area = self.model.mesh.surface_area_from_element_integration[surface_id]

            freq, flow_rate = self.compressor.process_FFT_of_volumetric_flow_rate(self.N_rev, flow_label)
            surface_velocity = flow_rate / surface_area

            # remove the zero frequency component
            _freq = freq[1:]
            _surface_velocity = surface_velocity[1:]

            table_name = f"compressor_excitation_{connection_type}_surface_{surface_id}"

            if self.checkBox_export_data.isChecked():
                output_data_type = self.comboBox_output_data_type.currentText()
                if output_data_type == "Surface velocity [m/s]":
                    unit = "m/s"
                    output_data = _surface_velocity
                else:
                    unit = "m³/s"
                    output_data = flow_rate[1:]

                self.export_reciprocating_compressor_data_excitation(surface_id, _freq, output_data, unit)

            data = {
                    "connection_type" : connection_type,
                    "table_names" : [table_name],
                    "parameters" : self.parameters,
                    "values" : [_surface_velocity],
                    "nodal_attribution" : False,
                    "averaged" : False
                    }

            self.remove_conflicting_excitations(surface_id)

            if self.save_table_values(table_name, _freq, _surface_velocity):
                return

            self.properties._set_property("reciprocating_compressor_excitation", data, surface=surface_id)
            self.actions_to_finalize()

    def actions_to_finalize(self):
        self.load_compressor_excitation_info()
        app().file.write_model_properties_in_file()
        app().file.write_imported_table_data_in_file()
        app().main_window.selection.set_geometry_selection()
        app().main_window.update_symbols()

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().file.write_imported_table_data_in_file()

    def remove_conflicting_excitations(self, surface_id: int):

        labels = [
                  "acoustic_pressure", 
                  "surface_velocity", 
                  "incident_plane_wave",
                  "mass_flow_rate", 
                  "reciprocating_compressor_excitation", 
                  "reciprocating_pump_excitation"
                  ]

        for label in labels:
            table_names = self.properties.get_property_related_table_names(label, surface_id, "surfaces")
            self.properties._remove_surface_property(label, surface_id)
            self.process_table_file_removal(table_names)

    def remove_table_files_from_surfaces(self, surface_id : list):
        table_names = self.properties.get_property_related_table_names("reciprocating_compressor_excitation", surface_id, "surfaces")
        self.process_table_file_removal(table_names)

    def remove_callback(self):
        surface_ids = [int(selected_item.text(0)) for selected_item in self.treeWidget_compressor_excitation.selectedItems()]

        if not surface_ids:
            return
        
        for surface_id in surface_ids:
            self.remove_table_files_from_surfaces(surface_id)
            self.properties._remove_surface_property("reciprocating_compressor_excitation", surface_id)
        
        self.clear_line_edit_selection_id()
        self.lineEdit_connection_type.clear()
        self.pushButton_remove.setDisabled(True)

        app().main_window.clear_selection()
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Resetting of compressor excitations"
        message = "Would you like to remove all compressor excitations from the acoustic model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            surface_ids = list()
            for (property, *args) in self.properties.surface_properties.keys():
                if property == "reciprocating_compressor_excitation":

                    surface_id = args[0]
                    surface_ids.append(surface_id)

            self.remove_table_files_from_surfaces(surface_ids)

            self.properties._reset_property("reciprocating_compressor_excitation")
            self.actions_to_finalize()

    def load_compressor_excitation_info(self):

        self.treeWidget_compressor_excitation.clear()

        for (property, *args), data in self.properties.surface_properties.items():
            if property == "reciprocating_compressor_excitation":
                
                surface_id = args[0]
                connection_type = data["connection_type"]

                rc_param = data.get("parameters", dict())
                acting_head = rc_param.get("acting_head", "")
                TDC_crank_angle = rc_param.get("TDC_crank_angle", 0)

                new = QTreeWidgetItem([str(surface_id), connection_type, acting_head, str(TDC_crank_angle)])
                for i in range(4):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_compressor_excitation.addTopLevelItem(new)

        self.update_tabs_visibility()

    def on_click_item(self, item):
        self.tree_item_clicked = True

        surface_ids, connection_type = self.get_selected_surfaces_and_connection_type_text()

        if not surface_ids:
            return
        
        app().main_window.selection.set_geometry_selection(surfaces=surface_ids)
        self.set_selection_text(surface_ids)
        self.lineEdit_connection_type.setText(connection_type)
        self.pushButton_remove.setDisabled(False)

        self.tree_item_clicked = False

    def get_selected_surfaces_and_connection_type_text(self):
        selected_items = self.treeWidget_compressor_excitation.selectedItems()

        if not selected_items:
            return list(), str() 

        connection_type = set()
        surface_ids = list()

        for item in selected_items:
            surface_id = item.text(0)
            connection_type.add(item.text(1))
            surface_ids.append(int(surface_id))

        connection_text = connection_type.pop() if len(connection_type) == 1 else "--"
        
        return surface_ids, connection_text

    def set_selection_text(self, selected_surfaces: list | set):
        selected_surfaces = list(selected_surfaces)
        selected_surfaces.sort()

        selected_surfaces = map(str, selected_surfaces)
        selection_text = ", ".join(selected_surfaces)

        print(selection_text)

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)
    
    def clear_line_edit_selection_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")

    def update_tabs_visibility(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_connection_type.clear()
        self.pushButton_remove.setDisabled(True)

        for (property, *_) in self.properties.surface_properties.keys():
            if property == "reciprocating_compressor_excitation":
                self.tabWidget_main.setTabVisible(RCTabTypes.LIST, True)
                return

        self.tabWidget_main.setTabVisible(RCTabTypes.LIST, False)
        self.tabWidget_main.setCurrentIndex(RCTabTypes.SETUP)

    def spinBox_event_number_of_points(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def spinBox_event_max_frequency(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def comboBox_event_frequency_resolution(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def pressure_unit_callback(self):
        unit_label = self.comboBox_pressure_units.currentText()
        self.label_suction_pressure_unit.setText(f"[{unit_label}]")
        self.label_discharge_pressure_unit.setText(f"[{unit_label}]")

    def temperature_unit_callback(self):
        unit_label = self.comboBox_temperature_units.currentText()
        self.label_suction_temperature_unit.setText(f"[{unit_label}]")
        self.label_discharge_temperature_unit.setText(f"[{unit_label}]")

    def plot_PV_diagram_head_end(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_PV_diagram_head_end()

    def plot_PV_diagram_crank_end(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_PV_diagram_crank_end()

    def plot_PV_diagram_both_ends(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_PV_diagram_both_ends()

    def plot_pressure_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_pressure_vs_time()
        return

    def plot_volume_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_volume_vs_time()
        return
    
    def plot_volumetric_flow_rate_at_suction_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_volumetric_flow_rate_at_suction_time()
        return

    def plot_volumetric_flow_rate_at_discharge_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_volumetric_flow_rate_at_discharge_time()
        return
    
    def plot_rod_pressure_load_frequency(self):
        self.process_aquisition_parameters()
        self.compressor.plot_rod_pressure_load_frequency(self.N_rev)
        return

    def plot_rod_pressure_load_time(self):
        self.process_aquisition_parameters()
        self.compressor.plot_rod_pressure_load_time()
        return
    
    def plot_piston_position_and_velocity_time(self):
        self.process_aquisition_parameters()
        self.compressor.plot_piston_position_and_velocity(domain="time")

    def plot_piston_position_and_velocity_angle(self):
        self.process_aquisition_parameters()
        self.compressor.plot_piston_position_and_velocity(domain="angle")

    def plot_volumetric_flow_rate_at_suction_frequency(self):
        self.process_aquisition_parameters()
        self.compressor.plot_volumetric_flow_rate_at_suction_frequency(self.N_rev)
        return

    def plot_volumetric_flow_rate_at_discharge_frequency(self):
        self.process_aquisition_parameters()
        self.compressor.plot_volumetric_flow_rate_at_discharge_frequency(self.N_rev)
        return

    def plot_pressure_head_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_head_end_pressure_vs_angle()
        return

    def plot_volume_head_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_head_end_volume_vs_angle()
        return

    def plot_pressure_crank_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_crank_end_pressure_vs_angle()
        return

    def plot_volume_crank_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_crank_end_volume_vs_angle()
        return

    def export_path_callback(self):

        path = app().config.get_last_folder_for("exported_data_folder")
        if path is None:
            directory_path = USER_PATH
        else:
            directory_path = path

        caption = "Enter a filename to export the reciprocating compressor excitation data"
        ext_filter = "Text file (*.dat);; Text file (*.txt);; Text file (*.csv);; Spreadsheet (*.xls);; Spreadsheet (*.xlsx)"

        if self.exporter is None:
            self.exporter = ExportModelResults()

        self.hide()
        file_path, check = self.exporter.getSaveFileName(
                                                         app().main_window, 
                                                         caption, 
                                                         directory_path, 
                                                         filter = ext_filter
                                                         )

        if not check:
            return

        self.checkBox_export_data.setChecked(True)
        self.lineEdit_export_path.setText(file_path)

        app().config.write_last_folder_path_in_file("exported_data_folder", file_path)

    def export_reciprocating_compressor_data_excitation(
                                                        self, 
                                                        surface_id: int, 
                                                        frequencies: np.ndarray, 
                                                        excitation_data: np.ndarray,
                                                        unit: str
                                                        ):

        recip_excitation_data = dict()
        title = "Reciprocating compressor excitation"

        if unit == "m/s":
            key = ("surface_velocity_at", surface_id)
        else:
            key = ("flow_rate_at", surface_id)

        legend_label = f"Reciprocating compressor excitation at surface [{surface_id}]"

        recip_excitation_data[key] = {
                                        "x_data" : frequencies,
                                        "y_data" : excitation_data,
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : "Compressor excitation",
                                        "title" : title,
                                        "data_type" : "compressor excitation",
                                        "legend" : legend_label,
                                        "unit" : unit,
                                        "color" : [0, 0, 1],
                                        "linestyle" : "-"  
                                        }

        if self.exporter is None:
            self.exporter = ExportModelResults()

        file_path = self.lineEdit_export_path.text()
        if not self.is_file_path_valid(file_path):
            file_path = ""

        self.exporter._set_data_to_export(recip_excitation_data, existing_path=file_path)

    def is_file_path_valid(self, file_path: str):
        if Path(dirname(file_path)).exists():
            ext = file_path.split(".")[-1]
            if ext in SUPPORTED_OUTPUT_DATA_EXTENSIONS:
                return True
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Control:
            self.treeWidget_compressor_excitation.setSelectionMode(QAbstractItemView.MultiSelection)
        elif event.key() == Qt.Key_Shift:
            self.treeWidget_compressor_excitation.setSelectionMode(QAbstractItemView.ContiguousSelection)
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.treeWidget_compressor_excitation.setSelectionMode(QAbstractItemView.SingleSelection)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)