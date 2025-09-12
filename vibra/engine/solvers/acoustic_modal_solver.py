from vibra.engine.solvers.linear_solver import SolverType, initialize_solver

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler

import logging
import numpy as np

from scipy.sparse.linalg import eigs


class AcousticModalSolver:
    def __init__(self, assembler: "AcousticAssembler", **kwargs):
        self.assembler = assembler
        self.reset_variables()

    def reset_variables(self):
        self.solution = None
        self.natural_frequencies = np.array([])
        self.complex_natural_frequencies = np.array([])
        self.analysis_type = "acoustic"

    def solve(self, which="LM"):
        """ This method solves the acoustic modal analysis for both damped and undamped problems.
        """

        self.reset_variables()

        n_modes = self.assembler.model.analysis_setup.get("modes", 40)
        sigma = self.assembler.model.analysis_setup.get("sigma_factor", 0.01)

        C_imp = self.assembler.damping_matrix

        logging.info("Solving the eigenproblem... [75/100]")

        linear_solver = initialize_solver(SolverType.PARDISO)

        A, B = self.assembler.build_eigenproblem_system()

        def solve_eigenproblem(n_modes):
            try:
                opinv = linear_solver.build_linear_operator(A - sigma * B)
                eigen_values, eigen_vectors = eigs(A, M=B, k=n_modes, sigma=sigma, which=which, OPinv=opinv)
                linear_solver.clear_memory()

            except Exception as error_log:
                from traceback import print_exception
                print_exception(error_log)
                eigen_values, eigen_vectors = eigs(A, M=B, k=n_modes, sigma=sigma, which=which)

            return eigen_values, eigen_vectors

        if np.any(C_imp.data):
            eigen_values, eigen_vectors = solve_eigenproblem(2*n_modes)
            logging.info("Post-processing the solution... [95/100]")

            n_dof = int(eigen_vectors.shape[0] / 2)

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
            self.solution = eigen_vectors[:n_dof, index_order][:, mask_dmp]
            self.complex_natural_frequencies = complex_natural_frequencies[mask_dmp]

        else:
            eigen_values, eigen_vectors = solve_eigenproblem(n_modes)

            logging.info("Post-processing the solution... [95/100]")

            Wn2 = np.absolute(np.real(eigen_values))
            natural_frequencies = np.sqrt(Wn2) / (2 * np.pi)

            # reordering the eigenvalues and eigenvectors founded
            index_order = np.argsort(natural_frequencies)
            self.natural_frequencies = natural_frequencies[index_order]
            self.solution = eigen_vectors[:, index_order]
