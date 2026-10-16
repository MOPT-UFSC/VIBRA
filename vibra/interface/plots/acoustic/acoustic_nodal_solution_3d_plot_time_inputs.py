from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QGridLayout

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.numeric_checks.unit_utilities import convert_pressure_unit
from vibra.interface.plots.general.animation_widget import AnimationWidget
from vibra.interface.plots.general.results_display_widget import ResultsDisplayWidget
from vibra.interface.ui_generated.plots.acoustic.acoustic_nodal_solution_3d_plot_time_inputs_ui import (
    AcousticNodalSolution3dPlotTimeInputs_UI,
)
from vibra.interface.viewer_3d.plot_setup import PressureFieldPlotSetupTime, PressurePlotType


class ReduceLoopType(IntEnum):
    DISABLED = 0
    USER_DEFINED = 1
    ROTATIONAL_SPEED = 2


class AcousticNodalSolution3dPlotTimeInputs(AcousticNodalSolution3dPlotTimeInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._add_animation_widget()
        self._add_color_widget()
        self._initialize()
        self._create_connections()
        self._configure_validators()

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
    def acoustic_post(self):
        return app().project.get_acoustic_postprocessing()

    @property
    def is_data_cached(self):
        cache_info = self.acoustic_post.compute_multiple_ifft_for_acoustic_nodal_solution.cache_info()
        return cache_info.currsize != 0

    def show_results_render(self):
        curent_render_widget = app().main_window.get_current_render_widget()
        results_render_widget = app().main_window.results_widget

        if curent_render_widget != results_render_widget:
            app().main_window.render_widgets_stack.setCurrentWidget(results_render_widget)
            app().main_window.render_widget_changed.emit()
            app().main_window.view_toolbar.disable_selection_tool()

    def _configure_validators(self):
        self.lineEdit_animation_time.setValidator(StrictDoubleValidator(1e-5, 1e8, 8))

    def _initialize(self):
        self.plot_setup = None

        # update the widgets accessibility
        if self.is_data_cached:
            self.plot_data_callback()
        else:
            self.set_frames_disabled(True)
            app().main_window.show_geometry_render_widget()

    def set_frames_disabled(self, disabled: bool):
        self.frame_animation.setDisabled(disabled)
        self.frame_color.setDisabled(disabled)
        self.frame_plot_controls.setDisabled(disabled)
        self.pushButton_process_nodal_solution_iffts.setEnabled(disabled)

    def _create_connections(self):

        # QComboBox connections
        self.comboBox_plot_type.currentIndexChanged.connect(self.plot_data_callback)
        self.comboBox_pressure_units.currentIndexChanged.connect(self.plot_data_callback)
        self.comboBox_reduced_time.currentIndexChanged.connect(lambda: self.reduced_loop_time_type_callback(True))

        # QLineEdit connections
        self.lineEdit_animation_time.editingFinished.connect(self.plot_data_callback)

        # QPushButton connections
        self.pushButton_process_nodal_solution_iffts.clicked.connect(self.plot_data_callback)

        self.results_display_widget.colormap_changed.connect(self.animation_widget.update_color_and_deformation)
        self.results_display_widget.min_max_value_changed.connect(self.animation_widget.update_color_and_deformation)

        self.reduced_loop_time_type_callback()

    def _add_animation_widget(self):

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_animation.setLayout(self.grid_layout)

        self.animation_widget = AnimationWidget()
        self.grid_layout.addWidget(self.animation_widget)
        self.frame_animation.adjustSize()

        self.animation_widget.label_animation_phase.setText("Time step:")
        self.animation_widget.label_phase_angle.setText(f"{0: .4e}s")

        self.update_slider_configuration()

    def _add_color_widget(self):
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_color.setLayout(grid_layout)

        self.results_display_widget = ResultsDisplayWidget()
        grid_layout.addWidget(self.results_display_widget)
        self.frame_color.adjustSize()

    def update_slider_configuration(self):
        frequencies = self.model.frequencies
        if not isinstance(frequencies, np.ndarray):
            return

        N_steps = 2 * len(frequencies)
        df = frequencies[1] - frequencies[0]
        T = 1 / df

        self.animation_widget.configure_animation_widget_for_transient_plot(T, N_steps)

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

        pressure_units = self.comboBox_pressure_units.currentText()
        unit_factor = convert_pressure_unit(1, "Pa", pressure_units)

        plot_setup = PressureFieldPlotSetupTime(
            time_index=0,
            plot_type=self.get_plot_type(),
            unit=pressure_units,
            unit_factor=unit_factor,
            reduced_loop_time=self.get_reduced_loop_time(),
        )

        if plot_setup == self.plot_setup:
            return

        self.plot_setup = plot_setup

        def plot_callback():
            self.animation_widget.reset_sliders(plot_setup=plot_setup)
            app().main_window.results_widget.update_plot(
                reset_camera=False,
                plot_setup=self.plot_setup,
            )

        LoadingWindow(plot_callback).run()

        self.set_frames_disabled(False)
        self.show_results_render()

    def get_plot_type(self) -> PressurePlotType:
        plot_types = [
            "non_absolute_animation",
            "absolute_animation",
        ]
        index = self.comboBox_plot_type.currentIndex()
        return PressurePlotType(plot_types[index])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        return super().closeEvent(a0)