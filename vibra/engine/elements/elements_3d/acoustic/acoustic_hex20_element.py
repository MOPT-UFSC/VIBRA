from typing import TYPE_CHECKING

from vibra.engine.elements.elements_3d.acoustic.acoustic_3d_element import Acoustic3DElement
from vibra.engine.elements.elements_3d.hex20_element import Hexahedron20

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class ActHexahedron20(Acoustic3DElement, Hexahedron20):

    def __init__(self, model: "Model", dof_per_node: int = 1, nodes_per_element: int = 20):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "acoustic_hexahedron_20"

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def process_particle_velocity(
            self,
            element_id : int,
            node_id : int,
            rho : float | np.ndarray,
            frequencies : np.ndarray,
            **kwargs
        ):
        """
        This method computes the particle velocity components in
        the x, y, and z directions.

        Parameters
        ----------
        element_id: int
            The element index.

        node_id: int
            The node index.

        rho: float
            The fluid density in kg/m³.

        frequencies: np.ndarray
            The frequencies vector.

        nodal_pressures: np.ndarray
            The nodal pressures solution.

        Return
        ------
        particle_velocity: np.array
            An array containing the particle velocity components in the
            x, y, and z directions.
        """

        solution = kwargs.get("solution")
        nodal_pressures = kwargs.get("nodal_pressures")
        node_ids = kwargs.get("node_ids")

        if node_ids is None:
            node_ids = self.connectivities[element_id, :]
    
        if isinstance(nodal_pressures, np.ndarray):
            Pe = nodal_pressures
        elif isinstance(solution, np.ndarray):
            Pe = solution[self.model.fluid_node_mapping[node_ids], :]
        else:
            return None

        omega = 2 * np.pi * frequencies

        if self.connectivities is None:
            self.reorder_connect()

        ## calculation points (adapted from Atalla and Sgard, 2015, pg. 171)
        p_calc = np.array([ 
            [-1.0, -1.0, -1.0],      # ->      (-1.0, -1.0, -1.0)   Node 1
            [ 1.0, -1.0, -1.0],      # ->      ( 1.0, -1.0, -1.0)   Node 2
            [ 1.0,  1.0, -1.0],      # ->      ( 1.0,  1.0, -1.0)   Node 3
            [-1.0,  1.0, -1.0],      # ->      (-1.0,  1.0, -1.0)   Node 4
            [-1.0, -1.0,  1.0],      # ->      (-1.0, -1.0,  1.0)   Node 5
            [ 1.0, -1.0,  1.0],      # ->      ( 1.0, -1.0,  1.0)   Node 6
            [ 1.0,  1.0,  1.0],      # ->      ( 1.0,  1.0,  1.0)   Node 7
            [-1.0,  1.0,  1.0],      # ->      (-1.0,  1.0,  1.0)   Node 8
            [ 0.0, -1.0, -1.0],      # ->      ( 0.0, -1.0, -1.0)   Node 9
            [ 1.0,  0.0, -1.0],      # ->      ( 1.0,  0.0, -1.0)   Node 10
            [ 0.0,  1.0, -1.0],      # ->      ( 0.0,  1.0, -1.0)   Node 11
            [-1.0,  0.0, -1.0],      # ->      (-1.0,  0.0, -1.0)   Node 12
            [ 0.0, -1.0,  1.0],      # ->      ( 0.0, -1.0,  1.0)   Node 17
            [ 1.0,  0.0,  1.0],      # ->      ( 1.0,  0.0,  1.0)   Node 18
            [ 0.0,  1.0,  1.0],      # ->      ( 0.0,  1.0,  1.0)   Node 19
            [-1.0,  0.0,  1.0],      # ->      (-1.0,  0.0,  1.0)   Node 20
            [-1.0, -1.0,  0.0],      # ->      (-1.0, -1.0,  0.0)   Node 13
            [ 1.0, -1.0,  0.0],      # ->      ( 1.0, -1.0,  0.0)   Node 14
            [ 1.0,  1.0,  0.0],      # ->      ( 1.0,  1.0,  0.0)   Node 15
            [-1.0,  1.0,  0.0],      # ->      (-1.0,  1.0,  0.0)   Node 16
            ], dtype=float)

        index = np.where(node_ids==node_id)[0]
        if index.size != 1:
            return None

        # local coordinates
        (ssx, ttx, rrx) = p_calc[index[0], :]

        # derivative of the shape function at the selected point
        _, dphi = self.get_shape_functions_and_derivatives(ssx, ttx, rrx)

        # nodal coordinates from element
        coords = self.nodal_coordinates[node_ids, 1:4]

        # Jacobian matrix
        JAC = dphi @ coords

        # inverse of Jacobian matrix
        _, invJAC = self.get_detJAC_and_invJAC(JAC)

        # derivative of shape functions
        B = invJAC @ dphi

        # calculate the particle velocities components
        particle_velocity = -(1 / (1j * rho * omega)) * (B @ Pe)

        return particle_velocity