import logging
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from scipy.sparse.csgraph import reverse_cuthill_mckee
import matplotlib.pyplot as plt

from vibra.utils.progress_status import ProgressStatus


class AcousticHarmonicSolver:
    def __init__(self, assembler, analysis_data=None):
        #
        self.assembler = assembler
        #
        self.reset_variables()
        self.load_analysis_data(analysis_data)

    def reset_variables(self):
        self.analysis_type = None
        self.frequencies = None
        self.dissipation_model = None
        self.modal_shape = None
        self.solution = None
        self.loads = None

    def load_analysis_data(self, analysis_data):
        if analysis_data is not None:
            if analysis_data["analysis_id"] == 3:
                self.analysis_type = "acoustic"
                if "frequencies" in analysis_data.keys():
                    self.frequencies = analysis_data["frequencies"]

    def load_dissipation_model(self, data):
        self.dissipation_model = data

    def get_max_min_values_of_pressures(self, column):
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
        thetas = np.arange(0, 360, 2) * (np.pi / 180)

        for theta in thetas:
            pressures = amplitudes * np.cos(phases + theta)

            p_min_i = min(pressures)
            p_max_i = max(pressures)

            if p_min_i < p_min:
                p_min = p_min_i
            if p_max_i > p_max:
                p_max = p_max_i

        return p_min, p_max

    def solve(self, print_log=False):
        """ """
        #
        self.unprescribed_indexes, self.prescribed_indexes = self.assembler.get_matrices_dropping_indexes()
        #
        M = self.assembler.mass_matrix
        K = self.assembler.stiffness_matrix
        C = self.assembler.damping_matrix
        C_visc = self.assembler.visc_damping_matrix
        Q = self.assembler.mass_flow_vectors
        F_eq = self.get_combined_model_excitation()
        #
        # _K, _M = self.reduces_matrices_bandwidth(K, M)
        # _Q = self.sp_permute_vector(Q, self.chuthill_indexes)
        # _F_eq = self.sp_permute_vector(F_eq, self.chuthill_indexes)
        #
        _K = K
        _M = M
        _Q = Q
        _F_eq = F_eq
        #
        rows = K.shape[0]
        cols = len(self.frequencies)
        solution = np.zeros((rows, cols), dtype=complex)
        #
        logging.info( "Solving harmonic analysis..." + ProgressStatus(0, len(self.frequencies)))

        for i, freq in enumerate(self.frequencies):

            message = f"Solution step {i+1} and frequency {freq} Hz"
            logging.info( message + ProgressStatus(i, len(self.frequencies)))

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")
            
            omega = 2 * np.pi * freq
            # _C = self.sp_permute_matrix(C[i], self.chuthill_indexes, self.chuthill_indexes)
            _C = C[i] + C_visc

            A = _K - (omega**2) * _M + 1j * omega * _C
            F = - 1j * omega * _Q[:, i] - _F_eq[:, i]

            solution[:, i] = spsolve(A, F)

        # solution = self.sp_permute_vector(solution, np.flip(self.chuthill_indexes))
        self.solution = self._reinsert_prescribed_dofs(solution)

        return self.solution

    def reduces_matrices_bandwidth(self, K, M):
        """
        """
        self.chuthill_indexes = reverse_cuthill_mckee(K, symmetric_mode=True)
        # self.chuthill_indexes = reverse_cuthill_mckee(M, symmetric_mode=True)
        #
        M = self.sp_permute_matrix(M, self.chuthill_indexes, self.chuthill_indexes)
        K = self.sp_permute_matrix(K, self.chuthill_indexes, self.chuthill_indexes)
        # plt.cla()
        # plt.spy(M, color=(0.25,0.25,0.25))
        # plt.show()
        return K, M

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
        rows = solution.shape[0] + len(self.prescribed_indexes)
        cols = solution.shape[1]

        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[self.unprescribed_indexes, :] = solution

        if len(self.prescribed_indexes) > 0:
            full_solution[self.prescribed_indexes, :] = self.array_prescribed_values[:, 0:cols]

        return full_solution
    
    def get_combined_model_excitation(self):
        """
        This method adds the effects of prescribed acoustic pressure into mass flow global vector.

        Returns
        ----------
        array
            F_eq. Each column corresponds to a frequency of analysis.
        """

        self.prescribed_values, self.array_prescribed_values = self.assembler.get_prescribed_values()
        #
        Kr = (self.assembler.stiffness_matrix_r.toarray())[self.unprescribed_indexes, :]
        Mr = (self.assembler.mass_matrix_r.toarray())[self.unprescribed_indexes, :]
        Cr = [(sparse_matrix.toarray())[self.unprescribed_indexes, :] for sparse_matrix in self.assembler.damping_matrix_r]
        Cr_visc = (self.assembler.visc_damping_matrix_r.toarray())[self.unprescribed_indexes, :]

        rows = Kr.shape[0]
        cols = len(self.frequencies)

        aux_ones = np.ones(cols, dtype=complex)
        F_eq = np.zeros((rows,cols), dtype=complex)

        if len(self.prescribed_values) != 0:
            list_prescribed_values = []

            for value in self.prescribed_values:
                if isinstance(value, complex):
                    list_prescribed_values.append(aux_ones*value)
                elif isinstance(value, np.ndarray):
                    list_prescribed_values.append(value)
      
            self.array_prescribed_values = np.array(list_prescribed_values)
                        
            for i, freq in enumerate(self.frequencies):
                #
                Kr_add = np.sum((Kr * self.array_prescribed_values[:, i]), axis=1)
                Mr_add = np.sum((Mr * self.array_prescribed_values[:, i]), axis=1)
                Cr_add = np.sum(((Cr[i] + Cr_visc) * self.array_prescribed_values[:, i]), axis=1)
                #
                omega = 2*np.pi*freq
                F_Kadd = Kr_add
                F_Madd = (-(omega**2))*Mr_add 
                F_Cadd = 1j*omega*Cr_add
                F_eq[:, i] = F_Kadd + F_Madd + F_Cadd
       
        return F_eq
    
    def sp_permute_matrix(self, A, perm_r, perm_c):
        """ permute rows and columns of A """
        M, N = A.shape
        # row permumation matrix
        Pr = coo_matrix((np.ones(M), (np.arange(M), perm_r))).tocsr()
        # column permutation matrix
        Pc = coo_matrix((np.ones(N), (perm_c, np.arange(N)))).tocsr()
        return Pc.T * A * Pr.T
    
    def sp_permute_vector(self, A, perm_r):
        """ permute rows and columns of A """
        M, N = A.shape
        # row permumation matrix
        Pr = coo_matrix((np.ones(M), (np.arange(M), perm_r))).tocsr()
        return Pr.T * A