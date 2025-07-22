
from vibra.engine.solvers.linear_solver import initialize_solver, SolverType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.assemblers.structural_assembler import StructuralAssembler

import logging
import numpy as np

from scipy.sparse import triu
from functools import cache


class StructuralHarmonicSolver:
    def __init__(self, assembler: "StructuralAssembler", **kwargs):

        self.assembler = assembler
        self.reset_variables()

    def reset_variables(self):
        self.disp_dofs = None
        self.solution = None
        self.loads = None

        self.analysis_type = "structural"

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

        data = self.solution[self.displacement_dofs, column]

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

    def solve_direct_method(self, print_log=False):
        """ This method solves the structural harmonic analysis for both damped and undamped problems.
        """
        frequencies = self.assembler.model.frequencies
        self.get_max_min_values_of_displacements.cache_clear()

        self.unprescribed_dofs_indexes, self.prescribed_dofs_indexes = self.assembler.get_matrices_dropping_indexes()
        self.prescribed_dofs_values, self.array_prescribed_dofs_values = self.assembler.get_prescribed_dofs_values()

        M = self.assembler.mass_matrix
        K = self.assembler.stiffness_matrix

        global_damping = self.assembler.model.analysis_setup.get("global_damping", (0, 0, 0, 0))
        alpha_v, beta_v, alpha_h, beta_h = global_damping
        F_combined = self.get_prescribed_dofs_model_excitation()

        rows = K.shape[0]
        cols = len(frequencies)
        solution = np.zeros((rows, cols), dtype=complex)

        logging.info(f"Solving harmonic analysis... [0/{len(frequencies)}]")

        for i, freq in enumerate(frequencies):
            logging.info(f"Solution step {i+1} and frequency {freq} Hz [{i}/{len(frequencies)}]")

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            omega = 2 * np.pi * freq

            F = F_combined[:, i]

            if i == 0:

                # evaluates A and C matrices for omega = 1
                C = ((beta_h + beta_v) * K + (alpha_h + alpha_v) * M)
                A = K - M + 1j * C

                is_A_complex = np.any(np.imag(A.data))
                is_F_complex = np.any(np.imag(F_combined))
                is_complex = is_A_complex or is_F_complex

                linear_solver = initialize_solver(SolverType.PARDISO, is_complex=is_complex, is_symmetric=True)
                del A, C

            C = 1j * ((beta_h + omega * beta_v) * K + (alpha_h + omega * alpha_v) * M)
            A = K - (omega**2) * M + 1j * omega * C
            if not is_complex:
                A.data = np.real(A.data)
                F = np.real(F)

            A = triu(A, format="csr")

            solution[:, i] = linear_solver.solve(A, F)
            linear_solver.clear_memory()
            del A, F

        self._reinsert_prescribed_dofs(solution)
    
    def solve_mode_superposition_method(self, print_log=False):
        """ 
        """
        self.get_max_min_values_of_displacements.cache_clear()
        #TODO: to be implemented

    def _reinsert_prescribed_dofs(self, solution):
        """
        This method reinsert the value of the prescribed degree of freedom in the solution.

        Parameters
        ----------
        solution : array
            Solution data from the direct method, modal superposition or modal shapes from modal analysis.

        Returns
        ----------
        array
            Solution of all the degrees of freedom.
        """

        rows = self.assembler.n_dofs
        cols = solution.shape[1]
        full_solution = np.zeros((rows, cols), dtype=complex)

        self.displacement_dofs = self.assembler.displacement_dofs

        if len(self.prescribed_dofs_indexes):
            full_solution[self.prescribed_dofs_indexes, :] = self.array_prescribed_dofs_values[:, 0:cols]

        if len(self.assembler.active_2d_element_dofs):
            unprescribed_shell_dofs = self.assembler.unprescribed_shell_dofs
            full_solution[unprescribed_shell_dofs, :] = solution
            self.solution = full_solution
            # print("reinserted dofs -> ", len(self.displacement_dofs))

        else:
            full_solution[self.unprescribed_dofs_indexes, :] = solution
            self.solution = full_solution
    
    def get_prescribed_dofs_model_excitation(self, freq_dependent=False, index=0):
        """
        This method adds the effects of prescribed acoustic pressure into mass flow global vector.

        Returns
        ----------
        array
            F_eq. Each column corresponds to a frequency of analysis.
        """

        frequencies = self.assembler.model.frequencies
        structural_loads = self.assembler.structural_loads

        if np.sum(self.array_prescribed_dofs_values) == 0:
            return structural_loads

        Kr = (self.assembler.stiffness_matrix_r.toarray())[self.unprescribed_dofs_indexes, :]
        Mr = (self.assembler.mass_matrix_r.toarray())[self.unprescribed_dofs_indexes, :]

        global_damping = self.assembler.model.analysis_setup.get("global_damping", (0, 0, 0, 0))
        alpha_v, beta_v, alpha_h, beta_h = global_damping

        logging.info(f"Processing prescribed dofs model excitation... [10/{len(frequencies)}]")

        rows = Kr.shape[0]
        if freq_dependent:
            cols = 1
            F_eq = np.zeros(rows, dtype=complex)

        else:
            cols = len(frequencies)
            F_eq = np.zeros((rows, cols), dtype=complex)

        if len(self.prescribed_dofs_values):

            for i, freq in enumerate(frequencies):
                #
                logging.info(f"Processing prescribed dofs model excitation... [{i + 10}/{len(frequencies) + 10}]")
                #
                Kr_add = np.sum((Kr * self.array_prescribed_dofs_values[:, i]), axis=1)
                Mr_add = np.sum((Mr * self.array_prescribed_dofs_values[:, i]), axis=1)
                #
                omega = 2 * np.pi * freq
                F_Kadd = Kr_add
                F_Madd = -(omega**2) * Mr_add
                F_Cadd = 1j * ((beta_h + omega * beta_v) * Kr_add + (alpha_h + omega * alpha_v) * Mr_add)
                F_eq[:, i] = F_Madd + F_Cadd + F_Kadd

            logging.info("Processing prescribed dofs model excitation... [100/100]")

        F_combined = structural_loads - F_eq

        return F_combined

    def plot_graph(self, matrix):
        """
        """
        import matplotlib.pyplot as plt
        plt.ion()
        plt.cla()
        plt.spy(matrix, color=(0.25,0.25,0.25))
        plt.show()