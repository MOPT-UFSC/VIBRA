import logging
from time import time
from typing import Optional

import h5py
import numpy as np

from vibra.engine.analysis_info import HarmonicAnalysisSetup
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.serialization.lazy_hdf5_matrix import LazyHDF5MatrixWriter
from vibra.engine.serialization.project_paths import ProjectPaths
from vibra.engine.solution import HarmonicSolution
from vibra.engine.solution.lazy_harmonic_solution import LazyHarmonicSolution
from vibra.engine.solvers import ModalSolver
from vibra.engine.solvers.linear_solver import LinearSolver, SolverType, initialize_solver


class HarmonicSolver:
    def __init__(
        self,
        assembler: AcousticAssembler | StructuralAssembler,
        project_paths: ProjectPaths | None = None,
    ):

        self.assembler = assembler
        self.project_paths = project_paths

        self.reset_variables()

    @property
    def frequencies(self) -> np.ndarray:
        return self.assembler.model.frequencies

    @property
    def total_dofs(self) -> int:
        if isinstance(self.assembler, AcousticAssembler):
            return self.assembler.acoustic_ndofs
        elif isinstance(self.assembler, StructuralAssembler):
            return self.assembler.structural_ndofs          

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

        if isinstance(self.assembler, StructuralAssembler):
            self.displacement_dof = self.assembler.displacement_dof

        nodal_solution_buffer = self._get_nodal_solution_buffer(is_resume)

        self._initialize_file_writer(is_resume)
        self.compute_frequency_sweep(nodal_solution_buffer, print_log, is_resume)
        self._close_file_writer()

        logging.info("Solving harmonic analysis (direct method)... [99/100]")

        self.solution = HarmonicSolution(
            analysis_id=self.assembler.model.analysis_id,
            frequencies=self.assembler.model.frequencies,
            nodal_solution=nodal_solution_buffer,
            displacement_dof=self.displacement_dof,
        )

        if self.assembler.model.stop_processing:
            self.solution = None
            return self.solution

        return self.solution

    def compute_frequency_sweep(
        self,
        nodal_solution_buffer: np.ndarray,
        print_log: bool,
        is_resume: bool,
        eigenvectors=None,
    ):

        # frequencies vector [in hertz]
        frequencies = self.frequencies

        # compute the solution for each frequency step
        for i, freq in enumerate(frequencies):
            if self.assembler.model.stop_processing:
                return

            logging.info(f"Solution step {i + 1} and frequency {freq} Hz [{i + 1}/{len(frequencies)}]")

            if is_resume and (i != 0) and isinstance(self._file_writer, LazyHDF5MatrixWriter) and self._file_writer.has_column(i):
                continue

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            A, f = self.assembler.build_harmonic_system(freq, i)

            if freq == 0:
                # In case of freq=0, the matrix may differ from the non-zero frequencies,
                # so we solve it with a particular linear solver
                linear_solver = self._get_linear_solver(eigenvectors, new_instance=True)
            else:
                linear_solver = self._get_linear_solver(eigenvectors)

            solution_freq = linear_solver.solve(A, f)
            solution_freq = self.assembler.reinsert_the_prescribed_dof_into_solution_freq(solution_freq, i)
            nodal_solution_buffer[:, i] = solution_freq

            if self._file_writer is not None:
                self._file_writer[:, i] = solution_freq

            # clear the memory and delete some variables to reduce the memory usage
            linear_solver.clear_memory()
            del A, f

    def solve_mode_superposition(
        self,
        print_log: bool = False,
        is_resume: bool = False,
        is_proportionally_damped: bool = False,
    ) -> HarmonicSolution:

        logging.info("Solving harmonic analysis (mode superposition method)... [10/100]")

        t0 = time()
        modal_solver = ModalSolver(self.assembler)
        modal_solution = modal_solver.solve(full_solution=False)
        dt = time() - t0
        print(f"Elapsed time to solve modal analysis: {dt: .6f} [s]")

        nodal_solution_buffer = self._get_nodal_solution_buffer(is_resume)
        self._initialize_file_writer(is_resume)

        if is_proportionally_damped:
            self.compute_proportionally_damped_frequency_sweep(
                nodal_solution_buffer,
                modal_solution.modal_shapes,
                modal_solution.natural_frequencies,
                print_log,
                is_resume,
            )

        else:
            self.compute_frequency_sweep(
                nodal_solution_buffer,
                print_log,
                is_resume,
            )

        self._close_file_writer()
        self.solution = HarmonicSolution(
            analysis_id=self.assembler.model.analysis_id,
            frequencies=self.assembler.model.frequencies,
            nodal_solution=nodal_solution_buffer,
            displacement_dof=self.displacement_dof,
        )

        return self.solution

    def compute_proportionally_damped_frequency_sweep(
        self,
        nodal_solution_buffer: np.ndarray,
        modal_shapes: np.ndarray,
        natural_frequencies: np.ndarray,
        print_log: bool,
        is_resume: bool,
    ):
        # frequencies vector [in hertz]
        frequencies = self.frequencies

        analysis_setup = self.assembler.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        # load the global damping parameters
        alpha, beta, eta = self.assembler.model.global_damping

        # vector of natural frequencies in rad/s
        omega_n = 2 * np.pi * natural_frequencies

        # Phi is the matrix of the eigenvectors
        Phi = modal_shapes
        Phi_t = Phi.T

        # compute the solution for each frequency step
        for i, freq in enumerate(frequencies):
            logging.info(f"Solution step {i + 1} and frequency {freq} Hz [{i + 1}/{len(frequencies)}]")

            if is_resume and i != 0 and isinstance(self._file_writer, LazyHDF5MatrixWriter) and self._file_writer.has_column(i):
                continue

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            f = self.assembler.get_combined_nodal_loads_vector(index=i)

            omega = 2 * np.pi * freq
            A = omega_n**2 - omega**2 + 1j * (omega * (beta * (omega_n**2) + alpha) + eta * (omega_n**2))
            diag = np.diag(1 / A)

            # compute the solution for each frequency step
            solution_freq = Phi @ (diag @ (Phi_t @ f))
            solution_freq = self.assembler.reinsert_the_prescribed_dof_into_solution_freq(solution_freq, i)
            nodal_solution_buffer[:, i] = solution_freq

            if isinstance(self._file_writer, LazyHDF5MatrixWriter):
                self._file_writer[:, i] = solution_freq

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

    def _initialize_file_writer(self, is_resume: bool):
        if self.project_paths is None:
            return

        self._file_writer = LazyHDF5MatrixWriter(
            self.project_paths.harmonic_solution_filepath,
            self.total_dofs,
            self.assembler.frequencies,
            dtype=complex,
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
        num_cols = len(self.assembler.frequencies)

        solution = np.zeros((num_rows, num_cols), dtype=complex)
        return solution
