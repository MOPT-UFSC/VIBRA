from PySide6.QtCore import Signal

from vibra import app
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.ui_generated.plots.general.results_display_widget_ui import ResultsDisplayWidget_UI
from vibra.interface.viewer_3d.coloring.color_palettes import COLORMAP_NAMES


class ResultsDisplayWidget(ResultsDisplayWidget_UI):
    colormap_changed = Signal()
    pressure_value_changed = Signal()

    def __init__(self):
        super().__init__()

        self.create_connections()
        self.load_user_preference_colormap()
        self.update_min_enabled(False)
        self.update_max_enabled(False)

    def configure_widget(self, bottom: float = -1e14, top: float = 1e14, decimals: int = 14):
        self.lineEdit_min_pressure.setValidator(StrictDoubleValidator(bottom, top, decimals))
        self.lineEdit_max_pressure.setValidator(StrictDoubleValidator(bottom, top, decimals))

        self.load_pressures()

    def create_connections(self):
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)
        self.lineEdit_min_pressure.editingFinished.connect(self.update_pressures)
        self.lineEdit_max_pressure.editingFinished.connect(self.update_pressures)
        self.pushButton_reset_pressures.clicked.connect(self.reset_pressures)
        self.min_pressure_check_box.stateChanged.connect(self.update_min_enabled)
        self.max_pressure_check_box.stateChanged.connect(self.update_max_enabled)

    def update_min_enabled(self, value):
        self.lineEdit_min_pressure.setEnabled(value)
        if value:
            render_widget = app().main_window.results_widget
            self.lineEdit_min_pressure.setText(f"{render_widget.min_value:.1e}")
        else:
            self.lineEdit_min_pressure.clear()

    def update_max_enabled(self, value):
        self.lineEdit_max_pressure.setEnabled(value)
        if value:
            render_widget = app().main_window.results_widget
            self.lineEdit_max_pressure.setText(f"{render_widget.max_value:.1e}")
        else:
            self.lineEdit_max_pressure.clear()

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

    def load_pressures(self):
        self.blockSignals(True)

        render_widget = app().main_window.results_widget
        min_value = f"{render_widget.min_value:.1e}"
        max_value = f"{render_widget.max_value:.1e}"

        self.lineEdit_min_pressure.setText(min_value)
        self.lineEdit_max_pressure.setText(max_value)

        self.blockSignals(False)

    def max_pressure(self) -> float | None:
        try:
            return float(self.lineEdit_max_pressure.text().replace(",", "."))
        except ValueError:
            return None

    def min_pressure(self) -> float | None:
        try:
            return float(self.lineEdit_min_pressure.text().replace(",", "."))
        except ValueError:
            return None

    def get_pressure_range(self) -> tuple[float, float] | None:
        try:
            min_value = float(self.lineEdit_min_pressure.text().replace(",", "."))
            max_value = float(self.lineEdit_max_pressure.text().replace(",", "."))
        except ValueError:
            return None

        if min_value >= max_value:
            return None

        return min_value, max_value

    def update_pressures(self):
        values = self.get_pressure_range()
        if values is None:
            return

        min_value, max_value = values
        render_widget = app().main_window.results_widget
        render_widget.set_min_value(min_value)
        render_widget.set_max_value(max_value)

        self.pressure_value_changed.emit()

    def reset_pressures(self):
        render_widget = app().main_window.results_widget
        render_widget.user_changed_pressure_values = False

        self.pressure_value_changed.emit()
        self.load_pressures()
