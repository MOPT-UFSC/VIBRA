from pathlib import Path
from typing import Literal
from enum import IntEnum

import numpy as np
from PySide6.QtWidgets import QDialog, QFileDialog, QPushButton, QWidget

from vibra import app
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.interface import error_title, warning_title
from vibra.interface.data.data_manager import is_frequencies_vector_equally_distributed
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.model_inputs.general.mesher_setup_inputs import MesherSetupInputs


class InputType(IntEnum):
    REAL_IMAGINARY = 0
    MAGNITUDE_PHASE = 1


def save_table_values(table_name: str, imported_values: np.ndarray, physical_domain: Literal["acoustic", "structural"]):
    
    # define the frequencies vector
    frequencies = imported_values[:, 0]

    if app().project.model.change_analysis_frequency_setup(list(frequencies)):
        app().main_window.hide_dialogs()
        title = "Project frequency setup cannot be modified"
        message = "The following imported table of values has a frequency setup "
        message += "different from the others already imported ones. The current "
        message += "project frequency setup is not going to be modified."
        message += f"\n\n{table_name}"
        PrintMessageInput([error_title, title, message])
        return True

    update_analysis_setup_in_file(frequencies)

    # real values vector
    real_values = imported_values[:, 1]
    
    # imaginary values vector
    imag_values = imported_values[:, 2]

    data = np.array([frequencies, real_values, imag_values], dtype=float).T

    app().project.model.properties.add_imported_tables(physical_domain, table_name, data)

    return False

def filter_outside_surfaces(surface_ids: list[int], bc_label: str) -> tuple[list[int], list[int]]:

    inside_surfaces = list()
    outside_surfaces = list()
    for surf_id in surface_ids:
        volume_ids = app().project.model.mesh.volumes_from_surface.get(surf_id)
        if len(volume_ids) == 1:
            outside_surfaces.append(surf_id)
        elif len(volume_ids) > 1:
            inside_surfaces.append(surf_id)

    if inside_surfaces:
        app().main_window.hide_dialogs()
        title = "Inside surfaces selected"
        message = "At least one inside surface has been detected in the current selection. "
        message += f"However, only the external surfaces are allowed for {bc_label} "
        message += "boundary condition. The inside surfaces will be ignored."
        PrintMessageInput([warning_title, title, message])

    return (outside_surfaces, inside_surfaces)

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

def check_acoustic_model_frequency_controls():

    properties = app().project.model.properties

    model_properties = [
        properties.surface_properties,
        properties.point_properties,
        properties.nodal_properties,
    ]

    prop_labels = [
        "acoustic_pressure",
        "surface_velocity",
        "mass_source",
        "specific_impedance",
        "absorption_surface",
        "transfer_impedance",
        "perforated_plate",
        "reciprocating_compressor_excitation",
        "compressor_excitation_waveform",
        "compressor_excitation_spectrum",
    ]

    for model_property in model_properties:
        for (property, *_), data in model_property.items():
            if property not in prop_labels:
                continue

            if "table_names" in data.keys():
                return

    # No idea of what it does
    app().project.configure_analysis(app().project.model.analysis_setup)

def check_structural_model_frequency_controls():

    properties = app().project.model.properties

    model_properties = [
        properties.surface_properties,
        properties.point_properties,
        properties.nodal_properties,
    ]

    prop_labels = [
        "prescribed_dof",
        "nodal_loads",
        "distributed_loads",
        "normal_pressure_loads",
    ]

    for model_property in model_properties:
        for (property, *_), data in model_property.items():
            if property not in prop_labels:
                continue

            if "table_names" in data.keys():
                return

    # No idea of what it does
    app().project.configure_analysis(app().project.model.analysis_setup)

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