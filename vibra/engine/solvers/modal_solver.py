import logging
import sys
from tqdm import tqdm

import numpy as np
from scipy.sparse.linalg import eigs

from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.solution import ModalSolution
from vibra.engine.solvers.linear_solver import SolverType, initialize_solver


class ModalSolver:
    def __init__(self, assembler: "AcousticAssembler|StructuralAssembler", **kwargs):
        self.assembler = assembler
        self.reset_variables()

    def reset_variables(self):
        self.solution: ModalSolution | None = None
        self.nodal_solution: np.ndarray | None = None
        self.natural_frequencies = np.array([])
        self.complex_natural_frequencies = np.array([])
        self.displacement_dof: np.ndarray | None = None

    def solve(self, which="LM", full_solution: bool = True) -> ModalSolution:
        """
        This method solves the acoustic modal analysis for both damped and undamped problems.
        """

        self.reset_variables()

        n_modes = self.assembler.model.analysis_setup.modes_number
        sigma = self.assembler.model.analysis_setup.sigma_factor
        
        logging.info("Solving the eigenproblem... [75/100]")

        A, B, is_symmetric = self.assembler.build_eigenproblem_system()

        linear_solver = initialize_solver(SolverType.PARDISO, is_symmetric=is_symmetric)

        if not is_symmetric:
            n_modes *= 2

        est_operations = min(A.shape[0], max(3 * (n_modes + 1), 20))

        progress_bar = tqdm(total=100, desc="Solving eigenproblem", unit="%")
        def update_progress(percentage: int):
            if (increment := percentage - progress_bar.n) > 0:
                progress_bar.update(increment)

        try:
            logging.info("Solving eigenproblem... [0/100]")

            opinv = linear_solver.build_linear_operator(A - sigma * B, est_operations=est_operations, progress_callback=update_progress)
            eigenvalues, eigenvectors = eigs(A, M=B, k=n_modes, sigma=sigma, which=which, OPinv=opinv)

        except Exception as error_log:
            from traceback import print_exception

            print_exception(error_log)
            eigenvalues, eigenvectors = eigs(A, M=B, k=n_modes, sigma=sigma, which=which)

        finally:
            linear_solver.clear_memory()
            update_progress(100)
            progress_bar.close()

        if not is_symmetric:
            logging.info("Post-processing the solution... [95/100]")

            n_dof = int(eigenvectors.shape[0] / 2)

            # filtering the eigenvalues with positive imaginary part
            mask = np.imag(eigenvalues) > 0
            eigenvalues = eigenvalues[mask]
            eigenvectors = eigenvectors[:, mask]

            Wn = np.abs(eigenvalues)
            natural_frequencies = Wn / (2 * np.pi)
            damping_ratio = -np.real(eigenvalues) / Wn

            # reordering the eigenvalues and eigenvectors founded
            index_order = np.argsort(natural_frequencies)
            damping_ratio = damping_ratio[index_order]
            natural_frequencies = natural_frequencies[index_order]
            complex_natural_frequencies = eigenvalues[index_order] / (2 * np.pi)

            # filtering the eigenvalues with damping ratio csi < 1
            mask_dmp = np.round(np.abs(damping_ratio), 6) < 1
            damping_ratio = damping_ratio[mask_dmp]
            self.natural_frequencies = natural_frequencies[mask_dmp]
            nodal_solution = eigenvectors[:n_dof, index_order][:, mask_dmp]
            self.complex_natural_frequencies = complex_natural_frequencies[mask_dmp]

        else:
            logging.info("Post-processing the solution... [95/100]")

            Wn2 = np.absolute(np.real(eigenvalues))
            natural_frequencies = np.sqrt(Wn2) / (2 * np.pi)

            # reordering the eigenvalues and eigenvectors founded
            index_order = np.argsort(natural_frequencies)
            self.natural_frequencies = natural_frequencies[index_order]
            nodal_solution = eigenvectors[:, index_order]

        if full_solution:
            self.nodal_solution = self.assembler.reinsert_the_prescribed_dof(nodal_solution)
        else:
            self.nodal_solution = nodal_solution

        if self.complex_natural_frequencies.size:
            cnf = self.complex_natural_frequencies
        else:
            cnf = None

        if isinstance(self.assembler, StructuralAssembler):
            self.displacement_dof = self.assembler.displacement_dof

        self.solution = ModalSolution(
            analysis_id=self.assembler.model.analysis_id,
            natural_frequencies=self.natural_frequencies,
            modal_shapes=self.nodal_solution,
            displacement_dof=self.displacement_dof,
            complex_natural_frequencies=cnf,
        )

        return self.solution
