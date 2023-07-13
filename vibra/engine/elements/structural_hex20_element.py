import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs
from time import time


def shapeH20(ssx, ttx, rrx):
    """ Shape Functions and Derivatives.
    """
    div8=1/8
    div4=1/4
    # shape functions 
    phit = np.zeros(20, dtype=float)
    #
    phit[0]=div8*(1-ssx)*(1-ttx)*(1-rrx)*(-ssx-ttx-rrx-2)
    phit[1]=div8*(1+ssx)*(1-ttx)*(1-rrx)*(ssx-ttx-rrx-2)
    phit[2]=div8*(1+ssx)*(1+ttx)*(1-rrx)*(ssx+ttx-rrx-2)
    phit[3]=div8*(1-ssx)*(1+ttx)*(1-rrx)*(-ssx+ttx-rrx-2)
    phit[4]=div8*(1-ssx)*(1-ttx)*(1+rrx)*(-ssx-ttx+rrx-2)
    phit[5]=div8*(1+ssx)*(1-ttx)*(1+rrx)*(ssx-ttx+rrx-2)
    phit[6]=div8*(1+ssx)*(1+ttx)*(1+rrx)*(ssx+ttx+rrx-2)
    phit[7]=div8*(1-ssx)*(1+ttx)*(1+rrx)*(-ssx+ttx+rrx-2)
    #
    phit[8]=div4*(1-ssx**2)*(1-ttx)*(1-rrx)
    phit[9]=div4*(1+ssx)*(1-ttx**2)*(1-rrx)
    phit[10]=div4*(1-ssx**2)*(1+ttx)*(1-rrx)
    phit[11]=div4*(1-ssx)*(1-ttx**2)*(1-rrx)
    phit[12]=div4*(1-ssx**2)*(1-ttx)*(1+rrx)
    phit[13]=div4*(1+ssx)*(1-ttx**2)*(1+rrx)
    phit[14]=div4*(1-ssx**2)*(1+ttx)*(1+rrx)
    phit[15]=div4*(1-ssx)*(1-ttx**2)*(1+rrx)
    phit[16]=div4*(1-ssx)*(1-ttx)*(1-rrx**2)
    phit[17]=div4*(1+ssx)*(1-ttx)*(1-rrx**2)
    phit[18]=div4*(1+ssx)*(1+ttx)*(1-rrx**2)
    phit[19]=div4*(1-ssx)*(1+ttx)*(1-rrx**2)

    # derivatives
    dphit = np.zeros((3,20), dtype=float)
    #
    dphit[0,0]=div8*(1-ttx)*(1-rrx)*(-(-ssx-ttx-rrx-2)+(1-ssx)*(-1))
    dphit[0,1]=div8*(1-ttx)*(1-rrx)*(+(ssx-ttx-rrx-2)+(1+ssx)*(1))
    dphit[0,2]=div8*(1+ttx)*(1-rrx)*(+(ssx+ttx-rrx-2)+(1+ssx)*(1))
    dphit[0,3]=div8*(1+ttx)*(1-rrx)*(-(-ssx+ttx-rrx-2)+(1-ssx)*(-1))
    dphit[0,4]=div8*(1-ttx)*(1+rrx)*(-(-ssx-ttx+rrx-2)+(1-ssx)*(-1)) 
    dphit[0,5]=div8*(1-ttx)*(1+rrx)*(+(ssx-ttx+rrx-2)+(1+ssx)*(1)) 
    dphit[0,6]=div8*(1+ttx)*(1+rrx)*(+(ssx+ttx+rrx-2)+(1+ssx)*(1)) 
    dphit[0,7]=div8*(1+ttx)*(1+rrx)*(-(-ssx+ttx+rrx-2)+(1-ssx)*(-1))
    dphit[0,8]=div4*(-2*ssx)*(1-ttx)*(1-rrx)
    dphit[0,9]=div4*(1)*(1-ttx**2)*(1-rrx)
    dphit[0,10]=div4*(-2*ssx)*(1+ttx)*(1-rrx)
    dphit[0,11]=div4*(-1)*(1-ttx**2)*(1-rrx)
    dphit[0,12]=div4*(-2*ssx)*(1-ttx)*(1+rrx)
    dphit[0,13]=div4*(1)*(1-ttx**2)*(1+rrx)
    dphit[0,14]=div4*(-2*ssx)*(1+ttx)*(1+rrx)
    dphit[0,15]=div4*(-1)*(1-ttx**2)*(1+rrx)
    dphit[0,16]=div4*(-1)*(1-ttx)*(1-rrx**2)
    dphit[0,17]=div4*(1)*(1-ttx)*(1-rrx**2)
    dphit[0,18]=div4*(1)*(1+ttx)*(1-rrx**2)
    dphit[0,19]=div4*(-1)*(1+ttx)*(1-rrx**2)
    #
    dphit[1,0]=div8*(1-ssx)*(1-rrx)*(-(-ssx-ttx-rrx-2)+(1-ttx)*(-1)) 
    dphit[1,1]=div8*(1+ssx)*(1-rrx)*(-(ssx-ttx-rrx-2)+(1-ttx)*(-1)) 
    dphit[1,2]=div8*(1+ssx)*(1-rrx)*(+(ssx+ttx-rrx-2)+(1+ttx)*(1)) 
    dphit[1,3]=div8*(1-ssx)*(1-rrx)*(+(-ssx+ttx-rrx-2)+(1+ttx)*(1)) 
    dphit[1,4]=div8*(1-ssx)*(1+rrx)*(-(-ssx-ttx+rrx-2)+(1-ttx)*(-1)) 
    dphit[1,5]=div8*(1+ssx)*(1+rrx)*(-(ssx-ttx+rrx-2)+(1-ttx)*(-1)) 
    dphit[1,6]=div8*(1+ssx)*(1+rrx)*(+(ssx+ttx+rrx-2)+(1+ttx)*(1)) 
    dphit[1,7]=div8*(1-ssx)*(1+rrx)*(+(-ssx+ttx+rrx-2)+(1+ttx)*(1))
    dphit[1,8]=div4*(1-ssx**2)*(-1)*(1-rrx)
    dphit[1,9]=div4*(1+ssx)*(-2*ttx)*(1-rrx)
    dphit[1,10]=div4*(1-ssx**2)*(1)*(1-rrx)
    dphit[1,11]=div4*(1-ssx)*(-2*ttx)*(1-rrx)
    dphit[1,12]=div4*(1-ssx**2)*(-1)*(1+rrx)
    dphit[1,13]=div4*(1+ssx)*(-2*ttx)*(1+rrx)
    dphit[1,14]=div4*(1-ssx**2)*(1)*(1+rrx)
    dphit[1,15]=div4*(1-ssx)*(-2*ttx)*(1+rrx)
    dphit[1,16]=div4*(1-ssx)*(-1)*(1-rrx**2)
    dphit[1,17]=div4*(1+ssx)*(-1)*(1-rrx**2)
    dphit[1,18]=div4*(1+ssx)*(1)*(1-rrx**2)
    dphit[1,19]=div4*(1-ssx)*(1)*(1-rrx**2)
    #
    dphit[2,0]=div8*(1-ssx)*(1-ttx)*(-(-ssx-ttx-rrx-2)+(1-rrx)*(-1)) 
    dphit[2,1]=div8*(1+ssx)*(1-ttx)*(-(ssx-ttx-rrx-2)+(1-rrx)*(-1)) 
    dphit[2,2]=div8*(1+ssx)*(1+ttx)*(-(ssx+ttx-rrx-2)+(1-rrx)*(-1)) 
    dphit[2,3]=div8*(1-ssx)*(1+ttx)*(-(-ssx+ttx-rrx-2)+(1-rrx)*(-1)) 
    dphit[2,4]=div8*(1-ssx)*(1-ttx)*(+(-ssx-ttx+rrx-2)+(1+rrx)*(1)) 
    dphit[2,5]=div8*(1+ssx)*(1-ttx)*(+(ssx-ttx+rrx-2)+(1+rrx)*(1)) 
    dphit[2,6]=div8*(1+ssx)*(1+ttx)*(+(ssx+ttx+rrx-2)+(1+rrx)*(1)) 
    dphit[2,7]=div8*(1-ssx)*(1+ttx)*(+(-ssx+ttx+rrx-2)+(1+rrx)*(1)) 
    dphit[2,8]=div4*(1-ssx**2)*(1-ttx)*(-1)
    dphit[2,9]=div4*(1+ssx)*(1-ttx**2)*(-1)
    dphit[2,10]=div4*(1-ssx**2)*(1+ttx)*(-1)
    dphit[2,11]=div4*(1-ssx)*(1-ttx**2)*(-1)
    dphit[2,12]=div4*(1-ssx**2)*(1-ttx)*(1)
    dphit[2,13]=div4*(1+ssx)*(1-ttx**2)*(1)
    dphit[2,14]=div4*(1-ssx**2)*(1+ttx)*(1)
    dphit[2,15]=div4*(1-ssx)*(1-ttx**2)*(1)
    dphit[2,16]=div4*(1-ssx)*(1-ttx)*(-2*rrx)
    dphit[2,17]=div4*(1+ssx)*(1-ttx)*(-2*rrx)
    dphit[2,18]=div4*(1+ssx)*(1+ttx)*(-2*rrx)
    dphit[2,19]=div4*(1-ssx)*(1+ttx)*(-2*rrx)

    return phit, dphit


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


class STRUCT_HEXAHEDRON_20:
    def __init__(self, structural_element):
        
        self.structural_element = structural_element
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def initialize_variables(self):
        """
        """
        self.element_label = "structural_hexahedron_20"
        self.nodal_coordinates = self.structural_element.mesher.nodal_coordinates.copy()
        self.connect = self.structural_element.mesher.connectivity_matrix.copy()
        #
        self.number_of_nodes = self.structural_element.mesher.number_of_nodes
        self.number_of_elements = self.structural_element.mesher.number_of_elements
        #
        self.nodes_per_element = 20
        self.dof_per_node = 3
        self.dofs_per_element = int(self.dof_per_node*self.nodes_per_element)


    def define_integration_points(self):
        """
        """
        # integration points
        self.nint = 14
        self.wps = np.zeros((self.nint))
        con1 = np.sqrt(19/33)
        con2 = np.sqrt(19/30)
        # self.pint = np.zeros((self.nint,3))
        self.pint = np.array([  [-con1, -con1, -con1],
                                [ con1, -con1, -con1],
                                [ con1,  con1, -con1],
                                [-con1,  con1, -con1],
                                [-con1, -con1,  con1],
                                [ con1, -con1,  con1],
                                [ con1,  con1,  con1],
                                [-con1,  con1,  con1],
                                [-con2,     0,     0],
                                [    0,     0, -con2],
                                [    0,  con2,     0],
                                [    0,     0,  con2],
                                [    0, -con2,     0],
                                [ con2,     0,     0]  ])
        #
        for ixc in [0, 1, 2, 3, 4, 5, 6, 7]:
            self.wps[ixc] = 121/361
        #
        for ixc in [8, 9, 10, 11, 12, 13]:
            self.wps[ixc] = 320/361


    def process_shape_functions_and_derivatives(self):
        """ This method processes the shape functions and their
            derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1] 
        rrx = self.pint[:, 2]
        #
        div8=1/8
        div4=1/4
        # shape functions 
        phit = np.zeros((self.nint, self.nodes_per_element), dtype=float)
        #
        phit[:, 0] = div8*(1-ssx)*(1-ttx)*(1-rrx)*(-ssx-ttx-rrx-2)
        phit[:, 1] = div8*(1+ssx)*(1-ttx)*(1-rrx)*(ssx-ttx-rrx-2)
        phit[:, 2] = div8*(1+ssx)*(1+ttx)*(1-rrx)*(ssx+ttx-rrx-2)
        phit[:, 3] = div8*(1-ssx)*(1+ttx)*(1-rrx)*(-ssx+ttx-rrx-2)
        phit[:, 4] = div8*(1-ssx)*(1-ttx)*(1+rrx)*(-ssx-ttx+rrx-2)
        phit[:, 5] = div8*(1+ssx)*(1-ttx)*(1+rrx)*(ssx-ttx+rrx-2)
        phit[:, 6] = div8*(1+ssx)*(1+ttx)*(1+rrx)*(ssx+ttx+rrx-2)
        phit[:, 7] = div8*(1-ssx)*(1+ttx)*(1+rrx)*(-ssx+ttx+rrx-2)
        #
        phit[:, 8] = div4*(1-ssx**2)*(1-ttx)*(1-rrx)
        phit[:, 9] = div4*(1+ssx)*(1-ttx**2)*(1-rrx)
        phit[:, 10] = div4*(1-ssx**2)*(1+ttx)*(1-rrx)
        phit[:, 11] = div4*(1-ssx)*(1-ttx**2)*(1-rrx)
        phit[:, 12] = div4*(1-ssx**2)*(1-ttx)*(1+rrx)
        phit[:, 13] = div4*(1+ssx)*(1-ttx**2)*(1+rrx)
        phit[:, 14] = div4*(1-ssx**2)*(1+ttx)*(1+rrx)
        phit[:, 15] = div4*(1-ssx)*(1-ttx**2)*(1+rrx)
        phit[:, 16] = div4*(1-ssx)*(1-ttx)*(1-rrx**2)
        phit[:, 17] = div4*(1+ssx)*(1-ttx)*(1-rrx**2)
        phit[:, 18] = div4*(1+ssx)*(1+ttx)*(1-rrx**2)
        phit[:, 19] = div4*(1-ssx)*(1+ttx)*(1-rrx**2)
        #
        # derivatives
        dphit = np.zeros((self.nint, self.dof_per_node, self.nodes_per_element), dtype=float)
        #
        dphit[:, 0, 0] = div8*(1-ttx)*(1-rrx)*(-(-ssx-ttx-rrx-2)+(1-ssx)*(-1))
        dphit[:, 0, 1] = div8*(1-ttx)*(1-rrx)*(+(ssx-ttx-rrx-2)+(1+ssx)*(1))
        dphit[:, 0, 2] = div8*(1+ttx)*(1-rrx)*(+(ssx+ttx-rrx-2)+(1+ssx)*(1))
        dphit[:, 0, 3] = div8*(1+ttx)*(1-rrx)*(-(-ssx+ttx-rrx-2)+(1-ssx)*(-1))
        dphit[:, 0, 4] = div8*(1-ttx)*(1+rrx)*(-(-ssx-ttx+rrx-2)+(1-ssx)*(-1)) 
        dphit[:, 0, 5] = div8*(1-ttx)*(1+rrx)*(+(ssx-ttx+rrx-2)+(1+ssx)*(1)) 
        dphit[:, 0, 6] = div8*(1+ttx)*(1+rrx)*(+(ssx+ttx+rrx-2)+(1+ssx)*(1)) 
        dphit[:, 0, 7] = div8*(1+ttx)*(1+rrx)*(-(-ssx+ttx+rrx-2)+(1-ssx)*(-1))
        dphit[:, 0, 8] = div4*(-2*ssx)*(1-ttx)*(1-rrx)
        dphit[:, 0, 9] = div4*(1)*(1-ttx**2)*(1-rrx)
        dphit[:, 0, 10] = div4*(-2*ssx)*(1+ttx)*(1-rrx)
        dphit[:, 0, 11] = div4*(-1)*(1-ttx**2)*(1-rrx)
        dphit[:, 0, 12] = div4*(-2*ssx)*(1-ttx)*(1+rrx)
        dphit[:, 0, 13] = div4*(1)*(1-ttx**2)*(1+rrx)
        dphit[:, 0, 14] = div4*(-2*ssx)*(1+ttx)*(1+rrx)
        dphit[:, 0, 15] = div4*(-1)*(1-ttx**2)*(1+rrx)
        dphit[:, 0, 16] = div4*(-1)*(1-ttx)*(1-rrx**2)
        dphit[:, 0, 17] = div4*(1)*(1-ttx)*(1-rrx**2)
        dphit[:, 0, 18] = div4*(1)*(1+ttx)*(1-rrx**2)
        dphit[:, 0, 19] = div4*(-1)*(1+ttx)*(1-rrx**2)
        #
        dphit[:, 1, 0] = div8*(1-ssx)*(1-rrx)*(-(-ssx-ttx-rrx-2)+(1-ttx)*(-1)) 
        dphit[:, 1, 1] = div8*(1+ssx)*(1-rrx)*(-(ssx-ttx-rrx-2)+(1-ttx)*(-1)) 
        dphit[:, 1, 2] = div8*(1+ssx)*(1-rrx)*(+(ssx+ttx-rrx-2)+(1+ttx)*(1)) 
        dphit[:, 1, 3] = div8*(1-ssx)*(1-rrx)*(+(-ssx+ttx-rrx-2)+(1+ttx)*(1)) 
        dphit[:, 1, 4] = div8*(1-ssx)*(1+rrx)*(-(-ssx-ttx+rrx-2)+(1-ttx)*(-1)) 
        dphit[:, 1, 5] = div8*(1+ssx)*(1+rrx)*(-(ssx-ttx+rrx-2)+(1-ttx)*(-1)) 
        dphit[:, 1, 6] = div8*(1+ssx)*(1+rrx)*(+(ssx+ttx+rrx-2)+(1+ttx)*(1)) 
        dphit[:, 1, 7] = div8*(1-ssx)*(1+rrx)*(+(-ssx+ttx+rrx-2)+(1+ttx)*(1))
        dphit[:, 1, 8] = div4*(1-ssx**2)*(-1)*(1-rrx)
        dphit[:, 1, 9] = div4*(1+ssx)*(-2*ttx)*(1-rrx)
        dphit[:, 1, 10] = div4*(1-ssx**2)*(1)*(1-rrx)
        dphit[:, 1, 11] = div4*(1-ssx)*(-2*ttx)*(1-rrx)
        dphit[:, 1, 12] = div4*(1-ssx**2)*(-1)*(1+rrx)
        dphit[:, 1, 13] = div4*(1+ssx)*(-2*ttx)*(1+rrx)
        dphit[:, 1, 14] = div4*(1-ssx**2)*(1)*(1+rrx)
        dphit[:, 1, 15] = div4*(1-ssx)*(-2*ttx)*(1+rrx)
        dphit[:, 1, 16] = div4*(1-ssx)*(-1)*(1-rrx**2)
        dphit[:, 1, 17] = div4*(1+ssx)*(-1)*(1-rrx**2)
        dphit[:, 1, 18] = div4*(1+ssx)*(1)*(1-rrx**2)
        dphit[:, 1, 19] = div4*(1-ssx)*(1)*(1-rrx**2)
        #
        dphit[:, 2, 0] = div8*(1-ssx)*(1-ttx)*(-(-ssx-ttx-rrx-2)+(1-rrx)*(-1)) 
        dphit[:, 2, 1] = div8*(1+ssx)*(1-ttx)*(-(ssx-ttx-rrx-2)+(1-rrx)*(-1)) 
        dphit[:, 2, 2] = div8*(1+ssx)*(1+ttx)*(-(ssx+ttx-rrx-2)+(1-rrx)*(-1)) 
        dphit[:, 2, 3] = div8*(1-ssx)*(1+ttx)*(-(-ssx+ttx-rrx-2)+(1-rrx)*(-1)) 
        dphit[:, 2, 4] = div8*(1-ssx)*(1-ttx)*(+(-ssx-ttx+rrx-2)+(1+rrx)*(1)) 
        dphit[:, 2, 5] = div8*(1+ssx)*(1-ttx)*(+(ssx-ttx+rrx-2)+(1+rrx)*(1)) 
        dphit[:, 2, 6] = div8*(1+ssx)*(1+ttx)*(+(ssx+ttx+rrx-2)+(1+rrx)*(1)) 
        dphit[:, 2, 7] = div8*(1-ssx)*(1+ttx)*(+(-ssx+ttx+rrx-2)+(1+rrx)*(1)) 
        dphit[:, 2, 8] = div4*(1-ssx**2)*(1-ttx)*(-1)
        dphit[:, 2, 9] = div4*(1+ssx)*(1-ttx**2)*(-1)
        dphit[:, 2, 10] = div4*(1-ssx**2)*(1+ttx)*(-1)
        dphit[:, 2, 11] = div4*(1-ssx)*(1-ttx**2)*(-1)
        dphit[:, 2, 12] = div4*(1-ssx**2)*(1-ttx)*(1)
        dphit[:, 2, 13] = div4*(1+ssx)*(1-ttx**2)*(1)
        dphit[:, 2, 14] = div4*(1-ssx**2)*(1+ttx)*(1)
        dphit[:, 2, 15] = div4*(1-ssx)*(1-ttx**2)*(1)
        dphit[:, 2, 16] = div4*(1-ssx)*(1-ttx)*(-2*rrx)
        dphit[:, 2, 17] = div4*(1+ssx)*(1-ttx)*(-2*rrx)
        dphit[:, 2, 18] = div4*(1+ssx)*(1+ttx)*(-2*rrx)
        dphit[:, 2, 19] = div4*(1-ssx)*(1+ttx)*(-2*rrx)

        self.phi = phit
        self.dphi = dphit
        # return phit, dphit


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
        """ This method returns elementary stiffness and mass matrices for HEXAHEDRON-20 nodes.
            ANSYS SOLID95 - Do not compare with new Ansys solid elements
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
            
            Ke += B[i,:,:].T@self.const_mat@B[i,:,:]*(detJAC[i,:,:]*self.wps[i])
            Me += rho*N[i,:,:].T@N[i,:,:]*(detJAC[i,:,:]*self.wps[i])
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

            phi, dphi = shapeH20(self.pint[i, 0], self.pint[i, 1], self.pint[i, 2])
            JAC = dphi@self.nodal_coordinates[ie, 1:4]
            detJAC, invJAC = get_detJAC_and_invJAC(JAC)
            dphi_t = invJAC @ dphi
            
            for iii in range(20):
                B[0,3*(iii)+0] = dphi_t[0,iii]
                B[0,3*(iii)+1] = 0.
                B[0,3*(iii)+2] = 0.
                B[1,3*(iii)+0] = 0.
                B[1,3*(iii)+1] = dphi_t[1,iii]
                B[1,3*(iii)+2] = 0.
                B[2,3*(iii)+0] = 0.
                B[2,3*(iii)+1] = 0.
                B[2,3*(iii)+2] = dphi_t[2,iii]
                B[3,3*(iii)+0] = dphi_t[1,iii]
                B[3,3*(iii)+1] = dphi_t[0,iii]
                B[3,3*(iii)+2] = 0.              
                B[4,3*(iii)+0] = dphi_t[2,iii]
                B[4,3*(iii)+1] = 0.
                B[4,3*(iii)+2] = dphi_t[0,iii]
                B[5,3*(iii)+0] = 0.
                B[5,3*(iii)+1] = dphi_t[2,iii]
                B[5,3*(iii)+2] = dphi_t[1,iii]

            for iii in range(20): 
                N[0,3*iii+0] = phi[iii]
                N[0,3*iii+1] = 0
                N[0,3*iii+2] = 0
                N[1,3*iii+0] = 0
                N[1,3*iii+1] = phi[iii]
                N[1,3*iii+2] = 0
                N[2,3*iii+0] = 0
                N[2,3*iii+1] = 0
                N[2,3*iii+2] = phi[iii]

            Ke += B.T@self.const_mat@B*(detJAC*self.wps[i])
            Me += rho*N.T@N*(detJAC*self.wps[i])
        
        return Ke, Me


    def reorder_connect(self):
        """
        """
        self.connect = self.connect[:, [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19]]
        #
        # # Connect -- Ansys ---> Gmsh
        # connect_t  = connect.copy()
        # connect_t[ee,10] = connect[ee,12]
        # connect_t[ee,11] = connect[ee,14]
        # connect_t[ee,12] = connect[ee,10]
        # connect_t[ee,13] = connect[ee,17]
        # connect_t[ee,14] = connect[ee,19]
        # connect_t[ee,15] = connect[ee,20]
        # connect_t[ee,16] = connect[ee,18]
        # connect_t[ee,17] = connect[ee,11]
        # connect_t[ee,18] = connect[ee,13]
        # connect_t[ee,19] = connect[ee,15]
        # connect_t[ee,20] = connect[ee,16]
        # connect = connect_t.copy()


    def generate_ind_rows_cols(self):
        """ This method process the dofs indices (rows and columns) to assembly of global matrices.
        """
        # processing the dofs indices (rows and columns) for assembly
        self.process_constitutive_model()
        self.reorder_connect()
        dofs, edofs = self.dof_per_node, self.dofs_per_element
        ind_dofs = (np.array([  dofs*self.connect[:,1] - 1 , dofs*self.connect[:,1] , dofs*self.connect[:,1] + 1 ,
                                dofs*self.connect[:,2] - 1 , dofs*self.connect[:,2] , dofs*self.connect[:,2] + 1 ,
                                dofs*self.connect[:,3] - 1 , dofs*self.connect[:,3] , dofs*self.connect[:,3] + 1 ,
                                dofs*self.connect[:,4] - 1 , dofs*self.connect[:,4] , dofs*self.connect[:,4] + 1 ,
                                dofs*self.connect[:,5] - 1 , dofs*self.connect[:,5] , dofs*self.connect[:,5] + 1 ,
                                dofs*self.connect[:,6] - 1 , dofs*self.connect[:,6] , dofs*self.connect[:,6] + 1 ,
                                dofs*self.connect[:,7] - 1 , dofs*self.connect[:,7] , dofs*self.connect[:,7] + 1 ,
                                dofs*self.connect[:,8] - 1 , dofs*self.connect[:,8] , dofs*self.connect[:,8] + 1 ,
                                dofs*self.connect[:,9] - 1 , dofs*self.connect[:,9] , dofs*self.connect[:,9] + 1 ,
                                dofs*self.connect[:,10] - 1, dofs*self.connect[:,10], dofs*self.connect[:,10] + 1,
                                dofs*self.connect[:,11] - 1, dofs*self.connect[:,11], dofs*self.connect[:,11] + 1,
                                dofs*self.connect[:,12] - 1, dofs*self.connect[:,12], dofs*self.connect[:,12] + 1,
                                dofs*self.connect[:,13] - 1, dofs*self.connect[:,13], dofs*self.connect[:,13] + 1,
                                dofs*self.connect[:,14] - 1, dofs*self.connect[:,14], dofs*self.connect[:,14] + 1,
                                dofs*self.connect[:,15] - 1, dofs*self.connect[:,15], dofs*self.connect[:,15] + 1,
                                dofs*self.connect[:,16] - 1, dofs*self.connect[:,16], dofs*self.connect[:,16] + 1,
                                dofs*self.connect[:,17] - 1, dofs*self.connect[:,17], dofs*self.connect[:,17] + 1,
                                dofs*self.connect[:,18] - 1, dofs*self.connect[:,18], dofs*self.connect[:,18] + 1,
                                dofs*self.connect[:,19] - 1, dofs*self.connect[:,19], dofs*self.connect[:,19] + 1,
                                dofs*self.connect[:,20] - 1, dofs*self.connect[:,20], dofs*self.connect[:,20] + 1  ], dtype=int)-2).T
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
            # print('Ke')
            # print(Ke)
            # print('Me')
            # print(Me)
            data_k[el,:] = Ke.flatten() 
            data_m[el,:] = Me.flatten() 
    
        data_k = data_k.flatten()
        data_m = data_m.flatten()
        stif_matrix = csr_matrix((data_k, (self.ind_rows, self.ind_cols)), shape=(total_dofs, total_dofs))
        mass_matrix = csr_matrix((data_m, (self.ind_rows, self.ind_cols)), shape=(total_dofs, total_dofs))

        return stif_matrix, mass_matrix