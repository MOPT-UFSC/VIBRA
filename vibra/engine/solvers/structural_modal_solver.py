# fmt: off
from vibra.engine.solvers.linear_solver import initialize_solver, SolverType
from vibra.utils.progress_status import ProgressStatus

import logging

import numpy as np
from functools import cache
from scipy.sparse.linalg import eigs


class StructuralModalSolver:
    def __init__(self, assembler, analysis_data=None):

        self.assembler = assembler

        self.reset_variables()
        self.load_analysis_data(analysis_data)

    def reset_variables(self):
        self.modes = 20
        self.sigma_factor = 0.01
        self.analysis_type = None
        self.natural_frequencies = None
        self.solution_full = None

    def load_analysis_data(self, analysis_data):
        if analysis_data is not None:
            if analysis_data["analysis_id"] in [2, 4]:
                if "modes" in analysis_data.keys():
                    self.modes = analysis_data["modes"]
                if "sigma_factor" in analysis_data.keys():
                    self.sigma_factor = analysis_data["sigma_factor"]
                if analysis_data["analysis_id"] == 2:
                    self.analysis_type = "structural"
                else:
                    self.analysis_type = "acoustic"

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

        data = self.solution_full[self.displacement_dofs, column]

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

    def solve(self, K=[], M=[], which="LM", harmonic_analysis=False):
        """ This method solves the structural modal analysis for undamped problems.
        """
        self.get_max_min_values_of_displacements.cache_clear()

        if K == [] and M == []:
            K = self.assembler.stiffness_matrix
            M = self.assembler.mass_matrix

        sigma = self.sigma_factor
        logging.info("Solving the eigenproblem..." + ProgressStatus(75, 100))

        is_M_complex = np.any(np.imag(M.data))
        is_K_complex = np.any(np.imag(K.data))
        is_complex = is_M_complex or is_K_complex

        if not is_complex:
            M.data = np.real(M.data)
            K.data = np.real(K.data)

        linear_solver = initialize_solver(SolverType.PARDISO, is_complex=is_complex, is_symmetric=True)
        opinv = linear_solver.build_linear_operator(K - sigma * M)

        eigen_values, eigen_vectors = eigs(K, M=M, k=self.modes, sigma=sigma, which=which, OPinv=opinv)
        linear_solver.clear_memory()

        logging.info("Post-processing the solution..." + ProgressStatus(95, 100))
        positive_real = np.absolute(np.real(eigen_values))
        natural_frequencies = np.sqrt(positive_real) / (2 * np.pi)
        modal_shape = np.real(eigen_vectors)
        # print(f"\nNatural frequencies: \n {natural_frequencies.reshape(-1, 1)}")

        index_order = np.argsort(natural_frequencies)
        natural_frequencies = natural_frequencies[index_order]
        modal_shape = modal_shape[:, index_order]

        self.natural_frequencies = natural_frequencies
        self.unprescribed_dofs_indexes, self.prescribed_dofs_indexes = self.assembler.get_matrices_dropping_indexes()
        self.prescribed_dofs_values, self.array_prescribed_dofs_values = self.assembler.get_prescribed_dofs_values()

        if not harmonic_analysis:
            modal_shape = self._reinsert_prescribed_dofs(modal_shape, modal_analysis=True)
            for value in self.prescribed_dofs_values:
                if value is not None:
                    if (isinstance(value, complex) and value != complex(0)) or (isinstance(value, np.ndarray) and sum(value) != complex(0)):
                        self.warning_modal = "The Prescribed DOFs of non-zero values have been ignored in the modal analysis. "
                        self.warning_modal += "The null value has been attributed to those DOFs with non-zero values."

        return natural_frequencies, modal_shape

    def _reinsert_prescribed_dofs(self, solution, modal_analysis=False):
        """
        This method reinsert the value of the prescribed degree of freedom in the solution. If modal analysis is performed, the values are zeros.

        Parameters
        ----------
        solution : array
            Solution data from the direct method, modal superposition or modal shapes from modal analysis.

        modal_analysis : boll, optional
            True if the modal analysis was evaluated.

        Returns
        ----------
        array
            Solution of all the degrees of freedom.
        """

        rows = self.assembler.n_dofs
        cols = solution.shape[1]
        self.displacement_dofs = self.assembler.displacement_dofs

        solution_full = np.zeros((rows, cols), dtype=complex)

        if len(self.assembler.active_2d_element_dofs):
            unprescribed_shell_dofs = self.assembler.unprescribed_shell_dofs
            solution_full[unprescribed_shell_dofs, :] = solution
            self.solution_full = solution_full
            # print("reinserted dofs -> ", len(self.displacement_dofs))

        else:
            solution_full[self.unprescribed_dofs_indexes, :] = solution
            self.solution_full = solution_full

# fmt: on