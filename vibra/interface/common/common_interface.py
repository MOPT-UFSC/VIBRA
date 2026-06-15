from pathlib import Path

import numpy as np
from PySide6.QtWidgets import QDialog, QFileDialog, QPushButton, QWidget

from vibra import app
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.interface.data.data_manager import is_frequencies_vector_equally_distributed
from vibra.interface.model_inputs.general.mesher_setup_inputs import MesherSetupInputs


def update_analysis_setup_in_file(frequencies: np.ndarray):

    equally_distributed = is_frequencies_vector_equally_distributed(frequencies)

    if equally_distributed:
        frequency_spacing = FrequencySpacing.EQUALLY_DISTRIBUTED
        f_min = frequencies[0]
        f_max = frequencies[-1]
        f_step = frequencies[1] - frequencies[0]
        frequencies = None

    else:
        f_min = f_max = f_step = None
        frequency_spacing = FrequencySpacing.USER_DEFINED
        frequencies = frequencies

    # transfer the analysis id to the
    analysis_id = app().project.model.analysis_id
    if analysis_id == AnalysisID.NO_ANALYSIS:
        analysis_id = app().main_window.analysis_toolbar.get_current_analysis_id()

    analysis_setup = app().project.model.get_harmonic_analysis_setup(
        analysis_id=analysis_id,
        frequency_spacing=frequency_spacing,
        f_min=f_min,
        f_max=f_max,
        f_step=f_step,
        frequencies=frequencies,
    )

    app().project.configure_analysis(analysis_setup)

def check_mesh_related_issues(run_analysis_button: QPushButton):

    # disable run_analysis button if there are disconnected nodes or collapsed elements
    mesh = app().project.model.mesh
    disconnected_nodes = bool(mesh.disconnected_nodes_data)
    collapsed_elements = bool(mesh.collapsed_elements_data)
    problematic_mesh = collapsed_elements or disconnected_nodes

    text = ""
    if collapsed_elements:
        text = "Collapsed elements have been detected during the mesh post-processing. \n"
        text += "The model solution will stay deactivated until the collapsed-related \n"
        text += "issues have been addressed."

    if disconnected_nodes:
        text += "Disconnected nodes have been detected during the mesh post-processing. \n"
        text += "The model solution will stay deactivated until the meshing-related issues \n"
        text += "have been addressed."

    run_analysis_button.setToolTip(text)
    run_analysis_button.setDisabled(problematic_mesh)

    analysis_toolbar = app().main_window.analysis_toolbar
    analysis_toolbar.run_analysis_action.setToolTip(text)
    analysis_toolbar.run_analysis_action.setDisabled(problematic_mesh)

    # interrupt the code execution if any mesh-related issue has been detected
    if problematic_mesh:
        return

    valid_analysis_setup = analysis_toolbar.is_analysis_setup_valid()
    analysis_toolbar.run_analysis_action.setEnabled(valid_analysis_setup)

def mesher_interface_callback(parent: QDialog, close_after_generate: bool = False):
    parent.hide()
    obj = MesherSetupInputs(close_after_generate=close_after_generate)
    if not obj.complete:
        app().main_window.set_input_widget(parent)
        return True

    app().main_window.update_plots()

def export_modal_analysis_results(parent: QDialog | QWidget, modes_to_frequencies: dict, physical_domain: str):

    last_path = app().config.get_last_folder_for("exported_table_folder")
    if last_path is None:
        last_path = str(Path().home())

    caption = "Export the modal analysis results"
    _filter = "Spreadsheet (*.xlsx);; Spreadsheet (*.xls);; Text file (*.dat);; Text file (*.txt);; Text file (*.csv)"

    export_path, extension = QFileDialog.getSaveFileName(
        parent,
        caption,
        str(last_path),
        filter=_filter,
    )

    if not extension:
        return

    app().config.write_last_folder_path_in_file("exported_table_folder", export_path)

    if physical_domain == "acoustic":
        complex_natural_frequencies = app().project.solver.complex_natural_frequencies
    else:
        complex_natural_frequencies = app().project.solver.complex_natural_frequencies

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