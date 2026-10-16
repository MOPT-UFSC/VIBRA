
from __future__ import annotations

from functools import cache
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from vibra.engine.postprocessing import StructuralPostprocessing

from vibra.interface.viewer_3d.plot_setup import DisplacementDataType, StressDataType


class MinimumAndMaximumValuesProcessor:
    def __init__(self, post_processing: StructuralPostprocessing):

        self.post_processing = post_processing


    @property
    def model(self):
        return self.post_processing.model


    @property
    def solution(self):
        return self.post_processing.model.solution


    @property
    def nodal_solution_time(self):
        return self.post_processing.nodal_solution_time


    @property
    def nodal_averaged_stresses_frequency(self):
        return self.post_processing.nodal_averaged_stresses_frequency
    

    @property
    def nodal_averaged_stresses_time(self):
        return self.post_processing.nodal_averaged_stresses_time


    @cache
    def get_values_for_displacement_frequency(
        self,
        column: int,
        n_diff: int,
        unit_factor: float,
        data_type: DisplacementDataType,
        is_modal: bool,
        ) -> list[float, float]:
        """
        This method returns the minimum and maximum values of selected frequency for animation purposes.

        Parameters
        ----------
        column: int
            The column index of the nodal solution.

        n_diff: int
            The number of differentiations.

        unit_factor: float
            The unit conversion factor.

        data_type: str 
            A string that represents the displacement data type to be processed.

        Return
        ------
        r_min, r_max: float values for minimum and maximum displacements,

        """

        if is_modal:
            data_complex = self.solution.structural_modal_shapes[self.solution.displacement_dof, column]
        else:
            data_complex = self.solution.structural_solution[self.solution.displacement_dof, column]

        if self.model.analysis_id.is_harmonic():
            freq = self.model.frequencies[column]
            data_complex *= (1j * 2 * np.pi * freq)**n_diff

        divisions = 36
        thetas = np.linspace(0, 2 * np.pi, divisions + 1, endpoint=True).reshape(-1, 1, 1)

        data_complex = unit_factor * data_complex.reshape(-1, 3)

        # u_xyz_all = Re{data_complex * exp(1j * thetas)}
        u_xyz_all = data_complex.real * np.cos(thetas) - data_complex.imag * np.sin(thetas)

        if data_type in ["u_x", "v_x", "a_x"]:
            u_xyz = u_xyz_all[:, :, 0]
        elif data_type in ["u_y", "v_y", "a_y"]:
            u_xyz = u_xyz_all[:, :, 1]
        elif data_type in ["u_z", "v_z", "a_z"]:
            u_xyz = u_xyz_all[:, :, 2]
        else:
            u_xyz = np.linalg.norm(u_xyz_all, axis=2)

        r_min = np.min(u_xyz)
        r_max = np.max(u_xyz)

        if data_type in ["u_sum", "v_sum", "a_sum"]:
            return 0.0, np.max(np.abs([r_min, r_max]))

        if np.abs(r_min) != np.abs(r_max):
            max_abs = np.max(np.abs([r_min, r_max]))
            r_min = -max_abs
            r_max = max_abs

        return r_min, r_max


    @cache
    def get_values_for_displacement_time(
        self,
        N: float,
        unit_factor: float,
        data_type: str,
        ) -> tuple[float, float]:

        _nodal_solution = unit_factor * self.nodal_solution_time[:, :N]

        ux_dof = self.solution.displacement_dof[0::3]
        uy_dof = self.solution.displacement_dof[1::3]
        uz_dof = self.solution.displacement_dof[2::3]

        if data_type in ["u_x", "v_x", "a_x"]:
            u_xyz = _nodal_solution[ux_dof, :]
        elif data_type in ["u_y", "v_y", "a_y"]:
            u_xyz = _nodal_solution[uy_dof, :]
        elif data_type in ["u_z", "v_z", "a_z"]:
            u_xyz = _nodal_solution[uz_dof, :]
        else:
            u_xyz = np.sqrt(_nodal_solution[ux_dof, :]**2 + _nodal_solution[uy_dof, :]**2 + _nodal_solution[uz_dof, :]**2)

        u_xyz: np.ndarray

        return (u_xyz.min(), u_xyz.max())


    @cache
    def get_values_for_stress_frequency(
        self,
        column: int,
        unit_factor: float,
        stress_index: int,
        data_type: StressDataType,
        ) -> list[float, float]:
        """
        This method returns the minimum and maximum values of selected frequency for animation purposes.

        Parameters
        ----------
        column: int
            The column index of the nodal solution.

        unit_factor: float
            The unit conversion factor.

        data_type: str 
            A string that represents the stress data type to be processed.

        Return
        ------
        r_min, r_max: float values for minimum and maximum displacements,

        """

        # initialize the stress vector
        data_complex = unit_factor * self.nodal_averaged_stresses_frequency[:, stress_index, column].copy()

        if data_type == "absolute_values":
            return (0, max(np.abs(data_complex)))

        if data_type == "real_values":
            return (min(np.real(data_complex)), max(np.real(data_complex)))

        if data_type == "imag_values":
            return (min(np.imag(data_complex)), max(np.imag(data_complex)))

        divisions = 36
        thetas = np.linspace(0, 2 * np.pi, divisions + 1, endpoint=True)

        data_complex = data_complex.reshape(-1, 1)

        # stresses = Re{data_complex * exp(1j * thetas)}
        stresses = data_complex.real * np.cos(thetas) - data_complex.imag * np.sin(thetas)

        s_min = np.min(stresses.ravel())
        s_max = np.max(stresses.ravel())

        if data_type == "absolute_animation":
            s_min = 0
            s_max = max(s_max, abs(s_min))

        if data_type == "non_absolute_animation":
            max_value = np.max(np.abs([s_min, s_max]))
            s_min = -max_value
            s_max = max_value

        return s_min, s_max


    @cache
    def get_values_for_advanced_stress_frequency(
        self,
        data_complex: tuple,
        data_type: StressDataType,
        ) -> list[float, float]:
        """
        This method returns the minimum and maximum values of selected frequency for animation purposes.

        Parameters
        ----------
        data_complex: a tuple of complex values in which the phase sweep will be applied.

        data_type: a string that represents the stress data type to be processed.

        Return
        ------
        r_min, r_max: float values for minimum and maximum displacements,

        """

        if data_type == "absolute_values":
            return (0, max(np.abs(data_complex)))

        if data_type == "real_values":
            return (min(np.real(data_complex)), max(np.real(data_complex)))

        if data_type == "imag_values":
            return (min(np.imag(data_complex)), max(np.imag(data_complex)))

        divisions = 36
        thetas = np.linspace(0, 2 * np.pi, divisions + 1, endpoint=True)

        data_complex = np.array(data_complex).reshape(-1, 1)

        # stresses = Re{data_complex * exp(1j * thetas)}
        stresses = data_complex.real * np.cos(thetas) - data_complex.imag * np.sin(thetas)

        s_min = np.min(stresses.ravel())
        s_max = np.max(stresses.ravel())

        if data_type == "absolute_animation":
            s_min = 0
            s_max = np.max(np.abs([s_max, s_min]))

        if data_type == "non_absolute_animation":
            max_value = np.max(np.abs([s_min, s_max]))
            s_min = -max_value
            s_max = max_value

        return s_min, s_max


    @cache
    def get_values_for_stresses_time(
        self,
        N: float, 
        unit_factor: float,
        stress_index: int,
        data_type: StressDataType,
        ) -> tuple[float, float]:

        # initialize the stress vector and convert the units
        nodal_stresses = unit_factor * self.nodal_averaged_stresses_time[:, stress_index, :N].copy()

        if data_type == "absolute_animation":
            nodal_stresses = np.abs(nodal_stresses)
            min_value = 0
        else:
            min_value = nodal_stresses.min()

        max_value = nodal_stresses.max()

        return (min_value, max_value)