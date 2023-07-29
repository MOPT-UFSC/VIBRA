import numpy as np
from scipy.linalg import eig
from scipy.sparse.linalg import spsolve


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
        self.modal_shape = None
        self.solution = None
        self.loads = None

    def load_analysis_data(self, analysis_data):
        if analysis_data is not None:
            if analysis_data["analysis_id"] == 3:
                self.analysis_type = "acoustic"
                if "frequencies" in analysis_data.keys():
                    self.frequencies = analysis_data["frequencies"]


    def solve(self):

        self.M = self.assembler.mass_matrix
        self.K = self.assembler.stiffness_matrix
        # print(self.K.shape)
        # print(self.M.shape)

        self.mass_flow = self.assembler.get_acoustic_excitations()
        
        self.unprescribed_indexes, self.prescribed_indexes = self.assembler.get_matrices_dropping_indexes()
        self.prescribed_values, self.array_prescribed_values = self.assembler.get_prescribed_values()
        
        rows = len(self.prescribed_indexes) + len(self.unprescribed_indexes)
        cols = len(self.frequencies)

        solution = np.zeros((rows, cols), dtype=complex)
        
        for i, freq in enumerate(self.frequencies):
            omega = 2 * np.pi * freq
            A = self.K - (omega**2) * self.M
            F =  -1j * omega * self.mass_flow
            solution[:, i] = spsolve(A, F)

        # print(solution.shape)
        self.solution = solution
        return solution

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
    
        
    def get_max_min_values_of_pressures(self, column):

        data = self.solution[:, column]
        
        _pressures = np.abs(data)
        _phases = np.angle(data)
        
        p_min = 1
        p_max = 0
        thetas = np.arange(0, 360, 2)*(np.pi/180)

        for theta in thetas:
            pressures = _pressures*np.cos(theta + _phases)

            p_min_i = min(pressures)
            p_max_i = max(pressures)

            if p_min_i < p_min:
                p_min = p_min_i
            if p_max_i > p_max:
                p_max = p_max_i
    
        return p_min, p_max