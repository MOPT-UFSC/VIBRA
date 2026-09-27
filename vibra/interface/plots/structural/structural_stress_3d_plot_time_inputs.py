from enum import IntEnum
from time import perf_counter

import numpy as np
from PySide6.QtCore import QSignalBlocker, Qt, Signal
from PySide6.QtWidgets import QGridLayout

from vibra import app
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.numeric_checks.unit_utilities import convert_stress_unit
from vibra.interface.plots.general.animation_widget import AnimationWidget
from vibra.interface.plots.general.results_display_widget import ResultsDisplayWidget
from vibra.interface.ui_generated.plots.structural.structural_stress_3d_plot_time_inputs_ui import StructuralStress3dPlotTimeInputs_UI
from vibra.interface.viewer_3d.plot_setup import StressDataType, StressFieldPlotSetupTime


class ReduceLoopType(IntEnum):
    DISABLED = 0
    USER_DEFINED = 1
    ROTATIONAL_SPEED = 2


class StructuralStress3dPlotTimeInputs(StructuralStress3dPlotTimeInputs_UI):

    value_changed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self._add_animation_widget()
        self._add_color_widget()
        self._initialize()
        self._configure_validators()
        self._create_connections()

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
    def structural_post(self):
        return app().project.get_structural_postprocessing()

    @property
    def is_nodal_solution_iffts_data_cached(self):
        cache_info = self.structural_post.compute_multiple_ifft_for_structural_nodal_solution.cache_info()
        return cache_info.currsize != 0

    @property
    def is_stress_data_cached(self):
        cache_info = self.structural_post.recover_nodal_averaged_structural_stresses.cache_info()
        return cache_info.currsize != 0

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

    def _initialize(self):
        self.time_vector = None
        self.plot_setup = None

        # update the widgets accessibility
        if self.is_stress_data_cached:
            self.plot_data_callback()
        else:
            self.set_frames_disabled(True)
            self.show_results_render()

    def _configure_validators(self):
        self.lineEdit_animation_time.setValidator(StrictDoubleValidator(1e-5, 1e8, 8))

    def set_frames_disabled(self, disabled: bool):
        self.frame_animation.setDisabled(disabled)
        self.frame_color.setDisabled(disabled)
        self.frame_plot_controls.setDisabled(disabled)
        self.pushButton_process_nodal_stresses.setEnabled(disabled)

    def show_results_render(self):
        self.pushButton_process_nodal_stresses.setDisabled(self.is_stress_data_cached)
        if not self.is_stress_data_cached:
            return

        curent_render_widget = app().main_window.get_current_render_widget()
        results_render_widget = app().main_window.results_widget

        if curent_render_widget != results_render_widget:
            app().main_window.render_widgets_stack.setCurrentWidget(results_render_widget)
            app().main_window.render_widget_changed.emit()
            app().main_window.view_toolbar.disable_selection_tool()

    def _create_connections(self):

        # QComboBox connections
        self.comboBox_plot_type.currentIndexChanged.connect(self.plot_data_callback)
        self.comboBox_plotting_results.currentIndexChanged.connect(self.plot_data_callback)
        self.comboBox_stress_units.currentIndexChanged.connect(self.plot_data_callback)

        # QPushButton connection
        self.pushButton_process_nodal_stresses.clicked.connect(self.plot_data_callback)

        self.results_display_widget.colormap_changed.connect(self.animation_widget.update_color_and_deformation)
        self.results_display_widget.min_max_value_changed.connect(self.animation_widget.update_color_and_deformation)

    def configure_results_display_widget(self):
        self.results_display_widget.configure_widget()

    def update_animation_widget_visibility(self):
        index = self.comboBox_plot_type.currentIndex()
        if index >= 2:
            self.animation_widget.setDisabled(True)
        else:
            self.animation_widget.setDisabled(False)

    # def process_stress_field(self):

    #     # recover the averaged structural stresses
    #     if not self.is_stress_data_cached:    
    #         def recover_stresses():
    #             t0 = perf_counter()
    #             self.structural_post.recover_nodal_averaged_structural_stresses()
    #             dt = perf_counter() - t0
    #             print(f"Time to compute all nodal stresses: {dt} s")

    #         LoadingWindow(recover_stresses).run()

    #     self.set_frames_disabled(False)
    #     self.load_frequencies()

    def plot_data_callback(self):

        stress_index = self.comboBox_plotting_results.currentIndex()
        plot_type = self.get_plot_type()

        if stress_index == 6 and plot_type == StressDataType.NON_ABSOLUTE_ANIMATION:
            with QSignalBlocker(self.comboBox_plot_type):
                self.comboBox_plot_type.setCurrentIndex(1)
                plot_type = self.get_plot_type()

        self.update_animation_widget_visibility()

        if self.get_plot_type() in [StressDataType.ABSOLUTE_ANIMATION, StressDataType.ABSOLUTE_VALUES]:
            self.results_display_widget.configure_validators(0, 1e14)
        else:
            self.results_display_widget.configure_validators(-1e14, 1e14)

        stress_units = self.comboBox_stress_units.currentText()
        unit_factor = convert_stress_unit(1, "Pa", stress_units)

        plot_setup = StressFieldPlotSetupTime(
            time_index=0,
            magnification_factor=self.animation_widget.magnification_factor,
            stress_type=stress_index,
            plot_type=plot_type,
            unit=stress_units,
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

    def get_plot_type(self) -> StressDataType:
        plot_types = [
            "non_absolute_animation",
            "absolute_animation",
        ]
        index = self.comboBox_plot_type.currentIndex()
        return StressDataType(plot_types[index])

    def update_slider_configuration(self):
        frequencies = self.model.frequencies
        if isinstance(frequencies, np.ndarray):
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()
