from PyQt5.QtWidgets import QComboBox, QDialog, QDoubleSpinBox, QFrame, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.engine.properties.fluid import Fluid
from vibra.engine.dissipation_models.thermoviscous_loss_models import ThermoviscousLossModels
from vibra.interface.mesh.mesher_inputs import MesherInputs
from vibra.interface.model_inputs.acoustic.fluid.set_fluid_input_simplified import SetFluidInputSimplified
from vibra.interface.model_inputs.acoustic.get_sphere_selection_information import GetSphereSelectionInformation
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance

import numpy as np

# fmt: off

window_title_1 = "Error"
window_title_2 = "Warning"

class SetThermoviscousLossModel(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/set_thermoviscous_model_inputs.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()

        self.project = app().main_window.project
        self.model = app().main_window.project.model
        self.mesh = app().main_window.project.model.mesh
        self.properties = app().main_window.project.model.properties

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()

        ConfigWidgetAppearance(self, tool_tip=True)

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

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type: QComboBox
        self.comboBox_section_type: QComboBox
        self.comboBox_formulation: QComboBox
        self.comboBox_filter_type: QComboBox

        # QDoubleSpin
        self.doubleSpinBox_selection_radius: QDoubleSpinBox

        # QFrame
        self.frame_fluid_info: QFrame
        self.frame_plot_buttons: QFrame

        # QLineEdit
        self.lineEdit_selection_id: QLineEdit
        self.lineEdit_selected_fluid: QLineEdit
        self.lineEdit_fluid_density: QLineEdit
        self.lineEdit_speed_of_sound: QLineEdit
        self.lineEdit_width_rectangular: QLineEdit
        self.lineEdit_height_rectangular: QLineEdit
        self.lineEdit_area_rectangular: QLineEdit
        self.lineEdit_diameter_circular: QLineEdit
        self.lineEdit_radius_circular: QLineEdit
        self.lineEdit_area_circular: QLineEdit
        self.lineEdit_center_coordinates: QLineEdit
        self.lineEdit_center_coordinates.setDisabled(True)

        # QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_confirm: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton
        self.pushButton_selection_info: QPushButton
        self.pushButton_get_fluid: QPushButton
        self.pushButton_plot_complex_fluid_density: QPushButton
        self.pushButton_plot_complex_speed_of_sound: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_thermoviscous_model: QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_section_type.currentIndexChanged.connect(self.rectangular_section_type_callback)
        #
        self.doubleSpinBox_selection_radius.valueChanged.connect(self.call_sphere_plotter)
        #
        self.lineEdit_width_rectangular.textChanged.connect(self.update_rectangular_duct_area)
        self.lineEdit_height_rectangular.textChanged.connect(self.update_rectangular_duct_area)
        self.lineEdit_diameter_circular.textChanged.connect(self.update_circular_duct_area)
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.attribute_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        self.pushButton_selection_info.clicked.connect(self.get_selection_information)
        self.pushButton_plot_complex_fluid_density.clicked.connect(self.plot_complex_fluid_density)
        self.pushButton_plot_complex_speed_of_sound.clicked.connect(self.plot_complex_speed_of_sound)
        #
        self.tabWidget_main.currentChanged.connect(self.tabEvent_callback)
        #
        self.treeWidget_thermoviscous_model.itemClicked.connect(self.on_click_item)
        self.treeWidget_thermoviscous_model.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.geometry_selection_callback()
        self.attribution_type_callback()
        self.update_plot_buttons_access()

    def update_plot_buttons_access(self):
        state = self.selected_fluid is None
        self.pushButton_plot_complex_fluid_density.setDisabled(state)
        self.pushButton_plot_complex_speed_of_sound.setDisabled(state)

    def _config_widgets(self):
        for i, w in enumerate([90, 60, 140, 140, 120]):
            self.treeWidget_thermoviscous_model.setColumnWidth(i, w)
            self.treeWidget_thermoviscous_model.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def update_rectangular_duct_area(self):
        try:
            height = float(self.lineEdit_height_rectangular.text())
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
                self.properties._remove_volume_property("thermoviscous_model", selection_id)
            else:
                self.properties._remove_group_property("thermoviscous_model", selection_id)

            app().main_window.file.write_model_properties_in_file()
            self.pushButton_remove.setDisabled(True)
            self.load_info()

    def reset_callback(self):

        volume_ids = list()
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "thermoviscous_model":
                volume_ids.append(volume_id)

        group_ids = list()
        for key, data in self.properties.group_properties.items():
            property, group_id = key
            if property == "thermoviscous_model":
                group_ids.append(group_id)

        if volume_ids or group_ids:

            self.hide()

            title = "Thermoviscous dissipation model resetting"
            message = "Would you like to remove the thermoviscous dissipation effects from the model?"

            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:

                for volume_id in volume_ids:
                    self.properties._remove_volume_property("thermoviscous_model", volume_id)

                for group_id in group_ids:
                    self.properties._remove_group_property("thermoviscous_model", group_id)

                app().main_window.file.write_model_properties_in_file()
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
        condition = self.comboBox_section_type.currentIndex() in [0, 1]
        if condition:
            self.lineEdit_width_rectangular.setDisabled(False)
            if self.lineEdit_width_rectangular.text() == "2*a >> 2*b":
                self.lineEdit_width_rectangular.text("")
        else:
            self.lineEdit_width_rectangular.setText("2*a >> 2*b")
            self.lineEdit_width_rectangular.setDisabled(True)

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

        self.treeWidget_thermoviscous_model.clear()

        for key, data in self.properties.volume_properties.items():

            property, volume_id = key
            if property == "thermoviscous_model":

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

                self.treeWidget_thermoviscous_model.addTopLevelItem(new)

        for key, data in self.properties.group_properties.items():

            property, group_id = key
            if property == "thermoviscous_model":
                
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

                self.treeWidget_thermoviscous_model.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        for key, _ in self.properties.volume_properties.items():
            property, _ = key
            if property == "thermoviscous_model":
                self.tabWidget_main.setTabVisible(2, True)
                return

        for key, _ in self.properties.group_properties.items():
            property, _ = key
            if property == "thermoviscous_model":
                self.tabWidget_main.setTabVisible(2, True)
                return

        self.tabWidget_main.setTabVisible(2, False)
        self.tabWidget_main.setCurrentIndex(0)

    def highlight_mesh_elements(self, elements):
        mesh_widget = self.main_window.viewer_tabs.mesh_widget
        mesh_widget.select_multiple_volumes(elements)

    def geometry_selection_callback(self):

        faces = self.main_window.selected_geometry_surfaces
        volumes = self.main_window.selected_geometry_volumes

        if volumes:
            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selection_id.setText(text)
            if self.comboBox_attribution_type.currentIndex() == 0:
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
                _round_center_coords = [round(value, 4) for value in center_coords[0]]
                self.lineEdit_center_coordinates.setText(str(_round_center_coords))
            except:
                self.lineEdit_center_coordinates.setText("")
                return list()

        else:
            if len(center_coords) == 1:
                try:
                    _round_center_coords = [round(value, 4) for value in center_coords[0]]
                    self.lineEdit_center_coordinates.setText(str(_round_center_coords))
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
                geometry_widget = self.main_window.viewer_tabs.geometry_widget
                geometry_widget.set_selection_spheres(center_coords, all_radius)

                mesh_widget = self.main_window.viewer_tabs.mesh_widget
                mesh_widget.set_selection_spheres(center_coords, all_radius)

    def hide_sphere(self):
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.clear_selection_spheres()
        mesh_widget = self.main_window.viewer_tabs.mesh_widget
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
                self.main_window.viewer_tabs.show_geometry()

    def generate_mesh(self):
        if not self.main_window.project.model.generated_mesh:
            self.mesher = MesherInputs(close_after_generate=True)
            if not self.mesher.complete:
                self.mesher = None
                return True

    def check_selected_bodies(self):
        lineEdit = self.lineEdit_selection_id.text()
        self.stop, self.volume_ids = self.mesh.check_input_volume_id(lineEdit)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
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
                          "height" : height
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
        
        thermoviscous_model_data = {
                                    "formulation" : formulation,
                                    "section_type" : "Circular duct",
                                    "diameter" : diameter
                                    }

        return thermoviscous_model_data

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

                if attribute_type == 0:
                    volume_ids = list(self.mesh.nodes_from_volumes.keys())
    
                elif attribute_type == 1:
                    if self.check_selected_bodies():
                        return
                    volume_ids = self.volume_ids

                for volume_id in volume_ids:
                    # surfaces_from_volume = self.mesh.surfaces_from_volumes[volume_id]
                    self.project.set_thermoviscous_model(model_data, volume=volume_id)

                print(f"The thermoviscous {model_data['formulation']} model for '{model_data['section_type']}' has been attributed to the volumes {volume_ids}.")

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

                self.project.set_thermoviscous_model(model_data, group=group_id)

                print(f"The thermoviscous {model_data['formulation']} model for '{model_data['section_type']}' has been attributed to the group {group_id}.")

            app().main_window.file.write_model_properties_in_file()
            self.load_info()
            # self.close()

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
            if property == "thermoviscous_model":
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
                self.main_window.viewer_tabs.show_geometry()

            group_properties = self.properties.group_properties.copy()
            for key, data in group_properties.items():
                property, group_id = key
                if property == "thermoviscous_model" and int(selected_id) == group_id:
                    return get_info(data)

            # volume_properties = self.properties.volume_properties.copy()
            # for key, data in volume_properties.items():
            #     property, volume_id = key
            #     if property == "thermoviscous_model" and int(picked_id) == volume_id:
            #         return get_info()

    def hide_sphere(self):
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.clear_selection_spheres()
        mesh_widget = self.main_window.viewer_tabs.mesh_widget
        mesh_widget.clear_selection_spheres()

    # Plot thermoviscous effective properties

    def get_fluid_callback(self):
        self.hide()
        self.fluid_dialog = SetFluidInputSimplified()
        self.fluid_dialog.fluid_widget.pushButton_attribute_fluid.setText("Select fluid")
        self.fluid_dialog.pushButton_attribute_fluid.clicked.connect(self.get_selected_fluid)
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

    def get_effective_properties(self, fluid):

        analysis_data = app().main_window.project.analysis_data
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

        model = ThermoviscousLossModels(self)
        # model.process_effective_properties(frequencies)

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

            return freq, rho_eff, C_eff

        return None, None, None

    def get_thermoviscous_loss_model(self):
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

    def plot_complex_fluid_density(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        freq, rho_eff, _ = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        tv_model = self.get_thermoviscous_loss_model()
        self.call_plotter(freq, rho_eff, "complex fluid density", tv_model)

    def plot_complex_speed_of_sound(self):

        if self.selected_fluid is None:
            self.get_fluid_callback()

        freq, _, C_eff = self.get_effective_properties(self.selected_fluid)

        if freq is None:
            return

        tv_model = self.get_thermoviscous_loss_model()
        self.call_plotter(freq, C_eff, "complex speed of sound", tv_model)

    def join_model_data(self, x_data, y_data, label: str, section_label: str):

        self.hide()
        self.data_to_plot = dict()
      
        if label == "complex fluid density":
            unit_label = "m/s"
            y_label = "Complex fluid density"
        else:
            unit_label = "m/s"
            y_label = "Complex speed of sound"

        legend_label = label
        title = f"Effective Fluid Properties for {section_label}"

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

    def call_plotter(self, x_data, y_data, label, pm_label):
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
            geometry_widget = self.main_window.viewer_tabs.geometry_widget
            geometry_widget.selection_changed.disconnect(self.geometry_selection_callback)
        except TypeError:
            pass  # ignore if there is nothing to disconect
        self.keep_window_open = False
        return super().closeEvent(a0)
    
# fmt: on