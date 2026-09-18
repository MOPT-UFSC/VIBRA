import logging
from copy import deepcopy
from enum import IntEnum
from numbers import Number
from pathlib import Path
from typing import Literal

import numpy as np
from PySide6.QtWidgets import QDialog, QFileDialog, QLineEdit, QPushButton, QWidget

from vibra import app
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.solution import ModalSolution
from vibra.interface import error_title, warning_title
from vibra.interface.data.data_manager import is_frequencies_vector_equally_distributed
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.model_inputs.general.mesher_setup_inputs import MesherSetupInputs
from vibra.utils.subprocess.subprocess_handler import SubProcessHandler, SubProcessStatus


class InputDataType(IntEnum):
    REAL_IMAGINARY = 0
    MAGNITUDE_PHASE = 1


def check_input_entries(input_left: str, input_right: str, label: str):

    value_left = None
    if input_left != "":
        try:
            input_left = input_left.replace(",", ".")
            value_left = float(input_left)

        except Exception:
            title = f"Invalid entry to the {label}"
            message = f"Wrong input for real part of {label}."
            PrintMessageInput([error_title, title, message])
            return

    value_right = None
    if input_right != "":
        try:
            input_right = input_right.replace(",", ".")
            value_right = float(input_right)

        except Exception:
            title = f"Invalid entry to the {label}"
            message = f"Wrong input for imaginary part of {label}."
            PrintMessageInput([error_title, title, message])
            return

    if value_left is None and isinstance(value_right, Number):
        value_left = 0.0

    if value_right is None and isinstance(value_left, Number):
        value_right = 0.0

    output = [value_left, value_right] 

    return output


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

            if "table_names" in data:
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

            if "table_names" in data:
                return

    # No idea of what it does
    app().project.configure_analysis(app().project.model.analysis_setup)


def check_mesh_related_issues(run_analysis_button: QPushButton):

    # disable run_analysis button if there are disconnected nodes or collapsed elements
    mesh = app().project.model.mesh
    assert mesh is not None

    disconnected_nodes = bool(mesh.disconnected_nodes)
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


def generate_mesh_and_finalize() -> bool:
    """
    Generate the mesh from the current mesh setup and finalize
    the interface state afterwards. Returns True on success.
    """

    def _load_mesh_from_working_dir():
        logging.info("Loading generated mesh... [10/100]")
        app().project.model.mesh = app().project.project_reader.read_mesh()

        logging.info("Reading model properties... [65/100]")
        app().project.model.properties = app().project.project_reader.read_model_properties()

        logging.info("Updating project state... [85/100]")
        app().project.reset_solution()
        app().project.mark_project_as_modified()

    def _generate_in_process():
        mesh_setup = app().project.model.mesh_setup
        app().project.generate_mesh(mesh_setup)

    def _finalize():
        logging.info("Updating render... [95/100]")
        app().main_window.action_mesh_workspace_callback()
        app().main_window.update_plots()
        app().main_window.analysis_toolbar.reset_solution_action.setDisabled(True)
        app().main_window.analysis_toolbar.check_analysis_setup_callback()
        app().main_window.action_export_element_transfer_data.setDisabled(True)

    if app().config.user_preferences.generate_mesh_in_subprocess:
        app().project.write_to_working_dir()

        command = f"{SubProcessHandler.get_executable()} --generate-mesh {app().project.working_directory!s}"
        status = SubProcessHandler(command).run()
        if status != SubProcessStatus.SUCCESS:
            return False

        LoadingWindow(_load_mesh_from_working_dir).run()

    else:
        LoadingWindow(_generate_in_process).run()

    LoadingWindow(_finalize).run()

    prompt_if_disconnected_nodes()

    return True


def prompt_if_disconnected_nodes():
    mesh = app().project.model.mesh
    if mesh is None or not mesh.disconnected_nodes:
        return

    confirmation = GetUserConfirmationInput(
        "Disconnected nodes detected",
        "The generated mesh contains disconnected nodes.\n"
        + "The model solution will stay deactivated until this is addressed.\n\n"
        + "Choose an option:\n"
        + "\"Go to Mesh Setup\" to adjust the mesh parameters and regenerate\n"
        + "the mesh to try to solve the problem.\n"
        + "\"Remove disconnected nodes\" to forcibly delete them from the\n"
        + "current mesh and keep using it as is.",
        buttons_config={
            "left_button_label": "Go to Mesh Setup",
            "right_button_label": "Remove disconnected nodes",
            "left_button_size": 160,
            "right_button_size": 230,
        },
    )

    # right button = remove the disconnected nodes
    if confirmation._continue:
        mesh.remove_disconnected_nodes()
        mesh.process_disconnected_nodes_criterion(print_log=True)
        app().main_window.update_plots()
        return

    # left button = open mesh setup
    app().main_window.input_ui.mesh_setup()


def process_decoupling_actions():

    def callback():
        logging.info("Processing degress of freedom decoupling... [10/100]")
        app().project.model.process_degrees_of_freedom_decoupling()

        logging.info("Processing degress of freedom decoupling... [70/100]")
        app().project.write_to_working_dir()

        # the degrees of freedom modifies the surfaces properties
        logging.info("Processing degress of freedom decoupling... [80/100]")
        app().project.update_model_properties_file()

        logging.info("Processing degress of freedom decoupling... [85/100]")
        app().main_window.update_mesh_information()

        logging.info("Processing degress of freedom decoupling... [90/100]")
        app().main_window.update_geometry_information()

        logging.info("Processing degress of freedom decoupling... [92/100]")
        app().project.model.mesh.process_disconnected_nodes_criterion()

        logging.info("Processing degress of freedom decoupling... [95/100]")
        app().main_window.update_plots()

    LoadingWindow(callback).run()


def remove_all_properties_assigned_to_new_surfaces(new_surface_ids: list[int], remove_adjacencies: bool = True):
    if not new_surface_ids:
        return

    model = app().project.model
    surface_properties = deepcopy(model.properties.surface_properties)
    line_properties = deepcopy(model.properties.line_properties)
    point_properties = deepcopy(model.properties.point_properties)

    for new_surface_id in new_surface_ids:
        for (property, surf_id) in surface_properties:
            if surf_id != new_surface_id:
                continue

            model.properties._remove_surface_property(property, surf_id)

        if not remove_adjacencies:
            continue

        for line_from_surface in model.mesh.lines_from_surface.get(new_surface_id, []):
            for (property, line_id) in line_properties:
                if line_from_surface != line_id:
                    continue

                model.properties._remove_line_property(property, line_id)
                for point_from_line in model.mesh.points_from_line.get(line_from_surface, []):
                    for (property, point_id) in point_properties:
                        if point_from_line != point_id:
                            continue

                        model.properties._remove_point_property(property, point_id)


def restore_mesh_data_modified_by_decoupling():

    mesh = app().project.model.mesh
    if mesh.cache_nodal_coordinates is None:
        return

    mesh.restore_data_from_cache()
    mesh.process_upwards_adjacencies_from_entities()

    # if self.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):
    #     self.mesh.cache_mesh_information()

    process_decoupling_actions()


def check_conflicting_model_properties(volume_ids: list[int], domain: str):
    """
    Use this function to map and remove the model properties that will 
    cause conflicts if the domain is changed.

    Parameters
    ----------
    volume_ids: list
        A list of volume IDs where the domain should be modified.

    domain: str
        The domain label (acoustic or structural)

    """

    model = app().project.model
    if not model.domains_processor.is_there_a_property_assigned_to_a_domain(domain, volume_ids):
        return False

    is_acoustic = domain == "acoustic"
    if is_acoustic:
        text = ["material", "fluid"]
    else:
        text = ["fluid", "material"]

    title = "Conflicting properties detected"
    message = f"You're trying to assign a {text[0]} to a volume that already has a {text[1]} assigned. "
    message += f"Would you like to proceed with {text[0]} assignment and remove all the "
    message += f"{domain}-related properties?"

    buttons_config = {"left_button_label": "Cancel", "right_button_label": "Continue"}
    obj = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

    if obj._cancel:
        return True

    existing_properties = model.domains_processor.get_properties_assigned_to_a_domain(domain, volume_ids)
    if not existing_properties:
        return False

    surfaces_with_decoupling = []
    properties = app().project.model.properties

    for (prop_name, entity_name, entity_id) in existing_properties:
        if is_acoustic and prop_name in ["perforated_plate_model", "transfer_impedance"]:
            surfaces_with_decoupling.append(entity_id)

        match entity_name:
            case "volume":
                properties._remove_volume_property(prop_name, volume_id=entity_id)
            case "surface":
                properties._remove_surface_property(prop_name, surface_id=entity_id)
            case "line":
                properties._remove_line_property(prop_name, line_id=entity_id)
            case "point":
                properties._remove_point_property(prop_name, point_id=entity_id)
            case "node":
                properties._remove_nodal_property(prop_name, node_id=entity_id)

    if not surfaces_with_decoupling:
        return False

    new_surface_ids = []
    for surf_id in surfaces_with_decoupling:
        data = properties._get_property("degrees_of_freedom_decoupling", surface=surf_id)
        if isinstance(data, dict):
            new_surface_id = data.get("new_surface_id")
            if isinstance(new_surface_id, int):
                new_surface_ids.append(new_surface_id)

            properties._remove_surface_property("degrees_of_freedom_decoupling", surf_id)

    remove_all_properties_assigned_to_new_surfaces(new_surface_ids)
    restore_mesh_data_modified_by_decoupling()


def export_modal_analysis_results(parent: QDialog | QWidget, modes_to_frequencies: dict, physical_domain: str):

    solution = app().project.model.solution
    if not isinstance(solution, ModalSolution):
        return

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

    if isinstance(solution.complex_natural_frequencies, np.ndarray):
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


def update_entities_selection(line_edit: QLineEdit, selection_label: str, selected_ids: list[int]):
    input_ids = line_edit.text()
    tokens = input_ids.replace(" ", "").split(",")
    list_ids = [int(_id) for _id in tokens]

    volumes = surfaces = lines = points = nodes = None

    match selection_label:
        case "volumes":
            volumes = selected_ids
        case "surfaces":
            surfaces = selected_ids
        case "lines":
            lines = selected_ids
        case "points":
            points = selected_ids
        case "nodes":
            nodes = selected_ids

    if len(list_ids) == len(selected_ids):
        return

    line_edit.setText(", ".join(map(str, selected_ids)))

    if selection_label == "nodes":
        app().main_window.selection.set_mesh_selection(nodes=nodes)

    else:
        app().main_window.selection.set_geometry_selection(
            volumes=volumes,
            surfaces=surfaces,
            lines=lines,
            points=points,
            )
