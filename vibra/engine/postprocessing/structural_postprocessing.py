import numpy as np

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from vibra.engine.solvers import StructuralModalSolver, StructuralHarmonicSolver

DisplacementTypes = Literal["u_sum", "u_x", "u_y", "u_z"]


def compute_structural_modal_field(
    solver: "StructuralModalSolver",
    index: int,
    phase_rad: float,
    displacement_type: DisplacementTypes,
):
    if solver.solution is None:
        return

    disp_dofs = solver.displacement_dofs
    results_complex: np.ndarray = solver.solution[disp_dofs, index]

    amplitudes = np.abs(results_complex)
    phases = np.angle(results_complex)
    results_real = amplitudes * np.cos(phases + phase_rad)

    current_solution = results_real.reshape(-1, 3).copy()
    if displacement_type == "u_sum":
        color_scalars = np.linalg.norm(current_solution, axis=1)
        displacements = current_solution.copy()

    elif displacement_type == "u_x":
        color_scalars = current_solution[:, 0]
        displacements = current_solution * np.array([1.0, 0.0, 0.0])

    elif displacement_type == "u_y":
        color_scalars = current_solution[:, 1]
        displacements = current_solution * np.array([0.0, 1.0, 0.0])

    elif displacement_type == "u_z":
        color_scalars = current_solution[:, 2]
        displacements = current_solution * np.array([0.0, 0.0, 1.0])

    min_value, max_value = solver.get_max_min_values_of_displacements(index, displacement_type)

    return displacements, color_scalars, min_value, max_value


def compute_structural_harmonic_field(
    solver: "StructuralHarmonicSolver",
    index: int,
    phase_rad: float,
    displacement_type: DisplacementTypes,
):
    if solver.solution is None:
        return

    disp_dofs = solver.displacement_dofs
    results_complex: np.ndarray = solver.solution[disp_dofs, index]

    amplitudes = np.abs(results_complex)
    phases = np.angle(results_complex)

    results_real = amplitudes * np.cos(phases + phase_rad)
    current_solution = results_real.reshape(-1, 3).copy()

    if displacement_type == "u_sum":
        color_scalars = np.linalg.norm(current_solution, axis=1)
        displacements = current_solution.copy()

    elif displacement_type == "u_x":
        color_scalars = current_solution[:, 0]
        displacements = current_solution * np.array([1.0, 0.0, 0.0])

    elif displacement_type == "u_y":
        color_scalars = current_solution[:, 1]
        displacements = current_solution * np.array([0.0, 1.0, 0.0])

    elif displacement_type == "u_z":
        color_scalars = current_solution[:, 2]
        displacements = current_solution * np.array([0.0, 0.0, 1.0])

    min_value, max_value = solver.get_max_min_values_of_displacements(index, displacement_type)

    return displacements, color_scalars, min_value, max_value
