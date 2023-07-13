import numpy as np
from vibra.engine.elements.element import Element


def shapeT4C(ssx, ttx, rrx):
    """ This function returns the shape functions and its derivatives.
    """
    # shape functions 
    phi = np.array([1-ssx-ttx-rrx, ttx, rrx, ssx], dtype=float)
    # derivatives
    dphi = np.array([[-1, 0, 0, 1],
                     [-1, 1, 0, 0],
                     [-1, 0, 1, 0]], dtype=float)

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


class STRUCT_TETRAHEDRON_4S(Element):
    #
    NODES_PER_ELEMENT = 4
    DOF_PER_NODE = 3
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE
    
    def __init__(self, model):
        
        self.model = model
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def initialize_variables(self):
        """
        """
        self.element_label = "structural_tetrahedron_4"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.connect= self.model.mesh.solids_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connect)

    def define_integration_points(self):
        """
        """
        # integration points
        # nint = 1
        # con = 1/4
        # pint = np.array([[ con, con, con]])
        # wps = 1
        #integration points
        self.nint = 4
        con1 = (5 - np.sqrt(5))/20
        con2 = (5 + 3*np.sqrt(5))/20
        self.wps = 1/4
        self.pint = np.array([  [ con1, con1, con1],
                                [ con1, con1, con2],
                                [ con1, con2, con1],
                                [ con2, con1, con1]  ])

    def process_shape_functions_and_derivatives(self):
        """ This method processes the shape functions and their
            derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        rrx = self.pint[:, 2]
        # shape functions 
        self.phi = np.array([1-ssx-ttx-rrx, ttx, rrx, ssx], dtype=float)
        # derivatives
        self.dphi = np.array([  [-1, 0, 0, 1],
                                [-1, 1, 0, 0],
                                [-1, 0, 1, 0]  ], dtype=float)


    def get_constitutive_model(self, el_index, model_type="linear-isotropic"):
        """
        """
        self.material = self.model.properties.get_material(element=el_index)
        vv = self.material.poisson
        E = self.material.elasticity_modulus

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
            
            return tempc*const_law

    def elementary_matrices(self, el_index):
        """ Stiffness and mass matrices.
            This is not a p-u mixed fomulation. Do not compare with SOLID285.
        """  
        #
        ie = self.connect[el_index, 1:]

        const_mat= self.get_constitutive_model(ie, model_type="linear-isotropic")
        rho = self.material.density
        #
        JAC = self.dphi@self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = get_detJAC_and_invJAC(JAC)
        dphi_t = invJAC @ self.dphi
        #
        B = np.zeros((6, self.DOFS_PER_ELEMENT), dtype=float)
        N = np.zeros((self.nint, 3, self.DOFS_PER_ELEMENT), dtype=float)
        #
        B[0, 0::3] = dphi_t[0, :]
        B[1, 1::3] = dphi_t[1, :]
        B[2, 2::3] = dphi_t[2, :]
        B[3, 0::3] = dphi_t[1, :]
        B[3, 1::3] = dphi_t[0, :]
        B[4, 0::3] = dphi_t[2, :]
        B[4, 2::3] = dphi_t[0, :]
        B[5, 1::3] = dphi_t[2, :]
        B[5, 2::3] = dphi_t[1, :]
        #
        N[:, 0, 0::3] = self.phi
        N[:, 1, 1::3] = self.phi
        N[:, 2, 2::3] = self.phi
        #
        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):

            Ke += (1/6)*B.T@const_mat@B*(detJAC*self.wps)
            Me += (1/6)*rho*N[i,:,:].T@N[i,:,:]*(detJAC*self.wps)

        return Ke, Me        
     
    def reorder_connect(self):
        """ Reordering connectivity matrix to adequate the GMSH connectivity to the FE model """
        self.connect = self.connect[:, [0, 6, 4, 5, 7]]

    def generate_ind_rows_cols(self):
        """ This method processess the dofs indices (rows and columns) for assembly """

        self.reorder_connect()
        dofs, edofs = self.DOF_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = (np.array([  dofs*self.connect[:,1]-1, dofs*self.connect[:,1], dofs*self.connect[:,1]+1,
                                dofs*self.connect[:,2]-1, dofs*self.connect[:,2], dofs*self.connect[:,2]+1,
                                dofs*self.connect[:,3]-1, dofs*self.connect[:,3], dofs*self.connect[:,3]+1,
                                dofs*self.connect[:,4]-1, dofs*self.connect[:,4], dofs*self.connect[:,4]+1  ], dtype=int)-2).T

        vect_indices = ind_dofs.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs,1))).T).flatten()
        self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()

        return self.ind_rows, self.ind_cols