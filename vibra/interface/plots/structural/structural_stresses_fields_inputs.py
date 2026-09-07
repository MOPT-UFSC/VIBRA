from enum import IntEnum
from time import perf_counter

import numpy as np
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QGridLayout, QTreeWidgetItem

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.plots.general.animation_widget import AnimationWidget
from vibra.interface.plots.general.results_display_widget import ResultsDisplayWidget
from vibra.interface.ui_generated.plots.structural.structural_stresses_field_inputs_ui import StructuralStressesFieldInputs_UI
from vibra.interface.viewer_3d.coloring.color_palettes import COLORMAP_NAMES
from vibra.interface.viewer_3d.plot_setup import StressFieldPlotSetupFrequency, StressPlotType


class ReduceLoopType(IntEnum):
    DISABLED = 0
    USER_DEFINED = 1
    ROTATIONAL_SPEED = 2


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

        # self.load_frequencies()

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
        return app().project.model.solution.structural_solution

    @property
    def structural_post(self):
        return app().project.get_structural_postprocessing()

    def showEvent(self, event):
        super().showEvent(event)

        render_widget = app().main_window.results_widget
        app().main_window.render_widgets_stack.setCurrentWidget(render_widget)
        app().main_window.render_widget_changed.emit()
        app().main_window.view_toolbar.disable_selection_tool()

    def _initialize(self):
        self.selected_frequency_index = None

    def _configure_widgets(self):

        self.lineEdit_selected_frequency.setDisabled(True)
        self.lineEdit_selected_frequency.setProperty("status", "information")

        for i, width in enumerate([80, 140]):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):

        # QComboBox connection
        self.comboBox_plot_type.currentIndexChanged.connect(self.update_plot)

        # QPushButton connection
        self.pushButton_plot_data.clicked.connect(self.process_stress_field)

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

    def process_stress_field(self):

        structural_post = self.structural_post

        t0 = perf_counter()
        avg_nodal_stresses, _ = structural_post.get_structural_stresses()
        dt = perf_counter() - t0
        print(f"Time to compute nodal stresses: {dt} s")

        nodal_averaged_stresses = structural_post.nodal_stresses_post_process(avg_nodal_stresses)
        # element_averaged_stresses = structural_post.nodal_stresses_post_process(element_stresses)

        self.load_frequencies()

    def update_plot(self):
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

        plot_setup = StressFieldPlotSetupFrequency(
            phase=self.animation_widget.phase_in_radians,
            index=self.selected_frequency_index,
            magnification_factor=self.animation_widget.magnification_factor,
            plot_type=self.get_plot_type(),
            unit="MPa",
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
