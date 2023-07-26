from vibra.engine.assemblers.modal_assembler import ModalAssembler

from vibra.engine.elements.acoustic_tet4_element import ACT_TETRAHEDRON_4C
from vibra.engine.elements.acoustic_tet10_element import ACT_TETRAHEDRON_10C
from vibra.engine.elements.acoustic_hex8_element import ACT_HEXAHEDRON_8C
from vibra.engine.elements.acoustic_hex20_element import ACT_HEXAHEDRON_20C

from vibra.engine.mesher.element_type import *


class AcousticModalAssembler(ModalAssembler):
    def new_element(self):
        
        element_type = self.model.mesh.element_type

        if element_type == TETRAHEDRON_4:
            return ACT_TETRAHEDRON_4C(self.model)
        elif element_type == TETRAHEDRON_10:
            return ACT_TETRAHEDRON_10C(self.model)
        elif element_type == HEXAHEDRON_8:
            return ACT_HEXAHEDRON_8C(self.model)
        elif element_type == HEXAHEDRON_20:
            return ACT_HEXAHEDRON_20C(self.model)
        else:
            raise NotImplementedError(f"Element type is not supported yet.")