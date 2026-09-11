from time import perf_counter

import numpy as np
from PySide6.QtCore import QSignalBlocker, Qt, Signal
from PySide6.QtWidgets import QGridLayout, QTreeWidgetItem

from vibra import app
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.numeric_checks.unit_utilities import convert_stress_unit
from vibra.interface.plots.general.animation_widget import AnimationWidget
from vibra.interface.plots.general.results_display_widget import ResultsDisplayWidget
from vibra.interface.ui_generated.plots.structural.structural_stresses_field_inputs_ui import StructuralStressesFieldInputs_UI
from vibra.interface.viewer_3d.plot_setup import StressFieldPlotSetupFrequency, StressPlotType


class StructuralStressesFieldsInputs(StructuralStressesFieldInputs_UI):

    value_changed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self._initialize()
        self._configure_widgets()
        self._add_animation_widget()
        self._add_color_widget()
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
    def is_stress_data_cached(self):
        cache_info = self.structural_post.recover_nodal_averaged_structural_stresses.cache_info()
        return cache_info.currsize != 0

    def _initialize(self):
        self.selected_frequency_index = None

    def _configure_widgets(self):

        self.lineEdit_selected_frequency.setDisabled(True)
        self.lineEdit_selected_frequency.setProperty("status", "information")

        for i, width in enumerate([80, 140]):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

        # update the widgets accessibility
        if self.is_stress_data_cached:
            self.process_stress_field()
        else:
            self.set_frames_disabled(True)

    def set_frames_disabled(self, disabled: bool):
        self.frame_animation.setDisabled(disabled)
        self.frame_color.setDisabled(disabled)
        self.frame_frequency.setDisabled(disabled)
        self.frame_plot_type.setDisabled(disabled)
        self.frame_tree_widget.setDisabled(disabled)
        self.pushButton_process_nodal_stresses.setEnabled(disabled)

    def _create_connections(self):

        # QComboBox connections
        self.comboBox_plot_type.currentIndexChanged.connect(self.update_plot)
        self.comboBox_plotting_results.currentIndexChanged.connect(self.update_plot)
        self.comboBox_stress_units.currentIndexChanged.connect(self.update_plot)

        # QPushButton connection
        self.pushButton_process_nodal_stresses.clicked.connect(self.process_stress_field)

        # QTreeWiget connections
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_click_item)

        self.results_display_widget.colormap_changed.connect(self.animation_widget.update_color_and_deformation)
        self.results_display_widget.pressure_value_changed.connect(self.animation_widget.update_color_and_deformation)

    def _add_animation_widget(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_animation.setLayout(self.grid_layout)

        self.animation_widget = AnimationWidget()
        self.grid_layout.addWidget(self.animation_widget)
        self.frame_animation.adjustSize()

    def _add_color_widget(self):
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_color.setLayout(grid_layout)

        self.results_display_widget = ResultsDisplayWidget()
        grid_layout.addWidget(self.results_display_widget)
        self.frame_color.adjustSize()

    def configure_results_display_widget(self):
        self.results_display_widget.configure_widget()

    def update_animation_widget_visibility(self):
        index = self.comboBox_plot_type.currentIndex()
        if index >= 2:
            self.animation_widget.setDisabled(True)
        else:
            self.animation_widget.setDisabled(False)

    def show_results_render(self):
        curent_render_widget = app().main_window.get_current_render_widget()
        results_render_widget = app().main_window.results_widget

        if curent_render_widget != results_render_widget:
            app().main_window.render_widgets_stack.setCurrentWidget(results_render_widget)
            app().main_window.render_widget_changed.emit()
            app().main_window.view_toolbar.disable_selection_tool()

    def process_stress_field(self):

        # recover the averaged structural stresses
        if not self.is_stress_data_cached:    
            def recover_stresses():
                t0 = perf_counter()
                self.structural_post.recover_nodal_averaged_structural_stresses()
                dt = perf_counter() - t0
                print(f"Time to compute all nodal stresses: {dt} s")

            LoadingWindow(recover_stresses).run()

        self.set_frames_disabled(False)
        self.load_frequencies()
        self.show_results_render()

    def update_plot(self):

        stress_index = self.comboBox_plotting_results.currentIndex()
        plot_type = self.get_plot_type()

        if stress_index == 6 and plot_type == StressPlotType.NON_ABSOLUTE_ANIMATION:
            with QSignalBlocker(self.comboBox_plot_type):
                self.comboBox_plot_type.setCurrentIndex(1)
                plot_type = self.get_plot_type()

        self.update_animation_widget_visibility()
        if self.lineEdit_selected_frequency.text() == "":
            return

        frequency_selected = float(self.lineEdit_selected_frequency.text())
        selector_mask = np.abs(self.frequencies - frequency_selected) < 1e-6

        if selector_mask.any():
            self.selected_frequency_index = self.indices[selector_mask][0]

        if self.selected_frequency_index is None:
            return

        if self.get_plot_type() in [StressPlotType.ABSOLUTE_ANIMATION, StressPlotType.ABSOLUTE_VALUES]:
            self.results_display_widget.configure_validators(0, 1e14)
        else:
            self.results_display_widget.configure_validators(-1e14, 1e14)

        stress_units = self.comboBox_stress_units.currentText()
        unit_factor = convert_stress_unit(1, "Pa", stress_units)

        plot_setup = StressFieldPlotSetupFrequency(
            phase=self.animation_widget.phase_in_radians,
            index=self.selected_frequency_index,
            magnification_factor=self.animation_widget.magnification_factor,
            stress_type=stress_index,
            plot_type=plot_type,
            unit=stress_units,
            unit_factor=unit_factor,
        )

        self.animation_widget.reset_sliders()
        LoadingWindow(app().main_window.results_widget.update_plot).run(
            reset_camera=False,
            plot_setup=plot_setup,
        )

    def get_plot_type(self) -> StressPlotType:
        plot_types = [
            "non_absolute_animation",
            "absolute_animation",
            "absolute_values",
            "real_values",
            "imag_values",
        ]
        index = self.comboBox_plot_type.currentIndex()
        return StressPlotType(plot_types[index])

    def load_frequencies(self):
        if isinstance(app().project.model.frequencies, np.ndarray):
            self.frequencies = app().project.model.frequencies
        else:
            return

        self.indices = np.arange(len(self.frequencies), dtype=int)

        self.treeWidget_frequencies.clear()
        for index, frequency in enumerate(self.frequencies):
            round_freq = round(frequency, 12)
            item = QTreeWidgetItem([str(index + 1), f"{round_freq}"])

            for i in range(2):
                item.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_frequencies.addTopLevelItem(item)

        first_item = self.treeWidget_frequencies.topLevelItem(0)
        first_item.setSelected(True)
        self.treeWidget_frequencies.itemClicked.emit(first_item, 0)

    def get_selected_frequency_index(self):
        if self.selected_frequency_index is None:
            return 0

        return self.selected_frequency_index

    def on_click_item(self, item: QTreeWidgetItem):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
