from functools import cache

import numpy as np

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from vibra.engine.solvers import StructuralModalSolver, StructuralHarmonicSolver

DisplacementTypes = Literal["u_sum", "u_x", "u_y", "u_z"]


class StructuralPostprocessing:
    def __init__(self, solver: "StructuralModalSolver|StructuralHarmonicSolver"):
        self.solver = solver

    @cache
    def get_max_min_values_of_displacements(self, column: int, disp_type: str):
        """ This method returns the minimum and maximum displacement values
            of selected frequency for animation purposes.

            Parameters:
            -----------
            column: int value relative to frequency column index.

            Returns:
            -----------
            u_min, u_max: float values for minimum and maximum displacements,

        """

        data = self.solver.solution[self.solver.displacement_dofs, column]

        amplitudes = np.abs(data)
        phases = np.angle(data)

        r_min = 1
        r_max = 0
        thetas = np.arange(0, 360, 2) * (np.pi / 180)

        for theta in thetas:

            results = (amplitudes * np.cos(phases + theta)).reshape(-1, 3)

            if disp_type == "u_x":
                u_xyz = results * np.array([1.0, 0.0, 0.0])
            elif disp_type == "u_y":
                u_xyz = results * np.array([0.0, 1.0, 0.0])
            elif disp_type == "u_z":
                u_xyz = results * np.array([0.0, 0.0, 1.0])
            else:
                u_xyz = np.linalg.norm(results, axis=1)

            r_min_i = np.min(u_xyz)
            if r_min_i < r_min:
                r_min = r_min_i

            r_max_i = np.max(u_xyz)
            if r_max_i > r_max:
                r_max = r_max_i

        # print("get_max_min_values_of_displacements", r_min, r_max)

        if disp_type == "u_sum":
            return 0., r_max

        else:

            if np.abs(r_min) != np.abs(r_max):
                max_abs = np.max(np.abs([r_min, r_max]))
                r_min = -max_abs
                r_max = max_abs

        return r_min, r_max


class ModalStructuralPostprocessing(StructuralPostprocessing):
    def __init__(self, solver: "StructuralModalSolver"):
        super().__init__(solver)

    def compute_structural_modal_field(
        self,
        index: int,
        phase_rad: float,
        displacement_type: DisplacementTypes,
    ):
        if self.solver.solution is None:
            return

        disp_dofs = self.solver.displacement_dofs
        results_complex: np.ndarray = self.solver.solution[disp_dofs, index]

        amplitudes = np.abs(results_complex)
        phases = np.angle(results_complex)
        delta = -phases[np.argmax(amplitudes)]
        results_real = amplitudes * np.cos(phases + phase_rad + delta)

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

        min_value, max_value = self.solver.get_max_min_values_of_displacements(index, displacement_type)

        return displacements, color_scalars, min_value, max_value, np.imag(displacements).any()


class HarmonicStructuralPostprocessing(StructuralPostprocessing):
    def __init__(self, solver: "StructuralHarmonicSolver"):
        super().__init__(solver)

    def compute_structural_harmonic_field(
        self,
        index: int,
        phase_rad: float,
        displacement_type: DisplacementTypes,
    ):
        if self.solver.solution is None:
            return

        disp_dofs = self.solver.displacement_dofs
        results_complex: np.ndarray = self.solver.solution[disp_dofs, index]

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

        min_value, max_value = self.get_max_min_values_of_displacements(index, displacement_type)

        return displacements, color_scalars, min_value, max_value, np.imag(displacements).any()
