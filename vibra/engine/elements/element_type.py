from dataclasses import dataclass
from enum import StrEnum


class ElementTopology(StrEnum):
    HEXAHEDRON_8 = "hexahedral_8"
    HEXAHEDRON_20 = "hexahedral_20"
    TETRAHEDRON_4 = "tetrahedral_4"
    TETRAHEDRON_10 = "tetrahedral_10"


@dataclass
class ElementType:
    element_geometry: str
    element_order: str

    @property
    def get_element(self):
        match self.element_geometry, self.element_order:
            case "tetrahedral", "linear":
                return ElementTopology.TETRAHEDRON_4
            case "tetrahedral", "quadratic":
                return ElementTopology.TETRAHEDRON_10
            case "hexahedral", "linear":
                return ElementTopology.HEXAHEDRON_8
            case "hexahedral", "quadratic":
                return ElementTopology.HEXAHEDRON_20
            case _:
                raise NotImplementedError("Invalid element type or shape function!")
