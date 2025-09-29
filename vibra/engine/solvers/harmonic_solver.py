from vibra.engine.solvers.linear_solver import SolverType, initialize_solver

from vibra.project_files.lazy_hdf5_matrix import LazyHDF5MatrixWriter
from vibra.project_files.project_file import ProjectFile

from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.solvers import ModalSolver

import logging
import numpy as np

from time import time


class HarmonicSolver:
    def __init__(self, assembler: AcousticAssembler | StructuralAssembler, project_file: ProjectFile | None = None, **kwargs):
        self.assembler = assembler
        self.project_file = project_file
        self.reset_variables()


    def reset_variables(self):
        self.solution = None
        self.displacement_dof = None

    def solve_direct(self, print_log: bool = False, is_resume: bool = False):
        """
        This method solves the acoustic harmonic analysis using the
        direct method for both damped and undamped problems.

        Parameter
        ---------
        print_log: bool, optional
            This argument controls the printing of the solution steps to the terminal.
        """

        logging.info(f"Solving harmonic analysis (direct method)... [10/100]")

        solution = self._get_solution_handler(is_resume)

        self.compute_frequency_sweep(solution, print_log, is_resume)

        logging.info(f"Solving harmonic analysis (direct method)... [99/100]")
        self._closing_solution_handler(solution)

        return self.solution

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
            self.solution = self.project_file.get_solution_loader()
        else:
            # reinsert the prescribed degrees of freedom into the solution vector
            self.solution = self.assembler.reinsert_the_prescribed_dof(solution)

    def compute_frequency_sweep(self, solution, print_log, is_resume, modes=None):
        # frequencies vector [in hertz]
        frequencies = self.assembler.model.frequencies

        # initialize the solver
        if modes is not None:
            linear_solver = initialize_solver(SolverType.MODAL_SUPERPOSITION, modes=modes)
        elif isinstance(self.assembler, StructuralAssembler):
            linear_solver = initialize_solver(SolverType.PARDISO, is_symmetric=True)
        else:
            linear_solver = initialize_solver(SolverType.PARDISO)
        
        # compute the solution for each frequency step
        for i, freq in enumerate(frequencies):
            logging.info(f"Solution step {i + 1} and frequency {freq} Hz [{i + 1}/{len(frequencies)}]")

            if is_resume and i != 0 and isinstance(solution, LazyHDF5MatrixWriter) and solution.has_column(i):
                continue

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            A, f = self.assembler.build_harmonic_system(freq, i)

            solution_freq = linear_solver.solve(A, f)
            if isinstance(solution, LazyHDF5MatrixWriter):
                # reinsert the prescribed degrees of freedom into the solution vector
                solution_freq = self.assembler.reinsert_the_prescribed_dof_into_solution_freq(solution_freq, i)

            solution[:, i] = solution_freq

            # clear the memory and delete some variables to reduce the memory usage
            linear_solver.clear_memory()
            del A, f

    def solve_mode_superposition(self, print_log: bool = False, is_resume: bool = False, is_proportionally_damped: bool = False):
        logging.info(f"Solving harmonic analysis (mode superposition method)... [10/100]")
        solution = self._get_solution_handler(is_resume)
        
        modal_solver = ModalSolver(self.assembler)
        natural_frequencies, modes = modal_solver.solve(full_solution=False)

        if is_proportionally_damped:
            self.compute_proportionally_damped_frequency_sweep(solution, modes, natural_frequencies, print_log, is_resume)
        else:
            self.compute_frequency_sweep(solution, print_log, is_resume)

        self._closing_solution_handler(solution)

        return self.solution

    def compute_proportionally_damped_frequency_sweep(self, solution, modes, natural_frequencies, print_log, is_resume):
        # frequencies vector [in hertz]
        frequencies = self.assembler.model.frequencies

        (alpha, beta, eta) = self.assembler.model.analysis_setup.get("global_damping", (0, 0, 0))
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
            A = omega_n ** 2 - omega ** 2 + 1j * (omega * (beta * (omega_n ** 2) + alpha) + eta * (omega_n ** 2))
            diag = np.diag(1 / A)

            # compute the solution for each frequency step
            solution_freq = Phi @ (diag @ (Phi_t @ f))

            if isinstance(solution, LazyHDF5MatrixWriter):
                # reinsert the prescribed degrees of freedom into the solution vector
                solution_freq = self.assembler.reinsert_the_prescribed_dof_into_solution_freq(solution_freq, i)

            solution[:, i] = solution_freq