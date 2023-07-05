import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs, eigsh, inv
from scipy.sparse.linalg import lobpcg, LinearOperator
from scipy.linalg import eig


class ModalSolver:   
    def __init__(self, assembler):
        self.assembler = assembler
        self.mass_matrix = assembler.mass_matrix
        self.stiffness_matrix = assembler.stiffness_matrix

        # Variables to store modal analysis results
        self.natural_frequencies = None
        self.eigen_vectors = None

        # Variables to store harmonic analysis results
        self.frequencies = None
        self.harmonic_response = None
   
    
    def modal_analysis(self, K=[], M=[], modes=20, which='LM', sigma=0.01, normalize=True):
        """
        """
        
        if K != [] and M != []:
            KT = K
            MT = M
        else:
            KT = self.stiffness_matrix
            MT = self.mass_matrix

        eigen_values, eigen_vectors = eigs(KT, M=MT, k=modes, which=which, sigma=sigma)

        positive_real = np.absolute(np.real(eigen_values))
        natural_frequencies = np.sqrt(positive_real)/(2*np.pi)
        modal_shape = np.real(eigen_vectors)

        index_order = np.argsort(natural_frequencies)
        natural_frequencies = natural_frequencies[index_order]
        modal_shape = modal_shape[:, index_order]
        
        if normalize:
            modal_shape /= np.max(np.abs(modal_shape), axis=0)

        self.natural_frequencies = natural_frequencies
        self.eigen_vectors = modal_shape

        return natural_frequencies, modal_shape