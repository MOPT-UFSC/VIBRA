# fmt: off

from vibra.utils.progress_status import ProgressStatus

import logging
import numpy as np

from time import time
from functools import cache
from pypardiso import PyPardisoSolver
from scipy.sparse import bmat, eye, triu, identity
from scipy.sparse.linalg import LinearOperator, eigs, eigsh, inv

from time import time


class LuInv(LinearOperator):
    def __init__(self, A, **kwargs):
        ps = PyPardisoSolver(**kwargs)
        if kwargs.get("mtype") == 6:
            ps.factorize(triu(A, format="csr"))
        else:
            ps.factorize(A)
        self.factorized_A = ps.factorized_A
        self.solve = ps.solve
        LinearOperator.__init__(self, A.dtype, A.shape)

    def _matvec(self, x):
        return self.solve(self.factorized_A, x.astype(self.dtype))


class AcousticModalSolver:
    def __init__(self, assembler, analysis_data=None):
        #
        self.assembler = assembler
        self.reset_variables()
        self.load_analysis_data(analysis_data)

    def reset_variables(self):
        self.modes = 40
        self.sigma_factor = 0.01
        self.analysis_type = None

        self.solution = None
        self.natural_frequencies = np.array([])
        self.complex_natural_frequencies = np.array([])

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

    def solve(self, K=[], M=[], which="LM", normalize=True, harmonic_analysis=False, complex_analysis=True):
        """
        """
        self.get_min_max_values_of_pressures.cache_clear()

        self.unprescribed_indexes, self.prescribed_indexes = self.assembler.get_matrices_dropping_indexes()
        self.prescribed_values, self.array_prescribed_values = self.assembler.get_prescribed_dofs_values()

        if K == [] and M == []:
            K = self.assembler.stiffness_matrix
            M = self.assembler.mass_matrix

        C_imp = self.assembler.damping_matrix

        logging.info("Solving the eigenproblem..." + ProgressStatus(75, 100))
        sigma = self.sigma_factor

        if np.sum(C_imp):

            N_t = len(self.unprescribed_indexes)
            I = eye(N_t, dtype=complex, format="csr")

            # ## Reference - Craig, Roy R., Kurdila, Andrew J. Fundamentals of Structural Dynamics. Second edition, 2006.
            # A = bmat([[ C_imp,    M], 
            #           [     M, None]], format="csr", dtype=complex)

            # B = bmat([[    K, None], 
            #           [ None,   -M]], format="csr", dtype=complex)            

            # ## Ans-theory
            # A = bmat([[-C_imp,   -M], 
            #           [     I, None]], format="csr", dtype=complex)

            # B = bmat([[   K, None], 
            #           [None,    I]], format="csr", dtype=complex)

            # # opinv = LuInv(B - sigma * A, mtype=13)
            # self.eigen_values, self.eigen_vectors = eigs(B, M=A, k=2*self.modes, which=which, sigma=sigma)#, OPinv=opinv)

            t0 = time()
            inv_M = inv(M.tocsc()).tocsr()
            # ps = PyPardisoSolver(mtype=6)
            # ps.factorize(triu(M, format="csr"))
            # inv_M = ps.solve(ps.factorized_A, identity(M.shape[0], dtype=complex, format="csr"))
            dt = time() - t0
            print(f"Elapsed time to calculate the inverse of matrix M: {dt : .4f}")

            AA = bmat([ [    None,            I],
                        [-inv_M@K, -inv_M@C_imp]], format="csr", dtype=complex)

            t0 = time()
            opinv = LuInv(AA - sigma * identity(AA.shape[0], dtype=complex, format="csr"), mtype=13)
            self.eigen_values, self.eigen_vectors = eigs(AA, k=2*self.modes, sigma=sigma, which=which, OPinv=opinv)
            dt = time() - t0
            print(f"Elapsed time to solve the eigensolver: {dt : .4f}")

            logging.info("Post-processing the solution..." + ProgressStatus(95, 100))

            N_dofs = int(self.eigen_vectors.shape[0] / 2)

            mask = np.imag(self.eigen_values) > 0
            _eigen_values = self.eigen_values[mask]
            _eigen_vectors = self.eigen_vectors[:, mask]

            Wn = np.abs(_eigen_values)
            natural_frequencies = Wn / (2 * np.pi)
            damping_ratio = -np.real(_eigen_values) / Wn

            index_order = np.argsort(natural_frequencies)

            damping_ratio = damping_ratio[index_order]
            natural_frequencies = natural_frequencies[index_order]
            complex_natural_frequencies = _eigen_values[index_order] / (2 * np.pi)
            modal_shapes = _eigen_vectors[:N_dofs, index_order]

            mask_dmp = np.round(np.abs(damping_ratio), 6) < 1

            damping_ratio = damping_ratio[mask_dmp]
            natural_frequencies = natural_frequencies[mask_dmp]
            modal_shapes = modal_shapes[:, mask_dmp]
            self.complex_natural_frequencies = complex_natural_frequencies[mask_dmp]

        else:

            opinv = LuInv(K - sigma * M, mtype=6)
            eigen_values, eigen_vectors = eigs(K, M=M, k=self.modes, sigma=sigma, which=which, OPinv=opinv)

            logging.info("Post-processing the solution..." + ProgressStatus(95, 100))
            positive_real = np.absolute(np.real(eigen_values))
            natural_frequencies = np.sqrt(positive_real) / (2 * np.pi)
            modal_shapes = eigen_vectors

            index_order = np.argsort(natural_frequencies)
            natural_frequencies = natural_frequencies[index_order]
            modal_shapes = modal_shapes[:, index_order]

        self.natural_frequencies = natural_frequencies
        self.solution = modal_shapes

        return natural_frequencies, modal_shapes

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

# fmt: on