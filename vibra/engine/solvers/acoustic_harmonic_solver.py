from vibra.engine.solvers.linear_solver import SolverType, initialize_solver

from typing import TYPE_CHECKING

from vibra.project_files.lazy_hdf5_matrix import LazyHDF5MatrixWriter, LazyHDF5MatrixLoader
from vibra.project_files.project_file import ProjectFile

if TYPE_CHECKING:
    from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler

import logging
import numpy as np

from time import time


class AcousticHarmonicSolver:
    def __init__(self, assembler: "AcousticAssembler", project_file: ProjectFile | None = None, **kwargs):
        self.assembler = assembler
        self.project_file = project_file
        self.reset_variables()


    def reset_variables(self):
        self.solution = None

    def solve(self, print_log: bool = False, is_resume: bool = False):
        """
        This method solves the acoustic harmonic analysis using the
        direct method for both damped and undamped problems.

        Parameter
        ---------
        print_log: bool, optional
            This argument controls the printing of the solution steps to the terminal.
        """

        logging.info(f"Solving harmonic analysis (direct method)... [10/100]")

        frequencies = self.assembler.model.frequencies

        if self.project_file:
            num_rows = self.assembler.total_dof
            solution = self.project_file.get_solution_writer(num_rows, frequencies, dtype=complex, is_resume=is_resume)
        else:
            num_rows = self.assembler.stiffness_matrix.shape[0]
            solution = np.zeros((num_rows, len(frequencies)), dtype=complex)

        self.compute_frequency_sweep(solution, print_log, is_resume)

        logging.info(f"Solving harmonic analysis (direct method)... [99/100]")
        if isinstance(solution, LazyHDF5MatrixWriter):
            solution.close()
            self.solution = self.project_file.get_solution_loader()
        else:
            # reinsert the prescribed degrees of freedom into the solution vector
            self.solution = self.assembler.reinsert_the_prescribed_dofs_into_solution_matrix(solution)

        return self.solution

    def compute_frequency_sweep(self, solution, print_log, is_resume):
        # frequencies vector [in hertz]
        frequencies = self.assembler.model.frequencies

        # initialize the solver
        linear_solver = initialize_solver(SolverType.PARDISO)
        
        for i, freq in enumerate(frequencies):
            logging.info(f"Solution step {i + 1} and frequency {freq} Hz [{i + 1}/{len(frequencies)}]")

            if is_resume and i != 0 and isinstance(solution, LazyHDF5MatrixWriter) and solution.has_column(i):
                continue

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            A, f = self.assembler.build_harmonic_system(freq, i)

            # compute the solution for each frequency step
            solution_freq = linear_solver.solve(A, f)
            if isinstance(solution, LazyHDF5MatrixWriter):
                # reinsert the prescribed degrees of freedom into the solution vector
                solution_freq = self.assembler.reinsert_the_prescribed_dofs_into_solution_freq(solution_freq, i)

            solution[:, i] = solution_freq

            # clear the memory and delete some variables to reduce the memory usage
            linear_solver.clear_memory()
            del A, f
