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


def get_detJAC_and_invJAC(JAC):
    """
    """
    
    detJAC = (  JAC[0,0] * JAC[1,1] * JAC[2,2] + 
                JAC[0,1] * JAC[1,2] * JAC[2,0] + 
                JAC[0,2] * JAC[1,0] * JAC[2,1]  ) - \
             (  JAC[2,0] * JAC[1,1] * JAC[0,2] + 
                JAC[2,1] * JAC[1,2] * JAC[0,0] + 
                JAC[2,2] * JAC[1,0] * JAC[0,1]  )
    
    # adj(JAC)
    AUJJ = np.zeros((3,3), dtype=float)
    AUJJ[0,0] =  1 * ((JAC[1,1] * JAC[2,2]) - (JAC[2,1] * JAC[1,2]))
    AUJJ[1,0] = -1 * ((JAC[1,0] * JAC[2,2]) - (JAC[1,2] * JAC[2,0]))
    AUJJ[2,0] =  1 * ((JAC[1,0] * JAC[2,1]) - (JAC[1,1] * JAC[2,0]))
    AUJJ[0,1] = -1 * ((JAC[0,1] * JAC[2,2]) - (JAC[0,2] * JAC[2,1]))
    AUJJ[1,1] =  1 * ((JAC[0,0] * JAC[2,2]) - (JAC[0,2] * JAC[2,0]))
    AUJJ[2,1] = -1 * ((JAC[0,0] * JAC[2,1]) - (JAC[0,1] * JAC[2,0]))
    AUJJ[0,2] =  1 * ((JAC[0,1] * JAC[1,2]) - (JAC[0,2] * JAC[1,1]))
    AUJJ[1,2] = -1 * ((JAC[0,0] * JAC[1,2]) - (JAC[0,2] * JAC[1,0]))
    AUJJ[2,2] =  1 * ((JAC[0,0] * JAC[1,1]) - (JAC[0,1] * JAC[1,0]))

    return detJAC, (1/detJAC) * AUJJ


def get_detJAC_and_invJAC_3D(JAC):
    """
    """
    
    detJAC = (  JAC[:,0,0] * JAC[:,1,1] * JAC[:,2,2] + 
                JAC[:,0,1] * JAC[:,1,2] * JAC[:,2,0] + 
                JAC[:,0,2] * JAC[:,1,0] * JAC[:,2,1]  ) - \
             (  JAC[:,2,0] * JAC[:,1,1] * JAC[:,0,2] + 
                JAC[:,2,1] * JAC[:,1,2] * JAC[:,0,0] + 
                JAC[:,2,2] * JAC[:,1,0] * JAC[:,0,1]  )
    detJAC = detJAC.reshape(-1, 1, 1)
    # adj(JAC)
    AUJJ = np.zeros((detJAC.shape[0], 3, 3), dtype=float)
    AUJJ[:,0,0] =  1 * ((JAC[:,1,1] * JAC[:,2,2]) - (JAC[:,2,1] * JAC[:,1,2]))
    AUJJ[:,1,0] = -1 * ((JAC[:,1,0] * JAC[:,2,2]) - (JAC[:,1,2] * JAC[:,2,0]))
    AUJJ[:,2,0] =  1 * ((JAC[:,1,0] * JAC[:,2,1]) - (JAC[:,1,1] * JAC[:,2,0]))
    AUJJ[:,0,1] = -1 * ((JAC[:,0,1] * JAC[:,2,2]) - (JAC[:,0,2] * JAC[:,2,1]))
    AUJJ[:,1,1] =  1 * ((JAC[:,0,0] * JAC[:,2,2]) - (JAC[:,0,2] * JAC[:,2,0]))
    AUJJ[:,2,1] = -1 * ((JAC[:,0,0] * JAC[:,2,1]) - (JAC[:,0,1] * JAC[:,2,0]))
    AUJJ[:,0,2] =  1 * ((JAC[:,0,1] * JAC[:,1,2]) - (JAC[:,0,2] * JAC[:,1,1]))
    AUJJ[:,1,2] = -1 * ((JAC[:,0,0] * JAC[:,1,2]) - (JAC[:,0,2] * JAC[:,1,0]))
    AUJJ[:,2,2] =  1 * ((JAC[:,0,0] * JAC[:,1,1]) - (JAC[:,0,1] * JAC[:,1,0]))

    return detJAC, (1/detJAC) * AUJJ


class STRUCT_HEXAHEDRON_8:
    def __init__(self, structural_element):
        
        self.structural_element = structural_element
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def initialize_variables(self):
        """
        """
        self.element_label = "structural_hexahedron_8"
        self.nodal_coordinates = self.structural_element.mesher.nodal_coordinates.copy()
        self.connect = self.structural_element.mesher.connectivity_matrix.copy()
        #
        self.number_of_nodes = self.structural_element.mesher.number_of_nodes
        self.number_of_elements = self.structural_element.mesher.number_of_elements
        #
        self.nodes_per_element = 8
        self.dof_per_node = 3
        self.dofs_per_element = int(self.dof_per_node*self.nodes_per_element)

 
    def define_integration_points(self):
        """
        """
        # integration points
        self.nint = 8
        con = 1/np.sqrt(3)
        self.wps = 1

        self.pint = np.array([  [-con, -con, -con],
                                [ con, -con, -con],
                                [ con,  con, -con],
                                [-con,  con, -con],
                                [-con, -con,  con],
                                [ con, -con,  con],
                                [ con,  con,  con],
                                [-con,  con,  con]  ])


    def process_shape_functions_and_derivatives(self):
        """ This method processes the shape functions and their
            derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1] 
        rrx = self.pint[:, 2]
        #
        denominator = 8
        # shape functions 
        phi = np.zeros((self.nint, self.nodes_per_element), dtype=float)
        #
        phi[:, 0] = (1.-ssx)*(1.-ttx)*(1.-rrx)
        phi[:, 1] = (1.+ssx)*(1.-ttx)*(1.-rrx)
        phi[:, 2] = (1.+ssx)*(1.+ttx)*(1.-rrx)
        phi[:, 3] = (1.-ssx)*(1.+ttx)*(1.-rrx)
        phi[:, 4] = (1.-ssx)*(1.-ttx)*(1.+rrx)
        phi[:, 5] = (1.+ssx)*(1.-ttx)*(1.+rrx)
        phi[:, 6] = (1.+ssx)*(1.+ttx)*(1.+rrx)
        phi[:, 7] = (1.-ssx)*(1.+ttx)*(1.+rrx)
        phi = phi/denominator
        #
        # derivatives
        dphi = np.zeros((self.nint, self.dof_per_node, self.nodes_per_element), dtype=float)
        #
        dphi[:, 0, 0] = (-1.)*(1.-ttx)*(1.-rrx)
        dphi[:, 0, 1] = (1.)*(1.-ttx)*(1.-rrx)
        dphi[:, 0, 2] = (1.)*(1.+ttx)*(1.-rrx)
        dphi[:, 0, 3] = (-1.)*(1.+ttx)*(1.-rrx)
        dphi[:, 0, 4] = (-1.)*(1.-ttx)*(1.+rrx)
        dphi[:, 0, 5] = (1.)*(1.-ttx)*(1.+rrx)
        dphi[:, 0, 6] = (1.)*(1.+ttx)*(1.+rrx)
        dphi[:, 0, 7] = (-1.)*(1.+ttx)*(1.+rrx)
        
        dphi[:, 1, 0] = (1.-ssx)*(-1.)*(1.-rrx)
        dphi[:, 1, 1] = (1.+ssx)*(-1.)*(1.-rrx)
        dphi[:, 1, 2] = (1.+ssx)*(1.)*(1.-rrx)
        dphi[:, 1, 3] = (1.-ssx)*(1.)*(1.-rrx)
        dphi[:, 1, 4] = (1.-ssx)*(-1.)*(1.+rrx)
        dphi[:, 1, 5] = (1.+ssx)*(-1.)*(1.+rrx)
        dphi[:, 1, 6] = (1.+ssx)*(1.)*(1.+rrx)
        dphi[:, 1, 7] = (1.-ssx)*(1.)*(1.+rrx)
        
        dphi[:, 2, 0] = (1.-ssx)*(1.-ttx)*(-1.)
        dphi[:, 2, 1] = (1.+ssx)*(1.-ttx)*(-1.)
        dphi[:, 2, 2] = (1.+ssx)*(1.+ttx)*(-1.)
        dphi[:, 2, 3] = (1.-ssx)*(1.+ttx)*(-1.)
        dphi[:, 2, 4] = (1.-ssx)*(1.-ttx)*(1.)
        dphi[:, 2, 5] = (1.+ssx)*(1.-ttx)*(1.)
        dphi[:, 2, 6] = (1.+ssx)*(1.+ttx)*(1.)
        dphi[:, 2, 7] = (1.-ssx)*(1.+ttx)*(1.)
            
        dphi = dphi/denominator

        self.phi = phi
        self.dphi = dphi


    def process_constitutive_model(self, model_type="linear-isotropic"):
        """ This method process the material constitutive model.
        """
        vv = self.structural_element.poisson
        E = self.structural_element.elasticity_modulus
        if model_type == "linear-isotropic":
            # Constititive model - Linear isotropic material
            #
            tempc = E/((1+vv)*(1-2*vv))
            tempn = (1-2*vv)/2
            tempt = 1-vv
            #
            const_law = np.array([  [tempt,    vv,    vv,     0,     0,     0],
                                    [   vv, tempt,    vv,     0,     0,     0],
                                    [   vv,    vv, tempt,     0,     0,     0],
                                    [    0,     0,     0, tempn,     0,     0],
                                    [    0,     0,     0,     0, tempn,     0],
                                    [    0,     0,     0,     0,     0, tempn]  ])
            self.const_mat = tempc*const_law


    def elementary_matrices(self, el_index):
        """ This method returns elementary stiffness and mass matrices for HEXAHEDRON-8 nodes.
            ANSYS SOLID45 w/o extra diplacements (very simple)
        """
        #
        ie = self.connect[el_index, 1:] - 1
        rho = self.structural_element.material_density
        #
        JAC = self.dphi@self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = get_detJAC_and_invJAC_3D(JAC)
        dphi_t = invJAC @ self.dphi
        #
        B = np.zeros((self.nint, 6, self.dofs_per_element), dtype=float)
        N = np.zeros((self.nint, 3, self.dofs_per_element), dtype=float)
        #
        B[:, 0, 0::3] = dphi_t[:, 0, :]
        B[:, 1, 1::3] = dphi_t[:, 1, :]
        B[:, 2, 2::3] = dphi_t[:, 2, :]
        B[:, 3, 0::3] = dphi_t[:, 1, :]
        B[:, 3, 1::3] = dphi_t[:, 0, :]
        B[:, 4, 0::3] = dphi_t[:, 2, :]
        B[:, 4, 2::3] = dphi_t[:, 0, :]
        B[:, 5, 1::3] = dphi_t[:, 2, :]
        B[:, 5, 2::3] = dphi_t[:, 1, :]
        #
        N[:, 0, 0::3] = self.phi
        N[:, 1, 1::3] = self.phi
        N[:, 2, 2::3] = self.phi
        #
        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            
            Ke += B[i,:,:].T@self.const_mat@B[i,:,:]*(detJAC[i,:,:]*self.wps)
            Me += rho*N[i,:,:].T@N[i,:,:]*(detJAC[i,:,:]*self.wps)
        #
        return Ke, Me


    def elementary_matrices_base(self, el_index):
        """ This method returns elementary stiffness and mass matrices for HEXAHEDRON-8 nodes.
            ANSYS SOLID45 w/o extra diplacements (very simple)
        """
        #
        ie = self.connect[el_index, 1:] - 1
        rho = self.structural_element.material_density
        #
        B = np.zeros((6, self.dofs_per_element), dtype=float)
        N = np.zeros((3, self.dofs_per_element), dtype=float)
        #
        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            
            phi, dphi = shapeH8(self.pint[i, 0], self.pint[i, 1], self.pint[i, 2])
            
            JAC = dphi@self.nodal_coordinates[ie, 1:4] 
            detJAC, iJAC = get_detJAC_and_invJAC(JAC) 
            dphi_t = iJAC @ dphi
            
            for iii in range(8):
                B[0,3*(iii)+0]=dphi_t[0,iii]
                B[1,3*(iii)+1]=dphi_t[1,iii]
                B[2,3*(iii)+2]=dphi_t[2,iii]
                B[3,3*(iii)+0]=dphi_t[1,iii]
                B[3,3*(iii)+1]=dphi_t[0,iii]          
                B[4,3*(iii)+0]=dphi_t[2,iii]
                B[4,3*(iii)+2]=dphi_t[0,iii]
                B[5,3*(iii)+1]=dphi_t[2,iii]
                B[5,3*(iii)+2]=dphi_t[1,iii]

            for iii in range(8): 
                N[0,3*iii+0]=phi[iii]
                N[1,3*iii+1]=phi[iii]
                N[2,3*iii+2]=phi[iii]
        
            Ke += B.T@self.const_mat@B*(detJAC*self.wps)
            Me += rho*N.T@N*(detJAC*self.wps)
            
        return Ke, Me


    def reorder_connect(self):
        """
        """
        self.connect = self.connect[:, [0, 4, 5, 6, 7, 8, 9, 10, 11]]


    def generate_ind_rows_cols(self):
        """ This method process the dofs indices (rows and columns) to assembly of global matrices.
        """
        # processing the dofs indices (rows and columns) for assembly
        self.process_constitutive_model()
        self.reorder_connect()
        dofs, edofs = self.dof_per_node, self.dofs_per_element
        ind_dofs = (np.array([  dofs*self.connect[:,1]-1, dofs*self.connect[:,1], dofs*self.connect[:,1]+1,
                                dofs*self.connect[:,2]-1, dofs*self.connect[:,2], dofs*self.connect[:,2]+1,
                                dofs*self.connect[:,3]-1, dofs*self.connect[:,3], dofs*self.connect[:,3]+1,
                                dofs*self.connect[:,4]-1, dofs*self.connect[:,4], dofs*self.connect[:,4]+1,
                                dofs*self.connect[:,5]-1, dofs*self.connect[:,5], dofs*self.connect[:,5]+1,
                                dofs*self.connect[:,6]-1, dofs*self.connect[:,6], dofs*self.connect[:,6]+1,
                                dofs*self.connect[:,7]-1, dofs*self.connect[:,7], dofs*self.connect[:,7]+1,
                                dofs*self.connect[:,8]-1, dofs*self.connect[:,8], dofs*self.connect[:,8]+1  ], dtype=int)-2).T
        vect_indices = ind_dofs.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs,1))).T).flatten()
        self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()
        return self.ind_rows, self.ind_cols
    

    def stif_mass_matrices(self):
        """ Calculates global matrices.
        """
        dofs = self.dof_per_node * self.nodes_per_element
        nel = self.number_of_elements
        total_dofs = self.dof_per_node*self.number_of_nodes

        data_k = np.zeros((nel, dofs**2), dtype=float)
        data_m = np.zeros((nel, dofs**2), dtype=float) 
        
        for el in range(nel):
            Ke, Me = self.elementary_matrices(el)
            # print(Ke)
            # print(Me)
            data_k[el,:] = Ke.flatten() 
            data_m[el,:] = Me.flatten() 
    
        data_k = data_k.flatten()
        data_m = data_m.flatten()
        stif_matrix = csr_matrix((data_k, (self.ind_rows, self.ind_cols)), shape=(total_dofs, total_dofs))
        mass_matrix = csr_matrix((data_m, (self.ind_rows, self.ind_cols)), shape=(total_dofs, total_dofs))

        return stif_matrix, mass_matrix