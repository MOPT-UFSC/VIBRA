import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDialog, QToolButton, QVBoxLayout

from vibra import app
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.data_handler.import_data_to_compare import ImportDataToCompare
from vibra.interface.formatters import icons
from vibra.interface.plots.general.advanced_cursor import AdvancedCursor
from vibra.interface.ui_generated.plots.general.frequency_response_plotter_ui import (
    FrequencyResponsePlotter_UI,
)
from vibra.interface.general.print_message_input import PrintMessageInput


class FrequencyResponsePlotter(FrequencyResponsePlotter_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._initialize_canvas()
        self._create_connections()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Frequency response plotter")

    def _initialize(self):

        self.keep_window_open = True
        self.decibel_data = False
        self._layout = None
        self.x_data = None
        self.y_data = None

        self.importer = None
        self.exporter = None

        self.model_results_data = dict()
        self.imported_results_data = dict()

        self.title = ""
        self.font_weight = "normal"

        self.colors = [ [0,0,1],
                        [0,0,0],
                        [1,0,0],
                        [0,1,1],
                        [0.75,0.75,0.75],
                        [0.5, 0.5, 0.5],
                        [0.25, 0.25, 0.25] ]

    def _create_connections(self):
        #
        self.checkBox_grid.stateChanged.connect(self.plot_data_in_freq_domain)
        self.checkBox_legends.stateChanged.connect(self.plot_data_in_freq_domain)
        self.checkBox_cursor_legends.stateChanged.connect(self.plot_data_in_freq_domain)
        #
        self.comboBox_plot_type.currentIndexChanged.connect(self._update_plot_type)
        self.comboBox_differentiate_data.currentIndexChanged.connect(self.plot_data_in_freq_domain)
        #
        self.radioButton_real.clicked.connect(self._update_comboBox)
        self.radioButton_imaginary.clicked.connect(self._update_comboBox)
        self.radioButton_absolute.clicked.connect(self._update_comboBox)
        self.radioButton_decibel_scale.clicked.connect(self._update_comboBox)
        self.radioButton_disable_cursors.clicked.connect(self.update_cursor_controls)
        self.radioButton_cross_cursor.clicked.connect(self.update_cursor_controls)
        self.radioButton_harmonic_cursor.clicked.connect(self.update_cursor_controls)
        #
        self.pushButton_import_data.clicked.connect(self.import_file)
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_harmonic_lines_confirm.clicked.connect(self.harmonic_lines_confirm_callback)
        self.pushButton_harmonic_lines_remove_all.clicked.connect(self.harmonic_lines_remove_all_callback)
        #
        self.lineEdit_harmonic_lines_1st_freq.returnPressed.connect(self.harmonic_lines_confirm_callback)
        # 
        app().main_window.theme_changed.connect(self.paint_toolbar_icons)
        self._initial_config()

    def import_file(self):

        if isinstance(self.importer, QDialog):
            if self.importer.isVisible():
                if self.importer.isMinimized():
                    self.importer.showNormal()
                self.importer.raise_()
            else:
                self.importer.exec()
            return

        elif self.importer is None:
            self.importer = ImportDataToCompare(self)
            self.importer.exec()

    def _initial_config(self):
        self.aux_bool = False
        self.plot_type = self.comboBox_plot_type.currentText()
        self.checkBox_cursor_legends.setChecked(False)
        self.checkBox_cursor_legends.setDisabled(True)
        self.frame_vertical_lines.setDisabled(True)

    def _update_comboBox(self):

        self.cache_plot_type = self.comboBox_plot_type.currentText()
        aux_real = self.radioButton_real.isChecked()
        aux_imag = self.radioButton_imaginary.isChecked()
        aux_decibel = self.radioButton_decibel_scale.isChecked()

        self.aux_bool = aux_real + aux_imag + aux_decibel
        if self.aux_bool:
            self.comboBox_plot_type.setDisabled(True)
            self.comboBox_plot_type.setCurrentIndex(2)
        else:
            self.comboBox_plot_type.setDisabled(False)
            self.comboBox_plot_type.setCurrentIndex(0)
        
        if self.plot_type == self.cache_plot_type:
            self.plot_data_in_freq_domain()

    def _update_plot_type(self):
        self.plot_type = self.comboBox_plot_type.currentText()
        self.plot_data_in_freq_domain()

    def update_cursor_controls(self):
        if self.radioButton_disable_cursors.isChecked():
            self.checkBox_cursor_legends.setChecked(False)
            self.checkBox_cursor_legends.setDisabled(True)
            self.frame_vertical_lines.setDisabled(True)
        else:
            self.checkBox_cursor_legends.setDisabled(False)
            if self.radioButton_harmonic_cursor.isChecked():
                self.frame_vertical_lines.setDisabled(False)
        self.plot_data_in_freq_domain()

    def _initialize_canvas(self):
        from vibra.interface.plots.general.mpl_canvas import MplCanvas
        self.mpl_canvas_frequency_plot = MplCanvas(self, width=8, height=6, dpi=110)
        self.ax = self.mpl_canvas_frequency_plot.axes
        self.fig = self.mpl_canvas_frequency_plot.fig
    
    def export_data_callback(self):
        self.hide()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results_data)

    def plot_harmonic_lines(
        self,
        fundamental_freq: float,
        n_harmonics: int,
        show_harmonic: bool,
        show_frequency: bool,
        remove_all: bool,
    ):
        if self.x_data is None:
            return

        for line in [l for l in self.ax.lines if getattr(l, "is_harmonic_line", False)]:
            line.remove()

        for text in [t for t in self.ax.texts if getattr(t, "is_harmonic_label", False)]:
            text.remove()

        if remove_all is False:
            x_min, x_max = self.ax.get_xlim()

            for i in range(n_harmonics):
                frequency = float((i + 1) * fundamental_freq)

                if x_min <= frequency <= x_max:
                    line = self.ax.axvline(x=frequency, color="k", alpha=0.3, label="_nolegend_")
                    line.is_harmonic_line = True

                    legend = ""
                    newline = ""
                    if show_harmonic:
                        legend += f" {i + 1}x"
                        newline = "\n"

                    if show_frequency:
                        legend += f"{newline} ({frequency:.0f} Hz)"

                    if legend:
                        txt = self.ax.text(
                            frequency,
                            0.95,
                            legend,
                            transform=self.ax.get_xaxis_transform(),
                            fontsize=6,
                            verticalalignment="bottom",
                            horizontalalignment="left",
                        )
                        txt.is_harmonic_label = True

        self.mpl_canvas_frequency_plot.draw()

    def check__harmonic_lines_plot_values(self):
        error_title = "Error"
        self.fundamental_freq = self.lineEdit_harmonic_lines_1st_freq.text().strip()

        if not self.fundamental_freq:
            title = "Missing input"
            error_message = "Please input some value for the 'Fundamental frequency'."
            
            PrintMessageInput([error_title, title, error_message])
            return False
        
        try:
            float(self.fundamental_freq)
        except ValueError:
            title = "Invalid input"
            error_message = "The value inputted at 'Fundamental Frequency' must be a number."

            PrintMessageInput([error_title, title, error_message])
            return False
        
        else:
            return True

    def harmonic_lines_confirm_callback(self):
        if not self.check__harmonic_lines_plot_values():
            return
        
        fundamental_frequency = float(self.fundamental_freq)
        number_of_lines = self.spinBox_harmonic_lines_number.value()
        show_legend = self.checkBox_harmonic_lines_show_harmonic.isChecked()
        show_frequency = self.checkBox_harmonic_lines_show_frequency.isChecked()
        remove_all = False

        self.plot_harmonic_lines(
            fundamental_frequency,
            number_of_lines,
            show_legend,
            show_frequency,
            remove_all,
        )

    def harmonic_lines_remove_all_callback(self):
        self.plot_harmonic_lines(0, 0, 0, True)

    def imported_real_data(self, decibel_data: bool=False):
        self.decibel_data = decibel_data
        self.comboBox_plot_type.setCurrentIndex(2)
        self.comboBox_plot_type.setDisabled(True)
        self.radioButton_absolute.setDisabled(True)
        self.radioButton_real.setDisabled(True)
        self.radioButton_real.setChecked(True)
        self.radioButton_imaginary.setDisabled(True)
        self.radioButton_decibel_scale.setDisabled(True)
        self.comboBox_differentiate_data.setDisabled(True)

    def load_data_to_plot(self, data: dict):

        if data.get("type") != "imported_data":
            self.x_label = data.get("x_label")
            self.unit = data.get("unit", "?")
            self.y_label = self.get_y_axis_label(data.get("y_label"))

        self.x_data = data.get("x_data")
        self.y_data = self.get_y_axis_data(data.get("y_data"))

        self.color = data.get("color")
        self.title = data.get("title")
        self.legend = data.get("legend")
        self.linestyle = data.get("linestyle")

    def get_scaled_data(self, data):
        if self.radioButton_decibel_scale.isChecked():
            if self.comboBox_differentiate_data.currentIndex() != 0:
                shift = 1
            else:
                shift = 0
            self.x_data = self.x_data[shift:]
            data2 = np.real(data[shift:]*np.conjugate(data[shift:]))
            # if "Pa" in self.unit:
            if self.unit == "Pa":
                return 10*np.log10(data2/((2e-5)**2))
            else:
                return 10*np.log10(data2)
        else:
            return data

    def get_y_axis_data(self, data: np.ndarray | None):
        if data is None:
            return None

        dif_data = self.process_differentiation(data)
        if self.radioButton_real.isChecked():
            return np.real(dif_data)

        elif self.radioButton_imaginary.isChecked():
            return np.imag(dif_data)

        elif self.radioButton_absolute.isChecked():
            return np.abs(dif_data)

        else:
            return self.get_scaled_data(dif_data)

    def get_y_axis_label(self, label: str):
        
        if self.radioButton_real.isChecked():
            type_label = "real"
        elif self.radioButton_imaginary.isChecked():
            type_label = "imaginary"
        else:
            type_label = "absolute"

        if self.decibel_data:
            return f"{label} [dB]"

        unit = self.get_unit_considering_differentiation()
        if self.radioButton_decibel_scale.isChecked():
            return f"{label} - {type_label} [dB]"
        else:
            return f"{label} - {type_label} [{unit}]"

    def process_differentiation(self, data: np.ndarray):
        frequencies = self.x_data

        index = self.comboBox_differentiate_data.currentIndex()
        if index == 0:
            output_data = data
        elif index == 1:
            output_data = data*(1j*2*np.pi)*frequencies
        else:
            output_data = data*((1j*2*np.pi*frequencies)**2)

        return output_data

    def get_unit_considering_differentiation(self):
        index = self.comboBox_differentiate_data.currentIndex()
        if index == 0:
            return self.unit
        elif index == 1:
            return self.unit + "/s"
        else:
            return self.unit + "/s²"

    def paint_toolbar_icons(self, *args, **kwargs):

        from vibra.interface.plots.general.custom_navigation_toolbar import CustomNavigationToolbar

        toolbar = self.findChild(CustomNavigationToolbar)
        if toolbar is None:
            return
        from vibra import LIGHT_ICON_COLOR, DARK_ICON_COLOR
        if app().config.user_preferences.interface_theme == "dark":
            color = DARK_ICON_COLOR.to_qt()
        else:
            color = LIGHT_ICON_COLOR.to_qt()

        icons.change_icon_color_for_widgets(toolbar.findChildren(QToolButton), color)

    def plot_data_in_freq_domain(self):

        self.ax.cla()
        self.legends = list()
        self.plots = list()

        if self._layout is None:
            from vibra.interface.plots.general.custom_navigation_toolbar import CustomNavigationToolbar
            toolbar = CustomNavigationToolbar(self.mpl_canvas_frequency_plot, self)

            # Paint the toolbar icons and connect the buttons to paint
            # themselves after every click or draw events
            self.paint_toolbar_icons()
            for button in toolbar.findChildren(QToolButton):
                button.clicked.connect(self.paint_toolbar_icons)                    
            self.mpl_canvas_frequency_plot.mpl_connect("draw_event", self.paint_toolbar_icons)

            self._layout = QVBoxLayout()
            self._layout.addWidget(toolbar)
            self._layout.addWidget(self.mpl_canvas_frequency_plot)
            self._layout.setContentsMargins(2, 2, 2, 2)
            self.widget_plot.setLayout(self._layout)

        for current_data in [self.model_results_data, self.imported_results_data]:
            for _, data in current_data.items():

                self.load_data_to_plot(data)

                if self.y_data is not None:
                    self.mask_x = self.x_data <= 0
                    self.mask_y = self.y_data <= 0
                    if self.aux_bool:
                        _plot = self.call_lin_lin_plot()
                    elif True in (self.mask_x + self.mask_y):
                        _plot = self.get_plot_considering_invalid_log_values()
                    elif "log-log" in self.plot_type:
                        _plot = self.call_log_log_plot()
                    elif "log-y" in self.plot_type:
                        _plot = self.call_semilog_y_plot()
                    elif "log-x" in self.plot_type:
                        _plot = self.call_semilog_x_plot()
                    else:
                        _plot = self.call_lin_lin_plot()

                    self.legends.append(self.legend)
                    self.plots.append(_plot)

        if self.plots:

            if self.checkBox_legends.isChecked():
                self.ax.legend(handles=self.plots, labels=self.legends)
                
            self.call_cursor()
            self.ax.set_xlabel(self.x_label, fontsize = 10, fontweight = self.font_weight)
            self.ax.set_ylabel(self.y_label, fontsize = 10, fontweight = self.font_weight)
            
            if self.title != "":
                self.ax.set_title(self.title, fontsize = 11, fontweight = self.font_weight)

            if self.checkBox_grid.isChecked():
                self.ax.grid()

            self.mpl_canvas_frequency_plot.draw()
            return

    def call_semilog_y_plot(self, first_index=0):
        _plot, = self.ax.semilogy(  self.x_data[first_index:], 
                                    self.y_data[first_index:], 
                                    linewidth = 1,
                                    color = self.color, 
                                    linestyle = self.linestyle  )
        return _plot

    def call_semilog_x_plot(self, first_index=0):
        _plot, = self.ax.semilogx(  self.x_data[first_index:], 
                                    self.y_data[first_index:], 
                                    linewidth = 1,
                                    color = self.color, 
                                    linestyle = self.linestyle  )
        return _plot

    def call_lin_lin_plot(self):

        if self.comboBox_plot_type.currentIndex() != 2:
            self.comboBox_plot_type.blockSignals(True)
            self.comboBox_plot_type.setCurrentIndex(2)
            self.comboBox_plot_type.blockSignals(False)

        _plot, = self.ax.plot(  self.x_data, 
                                self.y_data, 
                                linewidth = 1,
                                color = self.color, 
                                linestyle = self.linestyle  )
        return _plot

    def call_log_log_plot(self, first_index=0):
        _plot, = self.ax.loglog(self.x_data[first_index:], 
                                self.y_data[first_index:], 
                                linewidth = 1,
                                color = self.color, 
                                linestyle = self.linestyle  )
        return _plot
    
    def get_plot_considering_invalid_log_values(self):

        if "log-log" in self.plot_type:
        
            if True in self.mask_y[1:] or True in self.mask_x[1:]:
                _plot = self.call_lin_lin_plot()
            else:
                if self.mask_x[0] or self.mask_y[0]:
                    _plot = self.call_log_log_plot(first_index=1)
                else:
                    _plot = self.call_log_log_plot(first_index=0)

        elif "log-x" in self.plot_type:

            if True in self.mask_x[1:]:
                _plot = self.call_lin_lin_plot()
            else:
                if self.mask_x[0]:
                    _plot = self.call_semilog_x_plot(first_index=1)
                else:
                    _plot = self.call_semilog_x_plot(first_index=0)

        elif "log-y" in self.plot_type:

            if True in self.mask_y[1:]:
                _plot = self.call_lin_lin_plot()
            else:
                if self.mask_y[0]:
                    _plot = self.call_semilog_y_plot(first_index=1)
                else:
                    _plot = self.call_semilog_y_plot(first_index=0)

        else:
        
            _plot = self.call_lin_lin_plot()
        
        return _plot

    def call_cursor(self):

        show_cursor = not self.radioButton_disable_cursors.isChecked()
        show_legend = self.checkBox_cursor_legends.isChecked()
        
        if self.radioButton_harmonic_cursor.isChecked():
            number_vertLines = self.spinBox_vertical_lines.value()    
        else:
            number_vertLines = 1

        self.cursor = AdvancedCursor(   self.ax, 
                                        self.x_data, 
                                        self.y_data, 
                                        show_cursor,
                                        show_legend,
                                        number_vertLines = number_vertLines   )

        self.mouse_connection = self.fig.canvas.mpl_connect(s='motion_notify_event', func=self.cursor.mouse_move)

    def _set_model_results_data_to_plot(self, data):
        if isinstance(data, dict):
            self.model_results_data = data
            self.plot_data_in_freq_domain()
            while self.keep_window_open:
                self.exec()

    def _set_imported_results_data_to_plot(self, data):
        if isinstance(data, dict):
            self.imported_results_data = data
            self.plot_data_in_freq_domain()
        
    def reset_imported_results_data_to_plot(self):
        self.imported_results_data = dict()
        self.plot_data_in_freq_domain()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if isinstance(self.importer, QDialog):
            if self.importer.isVisible():
                self.importer.close()
            self.importer = None

        self.keep_window_open = False
        return super().closeEvent(a0)