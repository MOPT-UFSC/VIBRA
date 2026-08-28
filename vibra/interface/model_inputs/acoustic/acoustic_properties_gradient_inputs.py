import numpy as np
from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLineEdit

from vibra import app
from vibra.engine.properties.fluid import Fluid
from vibra.interface.general.utils import clear_style_sheet

# from vibra.interface import error_title, warning_title
from vibra.interface.model_inputs.fluid.set_fluid_inputs_simplified import SetFluidInputsSimplified
from vibra.interface.ui_generated.model.acoustic.others.acoustic_properties_gradient_inputs_ui import AcousticPropertiesGradientInputs_UI


class AcousticPropertiesGradientInputs(AcousticPropertiesGradientInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        app().main_window.workspace_updating_for_model_setup()

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._config_window()
        self._config_widgets()

        self._initialize()
        self._create_connections()
        self.load_model_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _config_widgets(self):
        self.current_line_edit = None

    def _initialize(self):
        self.selected_fluid = None
        self.keep_window_open = True
        self.material_model_data = dict()

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_refinement_regions.currentIndexChanged.connect(self.refinement_regions_callback)
        #
        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_apply_and_close.clicked.connect(lambda: self.apply_callback(True))
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_viscous_thermal_model.itemClicked.connect(self.on_click_item)
        self.treeWidget_viscous_thermal_model.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.clickable(self.lineEdit_selection_id).connect(self.lineEdit_selection_id_clicked)
        self.clickable(self.lineEdit_start_coords).connect(self.lineEdit_start_coords_clicked)
        self.clickable(self.lineEdit_end_coords).connect(self.lineEdit_end_coords_clicked)
        #
        self.geometry_selection_callback()
        self.attribution_type_callback()

    def geometry_selection_callback(self):

        nodes = app().main_window.selection.mesh_nodes
        points = app().main_window.selection.geometry_points
        lines = app().main_window.selection.geometry_lines
        surfaces = app().main_window.selection.geometry_surfaces
        volumes = app().main_window.selection.geometry_volumes

        if self.current_line_edit == self.lineEdit_selection_id:
            if volumes:
                text = ", ".join([str(i) for i in volumes])
                self.lineEdit_selection_id.setText(text)
                if self.comboBox_attribution_type.currentIndex() != 1:
                    self.comboBox_attribution_type.setCurrentIndex(1)
            return
        
        if volumes:
            if len(volumes):
                volume_id = list(volumes)[0]
                nodes_from_volume = self.mesh.get_nodes_from_volume(volume_id)
                avg_coords = np.average(self.mesh.nodal_coordinates[nodes_from_volume, 1:], axis=0)
                round_coords = np.round(avg_coords, 4)

        elif surfaces:
            if len(surfaces) == 1:
                surface_id = list(surfaces)[0]
                nodes_from_surface = self.mesh.get_nodes_from_surface(surface_id)
                avg_coords = np.average(self.mesh.nodal_coordinates[nodes_from_surface, 1:], axis=0)
                round_coords = np.round(avg_coords, 4)

        elif lines:
            if len(lines) == 1:
                line_id = list(lines)[0]
                nodes_from_line = self.mesh.get_nodes_from_line(line_id)
                avg_coords = np.average(self.mesh.nodal_coordinates[nodes_from_line, 1:], axis=0)
                round_coords = np.round(avg_coords, 4)

        elif points:
            if len(points) == 1:
                point_id = list(points)[0]
                node_id = self.mesh.nodes_from_points.get(point_id)
                if node_id is None:
                    return
                round_coords = np.round(self.mesh.nodal_coordinates[node_id, 1:], 4)

        elif nodes:
            if len(nodes) == 1:
                node_id = list(nodes)[0]
                round_coords = np.round(self.mesh.nodal_coordinates[node_id, 1:], 4)

        else:
            return
        
        point_coords = f"({round_coords[0]}, {round_coords[1]}, {round_coords[2]})"
        self.current_line_edit.setText(point_coords)


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

    def lineEdit_selection_id_clicked(self):
        app().main_window.selection.set_geometry_selection()
        self.current_line_edit = self.lineEdit_selection_id
        self.highlight_line_edit()

    def lineEdit_start_coords_clicked(self):
        app().main_window.selection.set_geometry_selection()
        self.current_line_edit = self.lineEdit_start_coords
        self.highlight_line_edit()

    def lineEdit_end_coords_clicked(self):
        app().main_window.selection.set_geometry_selection()
        self.current_line_edit = self.lineEdit_end_coords
        self.highlight_line_edit()

    def highlight_line_edit(self):
        line_edits = [self.lineEdit_end_coords, self.lineEdit_selection_id, self.lineEdit_start_coords]
        clear_style_sheet([line_edit for line_edit in line_edits if line_edit is not self.current_line_edit])
        self.current_line_edit.setStyleSheet("border-color: rgb(255,0,0); border-width: 2px")

    def attribution_type_callback(self):

        attribution_type = self.comboBox_attribution_type.currentIndex()
        if attribution_type == 0:
            self.lineEdit_selection_id.setText("All bodies")
            self.lineEdit_selection_id.setEnabled(False)

        else:
            self.lineEdit_selection_id_clicked()
            volumes = app().main_window.selection.geometry_volumes
            if not volumes:
                self.lineEdit_selection_id.setText("")

            self.lineEdit_selection_id.setEnabled(True)

    def refinement_regions_callback(self):
        pass

    def get_fluid_callback(self):
        self.hide()
        self.fluid_dialog = SetFluidInputsSimplified()
        self.fluid_dialog.fluid_widget.pushButton_apply.setVisible(False)
        self.fluid_dialog.fluid_widget.pushButton_apply_and_close.clicked.connect(self.get_selected_fluid)
        self.fluid_dialog.exec()
        app().main_window.set_input_widget(self)

    def get_selected_fluid(self):
        self.selected_fluid = self.fluid_dialog.get_selected_fluid()
        if isinstance(self.selected_fluid, Fluid):
            self.fluid_dialog.close()
            self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
            self.lineEdit_fluid_density.setText(f"{self.selected_fluid.fluid_density}")
            self.lineEdit_speed_of_sound.setText(f"{self.selected_fluid.speed_of_sound}")


    def tab_event_callback(self):
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

    def apply_callback(self, close: bool = False):
        if close:
            self.close()

    def remove_callback(self):
        pass

    def reset_callback(self):
        pass

    def load_model_info(self):
        pass

    def on_click_item(self, item):

        key = f"{item.text(0)} - {item.text(1)}"
        if item.text(0) == "Volume":
            volume_id = int(item.text(1))
            app().main_window.selection.set_geometry_selection(volumes=[volume_id])

        self.lineEdit_selection_id.setText(key)
        self.pushButton_remove.setEnabled(True)

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection.selection_changed.disconnect(self.geometry_selection_callback)
        return super().closeEvent(a0)