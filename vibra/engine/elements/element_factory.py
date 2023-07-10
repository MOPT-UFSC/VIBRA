from vibra.engine.mesher.element_type import TETRAHEDRON_4, TETRAHEDRON_10, HEXAHEDRON_8, HEXAHEDRON_20
from vibra.engine.elements.acoustic_tet4_element import ACT_TETRAHEDRON_4C


def new_element(model):
    '''
    This class is meant to figure out the element that should
    be used based on the mesh already created.
    '''
    
    element_type = model.mesh.element_type

    if element_type == TETRAHEDRON_4:
        return ACT_TETRAHEDRON_4C(model)
    else:
        raise NotImplementedError(f"Element type is not supported yet.")
    
    # elif element_type == TETRAHEDRON_10:
    #     return None
    # elif element_type == HEXAHEDRON_8:
    #     return None
    # elif element_type == HEXAHEDRON_20:
    #     return None