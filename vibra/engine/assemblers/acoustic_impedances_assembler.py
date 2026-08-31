
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from vibra.engine.properties.fluid import Fluid

if TYPE_CHECKING:
    from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler


@dataclass
class ExternalImpedanceData:
    connectivities: np.ndarray
    surface_data: np.ndarray


@dataclass
class InternalImpedanceData:
    connectivities_A: np.ndarray
    connectivities_B: np.ndarray
    surface_data_A: np.ndarray
    surface_data_B: np.ndarray
    non_linear: bool = False


@dataclass
class IncidentPlaneWaveData:
    ipw_vector: np.ndarray
    ipw_pressure: np.ndarray
    ipw_impedance: np.ndarray
    connectivities: np.ndarray
    element_face_normals: np.ndarray


class AcousticImpedancesAssembler:
    def __init__(self, assembler : "AcousticAssembler"):

        self.assembler = assembler

        self.reset()


    def reset(self):

        self.integration_data_Zsi: ExternalImpedanceData | None = None
        self.integration_data_Zat: ExternalImpedanceData | None = None
        self.integration_data_Zat: ExternalImpedanceData | None = None
        self.integration_data_Zpp: InternalImpedanceData | None = None
        self.integration_data_Zti: InternalImpedanceData | None = None
        self.integration_data_ipw: IncidentPlaneWaveData | None = None

        self.data_Zsi = {}
        self.rows_Zsi = np.array([], dtype=int)
        self.cols_Zsi = np.array([], dtype=int)

        self.data_Zat = {}
        self.rows_Zat = np.array([], dtype=int)
        self.cols_Zat = np.array([], dtype=int)

        self.data_Zipw = {}
        self.rows_Zipw = np.array([], dtype=int)
        self.cols_Zipw = np.array([], dtype=int)

        self.data_Zas = {}
        self.rows_Zas = np.array([], dtype=int)
        self.cols_Zas = np.array([], dtype=int)

        self.data_Zti_A = {}
        self.rows_Zti_A = np.array([], dtype=int)
        self.cols_Zti_A = np.array([], dtype=int)

        self.data_Zti_B = {}
        self.rows_Zti_B = np.array([], dtype=int)
        self.cols_Zti_B = np.array([], dtype=int)

        self.data_Zpp_A = {}
        self.rows_Zpp_A = np.array([], dtype=int)
        self.cols_Zpp_A = np.array([], dtype=int)

        self.data_Zpp_B = {}
        self.rows_Zpp_B = np.array([], dtype=int)
        self.cols_Zpp_B = np.array([], dtype=int)


    @property
    def model(self):
        return self.assembler.model


    @property
    def properties(self):
        return self.assembler.model.properties


    @property
    def element_1d(self):
        return self.assembler.element_1d


    @property
    def element_2d(self):
        return self.assembler.element_2d


    @property
    def number_3d_elements(self):
        return self.model.number_3d_acoustic_elements


    @property
    def acoustic_dofs(self):
        return self.model.acoustic_dofs_indices


    @property
    def acoustic_ndofs(self):
        return len(self.model.acoustic_dofs_indices)


    @property
    def total_dofs(self):
        return self.model.total_dof


    @property
    def gm_shape(self):
        return (self.model.total_dof, self.model.total_dof)


    @property
    def number_frequencies(self):
        return self.assembler.number_frequencies


    @property
    def prescribed_dof_indices(self):
        return self.assembler.prescribed_dof_indices


    @property
    def unprescribed_dof_indices(self):
        return self.assembler.unprescribed_dof_indices


    @property
    def fluid_properties_from_volume(self):
        return self.assembler.fluid_properties_from_volume


    def get_impedance_data_for_element_integration(self, property_label: str) -> ExternalImpedanceData | None:
        """ 
        This method processes the surface property data for element face
        integration.

        Parameters
        ----------
        property_label: str
            The property label on which the surface data will be processed.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        aux_data = {}
        aux_connect = {}
        integration_data = {}

        for key, data in self.properties.surface_properties.items():

            prop, surface_id = key
            if prop != property_label:
                continue

            data: dict
            density, speed_of_sound = self.assembler.get_fluid_properties_from_surface(surface_id)

            if property_label ==  "anechoic_termination" or "anechoic_termination" in data:
                complex_values = density * speed_of_sound

            elif property_label ==  "absorption_surface":
                alpha = data.get("values")[0]

                Z_0 = density * speed_of_sound
                Z_s = Z_0 * ((1 + (1-alpha)**(1/2)) / (1 - (1-alpha)**(1/2)))
                complex_values = Z_s

            else:
                complex_values = data.get("values")[0]

            # normalize data type to array
            complex_values_array = self.assembler.get_value_in_array_form(complex_values, flatten=True)

            surf_elements = list(self.model.mesh.elements_from_surface.get(surface_id))
            surf_connect = self.model.mesh.get_connectivity_from_surface(surface_id)

            for i, el in enumerate(surf_elements):
                aux_connect[el] = surf_connect[i]
                aux_data[el] = complex_values_array

        if aux_connect:

            integration_data = {
                "connectivities" : np.array(list(aux_connect.values()), dtype=int),
                "surface_data" : np.array(list(aux_data.values()), dtype=complex),
                }

            return ExternalImpedanceData(**integration_data)


    def get_incident_plane_wave_surface_data_for_element_integration(self) -> dict:
        """ 
        This method processes the plane wave data for element face
        integration.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        connectivities = {}
        elements_normals = {}

        for key, data in self.properties.surface_properties.items():

            prop, surface_id = key
            if prop != "incident_plane_wave":
                continue

            rho_eff_pm, C_eff_pm = self.model.get_porous_material_model_effective_properties(surface_id)
            rho_eff_tv, C_eff_tv = self.model.get_viscous_thermal_model_effective_properties(surface_id)

            ipw_vector = np.array(data.get("ipw_vector"), dtype=float)
            norm_ipw_vector = np.linalg.norm(ipw_vector)

            if norm_ipw_vector:
                ipw_vector /= norm_ipw_vector

            if isinstance(rho_eff_pm, np.ndarray):
                density = rho_eff_pm
                speed_of_sound = C_eff_pm

            elif isinstance(rho_eff_tv, np.ndarray):
                density = rho_eff_tv
                speed_of_sound = C_eff_tv

            else:
                fluid: Fluid = self.model.properties._get_property("fluid", surface=surface_id)
                if not isinstance(fluid, Fluid):
                    continue

                density = fluid.fluid_density
                speed_of_sound = fluid.speed_of_sound

            data: dict

            # normalize data type to array
            p_inc = self.assembler.get_value_in_array_form(data.get("values")[0], flatten=True)
            Z_ipw = self.assembler.get_value_in_array_form(density * speed_of_sound, flatten=True)

            rows = self.model.mesh.faces_connectivity[:, 1] == surface_id
            surface_elements_connectivities = self.model.mesh.faces_connectivity[rows, :]
            surface_elements_normals = self.model.mesh.get_element_face_normal_batched(surface_elements_connectivities)

            # elements_connectivities.extend(surface_elements_connectivities[:, 4:])
            # elements_normals.extend(surface_elements_normals)

            surf_elements = list(self.model.mesh.elements_from_surface.get(surface_id))
            surf_connect = self.model.mesh.get_connectivity_from_surface(surface_id) 

            for i, el in enumerate(surf_elements):
                connectivities[el] = self.model.fluid_node_mapping[surf_connect[i]]
                elements_normals[el] = surface_elements_normals[i, :]

        if connectivities:

            pw_data = {
                "ipw_vector": ipw_vector,
                "ipw_pressure": p_inc,
                "ipw_impedance": Z_ipw,
                "connectivities": np.array(list(connectivities.values()), dtype=int),
                "element_face_normals": np.array(list(elements_normals.values()), dtype=float),
            }

            return IncidentPlaneWaveData(**pw_data)


    def get_transfer_impedance_data_for_element_integration(self):
        """
        This method processes the transfer impedance data for element face
        integration.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        surface_data_A = {}
        surface_data_B = {}
        connectivity_surface_A = {}
        connectivity_surface_B = {}
        integration_data = {}

        # aux_ones = np.ones(self.number_frequencies, dtype=complex)

        for (property_label, surface_ids), p_data in self.properties.surface_properties.items():

            if property_label != "transfer_impedance":
                continue
        
            p_data: dict
            values = p_data.get("values")
            if values is None:
                continue

            _complex_values = values[0]
            if not isinstance(_complex_values, complex | float | np.ndarray):
                continue

            Z_tr = self.assembler.get_value_in_array_form(_complex_values, flatten=True)

            # if isinstance(_complex_values, complex | float):
            #     Z_tr = _complex_values * aux_ones

            # elif isinstance(_complex_values, np.ndarray):

            #     if _complex_values.shape[0] == 1:
            #         Z_tr = _complex_values * aux_ones

            #     else:
            #         Z_tr = _complex_values

            # else:
            #     continue

            decouple_data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_ids)
            if not isinstance(decouple_data, dict):
                continue

            new_surface_id = decouple_data.get("new_surface_id")
            if new_surface_id is None:
                continue

            surf_elements_A = list(self.model.mesh.elements_from_surface.get(surface_ids))
            surf_elements_B = list(self.model.mesh.elements_from_surface.get(new_surface_id))

            for i, el in enumerate(surf_elements_A):
                nodes_from_element = self.model.mesh.faces_connectivity[el, 4:]
                connectivity_surface_A[el] = nodes_from_element

                surface_data_A[el] = Z_tr

            for i, el in enumerate(surf_elements_B):
                nodes_from_element = self.model.mesh.faces_connectivity[el, 4:]
                connectivity_surface_B[el] = nodes_from_element

                surface_data_B[el] = Z_tr

        if connectivity_surface_A and connectivity_surface_B:
            integration_data = {
                "connectivities_A": np.array(list(connectivity_surface_A.values()), dtype=int),
                "connectivities_B": np.array(list(connectivity_surface_B.values()), dtype=int),
                "surface_data_A": np.array(list(surface_data_A.values()), dtype=complex),
                "surface_data_B": np.array(list(surface_data_B.values()), dtype=complex),
            }

            return InternalImpedanceData(**integration_data)


    def get_perforated_plate_data_for_element_integration(self, solution: np.ndarray | None = None):
        """
        This method processes the perforated plate data for element face
        integration.

        Parameters
        ----------
        solution: np.ndarray, optional
            It corresponds to the acoustic pressure field that is adopted to
            update the impedance of the perforated plate whenever nonlinear 
            effects are enabled.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        surface_data_A = {}
        surface_data_B = {}
        connectivity_surface_A = {}
        connectivity_surface_B = {}

        integration_data = {}

        for (property_label, surface_ids), pp_data in self.properties.surface_properties.items():

            if property_label == "perforated_plate_model":
                pp_data: dict

                pp_model = self.model.perforated_plate_impedance_data[surface_ids]
                pp_model: dict

                z_orifice = pp_model.get("z_orifice", 0)
                z_end = pp_model.get("z_end", 0)
                z_nl_urms = pp_model.get("z_nl_urms", 0)
                z_ud = pp_model.get("z_ud", 0)
                Z_0 = pp_model.get("Z_0", 0)

                non_linear = z_nl_urms != 0
    
                decouple_data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_ids)
                if not isinstance(decouple_data, dict):
                    continue

                new_surface_id = decouple_data.get("new_surface_id")
                if new_surface_id is None:
                    continue

                surf_elements_A = list(self.model.mesh.elements_from_surface.get(surface_ids))
                surf_elements_B = list(self.model.mesh.elements_from_surface.get(new_surface_id))

                for i, el in enumerate(surf_elements_A):

                    U_rms = 0
                    nodes_from_element = self.model.mesh.faces_connectivity[el, 4:]
                    connectivity_surface_A[el] = nodes_from_element

                    # if solution is not None:
                    #     p = solution[nodes_from_element, :]
                    #     p2_avg = np.average((1/2)*np.real(p*np.conj(p)), axis=0)
                    #     p_rms = np.sqrt(p2_avg)
                    #     U_rms = p_rms / Z_0

                    Ztr_A = Z_0 * (z_orifice + z_end + z_nl_urms*U_rms + z_ud)
                    surface_data_A[el] = Ztr_A

                for i, el in enumerate(surf_elements_B):

                    U_rms = 0
                    nodes_from_element = self.model.mesh.faces_connectivity[el, 4:]
                    connectivity_surface_B[el] = nodes_from_element

                    # if solution is not None:
                    #     p = solution[nodes_from_element, :]
                    #     p2_avg = np.average((1/2)*np.real(p*np.conj(p)), axis=0)
                    #     p_rms = np.sqrt(p2_avg)
                    #     U_rms = p_rms / Z_0

                    Ztr_B = Z_0 * (z_orifice + z_end + z_nl_urms*U_rms + z_ud)
                    surface_data_B[el] = Ztr_B

        if connectivity_surface_A and connectivity_surface_B:
            integration_data = {
                "connectivities_A": np.array(list(connectivity_surface_A.values()), dtype=int),
                "connectivities_B": np.array(list(connectivity_surface_B.values()), dtype=int),
                "surface_data_A": np.array(list(surface_data_A.values()), dtype=complex),
                "surface_data_B": np.array(list(surface_data_B.values()), dtype=complex),
                "non_linear": non_linear,
            }

            return InternalImpedanceData(**integration_data)


    def process_specific_impedance_data_to_assemble_damping_matrix(self):
        """ 
        This method processes the specific impedance data to assemble
        the global damping matrix.
        """

        self.integration_data_Zsi = self.get_impedance_data_for_element_integration("specific_impedance")
        if self.integration_data_Zsi is None:
            return

        logging.info("Processing the impedance data to assemble damping matrix... [1/14]")
        connectivities = self.integration_data_Zsi.connectivities      
        Z_si = self.integration_data_Zsi.surface_data

        nel = len(connectivities)
        dof = self.element_2d.dof_per_element

        for j in range(self.number_frequencies):
            self.data_Zsi[j] = np.zeros((nel, dof, dof), dtype=complex)

        logging.info("Processing the impedance data to assemble damping matrix... [2/14]")
        self.rows_Zsi, self.cols_Zsi = self.element_2d.get_rows_and_cols_indices_2D(connectivities)
        int2d_NtN = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zsi[j] = int2d_NtN / Z_si[:, j].reshape(-1, 1, 1)


    def process_anechoic_termination_data_to_assemble_damping_matrix(self):
        """ 
        This method processes the anechoic termination data to assemble
        the global damping matrix.
        """

        self.integration_data_Zat = self.get_impedance_data_for_element_integration("anechoic_termination")
        if not self.integration_data_Zat:
            return

        logging.info("Processing the impedance data to assemble damping matrix... [3/14]")
        connectivities = self.integration_data_Zat.connectivities
        Z_at = self.integration_data_Zat.surface_data

        nel = len(connectivities)
        dof = self.element_2d.dof_per_element

        for j in range(self.number_frequencies):
            self.data_Zat[j] = np.zeros((nel, dof, dof), dtype=complex)

        logging.info("Processinng the impedance data to assemble damping matrix... [4/14]")
        self.rows_Zat, self.cols_Zat = self.element_2d.get_rows_and_cols_indices_2D(connectivities)
        int2d_NtN = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zat[j] = int2d_NtN / Z_at[:, j].reshape(-1, 1, 1)


    def process_incident_plane_wave_data_to_assemble_damping_matrix(self):
        """ 
        This method processes the incident plane wave data to assemble
        the global damping matrix.
        """

        self.integration_data_ipw = self.get_incident_plane_wave_surface_data_for_element_integration()
        if self.integration_data_ipw is None:
            return

        logging.info("Processing the impedance data to assemble damping matrix... [5/14]")
        ipw_vector: np.ndarray = self.integration_data_ipw.ipw_vector
        Z_ipw: np.ndarray = self.integration_data_ipw.ipw_impedance
        connectivities: np.ndarray = self.integration_data_ipw.connectivities
        element_normals: np.ndarray = self.integration_data_ipw.element_face_normals

        nel = len(connectivities)
        dof = self.element_2d.dof_per_element

        for j in range(self.number_frequencies):
            self.data_Zipw[j] = np.zeros((nel, dof, dof), dtype=complex)

        logging.info("Processing the impedance data to assemble damping matrix... [6/14]")
        self.rows_Zipw, self.cols_Zipw = self.element_2d.get_rows_and_cols_indices_2D(connectivities)
        int2d_NtN = self.element_2d.stacked_matrices_NtN()

        s_vector = ipw_vector.reshape(3, 1)
        n_vectors = element_normals.reshape(-1, 1, 3)

        # the dot product between incident plane wave vector and the face element normal vector
        n_k = np.dot(n_vectors, s_vector)

        for j in range(self.number_frequencies):
            # the negative signal is being used to revert the signal from the elementary matrix
            self.data_Zipw[j] = -(n_k / Z_ipw[j]) * int2d_NtN


    def process_surface_impedance_data_to_assemble_damping_matrix(self):
        """ 
        This method processes the surface impedance data resulting from
        absorption surface to assemble the global damping matrix.
        """

        self.integration_data_Zas = self.get_impedance_data_for_element_integration("absorption_surface")
        if not self.integration_data_Zas:
            return

        logging.info("Processing the impedance data to assemble damping matrix... [7/14]")
        connectivities = self.integration_data_Zas.connectivities
        Z_as = self.integration_data_Zas.surface_data

        nel = len(connectivities)
        dof = self.element_2d.dof_per_element

        for j in range(self.number_frequencies):
            self.data_Zas[j] = np.zeros((nel, dof, dof), dtype=complex)

        logging.info("Processing the impedance data to assemble damping matrix... [8/14]")
        self.rows_Zas, self.cols_Zas = self.element_2d.get_rows_and_cols_indices_2D(connectivities)
        int2d_NtN = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zas[j] = int2d_NtN / Z_as[:, j].reshape(-1, 1, 1)


    def process_transfer_impedance_data_to_assemble_damping_matrix(self):
        """
        This method processes the internal transfer impedance data 
        to assemble the global damping matrix.
        """

        self.integration_data_Zti = self.get_transfer_impedance_data_for_element_integration()
        if self.integration_data_Zti is None:
            return

        logging.info("Processing the impedance data to assemble damping matrix... [9/14]")
        connectivities_A = self.integration_data_Zti.connectivities_A
        connectivities_B = self.integration_data_Zti.connectivities_B
        Zti_A = self.integration_data_Zti.surface_data_A
        Zti_B = self.integration_data_Zti.surface_data_B

        nel_A = len(connectivities_A)
        nel_B = len(connectivities_B)
        dof = self.element_2d.dof_per_element

        for j in range(self.number_frequencies):
            self.data_Zti_A[j] = np.zeros((nel_A, dof, dof), dtype=complex)
            self.data_Zti_B[j] = np.zeros((nel_B, dof, dof), dtype=complex)

        logging.info("Processing the impedance data to assemble damping matrix... [10/14]")
        self.rows_Zti_A, self.cols_Zti_A = self.element_2d.get_rows_and_cols_indices_2D(connectivities_A)
        int2d_NtN_A = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zti_A[j] = int2d_NtN_A / Zti_A[:, j].reshape(-1, 1, 1)

        logging.info("Processing the impedance data to assemble damping matrix... [11/14]")
        self.rows_Zti_B, self.cols_Zti_B = self.element_2d.get_rows_and_cols_indices_2D(connectivities_B)
        int2d_NtN_B = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zti_B[j] = int2d_NtN_B / Zti_B[:, j].reshape(-1, 1, 1)


    def process_perforated_plate_impedance_data_to_assemble_damping_matrix(self, solution: np.ndarray | None = None):
        """
        This method processes the perforated plate impedance data 
        to assemble the global damping matrix.

        Parameters
        ----------
        solution: np.ndarray, optional
        """

        self.integration_data_Zpp = self.get_perforated_plate_data_for_element_integration(solution)
        if self.integration_data_Zpp is None:
            return

        logging.info("Processing the impedance data to assemble damping matrix... [12/14]")

        Zpp_A = self.integration_data_Zpp.surface_data_A
        Zpp_B = self.integration_data_Zpp.surface_data_B
        # non_linear = self.integration_data_Zpp.non_linear
        connectivities_A = self.integration_data_Zpp.connectivities_A
        connectivities_B = self.integration_data_Zpp.connectivities_B

        nel_A = len(connectivities_A)
        nel_B = len(connectivities_B)
        dof = self.element_2d.dof_per_element

        for j in range(self.number_frequencies):
            self.data_Zpp_A[j] = np.zeros((nel_A, dof, dof), dtype=complex)
            self.data_Zpp_B[j] = np.zeros((nel_B, dof, dof), dtype=complex)

        logging.info("Processing the impedance data to assemble damping matrix... [13/14]")
        self.rows_Zpp_A, self.cols_Zpp_A = self.element_2d.get_rows_and_cols_indices_2D(connectivities_A)
        int2d_NtN_A = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zpp_A[j] = int2d_NtN_A / Zpp_A[:, j].reshape(-1, 1, 1)

        logging.info("Processing the impedance data to assemble damping matrix... [14/14]")
        self.rows_Zpp_B, self.cols_Zpp_B = self.element_2d.get_rows_and_cols_indices_2D(connectivities_B)
        int2d_NtN_B = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zpp_B[j] = int2d_NtN_B / Zpp_B[:, j].reshape(-1, 1, 1)


    def compute_data_to_assemble_damping_matrix(self):
        self.process_specific_impedance_data_to_assemble_damping_matrix()
        self.process_anechoic_termination_data_to_assemble_damping_matrix()
        self.process_incident_plane_wave_data_to_assemble_damping_matrix()
        self.process_surface_impedance_data_to_assemble_damping_matrix()
        self.process_transfer_impedance_data_to_assemble_damping_matrix()
        self.process_perforated_plate_impedance_data_to_assemble_damping_matrix()