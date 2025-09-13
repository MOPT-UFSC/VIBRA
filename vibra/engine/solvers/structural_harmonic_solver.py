from vibra.engine.solvers.linear_solver import initialize_solver, SolverType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.assemblers.structural_assembler import StructuralAssembler

import logging
import numpy as np


class StructuralHarmonicSolver:
    def __init__(self, assembler: "StructuralAssembler", **kwargs):
        self.assembler = assembler
        self.reset_variables()

    def reset_variables(self):
        self.solution = None
        self.displacement_dofs = None

    def solve_direct_method(self, print_log=False):
        """ This method solves the structural harmonic analysis for both damped and undamped problems.
        """
        frequencies = self.assembler.model.frequencies

        rows = self.assembler.stiffness_matrix.shape[0]
        cols = len(frequencies)
        solution = np.zeros((rows, cols), dtype=complex)

        logging.info(f"Solving harmonic analysis... [0/{len(frequencies)}]")

        linear_solver = initialize_solver(SolverType.PARDISO)

        for i, freq in enumerate(frequencies):
            logging.info(f"Solution step {i+1} and frequency {freq} Hz [{i}/{cols}]")

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            A, f = self.assembler.build_harmonic_system(freq, i)

            solution[:, i] = linear_solver.solve(A, f)

            linear_solver.clear_memory()
            del A, f

        self.solution = self.assembler.reinsert_the_prescribed_dofs(solution)
        self.displacement_dofs = self.assembler.displacement_dofs


    def solve_mode_superposition_method(self, print_log=False):
        """ 
        """
        #TODO: to be implemented

