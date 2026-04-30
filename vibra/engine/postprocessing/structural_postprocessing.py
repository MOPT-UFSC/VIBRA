from __future__ import annotations

from functools import cache
from typing import Literal

import numpy as np

from vibra.engine.model import Model
from vibra.engine.solution import HarmonicSolution, LazyHarmonicSolution, ModalSolution

DisplacementTypes = Literal["u_sum", "u_x", "u_y", "u_z"]


class StructuralPostprocessing:
    def __init__(self, model: Model):
        if not isinstance(model, Model):
            raise ValueError("The model argument must be of type Model.")

        self.model = model

    @property
    def mesh(self):
        return self.model.mesh

    @property
    def solution(self):
        return self.model.solution

    @property
    def acoustic_element_2d(self):
        if self.model.acoustic_element_2d is None:
            self.model.set_acoustic_elements()
        return self.model.acoustic_element_2d

    @property
    def acoustic_element_3d(self):
        if self.model.acoustic_element_3d is None:
            self.model.set_acoustic_elements()
        return self.model.acoustic_element_3d

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
        if not isinstance(self.solution, ModalSolution | HarmonicSolution):
            return

        if isinstance(self.solution, LazyHarmonicSolution) and not self.solution.is_valid():
            return

        data = self.solution.get_nodal_displacement_at_column(column)

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

    def compute_structural_displacement_field(
        self,
        column: int,
        phase_rad: float,
        displacement_type: DisplacementTypes,
        is_modal: bool = False,
    ):
        if not isinstance(self.solution, ModalSolution | HarmonicSolution):
            return

        if isinstance(self.solution, LazyHarmonicSolution) and not self.solution.is_valid():
            return

        displacements_complex = self.solution.get_nodal_displacement_at_column(column)

        amplitudes = np.abs(displacements_complex)
        phases = np.angle(displacements_complex)
        delta = -phases[np.argmax(amplitudes)]

        displacements = amplitudes * np.cos(phases + phase_rad + delta)
        current_solution = displacements.reshape(-1, 3).copy()

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

        min_value, max_value = self.get_max_min_values_of_displacements(column, displacement_type, is_modal)

        return displacements, color_scalars, min_value, max_value, np.imag(displacements).any()
