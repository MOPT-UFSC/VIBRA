import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs


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


def shapeH8(ssx, ttx, rrx):
    """ Shape Functions and Derivatives.
    """
    denominator = 8
    phi = np.zeros(8)
    phi[0]=(1.-ssx)*(1.-ttx)*(1.-rrx)
    phi[1]=(1.+ssx)*(1.-ttx)*(1.-rrx)
    phi[2]=(1.+ssx)*(1.+ttx)*(1.-rrx)
    phi[3]=(1.-ssx)*(1.+ttx)*(1.-rrx)
    phi[4]=(1.-ssx)*(1.-ttx)*(1.+rrx)
    phi[5]=(1.+ssx)*(1.-ttx)*(1.+rrx)
    phi[6]=(1.+ssx)*(1.+ttx)*(1.+rrx)
    phi[7]=(1.-ssx)*(1.+ttx)*(1.+rrx)
    phi = phi/denominator
    dphi = np.zeros((3,8))
    dphi[0,0]=(-1.)*(1.-ttx)*(1.-rrx)
    dphi[0,1]=(1.)*(1.-ttx)*(1.-rrx)
    dphi[0,2]=(1.)*(1.+ttx)*(1.-rrx)
    dphi[0,3]=(-1.)*(1.+ttx)*(1.-rrx)
    dphi[0,4]=(-1.)*(1.-ttx)*(1.+rrx)
    dphi[0,5]=(1.)*(1.-ttx)*(1.+rrx)
    dphi[0,6]=(1.)*(1.+ttx)*(1.+rrx)
    dphi[0,7]=(-1.)*(1.+ttx)*(1.+rrx)
    dphi[1,0]=(1.-ssx)*(-1.)*(1.-rrx)
    dphi[1,1]=(1.+ssx)*(-1.)*(1.-rrx)
    dphi[1,2]=(1.+ssx)*(1.)*(1.-rrx)
    dphi[1,3]=(1.-ssx)*(1.)*(1.-rrx)
    dphi[1,4]=(1.-ssx)*(-1.)*(1.+rrx)
    dphi[1,5]=(1.+ssx)*(-1.)*(1.+rrx)
    dphi[1,6]=(1.+ssx)*(1.)*(1.+rrx)
    dphi[1,7]=(1.-ssx)*(1.)*(1.+rrx)
    dphi[2,0]=(1.-ssx)*(1.-ttx)*(-1.)
    dphi[2,1]=(1.+ssx)*(1.-ttx)*(-1.)
    dphi[2,2]=(1.+ssx)*(1.+ttx)*(-1.)
    dphi[2,3]=(1.-ssx)*(1.+ttx)*(-1.)
    dphi[2,4]=(1.-ssx)*(1.-ttx)*(1.)
    dphi[2,5]=(1.+ssx)*(1.-ttx)*(1.)
    dphi[2,6]=(1.+ssx)*(1.+ttx)*(1.)
    dphi[2,7]=(1.-ssx)*(1.+ttx)*(1.)
    dphi = dphi/denominator
    return phi, dphi


def calcB(dphi_t):
    """ Assemble B matrix (6x24) from dphi_t (3x8).
    """
    B = np.zeros((6, 3*8))
    for iii in range(8):
        B[0,3*iii+0]=dphi_t[0,iii] 
        B[0,3*iii+1]=0.             
        B[0,3*iii+2]=0.
        B[1,3*iii+0]=0.             
        B[1,3*iii+1]=dphi_t[1,iii] 
        B[1,3*iii+2]=0.
        B[2,3*iii+0]=0.             
        B[2,3*iii+1]=0.             
        B[2,3*iii+2]=dphi_t[2,iii]
        B[3,3*iii+0]=dphi_t[1,iii] 
        B[3,3*iii+1]=dphi_t[0,iii] 
        B[3,3*iii+2]=0.
        B[4,3*iii+0]=dphi_t[2,iii] 
        B[4,3*iii+1]=0.             
        B[4,3*iii+2]=dphi_t[0,iii]
        B[5,3*iii+0]=0.             
        B[5,3*iii+1]=dphi_t[2,iii] 
        B[5,3*iii+2]=dphi_t[1,iii]
    return B


def calcJAC(dphi, coord, connect, ee):
    """ Compute Jacobian, its determinant and inverse.
    """
    AUJJ = np.zeros((3,3))
    ie = connect[ee,1:]-1
    dxdydz = dphi@coord[ie, 1:4]
    JAC = np.array([[dxdydz[0,0], dxdydz[0,1], dxdydz[0,2]],
                    [dxdydz[1,0], dxdydz[1,1], dxdydz[1,2]],
                    [dxdydz[2,0], dxdydz[2,1], dxdydz[2,2]]], dtype=float)
    detJAC = (JAC[0,0]*JAC[1,1]*JAC[2,2] + JAC[0,1]*JAC[1,2]*JAC[2,0] +
              JAC[0,2]*JAC[1,0]*JAC[2,1]) - \
             (JAC[2,0]*JAC[1,1]*JAC[0,2] + JAC[2,1]*JAC[1,2]*JAC[0,0] +
              JAC[2,2]*JAC[1,0]*JAC[0,1])
    AUJJ[0,0]=  (JAC[1,1]*JAC[2,2] - JAC[2,1]*JAC[1,2])
    AUJJ[1,0]= -(JAC[1,0]*JAC[2,2] - JAC[1,2]*JAC[2,0])
    AUJJ[2,0]=  (JAC[1,0]*JAC[2,1] - JAC[1,1]*JAC[2,0])
    AUJJ[0,1]= -(JAC[0,1]*JAC[2,2] - JAC[0,2]*JAC[2,1])
    AUJJ[1,1]=  (JAC[0,0]*JAC[2,2] - JAC[0,2]*JAC[2,0])
    AUJJ[2,1]= -(JAC[0,0]*JAC[2,1] - JAC[0,1]*JAC[2,0])
    AUJJ[0,2]=  (JAC[0,1]*JAC[1,2] - JAC[0,2]*JAC[1,1])
    AUJJ[1,2]= -(JAC[0,0]*JAC[1,2] - JAC[0,2]*JAC[1,0])
    AUJJ[2,2]=  (JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0])
    iJAC = (1/detJAC) * AUJJ
    return JAC, detJAC, iJAC


def bohex(yy, zz):
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


def calcB_analytic(xel):
    """ Compute B_{iI} (3x8) and volume V analytically.
        Appendix I, eq. 22 and 79, Flanagan & Belytschko (1981).
        Exact for arbitrary hexahedron geometry!!!!! Mais carinho um pouco...
        xel : (8,3) nodal coordinates (x,y,z).
        B_mean : (3,8) array, B_{iI} in article notation.
        V : scalar, exact element volume.
    """
    xx = xel[:, 0]
    yy = xel[:, 1]
    zz = xel[:, 2]
    B_mean = np.zeros((3, 8))
    B_mean[0, :] = bohex(yy, zz)   # B_x from (y, z)
    B_mean[1, :] = bohex(zz, xx)   # B_y from (z, x)
    B_mean[2, :] = bohex(xx, yy)   # B_z from (x, y)
    V = xx @ B_mean[0, :]           # eq. 15
    # print(xx @ B_mean[0, :], yy @ B_mean[1, :], zz @ B_mean[2, :])
    return B_mean, V


def matricesH8S(ee, coord, connect, E, vv, rho):
    """ H8 stiffness and mass matrices.
        Standard 2x2x2 Gauss integration.
    """
    CTTV = np.zeros((6,6))
    tempc=E/((1+vv)*(1-2*vv)); tempn=(1-2*vv)/2; tempt=1-vv
    CTTV[0,0]=tempt; CTTV[0,1]=vv;    CTTV[0,2]=vv
    CTTV[1,0]=vv;    CTTV[1,1]=tempt; CTTV[1,2]=vv
    CTTV[2,0]=vv;    CTTV[2,1]=vv;    CTTV[2,2]=tempt
    CTTV[3,3]=tempn; CTTV[4,4]=tempn; CTTV[5,5]=tempn
    CTTV=tempc*CTTV
    nint, con, wps = 8, 1/np.sqrt(3), 1
    pint = np.array([[-con,-con,-con],[ con,-con,-con],[ con, con,-con],[-con, con,-con],
                     [-con,-con, con],[ con,-con, con],[ con, con, con],[-con, con, con]])
    Ke, Me = 0, 0
    N = np.zeros((3,3*8))
    for i in range(nint):
        ssx, ttx, rrx = pint[i, 0], pint[i, 1], pint[i, 2]
        phi, dphi = shapeH8(ssx,ttx,rrx)
        JAC, detJAC, iJAC = calcJAC(dphi, coord, connect, ee)
        dphi_t = iJAC @ dphi
        B = calcB(dphi_t)
        for iii in range(8):
            N[0,3*iii]=phi[iii]; N[0,3*iii+1]=0;        N[0,3*iii+2]=0
            N[1,3*iii]=0;        N[1,3*iii+1]=phi[iii]; N[1,3*iii+2]=0
            N[2,3*iii]=0;        N[2,3*iii+1]=0;        N[2,3*iii+2]=phi[iii]
        Ke += B.T@CTTV@B*(detJAC*wps)
        Me += rho*N.T@N*(detJAC*wps)
    return Ke, Me


def matricesH8S_FB(ee, coord, connect, E, vv, rho, B_grad, kappa=0.125):
    """ H8 stiffness and mass matrices -- Flanagan-Belytschko formulation.
        Uniform strain with analytic B (exact for arbitrary geometry)
        + orthogonal hourglass control.
        Reference: Flanagan & Belytschko (1981), IJNME 17, 679-706.
        kappa: hourglass stiffness parameter (default 0.125).
    """
    CTTV = np.zeros((6,6))
    tempc=E/((1+vv)*(1-2*vv)); tempn=(1-2*vv)/2; tempt=1-vv
    CTTV[0,0]=tempt; CTTV[0,1]=vv;    CTTV[0,2]=vv
    CTTV[1,0]=vv;    CTTV[1,1]=tempt; CTTV[1,2]=vv
    CTTV[2,0]=vv;    CTTV[2,1]=vv;    CTTV[2,2]=tempt
    CTTV[3,3]=tempn; CTTV[4,4]=tempn; CTTV[5,5]=tempn
    CTTV=tempc*CTTV
    lam = E * vv / ((1+vv)*(1-2*vv))
    mu  = E / (2*(1+vv))
    #
    # ------------------------------------------------------------------
    # PART 1: Analytic B and volume (Appendix I)
    # ------------------------------------------------------------------
    ie = connect[ee, 1:] - 1*0
    xel = coord[ie, 1:4]
    B_mean, V = calcB_analytic(xel)     # B_mean (3x8), V exact
    dphi_t_an = B_mean / V                 # equivalent to dphi_t

    # if ee == 0:
    #     print(dphi_t_an)
    #     print(B_grad)

    # dphi_t_an = B_grad
    # B_mean = B_grad * V

    B0 = calcB(dphi_t_an)               # (6x24)
    Ke = B0.T @ CTTV @ B0 * V             # uniform strain stiffness
    
    # O comportamento do código até este ponto está satisfatório, porém 
    # a compensação do HG está estranha

    # ------------------------------------------------------------------
    # PART 2: Hourglass stiffness (eq. 49, 54)
    # ------------------------------------------------------------------
    gamma = np.zeros((4, 8))
    for alpha in range(4):
        gamma[alpha, :] = GAMMA[alpha, :]
        for i in range(3):
            xG = xel[:, i] @ GAMMA[alpha, :]
            gamma[alpha, :] -= (1./V) * B_mean[i, :] * xG
    
    BtB = 0.
    for i in range(3):
        for I in range(8):
            BtB += B_mean[i, I]**2
    coeff = kappa * (lam + 2.*mu) / 3. * BtB / V
    #
    Ke_hg = np.zeros((24, 24))
    for alpha in range(4):
        for I in range(8):
            for J in range(8):
                val = coeff * gamma[alpha, I] * gamma[alpha, J]
                for i in range(3):
                    Ke_hg[3*I+i, 3*J+i] += val

    # # 3. Estabilização de Hourglass (Flanagan-Belytschko)
    # # Vetores h clássicos
    # h = np.array([
    #     [1, 1, -1, -1, -1, -1, 1, 1], 
    #     [1, -1, -1, 1, -1, 1, 1, -1],
    #     [1, -1, 1, -1, 1, -1, 1, -1], 
    #     [-1, 1, -1, 1, 1, -1, 1, -1]
    # ])

    # h_factor = 0.14568

    # Ke_hg = np.zeros((24, 24))
    # # Coeficiente de rigidez baseado no traço de K0 para escala correta
    # # O Ansys usa ~5% da rigidez média para HG
    # kappa = (h_factor * 0.05 * np.trace(Ke) / 24.0)

    # for a in range(4):
    #     # Projeção/Ortogonalização
    #     gamma = h[a] - (h[a] @ xel @ dphi_t_an)
        
    #     # Expansão para 3 DOFs
    #     for d in range(3):
    #         Gamma_v = np.zeros(24)
    #         Gamma_v[d::3] = gamma
    #         # Normalização pelo comprimento do vetor para manter h_factor adimensional
    #         Ke_hg += kappa * np.outer(Gamma_v, Gamma_v) / np.dot(gamma, gamma)

    return Ke_hg


    # ------------------------------------------------------------------
    # MASS: consistent via 2x2x2 Gauss
    # ------------------------------------------------------------------
    nint, con, wps = 8, 1/np.sqrt(3), 1
    pint = np.array([[-con,-con,-con],[ con,-con,-con],[ con, con,-con],[-con, con,-con],
                     [-con,-con, con],[ con,-con, con],[ con, con, con],[-con, con, con]])
    Me = 0
    N = np.zeros((3, 3*8))
    for i in range(nint):
        ssx, ttx, rrx = pint[i, 0], pint[i, 1], pint[i, 2]
        phi, dphi = shapeH8(ssx, ttx, rrx)
        JAC, detJAC, iJAC = calcJAC(dphi, coord, connect, ee)
        for iii in range(8):
            N[0,3*iii]=phi[iii]; N[0,3*iii+1]=0;        N[0,3*iii+2]=0
            N[1,3*iii]=0;        N[1,3*iii+1]=phi[iii]; N[1,3*iii+2]=0
            N[2,3*iii]=0;        N[2,3*iii+1]=0;        N[2,3*iii+2]=phi[iii]
        Me += rho*N.T@N*(detJAC*wps)
    return Ke, Me


def generate_ind_rows_cols(connect):
    dofs, edofs = 3, 3*8
    ind_dofs = (np.array([dofs*connect[:,1]-1, dofs*connect[:,1], dofs*connect[:,1]+1,
                          dofs*connect[:,2]-1, dofs*connect[:,2], dofs*connect[:,2]+1,
                          dofs*connect[:,3]-1, dofs*connect[:,3], dofs*connect[:,3]+1,
                          dofs*connect[:,4]-1, dofs*connect[:,4], dofs*connect[:,4]+1,
                          dofs*connect[:,5]-1, dofs*connect[:,5], dofs*connect[:,5]+1,
                          dofs*connect[:,6]-1, dofs*connect[:,6], dofs*connect[:,6]+1,
                          dofs*connect[:,7]-1, dofs*connect[:,7], dofs*connect[:,7]+1,
                          dofs*connect[:,8]-1, dofs*connect[:,8], dofs*connect[:,8]+1], dtype=int)-2).T
    vect_indices = ind_dofs.flatten()
    ind_rows = ((np.tile(vect_indices, (edofs,1))).T).flatten()
    ind_cols = (np.tile(ind_dofs, edofs)).flatten()
    return ind_rows, ind_cols


def stif_mass_matrices(coord, connect, nnode, nel, ind_rows, ind_cols, E, vv, rho,
                       formulation='standard', kappa=0.125):
    """ Calculates global matrices.
        formulation: 'standard' (2x2x2) or 'fb' (Flanagan-Belytschko).
    """
    ngl = 3 * nnode
    data_k = np.zeros((nel, (3*8)*(3*8)), dtype=float)
    data_m = np.zeros((nel, (3*8)*(3*8)), dtype=float)
    for el in range(nel):
        if formulation == 'fb':
            Ke, Me = matricesH8S_FB(el, coord, connect, E, vv, rho, kappa)
        else:
            Ke, Me = matricesH8S(el, coord, connect, E, vv, rho)
        data_k[el,:] = Ke.flatten()
        data_m[el,:] = Me.flatten()
    data_k = data_k.flatten()
    data_m = data_m.flatten()
    stif_matrix = csr_matrix((data_k, (ind_rows, ind_cols)), shape=(ngl, ngl))
    mass_matrix = csr_matrix((data_m, (ind_rows, ind_cols)), shape=(ngl, ngl))
    return stif_matrix, mass_matrix