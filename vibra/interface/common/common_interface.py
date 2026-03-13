from pathlib import Path

import numpy as np
from PySide6.QtWidgets import QDialog, QFileDialog, QWidget

from vibra import app
from vibra.engine.analysis_info import HarmonicAnalysisSetup, HarmonicAnalysisSetupList


def update_analysis_setup_in_file(frequencies: np.ndarray):
    analysis_setup = app().new_project.model.new_analysis_setup

    # The previous version looks like an HarmonicAnalysisSetupRange,
    # but I think that the HarmonicAnalysisSetupList is more suitable.
    # If I am wrong please let me know.
    if isinstance(analysis_setup, HarmonicAnalysisSetup):
        new_analysis_setup = analysis_setup.convert_to(
            HarmonicAnalysisSetupList,
            all_frequencies=frequencies,
        )
    else:
        new_analysis_setup = HarmonicAnalysisSetupList(frequencies)

    app().new_project.configure_analysis(
        app().new_project.model.analysis_id,
        new_analysis_setup,
    )


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
        filter=_filter,
    )

    if not extension:
        return

    app().config.write_last_folder_path_in_file("exported_table_folder", export_path)

    if physical_domain == "acoustic":
        complex_natural_frequencies = app().new_project.solver.complex_natural_frequencies
    else:
        complex_natural_frequencies = app().new_project.solver.complex_natural_frequencies

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
        np.savetxt(export_path, modal_data_to_export, fmt=fmt, delimiter=",", header=header)

    else:
        from pandas import ExcelWriter
        from polars import DataFrame

        with ExcelWriter(export_path) as writer:
            header = header.split(",")
            df = DataFrame(modal_data_to_export, schema=header)
            df.to_pandas().to_excel(writer, sheet_name="Exported modal results", index=False)
