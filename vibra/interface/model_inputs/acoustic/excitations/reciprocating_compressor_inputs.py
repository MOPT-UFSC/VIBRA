import logging
from enum import IntEnum
from os.path import dirname
from pathlib import Path

import numpy as np
from PySide6.QtCore import QItemSelectionModel, QPoint, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QLineEdit, QTreeWidgetItem

from vibra import SUPPORTED_OUTPUT_DATA_EXTENSIONS, USER_PATH, app
from vibra.engine.properties.fluid import Fluid
from vibra.interface import error_title
from vibra.interface.common.common_interface import mesher_interface_callback, update_analysis_setup_in_file, update_entities_selection
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.model_inputs.fluid.set_fluid_inputs import SetFluidInputs
from vibra.interface.model_inputs.fluid.set_fluid_inputs_simplified import SetFluidInputsSimplified
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.numeric_checks.unit_utilities import (
    PressureUnits,
    TemperatureUnits,
    convert_temperature_unit,
    pressure_units_labels,
    temperature_units_labels,
)
from vibra.interface.plots.general.plot_2d_simplified import Plot2DSimplified
from vibra.interface.ui_generated.model.acoustic.excitations.reciprocating_compressor_inputs_ui import ReciprocatingCompressorInputs_UI
from vibra.model.machines.reciprocating_compressor_model import ConnectionType, CylindersActingMode, ReciprocatingCompressorModel


class CompressorExcitationData(IntEnum):
    SURFACE_VELOCITY = 0
    VOLUME_VELOCITY = 1


class TabIndex(IntEnum):
    SETUP = 0
    ADVANCED_OPTIONS = 1
    LIST = 2


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
        self._config_widgets()
        self._create_connections()

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

        self.exporter = None
        self.selected_fluid = None

        self.complete = False
        self.keep_window_open = True
        self.not_update_event = False
        self.tree_item_clicked = False
        self.aquisition_parameters_processed = False

        self.last_tab = self.tabWidget_main.currentIndex()

    def reset_entries(self):

        self.comboBox_cylinder_acting.setCurrentIndex(CylindersActingMode.BOTH_ENDS)
        self.comboBox_compression_stage.setCurrentText("First stage")
        self.comboBox_pressure_units.setCurrentText("kgf/cm² (a)")
        self.comboBox_temperature_units.setCurrentText("°C")

        self.lineEdit_bore_diameter.clear()
        self.lineEdit_stroke.clear()
        self.lineEdit_connecting_rod_length.clear()
        self.lineEdit_rod_diameter.clear()
        self.lineEdit_pressure_ratio.clear()
        self.lineEdit_suction_pressure.clear()
        self.lineEdit_suction_temperature.clear()
        self.lineEdit_discharge_pressure.clear()
        self.lineEdit_discharge_temperature.clear()
        self.lineEdit_isentropic_exponent.clear()
        self.lineEdit_molar_mass.clear()

        self.spinBox_tdc_crank_angle.setValue(0)
        self.spinBox_capacity.setValue(100)
        self.spinBox_valves_per_head.setValue(1)
        self.doubleSpinBox_clearance_head_end.setValue(0)
        self.doubleSpinBox_clearance_crank_end.setValue(0)
        self.doubleSpinBox_rotational_speed.setValue(360.0)

    def _config_widgets(self):

        self.default_stylesheet = self.lineEdit_selection_id.styleSheet()

        # disable the discharge temperature QLineEdit
        self.lineEdit_discharge_temperature.setDisabled(True)

        # configure the QTreeWidget appearance
        self.treeWidget_compressor_excitation.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for i in range(2):
            self.treeWidget_compressor_excitation.headerItem().setTextAlignment(i, Qt.AlignCenter)

        self._load_units_labels()
        self.configure_dynamic_validators()
        self.configure_static_validators()

    def _load_units_labels(self):
        # clear data from unit combo boxes
        self.comboBox_pressure_units.clear()
        self.comboBox_temperature_units.clear()

        # add temperature and pressure labels into unit combo boxes
        self.comboBox_pressure_units.addItems(pressure_units_labels)
        self.comboBox_temperature_units.addItems(temperature_units_labels)

        # set default units
        self.comboBox_pressure_units.setCurrentText("kgf/cm² (a)")
        self.comboBox_temperature_units.setCurrentText("°C")

    def configure_dynamic_validators(self):

        # adjust temperature bounds (t_min -> zero absolute)
        t_min = 0
        t_max = 1e4
        if self.comboBox_temperature_units.currentIndex() == TemperatureUnits.CELSIUS:
            t_min = -273.15
        elif self.comboBox_temperature_units.currentIndex() == TemperatureUnits.FARENHEIT:
            t_min = -459.67

        # adjust pressure bounds (p_min -> perfect vacuum)      
        p_min = 0 
        p_max = 1e8

        punit_index = self.comboBox_pressure_units.currentIndex()
        if punit_index == PressureUnits.Pa_g:
            p_min = -101325

        elif punit_index == PressureUnits.kPa_g:
            p_min = -101.325

        elif punit_index == PressureUnits.bar_g:
            p_min = -1.101325
            p_max = 2e3

        elif punit_index == PressureUnits.kgf_cm2_g:
            p_min = -(9.80665*1e4)

        elif punit_index == PressureUnits.psi_g:
            p_min = -(0.45359237*9.80665) / (0.0254**2)

        elif punit_index == PressureUnits.ksi_g:
            p_min = -(0.45359237*9.80665) / (1e3 * (0.0254**2))
            p_max = 1e3

        # configure validator for pressure and temeperature inputs
        self.lineEdit_suction_pressure.setValidator(StrictDoubleValidator(p_min, p_max, 6))
        self.lineEdit_discharge_pressure.setValidator(StrictDoubleValidator(p_min, p_max, 6))
        self.lineEdit_suction_temperature.setValidator(StrictDoubleValidator(t_min, t_max, 6))
        self.lineEdit_discharge_temperature.setValidator(StrictDoubleValidator(t_min, t_max, 6))

        press_unit = self.comboBox_pressure_units.currentText()
        self.label_suction_pressure_unit.setText(f"[{press_unit}]")
        self.label_discharge_pressure_unit.setText(f"[{press_unit}]")

        temp_unit = self.comboBox_temperature_units.currentText()
        self.label_suction_temperature_unit.setText(f"[{temp_unit}]")
        self.label_discharge_temperature_unit.setText(f"[{temp_unit}]")

        self.update_state_properties_at_discharge()

    def configure_static_validators(self):

        # configure validator for geometric parameters
        geom_validator = StrictDoubleValidator(1e-6, 1e8, 8)
        self.lineEdit_bore_diameter.setValidator(geom_validator)
        self.lineEdit_stroke.setValidator(geom_validator)
        self.lineEdit_connecting_rod_length.setValidator(geom_validator)
        self.lineEdit_rod_diameter.setValidator(geom_validator)

        # configure validator for pressure ratio and isentropic exponent
        self.lineEdit_pressure_ratio.setValidator(StrictDoubleValidator(1e-8, 10, 8))
        self.lineEdit_isentropic_exponent.setValidator(StrictDoubleValidator(1e-8, 10, 6))

    def _create_connections(self):
        #
        self.checkBox_export_data.stateChanged.connect(self.export_data_checkbox_callback)
        #
        self.comboBox_cylinder_acting.currentIndexChanged.connect(self.update_compressing_cylinders_setup)
        self.comboBox_frequency_resolution.currentIndexChanged.connect(self.comboBox_event_frequency_resolution)
        self.comboBox_pressure_units.currentIndexChanged.connect(self.pressure_unit_callback)
        self.comboBox_temperature_units.currentIndexChanged.connect(self.temperature_unit_callback)
        #
        self.lineEdit_isentropic_exponent.textChanged.connect(self.update_state_properties_at_discharge)
        self.lineEdit_suction_pressure.textChanged.connect(self.update_state_properties_at_discharge)
        self.lineEdit_pressure_ratio.textChanged.connect(self.update_state_properties_at_discharge)
        self.lineEdit_suction_temperature.textChanged.connect(self.update_state_properties_at_discharge)
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
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
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
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.export_data_checkbox_callback()
        self.update_compressing_cylinders_setup()
        self.update_state_properties_at_discharge()

    def export_data_checkbox_callback(self):
        is_checked = self.checkBox_export_data.isChecked()
        self.comboBox_output_data_type.setEnabled(is_checked)
        self.label_data_type.setEnabled(is_checked)
        self.label_export_path.setEnabled(is_checked)
        self.lineEdit_export_path.setEnabled(is_checked)
        self.pushButton_export_path.setEnabled(is_checked)

    def geometry_selection_callback(self):
        if self.tabWidget_main.currentIndex() == TabIndex.LIST:
            self.verify_if_selected_surfaces_are_in_tree_widget_compressor_excitation()
            return

        selected_surfaces = app().main_window.selection.geometry_surfaces

        if len(selected_surfaces) == 1:
            surface_id = next(iter(selected_surfaces))
            data = self.properties._get_property("reciprocating_compressor_excitation", surface=surface_id)

            if isinstance(data, dict):
                self.update_compressor_inputs(data)
    
    def verify_if_selected_surfaces_are_in_tree_widget_compressor_excitation(self):
        if self.tree_item_clicked:
            return

        selected_surfaces = app().main_window.selection.geometry_surfaces
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
        tab_list = current_tab == TabIndex.LIST

        self.pushButton_apply.setDisabled(tab_list)
        self.pushButton_apply_and_close.setDisabled(tab_list)
        self.lineEdit_selection_id.setDisabled(tab_list)

        if self.last_tab == TabIndex.LIST or tab_list:
            app().main_window.selection.clear_selection()
            self.clear_line_edit_selection_id()

        if tab_list:
            self.lineEdit_connection_type.clear()   
            self.pushButton_remove.setDisabled(True)
            self.treeWidget_compressor_excitation.clearSelection()

        self.last_tab = current_tab

    def update_compressing_cylinders_setup(self):

        self.lineEdit_rod_diameter.setDisabled(False)
        self.doubleSpinBox_clearance_head_end.setDisabled(False)
        self.doubleSpinBox_clearance_crank_end.setDisabled(False)

        self.pushButton_plot_PV_diagram_head_end.setDisabled(False)
        self.pushButton_plot_PV_diagram_crank_end.setDisabled(False)
        self.pushButton_plot_PV_diagram_both_ends.setDisabled(False)
        self.pushButton_plot_pressure_head_end_angle.setDisabled(False)
        self.pushButton_plot_pressure_crank_end_angle.setDisabled(False)
        self.pushButton_plot_volume_head_end_angle.setDisabled(False)
        self.pushButton_plot_volume_crank_end_angle.setDisabled(False)

        if self.comboBox_cylinder_acting.currentIndex() == CylindersActingMode.HEAD_END:

            self.lineEdit_rod_diameter.clear()
            self.lineEdit_rod_diameter.setDisabled(True)

            self.doubleSpinBox_clearance_crank_end.setValue(0.)
            self.doubleSpinBox_clearance_crank_end.setDisabled(True)
            if self.doubleSpinBox_clearance_head_end.value() == 0.:
                self.doubleSpinBox_clearance_head_end.setValue(15.80)

            self.pushButton_plot_PV_diagram_crank_end.setDisabled(True)
            self.pushButton_plot_PV_diagram_both_ends.setDisabled(True)
            self.pushButton_plot_pressure_crank_end_angle.setDisabled(True)
            self.pushButton_plot_volume_crank_end_angle.setDisabled(True)

        elif self.comboBox_cylinder_acting.currentIndex() == CylindersActingMode.CRANK_END:

            if self.lineEdit_rod_diameter.text() == "":
                self.lineEdit_rod_diameter.setText("0.135")

            self.doubleSpinBox_clearance_head_end.setValue(0.)
            self.doubleSpinBox_clearance_head_end.setDisabled(True)
            if self.doubleSpinBox_clearance_crank_end.value() == 0.:
                self.doubleSpinBox_clearance_crank_end.setValue(18.39)

            self.pushButton_plot_PV_diagram_head_end.setDisabled(True)
            self.pushButton_plot_PV_diagram_both_ends.setDisabled(True)
            self.pushButton_plot_pressure_head_end_angle.setDisabled(True)
            self.pushButton_plot_volume_head_end_angle.setDisabled(True)

        elif self.comboBox_cylinder_acting.currentIndex() == CylindersActingMode.BOTH_ENDS:

            if self.lineEdit_rod_diameter.text() == "":
                self.lineEdit_rod_diameter.setText("0.135")

            if self.doubleSpinBox_clearance_head_end.value() == 0.:
                self.doubleSpinBox_clearance_head_end.setValue(15.80)

            if self.doubleSpinBox_clearance_crank_end.text() == 0.:
                self.doubleSpinBox_clearance_crank_end.setValue(18.39)

    def get_state_properties(self):

        if self.check_all_parameters(check_all_entries=False):
            return dict()

        state_properties = {
            "source" : "reciprocating_compressor",
            "connection_type" : self.comboBox_connection_type.currentText().lower(),
            "pressure_unit" : self.comboBox_pressure_units.currentText(),
            "temperature_unit" : self.comboBox_temperature_units.currentText(),
            "suction_pressure" : self.parameters.get("suction_pressure"),
            "suction_temperature" : self.parameters.get("suction_temperature"),
            "pressure_ratio" : self.parameters.get("pressure_ratio"),
            "isentropic_exponent" : self.parameters.get("isentropic_exponent"),
            "molar_mass" : self.parameters.get("molar_mass"),
            "check_ideal_gas" : True,
            }

        if self.comboBox_connection_type.currentIndex() == ConnectionType.DISCHARGE:
            T_suction = self.parameters.get("suction_temperature")
            P_suction = self.parameters.get("suction_pressure")
            p_ratio = self.parameters.get('pressure_ratio')
            k = self.parameters.get("isentropic_exponent", 1.4)

            P_discharge = p_ratio * P_suction

            # convert temperature to Kelvin scale
            temp_unit = self.comboBox_temperature_units.currentText()
            T_suction_K = convert_temperature_unit(T_suction, temp_unit, "K")

            # compute the temperature at the discharge
            T_discharge_K = T_suction_K * (p_ratio**((k-1)/k))

            # revert the temperature to its original units
            T_discharge = convert_temperature_unit(T_discharge_K, "K", temp_unit)

            state_properties.update({
                "discharge_pressure" : P_discharge,
                "discharge_temperature" : T_discharge,
            })

        return state_properties

    def get_fluid_callback(self):

        state_properties = self.get_state_properties()
        if not state_properties:
            return

        self.hide()
        self.fluid_dialog = SetFluidInputsSimplified(state_properties = state_properties)
        self.fluid_dialog.fluid_widget.pushButton_apply.setVisible(False)
        self.fluid_dialog.fluid_widget.pushButton_apply_and_close.clicked.connect(self.get_selected_fluid)
        self.fluid_dialog.exec_and_keep_window_open()
        app().main_window.set_input_widget(self)

    def get_selected_fluid(self):

        self.selected_fluid = self.fluid_dialog.get_selected_fluid()
        if not isinstance(self.selected_fluid, Fluid):
            return
        
        self.fluid_dialog.close()
        self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
        self.lineEdit_isentropic_exponent.setText(f"{self.selected_fluid.isentropic_exponent : .6f}")
        self.lineEdit_molar_mass.setText(f"{self.selected_fluid.molar_mass : .6f}")

        if self.comboBox_connection_type.currentIndex() == ConnectionType.DISCHARGE:
            temp_unit = self.comboBox_temperature_units.currentText()
            temperature = convert_temperature_unit(self.selected_fluid.temperature, "K", temp_unit)
            self.lineEdit_discharge_temperature.setText(f"{temperature : .6f}")

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
            connection_type = data.get("connection_type")
            if isinstance(connection_type, str):
                self.comboBox_connection_type.setCurrentText(connection_type.capitalize())

        # compressor model parameters
        parameters = data.get("parameters")
        if not isinstance(parameters, dict):
            return

        if "valves_per_head" in parameters.keys():
            self.spinBox_valves_per_head.setValue(parameters.get("valves_per_head", 1))

        if "bore_diameter" in parameters.keys():
            self.lineEdit_bore_diameter.setText(str(parameters["bore_diameter"]))

        if "stroke" in parameters.keys():
            self.lineEdit_stroke.setText(str(parameters["stroke"]))

        if "connecting_rod_length" in parameters.keys():
            self.lineEdit_connecting_rod_length.setText(str(parameters["connecting_rod_length"]))

        if "rod_diameter" in parameters.keys():
            self.lineEdit_rod_diameter.setText(str(parameters["rod_diameter"]))

        if "pressure_ratio" in parameters.keys():
            self.lineEdit_pressure_ratio.setText(str(parameters["pressure_ratio"]))

        if "clearance_HE" in parameters.keys():
            self.doubleSpinBox_clearance_head_end.setValue(parameters["clearance_HE"])

        if "clearance_CE" in parameters.keys():
            self.doubleSpinBox_clearance_crank_end.setValue(parameters["clearance_CE"])

        if "tdc_crank_angle" in parameters.keys():
            self.spinBox_tdc_crank_angle.setValue(parameters["tdc_crank_angle"])

        if "rotational_speed" in parameters.keys():
            self.doubleSpinBox_rotational_speed.setValue(parameters["rotational_speed"])

        if "capacity" in parameters.keys():
            self.spinBox_capacity.setValue(parameters["capacity"])

        if "isentropic_exponent" in parameters.keys():
            isentropic_exponent = parameters["isentropic_exponent"]
            self.lineEdit_isentropic_exponent.setText(f"{isentropic_exponent : .6f}")

        if "molar_mass" in parameters.keys():
            molar_mass = parameters["molar_mass"]
            self.lineEdit_molar_mass.setText(f"{molar_mass : .6f}")

        if "suction_pressure" in parameters.keys():
            self.lineEdit_suction_pressure.setText(str(parameters["suction_pressure"]))

        if "suction_temperature" in parameters.keys():
            self.lineEdit_suction_temperature.setText(str(parameters["suction_temperature"]))

        if "pressure_unit" in parameters.keys():
            self.comboBox_pressure_units.setCurrentText(parameters["pressure_unit"])

        if "temperature_unit" in parameters.keys():
            self.comboBox_temperature_units.setCurrentText(parameters["temperature_unit"])

        if "acting_mode" in parameters.keys():
            self.comboBox_cylinder_acting.setCurrentIndex(parameters["acting_mode"])

        if "compression_stage" in parameters.keys():
            comp_stage = parameters["compression_stage"]
            if isinstance(comp_stage, int):
                self.comboBox_compression_stage.setCurrentIndex(parameters["compression_stage"])
            elif isinstance(comp_stage, str):
                comp_stage_labels = ["1st stage", "2nd stage", "3rd stage"]
                index = comp_stage_labels.index(comp_stage)
                self.comboBox_compression_stage.setCurrentIndex(index)

        if "points_per_revolution" in parameters.keys():
            self.spinBox_number_of_points.setValue(int(parameters["points_per_revolution"]))

        f_min, f_max, f_step, N_rev = self.get_aquisition_parameters(parameters)
        self.lineEdit_number_of_revolutions.setText(str(N_rev))
        self.spinBox_max_frequency.setValue(int(f_max))
        self.lineEdit_frequency_resolution.setText(str(f_step))

        f_steps = [0.1, 0.2, 0.5, 1.0, 2.0]
        if f_step in f_steps:
            index = f_steps.index(f_step)
            self.comboBox_frequency_resolution.setCurrentIndex(index)

    def generate_mesh(self):
        if not app().project.model.is_there_a_valid_mesh():
            return mesher_interface_callback(self, close_after_generate=True)

    def check_input_surfaces(self):

        input_ids = self.lineEdit_selection_id.text()
        surface_id, error_data = self.model.check_selected_ids(
            input_ids,
            "surfaces",
            domain="acoustic",
            single_id=True
        )

        if error_data is not None:
            self.lineEdit_selection_id.setFocus()
            self.lineEdit_selection_id.selectAll()
            PrintMessageInput(error_data)
            return None

        volumes_from_surface = self.model.mesh.volumes_from_surface.get(surface_id)
        if len(volumes_from_surface) != 1:
            title = "Invalid surface selected"
            message = "The selected surface does not correspond to the piping endings. "
            message += "It is necessary to change the selection to proceed with the "
            message += "compressor excitation attribution."
            PrintMessageInput([error_title, title, message])
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
                    PrintMessageInput([error_title, title, message])
                    return True
                else:
                    self.value = value

            except Exception:
                message = f"You have typed an invalid value to the {label}."
                PrintMessageInput([error_title, title, message])
                return True
        else:
            message = f"None value has been typed to the {label}."
            PrintMessageInput([error_title, title, message])
            return True
        return False

    def check_all_parameters(self, check_all_entries: bool=True):

        self.parameters = dict()

        line_edits = [
            self.lineEdit_bore_diameter,
            self.lineEdit_stroke,
            self.lineEdit_connecting_rod_length,
            self.lineEdit_rod_diameter,
            self.lineEdit_pressure_ratio,
            self.lineEdit_suction_pressure,
            self.lineEdit_suction_temperature,
        ]

        if check_all_entries:
            line_edits.extend([
                self.lineEdit_isentropic_exponent,
                self.lineEdit_molar_mass,
            ])

        for line_edit in line_edits:
            if line_edit.text() == "":
                if line_edit == self.lineEdit_rod_diameter:
                    if self.comboBox_cylinder_acting.currentIndex() == CylindersActingMode.HEAD_END:
                        continue

                line_edit.setFocus()
                line_edit.setStyleSheet("border: 2px solid red")
                return True

            else:
                _style_sheet = line_edit.styleSheet()
                if _style_sheet != self.default_stylesheet:
                    line_edit.setStyleSheet(self.default_stylesheet)

            key = line_edit.objectName().split("lineEdit_")[1]
            self.parameters[key] = float(line_edit.text())

        self.parameters['acting_mode'] = self.comboBox_cylinder_acting.currentIndex()
        self.parameters['compression_stage'] = self.comboBox_compression_stage.currentIndex()
        self.parameters['clearance_HE'] = self.doubleSpinBox_clearance_head_end.value()
        self.parameters['clearance_CE'] = self.doubleSpinBox_clearance_crank_end.value()
        self.parameters['tdc_crank_angle'] = self.spinBox_tdc_crank_angle.value()
        self.parameters['rotational_speed'] = self.doubleSpinBox_rotational_speed.value()
        self.parameters['capacity'] = self.spinBox_capacity.value()
        self.parameters['valves_per_head'] = self.spinBox_valves_per_head.value()
        self.parameters['pressure_unit'] = self.comboBox_pressure_units.currentText()
        self.parameters['temperature_unit'] = self.comboBox_temperature_units.currentText()

        if check_all_entries:
            self.compressor = ReciprocatingCompressorModel(**self.parameters)
            self.compressor.process_remaining_fluid_properties()

        return False

    def process_aquisition_parameters(self):

        self.currentIndex = self.comboBox_frequency_resolution.currentIndex()
        if self.check_all_parameters():
            return True

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.max_frequency = self.spinBox_max_frequency.value()

        T_rev = 60 / self.parameters["rotational_speed"]
        list_T = [10, 5, 2, 1, 0.5]
        list_df = [0.1, 0.2, 0.5, 1, 2]

        T_selected = list_T[self.currentIndex]
        df_selected = list_df[self.currentIndex]

        if np.remainder(T_selected, T_rev) == 0:
            T = T_selected
            df = 1 / T
        else:
            i = 0
            df = 1 / (T_rev)
            while df > df_selected:
                i += 1
                df = 1 / (i * T_rev)

        self.N_rev = i

        final_df_label = "{} Hz".format(round(df, 6))
        self.lineEdit_frequency_resolution.setText(final_df_label)
        self.lineEdit_number_of_revolutions.setText(str(self.N_rev))
        self.aquisition_parameters_processed = True

    def save_table_values(self, table_name: str, frequencies: np.ndarray, complex_values: np.ndarray):

        if app().project.model.change_analysis_frequency_setup(list(frequencies)):
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        update_analysis_setup_in_file(frequencies)

        # real values vector
        real_values = np.real(complex_values)
        
        # imaginary values vector
        imag_values = np.imag(complex_values)

        data = np.array([frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def update_state_properties_at_discharge(self):

        try:
            # fluid properties
            k_isen = float(self.lineEdit_isentropic_exponent.text())
            suction_pressure = float(self.lineEdit_suction_pressure.text())

            # pressure ratio
            pressure_ratio = float(self.lineEdit_pressure_ratio.text())

            # compute the discharge pressure
            discharge_pressure = pressure_ratio * suction_pressure

            # update the discharge pressure text
            self.lineEdit_discharge_pressure.setText(f"{discharge_pressure : .8e}")

        except Exception:
            return

        try:
            # get the temperature unit
            temp_unit = self.comboBox_temperature_units.currentText()

            # convert the suction temperature to the Kelvin scale
            T_suction = float(self.lineEdit_suction_temperature.text())
            T_suction_K = convert_temperature_unit(T_suction, temp_unit, "K") 

            # compute the discharge temperature
            T_discharge_K = T_suction_K * (pressure_ratio**((k_isen - 1) / k_isen))

            # reverts the original units to discharge temperature
            T_discharge = convert_temperature_unit(T_discharge_K, "K", temp_unit)

            # update the discharge temperature text
            self.lineEdit_discharge_temperature.setText(f"{T_discharge : .6f}")

        except Exception:
            return

    def apply_callback(self, close_window: bool = False):

        if self.generate_mesh():
            return True

        surface_id = self.check_input_surfaces()
        if surface_id is None:
            return True

        if self.process_aquisition_parameters():
            return

        if self.comboBox_connection_type.currentIndex() == ConnectionType.SUCTION:
            flow_label = "in_flow"
        else:
            flow_label = "out_flow"

        volume_id = self.model.mesh.volumes_from_surface[surface_id]
        connection_type = self.comboBox_connection_type.currentText().lower()

        state_properties = self.get_state_properties()
        if not state_properties:
            return True

        state_properties.update({"surface_id" : surface_id, "volume_id" : volume_id[0]})

        if not isinstance(self.selected_fluid, Fluid):

            self.hide()
            dialog = SetFluidInputs(state_properties = state_properties)
            app().main_window.set_input_widget(self)

            if not dialog.complete:
                return

            self.selected_fluid = dialog.fluid_widget.get_selected_fluid()
            if not isinstance(self.selected_fluid, Fluid):
                return

        self.parameters["molar_mass"] = self.selected_fluid.molar_mass
        self.parameters['isentropic_exponent'] = self.selected_fluid.isentropic_exponent
        self.parameters['points_per_revolution'] = self.compressor.number_points

        self.compressor.update_fluid_properties(
            self.selected_fluid.isentropic_exponent,
            self.selected_fluid.molar_mass,
            )

        self.model.mesh.process_face_elements_connected_to_nodes(surface_id)
        surface_area = self.model.mesh.surface_area_from_element_integration[surface_id]

        # process the volumetric flow rate spectrum (per valve)
        frequencies, flow_rate = self.compressor.process_FFT_of_volumetric_flow_rate(self.N_rev, flow_label)

        # compute the surface velocity
        surface_velocity = flow_rate / surface_area

        table_name = f"compressor_excitation_{connection_type}_surface_{surface_id}"

        if self.checkBox_export_data.isChecked():
            def export_data_callback():    
                logging.info("Exporting the compressor excitation data... (15%)")

                output_data_type = self.comboBox_output_data_type.currentText()
                if output_data_type == "Surface velocity [m/s]":
                    unit = "m/s"
                    output_data = surface_velocity

                else:
                    unit = "m³/s"
                    output_data = flow_rate

                logging.info("Exporting the compressor excitation data... (25%)")
                self.export_reciprocating_compressor_data_excitation(surface_id, frequencies, output_data, unit)

            LoadingWindow(export_data_callback).run()

        data = {
            "connection_type": connection_type,
            "table_names": [table_name],
            "parameters": self.parameters,
            "values": [surface_velocity],
            "element_integration": True,
        }

        self.remove_conflicting_excitations(surface_id)

        if self.save_table_values(table_name, frequencies, surface_velocity):
            return True

        self.properties._set_property("reciprocating_compressor_excitation", data, surface=surface_id)
        self.actions_to_finalize(close_window)

    def export_compressor_excitation_data(self, surface_id: int, surface_area: float, frequencies: np.ndarray, flow_rate: np.ndarray):
        output_data_type = self.comboBox_output_data_type.currentText()
        if output_data_type == "Surface velocity [m/s]":
            unit = "m/s"
            output_data = flow_rate / surface_area

        else:
            unit = "m³/s"
            output_data = flow_rate

        self.export_reciprocating_compressor_data_excitation(surface_id, frequencies, output_data, unit)

    def actions_to_finalize(self, close_window: bool = False):
        self.load_compressor_excitation_info()
        app().project.update_model_properties_file()
        app().main_window.selection.set_geometry_selection()
        app().main_window.update_symbols()

        if close_window:
            self.close()

    def remove_conflicting_excitations(self, surface_id: int):

        labels = [
            "acoustic_pressure",
            "surface_velocity",
            "incident_plane_wave",
            "compressor_excitation_spectrum",
            "compressor_excitation_waveform",
            "reciprocating_compressor_excitation",
            "mass_source",
            ]

        for label in labels:
            self.properties._remove_surface_property(label, surface_id)

    def remove_callback(self):
        surface_ids = [int(selected_item.text(0)) for selected_item in self.treeWidget_compressor_excitation.selectedItems()]

        if not surface_ids:
            return
        
        for surface_id in surface_ids:
            self.properties._remove_surface_property("reciprocating_compressor_excitation", surface_id)
        
        self.clear_line_edit_selection_id()
        self.lineEdit_connection_type.clear()
        self.pushButton_remove.setDisabled(True)

        app().main_window.selection.clear_selection()
        self.actions_to_finalize()

    def reset_callback(self):

        title = "Resetting of compressor excitations"
        message = "Would you like to remove all compressor excitations from the acoustic model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            self.properties._reset_property("reciprocating_compressor_excitation")
            self.actions_to_finalize()

    def load_compressor_excitation_info(self):

        self.treeWidget_compressor_excitation.clear()
        acting_labels = ["both ends", "head end", "crank end"]

        for (property, *args), data in self.properties.surface_properties.items():
            if property != "reciprocating_compressor_excitation":
                continue

            if not isinstance(data, dict):
                continue

            rc_param = data.get("parameters")
            if not isinstance(rc_param, dict):
                continue

            surface_id = args[0]
            connection_type = data["connection_type"]
            acting_mode = rc_param.get("acting_mode", CylindersActingMode.HEAD_END)
            tdc_crank_angle = rc_param.get("tdc_crank_angle", 0)

            new = QTreeWidgetItem([str(surface_id), connection_type, acting_labels[acting_mode], str(tdc_crank_angle)])
            for i in range(4):
                new.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_compressor_excitation.addTopLevelItem(new)

        self.update_tabs_visibility()

    def on_click_item(self, item: QTreeWidgetItem):
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

        self.lineEdit_selection_id.setText(selection_text)
        self.lineEdit_selection_id.setToolTip(selection_text)
    
    def clear_line_edit_selection_id(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_selection_id.setToolTip("")

    def update_tabs_visibility(self):
        self.lineEdit_selection_id.clear()
        self.lineEdit_connection_type.clear()
        self.pushButton_remove.setDisabled(True)

        for (property, *_) in self.properties.surface_properties:
            if property != "reciprocating_compressor_excitation":
                continue

            self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
            return

        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)
        self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)

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
        self.update_state_properties_at_discharge()

    def temperature_unit_callback(self):
        unit_label = self.comboBox_temperature_units.currentText()
        self.label_suction_temperature_unit.setText(f"[{unit_label}]")
        self.label_discharge_temperature_unit.setText(f"[{unit_label}]")
        self.update_state_properties_at_discharge()

    def plot_PV_diagram_head_end(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        volume_HE, pressure_HE = self.compressor.get_PV_diagram_head_end_data()
        if volume_HE is None:
            return

        plotter = Plot2DSimplified(
            x_label="Volume [m³]",
            y_left_label=f"Pressure [{self.compressor.pressure_unit}]",
            title="P-V diagram (head end)",
        )
        plotter.set_plot_data(volume_HE, pressure_HE)
        plotter.show()

    def plot_PV_diagram_crank_end(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        volume_CE, pressure_CE = self.compressor.get_PV_diagram_crank_end_data()
        if volume_CE is None:
            return

        plotter = Plot2DSimplified(
            x_label="Volume [m³]",
            y_left_label=f"Pressure [{self.compressor.pressure_unit}]",
            title="P-V diagram (crank end)",
        )
        plotter.set_plot_data(volume_CE, pressure_CE)
        plotter.show()

    def plot_PV_diagram_both_ends(self):
        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        volume_HE, pressure_HE = self.compressor.get_PV_diagram_head_end_data()
        if volume_HE is None:
            return

        volume_CE, pressure_CE = self.compressor.get_PV_diagram_crank_end_data()
        if volume_CE is None:
            return

        plotter = Plot2DSimplified(
            x_label="Volume [m³]",
            y_left_label=f"Pressure [{self.compressor.pressure_unit}]",
            title="P-V RECIPROCATING COMPRESSOR DIAGRAM",
        )

        plotter.set_plot_data(volume_HE, pressure_HE, label="Head End", color=(1, 0, 0))
        plotter.set_plot_data(volume_CE, pressure_CE, label="Crank End", color=(0, 0, 1), line_style="--")
        plotter.show()

    def plot_pressure_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        time, pressure_HE, pressure_CE = self.compressor.get_pressure_vs_time_data()
        if pressure_HE is None:
            return

        plotter = Plot2DSimplified(
            x_label="Time [s]",
            y_left_label=f"Pressure [{self.compressor.pressure_unit}]",
            title="PRESSURES vs TIME PLOT",
        )
        plotter.set_plot_data(time, pressure_HE, label="Head End", color=(1, 0, 0))
        plotter.set_plot_data(time, pressure_CE, label="Crank End", color=(0, 0, 1), line_style="--")
        plotter.show()

    def plot_volume_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        time, volume_HE, volume_CE = self.compressor.get_volume_vs_time_data()

        plotter = Plot2DSimplified(
            x_label="Time [s]",
            y_left_label="Volume [m³]",
            title="VOLUMES vs TIME PLOT",
        )
        plotter.set_plot_data(time, volume_HE, label="Head End", color=(1, 0, 0))
        plotter.set_plot_data(time, volume_CE, label="Crank End", color=(0, 0, 1), line_style="--")
        plotter.show()
    
    def plot_volumetric_flow_rate_at_suction_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        time, flow_rate = self.compressor.get_volumetric_flow_rate_at_suction_time_data()
        if flow_rate is None:
            return

        plotter = Plot2DSimplified(
            x_label="Time [s]",
            y_left_label="Volume [m³/s]",
            title="Volumetric flow rate at suction",
        )
        plotter.set_plot_data(time, flow_rate)
        plotter.show()

    def plot_volumetric_flow_rate_at_discharge_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        time, flow_rate = self.compressor.get_volumetric_flow_rate_at_discharge_time_data()
        if flow_rate is None:
            return

        plotter = Plot2DSimplified(
            x_label="Time [s]",
            y_left_label="Volume [m³/s]",
            title="Volumetric flow rate at discharge",
        )
        plotter.set_plot_data(time, flow_rate)
        plotter.show()
    
    def plot_rod_pressure_load_frequency(self):
        self.process_aquisition_parameters()

        freq, rod_pressure_load = self.compressor.get_rod_pressure_load_frequency_data(self.N_rev)

        plotter = Plot2DSimplified(
            x_label="Frequency [Hz]",
            y_left_label="Rod pressure load [kN]",
            title="Rod pressure load",
        )
        plotter.set_plot_data(freq, rod_pressure_load, absolute_value=True)
        plotter.show()

    def plot_rod_pressure_load_time(self):
        self.process_aquisition_parameters()

        time, rod_pressure_load_time = self.compressor.get_rod_pressure_load_time_data()

        plotter = Plot2DSimplified(
            x_label="Time [s]",
            y_left_label="Rod pressure load [kN]",
            title="Rod pressure load",
        )

        plotter.set_plot_data(time, rod_pressure_load_time, absolute_value=True)
        plotter.show()
    
    def plot_piston_position_and_velocity_time(self):
        self.process_aquisition_parameters()

        x_data, position, velocity = self.compressor.get_piston_position_and_velocity_data(domain="time")

        plotter = Plot2DSimplified(
            x_label="Time [s]",
            y_left_label="Piston relative displacement [m]",
            y_right_label="Piston velocity [m/s]",
            title="Piston displacement and velocity during a complete cycle",
        )
        plotter.set_plot_data(x_data, position, label="Piston position", color=(0, 0, 0))
        plotter.set_plot_data(x_data, velocity, label="Piston velocity", color=(0, 0, 1), y_label_position="right")
        plotter.show()

    def plot_piston_position_and_velocity_angle(self):
        self.process_aquisition_parameters()

        x_data, position, velocity = self.compressor.get_piston_position_and_velocity_data(domain="angle")

        plotter = Plot2DSimplified(
            x_label="Angle [deg]",
            y_left_label="Piston relative displacement [m]",
            y_right_label="Piston velocity [m/s]",
            title="Piston displacement and velocity during a complete cycle",
        )
        plotter.set_plot_data(x_data, position, label="Piston position", color=(0, 0, 0), line_width=2)
        plotter.set_plot_data(x_data, velocity, label="Piston velocity", color=(0, 0, 1), line_width=2, y_label_position="right")
        plotter.show()

    def plot_volumetric_flow_rate_at_suction_frequency(self):
        self.process_aquisition_parameters()

        freq, flow_rate = self.compressor.get_volumetric_flow_rate_at_suction_frequency_data(self.N_rev)
        if flow_rate is None:
            return

        plotter = Plot2DSimplified(
            x_label="Frequency [Hz]",
            y_left_label="Volumetric head flow rate [m³/s]",
            title="Volumetric flow rate at suction",
        )
        plotter.set_plot_data(freq, flow_rate, absolute_value=True)
        plotter.show()

    def plot_volumetric_flow_rate_at_discharge_frequency(self):
        self.process_aquisition_parameters()

        freq, flow_rate = self.compressor.get_volumetric_flow_rate_at_discharge_frequency_data(self.N_rev)
        if flow_rate is None:
            return

        plotter = Plot2DSimplified(
            x_label="Frequency [Hz]",
            y_left_label="Volumetric crank flow rate [m³/s]",
            title="Volumetric flow rate at discharge",
        )
        plotter.set_plot_data(freq, flow_rate, absolute_value=True)
        plotter.show()

    def plot_pressure_head_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        angle, pressure_HE = self.compressor.get_head_end_pressure_angle_data()

        plotter = Plot2DSimplified(
            x_label="Crank angle [degree]",
            y_left_label=f"Pressure [{self.compressor.pressure_unit}]",
            title="Head end pressure vs Angle",
        )
        plotter.set_plot_data(angle, pressure_HE)
        plotter.show()

    def plot_volume_head_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        angle, volume_HE = self.compressor.get_head_end_volume_angle_data()

        plotter = Plot2DSimplified(
            x_label="Crank angle [degree]",
            y_left_label="Volume [m³]",
            title="Head end volume vs Angle",
        )
        plotter.set_plot_data(angle, volume_HE)
        plotter.show()

    def plot_pressure_crank_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        angle, pressure_CE = self.compressor.get_crank_end_pressure_angle_data()

        plotter = Plot2DSimplified(
            x_label="Crank angle [degree]",
            y_left_label=f"Pressure [{self.compressor.pressure_unit}]",
            title="Crank end pressure vs Angle",
        )
        plotter.set_plot_data(angle, pressure_CE)
        plotter.show()

    def plot_volume_crank_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        angle, volume_CE = self.compressor.get_crank_end_volume_angle_data()

        plotter = Plot2DSimplified(
            x_label="Crank angle [degree]",
            y_left_label="Volume [m³]",
            title="Crank end volume vs Angle",
        )
        plotter.set_plot_data(angle, volume_CE)
        plotter.show()

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
        file_path, check = self.exporter.getSaveFileName(app().main_window, caption, str(directory_path), filter=ext_filter)
        if not check:
            return

        self.checkBox_export_data.setChecked(True)
        self.lineEdit_export_path.setText(file_path)

        app().config.write_last_folder_path_in_file("exported_data_folder", file_path)

    def export_reciprocating_compressor_data_excitation(self, surface_id: int, frequencies: np.ndarray, excitation_data: np.ndarray, unit: str):

        recip_excitation_data = dict()
        title = "Reciprocating compressor excitation"

        if unit == "m/s":
            key = ("surface_velocity_at", surface_id)
        else:
            key = ("flow_rate_at", surface_id)

        legend_label = f"Reciprocating compressor excitation at surface [{surface_id}]"

        recip_excitation_data[key] = {
            "x_data": frequencies,
            "y_data": excitation_data,
            "x_label": "Frequency [Hz]",
            "y_label": "Compressor excitation",
            "title": title,
            "data_type": "compressor excitation",
            "legend": legend_label,
            "unit": unit,
            "color": [0, 0, 1],
            "linestyle": "-",
        }

        if self.exporter is None:
            self.exporter = ExportModelResults()

        file_path = self.lineEdit_export_path.text()
        if self.is_file_path_valid(file_path):
            file_path = Path(file_path)
        else:
            file_path = ""

        self.exporter._set_data_to_export(recip_excitation_data, existing_path=file_path)

    def is_file_path_valid(self, file_path: str):
        if Path(dirname(file_path)).exists():
            ext = file_path.split(".")[-1].lower()
            if ext in SUPPORTED_OUTPUT_DATA_EXTENSIONS:
                return True
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.apply_callback()
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
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)