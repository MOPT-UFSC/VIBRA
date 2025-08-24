
from vibra.engine import AnalysisID
from vibra.engine.solvers.linear_solver import SolverType, initialize_solver
from vibra.engine.properties.fluid import Fluid

from typing import TYPE_CHECKING

from vibra.project_files.lazy_hdf5_matrix import LazyHDF5MatrixWriter, LazyHDF5MatrixLoader
from vibra.project_files.project_file import ProjectFile

if TYPE_CHECKING:
    from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler

import logging
import numpy as np

from functools import cache
from time import time

class AcousticHarmonicSolver:
    def __init__(self, assembler: "AcousticAssembler", project_file: ProjectFile | None = None, **kwargs):
        self.assembler = assembler
        self.project_file = project_file
        self.reset_variables()


    def reset_variables(self):
        self.loads = None
        self.solution = None
        self.dissipation_model = None
        self.analysis_type = "acoustic"


    def load_dissipation_model(self, data):
        self.dissipation_model = data


    @cache
    def get_min_max_values_of_pressures(self, column: int, plot_type: str):
        """ 
        This method returns the minimum and maximum pressure values
        of selected frequency used in the animation processing.

        Parameters
        ----------
        column: int value relative to frequency column index.

        Returns
        -------
        p_min, p_max: float values for minimum and maximum pressures,

        """
    
        data = self.solution[:, column]

        amplitudes = np.abs(data)
        phases = np.angle(data)

        p_min = 1
        p_max = 0

        divisions = 36
        thetas = np.linspace(0, 2 * np.pi, divisions + 1, endpoint=True)

        if plot_type == "absolute_values":
            return 0, max(np.abs(data))

        if plot_type == "real_values":
            return min(np.real(data)), max(np.real(data))

        if plot_type == "imag_values":
            return min(np.imag(data)), max(np.imag(data))

        for theta in thetas:
            pressures = amplitudes * np.cos(theta + phases)

            if plot_type == "absolute_animation":
                pressures = np.abs(pressures)

            p_min_i = min(pressures)
            p_max_i = max(pressures)

            if p_min_i < p_min:
                p_min = p_min_i
            if p_max_i > p_max:
                p_max = p_max_i

        if plot_type == "absolute_animation":
            p_min = 0

        if plot_type == "non_absolute_animation":
            max_value = np.max(np.abs([p_min, p_max]))
            p_min = -max_value
            p_max = max_value

        return p_min, p_max


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
            self.solution = self.reinsert_the_prescribed_dof_into_solution_matrix(solution)

        return self.solution

    def compute_frequency_sweep(self, solution, print_log, is_resume):
        self.get_min_max_values_of_pressures.cache_clear()

        # mass and stiffness matrices
        M = self.assembler.mass_matrix
        K = self.assembler.stiffness_matrix

        # damping matrices
        C_imp = self.assembler.damping_matrix
        C_visc = self.assembler.visc_damping_matrix

        # mass flow load vector
        f_Q = self.assembler.mass_flow_vectors

        # frequencies vector [in hertz]
        frequencies = self.assembler.model.frequencies

        # process the prescribed and unprescribed indexes
        self.unprescribed_indexes, self.prescribed_indexes = self.assembler.get_matrices_dropping_indexes()

        # process the prescribed values
        self.prescribed_values, self.array_prescribed_values = self.assembler.get_prescribed_dof_values()

        frequency_dependent = self.assembler.frequency_dependent
        
        # initialize the solver
        linear_solver = initialize_solver(SolverType.PARDISO)
        
        for i, freq in enumerate(frequencies):
            logging.info(f"Solution step {i + 1} and frequency {freq} Hz [{i + 1}/{len(frequencies)}]")

            if is_resume and i != 0 and isinstance(solution, LazyHDF5MatrixWriter) and solution.has_column(i):
                continue

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            # create the frequency vector
            omega = 2 * np.pi * freq

            # update the damping matrix [C]
            self.assembler.assemble_global_damping_matrix_2d_elements(index=i)
            C_imp = self.assembler.damping_matrix
            C = C_imp + C_visc

            if frequency_dependent:
                # reassemble the global mass and stiffness matrices
                factor_K, factor_M = self.assembler.compute_global_matrices_factors(index=i)
                self.assembler.assemble_global_mass_matrix(factor_M)
                self.assembler.assemble_global_stiffness_matrix(factor_K)

                M = self.assembler.mass_matrix
                K = self.assembler.stiffness_matrix

                # reassemble the mass source matrices
                self.assembler.assemble_mass_source_matrices_from_surfaces(index=i)
                self.assembler.assemble_mass_source_matrices_from_volumes(index=i)

            # update the prescribed dofs-related load vector for each frequency step
            f_eq = self.assembler.get_prescribed_pressure_model_excitation(self.array_prescribed_values, index=i)

            # compute the mass source load vector
            f_Qms = self.assembler.compute_mass_source_load_vector(omega, index=i)

            # define the linear system equation terms [A]{x} = {f}
            A = K - (omega**2) * M + 1j * omega * C
            f = f_Qms - 1j * omega * f_Q[:, i] - f_eq

            # compute the solution for each frequency step
            solution_freq = linear_solver.solve(A, f)
            if isinstance(solution, LazyHDF5MatrixWriter):
                # reinsert the prescribed degrees of freedom into the solution vector
                solution_freq = self.reinsert_the_prescribed_dof_into_solution_freq(solution_freq, i)

            solution[:, i] = solution_freq

            # clear the memory and delete some variables to reduce the memory usage
            linear_solver.clear_memory()
            del A, f

    def reinsert_the_prescribed_dof_into_solution_matrix(self, solution: np.ndarray):
        """
        This method reinserts the value of the prescribed degree of freedom in the solution array.

        Parameters
        ----------
        solution : np.ndarray
            Solution data obtained from harmonic analysis using the direct method.

        Returns
        -------
        full_solution: np.ndarray
            An array that contains the solution of all the degrees of freedom.
        """
        rows = solution.shape[0] + len(self.prescribed_indexes)
        cols = solution.shape[1]

        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[self.unprescribed_indexes, :] = solution

        if len(self.prescribed_indexes):
            full_solution[self.prescribed_indexes, :] = self.array_prescribed_values[:, 0:cols]

        return full_solution

    def reinsert_the_prescribed_dof_into_solution_freq(self, solution: np.ndarray, freq_index: int):
        """
        This method reinserts the value of the prescribed degree of freedom in the solution array.

        Parameters
        ----------
        solution : np.ndarray
            Solution data obtained from harmonic analysis using the direct method.
        freq_index: int
            Frequency index related to the input solution.

        Returns
        -------
        full_solution: np.ndarray
            An array that contains the solution of all the degrees of freedom.
        """
        rows = solution.shape[0] + len(self.prescribed_indexes)

        full_solution = np.zeros(rows, dtype=complex)
        full_solution[self.unprescribed_indexes] = solution

        if len(self.prescribed_indexes):
            full_solution[self.prescribed_indexes] = self.array_prescribed_values[:, freq_index]

        return full_solution