import numpy as np


def compute_structural_modal_field(
    modal_shape: np.ndarray,
    index: int,
    phase: float,
    update_coloring: bool = False,
    sum_response: bool = False,
    response_ux: bool = False,
    response_uy: bool = False,
    response_uz: bool = False,
):
    current_modal_shape = modal_shape[:, index].reshape(-1, 3).copy()

    if sum_response:
        values_1 = np.linalg.norm(current_modal_shape, axis=1).copy()
        displacements = current_modal_shape.copy()

    elif response_ux:
        values_1 = current_modal_shape[:, 0]
        displacements = current_modal_shape * np.array([1.0, 0.0, 0.0])

    elif response_uy:
        values_1 = current_modal_shape[:, 1]
        displacements = current_modal_shape * np.array([0.0, 1.0, 0.0])

    elif response_uz:
        values_1 = current_modal_shape[:, 2]
        displacements = current_modal_shape * np.array([0.0, 0.0, 1.0])

    max_abs = np.max(np.abs(values_1))
    values_1 /= max_abs

    min_value = round(min(values_1), 1)
    max_value = round(max(values_1), 1)

    if update_coloring:
        mod_values = displacements * np.cos(phase * np.pi / 180)

        if sum_response:
            values_2 = np.linalg.norm(mod_values, axis=1).copy()

        elif response_ux:
            values_2 = mod_values[:, 0]

        elif response_uy:
            values_2 = mod_values[:, 1]

        elif response_uz:
            values_2 = mod_values[:, 2]

        values_2 /= max_abs
        if not sum_response:
            if np.abs(min_value) != np.abs(max_value):
                min_value = -np.max(np.abs([min_value, max_value]))
                max_value = np.max(np.abs([min_value, max_value]))
    else:
        values_2 = values_1.copy()

    color_scalars = values_2

    return displacements, color_scalars, min_value, max_value
