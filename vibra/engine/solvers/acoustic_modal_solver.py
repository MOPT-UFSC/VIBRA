# fmt: off

from vibra.utils.progress_status import ProgressStatus

import logging

import numpy as np
from pypardiso import PyPardisoSolver
from scipy.sparse import csr_matrix, block_array, bmat, eye, triu 
from scipy.sparse.linalg import LinearOperator, eigs, eigsh, inv


class LuInv(LinearOperator):
    def __init__(self, A):
        ps = PyPardisoSolver(mtype=6)
        ps.factorize(triu(A, format="csr"))
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
        self.modal_shapes = np.array([])
        self.eigen_values = np.array([])
        self.eigen_vectors = np.array([])
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

    def solve(self, K=[], M=[], which="LM", normalize=True, harmonic_analysis=False, complex_analysis=True):
        """
        """

        self.unprescribed_indexes, self.prescribed_indexes = self.assembler.get_matrices_dropping_indexes()
        self.prescribed_values, self.array_prescribed_values = self.assembler.get_prescribed_dofs_values()

        if K == [] and M == []:
            K = self.assembler.stiffness_matrix
            M = self.assembler.mass_matrix

        C_imp = self.assembler.damping_matrix

        logging.info("Solving the eigenproblem..." + ProgressStatus(75, 100))
        sigma = self.sigma_factor

        if np.sum(C_imp):

            print("resolvendo análise modal complexa")

            N_t = len(self.unprescribed_indexes)

            eyes = eye(N_t, dtype=complex, format="csr")
            zeros = csr_matrix((N_t, N_t), dtype=complex)

            ## Reference - book
            # A = bmat([[ C_imp, M_add], 
            #           [ M_add,  None]], format="csr", dtype=complex)

            # B = bmat([[K_add,   None], 
            #         [ None, -M_add]], format="csr", dtype=complex)            

            ## As Ans-theory
            # A = bmat([  [ C_imp, -M_add], 
            #             [  eyes,  zeros]  ], format="csr", dtype=complex)

            # B = bmat([  [K_add, zeros], 
            #             [zeros,   eyes]  ], format="csr", dtype=complex)

            # from scipy.linalg import eig
            # eigen_values, eigen_vectors = eig(B.toarray(), b=A.toarray())
            # eigen_values, eigen_vectors = eigs(B, M=A, k=modes, which=which, sigma=sigma_factor)

            inv_M = inv(M.tocsc()).tocsr()
            print("a matriz foi invertida")

            AA = bmat([ [zeros, eyes],
                        [-inv_M@K, -inv_M@C_imp]])
    
            # eigen_values, eigen_vectors = eigs(AA, k=modes, which=which, sigma=sigma_factor)
            self.eigen_values, self.eigen_vectors = eigs(AA, k=2*self.modes, sigma=sigma, which=which)#, OPinv=opinv)

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

            # print(np.array([natural_frequencies, damping_ratio]).T[:10])
            # print(eigen_values[:10])

        else:

            print("resolvendo análise modal real")

            opinv = LuInv(K - sigma * M)
            self.eigen_values, self.eigen_vectors = eigs(K, M=M, k=self.modes, sigma=sigma, which=which, OPinv=opinv)

            logging.info("Post-processing the solution..." + ProgressStatus(95, 100))
            positive_real = np.absolute(np.real(self.eigen_values))
            natural_frequencies = np.sqrt(positive_real) / (2 * np.pi)
            modal_shapes = self.eigen_vectors

            index_order = np.argsort(natural_frequencies)
            natural_frequencies = natural_frequencies[index_order]
            modal_shapes = modal_shapes[:, index_order]

        self.natural_frequencies = natural_frequencies
        self.modal_shapes = modal_shapes

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