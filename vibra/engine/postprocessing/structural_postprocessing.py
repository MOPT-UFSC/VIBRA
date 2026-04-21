from __future__ import annotations

from functools import cache
from typing import TYPE_CHECKING, Literal

import numpy as np

if TYPE_CHECKING:
    from vibra.engine.project import Project

from vibra.engine.solvers import HarmonicSolver, ModalSolver

DisplacementTypes = Literal["u_sum", "u_x", "u_y", "u_z"]


class StructuralPostprocessing:
    def __init__(
        self,
        project: Project = None,
        structural_modal_solver: ModalSolver = None,
        structural_harmonic_solver: HarmonicSolver = None,
    ):
        if all(v is None for v in [project, structural_modal_solver, structural_harmonic_solver]):
            raise ValueError("At least one of 'project', 'structural_modal_solver', or 'structural_harmonic_solver' must be provided.")
        self.project = project
        self.structural_harmonic_solver = structural_harmonic_solver
        self.structural_modal_solver = structural_modal_solver

    @property
    def harmonic_solver(self):
        if (self.project is not None) and isinstance(self.project.solver, HarmonicSolver):
            return self.project.solver
        return self.structural_harmonic_solver

    @property
    def modal_solver(self):
        if (self.project is not None) and isinstance(self.project.solver, ModalSolver):
            return self.project.solver
        return self.structural_modal_solver

    @property
    def current_solver(self):
        if isinstance(self.structural_modal_solver, ModalSolver):
            return self.structural_modal_solver

        if isinstance(self.structural_harmonic_solver, HarmonicSolver):
            return self.structural_harmonic_solver

    @property
    def model(self):
        if (self.project is not None) and isinstance(self.project.solver, HarmonicSolver | ModalSolver):
            return self.project.model
        else:
            solver = self.current_solver
            return solver.assembler.model

    @property
    def mesh(self):
        if (self.project is not None) and isinstance(self.project.solver, HarmonicSolver | ModalSolver):
            return self.project.model.mesh
        else:
            solver = self.current_solver
            return solver.assembler.model.mesh

    @property
    def solution(self):
        if (self.project is not None) and isinstance(self.project.solver, HarmonicSolver | ModalSolver):
            return self.project.model.solution
        else:
            solver = self.current_solver
            return solver.solution


    @cache
    def get_max_min_values_of_displacements(self, column: int, disp_type: str, is_modal: bool = False):
        """This method returns the minimum and maximum displacement values
        of selected frequency for animation purposes.

        Parameters:
        -----------
        column: int value relative to frequency column index.

        Returns:
        -----------
        u_min, u_max: float values for minimum and maximum displacements,

        """

        if is_modal:
            solver = self.modal_solver
            nodal_solution = self.solution.modal_shape
        else:
            solver = self.harmonic_solver
            nodal_solution = self.solution.nodal_solution

        if not nodal_solution.any():
            return

        data = nodal_solution[solver.displacement_dof, column]

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
            return 0.0, r_max

        else:
            if np.abs(r_min) != np.abs(r_max):
                max_abs = np.max(np.abs([r_min, r_max]))
                r_min = -max_abs
                r_max = max_abs

        return r_min, r_max

    def compute_structural_displacement_field(self, index: int, phase_rad: float, displacement_type: DisplacementTypes, is_modal: bool = False):

        if is_modal:
            solver = self.modal_solver
            nodal_solution = self.solution.modal_shape
        else:
            solver = self.harmonic_solver
            nodal_solution = self.solution.nodal_solution

        if not nodal_solution.any():
            return

        results_complex: np.ndarray = solver.solution[solver.displacement_dof, index]

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

        min_value, max_value = self.get_max_min_values_of_displacements(index, displacement_type, is_modal)

        return displacements, color_scalars, min_value, max_value, np.imag(displacements).any()
