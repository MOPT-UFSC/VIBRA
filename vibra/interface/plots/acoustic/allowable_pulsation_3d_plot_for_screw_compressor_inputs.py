from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QGridLayout

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.plots.general.animation_widget import AnimationWidget
from vibra.interface.plots.general.results_display_widget import ResultsDisplayWidget
from vibra.interface.ui_generated.plots.acoustic.allowable_pulsations_3d_plot_for_screw_compressor_inputs_ui import (
    AllowablePulsations3dPlotForScrewCompressorInputs_UI,
)
from vibra.interface.viewer_3d.plot_setup import AllowablePulsationForScrewCompressorsPlotSetup, PressurePlotType


class AllowablePulsations3DPlotForScrewCompressorInputs(AllowablePulsations3dPlotForScrewCompressorInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()
        self.animation_widget = AnimationWidget()

        self._reset_variables()
        self._add_penalization_values_to_combo_box()
        self.add_color_widget()
        self._create_connections()

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
        return app().project.model.solution.acoustic_solution

    def show_results_render(self):
        curent_render_widget = app().main_window.get_current_render_widget()
        results_render_widget = app().main_window.results_widget

        if curent_render_widget != results_render_widget:
            app().main_window.render_widgets_stack.setCurrentWidget(results_render_widget)
            app().main_window.render_widget_changed.emit()
            app().main_window.view_toolbar.disable_selection_tool()

    def _load_analysis_setup_and_solution(self):
        self.analysis_method = ""
        if self.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.analysis_method = "Direct method"

        self.frequencies = self.model.frequencies

    def _reset_variables(self):
        self.unit_label = "kPa"
        self.time_vector = None
        self.plot_setup = None

    def _add_penalization_values_to_combo_box(self):
        self.comboBox_penalization_factor.clear()
        self.comboBox_penalization_factor.setFixedWidth(60)

        item_values = [str(value) for value in range(0, 100, 5)]
        self.comboBox_penalization_factor.addItems(item_values)

        # centralizes the displayed text of the combo box
        self.comboBox_penalization_factor.setEditable(True)
        line_edit = self.comboBox_penalization_factor.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)

        # centralizes the displayed texts of all items
        for i in range(self.comboBox_penalization_factor.count()):
            self.comboBox_penalization_factor.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

        tool_tip = "Use this to reduced the allowable pulsation criteria by (1 - penalization) factor. "
        self.comboBox_penalization_factor.setToolTip(tool_tip)
        self.label_penalization_factor.setToolTip(tool_tip)

    def add_color_widget(self):
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_color.setLayout(grid_layout)

        self.results_display_widget = ResultsDisplayWidget()
        grid_layout.addWidget(self.results_display_widget)
        self.frame_color.adjustSize()

    def _create_connections(self):
        # QPushButton connection
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        # QSpinBox connection
        self.comboBox_penalization_factor.currentIndexChanged.connect(self.penalize_allowable_pulsation_callback)
        #
        self.results_display_widget.colormap_changed.connect(self.animation_widget.update_color_and_deformation)
        self.results_display_widget.pressure_value_changed.connect(self.animation_widget.update_color_and_deformation)

    def penalize_allowable_pulsation_callback(self):
        curent_render_widget = app().main_window.get_current_render_widget()
        results_render_widget = app().main_window.results_widget

        if curent_render_widget == results_render_widget:
            self.plot_data_callback()

    def plot_data_callback(self):

        plot_setup = AllowablePulsationForScrewCompressorsPlotSetup(
            plot_type=self.get_plot_type(),
            unit="kPa",
            penalization_factor=int(self.comboBox_penalization_factor.currentText()),
        )

        if plot_setup == self.plot_setup:
            return

        self.plot_setup = plot_setup

        def plot_callback():
            app().main_window.results_widget.update_plot(
                reset_camera=False,
                plot_setup=self.plot_setup,
            )

        LoadingWindow(plot_callback).run()

        self.show_results_render()

    def get_plot_type(self) -> PressurePlotType:
        return PressurePlotType("non_absolute_animation")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        return super().closeEvent(a0)
