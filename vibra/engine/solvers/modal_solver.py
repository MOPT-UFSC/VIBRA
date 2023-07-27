import numpy as np
from scipy.linalg import eig
from scipy.sparse.linalg import LinearOperator, eigs, eigsh, inv, lobpcg

import logging
from vibra.utils.progress_status import ProgressStatus


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
                if analysis_data["analysis_id"] == 2:
                    self.analysis_type = "structural"
                else:
                    self.analysis_type = "acoustic"

    def reset_variables(self):
        self.modes = 20
        self.sigma_factor = 0.01
        self.analysis_type = None
        self.natural_frequencies = None
        self.modal_shape = None
        self.eigen_values = None
        self.eigen_vectors = None

    def solve(self, K=[], M=[], which="LM", normalize=True):
        if K != [] and M != []:
            KT = K
            MT = M
        else:
            KT = self.assembler.stiffness_matrix
            MT = self.assembler.mass_matrix

        logging.info("Finding eigen values and eigen vectors" + ProgressStatus(5, 100))
        self.eigen_values, self.eigen_vectors = eigs(KT, M=MT, k=self.modes, which=which, sigma=self.sigma_factor)

        logging.info("Extracting information from solution" + ProgressStatus(95, 100))
        positive_real = np.absolute(np.real(self.eigen_values))
        natural_frequencies = np.sqrt(positive_real) / (2 * np.pi)
        modal_shape = np.real(self.eigen_vectors)

        index_order = np.argsort(natural_frequencies)
        natural_frequencies = natural_frequencies[index_order]
        modal_shape = modal_shape[:, index_order]

        self.natural_frequencies = natural_frequencies
        self.modal_shape = modal_shape