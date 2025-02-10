import logging

import numpy as np
from scipy.sparse import lil_matrix, coo_matrix, csr_matrix
from scipy.sparse.linalg import LinearOperator, eigs, eigsh, inv, lobpcg
from scipy.sparse.csgraph import reverse_cuthill_mckee

from vibra.utils.progress_status import ProgressStatus


class AcousticModalSolver:
    def __init__(self, assembler, analysis_data=None):
        #
        self.assembler = assembler
        self.reset_variables()
        self.load_analysis_data(analysis_data)

    def reset_variables(self):
        self.modes = 30
        self.sigma_factor = 0.01
        self.analysis_type = None
        self.natural_frequencies = None
        self.modal_shape = None
        self.eigen_values = None
        self.eigen_vectors = None

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

    def solve(self, K=[], M=[], which="LM", normalize=True, harmonic_analysis=False):
        """
        """

        if K == [] and M == []:
            K = self.assembler.stiffness_matrix
            M = self.assembler.mass_matrix

        # self.plot_graph(K)
        logging.info("Solving the eigenproblem..." + ProgressStatus(10, 100))
        self.eigen_values, self.eigen_vectors = eigs(K, M=M, k=self.modes, which=which, sigma=self.sigma_factor, tol=1e-2)

        logging.info("Post-processing the solution..." + ProgressStatus(95, 100))
        positive_real = np.absolute(np.real(self.eigen_values))
        natural_frequencies = np.sqrt(positive_real) / (2 * np.pi)
        modal_shape = np.real(self.eigen_vectors)

        index_order = np.argsort(natural_frequencies)
        natural_frequencies = natural_frequencies[index_order]
        modal_shape = modal_shape[:, index_order]

        self.unprescribed_indexes, self.prescribed_indexes = self.assembler.get_matrices_dropping_indexes()
        self.prescribed_values, self.array_prescribed_values = self.assembler.get_prescribed_dofs_values()

        self.natural_frequencies = natural_frequencies
        self.modal_shape = modal_shape

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