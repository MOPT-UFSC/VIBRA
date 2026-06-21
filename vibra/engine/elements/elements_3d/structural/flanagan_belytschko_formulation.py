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


def compute_hourglass_stiffness(K_unif: np.ndarray, coords: np.ndarray, dphi_t_an: np.ndarray, material: Material, vol: float):
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
    h_factor = 0.214568

    K_hg = np.zeros((24, 24))
    # Coeficiente de rigidez baseado no traço de K0 para escala correta
    # O Ansys usa ~5% da rigidez média para HG
    kappa = (h_factor * 0.05 * np.trace(K_unif) / 24.0)

    E = material.elasticity_modulus  # noqa: F841
    vv = material.poisson_ratio  # noqa: F841

    # print()
    # print(dphi_t_an.shape)
    # for i in range(3):
    #     B_iI = dphi_t_an[i, :]

    #     G = E / (2*(1 + vv))
    #     mu = (E * vv) / ((1 + vv) * (1 - 2*vv))

    #     kappa_ = h_factor * 0.05 * (mu + (2/3) * G) * np.dot(B_iI, B_iI) * vol
    #     print(kappa_, kappa)

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


def calcular_k_stab_corrigido(coords, E, nu, eta=0.1):
    G = E / (2 * (1 + nu))
    V_ref = 8.0 # Volume do cubo unitário pai  # noqa: F841
    
    # 1. Vetores de base Gamma (Modos de Hourglass teóricos)
    Gamma = np.array([
        [ 1,  1, -1, -1, -1, -1,  1,  1], 
        [ 1, -1, -1,  1, -1,  1,  1, -1], 
        [ 1, -1,  1, -1, -1,  1, -1,  1], 
        [-1,  1, -1,  1,  1, -1,  1, -1]  
    ])

    # 2. Derivadas naturais no centro
    dN_nat = 1/8 * np.array([
        [-1,  1,  1, -1, -1,  1,  1, -1], # dN/dxi
        [-1, -1,  1,  1, -1, -1,  1,  1], # dN/deta
        [-1, -1, -1, -1,  1,  1,  1,  1]  # dN/dzeta
    ])

    # 3. Jacobiana e Volume
    J = dN_nat @ coords
    detJ = np.linalg.det(J)
    V = 8.0 * detJ
    invJ = np.linalg.inv(J)

    # 4. Vetores de Gradiente Nodal b_i (Essencial para a ortogonalização)
    # b[0]=bx, b[1]=by, b[2]=bz (Cada um é 1x8)
    b = invJ @ dN_nat 

    # 5. Ortogonalização Correta (Garante que K_stab @ {Modos Lineares} = 0)
    gamma = np.zeros((4, 8))
    for a in range(4):
        # A projeção deve ser feita sobre cada direção i (x, y, z)
        # gamma_a = Gamma_a - (1/V) * sum_i [ (Gamma_a^T * x_i) * b_i * V ] 
        # Note que o volume cancela, simplificando para:
        proj_sum = np.zeros(8)
        for i in range(3):
            # Produto escalar do modo teórico com a coordenada da direção i
            proj_i = np.dot(Gamma[a], coords[:, i])
            proj_sum += proj_i * b[i]
        
        gamma[a] = Gamma[a] - proj_sum

    # 6. Montagem da Matriz de Rigidez (24x24)
    K_stab = np.zeros((24, 24))
    
    # Coeficiente de rigidez baseado em Belytschko & Bindeman (1993)
    # Para o hexaedro, o termo (b_i^T * b_i) controla a escala
    L2_ref = np.sum(b**2)  # noqa: F841
    
    for a in range(4):
        # Matriz externa 8x8 para o modo a
        H_a = np.outer(gamma[a], gamma[a])
        
        # Rigidez específica para o modo
        # Q_a = (eta/8) * G * V * (b_i . b_i)
        for i in range(3):
            k_scalar = (eta / 8.0) * G * V * np.dot(b[i], b[i])
            
            # Aplica nos graus de liberdade [u, v, w]
            idx = np.arange(i, 24, 3)
            K_stab[np.ix_(idx, idx)] += k_scalar * H_a

    return K_stab

# --- PATCH TEST ---
def executar_patch_test():
    # Coordenadas de um cubo distorcido (para dificultar o teste)
    coords = np.array([[0,0,0],[1.1,0,0.1],[1.2,1,0.2],[0.1,1.1,0],
                       [0.1,0.1,1],[1,0,1.1],[1.1,1.2,1.2],[0,1,1.1]])
    
    E, nu = 210e9, 0.3
    K = calcular_k_stab_corrigido(coords, E, nu)

    # Teste 1: Deformação Linear (Ex = 0.02)
    u_linear = np.zeros(24)
    for i in range(8):
        u_linear[3*i] = 0.02 * coords[i, 0] # u = 0.02 * x
    
    forca_residua = K @ u_linear
    norma = np.linalg.norm(forca_residua)
    
    print(f"Patch Test (Deformação Linear) - Norma do erro: {norma:.2e}")
    if norma < 1e-5:
        print("RESULTADO: PASSOU (A estabilização é ortogonal)")
    else:
        print("RESULTADO: FALHOU")

# executar_patch_test()

def calcular_k_stab_definitivo(coords, E, nu, eta=0.1):
    G = E / (2 * (1 + nu))
    
    # 1. Vetores de Hourglass Teóricos (Gamma)
    h = np.array([
        [ 1,  1, -1, -1, -1, -1,  1,  1], 
        [ 1, -1, -1,  1, -1,  1,  1, -1], 
        [ 1, -1,  1, -1, -1,  1, -1,  1], 
        [-1,  1, -1,  1,  1, -1,  1, -1]  
    ])

    # 2. Gradientes nodais (b) no centro
    dN_nat = 1/8 * np.array([
        [-1,  1,  1, -1, -1,  1,  1, -1], # dxi
        [-1, -1,  1,  1, -1, -1,  1,  1], # deta
        [-1, -1, -1, -1,  1,  1,  1,  1]  # dzeta
    ])
    
    J = dN_nat @ coords
    V = 8.0 * np.linalg.det(J)
    b = np.linalg.inv(J) @ dN_nat # Matriz 3x8 (bx, by, bz)

    # 3. Ortogonalização (O PONTO CRÍTICO)
    # gamma_alpha = h_alpha - (1/V) * sum_i [ (h_alpha . x_i) * b_i * V ]
    gamma = np.zeros((4, 8))
    for alpha in range(4):
        subtrair = np.zeros(8)
        for i in range(3): # Direções x, y, z
            # Projeção do modo teórico na coordenada real
            proj = np.dot(h[alpha], coords[:, i])
            subtrair += proj * b[i]
        gamma[alpha] = h[alpha] - subtrair

    # 4. Matriz de Rigidez K_stab (24x24)
    K_stab = np.zeros((24, 24))
    for alpha in range(4):
        # Matriz de espalhamento para um nó (8x8)
        H_alpha = np.outer(gamma[alpha], gamma[alpha])
        
        # Coeficiente de rigidez (Belytschko)
        # Note: usamos a norma de b para escalar a rigidez do modo
        kappa = (eta / 8.0) * G * V * np.sum(b**2) / 3.0 # Escalar médio
        
        for i in range(3): # Aplicar em x, y, z de forma independente
            idx = np.arange(i, 24, 3)
            K_stab[np.ix_(idx, idx)] += kappa * H_alpha

    return K_stab