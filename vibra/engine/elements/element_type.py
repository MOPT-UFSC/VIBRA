from dataclasses import dataclass

from enum import StrEnum

class Element(StrEnum):
    HEXAHEDRAL_8 = "hexahedral_8"
    HEXAHEDRAL_20 = "hexahedral_20"
    TETRAHEDRAL_4 = "tetrahedral_4"
    TETRAHEDRAL_10 = "tetrahedral_10"

@dataclass
class ElementType:
    element_type: str
    shape_function: str

    @property
    def get_element_type(self):
        match self.element_type, self.shape_function:
            case "tetrahedral", "linear":
                return Element.TETRAHEDRAL_4
            case "tetrahedral", "quadratic":
                return Element.TETRAHEDRAL_10
            case "hexahedral", "linear":
                return Element.HEXAHEDRAL_8
            case "hexahedral", "quadratic":
                return Element.HEXAHEDRAL_20
            case _:
                raise NotImplementedError("Invalid element type or shape function!")
