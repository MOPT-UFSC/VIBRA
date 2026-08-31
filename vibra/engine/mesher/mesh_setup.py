from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

from vibra import errors
from vibra.engine.mesher.element_setup import GMSH_HEX8, GMSH_HEX20, GMSH_TET4, GMSH_TET10, ElementSetup


@dataclass
class ElementTopology:
    element_geometry: Literal["tetrahedral", "hexahedral"]
    element_order: Literal["linear", "quadratic"]


@dataclass(kw_only=True)
class MeshSetup:
    minimum_element_size: float = 0
    maximum_element_size: float = float("inf")
    geometry_tolerance: float = 1e-8
    size_factor: float = 1
    element_geometry: Literal["tetrahedral", "hexahedral"] = "tetrahedral"
    element_order: Literal["linear", "quadratic"] = "linear"

    compute_quality_metrics: bool = False
    merge_connected_volumes: bool = True
    disconnected_surfaces: list[int] = field(default_factory=list)

    # Advanced stuff
    local_mesh_size_control_parameters: list[LocalMeshSizeControlSetup] = field(default_factory=list)
    custom_element_setup: Optional[ElementSetup] = None
    random_seed: int = 1234

    def __post_init__(self):
        if self.maximum_element_size < self.minimum_element_size:
            msg = "The minimum element size should not surpass the maximum element size."
            raise errors.InvalidMeshSetupError(msg)

    @property
    def element_topology(self):
        return ElementTopology(self.element_geometry, self.element_order)

    @property
    def element_setup(self) -> ElementSetup:
        if self.custom_element_setup is not None:
            return self.custom_element_setup

        match self.element_geometry, self.element_order:
            case "tetrahedral", "linear":
                return GMSH_TET4
            case "tetrahedral", "quadratic":
                return GMSH_TET10
            case "hexahedral", "linear":
                return GMSH_HEX8
            case "hexahedral", "quadratic":
                return GMSH_HEX20
            case _:
                raise NotImplementedError("Invalid element type or shape function!")


@dataclass
class LocalMeshSizeControlSetup:
    entity_type: Literal["lines", "surfaces", "volumes"]
    element_size: float
    entity_ids: list[int]

    def as_dict(self) -> dict:
        return {
            "entity_type": self.entity_type,
            "element_size": self.element_size,
            "entity_ids": self.entity_ids,
        }
    
    def remove_ids(self, ids: list[int], entity_type: str):
        if entity_type == self.entity_type:
            self.entity_ids = list(set(self.entity_ids) - set(ids))
    
    def is_empty(self) -> bool:
        return len(self.entity_ids) == 0


TETRAHEDRON_4 = ElementTopology("tetrahedral", "linear")
TETRAHEDRON_10 = ElementTopology("tetrahedral", "quadratic")
HEXAHEDRON_8 = ElementTopology("hexahedral", "linear")
HEXAHEDRON_20 = ElementTopology("hexahedral", "quadratic")
DEFAULT_ELEMENT_TYPE = TETRAHEDRON_4
