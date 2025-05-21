from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.interface.ui_generated.model.setup.acoustic.viscous_thermal_model_inputs_ui import ViscousThermalModelInputs_UI
from vibra.engine.properties.fluid import Fluid
from vibra.engine.dissipation_models.viscous_thermal_loss_models import ViscousThermalLossModels
from vibra.interface.mesh.set_mesh_setup_inputs import MeshSetupInputs
from vibra.interface.model_inputs.acoustic.fluid.simplified_fluid_inputs import SimplifiedFluidInputs
from vibra.interface.model_inputs.acoustic.get_sphere_selection_information import GetSphereSelectionInformation
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

import warnings
import numpy as np

# fmt: off

window_title_1 = "Error"
window_title_2 = "Warning"

class ViscousThermalLossModelInputs(ViscousThermalModelInputs_UI):
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
        self._configure_qt_variables()
        self._create_connections()
        self._config_widgets()

        self.load_info()

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
        self.material_model_data = dict()

    def _configure_qt_variables(self):
        self.lineEdit_center_coordinates.setDisabled(True)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_section_type.currentIndexChanged.connect(self.rectangular_section_type_callback)
        self.comboBox_plot_type.currentIndexChanged.connect(self.plot_type_callback)
        #
        self.doubleSpinBox_selection_radius.valueChanged.connect(self.call_sphere_plotter)
        #
        self.lineEdit_width_rectangular.textChanged.connect(self.update_rectangular_duct_area)
        self.lineEdit_height_rectangular.textChanged.connect(self.update_rectangular_duct_area)
        self.lineEdit_diameter_circular.textChanged.connect(self.update_circular_duct_area)
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.attribute_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        self.pushButton_selection_info.clicked.connect(self.get_selection_information)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tabEvent_callback)
        #
        self.treeWidget_viscous_thermal_model.itemClicked.connect(self.on_click_item)
        self.treeWidget_viscous_thermal_model.itemDoubleClicked.connect(self.on_doubleclick_item)
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
            self.treeWidget_viscous_thermal_model.setColumnWidth(i, w)
            self.treeWidget_viscous_thermal_model.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def update_rectangular_duct_area(self):
        try:
            height = float(self.lineEdit_height_rectangular.text())
            if self.comboBox_section_type.currentIndex() == 1:
                self.lineEdit_width_rectangular.setText(f"{round(height, 6)}")
            width = float(self.lineEdit_width_rectangular.text())
            area = width * height
            self.lineEdit_area_rectangular.setText(f"{round(area, 6)}")
        except:
            self.lineEdit_area_rectangular.setText("--")

    def update_circular_duct_area(self):
        try:
            diameter = float(self.lineEdit_diameter_circular.text())
            area = (np.pi / 4) * (diameter**2)
            self.lineEdit_radius_circular.setText(f"{round(diameter/2, 6)}")
            self.lineEdit_area_circular.setText(f"{round(area, 6)}")
        except:
            self.lineEdit_area_circular.setText("--")

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
        self.get_lrf_info()

    def rectangular_section_type_callback(self):

        section_index = self.comboBox_section_type.currentIndex()

        if section_index in [1, 2]:
            self.lineEdit_width_rectangular.setDisabled(True)
            if section_index == 2:
                self.spinBox_number_of_terms.setDisabled(True)
                self.lineEdit_width_rectangular.setText("2*a >> 2*b")
            else:
                self.spinBox_number_of_terms.setEnabled(True)
                height = self.lineEdit_height_rectangular.text()
                self.lineEdit_width_rectangular.setText(height)

        else:

            self.spinBox_number_of_terms.setEnabled(True)
            self.lineEdit_width_rectangular.setDisabled(False)
            if self.lineEdit_width_rectangular.text() == "2*a >> 2*b":
                self.lineEdit_width_rectangular.setText("")

    def attribution_type_callback(self):

        self.comboBox_filter_type.setDisabled(True)
        self.doubleSpinBox_selection_radius.setDisabled(True)
        self.pushButton_selection_info.setDisabled(True)

        attribution_type = self.comboBox_attribution_type.currentIndex()
        if attribution_type == 0:
            self.lineEdit_selection_id.setText("All bodies")
            self.lineEdit_selection_id.setEnabled(False)
            self.hide_sphere()

        elif attribution_type == 1:
            volumes = self.main_window.selected_geometry_volumes
            if not volumes:
                self.lineEdit_selection_id.setText("")

            self.lineEdit_selection_id.setEnabled(True)
            self.hide_sphere()

        elif attribution_type in [2, 3]:
            surfaces = self.main_window.selected_geometry_surfaces
            if not surfaces or self.lineEdit_selection_id.text() == "All bodies":
                self.lineEdit_selection_id.setText("")

            self.comboBox_filter_type.setEnabled(True)
            self.doubleSpinBox_selection_radius.setEnabled(True)
            self.pushButton_selection_info.setEnabled(True)
            self.call_sphere_plotter()

    def load_info(self):

        self.treeWidget_viscous_thermal_model.clear()

        for key, data in self.properties.volume_properties.items():

            property, volume_id = key
            if property == "viscous_thermal_model":

                section_type = ""
                formulation = ""

                model_inputs = list()
                for key, value in data.items():
                    if key == "section_type":
                        section_type = data["section_type"]
                    elif key == "formulation":
                        formulation = data["formulation"]
                    else:
                        model_inputs.append(value)

                new = QTreeWidgetItem(["Volume", str(volume_id), section_type, formulation, str(model_inputs)])
                for i in range(5):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_viscous_thermal_model.addTopLevelItem(new)

        for key, data in self.properties.group_properties.items():

            property, group_id = key
            if property == "viscous_thermal_model":
                
                section_type = ""
                formulation = ""

                model_inputs = list()
                for key, value in data.items():
                    if key == "section_type":
                        section_type = data["section_type"]
                    elif key == "formulation":
                        formulation = data["formulation"]
                    else:
                        model_inputs.append(value)

                new = QTreeWidgetItem(["Group", str(group_id), section_type, formulation, str(model_inputs)])
                for i in range(5):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_viscous_thermal_model.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        for key, _ in self.properties.volume_properties.items():
            property, _ = key
            if property == "viscous_thermal_model":
                self.tabWidget_main.setTabVisible(2, True)
                return

        for key, _ in self.properties.group_properties.items():
            property, _ = key
            if property == "viscous_thermal_model":
                self.tabWidget_main.setTabVisible(2, True)
                return

        self.tabWidget_main.setTabVisible(2, False)
        self.tabWidget_main.setCurrentIndex(0)

    def highlight_mesh_elements(self, elements):
        mesh_widget = self.main_window.mesh_widget
        mesh_widget.select_multiple_volumes(elements)

    def geometry_selection_callback(self):
        if not self.isVisible():
            return

        faces = self.main_window.selected_geometry_surfaces
        volumes = self.main_window.selected_geometry_volumes

        if volumes:
            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selection_id.setText(text)
            self.lineEdit_center_coordinates.setText("---")
            if self.comboBox_attribution_type.currentIndex() != 1:
                self.comboBox_attribution_type.setCurrentIndex(1)
            self.hide_sphere()

        elif faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
            if self.comboBox_attribution_type.currentIndex() in [0, 1]:
                self.comboBox_attribution_type.setCurrentIndex(2)
            else:
                self.call_sphere_plotter()

        else:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_center_coordinates.setText("")
            self.hide_sphere()

    def get_center_coordinates(self):

        selection_id = self.lineEdit_selection_id.text()
        selection_index = self.comboBox_attribution_type.currentIndex()

        if selection_id == "" or selection_index == 0:
            self.lineEdit_center_coordinates.setText("")
            return list()

        index = self.comboBox_attribution_type.currentIndex()
        if index == 2:
            averaged_selection = False
        elif index == 3:
            averaged_selection = True

        center_coords = self.mesh.get_average_nodal_coordinates(selection_id, averaged=averaged_selection)
        if averaged_selection:
            try:
                str_center_coords = f"{center_coords[0][0]: .4f}, {center_coords[0][1]: .4f}, {center_coords[0][2]: .4f}"
                self.lineEdit_center_coordinates.setText(str_center_coords)
            except:
                self.lineEdit_center_coordinates.setText("")
                return list()

        else:
            if len(center_coords) == 1:
                try:
                    str_center_coords = f"{center_coords[0][0]: .4f}, {center_coords[0][1]: .4f}, {center_coords[0][2]: .4f}"
                    self.lineEdit_center_coordinates.setText(str_center_coords)
                except:
                    self.lineEdit_center_coordinates.setText("")
                    return list()
            else:
                self.lineEdit_center_coordinates.setText("Multiple centers")

        return center_coords

    def call_sphere_plotter(self):

        if self.comboBox_attribution_type.currentIndex() >= 2:

            self.selection_radius = self.doubleSpinBox_selection_radius.value()
            center_coords = self.get_center_coordinates()

            if len(center_coords):
                all_radius = [self.selection_radius for _ in center_coords]
                geometry_widget = self.main_window.geometry_widget
                geometry_widget.set_selection_spheres(center_coords, all_radius)

                mesh_widget = self.main_window.mesh_widget
                mesh_widget.set_selection_spheres(center_coords, all_radius)

    def hide_sphere(self):
        geometry_widget = self.main_window.geometry_widget
        geometry_widget.clear_selection_spheres()
        mesh_widget = self.main_window.mesh_widget
        mesh_widget.clear_selection_spheres()

    def get_selection_information(self):

        selection_id = self.lineEdit_selection_id.text()

        if selection_id != "":

            index = self.comboBox_attribution_type.currentIndex()
            if index >= 2:

                selection_radius = self.doubleSpinBox_selection_radius.value()
                
                if index == 2:
                    averaged_selection = False
                elif index == 3:
                    averaged_selection = True

                if self.generate_mesh():
                    return
                
                self.hide()
                filter_type = self.comboBox_filter_type.currentIndex()

                GetSphereSelectionInformation(  selection_id,
                                                selection_radius,
                                                averaged_selection,
                                                filter_type  )

                self.main_window.set_input_widget(self)
                self.main_window.action_model_workspace_callback()

    def generate_mesh(self):
        if not app().project.model.generated_mesh:
            self.mesher = MeshSetupInputs(close_after_generate=True)
            if not self.mesher.complete:
                self.mesher = None
                return True

    def get_rectangular_duct_inputs(self):

        section_type = self.comboBox_section_type.currentIndex()

        if section_type in [0, 1]:
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

        if section_type in [0, 1]:
            model_data = {
                          "formulation" : "Stinson model",
                          "section_type" : section_types[section_type],
                          "width" : width,
                          "height" : height,
                          "number_of_terms" : self.spinBox_number_of_terms.value()
                          }

        else:
            model_data = {
                          "formulation" : "Stinson model",
                          "section_type" : section_types[section_type],
                          "height" : height
                          }

        return model_data

    def get_circular_duct_inputs(self):

        lineEdit = self.lineEdit_diameter_circular
        diameter, stop = self.check_inputs(lineEdit, "Diameter (circular duct)")
        if stop:
            lineEdit.setFocus()
            return dict()
        
        if self.comboBox_formulation.currentIndex() == 0:
            formulation = "Stinson model"
        else:
            formulation = "LRF model"
        
        viscous_thermal_model_data = {
                                    "formulation" : formulation,
                                    "section_type" : "Circular duct",
                                    "diameter" : diameter
                                    }

        return viscous_thermal_model_data

    def attribute_callback(self):

        if self.tabWidget_main.currentIndex() == 0:
            model_data = self.get_rectangular_duct_inputs()
        elif self.tabWidget_main.currentIndex() == 1:
            model_data = self.get_circular_duct_inputs()
        else:
            return

        if model_data:

            attribute_type = self.comboBox_attribution_type.currentIndex()
            if attribute_type in [0, 1]:
                
                volume_ids = list()
                if attribute_type == 0:
                    if "volumes" in self.mesh.geometry_information.keys():
                        volume_ids = self.mesh.geometry_information["volumes"]

                elif attribute_type == 1:
                    input_ids = self.lineEdit_selection_id.text()
                    volume_ids = self.mesh.check_selected_ids(
                                                              input_ids, 
                                                              selection = "volumes", 
                                                              single_id = False
                                                              )

                    if volume_ids is None:
                        self.lineEdit_selection_id.setFocus()
                        return True

                for volume_id in volume_ids:
                    self.properties._set_property("viscous_thermal_model", model_data, volume=volume_id)

                print(f"The viscous_thermal {model_data['formulation']} model for '{model_data['section_type']}' has been attributed to the volumes {volume_ids}.")

            elif attribute_type in [2, 3]:

                if attribute_type == 2:
                    averaged_selection = False
                else:
                    averaged_selection = True

                group_id = self.get_lrf_group_index()
                filter_type = self.comboBox_filter_type.currentIndex()

                surface_ids = self.main_window.selected_geometry_surfaces
                self.selection_radius = self.doubleSpinBox_selection_radius.value()

                model_data["surface_ids"] = list(surface_ids)
                model_data["selection_radius"] = self.selection_radius
                model_data["averaged"] = averaged_selection
                model_data["filter_type"] = filter_type

                self.properties._set_property("viscous_thermal_model", model_data, group=group_id)

                print(f"The viscous_thermal {model_data['formulation']} model for '{model_data['section_type']}' has been attributed to the group {group_id}.")

            app().file.write_model_properties_in_file()
            self.load_info()

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
                message = f"You have typed and invalid value at the {label} input field.\n\n"
                message += str(_err)

        else:
            message = f"Insert some value at the {label} input field."

        if message != "":
            PrintMessageInput([window_title_1, title, message])
            return None, True
        else:
            return out, False

    def get_lrf_group_index(self):

        keys = list()
        for key in self.properties.group_properties.keys():
            property, group_id = key
            if property == "viscous_thermal_model":
                if group_id not in keys:
                    keys.append(group_id)

        index = 1
        while index in keys:
            index += 1

        return index

    def get_lrf_info(self):

        selected_id = self.lineEdit_selection_id.text()

        if selected_id != "":

            selected_id = int(selected_id)

            self.hide()
            def get_info(data):
                GetSphereSelectionInformation(  data["surface_ids"],
                                                data["selection_radius"],
                                                data["averaged"],
                                                data["filter_type"]  )

                self.main_window.set_input_widget(self)
                self.main_window.action_model_workspace_callback()

            group_properties = self.properties.group_properties.copy()
            for key, data in group_properties.items():
                property, group_id = key
                if property == "viscous_thermal_model" and int(selected_id) == group_id:
                    return get_info(data)

            # volume_properties = self.properties.volume_properties.copy()
            # for key, data in volume_properties.items():
            #     property, volume_id = key
            #     if property == "viscous_thermal_model" and int(picked_id) == volume_id:
            #         return get_info()

    def hide_sphere(self):
        geometry_widget = self.main_window.geometry_widget
        geometry_widget.clear_selection_spheres()
        mesh_widget = self.main_window.mesh_widget
        mesh_widget.clear_selection_spheres()

    # Plot viscous_thermal effective properties

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

    def get_effective_properties(self, fluid: Fluid):

        warnings.filterwarnings('ignore')

        frequencies = None
        analysis_setup = app().project.analysis_setup
        if isinstance(analysis_setup, dict):
            frequencies = analysis_setup.get("frequencies", None)

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

        model = ViscousThermalLossModels(self)

        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == 0:
            tv_data = self.get_rectangular_duct_inputs()

        elif tab_index == 1:
            tv_data = self.get_circular_duct_inputs()

        if tv_data:
            if tab_index == 0:
                if self.comboBox_section_type.currentIndex() in [0, 1]:
                    rho_eff, C_eff = model.get_rectangular_section_effective_properties(omega, fluid, tv_data)

                else:
                    rho_eff, C_eff = model.get_narrow_slit_section_effective_properties(omega, fluid, tv_data)

            elif tab_index == 1:
                if self.comboBox_formulation.currentIndex() == 0:
                    rho_eff, C_eff = model.get_circular_section_effective_properties_for_Stinson_model(omega, fluid, tv_data)
                else:
                    rho_eff, C_eff = model.get_circular_section_effective_properties_for_LRF_model(omega, fluid, tv_data)

            k_cr = omega / C_eff

            return freq, rho_eff, C_eff, k_cr

        return None, None, None, None

    def get_viscous_thermal_loss_model(self):
        tab_index = self.tabWidget_main.currentIndex()
        
        if tab_index == 0:
            section_index = self.comboBox_section_type.currentIndex()
            if section_index == 0:
                return "Rectangular duct"
            elif section_index == 1:
                return "Quadrangular duct"
            else:
                return "Narrow slit duct"

        elif tab_index == 1:
            return "Circular duct"

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
        alpha_n = 1 - np.abs(R_r)**2

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
        self.hide_sphere()
        try:
            warnings.filterwarnings('default')
            app().main_window.selection_changed.disconnect(self.geometry_selection_callback)
        except TypeError:
            pass  # ignore if there is nothing to disconect
        self.keep_window_open = False
        return super().closeEvent(a0)
    
# fmt: on