import numpy as np
from scipy.linalg import eig
from scipy.sparse.linalg import LinearOperator, eigs, spsolve


class AcousticHarmonicSolver:
    def __init__(self, assembler, analysis_data=None):
        #
        self.assembler = assembler
        self.reset_variables()
        self.load_analysis_data(analysis_data)
        
    def reset_variables(self):
        self.analysis_type = None
        self.frequencies = None
        self.modal_shape = None
        self.solution = None
        self.loads = None
        self.M = self.assembler.mass_matrix
        self.K = self.assembler.stiffness_matrix

    def load_analysis_data(self, analysis_data):
        if analysis_data is not None:
            if analysis_data["analysis_id"] == 3:
                self.analysis_type = "acoustic"
                if "frequencies" in analysis_data.keys():
                    self.frequencies = analysis_data["frequencies"]

    def solve(self):
        # def harmonic_analysys(freq, rho_local, K, M, q, g):
        # P = np.empty([len(q),len(freq)]).astype(complex)
        rows = 1
        cols = len(self.frequencies)
        P = np.zeros((rows, cols), dtype=complex)
        g = q = 1
        rho_local = 1
        for i, freq in enumerate(self.frequencies):
            omega = 2 * np.pi * freq
            A = self.K - (omega**2) * self.M
            F =  -1j * omega * (q + rho_local * g) 
            P[:, i] = spsolve(A, F)  #fluid mass flow rate

        return P


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
                full_solution[self.prescribed_indexes, :] = np.zeros((len(self.prescribed_values),cols))
            else:
                full_solution[self.prescribed_indexes, :] = self.array_prescribed_values[:, 0:cols]
        return np.real(full_solution)