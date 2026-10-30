import numpy as np
from PySide6.QtCore import Signal

from vibra import app
from vibra.engine.analysis_info import FrequencySpacing
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.ui_generated.plots.general.ifft_controls_widget_ui import IfftControlsWidget_UI
from vibra.utils.signal_processing import process_ifft_from_one_sided_spectrum_signal, process_multiple_iffts_from_one_sided_spectrum_signals


class IfftControlsWidget(IfftControlsWidget_UI):
    ifft_controls_changed = Signal()

    def __init__(self):
        super().__init__()

        self._configure_validators()
        self._create_connections()


    @property
    def model(self):
        return app().project.model


    def _configure_validators(self):
        f_max = self.model.analysis_setup.f_max
        self.lineEdit_maximum_frequency.setValidator(StrictDoubleValidator(f_max, 2e4, 8))


    def _create_connections(self):

        # QCheckBox connection
        self.checkBox_control_frequency_resolution.stateChanged.connect(self.frequency_resolution_control_callback)

        # QSpinBox connection
        self.spinBox_intervals_number.valueChanged.connect(self.intervals_changed_callback)

        # QLineEdit connection
        self.lineEdit_maximum_frequency.editingFinished.connect(self.maximum_frequency_changed_callback)

        self.intervals_changed_callback()


    def frequency_resolution_control_callback(self):
        controlled_resolution = self.checkBox_control_frequency_resolution.isChecked()
        self.spinBox_intervals_number.setEnabled(controlled_resolution)

        if not controlled_resolution:
            self.spinBox_intervals_number.setValue(1)
            return

        if self.spinBox_intervals_number.value() != 1:
            return

        self.spinBox_intervals_number.setValue(30)


    def intervals_changed_callback(self):
        if self.model.analysis_setup.frequency_spacing != FrequencySpacing.EQUALLY_DISTRIBUTED:
            return

        f_step = self.model.analysis_setup.f_step
        f_max = self.model.analysis_setup.f_max

        if self.checkBox_control_frequency_resolution.isChecked():
            N = self.spinBox_intervals_number.value()
            df = round(f_step / N, 8)
            if self.lineEdit_maximum_frequency.text() == "":
                self.reset_fmax_value_for_ifft_processing()
            else:
                current_max = float(self.lineEdit_maximum_frequency.text())
                if np.allclose(current_max, f_max, atol=1e-5):
                    self.reset_fmax_value_for_ifft_processing()

        else:
            df = f_step

            self.spinBox_intervals_number.setValue(1)
            self.lineEdit_maximum_frequency.setText(str(f_max))

        self.lineEdit_frequency_resolution.setText(str(df))
        self.ifft_controls_changed.emit()


    def maximum_frequency_changed_callback(self):
        self.ifft_controls_changed.emit()


    def reset_fmax_value_for_ifft_processing(self):
        if not self.checkBox_control_frequency_resolution.isChecked():
            return

        f_max = self.model.analysis_setup.f_max
        f_max_new = 200 * (f_max // 200 + 1)

        self.lineEdit_maximum_frequency.setText(str(f_max_new))


    def get_fmax_for_ifft_processing(self) -> float | None:
        if not self.checkBox_control_frequency_resolution.isChecked():
            return

        try:
            current_value = float(self.lineEdit_maximum_frequency.text())
            return round(current_value, 4)
        except:
            return


    def get_number_of_fstep_divisions(self):
        if self.checkBox_control_frequency_resolution.isChecked():
            return self.spinBox_intervals_number.value()

        return


    def get_ifft_number_of_spectral_lines(self):
        if self.checkBox_control_frequency_resolution.isChecked():
            f_step = self.model.analysis_setup.f_step
            f_max = self.get_fmax_for_ifft_processing()
            N_div = self.get_number_of_fstep_divisions()

            N_lines = round(f_max / (f_step / N_div))

            return N_lines

        return


    def get_ifft_processing_function(self, multiple_iffts: bool = False):

        if multiple_iffts:
            return process_multiple_iffts_from_one_sided_spectrum_signals

        return process_ifft_from_one_sided_spectrum_signal


    def process_ifft_for_spectrum(self, Xf: np.ndarray[complex], multiple_iffts: bool = False):

        if self.model.analysis_setup.frequency_spacing != FrequencySpacing.EQUALLY_DISTRIBUTED:
            return (None, None)

        freqs = self.model.frequencies
        n_div = self.get_number_of_fstep_divisions()

        ifft_function = self.get_ifft_processing_function(multiple_iffts=multiple_iffts)

        if n_div is None:
            time_vector, pressure_time = ifft_function(freqs.max(), Xf)

        else:
            f_step = self.model.analysis_setup.f_step
            f_max = self.model.analysis_setup.f_max

            f_max_ifft = self.get_fmax_for_ifft_processing()

            df = f_step / n_div
            N = round(f_max_ifft / df)

            # initialize the frequencies vector for ifft
            freqs_ifft = np.arange(1, N + 1, dtype=float) * df

            # process mask for solution steps
            mask = (np.round(freqs_ifft % f_step, 8) == 0) & (freqs_ifft < f_max + f_step / 100)

            # initialize the temporary solution array
            if multiple_iffts:
                nodal_solution_ifft = np.zeros((len(Xf), freqs_ifft.size), dtype=complex)
                nodal_solution_ifft[:, mask] = Xf

            else:
                nodal_solution_ifft = np.zeros(freqs_ifft.size, dtype=complex)
                nodal_solution_ifft[mask] = Xf

            time_vector, pressure_time = ifft_function(freqs_ifft.max(), nodal_solution_ifft)

        return time_vector, pressure_time