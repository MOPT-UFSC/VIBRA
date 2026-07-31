import numpy as np
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QGridLayout, QTreeWidgetItem

from vibra import app
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.plots.general.animation_widget import AnimationWidget
from vibra.interface.ui_generated.plots.acoustic.acoustic_pressure_field_inputs_ui import AcousticPressureFieldInputs_UI
from vibra.interface.viewer_3d.coloring.color_palettes import COLORMAP_NAMES
from vibra.interface.viewer_3d.plot_setup import FrequencyPressurePlotSetup, PlotSetup, PressurePlotType


class AcousticPressureFieldInputs(AcousticPressureFieldInputs_UI):
    value_changed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()
        self._configure_widgets()
        self._create_connections()
        self.add_animation_widget()

        self.load_user_preference_colormap()
        self.load_frequencies()

    def showEvent(self, event):
        super().showEvent(event)

        render_widget = app().main_window.results_widget
        app().main_window.render_widgets_stack.setCurrentWidget(render_widget)
        app().main_window.render_widget_changed.emit()
        app().main_window.view_toolbar.disable_selection_tool()

    def _initialize(self):
        self.selected_frequency_index = None

    def _configure_widgets(self):
        #
        self.lineEdit_selected_frequency.setDisabled(True)
        self.lineEdit_selected_frequency.setProperty("status", "information")
        #
        for i, width in enumerate([80, 140]):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)
        self.comboBox_plot_type.currentIndexChanged.connect(self.update_plot)
        #
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)
        #
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_click_item)

    def add_animation_widget(self):

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_animation.setLayout(self.grid_layout)

        self.animation_widget = AnimationWidget()
        self.grid_layout.addWidget(self.animation_widget)
        self.frame_animation.adjustSize()

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

    def update_transparency_callback(self):
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_analysis_actors_transparency(transparency)

    def update_plot(self):
        self.update_animation_widget_visibility()
        if self.lineEdit_selected_frequency.text() == "":
            return

        frequency_selected = float(self.lineEdit_selected_frequency.text())
        selector_mask = np.abs(self.frequencies - frequency_selected) < 1e-6

        if selector_mask.any():
            self.selected_frequency_index = self.indexes[selector_mask][0]

        if self.selected_frequency_index is None:
            return

        plot_setup = FrequencyPressurePlotSetup(
            phase=self.animation_widget.phase_in_radians,
            index=self.selected_frequency_index,
            plot_type=self.get_plot_type(),
            unit="Pa",
        )

        self.animation_widget.reset_sliders()
        LoadingWindow(app().main_window.results_widget.update_plot).run(plot_setup=plot_setup)

    def get_colormap(self) -> str:
        index = self.comboBox_colormaps.currentIndex()
        if not (0 <= index < len(COLORMAP_NAMES)):
            return "jet"
        return COLORMAP_NAMES[index]

    def get_plot_type(self) -> PressurePlotType:
        plot_types = [
            "non_absolute_animation",
            "absolute_animation",
            "absolute_values",
            "real_values",
            "imag_values",
        ]
        index = self.comboBox_plot_type.currentIndex()
        return PressurePlotType(plot_types[index])

    def load_frequencies(self):
        if isinstance(app().project.model.frequencies, np.ndarray):
            self.frequencies = app().project.model.frequencies
        else:
            return

        self.indexes = np.arange(len(self.frequencies), dtype=int)

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
