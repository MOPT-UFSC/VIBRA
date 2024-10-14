from PyQt5.QtWidgets import QComboBox, QDialog, QFrame, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.interface.model_inputs.acoustic.fluid.fluid_widget import FluidWidget
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput

from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter

from vibra.engine.properties.fluid import Fluid
from vibra.engine.dissipation_models.thermoviscous_loss_models import ThermoviscousLossModels

from pathlib import Path
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
        self.geometry_selection_callback()

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

        # QFrame
        self.frame_fluid_info: QFrame
        self.frame_plot_buttons: QFrame

        # QLineEdit
        self.lineEdit_selected_id: QLineEdit
        self.lineEdit_selected_fluid: QLineEdit
        self.lineEdit_fluid_density: QLineEdit
        self.lineEdit_speed_of_sound: QLineEdit
        self.lineEdit_width_rectangular: QLineEdit
        self.lineEdit_height_rectangular: QLineEdit
        self.lineEdit_area_rectangular: QLineEdit
        self.lineEdit_diameter_circular: QLineEdit
        self.lineEdit_radius_circular: QLineEdit
        self.lineEdit_area_circular: QLineEdit

        # QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_confirm: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton
        self.pushButton_get_fluid: QPushButton
        self.pushButton_plot_complex_fluid_density: QPushButton
        self.pushButton_plot_complex_speed_of_sound: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_thermoviscous_model: QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.update_attribution_type)
        self.comboBox_section_type.currentIndexChanged.connect(self.rectangular_section_type_callback)
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
        self.update_attribution_type()
        self.update_plot_buttons_access()

    def update_plot_buttons_access(self):
        state = self.selected_fluid is None
        self.pushButton_plot_complex_fluid_density.setDisabled(state)
        self.pushButton_plot_complex_speed_of_sound.setDisabled(state)

    def _config_widgets(self):
        for i, w in enumerate([80, 160, 140]):
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
        if self.lineEdit_selected_id.text() != "":
            volume_id = int(self.lineEdit_selected_id.text())
            self.properties._remove_volume_property("thermoviscous_model", volume_id)
            app().main_window.file.write_model_properties_in_file()
            self.load_info()

    def reset_callback(self):

        volume_ids = list()
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "thermoviscous_model":
                volume_ids.append(volume_id)

        if volume_ids:

            self.hide()

            title = "Porous material model resetting"
            message = "Would you like to remove the porous material effects from the model?"

            buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:

                for volume_id in volume_ids:
                    self.properties._remove_volume_property("thermoviscous_model", volume_id)

                app().main_window.file.write_model_properties_in_file()
                self.close()

    def tabEvent_callback(self):

        tab_index = self.tabWidget_main.currentIndex()

        if tab_index == 2:
            self.comboBox_attribution_type.setCurrentIndex(1)
            self.comboBox_attribution_type.setDisabled(True)
            self.lineEdit_selected_id.setText("")
            self.lineEdit_selected_id.setDisabled(True)
            self.frame_fluid_info.setDisabled(True)
            self.frame_plot_buttons.setDisabled(True)

        else:

            self.frame_fluid_info.setDisabled(False)
            self.frame_plot_buttons.setDisabled(False)

            self.comboBox_attribution_type.setDisabled(False)
            if self.comboBox_attribution_type.currentIndex() == 0:
                return

            self.lineEdit_selected_id.setDisabled(False)

    def on_click_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def rectangular_section_type_callback(self):
        condition = self.comboBox_section_type.currentIndex() in [0, 1]
        if condition:
            self.lineEdit_width_rectangular.setDisabled(False)
            if self.lineEdit_width_rectangular.text() == "2*a >> 2*b":
                self.lineEdit_width_rectangular.text("")
        else:
            self.lineEdit_width_rectangular.setText("2*a >> 2*b")
            self.lineEdit_width_rectangular.setDisabled(True)

    def update_attribution_type(self):
        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selected_id.setText("All bodies")
            self.lineEdit_selected_id.setEnabled(False)
        elif index == 1:
            self.lineEdit_selected_id.setText("")
            self.lineEdit_selected_id.setEnabled(True)
        # self.comboBox_attribution_type.setCurrentIndex(index)

    def update_tabs_visibility(self):
        self.tabWidget_main.setTabVisible(2, False)
        for key, data in self.properties.volume_properties.items():
            property, volume_id = key
            if property == "thermoviscous_model":
                self.tabWidget_main.setTabVisible(2, True)
                return

    def load_info(self):

        self.treeWidget_thermoviscous_model.clear()

        for key, data in self.properties.volume_properties.items():

            property, volume_id = key

            if property == "thermoviscous_model":

                model_inputs = list()
                for key, value in data.items():
                    if key == "section_type":
                        section_type = data["section_type"]
                    else:
                        model_inputs.append(value)

                new = QTreeWidgetItem([str(volume_id), section_type, str(model_inputs)])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_thermoviscous_model.addTopLevelItem(new)

        self.update_tabs_visibility()

    def geometry_selection_callback(self):

        volumes = self.main_window.selected_geometry_volumes

        if volumes:

            if self.comboBox_attribution_type.currentIndex() == 0:
                self.comboBox_attribution_type.setCurrentIndex(1)
                # return

            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selected_id.setText(text)

    def check_selected_bodies(self):
        lineEdit = self.lineEdit_selected_id.text()
        self.stop, self.volume_ids = self.mesh.check_input_volume_id(lineEdit)
        if self.stop:
            self.lineEdit_selected_id.setFocus()
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

        index = self.tabWidget_main.currentIndex()
        if index == 0:
            model_data = self.get_rectangular_duct_inputs()
        elif index == 1:
            model_data = self.get_circular_duct_inputs()
        else:
            return

        if model_data:

            if self.comboBox_attribution_type.currentIndex():
                if self.check_selected_bodies():
                    return
                volume_ids = self.volume_ids

            else:
                volume_ids = list(self.mesh.nodes_from_volumes.keys())

            for volume_id in volume_ids:
                # surfaces_from_volume = self.mesh.surfaces_from_volumes[volume_id]
                self.project.set_thermoviscous_model(model_data, volume=volume_id)

            print(f"The thermoviscous Stinson model for '{model_data['section_type']}' has been attributed to the volumes {volume_ids}.")

            app().main_window.file.write_model_properties_in_file()
            self.close()

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

    def get_fluid_callback(self):
        self.hide()
        self.fluid_widget = FluidWidget()
        self.fluid_widget._add_icon_and_title()
        self.fluid_widget.show()
        self.fluid_widget.pushButton_attribute_fluid.clicked.connect(self.get_selected_fluid)

    def get_selected_fluid(self):
        self.selected_fluid = self.fluid_widget.get_selected_fluid()
        if isinstance(self.selected_fluid, Fluid):
            self.update_plot_buttons_access()
            self.fluid_widget.close()
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
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)
    
# fmt: on