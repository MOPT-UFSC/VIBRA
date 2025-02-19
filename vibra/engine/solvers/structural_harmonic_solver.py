import logging
# import os
import numpy as np
from scipy.sparse.linalg import spsolve
from scipy.sparse import triu

#
# os.environ["OMP_DYNAMIC"] = "FALSE"
# os.environ["OMP_THREAD_LIMIT"] = "8"
# os.environ["OMP_NUM_THREADS"] = "4"
# 

from functools import cache
from pypardiso.pardiso_wrapper import PyPardisoSolver

from vibra.utils.progress_status import ProgressStatus


class StructuralHarmonicSolver:
    def __init__(self, assembler, analysis_data=None):

        self.assembler = assembler

        self.reset_variables()
        self.load_analysis_data(analysis_data)

    def reset_variables(self):
        self.analysis_type = None
        self.frequencies = None
        self.disp_dofs = None
        self.solution_full = None
        self.loads = None
        self.global_damping = (0, 0, 0, 0)

    def load_analysis_data(self, analysis_data):

        if analysis_data is not None:

            if analysis_data["analysis_id"] in [0, 1]:
                self.analysis_type = "structural"
                if "frequencies" in analysis_data.keys():
                    self.frequencies = analysis_data["frequencies"]
                else:
                    self.frequencies = self.assembler.model.frequencies

                self.global_damping = analysis_data.get("global_damping", (0, 0, 0, 0))

    @cache
    def get_max_min_values_of_displacements(self, column: int, disp_type: str):
        """ This method returns the minimum and maximum displacement values
            of selected frequency for animation purposes.

            Parameters:
            -----------
            column: int value relative to frequency column index.

            Returns:
            -----------
            u_min, u_max: float values for minimum and maximum displacements,

        """

        data = self.solution_full[self.displacement_dofs, column]

        amplitudes = np.abs(data)
        phases = np.angle(data)

        r_min = 1
        r_max = 0
        thetas = np.arange(0, 360, 2) * (np.pi / 180)

        for theta in thetas:

            results = (amplitudes * np.cos(phases + theta)).reshape(-1, 3)

            if disp_type == "u_x":
                u_xyz = results * np.array([1.0, 0.0, 0.0])
            elif disp_type == "u_y":
                u_xyz = results * np.array([0.0, 1.0, 0.0])
            elif disp_type == "u_z":
                u_xyz = results * np.array([0.0, 0.0, 1.0])
            else:
                u_xyz = np.linalg.norm(results, axis=1)

            r_min_i = np.min(u_xyz)
            if r_min_i < r_min:
                r_min = r_min_i

            r_max_i = np.max(u_xyz)
            if r_max_i > r_max:
                r_max = r_max_i

        # print("get_max_min_values_of_displacements", r_min, r_max)

        if disp_type == "u_sum":
            return 0., r_max

        else:

            if np.abs(r_min) != np.abs(r_max):
                max_abs = np.max(np.abs([r_min, r_max]))
                r_min = -max_abs
                r_max = max_abs

        return r_min, r_max

    def solve_direct_method(self, print_log=False):
        """ 
        """
        self.get_max_min_values_of_displacements.cache_clear()

        # Note: use mtype=3 for full symmetric complex matrix and mtype=6 for upper triangular complex matrix
        ps = PyPardisoSolver(mtype=6)
        #
        self.unprescribed_dofs_indexes, self.prescribed_dofs_indexes = self.assembler.get_matrices_dropping_indexes()
        self.prescribed_dofs_values, self.array_prescribed_dofs_values = self.assembler.get_prescribed_dofs_values()
        #
        M = self.assembler.mass_matrix
        K = self.assembler.stiffness_matrix
        #
        # self.plot_graph(M)
        #
        alpha_v, beta_v, alpha_h, beta_h = self.global_damping
        F_combined = self.get_prescribed_dofs_model_excitation()
        #
        rows = K.shape[0]
        cols = len(self.frequencies)
        solution = np.zeros((rows, cols), dtype=complex)
        #
        logging.info( "Solving harmonic analysis..." + ProgressStatus(0, len(self.frequencies)))

        for i, freq in enumerate(self.frequencies):

            message = f"Solution step {i+1} and frequency {freq} Hz"
            logging.info( message + ProgressStatus(i, len(self.frequencies)))

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            omega = 2 * np.pi * freq

            F = F_combined[:, i]

            C = 1j * ((beta_h + omega * beta_v) * K + (alpha_h + omega * alpha_v) * M)
            A = K - (omega**2) * M + 1j * omega * C

            A = triu(A, format="csr")
            # ps.factorize(A)

            # solution[:, i] = spsolve(A, F)
            solution[:, i] = ps.solve(A, F)
            ps.free_memory(everything=True)
            del A, F

        self._reinsert_prescribed_dofs(solution)
    
    def solve_mode_superposition_method(self, print_log=False):
        """ 
        """
        self.get_max_min_values_of_displacements.cache_clear()
        #TODO: to be implemented

    def _reinsert_prescribed_dofs(self, solution):
        """
        This method reinsert the value of the prescribed degree of freedom in the solution.

        Parameters
        ----------
        solution : array
            Solution data from the direct method, modal superposition or modal shapes from modal analysis.

        Returns
        ----------
        array
            Solution of all the degrees of freedom.
        """

        rows = self.assembler.n_dofs
        cols = solution.shape[1]
        full_solution = np.zeros((rows, cols), dtype=complex)

        self.displacement_dofs = self.assembler.displacement_dofs

        if len(self.prescribed_dofs_indexes):
            full_solution[self.prescribed_dofs_indexes, :] = self.array_prescribed_dofs_values[:, 0:cols]

        if len(self.assembler.active_2d_element_dofs):
            unprescribed_shell_dofs = self.assembler.unprescribed_shell_dofs
            full_solution[unprescribed_shell_dofs, :] = solution
            self.solution_full = full_solution
            # print("reinserted dofs -> ", len(self.displacement_dofs))

        else:
            full_solution[self.unprescribed_dofs_indexes, :] = solution
            self.solution_full = full_solution
    
    def get_prescribed_dofs_model_excitation(self, freq_dependent=False, index=0):
        """
        This method adds the effects of prescribed acoustic pressure into mass flow global vector.

        Returns
        ----------
        array
            F_eq. Each column corresponds to a frequency of analysis.
        """

        nodal_lodas = self.assembler.nodal_loads

        if np.sum(self.array_prescribed_dofs_values) == 0:
            return nodal_lodas

        Kr = (self.assembler.stiffness_matrix_r.toarray())[self.unprescribed_dofs_indexes, :]
        Mr = (self.assembler.mass_matrix_r.toarray())[self.unprescribed_dofs_indexes, :]

        alpha_v, beta_v, alpha_h, beta_h = self.global_damping

        logging.info( "Processing prescribed dofs model excitation..." + ProgressStatus(10, len(self.frequencies)))

        rows = Kr.shape[0]
        if freq_dependent:
            cols = 1
            F_eq = np.zeros(rows, dtype=complex)

        else:
            cols = len(self.frequencies)
            F_eq = np.zeros((rows, cols), dtype=complex)

        if len(self.prescribed_dofs_values):

            for i, freq in enumerate(self.frequencies):
                #
                logging.info("Processing prescribed dofs model excitation..." + ProgressStatus(i + 10, len(self.frequencies) + 10))
                #
                Kr_add = np.sum((Kr * self.array_prescribed_dofs_values[:, i]), axis=1)
                Mr_add = np.sum((Mr * self.array_prescribed_dofs_values[:, i]), axis=1)
                #
                omega = 2 * np.pi * freq
                F_Kadd = Kr_add
                F_Madd = -(omega**2) * Mr_add
                F_Cadd = 1j * ((beta_h + omega * beta_v) * Kr_add + (alpha_h + omega * alpha_v) * Mr_add)
                F_eq[:, i] = F_Madd + F_Cadd + F_Kadd

            logging.info("Processing prescribed dofs model excitation..." + ProgressStatus(100, 100))

        F_combined = nodal_lodas - F_eq

        return F_combined

    def plot_graph(self, matrix):
        """
        """
        import matplotlib.pyplot as plt
        plt.ion()
        plt.cla()
        plt.spy(matrix, color=(0.25,0.25,0.25))
        plt.show()