from vibra import app
from vibra.interface.ui_generated.plots.general.results_display_widget_ui import ResultsDisplayWidget_UI
from vibra.interface.viewer_3d.coloring.color_palettes import COLORMAP_NAMES
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator

from PySide6.QtCore import Signal


class ResultsDisplayWidget(ResultsDisplayWidget_UI):
    colormap_changed = Signal()
    pressure_value_changed = Signal()

    def __init__(self):
        super().__init__()

        self.create_connections()
        self.load_user_preference_colormap()
    
    def configure_widget(self):
        self.lineEdit_min_pressure.setValidator(StrictDoubleValidator(-1e-14, 1e14, 14))
        self.lineEdit_max_pressure.setValidator(StrictDoubleValidator(-1e-14, 1e14, 14))

        self.load_pressures()

    def create_connections(self):
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)
        self.lineEdit_min_pressure.textChanged.connect(self.update_min_pressure)
        self.lineEdit_max_pressure.textChanged.connect(self.update_max_pressure)
        self.pushButton_reset_pressures.clicked.connect(self.reset_pressures)

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

    def update_min_pressure(self):
        render_widget = app().main_window.results_widget
        render_widget.user_changed_pressure_values = True

        min_value, max_value = self.lineEdit_min_pressure.text(), self.lineEdit_max_pressure.text()
        if min_value >= max_value:
            self.reset_pressures()
            return

        render_widget.set_min_value(min_value)

        self.pressure_value_changed.emit()

    def update_max_pressure(self):
        render_widget = app().main_window.results_widget
        render_widget.user_changed_pressure_values = True

        min_value, max_value = self.lineEdit_min_pressure.text(), self.lineEdit_max_pressure.text()
        if max_value <= min_value:
            self.reset_pressures()
            return

        render_widget.set_max_value(max_value)

        self.pressure_value_changed.emit() 

    def reset_pressures(self):
        render_widget = app().main_window.results_widget
        render_widget.user_changed_pressure_values = False

        self.pressure_value_changed.emit()
        self.load_pressures()