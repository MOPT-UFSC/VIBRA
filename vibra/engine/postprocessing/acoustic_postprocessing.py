import numpy as np

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from vibra.engine.solvers import AcousticHarmonicSolver, AcousticModalSolver

AcousticPlotTypes = Literal[
    "absolute_animation",
    "non_absolute_animation",
    "absolute_values",
    "real_values",
    "imag_values",
]


def compute_acoustic_modal_field(
    solver: "AcousticModalSolver",
    index: int,
    phase_rad: float,
    plot_type: AcousticPlotTypes,
):

    if solver.solution is None:
        return None

    selected_mode_shape = solver.solution[:, index]
    amplitudes = np.abs(selected_mode_shape)
    phases = np.angle(selected_mode_shape)

    acoustic_pressures = amplitudes * np.cos(phases + phase_rad)
    if plot_type == "absolute_values":
        acoustic_pressures = np.abs(selected_mode_shape)
    elif plot_type == "real_values":
        acoustic_pressures = np.real(selected_mode_shape)
    elif plot_type == "imag_values":
        acoustic_pressures = np.imag(selected_mode_shape)
    elif plot_type == "absolute_animation":
        acoustic_pressures = np.abs(acoustic_pressures)

    min_value, max_value = solver.get_min_max_values_of_pressures(index, plot_type)

    return acoustic_pressures, min_value, max_value


def compute_acoustic_harmonic_field(
    solver: "AcousticHarmonicSolver",
    index: int,
    phase_rad: float,
    plot_type: AcousticPlotTypes,
):
    
    if solver.solution is None:
        return None

    selected_results = solver.solution[:, index]
    amplitudes = np.abs(selected_results)
    phases = np.angle(selected_results)
    acoustic_pressures = amplitudes * np.cos(phases + phase_rad)

    if plot_type == "absolute_values":
        acoustic_pressures = np.abs(selected_results)
    elif plot_type == "real_values":
        acoustic_pressures = np.real(selected_results)
    elif plot_type == "imag_values":
        acoustic_pressures = np.imag(selected_results)
    elif plot_type == "absolute_animation":
        acoustic_pressures = np.abs(acoustic_pressures)

    min_value, max_value = solver.get_min_max_values_of_pressures(index, plot_type)

    return acoustic_pressures, min_value, max_value