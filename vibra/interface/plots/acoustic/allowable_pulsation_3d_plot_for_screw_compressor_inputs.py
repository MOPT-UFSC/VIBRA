from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.plots.general.animation_widget import AnimationWidget
from vibra.interface.ui_generated.plots.acoustic.allowable_pulsations_3d_plot_for_screw_compressor_inputs_ui import (
    AllowablePulsations3dPlotForScrewCompressorInputs_UI,
)
from vibra.interface.viewer_3d.coloring.color_palettes import COLORMAP_NAMES
from vibra.interface.viewer_3d.plot_setup import AllowablePulsationForScrewCompressorsPlotSetup, PressurePlotType


class AllowablePulsations3DPlotForScrewCompressorInputs(AllowablePulsations3dPlotForScrewCompressorInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self._reset_variables()
        self._create_connections()

        self.load_user_preference_colormap()
        self._load_analysis_setup_and_solution()

        self.animation_widget = AnimationWidget()

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

    def _create_connections(self):

        # QComboBox connection
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)

        # QCheckBox connection
        self.checkBox_pre_study_analysis.stateChanged.connect(self.penalize_allowable_pulsation_callback)

        # QPushButton
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)

        # QSlider connection
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)

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
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_analysis_actors_transparency(transparency)

    def penalize_allowable_pulsation_callback(self):
        curent_render_widget = app().main_window.get_current_render_widget()
        results_render_widget = app().main_window.results_widget

        if curent_render_widget == results_render_widget:
            self.plot_data_callback()

    def plot_data_callback(self):

        plot_setup = AllowablePulsationForScrewCompressorsPlotSetup(
            plot_type=self.get_plot_type(),
            unit="kPa",
            pre_study_analysis=self.checkBox_pre_study_analysis.isChecked()
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
