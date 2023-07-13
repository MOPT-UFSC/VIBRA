from vibra.engine.assemblers.modal_assembler import ModalAssembler

from vibra.engine.elements.structural_tet4_element import STRUCT_TETRAHEDRON_4S
from vibra.engine.elements.structural_tet10_element import STRUCT_TETRAHEDRON_10S
from vibra.engine.elements.structural_hex8_element import STRUCT_HEXAHEDRON_8
from vibra.engine.elements.structural_hex20_element import STRUCT_HEXAHEDRON_20

from vibra.engine.mesher.element_type import *


class StructuralModalAssembler(ModalAssembler):
    pass
    def new_element(self):
        element_type = self.model.mesh.element_type

        if element_type == TETRAHEDRON_4:
            return STRUCT_TETRAHEDRON_4S(self.model)
        elif element_type == TETRAHEDRON_10:
            return STRUCT_TETRAHEDRON_10S(self.model)
        elif element_type == HEXAHEDRON_8:
            return STRUCT_HEXAHEDRON_8(self.model)
        elif element_type == HEXAHEDRON_20:
            return STRUCT_HEXAHEDRON_20(self.model)
        else:
            raise NotImplementedError(f"Element type is not supported yet.")