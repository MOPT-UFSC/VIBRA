from PyQt5.QtWidgets import QComboBox, QDialog, QDoubleSpinBox, QFrame, QLineEdit, QPushButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.engine.properties.fluid import Fluid
from vibra.engine.dissipation_models.viscous_thermal_loss_models import ViscousThermalLossModels
from vibra.interface.mesh.mesher_inputs import MesherInputs
from vibra.interface.model_inputs.acoustic.fluid.set_fluid_input_simplified import SetFluidInputSimplified
from vibra.interface.model_inputs.acoustic.get_sphere_selection_information import GetSphereSelectionInformation
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.formatters.config_widget_appearance import ConfigWidgetAppearance

import warnings
import numpy as np

# fmt: off

window_title_1 = "Error"
window_title_2 = "Warning"

class SetAcousticPropertiesGradientInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/set_acoustic_properties_gradient_inputs.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)
        self.main_window.viewer_tabs.show_geometry()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        # self._config_widgets()

        ConfigWidgetAppearance(self, tool_tip=True)

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
        self.material_model_data = dict()

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type: QComboBox
        self.comboBox_fluid_point_selector: QComboBox
        self.comboBox_refinement_regions: QComboBox
        self.comboBox_beyond_bounds_values: QComboBox
        self.comboBox_interpolation_direction: QComboBox

        # QFrame
        self.frame_fluid_info: QFrame
        self.frame_plot_buttons: QFrame

        # QLineEdit
        self.lineEdit_selection_id: QLineEdit
        self.lineEdit_selected_fluid: QLineEdit
        self.lineEdit_fluid_density: QLineEdit
        self.lineEdit_speed_of_sound: QLineEdit
        self.lineEdit_start_coords: QLineEdit
        self.lineEdit_end_coords: QLineEdit
        self.lineEdit_start_temperature: QLineEdit
        self.lineEdit_end_temperature: QLineEdit
        self.lineEdit_start_pressure: QLineEdit
        self.lineEdit_end_pressure: QLineEdit

        # QPushButton
        self.pushButton_exit: QPushButton
        self.pushButton_confirm: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton
        self.pushButton_get_fluid: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_viscous_thermal_model: QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_refinement_regions.currentIndexChanged.connect(self.refinement_regions_callback)
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.attribute_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
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


    def attribution_type_callback(self):

        attribution_type = self.comboBox_attribution_type.currentIndex()
        if attribution_type == 0:
            self.lineEdit_selection_id.setText("All bodies")
            self.lineEdit_selection_id.setEnabled(False)

        else:
            volumes = self.main_window.selected_geometry_volumes
            if not volumes:
                self.lineEdit_selection_id.setText("")

            self.lineEdit_selection_id.setEnabled(True)


    def refinement_regions_callback(self):
        pass


    def geometry_selection_callback(self):

        volumes = self.main_window.selected_geometry_volumes

        if volumes:
            text = ", ".join([str(i) for i in volumes])
            self.lineEdit_selection_id.setText(text)
            if self.comboBox_attribution_type.currentIndex() != 1:
                self.comboBox_attribution_type.setCurrentIndex(1)


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
            self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
            self.lineEdit_fluid_density.setText(f"{self.selected_fluid.fluid_density}")
            self.lineEdit_speed_of_sound.setText(f"{self.selected_fluid.speed_of_sound}")


    def tabEvent_callback(self):

        return

        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 1:
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


    def attribute_callback(self):
        pass

    def remove_callback(self):
        pass

    def reset_callback(self):
        pass

    def on_click_item(self, item):

        key = f"{item.text(0)} - {item.text(1)}"
        if item.text(0) == "Volume":
            volume_id = int(item.text(1))
            app().main_window.set_geometry_selection(volumes=[volume_id])

        self.lineEdit_selection_id.setText(key)
        self.pushButton_remove.setEnabled(True)


    def on_doubleclick_item(self, item):
        self.on_click_item(item)


    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)