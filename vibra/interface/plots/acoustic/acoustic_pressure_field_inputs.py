from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTreeWidgetItem

from vibra import app
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.ui_generated.plots.acoustic.acoustic_pressure_field_inputs_ui import AcousticPressureFieldInputs_UI
from vibra.interface.viewer_3d.coloring.color_palettes import COLORMAP_NAMES

import numpy as np


class AcousticPressureFieldInputs(AcousticPressureFieldInputs_UI):
    value_changed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()
        self._configure_qt_variables()
        self._create_connections()
        self.load_frequencies()
        self.load_user_preference_colormap()

    def showEvent(self, event):
        super().showEvent(event)

        render_widget = app().main_window.results_widget
        app().main_window.render_widgets_stack.setCurrentWidget(render_widget)
        app().main_window.render_widget_changed.emit()

        app().main_window.animation_toolbar.setDisabled(False)
        app().main_window.render_tools_toolbar.hide_selection_tool()

    def _initialize(self):
        self.current_frequency = None

    def _configure_qt_variables(self):
        #
        self.frame_button.setVisible(False)
        self.frame_transparency.setVisible(False)
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
        self.pushButton_plot.clicked.connect(self.update_plot)
        #
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)
        #
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.load_user_preference_colormap()

    def update_animation_widget_visibility(self):
        index = self.comboBox_plot_type.currentIndex()
        if index >= 2:
            app().main_window.animation_toolbar.setDisabled(True)
        else:
            app().main_window.animation_toolbar.setDisabled(False)

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
            app().main_window.results_widget.update_color_and_deformation()
        except AttributeError:
            pass

    def update_transparency_callback(self):
        return
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

    def update_plot(self):
        self.update_animation_widget_visibility()
        if self.lineEdit_selected_frequency.text() == "":
            return

        frequency_selected = float(self.lineEdit_selected_frequency.text())
        self.current_frequency = self.frequency_to_index.get(frequency_selected)

        if self.current_frequency is None:
            return

        LoadingWindow(app().main_window.results_widget.update_plot).run()

    def get_colormap(self) -> str:
        index = self.comboBox_colormaps.currentIndex()
        if not (0 <= index < len(COLORMAP_NAMES)):
            return "jet"
        return COLORMAP_NAMES[index]

    def get_plot_type(self):
        plot_types = [
            "absolute_animation",
            "non_absolute_animation",
            "absolute_values",
            "real_values",
            "imag_values",
        ]
        index = self.comboBox_plot_type.currentIndex()
        return plot_types[index]

    def load_frequencies(self):
        if isinstance(app().project.model.frequencies, np.ndarray):
            self.frequencies = app().project.model.frequencies
        else:
            return

        self.frequency_to_index = dict(
            zip(self.frequencies, np.arange(len(self.frequencies), dtype=int))
        )

        self.treeWidget_frequencies.clear()
        for index, frequency in enumerate(self.frequencies):
            new = QTreeWidgetItem([str(index + 1), str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)

        first_item = self.treeWidget_frequencies.topLevelItem(0)
        first_item.setSelected(True)
        self.treeWidget_frequencies.itemClicked.emit(first_item, 0)

    def current_frequency_index(self):
        if self.current_frequency is not None:
            return self.current_frequency
        return 0

    def on_click_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
