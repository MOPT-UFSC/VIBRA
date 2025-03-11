import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.solvers import AcousticHarmonicSolver, AcousticModalSolver


def compute_acoustic_modal_field(
    solver: "AcousticModalSolver",
    index: int,
    phase: float,
    response_abs: bool = False,
    response_real: bool = False,
):
    color_scalars = solver.modal_shape[:, index]

    if response_abs:
        color_scalars = np.abs(color_scalars)
    color_scalars /= np.max(np.abs(color_scalars))

    min_value = np.min(color_scalars)
    max_value = np.max(color_scalars)

    if response_real:
        if np.abs(min_value) != np.abs(max_value):
            min_value = -np.max(np.abs([min_value, max_value]))
            max_value = np.max(np.abs([min_value, max_value]))

    color_scalars *= np.cos(phase * np.pi / 180)
    if response_abs:
        color_scalars = np.abs(color_scalars)
    
    return color_scalars, min_value, max_value

def compute_acoustic_harmonic_field(
    solver: "AcousticHarmonicSolver",
    index: int,
    phase: float,
    response_abs: bool = False,
):
    current_pressures = solver.solution[:, index].copy()
    amplitudes = np.abs(current_pressures)
    phases = np.angle(current_pressures)
    output_pressures = amplitudes * np.cos(phases + phase)

    min_value, max_value = solver.get_min_max_values_of_pressures(index)
    if response_abs:
        min_value = 0
        output_pressures = np.abs(output_pressures)

    return output_pressures, min_value, max_value