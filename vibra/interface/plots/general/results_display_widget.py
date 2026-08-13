import numpy as np
from PySide6.QtCore import Signal

from vibra import app
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.ui_generated.plots.general.results_display_widget_ui import ResultsDisplayWidget_UI
from vibra.interface.viewer_3d.coloring.color_palettes import COLORMAP_NAMES
from vibra.utils.interface_utils import block_signals


class ResultsDisplayWidget(ResultsDisplayWidget_UI):
    colormap_changed = Signal()
    pressure_value_changed = Signal()

    def __init__(self):
        super().__init__()

        self.create_connections()
        self.load_user_preference_colormap()

    def configure_widget(self, bottom: float = -1e14, top: float = 1e14, decimals: int = 14):
        self.update_min_enabled(False)
        self.update_max_enabled(False)
        self.configure_validators(bottom, top, decimals)

    def configure_validators(self, bottom: float = -1e14, top: float = 1e14, decimals: int = 14):
        validator = StrictDoubleValidator(bottom, top, decimals)
        self.lineEdit_min_color_value.setValidator(validator)
        self.lineEdit_max_color_value.setValidator(validator)

        min_ = self.min_color_value()
        max_ = self.max_color_value()

        if min_ is not None:
            min_ = np.clip(min_, bottom, top)
            self.lineEdit_min_color_value.setText(str(min_))

        if max_ is not None:
            max_ = np.clip(max_, bottom, top)
            self.lineEdit_max_color_value.setText(str(max_))

    def create_connections(self):
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)
        self.lineEdit_min_color_value.editingFinished.connect(self.update_color_ranges)
        self.lineEdit_max_color_value.editingFinished.connect(self.update_color_ranges)
        self.min_color_check_box.stateChanged.connect(self.update_min_enabled)
        self.max_color_check_box.stateChanged.connect(self.update_max_enabled)

    def update_min_enabled(self, value):
        if value:
            render_widget = app().main_window.results_widget
            self.lineEdit_min_color_value.setText(f"{render_widget.min_value:.1e}")
        else:
            self.lineEdit_min_color_value.clear()

        self.lineEdit_min_color_value.setEnabled(value)
        self.update_color_ranges()

        with block_signals(self):
            self.min_color_check_box.setChecked(value)

    def update_max_enabled(self, value):
        if value:
            render_widget = app().main_window.results_widget
            self.lineEdit_max_color_value.setText(f"{render_widget.max_value:.1e}")
        else:
            self.lineEdit_max_color_value.clear()

        self.lineEdit_max_color_value.setEnabled(value)
        self.update_color_ranges()

        with block_signals(self):
            self.max_color_check_box.setChecked(value)

    def update_colormap_type(self):
        app().config.user_preferences.color_map = self.get_colormap()
        app().config.update_config_file()
        try:
            self.colormap_changed.emit()
        except AttributeError:
            pass

    def update_transparency_callback(self):
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_analysis_actors_transparency(transparency)

    def get_colormap(self) -> str:
        index = self.comboBox_colormaps.currentIndex()
        if not (0 <= index < len(COLORMAP_NAMES)):
            return "jet"
        return COLORMAP_NAMES[index]

    def load_user_preference_colormap(self):
        try:
            colormap = app().config.user_preferences.color_map
            if colormap in COLORMAP_NAMES:
                index = COLORMAP_NAMES.index(colormap)
                self.comboBox_colormaps.setCurrentIndex(index)
        except Exception:
            self.comboBox_colormaps.setCurrentIndex(0)

    def min_color_value(self) -> float | None:
        try:
            return float(self.lineEdit_min_color_value.text().replace(",", "."))
        except ValueError:
            return None

    def max_color_value(self) -> float | None:
        try:
            return float(self.lineEdit_max_color_value.text().replace(",", "."))
        except ValueError:
            return None

    def update_color_ranges(self):
        min_value = self.min_color_value()
        max_value = self.max_color_value()

        render_widget = app().main_window.results_widget
        render_widget.set_min_value(min_value)
        render_widget.set_max_value(max_value)

        self.pressure_value_changed.emit()
