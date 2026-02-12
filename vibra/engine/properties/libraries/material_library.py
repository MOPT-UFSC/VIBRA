from __future__ import annotations

from typing import override

from vibra.engine.properties.material import Material

from .property_library import PropertyLibrary


class MaterialLibrary(PropertyLibrary[Material]):
    @override
    @classmethod
    def default(cls) -> MaterialLibrary:
        return default_material_library()


def default_material_library() -> MaterialLibrary:
    materials = [
        Material(
            name="Carbon_Steel",
            material_density=7850,
            elasticity_modulus=200e9,
            poisson_ratio=0.3,
            thermal_expansion_coefficient=1.2e-5,
            color=[170, 170, 170],  # Light Gray
        ),
        Material(
            name="Stainless_Steel",
            material_density=7750,
            elasticity_modulus=193e9,
            poisson_ratio=0.31,
            thermal_expansion_coefficient=1.7e-5,
            color=[126, 46, 31],  # Wood color
        ),
        Material(
            name="Ni-Co-Cr_Alloy",
            material_density=8220,
            elasticity_modulus=212e9,
            poisson_ratio=0.315,
            thermal_expansion_coefficient=1.2e-5,
            color=[0, 255, 255],  # Cyan
        ),
        Material(
            name="Cast_Iron",
            material_density=7200,
            elasticity_modulus=110e9,
            poisson_ratio=0.28,
            thermal_expansion_coefficient=1.1e-5,
            color=[50, 50, 50],  # Dark Grey
        ),
        Material(
            name="Aluminum",
            material_density=2770,
            elasticity_modulus=71e9,
            poisson_ratio=0.333,
            thermal_expansion_coefficient=2.3e-5,
            color=[255, 255, 255],  # White
        ),
        Material(
            name="Brass",
            material_density=8150,
            elasticity_modulus=96e9,
            poisson_ratio=0.345,
            thermal_expansion_coefficient=1.9e-5,
            color=[181, 166, 66],  # Brass color
        ),
    ]

    material_library = MaterialLibrary()
    material_library.extend(materials)
    return material_library
