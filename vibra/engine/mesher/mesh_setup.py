from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

from vibra import errors
from vibra.engine.mesher.element_setup import (
    HEXAHEDRON_8,
    HEXAHEDRON_20,
    TETRAHEDRON_4,
    TETRAHEDRON_10,
    ElementSetup,
)


@dataclass(kw_only=True)
class MeshSetup:
    minimum_element_size: float = 0
    maximum_element_size: float = float("inf")
    geometry_tolerance: float = 1e-6
    size_factor: float = 1
    element_type: Literal["tetrahedral", "hexahedral"] = "tetrahedral"
    shape_function: Literal["linear", "quadratic"] = "linear"

    compute_quality_metrics: bool = False
    merge_connected_volumes: bool = False

    # Advanced stuff
    refinement_parameters: list[MeshRefinementSetup] = field(default_factory=list)
    custom_element_setup: Optional[ElementSetup] = None
    random_seed: int = 1234

    def __post_init__(self):
        if self.maximum_element_size < self.minimum_element_size:
            msg = "The minimum element size should not surpass the maximum element size."
            raise errors.InvalidMeshSetupError(msg)

    @property
    def element_setup(self) -> ElementSetup:
        if self.custom_element_setup is not None:
            return self.custom_element_setup

        match self.element_type, self.shape_function:
            case "tetrahedral", "linear":
                return TETRAHEDRON_4
            case "tetrahedral", "quadratic":
                return TETRAHEDRON_10
            case "hexahedral", "linear":
                return HEXAHEDRON_8
            case "hexahedral", "quadratic":
                return HEXAHEDRON_20
            case _:
                raise NotImplementedError("Invalid element type or shape function!")

    def as_dict(self) -> dict:
        return {
            "element_type": self.element_type,
            "shape_function": self.shape_function,
            "minimum_element_size": self.minimum_element_size,
            "maximum_element_size": self.maximum_element_size,
            "geometry_tolerance": self.geometry_tolerance,
            "mesh_connections": self.mesh_connections,
            "mesh_quality_metrics": self.mesh_quality_metrics,
            "mesh_refinement_parameters": [
                (i.entity_type, i.element_size, i.entity_ids) 
                for i in self.refinement_parameters
            ],
            "size_factor": self.size_factor,
        }  # fmt: skip


@dataclass
class MeshRefinementSetup:
    entity_type: Literal["lines", "surfaces", "volumes"]
    entity_ids: list[int]
    element_size: float

    def as_dict(self) -> dict:
        return {
            "entity_type": self.entity_type,
            "entity_ids": self.entity_ids,
            "element_size": self.element_size,
        }
