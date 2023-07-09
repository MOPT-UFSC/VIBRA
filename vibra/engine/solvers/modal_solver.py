import numpy as np
from scipy.linalg import eig
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import LinearOperator, eigs, eigsh, inv, lobpcg

from vibra.engine.assemblers.modal_assembler import ModalAssembler


class ModalSolver:
    def __init__(self, assembler, analysis_data=None):
        #
        self.assembler = assembler
        self.reset_variables()
        #
        if analysis_data is not None:
            if analysis_data["analysis_id"] in [2, 4]:
                if "modes" in analysis_data.keys():
                    self.modes = analysis_data["modes"]
                if "sigma_factor" in analysis_data.keys():
                    self.sigma_factor = analysis_data["sigma_factor"]

        self.natural_frequencies = None
        self.modal_shape = None

        self.eigen_values = None
        self.eigen_vectors = None

        # Variables to store harmonic analysis results
        # self.frequencies = None
        # self.harmonic_response = None

    def reset_variables(self):
        self.modes = 20
        self.sigma_factor = 0.01

    # def modal_analysis(self, K=[], M=[], modes=20, which='LM', sigma=0.01, normalize=True):
    def solve(self, K=[], M=[], which="LM", normalize=True):
        if K != [] and M != []:
            KT = K
            MT = M
        else:
            KT = self.assembler.stiffness_matrix
            MT = self.assembler.mass_matrix

        self.eigen_values, self.eigen_vectors = eigs(KT, M=MT, k=self.modes, which=which, sigma=self.sigma_factor)

        positive_real = np.absolute(np.real(self.eigen_values))
        natural_frequencies = np.sqrt(positive_real) / (2 * np.pi)
        modal_shape = np.real(self.eigen_vectors)

        index_order = np.argsort(natural_frequencies)
        natural_frequencies = natural_frequencies[index_order]
        modal_shape = modal_shape[:, index_order]

        if normalize:
            modal_shape /= np.max(np.abs(modal_shape), axis=0)

        self.natural_frequencies = natural_frequencies
        self.modal_shape = modal_shape

        # print(f"Natural frequencies:{natural_frequencies}")

        return natural_frequencies, modal_shape
