from PySide6.QtWidgets import QComboBox, QDialog, QDoubleSpinBox, QFrame, QLineEdit, QPushButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app, UI_DIR
from vibra.engine.properties.fluid import Fluid
from vibra.engine.transfer_impedances.perforate_plate import PerforatedPlateModels
from vibra.interface.mesh.mesher_inputs import MesherInputs
from vibra.interface.model_inputs.acoustic.fluid.set_fluid_input_simplified import SetFluidInputSimplified
from vibra.interface.model_inputs.acoustic.get_sphere_selection_information import GetSphereSelectionInformation
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

from molde import load_ui

import warnings
import numpy as np

# fmt: off

window_title_1 = "Error"
window_title_2 = "Warning"

class SetPerforatedPlateModelInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/set_perforated_plate_model_inputs.ui"
        load_ui(ui_path, self, ui_path.parent)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.action_model_workspace_callback()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        # self._create_connections()
        # self._config_widgets()

        # self.load_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _initialize(self):
        self.selected_fluid = None
        self.keep_window_open = True
        self.pp_model_data = dict()

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type: QComboBox
        self.comboBox_plot_type: QComboBox

        # QDoubleSpin
        self.doubleSpinBox_selection_radius: QDoubleSpinBox
        self.doubleSpinBox_evaluated_depth: QDoubleSpinBox

        # QFrame
        self.frame_fluid_info: QFrame
        self.frame_plot_buttons: QFrame

        # QLineEdit
        self.lineEdit_selection_id: QLineEdit
        self.lineEdit_selected_fluid: QLineEdit
        self.lineEdit_fluid_density: QLineEdit
        self.lineEdit_speed_of_sound: QLineEdit
        self.lineEdit_plate_thickness: QLineEdit
        self.lineEdit_hole_diameter: QLineEdit
        self.lineEdit_porosity: QLineEdit
        self.lineEdit_discharge_coefficient: QLineEdit

        # QPushButton
        self.pushButton_exit: QPushButton
        self.pushButton_confirm: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton
        # self.pushButton_get_fluid: QPushButton
        # self.pushButton_plot_data: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_perforated_plate_model: QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_plot_type.currentIndexChanged.connect(self.plot_type_callback)
        #
        self.doubleSpinBox_selection_radius.valueChanged.connect(self.call_sphere_plotter)
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.attribute_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        # self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        # self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tabEvent_callback)
        #
        self.treeWidget_perforated_plate_model.itemClicked.connect(self.on_click_item)
        self.treeWidget_perforated_plate_model.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.geometry_selection_callback()
        self.attribution_type_callback()
        self.update_plot_buttons_access()

    def update_plot_buttons_access(self):
        state = self.selected_fluid is None
        self.comboBox_plot_type.setDisabled(state)
        self.pushButton_plot_data.setDisabled(state)
        self.plot_type_callback()

    def plot_type_callback(self):
        if self.comboBox_plot_type.currentIndex() < 2:
            self.doubleSpinBox_evaluated_depth.setDisabled(True)
        else:
            self.doubleSpinBox_evaluated_depth.setDisabled(False)

    def _config_widgets(self):
        for i, w in enumerate([90, 60, 130, 120, 120]):
            self.treeWidget_perforated_plate_model.setColumnWidth(i, w)
            self.treeWidget_perforated_plate_model.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def remove_callback(self):
        if self.lineEdit_selection_id.text() != "":

            key = self.lineEdit_selection_id.text().split(" - ")
            selection_type = key[0]
            selection_id = int(key[1])

            if selection_type == "Volume":
                self.properties._remove_volume_property("viscous_thermal_model", selection_id)
            else:
                self.properties._remove_group_property("viscous_thermal_model", selection_id)

            app().file.write_model_properties_in_file()
            self.pushButton_remove.setDisabled(True)
            self.load_info()

    def reset_callback(self):

        volume_ids = list()
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "viscous_thermal_model":
                volume_ids.append(volume_id)

        group_ids = list()
        for key, data in self.properties.group_properties.items():
            property, group_id = key
            if property == "viscous_thermal_model":
                group_ids.append(group_id)

        if volume_ids or group_ids:

            self.hide()

            title = "Viscous-thermal dissipation model resetting"
            message = "Would you like to remove the Viscous-thermal dissipation effects from the model?"

            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:

                for volume_id in volume_ids:
                    self.properties._remove_volume_property("viscous_thermal_model", volume_id)

                for group_id in group_ids:
                    self.properties._remove_group_property("viscous_thermal_model", group_id)

                app().file.write_model_properties_in_file()
                self.load_info()

    def tabEvent_callback(self):

        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 2:
            self.comboBox_attribution_type.setCurrentIndex(1)
            self.comboBox_attribution_type.setDisabled(True)
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
            self.frame_fluid_info.setDisabled(True)
            self.frame_plot_buttons.setDisabled(True)

        else:

            if "-" in self.lineEdit_selection_id.text():
                self.lineEdit_selection_id.setText("")

            self.frame_fluid_info.setDisabled(False)
            self.frame_plot_buttons.setDisabled(False)

            self.comboBox_attribution_type.setDisabled(False)
            if self.comboBox_attribution_type.currentIndex() == 0:
                return

            self.lineEdit_selection_id.setDisabled(False)

    def on_click_item(self, item):

        key = f"{item.text(0)} - {item.text(1)}"
        if item.text(0) == "Volume":
            volume_id = int(item.text(1))
            app().main_window.set_geometry_selection(volumes=[volume_id])

        self.lineEdit_selection_id.setText(key)
        self.pushButton_remove.setEnabled(True)

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def attribution_type_callback(self):

        self.doubleSpinBox_selection_radius.setDisabled(True)

        attribution_type = self.comboBox_attribution_type.currentIndex()
        if attribution_type == 0:
            surfaces = self.main_window.selected_geometry_surfaces
            if not surfaces:
                self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setEnabled(True)

        elif attribution_type == 1:
            self.lineEdit_selection_id.setText("All faces")
            self.lineEdit_selection_id.setEnabled(False)

    def load_info(self):

        self.treeWidget_perforated_plate_model.clear()

        for key, data in self.properties.surface_properties.items():

            property, face_id = key
            if property == "perforate_plate_model":

                section_type = ""
                formulation = ""

                model_inputs = list()
                continue

                for key, value in data.items():
                    if key == "section_type":
                        section_type = data["section_type"]
                    elif key == "formulation":
                        formulation = data["formulation"]
                    else:
                        model_inputs.append(value)

                new = QTreeWidgetItem([str(face_id), section_type, formulation, str(model_inputs)])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_perforated_plate_model.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        for key, _ in self.properties.volume_properties.items():
            property, _ = key
            if property == "perforate_plate_model":
                self.tabWidget_main.setTabVisible(2, True)
                return

        for key, _ in self.properties.group_properties.items():
            property, _ = key
            if property == "perforate_plate_model":
                self.tabWidget_main.setTabVisible(2, True)
                return

        self.tabWidget_main.setTabVisible(2, False)
        self.tabWidget_main.setCurrentIndex(0)

    def geometry_selection_callback(self):

        faces = self.main_window.selected_geometry_surfaces

        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            self.comboBox_attribution_type.setCurrentIndex(0)

    def get_perforate_plate_circular_hole_inputs(self):

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
        
        lineEdit = self.lineEdit_discharge_coefficient
        discharge_coefficient = self.check_inputs(lineEdit, "Discharge coefficient")
        if discharge_coefficient is None:
            lineEdit.setFocus()
            return dict()

        if self.tabWidget_main.currentIndex() == 0:
            formulation = "circular_hole"
        
        perforated_plate_data = {
                                "formulation" : formulation,
                                "plate_thickness" : plate_thickness,
                                "hole_diameter" : hole_diameter,
                                "porosity" : porosity,
                                "discharge_coefficient" : discharge_coefficient
                                }

        return perforated_plate_data

    def attribute_callback(self):

        if self.tabWidget_main.currentIndex() == 0:
            model_data = self.get_perforate_plate_circular_hole_inputs()

        else:
            return

        if model_data:

            attribute_type = self.comboBox_attribution_type.currentIndex()
            if attribute_type in [0, 1]:
                
                surface_ids = list()
                if attribute_type == 1:
                    if "surfaces" in self.mesh.geometry_information.keys():
                        surface_ids = self.mesh.geometry_information["surfaces"]

                elif attribute_type == 0:
                    input_ids = self.lineEdit_selection_id.text()
                    surface_ids = self.mesh.check_selected_ids(
                                                               input_ids, 
                                                               selection = "surfaces", 
                                                               single_id = False
                                                               )

                    if surface_ids is None:
                        self.lineEdit_selection_id.setFocus()
                        return True

                for surface_id in surface_ids:
                    self.properties._set_property("viscous_thermal_model", model_data, surface=surface_id)

                print(f"The viscous_thermal {model_data['formulation']} model for '{model_data['section_type']}' has been attributed to the surfaces {surface_ids}.")

            app().file.write_model_properties_in_file()
            self.load_info()

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
            PrintMessageInput([window_title_1, title, message])
            return None
        else:
            return out

    # Plot viscous_thermal effective properties

    def get_fluid_callback(self):
        self.hide()
        self.fluid_dialog = SetFluidInputSimplified()
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

    def get_effective_properties(self, fluid: Fluid):

        warnings.filterwarnings('ignore')

        frequencies = None
        analysis_data = app().project.analysis_data
        if isinstance(analysis_data, dict):
            frequencies = analysis_data.get("frequencies", None)

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

        model = PerforatedPlateModels(self)

        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == 0:
            pp_data = self.get_circular_hole_inputs()

        if pp_data:
            if tab_index == 0:
                rho_eff, C_eff = model.get_transfer_impedance_for_circular_holes(omega, fluid, pp_data)

            k_cr = omega / C_eff

            return freq, rho_eff, C_eff, k_cr

        return None, None, None, None

    def get_perforated_plate_model(self):
        tab_index = self.tabWidget_main.currentIndex()
        
        if tab_index == 0:
            return "Circular hole"


    def plot_data_callback(self):
        plot_key = self.comboBox_plot_type.currentIndex()
        if plot_key == 0:
            self.plot_effective_fluid_density()
        elif plot_key == 1:
            self.plot_effective_speed_of_sound()
        elif plot_key == 2:
            self.plot_surface_impedance()
        else:
            self.plot_absorption_coefficient()

    def plot_effective_fluid_density(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        freq, rho_eff, _, _ = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        tv_model = self.get_perforated_plate_model()
        self.plot_data(freq, rho_eff, "effective fluid density", tv_model)

    def plot_effective_speed_of_sound(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        freq, _, C_eff, _ = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        tv_model = self.get_perforated_plate_model()
        self.plot_data(freq, C_eff, "effective speed of sound", tv_model)

    def plot_surface_impedance(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        return

        h = self.spinBox_number_of_terms.value()
        Z_0 = self.selected_fluid.speed_of_sound * self.selected_fluid.fluid_density

        freq, rho_eff, C_eff, k_cr = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        Z_pm = rho_eff * C_eff
        Z_s = Z_pm * (1 / np.tanh(k_cr * h))
        Z_norm = Z_s / Z_0

        tv_model = self.get_perforated_plate_model()
        self.plot_data(freq, Z_norm, "normalized surface impedance", tv_model)

    def plot_absorption_coefficient(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        return

        h = self.spinBox_number_of_terms.value()
        Z_0 = self.selected_fluid.speed_of_sound * self.selected_fluid.fluid_density

        freq, rho_eff, C_eff, k_cr = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        Z_pm = rho_eff * C_eff
        Z_s = Z_pm * (1 / np.tanh(k_cr * h))

        R_r = (Z_s - Z_0) / (Z_s + Z_0)
        alpha_n = 1 - np.abs(R_r)**2

        pm_model = self.get_perforated_plate_model()
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        try:
            warnings.filterwarnings('default')
            geometry_widget = self.main_window.geometry_widget
            geometry_widget.selection_changed.disconnect(self.geometry_selection_callback)
        except TypeError:
            pass  # ignore if there is nothing to disconect

        self.keep_window_open = False
        return super().closeEvent(a0)
    
# fmt: on