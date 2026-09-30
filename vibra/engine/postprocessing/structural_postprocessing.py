from __future__ import annotations

import logging
from collections import defaultdict
from functools import cache
from time import perf_counter

import numpy as np

from vibra.engine.model import Model
from vibra.engine.postprocessing.structural.minimum_and_maximum_values_processor import MinimumAndMaximumValuesProcessor
from vibra.engine.properties.material import Material
from vibra.engine.solution import HarmonicSolution, LazyHarmonicSolution, ModalSolution
from vibra.interface.viewer_3d.plot_setup import DisplacementDataType, StressDataType, StressType
from vibra.utils.signal_processing import process_multiple_iffts_from_one_sided_spectrum_signals


class StructuralPostprocessing:
    def __init__(self, model: Model):
        if not isinstance(model, Model):
            raise ValueError("The model argument must be of type Model.")

        self.model = model

        self.reset_attributes()

        # initialize the minimum/maximum values processor
        self.min_max_processor = MinimumAndMaximumValuesProcessor(self)


    @property
    def mesh(self):
        return self.model.mesh


    @property
    def solution(self):
        return self.model.solution


    @property
    def structural_element_2d(self):
        if self.model.structural_element_2d is None:
            self.model.set_structural_elements()
        return self.model.structural_element_2d


    @property
    def structural_element_3d(self):
        if self.model.structural_element_3d is None:
            self.model.set_structural_elements()
        return self.model.structural_element_3d


    def reset_attributes(self):
        self.time_vector = None
        self.nodal_solution_time = None
        self.nodal_averaged_stresses_frequency = None
        self.nodal_averaged_stresses_time = None


    @cache
    def recover_nodal_averaged_structural_stresses(
        self,
        time_domain: bool = False,
        node_ids : int | list[int] | None = None,
        surface_ids: int | list[int] | None = None,
        volume_ids: list[int] | None = None,
        ) -> np.ndarray:

        """
        This method computes the nodal averaged.

        Parameters
        ----------
        time_domain: bool, optional (default is False)
            Set this argument to True if the structural nodal 
            solution is in time domain and False otherwise.

        node_ids: int, list[int], None. (default None)
            The selected node IDs.

        surface_ids: int, list[int], None. (default None)
            The selected surface IDs.

        volume_ids: int, list[int], None. (default None)
            The selected volume IDss.

        Return
        ------
        avg_nodal_stresses: np.ndarray
            A 3D array in which each plane stores the averaged nodal stresses, so that each row
            contains a stress (Sx, Sy, Sz, Txy, Txz, Tyz) and the columns represent the frequencies.

        """

        logging.info("Recovering the structural stresses... (1/3)")

        if time_domain:
            solution = self.nodal_solution_time
            n_steps = solution.shape[1]
            data_type = float
        else:
            solution = None
            n_steps = len(self.model.frequencies)
            data_type = complex

        element_3d = self.structural_element_3d

        if element_3d.connectivities is None:
            element_3d.reorder_connect()

        if all(item is None for item in (node_ids, surface_ids, volume_ids)):
            node_ids = self.model.domains_processor.nodes_of_domain.get("structural", [])
            element_ids = self.model.domains_processor.elements_of_domain.get("structural", [])

        elif isinstance(node_ids, int):
            node_ids = [node_ids]

        elif not isinstance(node_ids, np.ndarray | list):

            node_ids = []
            if isinstance(surface_ids, int):
                surface_ids = [surface_ids]

            if isinstance(surface_ids, list):
                for surface_id in surface_ids:
                    surface_nodes = self.mesh.get_nodes_from_surface(surface_id)
                    node_ids.extend(surface_nodes)

            if isinstance(volume_ids, int):
                volume_ids = [volume_ids]

            if isinstance(volume_ids, list):
                for volume_id in volume_ids:
                    volume_nodes = self.mesh.get_nodes_from_volume(volume_id)
                    node_ids.extend(volume_nodes)

            logging.info("Recovering the structural stresses... (2/3)")
            if isinstance(node_ids, np.ndarray | list):
                node_ids = np.unique(node_ids)
                element_ids = self.model.get_solid_elements_from_nodes(node_ids, "structural")

        # initialize variables
        n_nodes = len(node_ids)
        n_el = len(element_ids)

        corner_indices = element_3d.corner_nodes_indices
        midside_data = element_3d.midside_nodes_indices
        is_quadratic = np.any(midside_data)

        if is_quadratic:
            midside_indices = midside_data[:, 0]
            ind_1 = midside_data[:, 1]
            ind_2 = midside_data[:, 2]

        # initialize variables
        last_progress = 0
        avg_nodal_stresses = np.zeros((n_nodes, 6, n_steps), dtype=data_type)
        _, counts = np.unique(self.mesh.solids_connectivity[element_ids, 4:], return_counts=True)

        # map all elements connectivities
        _connect_flat = self.model.get_mapped_nodes(element_3d.connectivities[element_ids, :].ravel(), "structural")
        _connectivities = _connect_flat.reshape(-1, element_3d.nodes_per_element)

        for i, _connect in enumerate(_connectivities):

            progress = int((100 * (i / n_el) // 5) * 5)
            if progress != last_progress:
                logging.info(f"Calculating the nodal stresses for each element... [{progress}/100]")

            # process the extrapolated nodal stresses
            enodal_stresses = element_3d.process_stresses_at_integration_points(
                element_ids[i],
                solution=solution,
                extrapolate=True,
                )

            # sum the nodal stresses at the corner nodes
            avg_nodal_stresses[_connect[corner_indices], :, :] += enodal_stresses

            # sum the nodal stresses at the midside nodes
            if is_quadratic:
                avg_nodal_stresses[_connect[midside_indices], :, :] += (enodal_stresses[ind_1, :, :] + enodal_stresses[ind_2, :, :]) / 2

        # average the nodal stresses
        avg_nodal_stresses /= counts.reshape(-1, 1, 1)

        return avg_nodal_stresses


    @cache
    def recover_element_structural_stresses(
        self,
        time_domain: bool = False,
        node_ids : int | list[int] | None = None,
        surface_ids: int | list[int] | None = None,
        volume_ids: list[int] | None = None,
        ) -> np.ndarray | None:

        """
        This method computes the nodal stresses for each element.

        Parameters
        ----------
        time_domain: bool, optional (default is False)
            Set this argument to True if the structural nodal 
            solution is in time domain and False otherwise.

        node_ids: int, list[int], None. (default None)
            The selected node IDs.

        surface_ids: int, list[int], None. (default None)
            The selected surface IDs.

        volume_ids: int, list[int], None. (default None)
            The selected volume IDss.

        Return
        ------
        element_stress_data: dict
            A dictionary whose keys are the element_id and the values are the nodal
            stresses for each element (3D array with dimensions: n_nodes x 6 x Nf).

        """

        logging.info("Recovering the structural stresses... (1/3)")

        if time_domain:
            solution = self.nodal_solution_time
            n_steps = solution.shape[1]
            data_type = float
        else:
            solution = None
            n_steps = len(self.model.frequencies)
            data_type = complex

        element_3d = self.structural_element_3d

        if element_3d.connectivities is None:
            element_3d.reorder_connect()

        if all(item is None for item in (node_ids, surface_ids, volume_ids)):
            node_ids = self.model.domains_processor.nodes_of_domain.get("structural", [])
            element_ids = self.model.domains_processor.elements_of_domain.get("structural", [])

        elif isinstance(node_ids, int):
            node_ids = [node_ids]

        elif not isinstance(node_ids, np.ndarray | list):

            node_ids = []
            if isinstance(surface_ids, int):
                surface_ids = [surface_ids]

            if isinstance(surface_ids, list):
                for surface_id in surface_ids:
                    surface_nodes = self.mesh.get_nodes_from_surface(surface_id)
                    node_ids.extend(surface_nodes)

            if isinstance(volume_ids, int):
                volume_ids = [volume_ids]

            if isinstance(volume_ids, list):
                for volume_id in volume_ids:
                    volume_nodes = self.mesh.get_nodes_from_volume(volume_id)
                    node_ids.extend(volume_nodes)

            logging.info("Recovering the structural stresses... (2/3)")
            if isinstance(node_ids, np.ndarray | list):
                node_ids = np.unique(node_ids)
                element_ids = self.model.get_solid_elements_from_nodes(node_ids, "structural")

        # initialize variables
        n_nodes = len(node_ids)
        n_el = len(element_ids)

        midside_data = element_3d.midside_nodes_indices
        is_quadratic = np.any(midside_data)

        if is_quadratic:
            ind_1 = midside_data[:, 1]
            ind_2 = midside_data[:, 2]

        # initialize variables
        last_progress = 0
        element_stress_data = np.zeros((n_el, n_nodes, 6, n_steps), dtype=data_type)

        for i, element_id in enumerate(element_ids):

            progress = int((100 * (i / n_el) // 5) * 5)
            if progress != last_progress:
                logging.info(f"Recovering the structural stresses... [{progress}/100]")

            # process the extrapolated nodal stresses
            enodal_stresses = element_3d.process_stresses_at_integration_points(
                element_id,
                solution=solution,
                extrapolate=True,
                )

            # map the node indexes
            if is_quadratic:
                midside_stresses = (enodal_stresses[ind_1, :, :] + enodal_stresses[ind_2, :, :]) / 2
                element_stress_data[element_id] = np.append(enodal_stresses, midside_stresses, axis=0)
            else:
                element_stress_data[element_id] = enodal_stresses

        return element_stress_data


    @cache
    def compute_multiple_ifft_for_structural_nodal_solution(self, n_diff: int = 0) -> tuple[np.ndarray, np.ndarray]:
        assert isinstance(self.solution, HarmonicSolution)
        assert self.solution.structural_solution is not None
        assert self.solution.analysis_id.is_structural() or self.solution.analysis_id.is_coupled()

        nodal_solution = self.solution.structural_solution.copy()

        # differentiate the nodal solution
        if n_diff:
            freqs = self.model.frequencies
            nodal_solution *= (1j * 2 * np.pi * freqs)**n_diff

        t0 = perf_counter()
        logging.info("Computing the iffts for structural nodal solution... [25/100]")
        self.time_vector, self.nodal_solution_time = process_multiple_iffts_from_one_sided_spectrum_signals(
            self.solution.frequencies,
            nodal_solution,
            dc_included=False,
        )

        logging.info("Computing the iffts for structural nodal solution... [100/100]")

        dt = perf_counter() - t0
        if dt > 0.5:
            print(f"Elapsed time to process the iffts for structural nodal solution: {dt: .6f} s")


    @cache
    def compute_multiple_ifft_for_structural_stresses(self) -> tuple[np.ndarray, np.ndarray]:
        assert isinstance(self.solution, HarmonicSolution)
        assert self.solution.structural_solution is not None
        assert self.solution.analysis_id.is_structural() or self.solution.analysis_id.is_coupled()

        t0 = perf_counter()
        logging.info("Computing the iffts for nodal stresses... [25/100]")
        n_nodes, n_stress, n_freq = self.nodal_averaged_stresses_frequency.shape

        time_vector, waveforms = process_multiple_iffts_from_one_sided_spectrum_signals(
            self.solution.frequencies,
            self.nodal_averaged_stresses_frequency.reshape(-1, n_freq),
            dc_included=False,
        )

        logging.info("Computing the iffts for nodal stresses... [100/100]")

        dt = perf_counter() - t0
        if dt > 0.5:
            print(f"Elapsed time to process the iffts for stresses: {dt: .6f} s")

        return time_vector, waveforms.reshape(n_nodes, n_stress, waveforms.shape[1])


    def compute_structural_stresses_frequency(self):
        t0 = perf_counter()
        self.nodal_averaged_stresses_frequency = self.recover_nodal_averaged_structural_stresses()
        if self.nodal_averaged_stresses_frequency is None:
            return

        dt = perf_counter() - t0
        if dt > 0.5:
            print(f"Time to compute nodal stresses (frequency): {dt} s")


    def compute_structural_stresses_time(self, stress_iffts: bool = True):
        t0 = perf_counter()
        if stress_iffts:
            if self.nodal_averaged_stresses_frequency is None:
                self.compute_structural_stresses_frequency()

            _, self.nodal_averaged_stresses_time = self.compute_multiple_ifft_for_structural_stresses()

        else:
            if self.nodal_solution_time is None:
                self.compute_multiple_ifft_for_structural_nodal_solution()

            self.nodal_averaged_stresses_time = self.recover_nodal_averaged_structural_stresses(time_domain=True)

        dt = perf_counter() - t0
        if dt > 0.5:
            print(f"Time to compute nodal stresses (time): {dt} s")


    def compute_advanced_structural_stresses(self, stresses: np.ndarray, stress_type: StressType):
        """
        Use this method to compute the following advanced nodal stresses: 
        Von Mises, Tresca, Maximum Principal 1, 2 and 3.

        Parameters
        ----------
        stresses: np.ndarray
            A N_steps x 6 2D array with the stress tensor components. 

        stress_type: StressType
            Attribute used to select the stress type. 

        Return
        ------
        stress_vector: np.ndarray
            The stress vector in frequency or time domain.

        """
        if stress_type == StressType.VON_MISES_STRESS:
            stress_vector = np.sqrt((1/2) * (
                (stresses[:, 0] - stresses[:, 1])**2 + 
                (stresses[:, 1] - stresses[:, 2])**2 + 
                (stresses[:, 2] - stresses[:, 0])**2 +
                6 * (stresses[:, 3]**2 + stresses[:, 4]**2 + stresses[:, 5]**2)
                ))

        else:

            """
            stress_tensor = |sigma_x, tau_xy, tau_xz| 
                            |tau_xy, sigma_y, tau_yz|
                            |tau_xz, tau_yz, sigma_z|
            """

            # compute the stress tensor at a specific time/phase (phase_rad = omega * t)
            stress_tensor = stresses[:, [0, 3, 4, 3, 1, 5, 4, 5, 2]].reshape(-1, 3, 3)

            # compute the maximum principal stresses
            eigen_values = np.linalg.eigvalsh(stress_tensor)

            # order the maximum principal stresses
            sigmas = np.sort(eigen_values, axis=1)

            if stress_type == StressType.TRESCA_STRESS:
                stress_vector = sigmas[:, 2] - sigmas[:, 0]  # sigma_1 - sigma_3

            elif stress_type == StressType.MAXIMUM_PRINCIPAL_STRESS_1:
                stress_vector = sigmas[:, 2] # sigma_1

            elif stress_type == StressType.MAXIMUM_PRINCIPAL_STRESS_2:
                stress_vector = sigmas[:, 1] # sigma_2
            
            else:
                stress_vector = sigmas[:, 0] # sigma_3

        return stress_vector


    def compute_displacements_for_3d_plot_frequency(
        self,
        column: int,
        phase_rad: float,
        data_type: DisplacementDataType,
        n_diff: int = 0,
        unit_factor: float = 1.0,
        is_modal: bool = False,
        stress_plot: bool = False,
    ):
        if not isinstance(self.solution, ModalSolution | HarmonicSolution):
            return

        if isinstance(self.solution, LazyHarmonicSolution) and not self.solution.is_valid():
            return

        if is_modal:
            modal_shapes = self.solution.structural_modal_shapes
            data_complex = modal_shapes[self.solution.displacement_dof, column].copy()
        else:
            nodal_solution = self.solution.structural_solution
            data_complex = nodal_solution[self.solution.displacement_dof, column].copy()

        if unit_factor != 1.0:
            data_complex *= unit_factor

        if self.model.analysis_id.is_harmonic():
            freq = self.model.frequencies[column]
            data_complex *= (1j * 2 * np.pi * freq)**n_diff

        phase_shifted_data  = compute_phase_shifted_values(data_complex, phase_rad)
        current_solution = phase_shifted_data.reshape(-1, 3).copy()

        if stress_plot:
            _, max_value = self.min_max_processor.get_values_for_displacement_frequency(column, 0, unit_factor, data_type, False)
            return current_solution, max_value

        if data_type in ["u_sum", "v_sum", "a_sum"]:
            color_scalars = np.linalg.norm(current_solution, axis=1)
            phase_shifted_data = current_solution.copy()

        elif data_type in ["u_x", "v_x", "a_x"]:
            color_scalars = current_solution[:, 0]
            phase_shifted_data = current_solution * np.array([1.0, 0.0, 0.0])

        elif data_type in ["u_y", "v_y", "a_y"]:
            color_scalars = current_solution[:, 1]
            phase_shifted_data = current_solution * np.array([0.0, 1.0, 0.0])

        elif data_type in ["u_z", "v_z", "a_z"]:
            color_scalars = current_solution[:, 2]
            phase_shifted_data = current_solution * np.array([0.0, 0.0, 1.0])

        min_value, max_value = self.min_max_processor.get_values_for_displacement_frequency(column, n_diff, round(unit_factor, 10), data_type, is_modal)

        return phase_shifted_data, color_scalars, min_value, max_value, np.imag(data_complex).any()


    def compute_displacements_for_3d_plot_time(
        self,
        time_index: int,
        plot_type: DisplacementDataType,
        unit_factor: float = 1.0,
        n_diff: int = 0,
        reduced_loop_time: float | None = None,
        stress_plot: bool = False,
    ):

        # compute the structural nodal solution iffts
        self.compute_multiple_ifft_for_structural_nodal_solution(n_diff=n_diff)

        if reduced_loop_time is None:
            n = self.time_vector.size
        else:
            n = np.sum(self.time_vector <= reduced_loop_time)

        # cache the minimum and maximum nodal displacements values 
        min_max_values = self.min_max_processor.get_values_for_displacement_time(int(n), round(unit_factor, 10), plot_type)

        if stress_plot:
            (_, max_value) = min_max_values
            displacements = unit_factor * self.nodal_solution_time[self.solution.displacement_dof, time_index].reshape(-1, 3).copy()
            return self.time_vector[:n], displacements, max_value

        displacements = unit_factor * self.nodal_solution_time[self.solution.displacement_dof, time_index].reshape(-1, 3).copy()

        if plot_type in ["u_sum", "v_sum", "a_sum"] :
            min_value = 0
            max_value = np.max(np.abs(min_max_values))
            scalars = np.linalg.norm(displacements, axis=1)

        else:
            min_value, max_value = min_max_values
            if plot_type in ["u_x", "v_x", "a_x"]:
                scalars = displacements[:, 0]
                displacements = displacements * np.array([1, 0, 0], dtype=float)
            elif plot_type in ["u_y", "v_y", "a_y"]:
                scalars = displacements[:, 1]
                displacements = displacements * np.array([0, 1, 0], dtype=float)
            elif plot_type in ["u_z", "v_z", "a_z"]:
                scalars = displacements[:, 2]
                displacements = displacements * np.array([0, 0, 1], dtype=float)

        return self.time_vector[:n], displacements, scalars, min_value, max_value


    def compute_structural_stresses_for_3d_plot_frequency(
        self,
        column: int,
        phase_rad: float,
        stress_type: StressType,
        data_type: StressDataType,
        unit_factor: float = 1.0,
    ):

        # compute the structural stresses (frequency domain)
        self.compute_structural_stresses_frequency()
        if self.nodal_averaged_stresses_frequency is None:
            return

        # initialize the stress vector
        stress_vector = self.nodal_averaged_stresses_frequency[:, stress_type, column].copy() * unit_factor

        match data_type:
            case StressDataType.ABSOLUTE_VALUES:
                stress_values = np.abs(stress_vector)
            case StressDataType.REAL_VALUES:
                stress_values = np.real(stress_vector)
            case StressDataType.IMAG_VALUES:
                stress_values = np.imag(stress_vector)
            case StressDataType.ABSOLUTE_ANIMATION:
                stress_values = compute_phase_shifted_values(stress_vector, phase_rad, absolute=True)
            case StressDataType.NON_ABSOLUTE_ANIMATION:
                stress_values = compute_phase_shifted_values(stress_vector, phase_rad)

        # cache the minimum and maximum nodal stresses values
        min_value, max_value = self.min_max_processor.get_values_for_stress_frequency(column, round(unit_factor, 10), stress_type, data_type)
        symmetric_animation = not np.any(stress_vector.imag)

        return stress_values, min_value, max_value, symmetric_animation


    def compute_structural_stresses_for_3d_plot_time(
        self,
        time_index: int,
        time_vector: np.ndarray,
        stress_type: StressType,
        data_type: StressDataType,
        unit_factor: float = 1.0,
    ):

        # compute the structural stresses (time domain)
        self.compute_structural_stresses_time()
        if self.nodal_averaged_stresses_time is None:
            return

        # initialize the stress vector
        stress_vector = unit_factor * self.nodal_averaged_stresses_time[:, stress_type, time_index].copy()

        match data_type:
            case StressDataType.ABSOLUTE_ANIMATION:
                stress_values = np.abs(stress_vector)
            case StressDataType.NON_ABSOLUTE_ANIMATION:
                stress_values = stress_vector

        # cache the minimum and maximum nodal stresses values
        min_value, max_value = self.min_max_processor.get_values_for_stresses_time(
            time_vector.size,
            round(unit_factor, 10),
            stress_type,
            data_type,
            )

        # force the processing of all animation frames
        symmetric_animation = False

        return stress_values, min_value, max_value, symmetric_animation


    def compute_advanced_structural_stresses_for_3d_plot_frequency(
        self,
        column: int,
        phase_rad: float,
        stress_type: StressType,
        data_type: StressDataType,
        unit_factor: float = 1.0,
    ):

        # compute the structural stresses (frequency domain)
        self.compute_structural_stresses_frequency()
        if self.nodal_averaged_stresses_frequency is None:
            return

        # evaluate the stresses at a specific phase (phase_rad = omega * t)
        stresses = unit_factor * compute_phase_shifted_values(self.nodal_averaged_stresses_frequency[:, :, column], phase_rad)
 
        if stress_type == StressType.VON_MISES_STRESS:
            stress_vector = np.sqrt((1/2) * (
                (stresses[:, 0] - stresses[:, 1])**2 + 
                (stresses[:, 1] - stresses[:, 2])**2 + 
                (stresses[:, 2] - stresses[:, 0])**2 +
                6 * (stresses[:, 3]**2 + stresses[:, 4]**2 + stresses[:, 5]**2)
                ))

        else:

            """
            stress_tensor = |sigma_x, tau_xy, tau_xz| 
                            |tau_xy, sigma_y, tau_yz|
                            |tau_xz, tau_yz, sigma_z|
            """

            # compute the stress tensor at a specific time/phase (phase_rad = omega * t)
            stress_tensor = stresses[:, [0, 3, 4, 3, 1, 5, 4, 5, 2]].reshape(-1, 3, 3)

            # compute the maximum principal stresses
            eigen_values = np.linalg.eigvalsh(stress_tensor)

            # order the maximum principal stresses
            sigmas = np.sort(eigen_values, axis=1)

            if stress_type == StressType.TRESCA_STRESS:
                stress_vector = sigmas[:, 2] - sigmas[:, 0]  # sigma_1 - sigma_3

            elif stress_type == StressType.MAXIMUM_PRINCIPAL_STRESS_1:
                stress_vector = sigmas[:, 2] # sigma_1

            elif stress_type == StressType.MAXIMUM_PRINCIPAL_STRESS_2:
                stress_vector = sigmas[:, 1] # sigma_2
            
            else:
                stress_vector = sigmas[:, 0] # sigma_3

        match data_type:
            case StressDataType.ABSOLUTE_VALUES:
                stress_values = np.abs(stress_vector)
            case StressDataType.REAL_VALUES:
                stress_values = np.real(stress_vector)
            case StressDataType.IMAG_VALUES:
                stress_values = np.imag(stress_vector)
            case StressDataType.ABSOLUTE_ANIMATION:
                stress_values = np.abs(stress_vector.copy())
            case StressDataType.NON_ABSOLUTE_ANIMATION:
                stress_values = stress_vector.copy()

        # cache the minimum and maximum nodal stresses values
        min_value, max_value = self.min_max_processor.get_values_for_advanced_stress_frequency(
            tuple(stress_vector),
            data_type,
            )

        # force the processing of all animation frames
        symmetric_animation = False

        return stress_values, min_value, max_value, symmetric_animation


    def compute_advanced_structural_stresses_for_3d_plot_time(
        self,
        time_index: int,
        stress_type: StressType,
        data_type: StressDataType,
        unit_factor: float = 1.0,
    ):

        # compute structural stress field (time domain)
        self.compute_structural_stresses_time()

        # evaluate the stresses at a specific time
        stresses = unit_factor * self.nodal_averaged_stresses_time[:, :, time_index]

        stress_vector = self.compute_advanced_structural_stresses(stresses, stress_type)
 
        match data_type:
            case StressDataType.ABSOLUTE_ANIMATION:
                stress_values = np.abs(stress_vector.copy())
            case StressDataType.NON_ABSOLUTE_ANIMATION:
                stress_values = stress_vector.copy()

        min_value, max_value = self.min_max_processor.get_values_for_advanced_stress_frequency(
            tuple(stress_vector),
            data_type,
            )

        # force the processing of all animation frames
        symmetric_animation = False

        return stress_values, min_value, max_value, symmetric_animation


    def map_material_to_elements(self, element_ids: list[int]) -> dict[int, list[int]]:
        """
        This method maps the materials to the elements.

        Parameter
        ---------
        element_ids: list
            The list of elements to map the materials.
        
        Return
        ------
        material_to_elements: dict
            The material-to-elements mapping dictionary.
        """
        material_to_volumes = defaultdict(list)

        for vol_id in self.model.domains_processor.volumes_of_domain.get("structural", []):
            material = self.model.properties._get_property("material", volume=vol_id)
            if isinstance(material, Material):
                material_to_volumes[material.identifier].append(vol_id)

        material_to_elements = defaultdict(list)

        for mat_id, volume_ids in material_to_volumes.items():

            mask = np.isin(self.mesh.solids_connectivity[:, 1], volume_ids)
            elements_from_volumes = self.mesh.solids_connectivity[mask, 0]

            valid_element_ids = np.intersect1d(element_ids, elements_from_volumes)
            material_to_elements[mat_id] = np.unique(valid_element_ids)

        return material_to_elements


def compute_shifted_values(data: np.ndarray, phase_rad: float):
    amplitudes = np.abs(data)
    phases = np.angle(data)
    delta = -phases[np.argmax(amplitudes)]
    return amplitudes * np.cos(phases + phase_rad + delta)


def compute_phase_shifted_values(values: np.ndarray, phase_rad: float, absolute: bool = False) -> np.ndarray:
    shifted_values = values.real * np.cos(phase_rad) -  values.imag * np.sin(phase_rad)
    if absolute:
        return np.absolute(shifted_values)

    return shifted_values