from dataclasses import dataclass
from enum import StrEnum


class ElementTopology(StrEnum):
    HEX_8 = "hexahedral_8"
    HEX_20 = "hexahedral_20"
    TET_4 = "tetrahedral_4"
    TET_10 = "tetrahedral_10"


@dataclass
class ElementType:
    element_geometry: str
    element_order: str

    def get_element_topology(self):
        match self.element_geometry, self.element_order:
            case "tetrahedral", "linear":
                return ElementTopology.TET_4
            case "tetrahedral", "quadratic":
                return ElementTopology.TET_10
            case "hexahedral", "linear":
                return ElementTopology.HEX_8
            case "hexahedral", "quadratic":
                return ElementTopology.HEX_20
            case _:
                raise NotImplementedError("Invalid element type or shape function!")


TETRAHEDRON_4 = ElementType("tetrahedral", "linear")
TETRAHEDRON_10 = ElementType("tetrahedral", "quadratic")
HEXAHEDRON_8 = ElementType("hexahedral", "linear")
HEXAHEDRON_20 = ElementType("hexahedral", "quadratic")
DEFAULT_ELEMENT_TYPE = TETRAHEDRON_4
