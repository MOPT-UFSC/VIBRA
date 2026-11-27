import logging
import sys
from time import time
from typing import Optional

import h5py
import numpy as np
from tqdm import tqdm

from vibra.engine.analysis_info import HarmonicAnalysisSetup
from vibra.engine.assemblers.acoustic.acoustic_assembler import AcousticAssembler
from vibra.engine.assemblers.structural.structural_assembler import StructuralAssembler
from vibra.engine.serialization.lazy_hdf5_matrix import LazyHDF5MatrixWriter
from vibra.engine.serialization.project_paths import ProjectPaths
from vibra.engine.solution import HarmonicSolution
from vibra.engine.solvers import ModalSolver
from vibra.engine.solvers.linear_solver import LinearSolver, SolverType, initialize_solver


class StaticSolver:
    def __init__(
        self,
        assembler: AcousticAssembler | StructuralAssembler,
        project_paths: ProjectPaths | None = None,
    ):

        self.assembler = assembler
        self.project_paths = project_paths

        self.reset_variables()

    @property
    def model(self):
        return self.assembler.model

    @property
    def frequencies(self) -> np.ndarray:
        return self.assembler.model.frequencies

    @property
    def total_dofs(self) -> int:
        if isinstance(self.assembler, AcousticAssembler):
            return len(self.assembler.acoustic_dofs_indices)
        elif isinstance(self.assembler, StructuralAssembler):
            return len(self.assembler.structural_dofs_indices)
        else:
            return -1

    def reset_variables(self):
        self.solution: Optional[HarmonicSolution] = None
        self.nodal_solution: Optional[np.ndarray] = None
        self.displacement_dof: Optional[np.ndarray] = None
        self._linear_solver: Optional[LinearSolver] = None
        self._file_writer: Optional[LazyHDF5MatrixWriter] = None

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

        nodal_solution_buffer = self._get_nodal_solution_buffer(is_resume)
        self.compute_frequency_sweep(nodal_solution_buffer, print_log, is_resume)

        logging.info("Solving harmonic analysis (direct method)... [99/100]")

        if isinstance(self.assembler, StructuralAssembler):
            self.displacement_dof = self.assembler.displacement_dof

            if isinstance(self.model.solution, HarmonicSolution) and self.model.analysis_id.is_coupled():
                acoustic_solution = self.model.solution.acoustic_solution
            else:
                acoustic_solution = None

            self.solution = HarmonicSolution(
                analysis_id=self.model.analysis_id,
                frequencies=self.model.frequencies,
                structural_solution=nodal_solution_buffer,
                acoustic_solution=acoustic_solution,
                displacement_dof=self.assembler.displacement_dof,
            )

        elif isinstance(self.assembler, AcousticAssembler):
            self.solution = HarmonicSolution(
                analysis_id=self.model.analysis_id,
                frequencies=self.model.frequencies,
                acoustic_solution=nodal_solution_buffer,
            )

        else:
            raise ValueError(f"Unsupported assembler type: {type(self.assembler)}")

        if self.model.stop_processing:
            self.solution = None
            return self.solution

        return self.solution

    def compute_frequency_sweep(
        self,
        nodal_solution_buffer: np.ndarray,
        print_log: bool,
    ):

        if isinstance(self.assembler, AcousticAssembler):
            analysis_label = "acoustic static analysis"
        else:
            analysis_label = "structural static analysis"

        if self.assembler.model.stop_processing:
            return

        # if isinstance(self._file_writer, LazyHDF5MatrixWriter) and self._file_writer.has_column(0):
        #     continue

        linear_solver = self._get_linear_solver()

        # compute the dynamic stiffness matrix
        Ks = self.assembler.compute_static_stiffness_matrix()

        # compute the load vector
        f = self.assembler.compute_load_vector(0)

        # reset global matrices attributes
        if self.model.reduced_memory_mode:
            self.assembler.reset_global_matrices_attributes()

        logging.info(f"Solving the {analysis_label} [25/100]")

        if np.any(f):

            is_complex = np.any(np.iscomplex(Ks.data)) or np.any(np.iscomplex(f))
            if not is_complex:
                Ks.data = np.real(Ks.data)
                f = np.real(f)

            # solve the linear system
            solution_freq = linear_solver.solve(Ks, f)

            # delete some variables and clear the memory to reduce the memory usage
            linear_solver.clear_memory()
            del Ks

        else:
            # We will have the trivial solution whenever there is no excitation
            solution_freq = np.zeros_like(f, dtype=np.complex128)

        del f

        solution_freq = self.assembler.reinsert_the_prescribed_dof_into_solution_freq(solution_freq, i)
        nodal_solution_buffer[:, i] = solution_freq

    def _get_linear_solver(self) -> LinearSolver:
        if self._linear_solver is None:
            if isinstance(self.assembler, StructuralAssembler):
                linear_solver = initialize_solver(SolverType.PARDISO, is_symmetric=True)
            else:
                linear_solver = initialize_solver(SolverType.PARDISO)

        if self._linear_solver is not None:
            return self._linear_solver

        self._linear_solver = linear_solver
        return linear_solver

    def _initialize_file_writer(self, is_resume: bool):
        if self.project_paths is None:
            return

        self._file_writer = LazyHDF5MatrixWriter(
            self.project_paths.harmonic_solution_filepath,
            self.total_dofs,
            self.assembler.frequencies,
            dtype=np.complex128,
            is_resume=is_resume,
        )

        if self.displacement_dof is not None:
            self._file_writer.save_extra_data("displacement_dof", self.displacement_dof, dtype=int)

    def _close_file_writer(self):
        if self._file_writer is None:
            return

        self._file_writer.close()
        self._file_writer = None

    def _get_nodal_solution_buffer(self, is_resume: bool):
        if is_resume and (self.project_paths is not None):
            # loads partial solution to be used as an in-memory buffer
            with h5py.File(self.project_paths.harmonic_solution_filepath, "r") as file:
                return np.array(file["solution"])

        num_rows = self.total_dofs
        solution = np.zeros((num_rows, 1), dtype=np.complex128)

        return solution