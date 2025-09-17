from vibra.engine.solvers.linear_solver import SolverType, initialize_solver

from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.assemblers.structural_assembler import StructuralAssembler

import logging
import numpy as np

from scipy.sparse.linalg import eigs


class ModalSolver:
    def __init__(self, assembler: "AcousticAssembler|StructuralAssembler", **kwargs):
        self.assembler = assembler
        self.reset_variables()

    def reset_variables(self):
        self.solution = None
        self.natural_frequencies = np.array([])
        self.complex_natural_frequencies = np.array([])
        self.displacement_dofs = None

    def solve(self, which="LM", full_solution=True):
        """ This method solves the acoustic modal analysis for both damped and undamped problems.
        """

        self.reset_variables()

        n_modes = self.assembler.model.analysis_setup.get("modes", 40)
        sigma = self.assembler.model.analysis_setup.get("sigma_factor", 0.01)

        logging.info("Solving the eigenproblem... [75/100]")

        A, B, is_symmetric = self.assembler.build_eigenproblem_system()

        linear_solver = initialize_solver(SolverType.PARDISO, is_symmetric=is_symmetric)

        if not is_symmetric:
            n_modes *= 2

        try:
            opinv = linear_solver.build_linear_operator(A - sigma * B)
            eigen_values, eigen_vectors = eigs(A, M=B, k=n_modes, sigma=sigma, which=which, OPinv=opinv)
            linear_solver.clear_memory()

        except Exception as error_log:
            from traceback import print_exception
            print_exception(error_log)
            eigen_values, eigen_vectors = eigs(A, M=B, k=n_modes, sigma=sigma, which=which)

        if not is_symmetric:
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
            logging.info("Post-processing the solution... [95/100]")

            Wn2 = np.absolute(np.real(eigen_values))
            natural_frequencies = np.sqrt(Wn2) / (2 * np.pi)

            # reordering the eigenvalues and eigenvectors founded
            index_order = np.argsort(natural_frequencies)
            self.natural_frequencies = natural_frequencies[index_order]
            self.solution = eigen_vectors[:, index_order]

        if full_solution:
            self.solution = self.assembler.reinsert_the_prescribed_dofs(self.solution)
        
        if isinstance(self.assembler, StructuralAssembler):
            self.displacement_dofs = self.assembler.displacement_dofs
