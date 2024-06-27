import logging
import os
import numpy as np
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
#
# os.environ["OMP_DYNAMIC"] = "FALSE"
# os.environ["OMP_THREAD_LIMIT"] = "8"
# os.environ["OMP_NUM_THREADS"] = "4"
# 
from pypardiso import *

from vibra.utils.progress_status import ProgressStatus


class AcousticHarmonicSolver:
    def __init__(self, assembler, analysis_data=None):
        #
        self.assembler = assembler
        #
        self.reset_variables()
        self.load_analysis_data(analysis_data)

    def reset_variables(self):
        self.analysis_type = None
        self.frequencies = None
        self.dissipation_model = None
        self.modal_shape = None
        self.solution = None
        self.loads = None

    def load_analysis_data(self, analysis_data):
        if analysis_data is not None:
            if analysis_data["analysis_id"] == 3:
                self.analysis_type = "acoustic"
                if "frequencies" in analysis_data.keys():
                    self.frequencies = analysis_data["frequencies"]

    def load_dissipation_model(self, data):
        self.dissipation_model = data

    def get_max_min_values_of_pressures(self, column):
        """ This method returns the minimum and maximum pressure values
            of selected frequency for animation purposes.

            Parameters:
            -----------
            column: int value relative to frequency column index.

            Returns:
            -----------
            p_min, p_max: float values for minimum and maximum pressures,

        """
        data = self.solution[:, column]

        amplitudes = np.abs(data)
        phases = np.angle(data)

        p_min = 1
        p_max = 0
        thetas = np.arange(0, 360, 2) * (np.pi / 180)

        for theta in thetas:
            pressures = amplitudes * np.cos(phases + theta)

            p_min_i = min(pressures)
            p_max_i = max(pressures)

            if p_min_i < p_min:
                p_min = p_min_i
            if p_max_i > p_max:
                p_max = p_max_i

        return p_min, p_max

    def solve(self, print_log=False):
        """ """
        ps = PyPardisoSolver(mtype=3)
        #
        self.unprescribed_indexes, self.prescribed_indexes = self.assembler.get_matrices_dropping_indexes()
        #
        M = self.assembler.mass_matrix
        K = self.assembler.stiffness_matrix
        #
        C_imp = self.assembler.damping_matrix
        C_visc = self.assembler.visc_damping_matrix
        Q = self.assembler.mass_flow_vectors
        Q_visc = self.assembler.Qvisc_damping_matrix*0
        # np.savetxt("mass_flow_vectors.dat", Q)
        #
        # self.plot_graph(M)

        freq_dependent = False
        condition = self.assembler.model.lrf_properties or self.assembler.model.porous_material_properties
        if condition:
            freq_dependent = True
        else:
            F_eq = self.get_prescribed_pressure_model_excitation()

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

            if freq_dependent:
                self.assembler.assemble_global_mass_matrix(index=i)
                F_eq = self.get_prescribed_pressure_model_excitation(freq_dependent=True, index=i)
                M = self.assembler.mass_matrix
                F = Q_visc @ Q[:, i] - 1j * omega * Q[:, i] - F_eq
            else:
                F = Q_visc @ Q[:, i] - 1j * omega * Q[:, i] - F_eq[:, i]

            C = C_imp[i] + C_visc
            A = K - (omega**2) * M + 1j * omega * C

            # solution[:, i] = spsolve(A, F)
            solution[:, i] = ps.solve(A, F)

        self.solution = self._reinsert_prescribed_dofs(solution)

        return self.solution

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
        rows = solution.shape[0] + len(self.prescribed_indexes)
        cols = solution.shape[1]

        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[self.unprescribed_indexes, :] = solution

        if len(self.prescribed_indexes) > 0:
            full_solution[self.prescribed_indexes, :] = self.array_prescribed_values[:, 0:cols]

        return full_solution
    
    def get_prescribed_pressure_model_excitation(self, freq_dependent=False, index=0):
        """
        This method adds the effects of prescribed acoustic pressure into mass flow global vector.

        Returns
        ----------
        array
            F_eq. Each column corresponds to a frequency of analysis.
        """

        # logging.info("Processing prescribed pressure model excitation..." + ProgressStatus(0, len(self.frequencies)))
        self.prescribed_values, self.array_prescribed_values = self.assembler.get_prescribed_values()
        #
        Kr = (self.assembler.stiffness_matrix_r.toarray())[self.unprescribed_indexes, :]
        Mr = (self.assembler.mass_matrix_r.toarray())[self.unprescribed_indexes, :]
        Cr_visc = (self.assembler.visc_damping_matrix_r.toarray())[self.unprescribed_indexes, :]

        # logging.info( "Processing prescribed pressure model excitation..." + ProgressStatus(10, len(self.frequencies)))

        rows = Kr.shape[0]
        if freq_dependent:
            cols = 1
            F_eq = np.zeros(rows, dtype=complex)
        else:
            cols = len(self.frequencies)
            F_eq = np.zeros((rows,cols), dtype=complex)

        nf = len(self.frequencies)
        aux_ones = np.ones(nf, dtype=complex)

        if len(self.prescribed_values) != 0:
            list_prescribed_values = list()

            for value in self.prescribed_values:
                if isinstance(value, complex):
                    list_prescribed_values.append(aux_ones*value)
                elif isinstance(value, np.ndarray):
                    list_prescribed_values.append(value)
      
            self.array_prescribed_values = np.array(list_prescribed_values)

            if freq_dependent:
                # logging.info("Processing prescribed pressure model excitation..." + ProgressStatus(index + 10, len(self.frequencies) + 10))

                Cr = (self.assembler.damping_matrix_r[index].toarray())[self.unprescribed_indexes, :]
                #
                Kr_add = np.sum((Kr * self.array_prescribed_values[:, index]), axis=1)
                Mr_add = np.sum((Mr * self.array_prescribed_values[:, index]), axis=1)
                Cr_add = np.sum(((Cr + Cr_visc) * self.array_prescribed_values[:, index]), axis=1)
                #
                omega = 2*np.pi*self.frequencies[index]
                F_Kadd = Kr_add
                F_Madd = (-(omega**2))*Mr_add 
                F_Cadd = 1j*omega*Cr_add
                F_eq = F_Kadd + F_Madd + F_Cadd
            
            else:
               
                for i, freq in enumerate(self.frequencies):
                    #
                    logging.info("Processing prescribed pressure model excitation..." + ProgressStatus(i + 10, len(self.frequencies) + 10))

                    Cr = (self.assembler.damping_matrix_r[i].toarray())[self.unprescribed_indexes, :]
                    #
                    Kr_add = np.sum((Kr * self.array_prescribed_values[:, i]), axis=1)
                    Mr_add = np.sum((Mr * self.array_prescribed_values[:, i]), axis=1)
                    Cr_add = np.sum(((Cr + Cr_visc) * self.array_prescribed_values[:, i]), axis=1)
                    #
                    omega = 2*np.pi*freq
                    F_Kadd = Kr_add
                    F_Madd = (-(omega**2))*Mr_add 
                    F_Cadd = 1j*omega*Cr_add
                    F_eq[:, i] = F_Kadd + F_Madd + F_Cadd

                logging.info("Processing prescribed pressure model excitation..." + ProgressStatus(100, 100))

        return F_eq

    def plot_graph(self, matrix):
        """
        """
        plt.ion()
        plt.cla()
        plt.spy(matrix, color=(0.25,0.25,0.25))
        plt.show()