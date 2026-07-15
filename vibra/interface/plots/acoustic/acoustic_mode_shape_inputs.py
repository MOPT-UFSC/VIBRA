import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QTreeWidgetItem

from vibra import app
from vibra.engine.solution import ModalSolution
from vibra.interface.common.common_interface import export_modal_analysis_results
from vibra.interface.formatters.icons import change_icon_color_for_widgets
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.plots.general.animation_widget import AnimationWidget
from vibra.interface.ui_generated.plots.acoustic.acoustic_mode_shape_inputs_ui import (
    AcousticModeShapeInputs_UI,
)
from vibra.interface.viewer_3d.coloring.color_palettes import COLORMAP_NAMES
from vibra.interface.viewer_3d.plot_setup import FrequencyPressurePlotSetup


class AcousticModeShapeInputs(AcousticModeShapeInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()
        self._paint_icons()
        self._create_connections()
        self.add_animation_widget()

    def showEvent(self, event):
        super().showEvent(event)

        render_widget = app().main_window.results_widget
        app().main_window.render_widgets_stack.setCurrentWidget(render_widget)
        app().main_window.render_widget_changed.emit()
        app().main_window.view_toolbar.disable_selection_tool()

    def _initialize(self):
        self.mode_index = None

    def _create_connections(self):
        #
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)
        self.comboBox_plot_type.currentIndexChanged.connect(self.update_plot)
        #
        self.pushButton_export_results.clicked.connect(self.export_results_callback)
        #
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)
        #
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_click_item)
        #
        app().main_window.theme_changed.connect(self._paint_icons)
        #
        self.load_user_preference_colormap()

    def add_animation_widget(self):

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_animation.setLayout(self.grid_layout)

        self.animation_widget = AnimationWidget()
        self.grid_layout.addWidget(self.animation_widget)
        self.frame_animation.adjustSize()

    def _configure_widgets(self):
        #
        self.frame_transparency.setVisible(False)
        self.lineEdit_natural_frequency.setDisabled(True)
        self.lineEdit_natural_frequency.setProperty("status", "information")

        solution = app().project.model.solution
        if not isinstance(solution, ModalSolution):
            return

        if isinstance(solution.complex_natural_frequencies, np.ndarray) and solution.complex_natural_frequencies.size:
            widths = [60, 160]
            headers = ["Mode", "Damped frequency [Hz]", "Damping ratio [--]"]

        else:
            widths = [120, 160]
            headers = ["Mode", "Frequency [Hz]"]

        font = QFont()
        font.setPointSize(9)

        self.treeWidget_frequencies.setColumnCount(len(headers))

        for i, header in enumerate(headers):
            self.treeWidget_frequencies.headerItem().setFont(i, font)
            self.treeWidget_frequencies.headerItem().setText(i, header)
            if i < 2:
                self.treeWidget_frequencies.setColumnWidth(i, widths[i])

            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _paint_icons(self):

        icon_color = None
        theme = app().config.user_preferences.interface_theme
        from vibra import DARK_ICON_COLOR, LIGHT_ICON_COLOR

        if theme == "dark":
            icon_color = DARK_ICON_COLOR.to_qt()
        else:
            icon_color = LIGHT_ICON_COLOR.to_qt()

        widgets = [self.pushButton_export_results]

        change_icon_color_for_widgets(widgets, icon_color)

    def update_animation_widget_visibility(self):
        index = self.comboBox_plot_type.currentIndex()
        if index >= 2:
            self.animation_widget.setDisabled(True)
        else:
            self.animation_widget.setDisabled(False)

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

    def get_colormap(self) -> str:
        index = self.comboBox_colormaps.currentIndex()
        if not (0 <= index < len(COLORMAP_NAMES)):
            return "jet"
        return COLORMAP_NAMES[index]

    def export_results_callback(self):
        export_modal_analysis_results(self, self.modes_to_frequencies, "acoustic")

    def update_plot(self):
        self.update_animation_widget_visibility()
        if self.lineEdit_natural_frequency.text() == "":
            return

        self.mode_index = self.natural_frequencies.index(self.selected_natural_frequency)
        self.animation_widget.reset_sliders()

        plot_setup = FrequencyPressurePlotSetup(
            phase=self.animation_widget.phase_in_radians,
            index=self.mode_index,
            plot_type=self.get_plot_type(),
        )
        LoadingWindow(app().main_window.results_widget.update_plot).run(plot_setup=plot_setup)

    def update_transparency_callback(self):
        return
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

    def get_plot_type(self):
        plot_types = [
            "non_absolute_animation",
            "absolute_animation",
            "absolute_values",
            "real_values",
            "imag_values",
        ]
        index = self.comboBox_plot_type.currentIndex()
        return plot_types[index]

    def load_natural_frequencies(self):
        solution = app().project.model.solution
        if not isinstance(solution, ModalSolution):
            return

        self._configure_widgets()

        if isinstance(solution.complex_natural_frequencies, np.ndarray) and solution.complex_natural_frequencies.size:
            self.natural_frequencies = list(solution.complex_natural_frequencies)
        else:
            self.natural_frequencies = list(solution.natural_frequencies)

        modes = np.arange(1, len(self.natural_frequencies) + 1, 1)
        self.modes_to_frequencies = dict(zip(modes, self.natural_frequencies))

        self.treeWidget_frequencies.clear()
        for mode, value in self.modes_to_frequencies.items():
            if isinstance(value, complex):
                cols = 3
                damping_ratio = -np.real(value) / np.abs(value)
                damped_frequency = np.abs(value) * ((1 - damping_ratio**2) ** (1 / 2))
                new = QTreeWidgetItem([str(mode), str(round(damped_frequency, 4)), str(round(damping_ratio, 4))])
            else:
                cols = 2
                new = QTreeWidgetItem([str(mode), str(round(value, 4))])

            if mode == 1:
                new.setSelected(True)

            for i in range(cols):
                new.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_frequencies.addTopLevelItem(new)

        first_item = self.treeWidget_frequencies.topLevelItem(0)
        self.treeWidget_frequencies.scrollToTop()

        if first_item is not None:
            first_item.setSelected(True)
            self.treeWidget_frequencies.itemClicked.emit(first_item, 0)

    def current_mode_index(self):
        if self.mode_index is not None:
            return self.mode_index
        return 0

    def on_click_item(self, item: QTreeWidgetItem):
        selected_frequency = self.modes_to_frequencies[int(item.text(0))]

        if isinstance(selected_frequency, complex):
            damping_ratio = -np.real(selected_frequency) / np.abs(selected_frequency)
            damped_frequency = np.abs(selected_frequency) * ((1 - damping_ratio**2) ** (1 / 2))
            self.lineEdit_natural_frequency.setText(str(round(damped_frequency, 4)))
        else:
            self.lineEdit_natural_frequency.setText(f"{selected_frequency: .6f}")

        self.selected_natural_frequency = selected_frequency
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
