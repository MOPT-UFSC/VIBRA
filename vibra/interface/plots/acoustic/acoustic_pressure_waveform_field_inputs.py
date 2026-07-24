from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QGridLayout

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.plots.general.animation_widget import AnimationWidget
from vibra.interface.ui_generated.plots.acoustic.acoustic_pressure_waveform_field_inputs_ui import AcousticPressureWaveformFieldInputs_UI
from vibra.interface.viewer_3d.coloring.color_palettes import COLORMAP_NAMES
from vibra.interface.viewer_3d.plot_setup import PressurePlotType, TransientPressurePlotSetup


class ReduceLoopType(IntEnum):
    DISABLED = 0
    USER_DEFINED = 1
    ROTATIONAL_SPEED = 2


class AcousticPressureWaveformFieldInputs(AcousticPressureWaveformFieldInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self._reset_variables()
        self._create_connections()
        self.add_animation_widget()
        self._configure_validators()

        self.load_user_preference_colormap()
        self._load_analysis_setup_and_solution()

    @property
    def model(self):
        return app().project.model

    @property
    def mesh(self):
        return app().project.model.mesh

    @property
    def properties(self):
        return app().project.model.properties

    @property
    def nodal_solution(self):
        return app().project.model.solution.nodal_solution

    def showEvent(self, event):
        super().showEvent(event)

        render_widget = app().main_window.results_widget
        app().main_window.render_widgets_stack.setCurrentWidget(render_widget)
        app().main_window.render_widget_changed.emit()
        app().main_window.view_toolbar.disable_selection_tool()

    def _configure_validators(self):
        self.lineEdit_animation_time.setValidator(StrictDoubleValidator(1e-5, 1e8, 8))

    def _load_analysis_setup_and_solution(self):
        self.analysis_method = ""
        if self.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.analysis_method = "Direct method"

        self.frequencies = self.model.frequencies

        self.update_slider_configuration()

    def _reset_variables(self):
        self.unit_label = "Pa"
        self.time_vector = None
        self.plot_setup = None

    def _create_connections(self):
        #
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)
        self.comboBox_plot_type.currentIndexChanged.connect(self.plot_data_callback)
        self.comboBox_reduced_time.currentIndexChanged.connect(lambda: self.reduced_loop_time_type_callback(True))
        #
        self.lineEdit_animation_time.editingFinished.connect(self.plot_data_callback)
        #
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)
        #
        self.reduced_loop_time_type_callback()

    def add_animation_widget(self):

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_animation.setLayout(self.grid_layout)

        self.animation_widget = AnimationWidget()
        self.grid_layout.addWidget(self.animation_widget)
        self.frame_animation.adjustSize()

        self.animation_widget.label_animation_phase.setText("Time step:")
        self.animation_widget.label_phase_angle.setText(f"{0: .4e}s")

    def update_slider_configuration(self):
        if isinstance(self.frequencies, np.ndarray):
            N_steps = 2 * len(self.frequencies)
            df = self.frequencies[1] - self.frequencies[0]
            T = 1 / df

        self.animation_widget.configure_animation_widget_for_transient_plot(T, N_steps)

    def load_user_preference_colormap(self):
        try:
            colormap = app().config.user_preferences.color_map
            if colormap in COLORMAP_NAMES:
                index = COLORMAP_NAMES.index(colormap)
                self.comboBox_colormaps.setCurrentIndex(index)
        except Exception:
            self.comboBox_colormaps.setCurrentIndex(0)

    def update_colormap_type(self):
        app().config.user_preferences.color_map = self.get_colormap()
        app().config.update_config_file()
        try:
            self.animation_widget.update_color_and_deformation()
        except AttributeError:
            pass

    def update_transparency_callback(self):
        return
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

    def reduced_loop_time_type_callback(self, update_plot: bool = False):
        index = self.comboBox_reduced_time.currentIndex()
        is_disabled = index == ReduceLoopType.DISABLED

        self.label_animation_time.setDisabled(is_disabled)
        self.label_animation_time_unit.setDisabled(is_disabled)
        self.lineEdit_animation_time.setDisabled(is_disabled)

        if index == ReduceLoopType.ROTATIONAL_SPEED:
            self.label_animation_time.setText("Rotational speed:")
            self.label_animation_time_unit.setText("[rpm]")
        else:
            self.label_animation_time.setText("Animation time:")
            self.label_animation_time_unit.setText("[s]")

        tool_tip = "" if is_disabled else "Press enter to confirm the time filter"
        self.lineEdit_animation_time.setToolTip(tool_tip)

        if is_disabled and self.lineEdit_animation_time.text() != "":
            self.lineEdit_animation_time.clear()

        if update_plot:
            self.plot_data_callback()

    def get_reduced_loop_time(self) -> float | None:
        value_str = self.lineEdit_animation_time.text()
        if value_str == "":
            return None

        index = self.comboBox_reduced_time.currentIndex()
        match index:
            case ReduceLoopType.DISABLED:
                return None

            case ReduceLoopType.USER_DEFINED:
                return float(value_str)

            case ReduceLoopType.ROTATIONAL_SPEED:
                return 60 / float(value_str)

            case _:
                return None

    def plot_data_callback(self):

        plot_setup = TransientPressurePlotSetup(
            time_index=0,
            plot_type=self.get_plot_type(),
            unit="Pa",
            reduced_loop_time=self.get_reduced_loop_time(),
        )

        if plot_setup == self.plot_setup:
            return

        self.plot_setup = plot_setup

        def plot_callback():
            self.animation_widget.reset_sliders(plot_setup=plot_setup)
            app().main_window.results_widget.update_plot(plot_setup=self.plot_setup)

        LoadingWindow(plot_callback).run()

    def get_plot_type(self) -> PressurePlotType:
        plot_types = [
            "non_absolute_animation",
            "absolute_animation",
        ]
        index = self.comboBox_plot_type.currentIndex()
        return PressurePlotType(plot_types[index])

    def get_colormap(self) -> str:
        index = self.comboBox_colormaps.currentIndex()
        if not (0 <= index < len(COLORMAP_NAMES)):
            return "jet"
        return COLORMAP_NAMES[index]

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        return super().closeEvent(a0)
