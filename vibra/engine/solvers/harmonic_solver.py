import logging
from time import time

import numpy as np

from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.solution import AcousticHarmonicSolution, HarmonicSolution, StructuralHarmonicSolution
from vibra.engine.solvers import ModalSolver
from vibra.engine.solvers.linear_solver import LinearSolver, SolverType, initialize_solver
from vibra.project_files.lazy_hdf5_matrix import LazyHDF5MatrixWriter
from vibra.project_files.project_file import ProjectFile


class HarmonicSolver:
    def __init__(self, assembler: AcousticAssembler | StructuralAssembler, project_file: ProjectFile | None = None, **kwargs):
        self.assembler = assembler
        self.project_file = project_file

        self.reset_variables()

    @property
    def frequencies(self) -> np.ndarray:
        return self.assembler.model.frequencies

    def reset_variables(self):
        self.solution = None
        self.displacement_dof = None
        self._linear_solver = None

    def solve_direct(self, print_log: bool = False, is_resume: bool = False) -> HarmonicSolution:
        """
        This method solves the acoustic harmonic analysis using the
        direct method for both damped and undamped problems.

        Parameter
        ---------
        print_log: bool, optional
            This argument controls the printing of the solution steps to the terminal.
        """

        logging.info("Solving harmonic analysis (direct method)... [10/100]")

        solution = self._get_solution_handler(is_resume)

        self.compute_frequency_sweep(solution, print_log, is_resume)

        logging.info("Solving harmonic analysis (direct method)... [99/100]")
        self._closing_solution_handler(solution)

        if isinstance(self.assembler, StructuralAssembler):
            return StructuralHarmonicSolution(
                self.assembler.model.analysis_setup.frequencies(),
                self.solution,
                self.displacement_dof,
            )
        else:
            return AcousticHarmonicSolution(
                self.assembler.model.analysis_setup.frequencies(),
                self.solution,
            )


    def _get_solution_handler(self, is_resume):
        if isinstance(self.assembler, StructuralAssembler):
            self.displacement_dof = self.assembler.displacement_dof

        frequencies = self.assembler.model.frequencies

        if self.project_file:
            num_rows = self.assembler.total_dof
            solution = self.project_file.get_solution_writer(num_rows, frequencies, dtype=complex, is_resume=is_resume)
            if self.displacement_dof is not None:
                solution.save_extra_data("displacement_dof", self.displacement_dof, dtype=int)
        else:
            num_rows = self.assembler.stiffness_matrix.shape[0]
            solution = np.zeros((num_rows, len(frequencies)), dtype=complex)
        return solution

    def _closing_solution_handler(self, solution):
        if isinstance(solution, LazyHDF5MatrixWriter):
            solution.close()
            if self.assembler.model.stop_processing:
                self.reset_variables()
            else:
                self.solution = self.project_file.get_solution_loader()
        else:
            # reinsert the prescribed degrees of freedom into the solution vector
            self.solution = self.assembler.reinsert_the_prescribed_dof(solution)

    def compute_frequency_sweep(self, solution, print_log, is_resume, eigenvectors=None):

        # frequencies vector [in hertz]
        frequencies = self.assembler.model.frequencies

        # compute the solution for each frequency step
        for i, freq in enumerate(frequencies):
            if self.assembler.model.stop_processing:
                return

            logging.info(f"Solution step {i + 1} and frequency {freq} Hz [{i + 1}/{len(frequencies)}]")

            if is_resume and i != 0 and isinstance(solution, LazyHDF5MatrixWriter) and solution.has_column(i):
                continue

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            A, f = self.assembler.build_harmonic_system(freq, i)

            if freq == 0:
                # In case of freq=0, the matrix may differ from the non-zero frequencies, so we solve it with
                # a particular linear solver
                linear_solver = self._get_linear_solver(eigenvectors, True)
            else:
                linear_solver = self._get_linear_solver(eigenvectors)

            solution_freq = linear_solver.solve(A, f)

            if isinstance(solution, LazyHDF5MatrixWriter):
                # reinsert the prescribed degrees of freedom into the solution vector
                solution_freq = self.assembler.reinsert_the_prescribed_dof_into_solution_freq(solution_freq, i)

            solution[:, i] = solution_freq

            # clear the memory and delete some variables to reduce the memory usage
            linear_solver.clear_memory()
            del A, f

    def _get_linear_solver(self, eigenvectors, new_instance: bool = False) -> LinearSolver:
        if self._linear_solver is None or new_instance:
            if eigenvectors is not None:
                linear_solver = initialize_solver(SolverType.MODAL_SUPERPOSITION, eigenvectors=eigenvectors)
            elif isinstance(self.assembler, StructuralAssembler):
                linear_solver = initialize_solver(SolverType.PARDISO, is_symmetric=True)
            else:
                linear_solver = initialize_solver(SolverType.PARDISO)

        if new_instance:
            return linear_solver
        elif self._linear_solver is not None:
            return self._linear_solver
        else:
            self._linear_solver = linear_solver
            return linear_solver

    def solve_mode_superposition(
        self,
        print_log: bool = False,
        is_resume: bool = False,
        is_proportionally_damped: bool = False,
    ) -> HarmonicSolution:
        logging.info("Solving harmonic analysis (mode superposition method)... [10/100]")
        solution = self._get_solution_handler(is_resume)

        t0 = time()
        modal_solver = ModalSolver(self.assembler)
        modal_solution = modal_solver.solve(full_solution=False)
        dt = time() - t0
        print(f"Elapsed time to solve modal analysis: {dt: .6f} [s]")

        if is_proportionally_damped:
            self.compute_proportionally_damped_frequency_sweep(
                solution,
                modal_solution.modal_shape,
                modal_solution.natural_frequencies,
                print_log,
                is_resume,
            )
        else:
            self.compute_frequency_sweep(solution, print_log, is_resume)

        self._closing_solution_handler(solution)

        if isinstance(self.assembler, StructuralAssembler):
            return StructuralHarmonicSolution(
                self.assembler.model.frequencies,
                self.solution,
                self.displacement_dof,
            )
        else:
            return AcousticHarmonicSolution(
                self.assembler.model.frequencies,
                self.solution,
            )

    def compute_proportionally_damped_frequency_sweep(self, solution, modes, natural_frequencies, print_log, is_resume):
        # frequencies vector [in hertz]
        frequencies = self.assembler.model.frequencies

        (alpha, beta, eta) = self.assembler.model.old_analysis_setup.get("global_damping", (0, 0, 0))
        omega_n = 2 * np.pi * natural_frequencies
        # Phi is the matrix of the eigenvectors
        Phi = modes
        Phi_t = Phi.T

        # compute the solution for each frequency step
        for i, freq in enumerate(frequencies):
            logging.info(f"Solution step {i + 1} and frequency {freq} Hz [{i + 1}/{len(frequencies)}]")

            if is_resume and i != 0 and isinstance(solution, LazyHDF5MatrixWriter) and solution.has_column(i):
                continue

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            f = self.assembler.get_combined_nodal_loads_vector(index=i)

            omega = 2 * np.pi * freq
            A = omega_n**2 - omega**2 + 1j * (omega * (beta * (omega_n**2) + alpha) + eta * (omega_n**2))
            diag = np.diag(1 / A)

            # compute the solution for each frequency step
            solution_freq = Phi @ (diag @ (Phi_t @ f))

            if isinstance(solution, LazyHDF5MatrixWriter):
                # reinsert the prescribed degrees of freedom into the solution vector
                solution_freq = self.assembler.reinsert_the_prescribed_dof_into_solution_freq(solution_freq, i)

            solution[:, i] = solution_freq
