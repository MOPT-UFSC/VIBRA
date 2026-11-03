from dataclasses import dataclass

import numpy as np

from vibra.engine.model import Model


@dataclass
class AcousticImpedanceData:
    nodal_pressures: np.ndarray
    nodal_coordinates: np.ndarray


class NodalSolutionInterpolator:
    def __init__(self, model: Model):
        self.model = model


    def interpolate_nodal_solution_data(self, surface_id: int, acoustic_impedance_data: AcousticImpedanceData):
        nodes = self.model.mesh.get_nodes_from_surface(surface_id)
        coords = self.model.mesh.nodal_coordinates[nodes, 1:]

        nodes_res = acoustic_impedance_data.nodal_coordinates[:, 0]
        coords_res = acoustic_impedance_data.nodal_coordinates[:, 1:]

        for node_id in nodes:
            coords = self.model.mesh.nodal_coordinates[node_id, 1:]
            sorted_ind = np.linalg.norm(coords_res-coords, axis=1).argsort()
            for near_node in np.flip(nodes_res[sorted_ind]):
                pass


import numpy as np

def shape_t6(xi, eta):
    # nos 1,2,3 = vertices; 4,5,6 = meio dos lados 1-2, 2-3, 3-1
    L1, L2, L3 = 1.0 - xi - eta, xi, eta
    N = np.array([L1*(2*L1-1), L2*(2*L2-1), L3*(2*L3-1),
                  4*L1*L2, 4*L2*L3, 4*L3*L1])
    dN = np.array([[1-4*L1,     1-4*L1    ],
                   [4*L2-1,     0.0       ],
                   [0.0,        4*L3-1    ],
                   [4*(L1-L2), -4*L2      ],
                   [4*L3,       4*L2      ],
                   [-4*L3,      4*(L1-L3) ]])      # colunas: dN/dxi, dN/deta
    return N, dN

def inverse_map_t6(Xe, xp, tol=1e-12, maxit=20):
    # Xe: (6,2) coordenadas nodais; xp: (2,) ponto fisico
    # chute inicial: inversa afim pelos vertices (exata se lados retos)
    A = np.column_stack((Xe[1]-Xe[0], Xe[2]-Xe[0]))
    s = np.linalg.solve(A, xp - Xe[0])
    for _ in range(maxit):
        N, dN = shape_t6(*s)
        r = N @ Xe - xp
        if np.linalg.norm(r) < tol:
            break
        J = dN.T @ Xe          # J[i,j] = dx_j/dxi_i
        s -= np.linalg.solve(J.T, r)
    return s

def inside_t6(s, eps=1e-10):
    xi, eta = s
    return xi >= -eps and eta >= -eps and xi + eta <= 1 + eps