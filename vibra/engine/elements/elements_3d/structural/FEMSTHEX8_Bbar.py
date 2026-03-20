import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs


def shapeH8(ssx, ttx, rrx):
    """ Shape Functions and Derivatives.
    """
    denominator = 8
    #shape functions 
    phi = np.zeros(8)
    #
    phi[0]=(1.-ssx)*(1.-ttx)*(1.-rrx)
    phi[1]=(1.+ssx)*(1.-ttx)*(1.-rrx)
    phi[2]=(1.+ssx)*(1.+ttx)*(1.-rrx)
    phi[3]=(1.-ssx)*(1.+ttx)*(1.-rrx)
    phi[4]=(1.-ssx)*(1.-ttx)*(1.+rrx)
    phi[5]=(1.+ssx)*(1.-ttx)*(1.+rrx)
    phi[6]=(1.+ssx)*(1.+ttx)*(1.+rrx)
    phi[7]=(1.-ssx)*(1.+ttx)*(1.+rrx)
    phi = phi/denominator

    #derivatives
    dphi = np.zeros((3,8))
    #
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
        B[0,3*(iii)+0]=dphi_t[0,iii]
        B[0,3*(iii)+1]=0.
        B[0,3*(iii)+2]=0.
        B[1,3*(iii)+0]=0.
        B[1,3*(iii)+1]=dphi_t[1,iii]
        B[1,3*(iii)+2]=0.
        B[2,3*(iii)+0]=0.
        B[2,3*(iii)+1]=0.
        B[2,3*(iii)+2]=dphi_t[2,iii]
        B[3,3*(iii)+0]=dphi_t[1,iii]
        B[3,3*(iii)+1]=dphi_t[0,iii]
        B[3,3*(iii)+2]=0.              
        B[4,3*(iii)+0]=dphi_t[2,iii]
        B[4,3*(iii)+1]=0.
        B[4,3*(iii)+2]=dphi_t[0,iii]
        B[5,3*(iii)+0]=0.
        B[5,3*(iii)+1]=dphi_t[2,iii]
        B[5,3*(iii)+2]=dphi_t[1,iii]
    return B


def calcJAC(dphi, coord, connect, ee):
    """ Compute Jacobian, its determinant and inverse.
    """
    AUJJ = np.zeros((3,3))
    ie = connect[ee,1:]-1*0
    dxdydz = dphi@coord[ie, 1:4]
    JAC = np.array([[dxdydz[0,0], dxdydz[0,1], dxdydz[0,2]],
                    [dxdydz[1,0], dxdydz[1,1], dxdydz[1,2]],
                    [dxdydz[2,0], dxdydz[2,1], dxdydz[2,2]]], dtype=float)
    detJAC = (JAC[0,0] * JAC[1,1] * JAC[2,2] + 
              JAC[0,1] * JAC[1,2] * JAC[2,0] + 
              JAC[0,2] * JAC[1,0] * JAC[2,1]) - \
            ( JAC[2,0] * JAC[1,1] * JAC[0,2] + 
              JAC[2,1] * JAC[1,2] * JAC[0,0] + 
              JAC[2,2] * JAC[1,0] * JAC[0,1])
    # adj(JAC)
    AUJJ[0,0]= 1 * ((JAC[1,1] * JAC[2,2]) - (JAC[2,1] * JAC[1,2]))
    AUJJ[1,0]= -1 * ((JAC[1,0] * JAC[2,2]) - (JAC[1,2] * JAC[2,0]))
    AUJJ[2,0]= 1 * ((JAC[1,0] * JAC[2,1]) - (JAC[1,1] * JAC[2,0]))
    AUJJ[0,1]= -1 * ((JAC[0,1] * JAC[2,2]) - (JAC[0,2] * JAC[2,1]))
    AUJJ[1,1]= 1 * ((JAC[0,0] * JAC[2,2]) - (JAC[0,2] * JAC[2,0]))
    AUJJ[2,1]= -1 * ((JAC[0,0] * JAC[2,1]) - (JAC[0,1] * JAC[2,0]))
    AUJJ[0,2]= 1 * ((JAC[0,1] * JAC[1,2]) - (JAC[0,2] * JAC[1,1]))
    AUJJ[1,2]= -1 * ((JAC[0,0] * JAC[1,2]) - (JAC[0,2] * JAC[1,0]))
    AUJJ[2,2]= 1 * ((JAC[0,0] * JAC[1,1]) - (JAC[0,1] * JAC[1,0]))
    #Inverse Jacobian
    iJAC = (1/detJAC) * AUJJ
    return JAC, detJAC, iJAC


def matricesH8S(ee, coord, connect, E, vv, rho):
    """ H8 stiffness and mass matrices.
        Solid45 w/o extra diplacements (very simple)
    """
    # Constititive model - Linear isotropic material
    CTTV = np.zeros((6,6))
    #
    tempc=E/((1+vv)*(1-2*vv))
    tempn=(1-2*vv)/2
    tempt=1-vv
    #
    CTTV[0,0]=tempt
    CTTV[0,1]=vv
    CTTV[0,2]=vv
    CTTV[1,0]=vv
    CTTV[1,1]=tempt
    CTTV[1,2]=vv
    CTTV[2,0]=vv
    CTTV[2,1]=vv
    CTTV[2,2]=tempt
    CTTV[3,3]=tempn
    CTTV[4,4]=tempn
    CTTV[5,5]=tempn
    #
    CTTV=tempc*CTTV
    # integration points
    nint, con, wps = 8, 1/np.sqrt(3), 1

    pint = np.array([[-con, -con, -con],
                     [ con, -con, -con],
                     [ con,  con, -con],
                     [-con,  con, -con],
                     [-con, -con,  con],
                     [ con, -con,  con],
                     [ con,  con,  con],
                     [-con,  con,  con]])
    # 
    Ke, Me = 0, 0
    B = np.zeros((6,3*8))
    N = np.zeros((3,3*8))
    # integration
    for i in range(nint):
        ssx, ttx, rrx = pint[i, 0], pint[i, 1], pint[i, 2]
        phi, dphi = shapeH8(ssx,ttx,rrx)
        JAC, detJAC, iJAC = calcJAC(dphi, coord, connect, ee)
        dphi_t = iJAC @ dphi
        B = calcB(dphi_t)

        for iii in range(8): 
            N[0,3*iii+0]=phi[iii]
            N[0,3*iii+1]=0
            N[0,3*iii+2]=0
            N[1,3*iii+0]=0
            N[1,3*iii+1]=phi[iii]
            N[1,3*iii+2]=0
            N[2,3*iii+0]=0
            N[2,3*iii+1]=0
            N[2,3*iii+2]=phi[iii]
      
        Ke += B.T@CTTV@B*(detJAC*wps)
        Me += rho*N.T@N*(detJAC*wps)
        
    return Ke, Me


def matricesH8S_Bbar(ee, coord, connect, E, vv, rho):
    """ H8 stiffness with B-bar method and mass matrices.
        Hughes (1980), Simo et al. (1985).
        Zienkiewicz & Taylor & Zhu (Pg 327)
    """
    # Constititive model - Linear isotropic material
    CTTV = np.zeros((6,6))
    #
    tempc=E/((1+vv)*(1-2*vv))
    tempn=(1-2*vv)/2
    tempt=1-vv
    #
    CTTV[0,0]=tempt
    CTTV[0,1]=vv
    CTTV[0,2]=vv
    CTTV[1,0]=vv
    CTTV[1,1]=tempt
    CTTV[1,2]=vv
    CTTV[2,0]=vv
    CTTV[2,1]=vv
    CTTV[2,2]=tempt
    CTTV[3,3]=tempn
    CTTV[4,4]=tempn
    CTTV[5,5]=tempn
    #
    CTTV=tempc*CTTV
    # integration points
    nint, con, wps = 8, 1/np.sqrt(3), 1

    pint = np.array([[-con, -con, -con],
                     [ con, -con, -con],
                     [ con,  con, -con],
                     [-con,  con, -con],
                     [-con, -con,  con],
                     [ con, -con,  con],
                     [ con,  con,  con],
                     [-con,  con,  con]])
    # ------------------------------------------------------------------
    # B-bar: compute B at centroid (0,0,0) and extract dilatational part
    # ------------------------------------------------------------------
    # dilatational projector: m = [1,1,1,0,0,0]^T
    # B_dil = (1/3) * m * m^T * B  extracts the volumetric part of B
    # ------------------------------------------------------------------
    phi0, dphi0 = shapeH8(0., 0., 0.)   #no centroide
    JAC0, detJAC0, iJAC0 = calcJAC(dphi0, coord, connect, ee)
    dphi_t0 = iJAC0 @ dphi0
    B0 = calcB(dphi_t0)
    # dilatational part of B at centroid: Bbar_dil = (1/3) m m^T B0
    # m^T B0 extracts row0+row1+row2 of B0 (the trace of strain)
    # then (1/3) m * (that row) distributes it equally to rows 0,1,2
    mTB0 = B0[0,:] + B0[1,:] + B0[2,:]  # (1x24) = m^T * B0
    Bbar_dil = np.zeros((6, 3*8))
    Bbar_dil[0,:] = mTB0/3.
    Bbar_dil[1,:] = mTB0/3.
    Bbar_dil[2,:] = mTB0/3.
    # rows 3,4,5 of Bbar_dil are zero (shear has no dilatational part)
    # 
    Ke, Me = 0, 0
    N = np.zeros((3,3*8))
    # integration
    for i in range(nint):
        ssx, ttx, rrx = pint[i, 0], pint[i, 1], pint[i, 2]
        phi, dphi = shapeH8(ssx,ttx,rrx)
        JAC, detJAC, iJAC = calcJAC(dphi, coord, connect, ee)
        dphi_t = iJAC @ dphi
        B = calcB(dphi_t)
        # ------------------------------------------------------------------
        # B-bar: replace dilatational part of B by centroid dilatational part
        # Bbar = B - B_dil(gauss_pt) + Bbar_dil(centroid)
        # ------------------------------------------------------------------
        # dilatational part of B at this Gauss point
        mTB = B[0,:] + B[1,:] + B[2,:]  # (1x24)
        Bdil = np.zeros((6, 3*8))
        Bdil[0,:] = mTB/3.
        Bdil[1,:] = mTB/3.
        Bdil[2,:] = mTB/3.
        # B-bar = deviatoric(gauss_pt) + dilatational(centroid)
        Bbar = B - Bdil + Bbar_dil

        for iii in range(8): 
            N[0,3*iii+0]=phi[iii]
            N[0,3*iii+1]=0
            N[0,3*iii+2]=0
            N[1,3*iii+0]=0
            N[1,3*iii+1]=phi[iii]
            N[1,3*iii+2]=0
            N[2,3*iii+0]=0
            N[2,3*iii+1]=0
            N[2,3*iii+2]=phi[iii]
      
        Ke += Bbar.T@CTTV@Bbar*(detJAC*wps)
        Me += rho*N.T@N*(detJAC*wps)
        
    return Ke, Me

def generate_ind_rows_cols(connect):
    # processing the dofs indices (rows and columns) for assembly
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


def stif_mass_matrices(coord, connect, nnode, nel, ind_rows, ind_cols, E, vv, rho, bbar=False):
    """ Calculates global matrices.
    """
    ngl = 3 * nnode
    data_k = np.zeros((nel, (3*8)*(3*8)), dtype=float)
    data_m = np.zeros((nel, (3*8)*(3*8)), dtype=float)
    
    for el in range(nel): #Aqui inventei, sei lá se deu certo, kkkk
        if bbar:
            Ke, Me = matricesH8S_Bbar(el, coord, connect, E, vv, rho)
        else:
            Ke, Me = matricesH8S(el, coord, connect, E, vv, rho)
        data_k[el,:] = Ke.flatten() 
        data_m[el,:] = Me.flatten() 
   
    data_k = data_k.flatten()
    data_m = data_m.flatten()
    stif_matrix = csr_matrix((data_k, (ind_rows, ind_cols)), shape=(ngl, ngl))
    mass_matrix = csr_matrix((data_m, (ind_rows, ind_cols)), shape=(ngl, ngl))

    return stif_matrix, mass_matrix