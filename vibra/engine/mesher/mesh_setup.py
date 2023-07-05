from dataclasses import dataclass
from vibra.engine.mesher.element_type import ElementType


@dataclass
class MeshSetup:
    element_type: ElementType
    geometry_tolerance: float
    size_factor: float
    minimum_element_size: float
    maximum_element_size: float
