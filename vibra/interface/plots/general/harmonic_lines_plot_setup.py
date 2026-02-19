from vibra.interface.ui_generated.plots.general.harmonic_lines_plot_setup_ui import HarmonicLinesPlotSetup_UI
from vibra import app
from PySide6.QtCore import Qt

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCloseEvent


from vibra.interface.general.print_message_input import PrintMessageInput





class HarmonicLinesPlotSetup(HarmonicLinesPlotSetup_UI):
    settings_confirmed = Signal(float, int, bool)

    def __init__(self, *args, **kwargs):
        super().__init__()

        app().main_window.set_input_widget(self)

        self._config_window()
        self._create_connections()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Harmonic lines plot setup")
    
    def _create_connections(self):
        self.pushButton_confirm.clicked.connect(self.confirm_callback)
        self.pushButton_cancel.clicked.connect(self.close)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)
    
    def check_values(self):
        error_title = "Error"
        self.fundamental_freq = self.lineEdit_fundamental_frequency.text().strip()

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

    def confirm_callback(self):
        if not self.check_values():
            return
        
        self.fundamental_frequency = float(self.fundamental_freq)
        self.number_of_lines = self.spinBox_number_of_lines.value()
        self.show_legend = self.checkBox_show_legend.isChecked()

        self.settings_confirmed.emit(
            self.fundamental_frequency,
            self.number_of_lines,
            self.show_legend,
        )

        self.close()

        