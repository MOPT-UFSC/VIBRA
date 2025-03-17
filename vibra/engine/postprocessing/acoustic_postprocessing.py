import numpy as np

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from vibra.engine.solvers import AcousticHarmonicSolver, AcousticModalSolver

ModalAcousticPlotTypes = Literal[
    "absolute_animation",
    "non_absolute_animation",
    "absolute_values",
    "real_values",
    "imag_values",
]


def compute_acoustic_modal_field(
    solver: "AcousticModalSolver",
    index: int,
    phase_deg: float,
    plot_type: ModalAcousticPlotTypes,
):
    selected_mode_shape = solver.modal_shapes[:, index]
    phase_rad = phase_deg * np.pi / 180

    pressures = np.abs(selected_mode_shape)
    phases = np.angle(selected_mode_shape)

    acoustic_pressures = pressures * np.cos(phases + phase_rad)
    if plot_type == "absolute_values":
        acoustic_pressures = np.abs(selected_mode_shape)
    elif plot_type == "real_values":
        acoustic_pressures = np.real(selected_mode_shape)
    elif plot_type == "imag_values":
        acoustic_pressures = np.imag(selected_mode_shape)
    elif plot_type == "absolute_animation":
        acoustic_pressures = np.abs(acoustic_pressures)

    min_value, max_value = get_min_max_values_of_pressures(selected_mode_shape, plot_type)

    return acoustic_pressures, min_value, max_value

def compute_acoustic_harmonic_field(
    solver: "AcousticHarmonicSolver",
    index: int,
    phase_deg: float,
    response_abs: bool = False,
):
    current_pressures = solver.solution[:, index].copy()
    amplitudes = np.abs(current_pressures)
    phases = np.angle(current_pressures)
    phase_rad = phase_deg * np.pi / 180
    output_pressures = amplitudes * np.cos(phases + phase_rad)

    min_value, max_value = solver.get_min_max_values_of_pressures(index)
    if response_abs:
        min_value = 0
        output_pressures = np.abs(output_pressures)

    return output_pressures, min_value, max_value


def get_min_max_values_of_pressures(data: np.ndarray, plot_type: str):
    _pressures = np.abs(data)
    _phases = np.angle(data)

    p_min = 1
    p_max = 0

    divisions = 36
    thetas = np.linspace(0, 2 * np.pi, divisions + 1, endpoint=True)

    if plot_type == "absolute_values":
        return 0, max(np.abs(data))

    if plot_type == "real_values":
        return min(np.real(data)), max(np.real(data))

    if plot_type == "imag_values":
        return min(np.imag(data)), max(np.imag(data))

    for theta in thetas:
        pressures = _pressures * np.cos(theta + _phases)

        if plot_type == "absolute_animation":
            pressures = np.abs(pressures)

        p_min_i = min(pressures)
        p_max_i = max(pressures)

        if p_min_i < p_min:
            p_min = p_min_i
        if p_max_i > p_max:
            p_max = p_max_i

    if plot_type == "absolute_animation":
        p_min = 0

    if plot_type == "non_absolute_animation":
        max_value = np.max(np.abs([p_min, p_max]))
        p_min = -max_value
        p_max = max_value

    return p_min, p_max
