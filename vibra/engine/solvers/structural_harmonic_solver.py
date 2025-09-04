
from vibra.engine.solvers.linear_solver import initialize_solver, SolverType
from vibra.engine import AnalysisID

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

        
    def get_prescribed_dofs_model_excitation(self, index: int = 0):
        """
        This method adds the effects of prescribed acoustic pressure into mass flow global vector.

        Parameter
        ---------
        index: int, optional
        It corresponds to the frequency index.

        Returns
        -------
        f_eq: np.ndarray
        The array of equivalent prescribed dof model excitation from
        i-th frequency index.
        """

        if np.sum(self.prescribed_dofs_values) == 0:
            return 0.

        alpha, beta, eta = self.assembler.model.analysis_setup.get("global_damping", (0, 0, 0))

        frequencies = self.assembler.model.frequencies
        omega = 2 * np.pi * frequencies[index]

        values = self.array_prescribed_dofs_values[:, index]

        self.Kr = self.assembler.stiffness_matrix_r
        self.Mr = self.assembler.mass_matrix_r

        Kr_add = self.Kr @ values
        Mr_add = self.Mr @ values

        f_eq = (1 + 1j*(eta + omega * beta)) * Kr_add + (-(omega**2) + 1j*(omega * alpha)) * Mr_add

        if len(self.assembler.active_2d_element_dofs):
            unprescribed_indexes = self.assembler.unprescribed_shell_dofs
        else:
            unprescribed_indexes = self.unprescribed_dofs_indexes

        return f_eq[unprescribed_indexes]


    def get_prescribed_dofs_model_excitation_reference(self, freq_dependent: bool = False):
        """
        This method adds the effects of prescribed acoustic pressure into mass flow global vector.

        Returns
        ----------
        array
            F_eq. Each column corresponds to a frequency of analysis.
        """

        if np.sum(self.prescribed_dofs_values) == 0:
            return 0.

        alpha, beta, eta = self.assembler.model.analysis_setup.get("global_damping", (0, 0, 0))

        frequencies = self.assembler.model.frequencies

        if len(self.assembler.active_2d_element_dofs):
            unprescribed_indexes = self.assembler.unprescribed_shell_dofs
        else:
            unprescribed_indexes = self.unprescribed_dofs_indexes

        Kr = (self.assembler.stiffness_matrix_r.toarray())[unprescribed_indexes, :]
        Mr = (self.assembler.mass_matrix_r.toarray())[unprescribed_indexes, :]

        logging.info(f"Processing prescribed dofs model excitation... [10/{len(frequencies)}]")

        rows = Kr.shape[0]
        if freq_dependent:
            cols = 1
            f_eq = np.zeros(rows, dtype=complex)

        else:
            cols = len(frequencies)
            f_eq = np.zeros((rows, cols), dtype=complex)

        if len(self.prescribed_dofs_values):

            for i, freq in enumerate(frequencies):
                #
                logging.info(f"Processing prescribed dofs model excitation... [{i + 10}/{len(frequencies) + 10}]")
                #
                Kr_add = np.sum((Kr * self.array_prescribed_dofs_values[:, i]), axis=1)
                Mr_add = np.sum((Mr * self.array_prescribed_dofs_values[:, i]), axis=1)
                #
                omega = 2 * np.pi * freq
                f_eq[:, i] = (1 + 1j*(eta + omega * beta)) * Kr_add + (-(omega**2) + 1j*(omega * alpha)) * Mr_add

            logging.info("Processing prescribed dofs model excitation... [100/100]")

        return f_eq


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
        alpha, beta, eta = self.assembler.model.analysis_setup.get("global_damping", (0, 0, 0))

        self.get_max_min_values_of_displacements.cache_clear()

        self.unprescribed_dofs_indexes, self.prescribed_dofs_indexes = self.assembler.get_matrices_dropping_indexes()
        self.prescribed_dofs_values, self.array_prescribed_dofs_values = self.assembler.get_prescribed_dofs_values()

        M = self.assembler.mass_matrix
        K = self.assembler.stiffness_matrix

        structural_loads = self.assembler.structural_loads

        rows = K.shape[0]
        cols = len(frequencies)
        solution = np.zeros((rows, cols), dtype=complex)

        logging.info(f"Solving harmonic analysis... [0/{len(frequencies)}]")

        for i, freq in enumerate(frequencies):
            logging.info(f"Solution step {i+1} and frequency {freq} Hz [{i}/{cols}]")

            omega = 2 * np.pi * freq

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            f_eq = self.get_prescribed_dofs_model_excitation(index=i)
            f = structural_loads[:, i] - f_eq

            if i == 0:
                # evaluates A matrix for omega = 1
                A = (-1 + 1j*alpha) * M + (1 + 1j*(eta + beta)) * K

                is_A_complex = np.any(np.imag(A.data))
                is_F_complex = np.any(np.imag(f))
                is_complex = is_A_complex or is_F_complex

                linear_solver = initialize_solver(SolverType.PARDISO, is_complex=is_complex, is_symmetric=True)
                del A

            A = (-(omega**2) + 1j*(omega * alpha)) * M + (1 + 1j*(eta + omega * beta)) * K 

            if not is_complex:
                A.data = np.real(A.data)
                f = np.real(f)

            A = triu(A, format="csr")
            solution[:, i] = linear_solver.solve(A, f)

            linear_solver.clear_memory()
            del A, f

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


    def plot_graph(self, matrix):
        """
        """
        import matplotlib.pyplot as plt
        plt.ion()
        plt.cla()
        plt.spy(matrix, color=(0.25,0.25,0.25))
        plt.show()