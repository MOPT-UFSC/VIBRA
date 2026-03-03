from functools import cache

import numpy as np

from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from vibra.project_files.project import Project
    
from vibra.engine.solvers import ModalSolver, HarmonicSolver

DisplacementTypes = Literal["u_sum", "u_x", "u_y", "u_z"]

from collections import defaultdict


class StructuralPostprocessing:
    def __init__(self, project: 'Project'=None, structural_modal_solver: ModalSolver=None, structural_harmonic_solver: HarmonicSolver=None):
        if all(v is None for v in [project, structural_modal_solver, structural_harmonic_solver]):  
            raise ValueError("At least one of 'project', 'structural_modal_solver', or 'structural_harmonic_solver' must be provided.")
        self.project = project
        self.structural_harmonic_solver = structural_harmonic_solver
        self.structural_modal_solver = structural_modal_solver

    @property
    def harmonic_solver(self):
        if self.project is not None:
            return self.project.structural_harmonic_solver
        return self.structural_harmonic_solver

    @property
    def modal_solver(self):
        if self.project is not None:
            return self.project.structural_modal_solver
        return self.structural_modal_solver

    @cache
    def get_max_min_values_of_displacements(self, column: int, disp_type: str, is_modal: bool = False):
        """ This method returns the minimum and maximum displacement values
            of selected frequency for animation purposes.

            Parameters:
            -----------
            column: int value relative to frequency column index.

            Returns:
            -----------
            u_min, u_max: float values for minimum and maximum displacements,

        """

        if is_modal:
            data = self.modal_solver.solution[self.modal_solver.displacement_dof, column]
        else:
            data = self.harmonic_solver.solution[self.harmonic_solver.displacement_dof, column]

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

        if disp_type == "u_sum":
            return 0., r_max

        else:

            if np.abs(r_min) != np.abs(r_max):
                max_abs = np.max(np.abs([r_min, r_max]))
                r_min = -max_abs
                r_max = max_abs

        return r_min, r_max

    def compute_structural_displacement_field(
        self,
        index: int,
        phase_rad: float,
        displacement_type: DisplacementTypes,
        is_modal: bool = False
    ):
        if is_modal:
            solver = self.modal_solver
        else:
            solver = self.harmonic_solver

        if solver.solution is None:
            return

        disp_dof = solver.displacement_dof
        results_complex: np.ndarray = solver.solution[disp_dof, index]

        amplitudes = np.abs(results_complex)
        phases = np.angle(results_complex)
        delta = -phases[np.argmax(amplitudes)]
        results_real = amplitudes * np.cos(phases + phase_rad + delta)

        current_solution = results_real.reshape(-1, 3).copy()
        if displacement_type == "u_sum":
            color_scalars = np.linalg.norm(current_solution, axis=1)
            displacements = current_solution.copy()

        elif displacement_type == "u_x":
            color_scalars = current_solution[:, 0]
            displacements = current_solution * np.array([1.0, 0.0, 0.0])

        elif displacement_type == "u_y":
            color_scalars = current_solution[:, 1]
            displacements = current_solution * np.array([0.0, 1.0, 0.0])

        elif displacement_type == "u_z":
            color_scalars = current_solution[:, 2]
            displacements = current_solution * np.array([0.0, 0.0, 1.0])

        min_value, max_value = self.get_max_min_values_of_displacements(index, displacement_type, is_modal)

        return displacements, color_scalars, min_value, max_value, np.imag(displacements).any()


    def get_structural_stresses(
            self,
            node_ids : int | list[int] | None = None,
            surface_ids: int | list[int] | None = None,
            volume_ids: list[int] | None = None,
            element_averaged_stresses: bool = True,
            nodal_averaged_stresses: bool = False,
            ):
        """
        This method computes the nodal average particle velocity in the selected surface.

        Parameters
        ----------
        surface_id: int
            The selected surface ID.

        rho: float
            The fluid density related to the selected surface.

        Returns
        -------

        particle_velocities: dict
            A dictionary with the normal particle velocity and its components in
            the x, y, and z directions, computed in the selected surface.
        """

        mesh = self.harmonic_solver.assembler.model.mesh

        element_3d = self.harmonic_solver.assembler.model.acoustic_element_3d

        if element_3d is None:
            self.harmonic_solver.assembler.define_structural_elements()
            element_3d = self.harmonic_solver.assembler.element_3d

        if element_3d.connectivity is None:
            element_3d.reorder_connect()

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        if not isinstance(node_ids, np.ndarray | list):

            node_ids = list()
            if isinstance(surface_ids, int):
                surface_ids = [surface_ids]

            if isinstance(surface_ids, list):
                for surface_id in surface_ids:
                    surface_nodes = mesh.get_nodes_from_surface(surface_id)
                    node_ids.extend(surface_nodes)

            if isinstance(volume_ids, int):
                volume_ids = [volume_ids]

            if isinstance(volume_ids, list):
                for volume_id in volume_ids:
                    volume_nodes = mesh.get_nodes_from_volume(volume_id)
                    node_ids.extend(volume_nodes)
    
        if not node_ids:
            print("Invalid node ids")
            return dict(), dict()

        node_ids = np.unique(node_ids)

        map_elements_to_nodes, filtered_nodes = mesh.get_solid_elements_connected_to_nodes(
            node_ids=node_ids, return_nodes=True)

        local_dofs = np.arange(element_3d.DOF_PER_NODE, dtype=int)
        dofs_indexes = filtered_nodes.reshape(-1, 1) * element_3d.DOF_PER_NODE + local_dofs

        # Load all frequency solutions to optimize multiple load on the `process_particle_velocity` method below.
        node_to_index = dict(zip(filtered_nodes, np.arange(filtered_nodes.size, dtype=int)))
        solution = self.harmonic_solver.solution[dofs_indexes.flatten(), :]

        nodal_stresses_data = dict()
        avg_nodal_stresses_data = defaultdict(float)

        for node_id, solid_element_ids in map_elements_to_nodes.items():

            n_el = len(solid_element_ids)

            for element_id in solid_element_ids:
                connect = element_3d.connectivity[element_id, 1:]
                indexes = np.array([node_to_index.get(node) for node in connect], dtype=int)

                dofs_indexes = indexes.reshape(-1, 1) * element_3d.DOF_PER_NODE + local_dofs
                dofs_indexes = dofs_indexes.flatten()
                
                element_stresses = element_3d.process_stresses_at_integration_points(
                    element_id,
                    nodal_solution = solution[dofs_indexes, :]
                    )

                nodal_stresses = element_3d.extrapolate_stresses_to_nodes(element_stresses)
                for i, e_node in enumerate(connect):
                    nodal_stresses_data[(element_id, e_node)] = nodal_stresses[:, i, :]

                avg_nodal_stresses_data[node_id] += nodal_stresses_data[(element_id, node_id)] / n_el         

        return avg_nodal_stresses_data, nodal_stresses_data


    def nodal_stresses_post_process(self, input_stresses_data: dict):

        sigma_x = dict()
        sigma_y = dict()
        sigma_z = dict()
        tau_xy = dict()
        tau_xz = dict()
        tau_yz = dict()

        output_stresses_data = dict()

        keys = np.sort(list(input_stresses_data.keys()))

        for i, key in enumerate(keys):

            stresses = input_stresses_data.get(key)
            if stresses is None:
                continue

            sigma_x[key] = stresses[0, :]
            sigma_y[key] = stresses[1, :]
            sigma_z[key] = stresses[2, :]
            tau_xy[key] = stresses[3, :]
            tau_xz[key] = stresses[4, :]
            tau_yz[key] = stresses[5, :]

        output_stresses_data["sigma_x"] = sigma_x
        output_stresses_data["sigma_y"] = sigma_y
        output_stresses_data["sigma_z"] = sigma_z
        output_stresses_data["tau_xy"] = tau_xy
        output_stresses_data["tau_yz"] = tau_yz
        output_stresses_data["tau_xz"] = tau_xz

        ## Only for validation purposes
        # output_data = np.zeros((len(ordered_nodes), 4), dtype=float)
        # output_data[:, 0] = ordered_nodes

        # for row, node_id in enumerate(ordered_nodes):
        #     output_data[row, 1:] =  self.assembler.model.mesh.nodal_normals_data[node_id]

        # fname = f"nodal_normals_data_surface_{surface_id}.dat"
        # header = "Node index || x-axis component [m] || y-axis component [m] || z-axis component [m]"
        # np.savetxt(fname, output_data, fmt=["%i", "%.16f", "%.16f", "%.16f"], delimiter=",", header=header)

        return output_stresses_data