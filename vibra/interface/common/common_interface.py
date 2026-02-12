from PySide6.QtWidgets import QDialog, QFileDialog, QWidget

from vibra import app

from pathlib import Path
import numpy as np


def update_analysis_setup_in_file(frequencies: np.ndarray):

    analysis_setup = app().file.read_analysis_setup_from_file()

    analysis_setup.update(
        {
        "frequency_spacing" : "tabular",
        "f_min" : float(frequencies[0]),
        "f_max" : float(frequencies[-1]),
        "f_step" : float(frequencies[1] - frequencies[0]),
        "frequencies" : None,
        "solution_steps_mask" : list(),
        }
        )

    app().project.model.set_analysis_setup(analysis_setup)
    app().file.write_analysis_setup_in_file(analysis_setup)

def export_modal_analysis_results(parent: QDialog | QWidget, modes_to_frequencies: dict, physical_domain: str):

    last_path = app().config.get_last_folder_for("exported_table_folder")
    if last_path is None:
        last_path = str(Path().home())

    caption = "Export the modal analysis results"
    _filter = "Spreadsheet (*.xlsx);; Spreadsheet (*.xls);; Text file (*.dat);; Text file (*.txt);; Text file (*.csv)"

    export_path, extension = QFileDialog.getSaveFileName(
        parent,
        caption,
        last_path,
        filter = _filter,
        )

    if not extension:
        return

    app().config.write_last_folder_path_in_file("exported_table_folder", export_path)

    if physical_domain == "acoustic":
        complex_natural_frequencies = app().project.acoustic_modal_solver.complex_natural_frequencies
    else:
        complex_natural_frequencies = app().project.structural_modal_solver.complex_natural_frequencies

    if complex_natural_frequencies.size:
        cols = 3
        fmt = "%i %.12e %.12e"
        header = "Mode, Damped frequency [Hz], Damping ratio [--]"

    else:
        cols = 2
        fmt = "%i %.12e"
        header = "Mode, Natural frequency [Hz]"

    rows = len(modes_to_frequencies)
    modal_data_to_export = np.zeros((rows, cols), dtype=float)

    for i, (mode, value) in enumerate(modes_to_frequencies.items()):
        if isinstance(value, complex):
            damping_ratio = -np.real(value) / np.abs(value)
            damped_frequency = np.abs(value) * ((1 - damping_ratio**2) ** (1 / 2))
            modal_data_to_export[i, :] = [mode, damped_frequency, damping_ratio]

        else:
            modal_data_to_export[i, :] = [mode, value]

    if "Text file" in extension:
        np.savetxt(export_path, modal_data_to_export, fmt=fmt, delimiter=',', header=header)

    else:
        from pandas import ExcelWriter
        from polars import DataFrame

        with ExcelWriter(export_path) as writer:
            header = header.split(",")
            df = DataFrame(modal_data_to_export, schema=header)
            df.to_pandas().to_excel(writer, sheet_name="Exported modal results", index=False)