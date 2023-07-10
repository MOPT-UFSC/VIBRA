from dataclasses import dataclass

from vibra.engine.mesher.element_type import DEFAULT_ELEMENT_TYPE, ElementType


@dataclass
class MeshSetup:
    element_type: ElementType
    geometry_tolerance: float
    size_factor: float
    minimum_element_size: float
    maximum_element_size: float


AUTO_MESH_SETUP = MeshSetup(
    element_type=DEFAULT_ELEMENT_TYPE,
    geometry_tolerance=1e-6,
    size_factor=0.1,
    minimum_element_size=0,
    maximum_element_size=0,
)
