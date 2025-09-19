from vibra.engine.solvers.linear_solver import SolverType, initialize_solver
from vibra.engine import AnalysisID

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler

import logging
import numpy as np

from functools import cache
from scipy.sparse import block_array
from scipy.sparse.linalg import eigs, eigsh


class AcousticModalSolver:
    def __init__(self, assembler: "AcousticAssembler", **kwargs):
        self.assembler = assembler
        self.reset_variables()

    def reset_variables(self):
        self.solution = None
        self.natural_frequencies = np.array([])
        self.complex_natural_frequencies = np.array([])
        self.analysis_type = "acoustic"

    @cache
    def get_min_max_values_of_pressures(self, column: int, plot_type: str):
        """ This method returns the minimum and maximum pressure values
            of selected frequency for animation purposes.

            Parameters:
            -----------
            column: int value relative to frequency column index.

            Returns:
            -----------
            p_min, p_max: float values for minimum and maximum pressures,

        """
    
        data = self.solution[:, column]
        
        amplitudes = np.abs(data)
        phases = np.angle(data)

        p_min = 1
        p_max = 0

        divisions = 36
        thetas = np.linspace(0, 2 * np.pi, divisions + 1, endpoint=True)

        if plot_type == "absolute_values":
            return 0, max(np.abs(data))

        if plot_type == "real_values":
            return min(np.real(data)), max(np.real(data))

        if plot_type == "imag_values":
            return min(np.imag(data)), max(np.imag(data))

        for theta in thetas:
            pressures = amplitudes * np.cos(theta + phases)

            if plot_type == "absolute_animation":
                pressures = np.abs(pressures)

            p_min_i = min(pressures)
            p_max_i = max(pressures)

            if p_min_i < p_min:
                p_min = p_min_i
            if p_max_i > p_max:
                p_max = p_max_i

        if plot_type == "absolute_animation":
            p_min = 0

        if plot_type == "non_absolute_animation":
            max_value = np.max(np.abs([p_min, p_max]))
            p_min = -max_value
            p_max = max_value

        return p_min, p_max

    def solve(self, K=[], M=[], which="LM"):
        """ This method solves the acoustic modal analysis for both damped and undamped problems.
        """

        self.reset_variables()

        n_modes = self.assembler.model.analysis_setup.get("modes", 40)
        self.get_min_max_values_of_pressures.cache_clear()

        self.unprescribed_indexes, self.prescribed_indexes = self.assembler.get_matrices_dropping_indexes()
        self.prescribed_values, self.array_prescribed_values = self.assembler.get_prescribed_dof_values()

        if K == [] and M == []:
            K = self.assembler.stiffness_matrix
            M = self.assembler.mass_matrix

        C_imp = self.assembler.damping_matrix

        logging.info("Solving the eigenproblem... [75/100]")
        sigma = self.assembler.model.analysis_setup.get("sigma_factor", 0.01)

        is_M_complex = np.any(np.imag(M.data))
        is_K_complex = np.any(np.imag(K.data))
        is_C_complex = np.any(np.imag(C_imp.data))
        is_complex = is_M_complex or is_K_complex or is_C_complex

        if np.any(C_imp.data):
            if not is_complex:
                M.data = np.real(M.data)
                K.data = np.real(K.data)
                C_imp.data = np.real(C_imp.data)

            B = block_array([[M, None], [None, M]], format="csr")
            A = block_array([[None, M], [-K, -C_imp]], format="csr")

            linear_solver = initialize_solver(SolverType.PARDISO, is_complex=is_complex, is_symmetric=False)
            opinv = linear_solver.build_linear_operator(A - sigma * B)

            eigen_values, eigen_vectors = eigs(A, M=B, k=2*n_modes, sigma=sigma, which=which, OPinv=opinv)
            linear_solver.clear_memory()

            logging.info("Post-processing the solution... [95/100]")

            n_dofs = int(eigen_vectors.shape[0] / 2)

            # filtering the eigenvalues with positive imaginary part
            mask = np.imag(eigen_values) > 0
            eigen_values = eigen_values[mask]
            eigen_vectors = eigen_vectors[:, mask]

            Wn = np.abs(eigen_values)
            natural_frequencies = Wn / (2 * np.pi)
            damping_ratio = -np.real(eigen_values) / Wn

            # reordering the eigenvalues and eigenvectors founded
            index_order = np.argsort(natural_frequencies)
            damping_ratio = damping_ratio[index_order]
            natural_frequencies = natural_frequencies[index_order]
            complex_natural_frequencies = eigen_values[index_order] / (2 * np.pi)

            # filtering the eigenvalues with damping ratio csi < 1
            mask_dmp = np.round(np.abs(damping_ratio), 6) < 1
            damping_ratio = damping_ratio[mask_dmp]
            self.natural_frequencies = natural_frequencies[mask_dmp]
            self.solution = eigen_vectors[:n_dofs, index_order][:, mask_dmp]
            self.complex_natural_frequencies = complex_natural_frequencies[mask_dmp]

        else:
            if not is_complex:
                M.data = np.real(M.data)
                K.data = np.real(K.data)

            ## symmetrize the global matrices
            # M = (M + M.T) / 2
            # K = (K + K.T) / 2

            # np.savetxt("mass_matrix_base.dat", M.toarray(), delimiter=",", fmt="%.16e")
            # np.savetxt("stiffness_matrix_base.dat", K.toarray(), delimiter=",", fmt="%.16e")

            try:

                linear_solver = initialize_solver(SolverType.PARDISO, is_complex=is_complex, is_symmetric=True)
                opinv = linear_solver.build_linear_operator(K - sigma * M)

                eigen_values, eigen_vectors = eigs(K, M=M, k=n_modes, sigma=sigma, which=which, OPinv=opinv)
                linear_solver.clear_memory()

            except Exception as error_log:
                from traceback import print_exception
                print_exception(error_log)
                eigen_values, eigen_vectors = eigs(K, M=M, k=n_modes, sigma=sigma, which=which)

            logging.info("Post-processing the solution... [95/100]")

            Wn2 = np.absolute(np.real(eigen_values))
            natural_frequencies = np.sqrt(Wn2) / (2 * np.pi)

            # reordering the eigenvalues and eigenvectors founded
            index_order = np.argsort(natural_frequencies)
            self.natural_frequencies = natural_frequencies[index_order]
            self.solution = eigen_vectors[:, index_order]


    def _reinsert_prescribed_dof(self, solution, modal_analysis=False):
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
        rows = solution.shape[0] + len(self.prescribed_indexes)
        cols = solution.shape[1]

        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[self.unprescribed_indexes, :] = solution

        if len(self.prescribed_indexes) > 0:
            if modal_analysis:
                full_solution[self.prescribed_indexes, :] = np.zeros((len(self.prescribed_values), cols))
            else:
                full_solution[self.prescribed_indexes, :] = self.array_prescribed_values[:, 0:cols]
        
        return np.real(full_solution)


    def plot_graph(self, graph):
        """
        """
        import matplotlib.pyplot as plt
        plt.ion()
        plt.cla()
        plt.spy(graph, color=(0.25,0.25,0.25))
        plt.show()
