from vibra.engine.properties.material import Material

import numpy as np


# Hourglass base vectors (Table I, Flanagan & Belytschko 1981)
GAMMA = np.array([[ 1., 1.,-1.,-1.,-1.,-1., 1., 1.],
                  [ 1.,-1.,-1., 1.,-1., 1., 1.,-1.],
                  [ 1.,-1., 1.,-1., 1.,-1., 1.,-1.],
                  [-1., 1.,-1., 1., 1.,-1., 1.,-1.]])  # (4 x 8)


# Nodal permutations (Table III, 0-indexed)
_PERMS = [
    [0,1,2,3,4,5,6,7],
    [1,2,3,0,5,6,7,4],
    [2,3,0,1,6,7,4,5],
    [3,0,1,2,7,4,5,6],
    [4,7,6,5,0,3,2,1],
    [5,4,7,6,1,0,3,2],
    [6,5,4,7,2,1,0,3],
    [7,6,5,4,3,2,1,0],
]


def bohex(yy: np.ndarray, zz: np.ndarray):
    """ Compute one component of B_{iI} analytically.
        Appendix I, eq. 79, Flanagan & Belytschko (1981).
        B_x = bohex(y, z), B_y = bohex(z, x), B_z = bohex(x, y).
    """
    b = np.zeros(8)
    for node in range(8):
        p = _PERMS[node]
        b[node] = (1./12.) * (
            yy[p[1]]*((zz[p[5]]-zz[p[2]])-(zz[p[3]]-zz[p[4]]))
          + yy[p[2]]*(zz[p[1]]-zz[p[3]])
          + yy[p[3]]*((zz[p[2]]-zz[p[7]])-(zz[p[4]]-zz[p[1]]))
          + yy[p[4]]*((zz[p[7]]-zz[p[5]])-(zz[p[1]]-zz[p[3]]))
          + yy[p[5]]*(zz[p[4]]-zz[p[1]])
          + yy[p[7]]*(zz[p[3]]-zz[p[4]])
        )
    return b


def get_B_analytic(coords: np.ndarray):
    """ Compute B_{iI} (3x8) and volume V analytically.
        Appendix I, eq. 22 and 79, Flanagan & Belytschko (1981).
        Exact for arbitrary hexahedron geometry!!!!! Mais carinho um pouco...
        coords : (8,3) nodal coordinates (x,y,z).
        B_mean : (3,8) array, B_{iI} in article notation.
        V : scalar, exact element volume.
    """

    xx = coords[:, 0]
    yy = coords[:, 1]
    zz = coords[:, 2]

    B_mean = np.zeros((3, 8))
    B_mean[0, :] = bohex(yy, zz)   # B_x from (y, z)
    B_mean[1, :] = bohex(zz, xx)   # B_y from (z, x)
    B_mean[2, :] = bohex(xx, yy)   # B_z from (x, y)
    
    V = xx @ B_mean[0, :]           # eq. 15

    return B_mean, V


def compute_hourglass_stiffness(K_unif: np.ndarray, coords: np.ndarray, dphi_t_an: np.ndarray):
    # 3. Estabilização de Hourglass (Flanagan-Belytschko)
    # Vetores h clássicos
    h = np.array([
        [1, 1, -1, -1, -1, -1, 1, 1], 
        [1, -1, -1, 1, -1, 1, 1, -1],
        [1, -1, 1, -1, 1, -1, 1, -1], 
        [-1, 1, -1, 1, 1, -1, 1, -1]
    ])

    # This h_factor was manually adjusted to improve the
    # results accuracy. Once we find a robust approach to
    # compute the hourglass stiffness, it will be removed. 
    h_factor = 0.14568

    K_hg = np.zeros((24, 24))
    # Coeficiente de rigidez baseado no traço de K0 para escala correta
    # O Ansys usa ~5% da rigidez média para HG
    kappa = (h_factor * 0.05 * np.trace(K_unif) / 24.0)

    for a in range(4):
        # Projeção/Ortogonalização
        gamma = h[a] - (h[a] @ coords @ dphi_t_an)
        
        # Expansão para 3 DOFs
        for d in range(3):
            Gamma_v = np.zeros(24)
            Gamma_v[d::3] = gamma
            # Normalização pelo comprimento do vetor para manter h_factor adimensional
            K_hg += kappa * np.outer(Gamma_v, Gamma_v) / np.dot(gamma, gamma)

    return K_hg